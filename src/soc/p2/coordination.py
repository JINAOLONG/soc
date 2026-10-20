"""Single-host SQLite A_NO_TAKEOVER authority primitives.

Only a trusted coordinator may access this database. These primitives do not
establish filesystem durability, isolate workers, or confer science permission.
"""
from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
from typing import Callable

from soc.p2.identity import EvidenceError, digest, semantic_bytes

TERMINAL = {'PUBLISHED', 'HALTED', 'FAILED', 'INCOMPLETE'}
NEXT = {'PREPARED': 'SPAWN_RESERVED', 'SPAWN_RESERVED': 'RUNNING',
        'RUNNING': 'OUTPUT_READY', 'OUTPUT_READY': 'VERIFIED', 'VERIFIED': 'PUBLISHED'}
PURPOSES = {'INPUT_GENERATION', 'PRIMARY_EXECUTION', 'REGISTERED_REPLAY'}


class SQLiteAuthority:
    def __init__(self, path: Path, clock: Callable[[], int], clock_id: str):
        if not clock_id:
            raise EvidenceError('unknown clock identity')
        self.clock, self.clock_id = clock, clock_id
        self.last_tick = None
        self.db = sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.execute('PRAGMA journal_mode=DELETE')
        self.db.execute('PRAGMA synchronous=EXTRA')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS scopes(
            scientific_tuple TEXT PRIMARY KEY, scope TEXT UNIQUE NOT NULL, body BLOB NOT NULL);
          CREATE TABLE IF NOT EXISTS domains(
            domain TEXT PRIMARY KEY, scope TEXT NOT NULL, purpose TEXT NOT NULL,
            target TEXT NOT NULL, current_sha TEXT NOT NULL,
            UNIQUE(scope,purpose,target));
          CREATE TABLE IF NOT EXISTS history(
            sha TEXT PRIMARY KEY, domain TEXT NOT NULL, revision INTEGER NOT NULL,
            body BLOB NOT NULL, UNIQUE(domain,revision));
          CREATE TABLE IF NOT EXISTS admissions(domain TEXT PRIMARY KEY, attempt TEXT NOT NULL);
        ''')

    def close(self):
        self.db.close()

    def _tick(self):
        value=self.clock()
        if type(value) is not int or value < 0 or (self.last_tick is not None and value < self.last_tick):
            raise EvidenceError('unknown/reversed authority clock')
        self.last_tick=value
        return value

    @contextmanager
    def transaction(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            yield
            self.db.execute('COMMIT')
        except BaseException:
            self.db.execute('ROLLBACK')
            raise

    def register_scope(self, blueprint: str, matrix: str, calibration: str, root_authorization: str) -> str:
        body = dict(namespace='soc.p2.budget-scope.v3', schema_version=3,
                    blueprint_sha256=blueprint, matrix_sha256=matrix,
                    calibration_metadata_sha256=calibration, root_authorization_sha256=root_authorization)
        for sha in (blueprint, matrix, calibration, root_authorization):
            if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
                raise EvidenceError('invalid scope digest')
        raw = semantic_bytes(body)
        scope = digest(raw)
        key = digest(semantic_bytes([blueprint, matrix, calibration]))
        with self.transaction():
            old = self.db.execute('SELECT scope,body FROM scopes WHERE scientific_tuple=?', (key,)).fetchone()
            if old and (old[0] != scope or bytes(old[1]) != raw):
                raise EvidenceError('new authorization cannot create a second budget')
            if not old:
                self.db.execute('INSERT INTO scopes VALUES(?,?,?)', (key, scope, raw))
        return scope

    def _record(self, domain):
        row = self.db.execute('SELECT h.sha,h.body FROM domains d JOIN history h ON h.sha=d.current_sha WHERE d.domain=?',
                              (domain,)).fetchone()
        if not row or digest(bytes(row[1])) != row[0]:
            raise EvidenceError('missing/corrupt authority record')
        return row[0], json.loads(row[1])

    def read(self, domain) -> tuple[str, dict]:
        # All authoritative reads share the writer serialization point.
        with self.transaction():
            return self._record(domain)

    def _append(self, body):
        raw = semantic_bytes(body)
        sha = digest(raw)
        self.db.execute('INSERT INTO history VALUES(?,?,?,?)',
                        (sha, body['domain_sha256'], body['revision'], raw))
        self.db.execute('UPDATE domains SET current_sha=? WHERE domain=?', (sha, body['domain_sha256']))
        return sha, body

    def prepare(self, scope: str, purpose: str, target: str, owner: str, authorization: str,
                attempt: str, deadline: int):
        if purpose not in PURPOSES or not all(type(x) is str and x and x.isascii() for x in (target, owner, attempt)):
            raise EvidenceError('invalid domain identity')
        if type(deadline) is not int or deadline <= self._tick():
            raise EvidenceError('explicit future lease deadline required')
        domain = digest(semantic_bytes(dict(namespace='soc.p2.coordination-domain.v3', schema_version=3,
                            budget_scope_sha256=scope, purpose=purpose, semantic_target_id=target)))
        with self.transaction():
            scoped = self.db.execute('SELECT body FROM scopes WHERE scope=?', (scope,)).fetchone()
            if not scoped or json.loads(scoped[0])['root_authorization_sha256'] != authorization:
                raise EvidenceError('unregistered budget/root authorization')
            if self.db.execute('SELECT 1 FROM domains WHERE domain=?', (domain,)).fetchone():
                raise EvidenceError('domain already exists; no replacement owner')
            count = self.db.execute('SELECT count(*) FROM domains WHERE scope=? AND purpose=?', (scope,purpose)).fetchone()[0]
            if count >= (1080 if purpose == 'INPUT_GENERATION' else 2520):
                raise EvidenceError('registered purpose budget exhausted')
            body = dict(namespace='soc.p2.coordination-record.v3', schema_version=3,
                        domain_sha256=domain, policy='A_NO_TAKEOVER', revision=0,
                        parent_record_sha256=None, active_authorization_sha256=authorization,
                        owner_id=owner, epoch=0, lease_clock_id=self.clock_id,
                        lease_deadline_ticks=deadline, phase='PREPARED', spawn_reserved_ever=False,
                        original_attempt_id=attempt, inventory_sha256=None, receipt_sha256=None,
                        recovery_authorization_sha256=None)
            raw = semantic_bytes(body)
            sha = digest(raw)
            self.db.execute('INSERT INTO domains VALUES(?,?,?,?,?)', (domain, scope, purpose, target, sha))
            self.db.execute('INSERT INTO history VALUES(?,?,?,?)', (sha, domain, 0, raw))
        return sha, body

    def _current(self, domain, expected, owner, authorization):
        sha, row = self._record(domain)
        if sha != expected or row['owner_id'] != owner or row['active_authorization_sha256'] != authorization or row['epoch'] != 0:
            raise EvidenceError('stale pointer/owner/authorization')
        if row['phase'] in TERMINAL:
            raise EvidenceError('terminal record is immutable')
        return sha, row

    def _expired(self, row):
        if row['lease_clock_id'] != self.clock_id: return True
        try: tick=self._tick()
        except EvidenceError: return True
        return tick >= row['lease_deadline_ticks']

    def transition(self, domain, expected, owner, authorization, phase, *, inventory=None,
                   receipt=None, checked=False, recovery_authorization=None):
        expired = False
        with self.transaction():
            sha, row = self._current(domain, expected, owner, authorization)
            if self._expired(row):
                phase, expired = 'HALTED', True
            elif phase not in {'HALTED', 'FAILED', 'INCOMPLETE'} and NEXT.get(row['phase']) != phase:
                raise EvidenceError('illegal phase transition')
            if not expired:
                if phase == 'RUNNING' and not self.db.execute('SELECT 1 FROM admissions WHERE domain=?', (domain,)).fetchone():
                    raise EvidenceError('trusted one-use admission required')
                if phase in {'OUTPUT_READY', 'VERIFIED', 'PUBLISHED'} and not checked:
                    raise EvidenceError('missing authority acceptance predicates')
                if phase in {'OUTPUT_READY', 'VERIFIED'} and not inventory:
                    raise EvidenceError('missing inventory')
                if phase == 'PUBLISHED' and (not receipt or not inventory or inventory != row['inventory_sha256']):
                    raise EvidenceError('A2 publication inventory/receipt mismatch')
                if phase != 'PUBLISHED' and receipt is not None:
                    raise EvidenceError('receipt belongs to published record only')
            update = {**row, 'revision': row['revision']+1, 'parent_record_sha256': sha, 'phase': phase}
            if phase == 'SPAWN_RESERVED': update['spawn_reserved_ever'] = True
            if not expired:
                if inventory is not None: update['inventory_sha256'] = inventory
                if receipt is not None: update['receipt_sha256'] = receipt
                if recovery_authorization is not None: update['recovery_authorization_sha256'] = recovery_authorization
            result = self._append(update)
        if expired:
            raise EvidenceError('lease/clock invalid; permanently HALTED')
        return result

    def claim_admission(self, domain, expected, owner, authorization):
        expired = False
        with self.transaction():
            sha, row = self._current(domain, expected, owner, authorization)
            if self._expired(row):
                self._append({**row, 'phase': 'HALTED', 'parent_record_sha256': sha, 'revision': row['revision']+1})
                expired = True
            else:
                if row['phase'] != 'SPAWN_RESERVED' or not row['spawn_reserved_ever']:
                    raise EvidenceError('durable reservation required')
                try:
                    self.db.execute('INSERT INTO admissions VALUES(?,?)', (domain, row['original_attempt_id']))
                except sqlite3.IntegrityError as exc:
                    raise EvidenceError('admission already consumed; unknown start never retries') from exc
        if expired:
            raise EvidenceError('invalid lease at admission; HALTED')

    def renew(self, domain, expected, owner, authorization, deadline, *, explicitly_preauthorized=False):
        if not explicitly_preauthorized or type(deadline) is not int:
            raise EvidenceError('renewal not authorized')
        expired = False
        with self.transaction():
            sha, row = self._current(domain, expected, owner, authorization)
            if self._expired(row):
                row = {**row, 'phase': 'HALTED'}
                expired = True
            elif deadline <= max(self._tick(), row['lease_deadline_ticks']):
                raise EvidenceError('renewal must extend original valid lease')
            else:
                row = {**row, 'lease_deadline_ticks': deadline}
            result = self._append({**row, 'revision': row['revision']+1, 'parent_record_sha256': sha})
        if expired: raise EvidenceError('expired lease cannot renew')
        return result


def verify_publication(store, previous_ref, receipt_ref, inventory_ref, published_ref):
    """A2 byte/identity closure only; authority authenticity needs backend evidence."""
    r_raw, p_raw = store.get(previous_ref), store.get(published_ref)
    r, p = json.loads(r_raw), json.loads(p_raw)
    q_raw, i_raw = store.get(receipt_ref), store.get(inventory_ref)
    if r['phase'] != 'VERIFIED' or p['phase'] != 'PUBLISHED' or p['parent_record_sha256'] != digest(r_raw) or p['revision'] != r['revision']+1:
        raise EvidenceError('A2 verified/published chain mismatch')
    if p['receipt_sha256'] != digest(q_raw) or p['inventory_sha256'] != digest(i_raw) or r['inventory_sha256'] != digest(i_raw):
        raise EvidenceError('A2 inventory/completion mismatch')
    for key in ('domain_sha256', 'policy', 'owner_id', 'active_authorization_sha256', 'epoch',
                'lease_clock_id', 'original_attempt_id', 'spawn_reserved_ever'):
        if r[key] != p[key]: raise EvidenceError('A2 immutable field changed: '+key)
    if r['receipt_sha256'] is not None:
        raise EvidenceError('VERIFIED cannot prefill future receipt')
    q = json.loads(q_raw)
    if 'artifact_inventory_sha256' in q and q['artifact_inventory_sha256'] != digest(i_raw):
        raise EvidenceError('primary completion inventory mismatch')
    refs = json.loads(i_raw)
    forbidden = {previous_ref['path'], receipt_ref['path'], inventory_ref['path'], published_ref['path']}
    if type(refs) is not list or len({x['path'] for x in refs}) != len(refs):
        raise EvidenceError('invalid inventory membership')
    for ref in refs:
        if ref['path'] in forbidden: raise EvidenceError('cyclic inventory')
        store.get(ref)
    return {'binding': 'MATCH', 'authority_authenticity': 'NOT_ESTABLISHED_BY_HASHES'}

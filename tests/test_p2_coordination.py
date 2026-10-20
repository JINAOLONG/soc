import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

from soc.p2.coordination import SQLiteAuthority, verify_publication
from soc.p2.identity import ArtifactStore, EvidenceError, Types, digest, semantic_bytes

ROOT=Path(__file__).resolve().parents[1]


class P2CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'authority.sqlite'
        self.tick=10
        self.a=SQLiteAuthority(self.path,lambda:self.tick,'HAND-BOOT/INSTANCE')
        self.scope=self.a.register_scope('1'*64,'2'*64,'3'*64,'4'*64)
        self.sha,self.row=self.a.prepare(self.scope,'PRIMARY_EXECUTION','hand-trial','hand-owner','4'*64,'hand-attempt',100)
        self.domain=self.row['domain_sha256']

    def tearDown(self):
        self.a.close();self.temp.cleanup()

    def move(self,phase,**kw):
        self.sha,self.row=self.a.transition(self.domain,self.sha,'hand-owner','4'*64,phase,**kw)

    def test_closed_record_and_one_root(self):
        Types(ROOT/'docs/P2_design/v3/P2_typed_identity_schema_v3.json').validate('COORDINATION_RECORD_V3',self.row)
        self.assertEqual(self.scope,self.a.register_scope('1'*64,'2'*64,'3'*64,'4'*64))
        with self.assertRaises(EvidenceError):self.a.register_scope('1'*64,'2'*64,'3'*64,'5'*64)

    def test_domain_cannot_change_owner_auth_or_recreate(self):
        with self.assertRaises(EvidenceError):self.a.prepare(self.scope,'PRIMARY_EXECUTION','hand-trial','new-owner','4'*64,'new-attempt',100)
        with self.assertRaises(EvidenceError):self.a.transition(self.domain,self.sha,'new-owner','4'*64,'SPAWN_RESERVED')
        with self.assertRaises(EvidenceError):self.a.transition(self.domain,self.sha,'hand-owner','5'*64,'SPAWN_RESERVED')

    def test_reservation_admission_and_duplicate_rejection(self):
        with self.assertRaises(EvidenceError):self.a.claim_admission(self.domain,self.sha,'hand-owner','4'*64)
        self.move('SPAWN_RESERVED')
        self.assertTrue(self.row['spawn_reserved_ever'])
        self.a.claim_admission(self.domain,self.sha,'hand-owner','4'*64)
        with self.assertRaises(EvidenceError):self.a.claim_admission(self.domain,self.sha,'hand-owner','4'*64)
        self.move('RUNNING')
        with self.assertRaises(EvidenceError):self.move('PREPARED')

    def test_expiry_commits_halt_and_does_not_refund(self):
        self.move('SPAWN_RESERVED');self.tick=100
        with self.assertRaises(EvidenceError):self.a.claim_admission(self.domain,self.sha,'hand-owner','4'*64)
        sha,row=self.a.read(self.domain)
        self.assertEqual(row['phase'],'HALTED')
        self.assertTrue(row['spawn_reserved_ever'])
        with self.assertRaises(EvidenceError):self.a.transition(self.domain,sha,'hand-owner','4'*64,'PREPARED')

    def test_clock_change_blocks_not_inferred_takeover(self):
        self.a.clock_id='DIFFERENT-BOOT'
        with self.assertRaises(EvidenceError):self.move('SPAWN_RESERVED')
        self.assertEqual(self.a.read(self.domain)[1]['phase'],'HALTED')

    def test_reversed_clock_blocks_admission(self):
        self.move('SPAWN_RESERVED');self.tick=9
        with self.assertRaises(EvidenceError):self.a.claim_admission(self.domain,self.sha,'hand-owner','4'*64)
        self.assertEqual(self.a.read(self.domain)[1]['phase'],'HALTED')

    def test_renewal_only_explicit_before_expiry(self):
        with self.assertRaises(EvidenceError):self.a.renew(self.domain,self.sha,'hand-owner','4'*64,200)
        self.sha,self.row=self.a.renew(self.domain,self.sha,'hand-owner','4'*64,200,explicitly_preauthorized=True)
        self.assertEqual(self.row['epoch'],0)
        self.assertFalse(self.row['spawn_reserved_ever'])
        self.tick=200
        with self.assertRaises(EvidenceError):self.a.renew(self.domain,self.sha,'hand-owner','4'*64,300,explicitly_preauthorized=True)
        self.assertEqual(self.a.read(self.domain)[1]['phase'],'HALTED')

    def test_exact_cas_race_has_one_winner(self):
        replies=[]
        expected=self.sha
        def contender():
            authority=SQLiteAuthority(self.path,lambda:10,'HAND-BOOT/INSTANCE')
            try:
                authority.transition(self.domain,expected,'hand-owner','4'*64,'SPAWN_RESERVED')
                replies.append('APPLIED')
            except EvidenceError:replies.append('REJECTED')
            finally:authority.close()
        threads=[threading.Thread(target=contender) for _ in range(2)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertCountEqual(replies,['APPLIED','REJECTED'])

    def test_crash_after_admission_is_not_restart_permission(self):
        self.move('SPAWN_RESERVED')
        command=[sys.executable,'-B','-c',
                 'import os,sys;from pathlib import Path;from soc.p2.coordination import SQLiteAuthority;'
                 'a=SQLiteAuthority(Path(sys.argv[1]),lambda:10,"HAND-BOOT/INSTANCE");'
                 'a.claim_admission(sys.argv[2],sys.argv[3],"hand-owner","4"*64);os._exit(23)',
                 str(self.path),self.domain,self.sha]
        result=subprocess.run(command,capture_output=True)
        self.assertEqual(result.returncode,23,result.stderr)
        with self.assertRaises(EvidenceError):self.a.claim_admission(self.domain,self.sha,'hand-owner','4'*64)

    def test_terminal_history_survives_reopen(self):
        self.move('SPAWN_RESERVED');self.move('INCOMPLETE')
        self.a.close();self.a=SQLiteAuthority(self.path,lambda:10,'HAND-BOOT/INSTANCE')
        self.assertEqual(self.a.read(self.domain)[1]['phase'],'INCOMPLETE')
        self.assertEqual(self.a.db.execute('SELECT count(*) FROM history').fetchone()[0],3)
        with self.assertRaises(EvidenceError):self.move('PREPARED')

    def test_publication_requires_registered_replay_acceptance_predicates(self):
        self.move('SPAWN_RESERVED');self.a.claim_admission(self.domain,self.sha,'hand-owner','4'*64);self.move('RUNNING')
        with self.assertRaises(EvidenceError):self.move('OUTPUT_READY',inventory='a'*64)
        self.move('OUTPUT_READY',inventory='a'*64,checked=True)
        with self.assertRaises(EvidenceError):self.move('PUBLISHED',inventory='a'*64,receipt='b'*64,checked=True)
        self.move('VERIFIED',inventory='a'*64,checked=True)
        with self.assertRaises(EvidenceError):self.move('PUBLISHED',inventory='c'*64,receipt='b'*64,checked=True)
        self.move('PUBLISHED',inventory='a'*64,receipt='b'*64,checked=True)
        with self.assertRaises(EvidenceError):self.move('HALTED')

    def test_a2_external_binding_and_tamper(self):
        store=ArtifactStore(Path(self.temp.name)/'artifacts')
        raw=store.put('raw.json',b'{"hand":1}\n')
        inventory=store.inventory([raw])
        r={**self.row,'phase':'VERIFIED','inventory_sha256':inventory['sha256']}
        r_ref=store.put('verified.json',semantic_bytes(r))
        q_ref=store.put('complete.json',semantic_bytes({'artifact_inventory_sha256':inventory['sha256']}))
        p={**r,'revision':r['revision']+1,'phase':'PUBLISHED','parent_record_sha256':r_ref['sha256'],
           'receipt_sha256':q_ref['sha256']}
        p_ref=store.put('published.json',semantic_bytes(p))
        result=verify_publication(store,r_ref,q_ref,inventory,p_ref)
        self.assertEqual(result['binding'],'MATCH')
        self.assertEqual(result['authority_authenticity'],'NOT_ESTABLISHED_BY_HASHES')
        bad=store.put('bad.json',semantic_bytes({**p,'owner_id':'new-owner'}))
        with self.assertRaises(EvidenceError):verify_publication(store,r_ref,q_ref,inventory,bad)

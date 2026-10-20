"""Registered aggregation primitives. Never compute scientific results on import."""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
from itertools import product

from soc.p2.identity import EvidenceError, semantic_bytes


def percentile(values, probability: F) -> F:
    values = sorted(F(v) for v in values)
    if not values or not 0 <= probability <= 1:
        raise EvidenceError('invalid type7 input')
    h = (len(values)-1)*probability
    lo = h.numerator//h.denominator
    return values[lo]+(h-lo)*(values[min(lo+1, len(values)-1)]-values[lo])


def registered_indices(permit):
    permit.authorize_analysis('REGISTERED_BOOTSTRAP_INDICES')
    limit = 18446744073709551610
    for replicate in range(10000):
        vector = []
        for position in range(10):
            counter = 0
            while True:
                key = dict(domain='soc.p2.analysis.bootstrap.v1', analysis_seed=20261018,
                           replicate=replicate, position=position, counter=counter)
                q = int.from_bytes(hashlib.sha256(semantic_bytes(key)).digest()[:8], 'big')
                if q < limit:
                    vector.append(q % 10)
                    break
                counter += 1
        yield vector


def paired_means(conditions: dict[str, list[F]], vectors: list[list[int]]) -> dict:
    """Same index vector across conditions; fixture vectors may be hand specified."""
    if not conditions or any(len(v) != 10 for v in conditions.values()) or not vectors:
        raise EvidenceError('paired ten-seed data/indices required')
    samples = {c: [] for c in conditions}
    macro = []
    for vector in vectors:
        if len(vector) != 10 or any(type(i) is not int or not 0 <= i < 10 for i in vector):
            raise EvidenceError('invalid paired index vector')
        means = {c: sum((F(values[i]) for i in vector), F(0))/10 for c, values in conditions.items()}
        for c, v in means.items(): samples[c].append(v)
        macro.append(sum(means.values(), F(0))/len(means))
    def ci(values):
        return percentile(values, F(1, 40)), percentile(values, F(39, 40))
    return {'conditions': {c: ci(v) for c, v in samples.items()}, 'macro': ci(macro)}


def classify_opportunity(cells: dict, intervals: dict, *, evidence_complete: bool,
                         m2_valid: bool, evaluated=True) -> str:
    """COARSE and B1 only. Caller must independently validate source evidence."""
    if not evaluated: return 'NOT_EVALUATED'
    if (not evidence_complete or not m2_valid or len(cells) != 12 or set(cells) != set(intervals)
            or any(len(v) != 10 for v in cells.values())):
        return 'INCONCLUSIVE'
    p, coverage = {}, []
    for condition, rows in cells.items():
        p[condition] = []
        for e, f, hits in rows:
            if any(type(v) is not int for v in (e, f, hits)) or not 0 <= hits <= f <= e:
                raise EvidenceError('invalid denominator counts')
            if not e or not f: return 'INCONCLUSIVE'
            coverage.append(F(f, e))
            p[condition].append(F(hits, f))
    for c, ci in intervals.items():
        if len(ci) != 2 or not 0 <= F(ci[0]) <= F(ci[1]) <= 1:
            raise EvidenceError('invalid opportunity interval')
    cutoff = F(1, 20)
    if min(coverage) >= F(4, 5) and all(F(intervals[c][0]) >= cutoff and
                       sum(x >= cutoff for x in p[c]) >= 8 for c in cells):
        return 'SUPPORTED'
    if all(x == 1 for x in coverage) and all(F(intervals[c][1]) < cutoff and
                       sum(x >= cutoff for x in p[c]) <= 2 for c in cells):
        return 'NOT_SUPPORTED'
    return 'INCONCLUSIVE'


def count_opportunities(records: list[dict]) -> tuple[int,int,int]:
    from soc.p2.identity import fraction
    e=f=hits=0
    for record in records:
        status=record['status']
        if status=='NOT_IN_SCOPE':continue
        if status=='COVERAGE_INSUFFICIENT':
            e+=1;continue
        if status!='FULL':raise EvidenceError('invalid/missing diagnostic evidence')
        gain=fraction(record['gain'])
        if not 0<=gain<=1:raise EvidenceError('invalid gain')
        e+=1;f+=1;hits+=gain>=F(1,20)
    return e,f,hits


def exact_m2_pairs(rows: list[dict], expected: set[tuple]) -> list[dict]:
    """Verify exact roster and original same-workload identities before contrasts.

    Intermediate rows are internal inputs, not a replacement scientific schema.
    Required source raw refs must already have been verified by the caller.
    """
    seen, result = set(), []
    for row in rows:
        key = tuple(row[k] for k in ('condition_id', 'seed', 'config_id', 'method', 'reference', 'workload_id'))
        if key not in expected or key in seen or row['reference'] != 'B2' or row['method'] not in {'B1', 'B3', 'B4', 'B5'}:
            raise EvidenceError('unexpected/duplicate M2 pair')
        seen.add(key)
        a, b = row['method_record'], row['reference_record']
        if a['workload_sha256'] != b['workload_sha256'] or a['workload_id'] != b['workload_id'] or a['workload_id'] != row['workload_id']:
            raise EvidenceError('same seed is not same workload')
        for r in (a, b):
            if r['completion_status'] != 'COMPLETE' or r['validity'] != 'VALID' or r['groups']['H']['count'] != 50 or r['groups']['L']['count'] != 50:
                raise EvidenceError('invalid/incomplete M2 source')
        difference = {
            'H_DMR_DIFF': F(a['groups']['H']['dmr'])-F(b['groups']['H']['dmr']),
            'L_P95_DIFF': F(a['groups']['L']['p95'])-F(b['groups']['L']['p95']),
            'H_WAIT_DIFF': (F(a['H_busy_wait_sum'])-F(b['H_busy_wait_sum']))/50,
            'L_WAIT_DIFF': (F(a['L_busy_wait_sum'])-F(b['L_busy_wait_sum']))/50}
        result.append({'key': key, 'contrasts': difference})
    if seen != expected:
        raise EvidenceError('missing M2 pair')
    return result


def expected_m2_roster(selected: dict[str, str], seeds: list[str], workloads: dict) -> set[tuple]:
    if len(selected) != 18 or len(seeds) != 10 or len(set(seeds)) != 10:
        raise EvidenceError('M2 requires18 selected conditions and10 unique seeds')
    return {(c, s, selected[c], m, 'B2', workloads[c, s])
            for c, s, m in product(sorted(selected), seeds, ('B1', 'B3', 'B4', 'B5'))}

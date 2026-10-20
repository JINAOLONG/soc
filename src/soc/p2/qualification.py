"""Offline qualification, waiting decomposition and conservative RN64 bounds."""
from __future__ import annotations

from fractions import Fraction as F
import math

from soc.model.schema import Workload, communication, topological_order
from soc.p2.identity import EvidenceError


def busy_pressure(workload: Workload, executions: list[dict], window: float) -> F:
    if type(window) not in (int, float) or not math.isfinite(window) or window <= 0:
        raise EvidenceError('invalid pressure window')
    totals = []
    for resource in workload.resources:
        rows = sorted((F(r['start']), F(r['finish'])) for r in executions if r['resource'] == resource.id)
        end = F(0)
        total = F(0)
        for a, b in rows:
            if a < end or b <= a: raise EvidenceError('invalid/overlapping busy intervals')
            total += max(F(0), min(b, F(window))-max(a, F(0)))
            end = b
        totals.append(total/F(window))
    return max(totals, default=F(0))


def waiting(workload: Workload, executions: list[dict]) -> list[dict]:
    rows = {(r['service'], r['node']): r for r in executions}
    if len(rows) != len(executions) or set(rows) != {(s.id,n.id) for s in workload.services for n in s.nodes}:
        raise EvidenceError('waiting requires complete unique executions')
    result = []
    for s in workload.services:
        for n in s.nodes:
            row = rows[s.id, n.id]
            dep = max((rows[s.id, p.node]['finish'] for p in n.predecessors), default=s.arrival)
            data = max((rows[s.id, p.node]['finish']+communication(workload, rows[s.id, p.node]['resource'],
                         row['resource'], p.size) for p in n.predecessors), default=s.arrival)
            ready, start = F(data), F(row['start'])
            if start < ready: raise EvidenceError('start before data')
            intervals = sorted((max(ready, F(r['start'])), min(start, F(r['finish'])))
                               for r in executions if r['resource'] == row['resource'] and r is not row)
            busy = F(0)
            end = ready
            for a,b in intervals:
                if b > max(a,end):
                    busy += b-max(a,end)
                    end = b
            result.append(dict(service=s.id,node=n.id,group=s.group,dependency_ready=F(dep),data_ready=ready,
                               assigned_busy_wait=busy,policy_idle=start-ready-busy))
    return result


def feasibility(workload: Workload) -> dict:
    reports = {}
    for s in workload.services:
        nodes = {n.id:n for n in s.nodes}
        bound = {}
        for nid in topological_order(s):
            n = nodes[nid]
            candidates = [s.arrival]
            for edge in n.predecessors:
                pred = nodes[edge.node]
                c = min(communication(workload, p.resource, q.resource, edge.size)
                        for p in pred.durations for q in n.durations)
                candidates.append(bound[edge.node]+c)
            b = max(candidates)+min(d.realized for d in n.durations)
            if not math.isfinite(b): raise EvidenceError('nonfinite conservative bound')
            bound[nid] = b
        maximum = max(bound.values())
        reports[s.id] = dict(bound=maximum, absolute_deadline=s.deadline,
                            classification='CERTIFIED_NATURALLY_INFEASIBLE' if maximum > s.deadline
                            else 'FEASIBILITY_NOT_ESTABLISHED')
    return reports


def controls_witness(workload: Workload, executions: list[dict], required_groups: set[str]) -> bool:
    rows = {(r['service'], r['node']): r for r in executions}
    if len(rows) != len(executions) or set(rows) != {(s.id,n.id) for s in workload.services for n in s.nodes}:
        raise EvidenceError('invalid control trace membership')
    if not required_groups <= {s.group for s in workload.services}:
        raise EvidenceError('missing required control group')
    ordered = sorted(workload.services, key=lambda s:(s.arrival,s.id))
    for i,s in enumerate(ordered):
        end = max(rows[s.id,n.id]['finish'] for n in s.nodes)
        if (s.group in required_groups and end > s.deadline) or (i+1 < len(ordered) and end > ordered[i+1].arrival):
            return False
    return True


def classify_config(load: str, rows: list[dict], expected_seeds: set[str]) -> bool:
    if len(expected_seeds) != 10 or len(rows) != 10 or {r['seed'] for r in rows} != expected_seeds:
        raise EvidenceError('qualification requires exact ten-seed membership')
    for r in rows:
        if r['validity'] != 'VALID': raise EvidenceError('invalid/incomplete configuration evidence')
        if not 0 <= F(r['pressure']) <= 1 or any(not 0 <= F(r[g+'_dmr']) <= 1 for g in ('H','L')):
            raise EvidenceError('invalid pressure/miss values')
    if not all(r['H_control_witness'] and r['LOW_control_witness'] for r in rows): return False
    p = sum((F(r['pressure']) for r in rows),F(0))/10
    h = sum((F(r['H_dmr']) for r in rows),F(0))/10
    l = sum((F(r['L_dmr']) for r in rows),F(0))/10
    if load == 'light': return 0 <= p < F(1,2) and h <= F(1,100) and l <= F(1,100)
    if load not in {'medium','near-saturation'}: raise EvidenceError('unknown load')
    band = F(1,2) <= p < F(4,5) if load == 'medium' else F(4,5) <= p <= 1
    return band and F(1,100) <= h <= F(4,5) and all(r['positive_assigned_busy_wait'] for r in rows)


def select_configs(eligibility: dict[str, dict[str, bool]]) -> dict:
    if len(eligibility) != 18: raise EvidenceError('all18 declared conditions required')
    selected = {}
    for c, variants in eligibility.items():
        if set(variants) != {'A','B'} or any(type(x) is not bool for x in variants.values()):
            raise EvidenceError('both fixed A/B eligibility states required')
        if variants['A']: selected[c] = 'A'
        elif variants['B']: selected[c] = 'B'
        else: return {'status':'NO_ELIGIBLE_CONDITION','selected':selected,'failed_condition':c}
    return {'status':'SELECTED_ALL_18','selected':selected}

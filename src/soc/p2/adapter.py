"""S2 birth boundary and shared physical engine adapter.

No old fixture envelope is accepted as scientific input. Header-free runtime
payloads are checked only after trusted birth verification, never by an origin
label alone. Tests exercise rejection and hand-authored physical payloads.
"""
from __future__ import annotations

from collections import Counter
import json
import math

from soc.model.schema import Workload
from soc.model.observation import observe, Running, Completed
from soc.p2.generation import parse_payload
from soc.p2.identity import EvidenceError, strict_json


def resolve_scientific_input(envelope: dict, store, types, verify_birth) -> Workload:
    types.validate('SCIENTIFIC_INPUT_ENVELOPE',envelope)
    for field in ('resolution_receipt_ref','generation_receipt_ref','lineage_validation_ref','payload_ref'):
        store.get(envelope[field])
    if not verify_birth(envelope):
        raise EvidenceError('independent generation/resolution/parent lineage not established')
    value=strict_json(store.get(envelope['payload_ref']))
    types.validate('RUNTIME_PAYLOAD',value)
    workload=parse_payload(value)
    counts={g:sum(s.group==g for s in workload.services) for g in ('H','L')}
    expected={'H':50,'L':0} if envelope['control_variant']=='H_ISOLATED' else {'H':50,'L':50}
    if counts!=expected:
        raise EvidenceError('scientific input group count/N-A mismatch')
    return workload


def validate_physical_payload(workload: Workload, trace: dict) -> dict:
    """Independent physical oracle, without science/fixture label conversions."""
    from soc.validation.trace import _summary
    errors=[]
    def fail(code): errors.append(code)
    if set(trace)!={'method','executions','events','decisions','metrics'}:
        return {'status':'FAIL','errors':['TRACE_FIELDS'],'metrics':None}
    if trace['method'] not in {'B1','B2','B3','B4','B5'}:
        fail('METHOD')
    nodes={(s.id,n.id):(s,n) for s in workload.services for n in s.nodes}
    kinds={r.id:r.kind for r in workload.resources}
    links={(l.source,l.destination):l for l in workload.links}
    rows={}
    def numeric(v): return type(v) in (int,float) and math.isfinite(v) and v>=0
    for row in trace['executions']:
        if (set(row)!={'service','node','resource','start','finish'} or not numeric(row['start']) or
                not numeric(row['finish']) or row['finish']<=row['start']):
            fail('INTERVAL');continue
        key=row['service'],row['node']
        if key in rows or key not in nodes:
            fail('TASK_MEMBERSHIP');continue
        rows[key]=row
        s,n=nodes[key]
        compatible={d.resource:d.realized for d in n.durations}
        if row['resource'] not in compatible: fail('COMPATIBILITY')
        elif row['finish']!=row['start']+compatible[row['resource']]: fail('DURATION')
        if row['start']<s.arrival: fail('ARRIVAL')
    if rows.keys()!=nodes.keys(): fail('FULL_DRAIN')
    for key,row in rows.items():
        s,n=nodes[key]
        for e in n.predecessors:
            p=rows.get((s.id,e.node))
            if p is None: fail('MISSING_PREDECESSOR');continue
            if p['resource'] not in kinds or row['resource'] not in kinds: continue
            delay=0.0
            if p['resource']!=row['resource']:
                link=links[kinds[p['resource']],kinds[row['resource']]]
                delay=link.latency+e.size/link.bandwidth
            if row['start']<p['finish']+delay: fail('DATA_READINESS')
    for resource in kinds:
        intervals=sorted((r['start'],r['finish']) for r in rows.values() if r['resource']==resource)
        if any(b[0]<a[1] for a,b in zip(intervals,intervals[1:])): fail('RESOURCE_OVERLAP')
    expected=Counter((s.arrival,'arrival',s.id,'','') for s in workload.services)
    for (sid,nid),r in rows.items():
        expected[r['start'],'start',sid,nid,r['resource']]+=1
        expected[r['finish'],'complete',sid,nid,r['resource']]+=1
    actual=Counter()
    prior=(-1,-1)
    for e in trace['events']:
        if set(e)!={'time','kind','service','node','resource'} or not numeric(e['time']) or e['kind'] not in {'complete','arrival','start'}:
            fail('EVENT_SCHEMA');continue
        order=e['time'],{'complete':0,'arrival':1,'start':2}[e['kind']]
        if order<prior: fail('EVENT_ORDER')
        prior=order
        actual[e['time'],e['kind'],e['service'],e['node'],e['resource']]+=1
    if actual!=expected: fail('EVENT_ACCOUNTING')
    metrics=None
    if not errors:
        metrics=_summary(workload,rows)
        if metrics!=trace['metrics']: fail('METRIC_MISMATCH')
    return {'status':'FAIL' if errors else 'PASS','errors':errors,'metrics':metrics}


def verify_decision_views(workload: Workload, trace: dict, *, compact=False):
    """Rebuild each public call view from prior actual starts/completions.

    Equal-time decisions are ordered by starts already made, not by guessing
    future completions. Also verifies each invocation's selected ready action.
    """
    from dataclasses import asdict
    executions=trace['executions']
    started=set()
    expected_time=0.0
    for decision in trace['decisions']:
        now=decision['time']
        if expected_time is None or now!=expected_time:
            raise EvidenceError('missing/extra invocation or time-advance hook')
        running=[]; completed=[]
        for i,r in enumerate(executions):
            if i not in started: continue
            if r['finish']<=now:
                completed.append(Completed(r['service'],r['node'],r['resource'],r['finish']))
            else:
                running.append(Running(r['service'],r['node'],r['resource'],r['start'],now-r['start']))
        rebuilt_view=observe(workload,now,tuple(running),tuple(completed))
        # JSON lists and dataclass tuples have identical exported representation.
        if not compact and json.dumps(asdict(rebuilt_view),sort_keys=True)!=json.dumps(decision['observation'],sort_keys=True):
            raise EvidenceError('decision public view/future truth mismatch')
        if compact:
            from soc.scheduler.kernels import choose
            expected = choose(rebuilt_view, trace['method'])
            if decision['proposal'] != (asdict(expected) if expected is not None else None):
                raise EvidenceError('compact decision disagrees with reconstructed public view')
        proposal=decision['proposal']
        if proposal is not None:
            matches=[i for i,r in enumerate(executions) if i not in started and r['service']==proposal['service']
                     and r['node']==proposal['node'] and r['resource']==proposal['resource'] and r['start']==now]
            if len(matches)!=1: raise EvidenceError('dispatch/start mismatch')
            started.add(matches[0])
        else:
            if any(i not in started and r['start']==now for i,r in enumerate(executions)):
                raise EvidenceError('empty dispatch omitted actual same-time start')
            future=[s.arrival for s in workload.services if s.arrival>now]
            future += [r['finish'] for i,r in enumerate(executions) if i in started and r['finish']>now]
            # Independently reconstruct data wakeups, including calls which
            # return NONE and leave no physical start event behind.
            busy={r.resource for r in running}
            completed_by_node={r.node:r for r in completed}
            occupied={r.node for r in running}|completed_by_node.keys()
            kinds={r.id:r.kind for r in workload.resources}
            links={(l.source,l.destination):l for l in workload.links}
            for s in workload.services:
                if s.arrival>now:continue
                for n in s.nodes:
                    if n.id in occupied or not all(e.node in completed_by_node for e in n.predecessors):continue
                    for d in n.durations:
                        if d.resource in busy:continue
                        ready=s.arrival
                        for edge in n.predecessors:
                            p=completed_by_node[edge.node]
                            delay=0.0
                            if p.resource!=d.resource:
                                link=links[kinds[p.resource],kinds[d.resource]]
                                delay=link.latency+edge.size/link.bandwidth
                            ready=max(ready,p.finish+delay)
                        if ready>now:future.append(ready)
            expected_time=min(future) if future else None
    if len(started)!=len(executions) or (executions and (not trace['decisions'] or trace['decisions'][-1]['proposal'] is not None or
            trace['decisions'][-1]['time']!=max(r['finish'] for r in executions))):
        raise EvidenceError('missing invocation/final refresh')


def execute_authorized(workload: Workload, method: str, permit) -> dict:
    permit.authorize_execution(workload,method)
    # Identity of science comes from separately verified birth and context, not
    # the legacy fixture transport header emitted by the shared P1 engine API.
    from soc.simulator.engine import simulate
    raw=simulate(workload,method)
    body={k:v for k,v in raw.items() if k not in {'schema_version','origin'}}
    checked=validate_physical_payload(workload,body)
    verify_decision_views(workload,body)
    if checked['status']!='PASS': raise EvidenceError('physical/metric verification failed')
    return body

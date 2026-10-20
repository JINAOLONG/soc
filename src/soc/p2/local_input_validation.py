"""Independent numeric birth checks for the explicitly requested local simulation.

Does not call Generator, field_key, factor, arrival or critical_estimate. Reads
the frozen decimal tables and recomputes every numeric cell and inherited bit.
This is input validation, not a claim of V3 production authority publication.
"""
from decimal import Decimal
from fractions import Fraction as F
import hashlib
import json

from soc.p2.identity import EvidenceError


def validate_main(root, config, seed, workload):
    def table(name):
        return json.loads((root/'docs/P2_design/v2'/name).read_bytes(), parse_float=Decimal)
    templates=table('P2_workload_templates_v2.json')['templates']
    template=next(t for t in templates if t['template_id']==config['template_id'])
    profiles={r['role']:r['estimated_base_ms'] for r in table('P2_resource_profiles_v2.json')['profiles']}
    net=table('P2_communication_profiles_v2.json')
    edges=next(t['edges'] for t in net['edge_tables'] if t['template_id']==config['template_id'])
    def u(slot,field,group='',node='',resource=''):
        body=dict(domain='soc.p2.gen.v2',schema_version=2,generator_version='soc-p2-synthetic-v2-PROPOSED',
                  actual_seed_decimal_string=seed,scenario=config['scenario'],condition_id=config['condition_id'],
                  config_id=config['config_id'],service_slot=slot,service_group=group,template_node_id=node,
                  resource_id=resource,edge_id='',field=field,counter=0)
        data=(json.dumps(body,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
        return F(int.from_bytes(hashlib.sha256(data).digest()[:8],'big'),2**64)
    expected_ids=[]
    exact_bounds=[]
    for slot in range(50):
        at=float(F(config['period_ms'])*(5*(slot//5)+F(slot%5,4)+u(slot,'arrival_jitter')/10))
        for group in ('H','L'):
            sid=f"{config['scenario']}/{config['load']}/{config['size']}/{config['config_id']}/s{slot:03d}/{group}"
            expected_ids.append(sid)
            s=workload.services[len(expected_ids)-1]
            if (s.id,s.arrival,s.group)!=(sid,at,group): raise EvidenceError('independent arrival/group/ID mismatch')
            if [n.id for n in s.nodes]!=[sid+'/'+n['id'] for n in template['nodes']]:
                raise EvidenceError('independent template node membership mismatch')
            minima={}; max_total=F(0)
            for n,t in zip(s.nodes,template['nodes']):
                shared=F(9,10)+u(slot,'service_role_factor',group,t['id'])/5
                row={r:F(c)*F(t['cost_scale'])*shared for r,c in profiles[t['role']].items() if c is not None}
                values=[(d.resource,d.estimate,d.realized) for d in n.durations]
                expected=[(r,float(e),float(e*(F(9,10)+u(slot,'duration_factor',group,t['id'],r)/5))) for r,e in sorted(row.items())]
                if values!=expected: raise EvidenceError('independent duration/compatibility mismatch')
                deps=[(sid+'/'+e['source'],float(F(e['size_mib']))) for e in edges if e['destination']==t['id']]
                if [(e.node,e.size) for e in n.predecessors]!=deps: raise EvidenceError('independent edge mismatch')
                minima[t['id']]=min(row.values())
                max_total+=max(row.values())*F(11,10)
            done={}; pending={n['id']:n for n in template['nodes']}
            while pending:
                ready=sorted(k for k,n in pending.items() if all(p in done for p in n['predecessors']))
                if not ready: raise EvidenceError('independent cyclic graph')
                for k in ready:
                    done[k]=minima[k]+max((done[p] for p in pending[k]['predecessors']),default=F(0))
                    del pending[k]
            deadline=(F(5,2) if group=='H' else F(4))*max(done.values())
            if s.relative_deadline!=float(deadline): raise EvidenceError('independent deadline mismatch')
            for e in edges:
                size=F(e['size_mib'])
                max_total+=max(F(l['latency_ms'])+size/F(l['bandwidth_mib_per_ms']) for l in net['links'])
            exact_bounds.append(max_total+deadline)
    if len(workload.services)!=100: raise EvidenceError('independent full service count mismatch')
    if [(l.source,l.destination,l.latency,l.bandwidth) for l in workload.links]!=[
        (l['source_type'],l['destination_type'],float(F(l['latency_ms'])),float(F(l['bandwidth_mib_per_ms']))) for l in net['links']]:
        raise EvidenceError('independent communication table mismatch')
    if [(r.id,r.kind) for r in workload.resources]!=[(f'CPU{i}','CPU') for i in range(4)]+[('GPU0','GPU'),('NPU0','NPU')]:
        raise EvidenceError('independent resource identity mismatch')
    import math
    return {'status':'PASS','services':100,'nodes':100*config['size'],'independent_control_gap':math.ceil(max(exact_bounds))+1}


def validate_control(parent, child, variant, gap):
    expected=[s for s in parent.services if variant!='H_ISOLATED' or s.group=='H']
    if variant not in {'H_ISOLATED','LOW_COMPETITION'} or len(child.services)!=len(expected):
        raise EvidenceError('independent control variant/count mismatch')
    if child.resources!=parent.resources or child.links!=parent.links: raise EvidenceError('control platform changed')
    for i,(a,b) in enumerate(zip(expected,child.services)):
        if (a.id,a.relative_deadline,a.group,a.nodes)!=(b.id,b.relative_deadline,b.group,b.nodes) or b.arrival!=float(i*gap):
            raise EvidenceError('control bit inheritance/arrival mismatch')
    return {'status':'PASS','variant':variant,'services':len(expected),'gap':gap}

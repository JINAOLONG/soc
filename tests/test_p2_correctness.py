import copy
from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest

from soc.model.observation import Running, observe
from soc.model.schema import Service, Workload
from soc.simulator.engine import simulate
from soc.p2.adapter import validate_physical_payload, verify_decision_views, resolve_scientific_input
from soc.p2.analysis import classify_opportunity, count_opportunities, exact_m2_pairs, paired_means, percentile, registered_indices
from soc.p2.diagnostic import evaluate, snapshot, unique_states
from soc.p2.generation import Generator
from soc.p2.identity import ArtifactStore, EvidenceError, Types, digest, fraction, rational, semantic_bytes
from soc.p2.qualification import busy_pressure, classify_config, controls_witness, feasibility, select_configs, waiting
from soc.p2.runner import NoScientificPermit, ScientificExecutionUnavailable
from p1_fixtures import hand_dag, node, network, overrun, priority, simultaneous

ROOT=Path(__file__).resolve().parents[1]


class P2CorrectnessTests(unittest.TestCase):
    def test_b1_single_ready_is_full_zero_not_absence_claim(self):
        w=Workload((Service('manual-H',0,10,'H',(node('manual-node'),)),),network())
        result=evaluate(observe(w,0))
        self.assertEqual(result['status'],'FULL')
        self.assertEqual(fraction(result['gain']),0)
        self.assertEqual(result['assignments'],1)

    def test_remaining_path_opportunity_with_local_L_slack(self):
        w=Workload((Service('H',0,13,'H',(node('a',duration=2),node('b','NPU0',4,(('a',0),)))),
                    Service('L',0,12,'L',(node('l',estimates={'CPU1':6.5,'NPU0':6}),))),network())
        result=evaluate(observe(w,0))
        self.assertEqual(result['status'],'FULL')
        self.assertEqual(fraction(result['baseline']),10)
        self.assertEqual(fraction(result['optimal']),6)
        self.assertEqual(fraction(result['gain']),F(2,5))

    def test_pending_H_cap_and_expired_estimates_are_partial_not_zero(self):
        w=Workload(tuple(Service(f'H{i}',0,10,'H',(node(f'n{i}',f'CPU{i}'),)) for i in range(3)),network())
        result=evaluate(observe(w,0))
        self.assertEqual(result['status'],'COVERAGE_INSUFFICIENT')
        self.assertIn('PENDING_H_CAP',result['reasons'])
        self.assertNotIn('gain',result)
        w=Workload((Service('running',0,10,'H',(
            node('overrun',estimates={'CPU0':1},actual={'CPU0':5}),
            node('successor','NPU0',1,(('overrun',0),)))),
            Service('later',2,10,'L',(node('later-node','GPU0'),))),network())
        view=observe(w,2,(Running('running','overrun','CPU0',0,2),))
        result=evaluate(view)
        self.assertIn('ESTIMATE_EXHAUSTED',result['reasons'])

    def test_snapshot_typed_bits_and_scope_dedup(self):
        h=hand_dag().services[0]
        w=Workload((h,),network())
        body=snapshot(observe(w,0),{h.id:'HAND-8'})
        Types(ROOT/'docs/P2_design/v3/P2_typed_identity_schema_v3.json').validate('PUBLIC_SNAPSHOT',body)
        self.assertNotIn('realized',json.dumps(body))
        events=[dict(event_id=f'hand-{i}',event_seq=i,decision_seq=i,stream_role='PRIMARY',
                     state_sha256=digest(semantic_bytes(body)),snapshot=body) for i in range(2)]
        rows=unique_states({'run_id':'hand-run','primary_attempt_id':'hand-attempt','observer_spec_sha256':'0'*64},events)
        self.assertEqual([r['counted_as_event_seq'] for r in rows],[0,0])
        scope_body=dict(namespace='soc.p2.denominator-scope.v2',schema_version=2,run_id='hand-run',
                        primary_attempt_id='hand-attempt',observer_spec_sha256='0'*64)
        expected=digest(semantic_bytes(dict(namespace='soc.p2.state-key.v2',schema_version=2,
                        denominator_scope_sha256=digest(semantic_bytes(scope_body)),state_sha256=events[0]['state_sha256'])))
        self.assertEqual(rows[0]['state_key'],expected)
        events[1]['event_id']='hand-0'
        with self.assertRaises(EvidenceError):unique_states({'run_id':'r','primary_attempt_id':'a','observer_spec_sha256':'0'*64},events)

    def test_independent_adapter_checks_physical_payload_and_views(self):
        w=hand_dag();trace=simulate(w,'B2');body={k:v for k,v in trace.items() if k not in {'origin','schema_version'}}
        self.assertEqual(validate_physical_payload(w,body)['status'],'PASS')
        verify_decision_views(w,body)
        broken=copy.deepcopy(body);broken['executions'][0]['finish']+=.5
        self.assertEqual(validate_physical_payload(w,broken)['status'],'FAIL')
        broken=copy.deepcopy(body);broken['decisions'][0]['observation']['now']=1
        with self.assertRaises(EvidenceError):verify_decision_views(w,broken)

    def test_missing_final_or_start_invocation_rejected(self):
        w=simultaneous();trace=simulate(w,'B1')
        with self.assertRaises(EvidenceError):verify_decision_views(w,{**trace,'decisions':trace['decisions'][:-1]})
        first=[r for r in trace['decisions'] if r['proposal'] is not None][0]
        with self.assertRaises(EvidenceError):verify_decision_views(w,{**trace,'decisions':[r for r in trace['decisions'] if r is not first]})
        interior_none=next(r for r in trace['decisions'][:-1] if r['proposal'] is None)
        with self.assertRaises(EvidenceError):verify_decision_views(w,{**trace,'decisions':[r for r in trace['decisions'] if r is not interior_none]})

    def test_fixture_relabel_does_not_supply_scientific_birth(self):
        with tempfile.TemporaryDirectory() as d:
            store=ArtifactStore(Path(d));types=Types(ROOT/'docs/P2_design/v3/P2_typed_identity_schema_v3.json')
            with self.assertRaises(EvidenceError):resolve_scientific_input(hand_dag().to_dict(),store,types,lambda e:True)
            raw=store.put('hand.json',semantic_bytes({'hand':True}))
            envelope=dict(namespace='soc.science.p2.input',schema_version=2,origin='SCIENTIFIC_CALIBRATION',
                workload_id='hand-workload',input_descriptor_sha256='0'*64,blueprint_sha256='0'*64,
                resolution_receipt_ref=raw,generation_receipt_ref=raw,lineage_validation_ref=raw,payload_ref=raw,
                control_variant='MAIN',actual_seed_decimal_string='0',partition='CALIBRATION')
            with self.assertRaises(EvidenceError):resolve_scientific_input(envelope,store,types,lambda e:False)

    def test_control_transform_reuses_hand_numeric_bits(self):
        w=priority();g=Generator(ROOT)
        sidecar={s.id:{'estimates':{n.id:{d.resource:rational(F(d.estimate)) for d in n.durations} for n in s.nodes},
                      'deadline':rational(F(s.relative_deadline))} for s in w.services}
        h,gap=g.derive_control(w,sidecar,'H_ISOLATED')
        low,gap2=g.derive_control(w,sidecar,'LOW_COMPETITION')
        self.assertEqual(gap,gap2)
        self.assertEqual(h.services[0].nodes,w.services[0].nodes)
        self.assertEqual(low.services[1].nodes,w.services[1].nodes)
        self.assertEqual(low.services[1].arrival,gap)
        self.assertEqual(low.services[1].relative_deadline,w.services[1].relative_deadline)

    def test_exact_pressure_wait_and_strict_feasibility(self):
        w=priority();trace=simulate(w,'B2')
        self.assertEqual(busy_pressure(w,trace['executions'],4),1)
        rows=waiting(w,trace['executions'])
        self.assertEqual(next(r['assigned_busy_wait'] for r in rows if r['group']=='L'),2)
        self.assertTrue(all(r['policy_idle']>=0 for r in rows))
        equality=Workload((Service('equal',0,1,'H',(node('eq'),)),),network())
        impossible=Workload((Service('miss',0,.5,'H',(node('miss-node'),)),),network())
        self.assertEqual(feasibility(equality)['equal']['classification'],'FEASIBILITY_NOT_ESTABLISHED')
        self.assertEqual(feasibility(impossible)['miss']['classification'],'CERTIFIED_NATURALLY_INFEASIBLE')

    def test_qualification_edges_and_no_relabel_or_seed_drop(self):
        seeds={f'hand-seed-{i}' for i in range(10)}
        rows=[dict(seed=s,validity='VALID',pressure=F(1,2),H_dmr=F(1,100),L_dmr=F(0),
                   H_control_witness=True,LOW_control_witness=True,positive_assigned_busy_wait=True) for s in sorted(seeds)]
        self.assertTrue(classify_config('medium',rows,seeds))
        self.assertFalse(classify_config('light',rows,seeds))
        with self.assertRaises(EvidenceError):classify_config('medium',rows[:-1],seeds)
        rows[0]['validity']='INVALID'
        with self.assertRaises(EvidenceError):classify_config('medium',rows,seeds)
        selected={f'hand-condition-{i}':{'A':True,'B':True} for i in range(18)}
        self.assertTrue(all(x=='A' for x in select_configs(selected)['selected'].values()))
        selected['hand-condition-0']={'A':False,'B':False}
        self.assertEqual(select_configs(selected)['status'],'NO_ELIGIBLE_CONDITION')

    def test_coarse_three_way_rule_with_hand_counts_and_intervals(self):
        self.assertEqual(count_opportunities([{'status':'NOT_IN_SCOPE'},{'status':'COVERAGE_INSUFFICIENT'},
                         {'status':'FULL','gain':rational(F(1,20))},{'status':'FULL','gain':rational(F(1,100))}]),(3,2,1))
        cells={f'hand-{i}':[(100,80,8)]*10 for i in range(12)}
        intervals={c:(F(1,10),F(1,5)) for c in cells}
        self.assertEqual(classify_opportunity(cells,intervals,evidence_complete=True,m2_valid=True),'SUPPORTED')
        # These are constructed rule tests, not a claim the B1 global negative
        # can be reached by the registered workload family.
        absent={c:[(100,100,0)]*10 for c in cells}
        ci={c:(F(0),F(1,100)) for c in cells}
        self.assertEqual(classify_opportunity(absent,ci,evidence_complete=True,m2_valid=True),'NOT_SUPPORTED')
        absent['hand-0']=[(100,99,0)]*10
        self.assertEqual(classify_opportunity(absent,ci,evidence_complete=True,m2_valid=True),'INCONCLUSIVE')
        self.assertEqual(classify_opportunity(cells,intervals,evidence_complete=True,m2_valid=False),'INCONCLUSIVE')
        self.assertEqual(classify_opportunity({}, {}, evidence_complete=False,m2_valid=False,evaluated=False),'NOT_EVALUATED')

    def test_type7_and_paired_hand_vectors_not_registered_bootstrap(self):
        self.assertEqual(percentile([0,10],F(1,4)),F(5,2))
        values={'hand-A':[F(i) for i in range(10)],'hand-B':[F(i+10) for i in range(10)]}
        result=paired_means(values,[[0]*10,[9]*10])
        self.assertEqual(result['macro'],(F(209,40),F(551,40)))
        with self.assertRaises(ScientificExecutionUnavailable):next(registered_indices(NoScientificPermit()))

    def test_m2_pairs_use_exact_workload_direction_and_service_denominator(self):
        def record(h,l,wait):return dict(workload_sha256='a'*64,workload_id='hand-w',completion_status='COMPLETE',
            validity='VALID',groups={'H':{'count':50,'dmr':h},'L':{'count':50,'p95':l}},H_busy_wait_sum=wait,L_busy_wait_sum=0)
        row=dict(condition_id='hand-c',seed='hand-s',config_id='hand-config',method='B1',reference='B2',workload_id='hand-w',
                 method_record=record(F(1,5),12,100),reference_record=record(F(1,10),10,50))
        expected={('hand-c','hand-s','hand-config','B1','B2','hand-w')}
        result=exact_m2_pairs([row],expected)[0]['contrasts']
        self.assertEqual(result,{'H_DMR_DIFF':F(1,10),'L_P95_DIFF':2,'H_WAIT_DIFF':1,'L_WAIT_DIFF':0})
        with self.assertRaises(EvidenceError):exact_m2_pairs([],expected)
        with self.assertRaises(EvidenceError):exact_m2_pairs([row,row],expected)
        row['reference_record']['workload_sha256']='b'*64
        with self.assertRaises(EvidenceError):exact_m2_pairs([row],expected)

import copy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from soc.model.observation import observe
from soc.p2.adapter import verify_decision_views
from soc.p2.generation import Generator
from soc.p2.identity import EvidenceError
from soc.p2.local_input_validation import validate_main, validate_control
from soc.p2.local_run import LocalPermit, positive_busy_wait, write_new
from soc.p2.qualification import waiting
from soc.scheduler.kernels import online_tables
from soc.simulator.engine import simulate
from p1_fixtures import fixture_cases, hand_dag


class LocalSimulationTests(unittest.TestCase):
    def test_compact_45_fixture_baseline_traces_preserve_all_decisions_and_events(self):
        for name,w in fixture_cases().items():
            for method in ('B1','B2','B3','B4','B5'):
                with self.subTest(name=name,method=method):
                    full=simulate(w,method); compact=simulate(w,method,compact_decisions=True)
                    expected={**full,'decisions':[{k:v for k,v in d.items() if k!='observation'} for d in full['decisions']]}
                    self.assertEqual(compact,expected)
                    verify_decision_views(w,compact,compact=True)

    def test_compact_missing_hook_or_wrong_proposal_fails_reconstruction(self):
        w=hand_dag();trace=simulate(w,'B2',compact_decisions=True)
        broken=copy.deepcopy(trace);broken['decisions']=broken['decisions'][:-1]
        with self.assertRaises(EvidenceError): verify_decision_views(w,broken,compact=True)
        broken=copy.deepcopy(trace)
        next(d for d in broken['decisions'] if d['proposal'])['proposal']['score']+=1
        with self.assertRaises(EvidenceError): verify_decision_views(w,broken,compact=True)

    def test_public_table_cache_cannot_be_poisoned_by_returned_mutable_maps(self):
        view=observe(hand_dag(),0);reference=copy.deepcopy(online_tables(view))
        rank,octs,oct_rank=online_tables(view)
        rank.clear();oct_rank.clear();next(iter(octs.values())).clear()
        self.assertEqual(online_tables(view),reference)

    def test_exclusive_evidence_writes_do_not_replace_existing_reservation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reserved.json'
            write_new(p,{'reservation':1})
            with self.assertRaises(FileExistsError): write_new(p,{'reservation':2})
            self.assertEqual(json.loads(p.read_text()),{'reservation':1})

    def test_local_permit_rejects_unregistered_generation(self):
        permit=LocalPermit({'configs':[{'config_id':'manual'}],'registered_seeds':[0]})
        permit.authorize_generation({'config_id':'manual'},'0')
        with self.assertRaises(EvidenceError):permit.authorize_generation({'config_id':'manual'},'1')
        with self.assertRaises(EvidenceError):permit.authorize_generation({'config_id':'other'},'0')

    def test_busy_wait_predicate_matches_full_exact_decomposition(self):
        for w in fixture_cases().values():
            for method in ('B1','B2','B3','B4','B5'):
                trace=simulate(w,method,compact_decisions=True)
                self.assertEqual(positive_busy_wait(w,trace),any(r['assigned_busy_wait']>0 for r in waiting(w,trace['executions'])))

    def test_independent_birth_detects_duration_arrival_deadline_and_edge_corruption(self):
        # Literal two-node engineering graph, artificial seed0/config, no
        # registered science template, realization or seed is accessed here.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);base=root/'docs/P2_design/v2';base.mkdir(parents=True)
            docs={
                'P2_workload_templates_v2.json':{'templates':[{'template_id':'manual','nodes':[
                    {'id':'a','role':'manual','cost_scale':'1','predecessors':[]},
                    {'id':'b','role':'manual','cost_scale':'1/2','predecessors':['a']}]}]},
                'P2_resource_profiles_v2.json':{'profiles':[{'role':'manual','estimated_base_ms':{'CPU0':1,'GPU0':2}}]},
                'P2_communication_profiles_v2.json':{'links':[
                    {'source_type':a,'destination_type':b,'latency_ms':0,'bandwidth_mib_per_ms':1}
                    for a in ('CPU','GPU','NPU') for b in ('CPU','GPU','NPU')],
                    'edge_tables':[{'template_id':'manual','edges':[{'source':'a','destination':'b','size_mib':'1/4'}]}]}}
            for name,body in docs.items(): (base/name).write_text(json.dumps(body))
            config=dict(config_id='manual',scenario='manual',condition_id='manual',load='manual',size=2,template_id='manual',period_ms=5)
            gen=Generator(root);w,sidecar=gen.materialize(config,'0',LocalPermit({'configs':[config],'registered_seeds':[0]}))
            valid=validate_main(root,config,'0',w);self.assertEqual(valid['status'],'PASS')
            s=w.services[0];n=s.nodes[0];duration=n.durations[0]
            mutants=[replace(s,arrival=s.arrival+1),replace(s,relative_deadline=s.relative_deadline+1),
                     replace(s,nodes=(replace(n,durations=(replace(duration,realized=duration.realized+1),*n.durations[1:])),*s.nodes[1:])),
                     replace(s,nodes=(n,replace(s.nodes[1],predecessors=())))]
            for mutant in mutants:
                with self.assertRaises(EvidenceError):validate_main(root,config,'0',replace(w,services=(mutant,*w.services[1:])))
            child,gap=gen.derive_control(w,sidecar,'H_ISOLATED')
            self.assertEqual(gap,valid['independent_control_gap'])
            self.assertEqual(validate_control(w,child,'H_ISOLATED',gap)['status'],'PASS')
            bad=replace(child,services=(replace(child.services[0],relative_deadline=1),*child.services[1:]))
            with self.assertRaises(EvidenceError):validate_control(w,bad,'H_ISOLATED',gap)

from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from soc.p2.identity import (ArtifactStore, EvidenceError, Types, bits, unbits,
                             digest, fraction, rational, semantic_bytes, strict_json)
from soc.p2.generation import (Generator, arrival, critical_estimate, factor,
                               field_key, parse_payload, payload, rn64, uniform)
from soc.p2.runner import NoScientificPermit, ScientificExecutionUnavailable, inspect_plan, preflight
from p1_fixtures import hand_dag

ROOT=Path(__file__).resolve().parents[1]


class P2IdentityTests(unittest.TestCase):
    def test_semantic_canonicalization_and_rejections(self):
        self.assertEqual(semantic_bytes({'z':None,'a':[1,True,'x']}),b'{"a":[1,true,"x"],"z":null}\n')
        for value in (1.0,{'a':float('nan')},{'é':1}, {'x':'é'}):
            with self.subTest(value=repr(value)),self.assertRaises(EvidenceError): semantic_bytes(value)
        with self.assertRaises(EvidenceError):strict_json(b'{"a":1,"a":2}')
        with self.assertRaises(EvidenceError):strict_json(b'{"x":NaN}')

    def test_rational_and_binary64_boundaries(self):
        self.assertEqual(fraction(rational(F(-2,3))),F(-2,3))
        for value in ({'numerator':'2','denominator':'4'},{'numerator':'-0','denominator':'1'}):
            with self.assertRaises(EvidenceError):fraction(value)
        self.assertEqual(bits(-0.0),'0000000000000000')
        self.assertEqual(unbits(bits(.1)),.1)
        for value in ('8000000000000000','7ff0000000000000','7ff8000000000000'):
            with self.assertRaises(EvidenceError):unbits(value)
        # Exact halfway tie rounds to even, not via a decimal/float intermediate.
        self.assertEqual(rn64(F(1)+F(1,2**53)),1.0)
        self.assertEqual(rn64(F(1)+F(3,2**53)),1+2**-51)

    def test_artifact_immutable_conflicts_and_paths(self):
        with tempfile.TemporaryDirectory() as d:
            store=ArtifactStore(Path(d))
            ref=store.put('a/record.json',b'original')
            self.assertEqual(store.get(ref),b'original')
            self.assertEqual(store.put('a/record.json',b'original'),ref)
            with self.assertRaises(EvidenceError):store.put('a/record.json',b'changed')
            for path in ('../escape','/absolute','a//x','a/./x','a\\x'):
                with self.subTest(path=path),self.assertRaises(EvidenceError):store.put(path,b'x')
            (Path(d)/'link').symlink_to('/tmp',target_is_directory=True)
            with self.assertRaises(EvidenceError):store.put('link/escape',b'x')
            broken={**ref,'sha256':'0'*64}
            with self.assertRaises(EvidenceError):store.get(broken)

    def test_inventory_uniqueness_and_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            store=ArtifactStore(Path(d));r=store.put('x',b'x')
            self.assertEqual(json.loads(store.get(store.inventory([r]))),[r])
            with self.assertRaises(EvidenceError):store.inventory([r,r])
            (Path(d)/'x').write_bytes(b'y')
            with self.assertRaises(EvidenceError):store.inventory([r])

    def test_closed_original_schema_and_id_prefix(self):
        types=Types(ROOT/'docs/P2_design/v3/P2_typed_identity_schema_v3.json')
        body=dict(namespace='soc.p2.coordination-domain.v3',schema_version=3,budget_scope_sha256='0'*64,
                  purpose='PRIMARY_EXECUTION',semantic_target_id='hand-trial')
        ident,sha=types.identity('COORDINATION_DOMAIN_PREIMAGE_V3',body)
        self.assertEqual(sha,digest(semantic_bytes(body)))
        self.assertTrue(ident.startswith('urn:soc:coordination-domain-preimage-v3:'))
        for bad in ({**body,'extra':0},{**body,'schema_version':True},{**body,'purpose':'DEVELOPMENT'}):
            with self.assertRaises(EvidenceError):types.validate('COORDINATION_DOMAIN_PREIMAGE_V3',bad)

    def test_manual_field_keys_are_method_free_and_exact(self):
        config={'scenario':'COCKPIT','condition_id':'HAND-CONDITION','config_id':'HAND-CONFIG'}
        key=field_key('0',config,0,'service_role_factor','H','manual-node')
        self.assertEqual(len(key),14)
        self.assertEqual(key['resource_id'],'')
        self.assertEqual(uniform(key),F(int(digest(semantic_bytes(key))[:16],16),2**64))
        self.assertTrue(F(9,10)<=factor(key)<F(11,10))
        other=field_key('0',config,0,'duration_factor','H','manual-node','CPU0')
        self.assertNotEqual(other,key)
        self.assertNotIn('method',key)
        jitter=field_key('0',config,0,'arrival_jitter','H','ignored','CPU0')
        self.assertEqual((jitter['service_group'],jitter['template_node_id'],jitter['resource_id']),('','',''))
        with self.assertRaises(EvidenceError):field_key('00',config,0,'arrival_jitter')

    def test_arrival_and_critical_deadline_hand_values(self):
        self.assertEqual(arrival(F(20),4,F(0)),20)
        self.assertEqual(arrival(F(20),5,F(1,2)),101)
        graph=[{'id':'a','predecessors':[]},{'id':'b','predecessors':['a']},{'id':'c','predecessors':[]}]
        cost={'a':{'CPU0':F(2)},'b':{'CPU0':F(4),'NPU0':F(1)},'c':{'GPU0':F(5)}}
        self.assertEqual(critical_estimate(graph,cost),5)

    def test_scientific_generation_denied_before_any_draw(self):
        generator=Generator(ROOT)
        # Deliberately incomplete config: gate rejection must precede parsing or draw.
        with self.assertRaises(ScientificExecutionUnavailable):generator.materialize({},'0',NoScientificPermit())

    def test_generation_loop_with_literal_hand_graph_and_no_random_draws(self):
        # No registered template, configuration, seed, or random draw. Exercise
        # the production arithmetic with a two-slot literal engineering model.
        g=object.__new__(Generator)
        g.templates={'HAND-TEMPLATE':{'nodes':[{'id':'a','role':'hand','cost_scale':'1','predecessors':[]},
                                             {'id':'b','role':'hand','cost_scale':'1/2','predecessors':['a']}]}}
        g.profiles={'hand':{'estimated_base_ms':{'CPU0':2,'NPU0':None}}}
        g.edges={'HAND-TEMPLATE':[{'source':'a','destination':'b','size_mib':F(1,4)}]}
        g.network={'links':[{'source_type':a,'destination_type':b,'latency_ms':0,'bandwidth_mib_per_ms':1}
                            for a in ('CPU','GPU','NPU') for b in ('CPU','GPU','NPU')]}
        config=dict(scenario='COCKPIT',load='light',size=2,config_id='HAND-CONFIG',condition_id='HAND',
                    template_id='HAND-TEMPLATE',period_ms=20)
        with patch('soc.p2.generation.factor',return_value=F(1)),patch('soc.p2.generation.uniform',return_value=F(0)):
            w,sidecar=g._build(config,'0',slots=2)
        self.assertEqual(len(w.services),4)
        self.assertEqual([s.arrival for s in w.services],[0,0,5,5])
        self.assertEqual([s.relative_deadline for s in w.services],[7.5,12,7.5,12])
        self.assertEqual([n.durations[0].realized for n in w.services[0].nodes],[2,1])
        self.assertEqual(fraction(sidecar[w.services[0].id]['deadline']),F(15,2))

    def test_payload_roundtrip_keeps_fixture_family_separate(self):
        w=hand_dag()
        body=json.loads(json.dumps(payload(w)))
        self.assertEqual(parse_payload(body),w)
        with self.assertRaises(EvidenceError):parse_payload(w.to_dict())

    def test_approved_plan_is_symbolic_and_science_stays_blocked(self):
        plan=inspect_plan(ROOT)
        self.assertEqual((plan['trial_slots'],plan['symbolic_inputs'],plan['materialized_inputs']),(2520,1080,0))
        gate=preflight(ROOT)
        self.assertEqual(gate['status'],'BLOCKED')
        self.assertIn('SCIENTIFIC_EXECUTION_NOT_AUTHORIZED',gate['reasons'])
        self.assertFalse(gate['scientific_execution_authorized'])

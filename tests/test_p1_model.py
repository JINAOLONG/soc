import copy
import unittest
from dataclasses import replace

from soc.model.schema import (Dependency, Duration, Link, Node, Service, Workload,
                              ModelError, communication, canonical_bytes, topological_order)
from p1_fixtures import hand_dag, network, node


class ModelTests(unittest.TestCase):
    def test_eight_node_dag_and_identity_roundtrip(self):
        w = hand_dag()
        self.assertEqual(len(w.services[0].nodes), 8)
        self.assertEqual(set(topological_order(w.services[0])), set("abcdefgh"))
        self.assertEqual(canonical_bytes(w.to_dict()), canonical_bytes(Workload.from_dict(w.to_dict()).to_dict()))

    def test_cycle_missing_duplicate_empty_rejected(self):
        bad_nodes = [(), (node("a", predecessors=(("missing", 0),)),),
                     (node("a"), node("a")),
                     (node("a", predecessors=(("b", 0),)), node("b", predecessors=(("a", 0),)))]
        for nodes in bad_nodes:
            with self.subTest(nodes=nodes), self.assertRaises(ModelError):
                Service("bad", 0, 1, "H", nodes)

    def test_invalid_numbers_and_compatibility_rejected(self):
        for value in (float("nan"), float("inf"), -1, 0, True):
            with self.subTest(value=value), self.assertRaises(ModelError):
                Duration("CPU0", value, 1)
        with self.assertRaises(ModelError):
            Node("x", ())
        with self.assertRaises(ModelError):
            Node("x", (Duration("CPU0", 1, 1), Duration("CPU0", 2, 2)))
        with self.assertRaises(ModelError):
            Link("CPU", "GPU", 0, 0)
        with self.assertRaises(ModelError):
            Dependency("x", -1)

    def test_resource_service_and_global_node_uniqueness(self):
        w = hand_dag()
        for changed in [dict(resources=w.resources+(w.resources[0],)), dict(services=w.services+(w.services[0],)),
                        dict(services=(w.services[0], Service("other", 0, 1, "H", (node("a"),)))),
                        dict(links=w.links[:-1])]:
            with self.subTest(changed=changed), self.assertRaises(ModelError):
                replace(w, **changed)
        with self.assertRaises(ModelError):
            Workload((Service("x", 0, 1, "H", (node("x", "BAD"),)),), network())

    def test_same_unit_zero_and_cross_unit_formula(self):
        w = replace(hand_dag(), links=network(latency=2, bandwidth=4))
        self.assertEqual(communication(w, "CPU0", "CPU0", 100), 0)
        self.assertEqual(communication(w, "CPU0", "CPU1", 8), 4)
        self.assertEqual(communication(w, "CPU0", "NPU0", 8), 4)
        with self.assertRaises(ModelError):
            communication(w, "CPU0", "UNKNOWN", 1)

    def test_original_input_is_not_mutated_by_construction(self):
        raw = copy.deepcopy(hand_dag().to_dict())
        saved = copy.deepcopy(raw)
        Workload.from_dict(raw)
        self.assertEqual(raw, saved)

    def test_deadlines_and_input_schema_are_strict(self):
        for kwargs in [dict(arrival=-1), dict(relative_deadline=0), dict(group="ASIL")]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ModelError):
                replace(hand_dag().services[0], **kwargs)
        raw = hand_dag().to_dict()
        raw["origin"] = "FORMAL_EVALUATION"
        with self.assertRaises(ModelError):
            Workload.from_dict(raw)

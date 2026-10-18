import unittest
from dataclasses import replace

from soc.model.observation import observe, Running, Completed
from soc.model.schema import Workload, Service, Link
from soc.scheduler.kernels import (source_tables, insertion_start, online_tables, mean_transfer,
                                    predictions, ordered_ready, choose)
from p1_fixtures import priority, network, node, oeft_choice, overrun


class KernelTests(unittest.TestCase):
    def test_kernel_numeric_inputs_reject_bool_and_nonfinite(self):
        for bad in (True, float("nan"), float("inf"), -1):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                insertion_start(0, bad, ())
            with self.subTest(value=bad), self.assertRaises(ValueError):
                source_tables({"a": {"p": bad}}, {"a": ()}, {})

    def test_heft_original_fig3_table1_all_ten_ranks(self):
        from p1_source_examples import heft_example
        ranks, _, _ = heft_example()
        expected = [108,77,80,80,69,63.333,42.667,35.667,44.333,14.667]
        for i, value in enumerate(expected, 1):
            self.assertAlmostEqual(ranks[str(i)], value, delta=.0005)

    def test_peft_original_fig1_table2_all_thirty_oct_cells(self):
        from p1_source_examples import peft_example
        rank, oct_table, oct_rank = peft_example()
        expected = [(64,68,86),(42,39,42),(27,41,43),(42,39,50),(28,37,28),
                    (42,39,44),(13,16,22),(13,16,33),(13,16,20),(0,0,0)]
        for i, row in enumerate(expected, 1):
            self.assertEqual(oct_table[str(i)], dict(zip(("P1", "P2", "P3"), row)))
        self.assertAlmostEqual(rank["1"], 169)
        self.assertAlmostEqual(oct_rank["1"], 218/3)

    def test_source_recurrences_hand_arithmetic(self):
        costs = {"a": {"p": 2, "q": 4}, "b": {"p": 4, "q": 2}, "c": {"p": 1, "q": 3}}
        successors = {"a": ("b", "c"), "b": (), "c": ()}
        rank, oct_table, ranks = source_tables(costs, successors, {("a", "b"): 1, ("a", "c"): 2})
        self.assertEqual(rank, {"b": 3, "c": 2, "a": 7})
        self.assertEqual(oct_table, {"b": {"p": 0, "q": 0}, "c": {"p": 0, "q": 0}, "a": {"p": 3, "q": 3}})
        self.assertEqual(ranks, {"b": 0, "c": 0, "a": 3})
        changed_costs = {**costs, "a": {"p": 200, "q": 400}}
        self.assertEqual(source_tables(changed_costs, successors, {("a", "b"): 1, ("a", "c"): 2})[1], oct_table)

    def test_insertion_uses_idle_gap_not_append_only(self):
        self.assertEqual(insertion_start(1, 2, ((0, 1), (5, 8))), 1)
        self.assertEqual(insertion_start(2, 4, ((0, 1), (5, 8))), 8)
        self.assertEqual(insertion_start(1, 4, ((0, 1), (5, 8))), 1)
        with self.assertRaises(ValueError):
            insertion_start(0, 1, ((3, 5), (4, 8)))

    def test_b1_b2_and_b5_have_distinct_priority_roles(self):
        view = observe(priority(), 0)
        self.assertEqual(ordered_ready(view, "B1")[0][0], "L")
        self.assertEqual(ordered_ready(view, "B2")[0][0], "H")
        self.assertEqual(ordered_ready(view, "B5")[0][0], "H")

    def test_eft_and_oeft_choose_different_processors(self):
        view = observe(oeft_choice(), 0)
        self.assertEqual(choose(view, "B3").resource, "CPU0")
        self.assertEqual(choose(view, "B4").resource, "GPU0")

    def test_oct_is_independent_of_busy_availability(self):
        w = oeft_choice()
        idle = observe(w, 0)
        busy = observe(w, 0, (Running("oeft", "parent", "CPU0", 0, 0),))
        self.assertEqual(online_tables(idle), online_tables(busy))

    def test_busy_prediction_uses_estimate_elapsed_not_actual_finish(self):
        w = overrun()
        view = observe(w, 2, (Running("running", "overrun", "CPU0", 0, 2),))
        p = predictions(view, "later", "later-node")[0]
        self.assertEqual(p.resource, "CPU0")
        self.assertEqual(p.estimated_start, 2)
        self.assertFalse(p.feasible_now)
        self.assertIsNone(choose(view, "B1"))

    def test_deterministic_task_and_resource_ties(self):
        w = Workload((Service("b", 0, 10, "H", (node("b-node", estimates={"CPU1": 1, "CPU0": 1}),)),
                      Service("a", 0, 10, "H", (node("a-node", estimates={"CPU1": 1, "CPU0": 1}),))), network())
        for method in ("B1", "B2", "B3", "B4", "B5"):
            self.assertEqual((choose(observe(w, 0), method).service, choose(observe(w, 0), method).resource), ("a", "CPU0"))

    def test_compatibility_and_destination_copy_readiness(self):
        w = Workload((Service("s", 0, 30, "H", (node("p"), node("c", predecessors=(("p", 4),),
                                    estimates={"CPU0": 10, "GPU0": 1}))),), network())
        view = observe(w, 2, completed=(Completed("s", "p", "CPU0", 1),))
        proposals = {p.resource: p for p in predictions(view, "s", "c")}
        self.assertEqual(set(proposals), {"CPU0", "GPU0"})
        self.assertEqual(proposals["CPU0"].estimated_start, 2)
        self.assertEqual(proposals["GPU0"].estimated_start, 5)
        self.assertFalse(proposals["GPU0"].feasible_now)

    def test_mean_bandwidth_is_not_mean_pairwise_delay(self):
        w = Workload((Service("s", 0, 20, "H", (node("p", estimates={"CPU0": 1, "GPU0": 1}),
              node("c", "NPU0", predecessors=(("p", 6),)))),), network())
        links = tuple(replace(l, bandwidth=2 if l.source == "CPU" else 4) for l in w.links)
        view = observe(replace(w, links=links), 0)
        parent, child = view.services[0].nodes[1], view.services[0].nodes[0]
        self.assertEqual(mean_transfer(view, parent, child, 6), 2)

    def test_invalid_graph_and_unknown_baseline_fail_closed(self):
        with self.assertRaises(ValueError):
            source_tables({"a": {"p": 1}}, {"a": ("a",)}, {("a", "a"): 0})
        with self.assertRaises(ValueError):
            choose(observe(priority(), 0), "CPOP")

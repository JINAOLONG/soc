import unittest

from soc.model.schema import canonical_bytes, ModelError
from soc.scheduler.kernels import Proposal, choose
from soc.simulator.engine import simulate, DeadlockError
from soc.validation.trace import validate_trace
from p1_fixtures import fixture_cases, hand_dag, HAND_INTERVALS, priority, simultaneous, wait_scan, overrun


class EngineTests(unittest.TestCase):
    def test_eight_node_manual_times_all_baselines_and_validator(self):
        for method in ("B1", "B2", "B3", "B4", "B5"):
            with self.subTest(method=method):
                w = hand_dag()
                trace = simulate(w, method)
                self.assertEqual({r["node"]: (r["start"], r["finish"]) for r in trace["executions"]}, HAND_INTERVALS)
                self.assertEqual(validate_trace(w, trace)["status"], "PASS")
                self.assertEqual(trace["metrics"]["groups"]["H"]["dmr"], 0)
                self.assertEqual(trace["metrics"]["groups"]["L"]["dmr"], 1)

    def test_b1_b2_and_b5_hand_checked_start_difference(self):
        w = priority()
        self.assertEqual(simulate(w, "B1")["executions"][0]["node"], "L-root")
        self.assertEqual(simulate(w, "B2")["executions"][0]["node"], "H-root")
        self.assertEqual(simulate(w, "B5")["executions"][0]["node"], "H-root")

    def test_same_time_completions_before_arrivals_before_dispatch(self):
        trace = simulate(simultaneous(), "B1")
        self.assertEqual([e["kind"] for e in trace["events"] if e["time"] == 2], ["complete", "arrival", "start"])
        self.assertEqual(trace["metrics"]["groups"]["H"]["dmr"], 0)
        self.assertEqual(trace["metrics"]["groups"]["L"]["dmr"], 0)

    def test_waiting_does_not_reserve_idle_units_or_block_other_tasks(self):
        trace = simulate(wait_scan(), "B2")
        starts = {r["node"]: r["start"] for r in trace["executions"]}
        self.assertEqual(starts, {"busy": 0, "other-node": 1, "wait": 5})

    def test_overrun_wait_never_uses_true_release_as_estimate(self):
        trace = simulate(overrun(), "B2")
        starts = {r["node"]: r["start"] for r in trace["executions"]}
        self.assertEqual(starts["later-node"], 5)
        decision = next(d for d in trace["decisions"] if d["time"] == 2)
        self.assertIsNone(decision["proposal"])
        self.assertNotIn("finish", decision["observation"]["running"][0])

    def test_pending_remapping_recomputes_destination_data_and_does_not_reserve_gpu(self):
        from p1_fixtures import remapping
        trace = simulate(remapping(), "B1")
        rows = {r["node"]: r for r in trace["executions"]}
        self.assertEqual((rows["gpu-load"]["resource"], rows["gpu-load"]["start"]), ("GPU0", 2))
        self.assertEqual((rows["consumer"]["resource"], rows["consumer"]["start"]), ("NPU0", 4))
        self.assertEqual(validate_trace(remapping(), trace)["status"], "PASS")

    def test_all_fixtures_all_methods_exact_replay_input_fairness_and_independent_metrics(self):
        for name, workload in fixture_cases().items():
            before = canonical_bytes(workload.to_dict())
            for method in ("B1", "B2", "B3", "B4", "B5"):
                with self.subTest(fixture=name, method=method):
                    first, second = simulate(workload, method), simulate(workload, method)
                    self.assertEqual(canonical_bytes(first), canonical_bytes(second))
                    audit = validate_trace(workload, first)
                    self.assertEqual(audit["status"], "PASS", audit)
                    self.assertEqual(audit["metrics"], first["metrics"])
                    self.assertEqual(canonical_bytes(workload.to_dict()), before)

    def test_deadlock_is_explicit_when_controller_refuses_all_progress(self):
        with self.assertRaisesRegex(DeadlockError, "no legal start"):
            simulate(priority(), "B1", policy=lambda view: None)

    def test_engine_rejects_invalid_controller_assignment_and_early_dependency(self):
        for proposal in (Proposal("H", "H-root", "GPU0", 0, 1, 1, True),
                         Proposal("unknown", "H-root", "CPU0", 0, 1, 1, True)):
            with self.subTest(proposal=proposal), self.assertRaises(ModelError):
                simulate(priority(), "B1", policy=lambda view: proposal)
        p = Proposal("H-hand", "h", "CPU0", 0, 1, 1, True)
        with self.assertRaises(ModelError):
            simulate(hand_dag(), "B1", policy=lambda view: p)

    def test_scheduler_never_observes_future_services_or_realized_costs(self):
        seen = []
        def audit_policy(view):
            self.assertTrue(all(s.arrival <= view.now for s in view.services))
            self.assertNotIn("realized", repr(view))
            self.assertNotIn("event_queue", repr(view))
            seen.append(view)
            return choose(view, "B1")
        simulate(simultaneous(), "B1", policy=audit_policy)
        self.assertEqual(len(seen[0].services), 1)
        self.assertEqual({s.id for s in seen[-1].services}, {"early", "new"})

    def test_empty_and_minimal_inputs_and_full_drain(self):
        cases = fixture_cases()
        empty = simulate(cases["empty"], "B1")
        self.assertEqual(empty["events"], [])
        self.assertIsNone(empty["metrics"]["groups"]["L"]["dmr"])
        small = simulate(cases["minimal"], "B1")
        self.assertEqual(small["executions"][0]["finish"], 1)
        hand = simulate(hand_dag(), "B1")
        self.assertEqual(len([e for e in hand["events"] if e["kind"] == "complete"]), 9)
        self.assertEqual(hand["metrics"]["groups"]["L"]["p95"], 13)

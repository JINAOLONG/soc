import unittest
from unittest.mock import patch

from soc.model.schema import Workload, Service
from soc.simulator.engine import simulate
from soc.validation.trace import validate_trace
from p1_fixtures import hand_dag, network, node
from p1_negative_cases import negative_cases


class TraceTests(unittest.TestCase):
    def test_all_explicit_illegal_trace_cases_rejected_with_expected_code(self):
        w = hand_dag()
        for name, expected, trace in negative_cases(simulate(w, "B1")):
            with self.subTest(case=name):
                result = validate_trace(w, trace)
                self.assertEqual(result["status"], "FAIL")
                self.assertIn(expected, {e["code"] for e in result["errors"]})

    def test_arrival_constraint_independently_checked(self):
        w = Workload((Service("s", 2, 10, "H", (node("n"),)),), network())
        trace = simulate(w, "B1")
        trace["executions"][0].update(start=0, finish=1)
        self.assertIn("ARRIVAL", {e["code"] for e in validate_trace(w, trace)["errors"]})

    def test_validator_does_not_call_engine_runtime_metrics_or_transfer(self):
        w = hand_dag()
        trace = simulate(w, "B1")
        with patch("soc.simulator.engine.simulate", side_effect=AssertionError("engine called")), \
             patch("soc.metrics.fixture.summarize", side_effect=AssertionError("metrics called")), \
             patch("soc.model.schema.communication", side_effect=AssertionError("transfer called")), \
             patch("soc.scheduler.kernels.choose", side_effect=AssertionError("scheduler called")):
            self.assertEqual(validate_trace(w, trace)["status"], "PASS")

    def test_same_time_wrong_event_phase_is_rejected(self):
        from p1_fixtures import simultaneous
        w = simultaneous()
        trace = simulate(w, "B1")
        indices = [i for i, e in enumerate(trace["events"]) if e["time"] == 2]
        i, j = indices[:2]
        trace["events"][i], trace["events"][j] = trace["events"][j], trace["events"][i]
        self.assertIn("EVENT_ORDER", {e["code"] for e in validate_trace(w, trace)["errors"]})

    def test_bad_trace_shapes_fail_closed(self):
        for trace in (None, {}, {"schema_version": 1, "origin": "HAND_AUTHORED_CORRECTNESS_FIXTURE", "events": {}, "executions": []}):
            with self.subTest(trace=trace):
                self.assertEqual(validate_trace(hand_dag(), trace)["status"], "FAIL")

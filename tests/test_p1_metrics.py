import unittest

from soc.metrics.fixture import quantile, summarize
from soc.model.schema import ModelError
from p1_fixtures import hand_dag


class MetricTests(unittest.TestCase):
    def test_type7_and_absent_group_semantics(self):
        self.assertEqual(quantile([10, 20], .95), 19.5)
        self.assertEqual(quantile([7], .99), 7)
        self.assertIsNone(quantile([], .95))
        with self.assertRaises(ValueError):
            quantile([float("nan")], .95)

    def test_handwritten_completions_equality_miss_and_group_quantiles(self):
        w = hand_dag()
        from p1_fixtures import HAND_INTERVALS
        rows = [dict(service=s.id, node=n.id, resource=n.durations[0].resource,
                     start=HAND_INTERVALS[n.id][0], finish=HAND_INTERVALS[n.id][1])
                for s in w.services for n in s.nodes]
        result = summarize(w, rows)
        self.assertEqual(result["groups"]["H"], dict(count=1, dmr=0, p50=13, p95=13, p99=13, maximum=13))
        self.assertEqual(result["groups"]["L"]["dmr"], 1)
        self.assertEqual(result["groups"]["L"]["p95"], 13)
        self.assertEqual(result["resources"]["CPU0"]["busy"], 4)
        self.assertEqual(result["cross_unit_data_total"], 8)  # 1+1+2+1+1+1+1 MiB
        self.assertEqual(result["makespan"], 13)

    def test_missing_duplicate_or_unknown_node_cannot_be_a_metric_sample(self):
        with self.assertRaises(ModelError):
            summarize(hand_dag(), [])
        rows = [dict(service=s.id, node=n.id, finish=13) for s in hand_dag().services for n in s.nodes]
        with self.assertRaises(ModelError):
            summarize(hand_dag(), rows+[rows[0]])

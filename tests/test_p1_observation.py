import dataclasses
import unittest
from dataclasses import replace

from soc.model.observation import observe, Running, Completed, dependency_ready
from soc.model.schema import Workload, Service, ModelError
from p1_fixtures import hand_dag, network, node


class ObservationTests(unittest.TestCase):
    def test_recursive_immutability_and_no_private_attributes(self):
        view = observe(hand_dag(), 0)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            view.now = 4
        with self.assertRaises(dataclasses.FrozenInstanceError):
            view.services[0].nodes[0].estimates = ()
        self.assertFalse(hasattr(view, "__dict__"))
        public = repr(dataclasses.asdict(view))
        for forbidden in ("realized", "event_queue", "future", "true_duration"):
            self.assertNotIn(forbidden, public)

    def test_noninterference_of_future_services_and_actual_durations(self):
        w = hand_dag()
        changed = tuple(replace(s, nodes=tuple(replace(n, durations=tuple(replace(d, realized=d.realized+1000)
                       for d in n.durations)) for n in s.nodes)) for s in w.services)
        future = Service("secret", 100, 1, "H", (node("hidden"),))
        other = Workload((*changed, future), network())
        self.assertEqual(observe(w, 0), observe(other, 0))
        self.assertNotIn("secret", repr(observe(other, 0)))

    def test_future_and_duplicate_status_cannot_be_injected(self):
        for completed in [(Completed("H-hand", "a", "CPU0", 2),),
                          (Completed("unknown", "a", "CPU0", 0),),
                          (Completed("H-hand", "a", "GPU0", 0),)]:
            with self.subTest(completed=completed), self.assertRaises(ModelError):
                observe(hand_dag(), 1, completed=completed)
        with self.assertRaises(ModelError):
            observe(hand_dag(), 1, (Running("H-hand", "a", "CPU0", 0, 1),),
                    (Completed("H-hand", "a", "CPU0", 1),))

    def test_dependency_ready_and_running_observations(self):
        w = hand_dag()
        self.assertEqual(dependency_ready(observe(w, 0)), (("H-hand", "a"), ("L-hand", "l")))
        view = observe(w, 2, (Running("L-hand", "l", "CPU3", 0, 2),),
                       (Completed("H-hand", "a", "CPU0", 2),))
        self.assertEqual(dependency_ready(view), (("H-hand", "b"), ("H-hand", "c")))
        self.assertEqual(view.running[0].elapsed, 2)
        with self.assertRaises(ModelError):
            observe(w, 2, (Running("L-hand", "l", "CPU3", 0, 1),))

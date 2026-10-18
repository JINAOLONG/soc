"""Fixed manual inputs. No seed derivation, RNG, or scientific partition imports."""
from soc.model.schema import Dependency, Duration, Link, Node, Service, Workload


def network(latency=0, bandwidth=1):
    return tuple(Link(a, b, latency, bandwidth) for a in ("CPU", "GPU", "NPU") for b in ("CPU", "GPU", "NPU"))


def node(name, resource="CPU0", duration=1, predecessors=(), estimates=None, actual=None):
    estimates = estimates or {resource: duration}
    actual = actual or estimates
    return Node(name, tuple(Duration(r, e, actual[r]) for r, e in estimates.items()),
                tuple(Dependency(p, size) for p, size in predecessors))


def hand_dag():
    h = Service("H-hand", 0, 13, "H", (
        node("a", duration=2),
        node("b", "GPU0", 3, (("a", 1),)),
        node("c", "CPU1", 2, (("a", 0),)),
        node("d", "NPU0", 2, (("b", 1), ("c", 2))),
        node("e", "CPU0", 1, (("c", 1),)),
        node("f", "GPU0", 1, (("d", 1),)),
        node("g", "CPU2", 1, (("d", 0), ("e", 0))),
        node("h", "CPU0", 1, (("f", 1), ("g", 1))),
    ))
    l = Service("L-hand", 0, 12, "L", (node("l", "CPU3", 13),))
    return Workload((h, l), network())


HAND_INTERVALS = {"a": (0, 2), "b": (3, 6), "c": (2, 4), "d": (7, 9),
                  "e": (5, 6), "f": (10, 11), "g": (9, 10), "h": (12, 13), "l": (0, 13)}


def priority():
    return Workload((Service("H", 0, 10, "H", (node("H-root", duration=2),)),
                     Service("L", 0, 3, "L", (node("L-root", duration=2),))), network())


def simultaneous():
    return Workload((Service("early", 0, 2, "H", (node("early-root", duration=2),)),
                     Service("new", 2, 1, "L", (node("new-root"),))), network())


def wait_scan():
    # At t=1 the best map of 'waiting' is busy CPU0 (predicted finish 6),
    # versus idle GPU0 (finish 21). Unrelated lower-priority work must start.
    return Workload((Service("occupier", 0, 5, "H", (node("busy", duration=5),)),
                     Service("waiting", 1, 8, "H", (node("wait", estimates={"CPU0": 1, "GPU0": 20}),)),
                     Service("other", 1, 50, "L", (node("other-node", "GPU0", 2),))), network())


def overrun():
    return Workload((Service("running", 0, 10, "H", (node("overrun", estimates={"CPU0": 1}, actual={"CPU0": 5}),)),
                     Service("later", 2, 10, "L", (node("later-node", estimates={"CPU0": 1, "GPU0": 10}),))), network())


def oeft_choice():
    # HEFT selects root CPU0 (EFT1). PEFT selects GPU0 (EFT2+OCT1)
    # versus CPU0 (EFT1+OCT3), because child GPU is fast and edge costs 10.
    return Workload((Service("oeft", 0, 100, "H", (
        node("parent", estimates={"CPU0": 1, "GPU0": 2}),
        node("child", predecessors=(("parent", 10),), estimates={"CPU0": 3, "GPU0": 1}),)),), network())


def remapping():
    # Parent done CPU0 at 1. Child initially favors busy NPU until an arrival
    # competes; destination-specific transfer must never be copied from CPU.
    return Workload((Service("copies", 0, 100, "H", (
        node("producer", duration=1),
        node("consumer", predecessors=(("producer", 3),), estimates={"CPU0": 20, "GPU0": 1, "NPU0": 2}),)),
        Service("gpu-user", 2, 1, "H", (node("gpu-load", "GPU0", 4),))), network())


def fixture_cases():
    return {"hand_dag": hand_dag(), "priority": priority(), "simultaneous": simultaneous(),
            "wait_scan": wait_scan(), "overrun": overrun(), "oeft_choice": oeft_choice(),
            "remapping": remapping(), "empty": Workload((), network()),
            "minimal": Workload((Service("one", 0, 1, "H", (node("one-node"),)),), network())}

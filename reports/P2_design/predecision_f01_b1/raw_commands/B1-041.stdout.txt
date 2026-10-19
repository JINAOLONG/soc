"""Immutable offline input records. Realized costs never belong in public views."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math


class ModelError(ValueError):
    pass


def number(value: float, name: str, *, positive: bool = False) -> None:
    if (isinstance(value, bool) or not isinstance(value, (int, float)) or
            not math.isfinite(value) or (value <= 0 if positive else value < 0)):
        raise ModelError(f"invalid {name}: expected finite {'positive' if positive else 'nonnegative'} number")


def identity(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ModelError("identity must be a nonempty string")


@dataclass(frozen=True, slots=True)
class Resource:
    id: str
    kind: str

    def __post_init__(self):
        identity(self.id)
        if self.kind not in {"CPU", "GPU", "NPU"}:
            raise ModelError("unknown resource kind")


@dataclass(frozen=True, slots=True)
class Duration:
    resource: str
    estimate: float
    realized: float

    def __post_init__(self):
        identity(self.resource)
        number(self.estimate, "estimated duration", positive=True)
        number(self.realized, "realized duration", positive=True)


@dataclass(frozen=True, slots=True)
class Dependency:
    node: str
    size: float

    def __post_init__(self):
        identity(self.node)
        number(self.size, "edge size")


@dataclass(frozen=True, slots=True)
class Node:
    id: str
    durations: tuple[Duration, ...]
    predecessors: tuple[Dependency, ...] = ()

    def __post_init__(self):
        identity(self.id)
        object.__setattr__(self, "durations", tuple(self.durations))
        object.__setattr__(self, "predecessors", tuple(self.predecessors))
        if not self.durations or any(not isinstance(x, Duration) for x in self.durations):
            raise ModelError("empty/invalid compatible duration set")
        if len({x.resource for x in self.durations}) != len(self.durations):
            raise ModelError("duplicate resource duration")
        if any(not isinstance(x, Dependency) for x in self.predecessors):
            raise ModelError("invalid dependency")
        if len({x.node for x in self.predecessors}) != len(self.predecessors):
            raise ModelError("duplicate predecessor")

    def cost(self, resource: str) -> Duration:
        for row in self.durations:
            if row.resource == resource:
                return row
        raise ModelError("incompatible resource")


@dataclass(frozen=True, slots=True)
class Service:
    id: str
    arrival: float
    relative_deadline: float
    group: str
    nodes: tuple[Node, ...]

    def __post_init__(self):
        identity(self.id)
        number(self.arrival, "arrival")
        number(self.relative_deadline, "relative deadline", positive=True)
        number(self.arrival + self.relative_deadline, "absolute deadline", positive=True)
        if self.group not in {"H", "L"}:
            raise ModelError("group must be H or L")
        object.__setattr__(self, "nodes", tuple(self.nodes))
        if not self.nodes or any(not isinstance(n, Node) for n in self.nodes):
            raise ModelError("empty/invalid service DAG")
        topological_order(self)

    @property
    def deadline(self) -> float:
        return self.arrival + self.relative_deadline


def topological_order(service: Service) -> tuple[str, ...]:
    nodes = {n.id: n for n in service.nodes}
    if len(nodes) != len(service.nodes):
        raise ModelError("duplicate node identity")
    for n in service.nodes:
        if any(e.node not in nodes for e in n.predecessors):
            raise ModelError("missing predecessor")
    done = []
    remaining = set(nodes)
    while remaining:
        ready = sorted(n for n in remaining if all(e.node in done for e in nodes[n].predecessors))
        if not ready:
            raise ModelError("cyclic DAG")
        done.extend(ready)
        remaining.difference_update(ready)
    return tuple(done)


@dataclass(frozen=True, slots=True)
class Link:
    source: str
    destination: str
    latency: float
    bandwidth: float

    def __post_init__(self):
        if self.source not in {"CPU", "GPU", "NPU"} or self.destination not in {"CPU", "GPU", "NPU"}:
            raise ModelError("invalid link type")
        number(self.latency, "latency")
        number(self.bandwidth, "bandwidth", positive=True)


DEFAULT_RESOURCES = tuple(Resource(f"CPU{i}", "CPU") for i in range(4)) + (
    Resource("GPU0", "GPU"), Resource("NPU0", "NPU"))


@dataclass(frozen=True, slots=True)
class Workload:
    services: tuple[Service, ...]
    links: tuple[Link, ...]
    resources: tuple[Resource, ...] = DEFAULT_RESOURCES

    def __post_init__(self):
        for field in ("services", "links", "resources"):
            object.__setattr__(self, field, tuple(getattr(self, field)))
        if any(not isinstance(x, Service) for x in self.services):
            raise ModelError("invalid service")
        if any(not isinstance(x, Resource) for x in self.resources):
            raise ModelError("invalid resource")
        if len(set(r.id for r in self.resources)) != len(self.resources):
            raise ModelError("duplicate resource identity")
        if set(self.resources) != set(DEFAULT_RESOURCES):
            raise ModelError("model requires CPU0..3, GPU0, NPU0")
        if len({s.id for s in self.services}) != len(self.services):
            raise ModelError("duplicate service identity")
        nodes = [n for s in self.services for n in s.nodes]
        if len({n.id for n in nodes}) != len(nodes):
            raise ModelError("node identities must be globally unique")
        ids = {r.id for r in self.resources}
        if any(d.resource not in ids for n in nodes for d in n.durations):
            raise ModelError("duration references unknown resource")
        if any(not isinstance(x, Link) for x in self.links):
            raise ModelError("invalid link")
        pairs = {(x.source, x.destination) for x in self.links}
        if len(pairs) != len(self.links) or pairs != {(a, b) for a in ("CPU", "GPU", "NPU") for b in ("CPU", "GPU", "NPU")}:
            raise ModelError("network requires exactly nine directed type pairs")

    def to_dict(self) -> dict:
        return {"schema_version": 1, "origin": "HAND_AUTHORED_CORRECTNESS_FIXTURE", **asdict(self)}

    @classmethod
    def from_dict(cls, value: dict) -> Workload:
        if value.get("schema_version") != 1 or value.get("origin") != "HAND_AUTHORED_CORRECTNESS_FIXTURE":
            raise ModelError("unsupported input identity")
        services = tuple(Service(s["id"], s["arrival"], s["relative_deadline"], s["group"],
                                 tuple(Node(n["id"], tuple(Duration(**d) for d in n["durations"]),
                                            tuple(Dependency(**e) for e in n["predecessors"])) for n in s["nodes"]))
                         for s in value["services"])
        return cls(services, tuple(Link(**x) for x in value["links"]),
                   tuple(Resource(**x) for x in value["resources"]))


def canonical_bytes(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def communication(workload: Workload, source: str, destination: str, size: float) -> float:
    number(size, "edge size")
    kinds = {r.id: r.kind for r in workload.resources}
    if source not in kinds or destination not in kinds:
        raise ModelError("unknown transfer resource")
    if source == destination:
        return 0.0
    link = next(x for x in workload.links if (x.source, x.destination) == (kinds[source], kinds[destination]))
    delay = link.latency + size / link.bandwidth
    number(delay, "transfer duration")
    return delay

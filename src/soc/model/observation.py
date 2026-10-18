"""Public DTOs constructed by projection, not wrappers around offline state."""
from dataclasses import dataclass

from soc.model.schema import Workload, ModelError, Resource, Link, number


@dataclass(frozen=True, slots=True)
class PublicNode:
    id: str
    estimates: tuple[tuple[str, float], ...]
    predecessors: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class PublicService:
    id: str
    arrival: float
    deadline: float
    group: str
    nodes: tuple[PublicNode, ...]


@dataclass(frozen=True, slots=True)
class Running:
    service: str
    node: str
    resource: str
    start: float
    elapsed: float


@dataclass(frozen=True, slots=True)
class Completed:
    service: str
    node: str
    resource: str
    finish: float


@dataclass(frozen=True, slots=True)
class Observation:
    now: float
    services: tuple[PublicService, ...]
    running: tuple[Running, ...]
    completed: tuple[Completed, ...]
    resources: tuple[Resource, ...]
    links: tuple[Link, ...]


def observe(workload: Workload, now: float, running: tuple[Running, ...] = (),
            completed: tuple[Completed, ...] = ()) -> Observation:
    """Project only supplied observable facts; no queued completion input exists."""
    number(now, "observation time")
    services = tuple(PublicService(s.id, s.arrival, s.deadline, s.group,
                                 tuple(PublicNode(n.id, tuple(sorted((d.resource, d.estimate) for d in n.durations)),
                                                  tuple(sorted((e.node, e.size) for e in n.predecessors)))
                                       for n in sorted(s.nodes, key=lambda n: n.id)))
                     for s in sorted(workload.services, key=lambda s: s.id) if s.arrival <= now)
    visible = {(s.id, n.id): n for s in services for n in s.nodes}
    used = set()
    busy = set()
    for row in (*running, *completed):
        if type(row) not in (Running, Completed) or (row.service, row.node) not in visible:
            raise ModelError("status is not a visible task")
        key = row.service, row.node
        if key in used or row.resource not in dict(visible[key].estimates):
            raise ModelError("duplicate status or incompatible assignment")
        used.add(key)
        if isinstance(row, Running):
            number(row.start, "running start")
            number(row.elapsed, "running elapsed")
            if row.start > now or row.elapsed != now - row.start or row.resource in busy:
                raise ModelError("invalid running observation")
            busy.add(row.resource)
        else:
            number(row.finish, "observed completion")
            if row.finish > now:
                raise ModelError("future completion cannot be observed")
        arrival = next(s.arrival for s in services if s.id == row.service)
        if (row.start if isinstance(row, Running) else row.finish) < arrival:
            raise ModelError("observation predates arrival")
    key = lambda r: (r.service, r.node, r.resource)
    return Observation(now, services, tuple(sorted(running, key=key)), tuple(sorted(completed, key=key)),
                       tuple(sorted(workload.resources, key=lambda r: r.id)),
                       tuple(sorted(workload.links, key=lambda r: (r.source, r.destination))))


def dependency_ready(view: Observation) -> tuple[tuple[str, str], ...]:
    finished = {r.node for r in view.completed}
    occupied = {r.node for r in (*view.completed, *view.running)}
    return tuple((s.id, n.id) for s in view.services for n in s.nodes
                 if n.id not in occupied and all(p in finished for p, _ in n.predecessors))

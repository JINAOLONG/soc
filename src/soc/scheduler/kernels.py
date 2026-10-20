"""Source equation kernels and explicit P1 online adaptation. No private input."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import isfinite

from soc.model.observation import Observation, PublicNode, dependency_ready


def _finite_number(value) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and isfinite(value)


def insertion_start(ready: float, duration: float, intervals: tuple[tuple[float, float], ...]) -> float:
    """Earliest entire idle gap; not append-only. Touching endpoints are legal."""
    if not _finite_number(ready) or ready < 0 or not _finite_number(duration) or duration <= 0:
        raise ValueError("invalid insertion input")
    start = ready
    last = 0.0
    for left, right in sorted(intervals):
        if not _finite_number(left) or not _finite_number(right) or left < last or right <= left:
            raise ValueError("invalid/overlapping occupied intervals")
        last = right
        if start + duration <= left:
            # Remaining intervals must also be valid: validate separately below.
            break
        if start < right:
            start = right
    prior = 0.0
    for left, right in sorted(intervals):
        if not _finite_number(left) or not _finite_number(right) or left < prior or right <= left:
            raise ValueError("invalid/overlapping occupied intervals")
        prior = right
    return start


def source_tables(costs: dict[str, dict[str, float]],
                  successors: dict[str, tuple[str, ...]],
                  edge_means: dict[tuple[str, str], float]) -> tuple[dict, dict, dict]:
    """HEFT Eq8/9, PEFT Eq7/8. Supplied means avoid inventing source averaging.

    Complete matrices reproduce source definitions. Ragged matrices implement
    the user-approved compatible-row extension D2, not original static HEFT/PEFT.
    No availability argument exists: OCT cannot incorporate resource availability.
    """
    if not costs or set(successors) != set(costs):
        raise ValueError("incomplete graph")
    for row in costs.values():
        if not row or any(not _finite_number(v) or v <= 0 for v in row.values()):
            raise ValueError("invalid execution matrix")
    edges = {(u, v) for u, children in successors.items() for v in children}
    if any(v not in costs for _, v in edges) or edges != set(edge_means):
        raise ValueError("invalid edge identity")
    if any(not _finite_number(c) or c < 0 for c in edge_means.values()):
        raise ValueError("invalid mean edge cost")
    rank, oct_table, oct_rank = {}, {}, {}
    todo = set(costs)
    while todo:
        ready = sorted(u for u in todo if all(v in rank for v in successors[u]))
        if not ready:
            raise ValueError("cyclic graph")
        for u in ready:
            rank[u] = sum(costs[u].values()) / len(costs[u]) + max(
                (edge_means[u, v] + rank[v] for v in successors[u]), default=0.0)
            oct_table[u] = {p: max((min(oct_table[v][q] + costs[v][q] +
                                              (0 if p == q else edge_means[u, v])
                                              for q in costs[v])
                                    for v in successors[u]), default=0.0) for p in costs[u]}
            oct_rank[u] = sum(oct_table[u].values()) / len(oct_table[u])
            todo.remove(u)
    if any(not isfinite(v) for v in rank.values()) or any(not isfinite(v) for row in oct_table.values() for v in row.values()):
        raise ValueError("overflow in source table")
    return rank, oct_table, oct_rank


def transfer(view: Observation, source: str, destination: str, size: float) -> float:
    if source == destination:
        return 0.0
    kinds = {r.id: r.kind for r in view.resources}
    link = next(x for x in view.links if (x.source, x.destination) == (kinds[source], kinds[destination]))
    return link.latency + size / link.bandwidth


def mean_transfer(view: Observation, parent: PublicNode, child: PublicNode, size: float) -> float:
    """Approved D3: separately average L and B across distinct compatible units."""
    kinds = {r.id: r.kind for r in view.resources}
    links = {(x.source, x.destination): x for x in view.links}
    pairs = [links[kinds[p], kinds[q]] for p, _ in parent.estimates
             for q, _ in child.estimates if p != q]
    if not pairs:
        return 0.0
    return sum(x.latency for x in pairs)/len(pairs) + size/(sum(x.bandwidth for x in pairs)/len(pairs))


@lru_cache(maxsize=512)
def _service_tables(service, resources, links):
    # Only immutable arrived public data enter this cache. Cache values are
    # immutable too, so callers cannot alter later scheduling through a table.
    view = Observation(0.0, (service,), (), (), resources, links)
    nodes = {n.id: n for n in service.nodes}
    children = {n: tuple(sorted(child.id for child in service.nodes
                                if any(p == n for p, _ in child.predecessors))) for n in nodes}
    means = {(p, n.id): mean_transfer(view, nodes[p], n, size)
             for n in service.nodes for p, size in n.predecessors}
    rank, oct_table, oct_rank = source_tables({n.id: dict(n.estimates) for n in service.nodes}, children, means)
    return tuple(rank.items()), tuple((n, tuple(row.items())) for n, row in oct_table.items()), tuple(oct_rank.items())


def online_tables(view: Observation) -> tuple[dict, dict, dict]:
    """Refresh each decision from complete *arrived*, public DAGs and estimates."""
    all_rank, all_oct, all_oct_rank = {}, {}, {}
    for service in view.services:
        rank, oct_table, oct_rank = _service_tables(service, view.resources, view.links)
        all_rank.update(rank)
        all_oct.update((n, dict(row)) for n, row in oct_table)
        all_oct_rank.update(oct_rank)
    return all_rank, all_oct, all_oct_rank


@dataclass(frozen=True, slots=True)
class Proposal:
    service: str
    node: str
    resource: str
    estimated_start: float
    eft: float
    score: float
    feasible_now: bool


def predictions(view: Observation, service_id: str, node_id: str, oct_row: dict | None = None) -> tuple[Proposal, ...]:
    if (service_id, node_id) not in dependency_ready(view):
        raise ValueError("candidate must be dependency-ready")
    service = next(s for s in view.services if s.id == service_id)
    node = next(n for n in service.nodes if n.id == node_id)
    completed = {r.node: r for r in view.completed}
    busy = {r.resource: r for r in view.running}
    node_index = {n.id: n for s in view.services for n in s.nodes}
    proposals = []
    for resource, duration in node.estimates:
        data = max((completed[p].finish + transfer(view, completed[p].resource, resource, size)
                    for p, size in node.predecessors), default=service.arrival)
        occupied = ()
        if resource in busy:
            running = busy[resource]
            estimate = dict(node_index[running.node].estimates)[resource]
            release = view.now + max(0.0, estimate-running.elapsed)
            if release > view.now:
                occupied = ((view.now, release),)
        start = insertion_start(max(view.now, data), duration, occupied)
        eft = start + duration
        score = eft + (oct_row[resource] if oct_row is not None else 0)
        if not isfinite(score):
            raise ValueError("nonfinite predicted score")
        proposals.append(Proposal(service_id, node_id, resource, start, eft, score,
                                  resource not in busy and data <= view.now))
    return tuple(sorted(proposals, key=lambda p: (p.score, p.resource)))


def ordered_ready(view: Observation, method: str, *, _tables=None) -> tuple[tuple[str, str], ...]:
    if method not in {"B1", "B2", "B3", "B4", "B5"}:
        raise ValueError("unknown baseline")
    rank, _, oct_rank = (_tables if _tables is not None else online_tables(view)) if method in {"B3", "B4", "B5"} else ({}, {}, {})
    services = {s.id: s for s in view.services}
    def key(pair):
        s, n = pair
        service = services[s]
        if method == "B1":
            return service.deadline, s, n
        if method == "B2":
            return service.group != "H", service.deadline, s, n
        if method == "B3":
            return -rank[n], s, n
        if method == "B4":
            return -oct_rank[n], s, n
        return service.group != "H", -oct_rank[n], s, n
    return tuple(sorted(dependency_ready(view), key=key))


def choose(view: Observation, method: str) -> Proposal | None:
    """D5: best mapping may wait; continue scanning others; reserve nothing."""
    if method not in {"B1", "B2", "B3", "B4", "B5"}: raise ValueError('unknown baseline')
    ready_services={s for s,n in dependency_ready(view)}
    if not ready_services: return None
    # Rank/OCT recurrences are entirely within one arrived service graph.
    # Only services with a ready candidate need their unchanged source tables;
    # predictions still receive the whole public running/completed view.
    rank_view=Observation(view.now,tuple(s for s in view.services if s.id in ready_services),
                          (),(),view.resources,view.links)
    tables=online_tables(rank_view) if method in {'B3','B4','B5'} else ({},{},{})
    _, oct_table, _ = tables
    for service, node in ordered_ready(view, method, _tables=tables):
        proposals = predictions(view, service, node, oct_table[node] if method in {"B4", "B5"} else None)
        if proposals[0].feasible_now:
            return proposals[0]
    return None

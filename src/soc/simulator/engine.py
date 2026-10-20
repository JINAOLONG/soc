"""D1 event engine. The only scheduler call argument is an immutable Observation."""
from __future__ import annotations

from dataclasses import asdict
import heapq
from typing import Callable

from soc.model.schema import Workload, ModelError, communication, number
from soc.model.observation import Observation, Running, Completed, observe, dependency_ready, _public_service
from soc.scheduler.kernels import Proposal, choose
from soc.metrics.fixture import summarize


class DeadlockError(RuntimeError):
    pass


def simulate(workload: Workload, method: str,
             policy: Callable[[Observation], Proposal | None] | None = None,
             *, compact_decisions: bool = False) -> dict:
    """Execute only the supplied input; never derive a seed or materialize a job.

    Optional policies are for synthetic negative tests. Normal B1–B5 accept only
    public observations. This function exposes no queue or realized duration to
    the policy, and makes no performance/host-timing claims.
    """
    if method not in {"B1", "B2", "B3", "B4", "B5"}:
        raise ValueError("unknown baseline")
    queue = [(s.arrival, 1, s.id, "", "") for s in workload.services]
    heapq.heapify(queue)
    services = {s.id: s for s in workload.services}
    nodes = {(s.id, n.id): n for s in workload.services for n in s.nodes}
    running: dict[tuple[str, str], dict] = {}
    completed: dict[tuple[str, str], Completed] = {}
    events, executions, decisions = [], [], []
    now = 0.0
    public_projection = tuple(_public_service(s) for s in sorted(workload.services,key=lambda s:s.id))
    controller = policy if policy is not None else lambda view: choose(view, method)
    while queue or running or len(completed) < len(nodes):
        # Full batches are drained before the first observation at this time.
        while queue and queue[0][0] == now:
            at, phase, service, node, resource = heapq.heappop(queue)
            if phase == 0:
                row = running.pop((service, node))
                completed[service, node] = Completed(service, node, resource, at)
                events.append(dict(time=at, kind="complete", service=service, node=node, resource=resource))
            else:
                events.append(dict(time=at, kind="arrival", service=service, node="", resource=""))
        while True:
            view = observe(workload, now,
                           tuple(Running(s, n, r["resource"], r["start"], now-r["start"])
                                 for (s, n), r in running.items()), tuple(completed.values()),
                           _projection=public_projection)
            proposal = controller(view)
            decision = dict(time=now, proposal=asdict(proposal) if proposal is not None else None)
            if not compact_decisions:
                decision['observation'] = asdict(view)
            decisions.append(decision)
            if proposal is None:
                break
            key = proposal.service, proposal.node
            if key not in dependency_ready(view):
                raise ModelError("policy attempted non-ready/duplicate task")
            node = nodes[key]
            cost = node.cost(proposal.resource)
            if any(r["resource"] == proposal.resource for r in running.values()):
                raise ModelError("policy attempted occupied resource")
            for edge in node.predecessors:
                pred = completed[proposal.service, edge.node]
                if now < pred.finish + communication(workload, pred.resource, proposal.resource, edge.size):
                    raise ModelError("policy attempted start before data ready")
            finish = now + cost.realized
            number(finish, "actual completion", positive=True)
            if finish <= now:
                raise ModelError("duration below representable virtual-time resolution")
            row = dict(service=proposal.service, node=proposal.node, resource=proposal.resource,
                       start=now, finish=finish)
            running[key] = row
            executions.append(row.copy())
            events.append(dict(time=now, kind="start", service=proposal.service,
                               node=proposal.node, resource=proposal.resource))
            heapq.heappush(queue, (finish, 0, proposal.service, proposal.node, proposal.resource))
        if len(completed) == len(nodes) and not queue:
            break
        # Data arrival is a wakeup, not a fabricated resource reservation.
        wakeups = []
        busy = {r["resource"] for r in running.values()}
        for service, node_id in dependency_ready(view):
            node = nodes[service, node_id]
            for cost in node.durations:
                if cost.resource in busy:
                    continue
                ready = max((completed[service, e.node].finish + communication(
                    workload, completed[service, e.node].resource, cost.resource, e.size)
                    for e in node.predecessors), default=services[service].arrival)
                if ready > now:
                    wakeups.append(ready)
        candidates = ([queue[0][0]] if queue else []) + wakeups
        if not candidates:
            raise DeadlockError("unfinished admitted nodes, no legal start or future event/data wakeup")
        next_time = min(candidates)
        if next_time <= now:
            raise DeadlockError("event progression failed")
        now = next_time
    return dict(schema_version=1, origin="HAND_AUTHORED_CORRECTNESS_FIXTURE", method=method,
                executions=executions, events=events, decisions=decisions,
                metrics=summarize(workload, executions))

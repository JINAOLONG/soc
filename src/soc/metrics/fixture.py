"""Service metrics for hand-authored correctness inputs; no scientific aggregation."""
import math

from soc.model.schema import Workload, ModelError, communication


def quantile(values: list[float], p: float) -> float | None:
    if not 0 <= p <= 1 or isinstance(p, bool):
        raise ValueError("invalid probability")
    if not values:
        return None
    if any(isinstance(x, bool) or not math.isfinite(x) or x < 0 for x in values):
        raise ValueError("invalid response")
    ordered = sorted(values)
    h = (len(ordered) - 1) * p
    lo, hi = math.floor(h), math.ceil(h)
    return ordered[lo] + (h-lo)*(ordered[hi]-ordered[lo])


def summarize(workload: Workload, executions: list[dict]) -> dict:
    expected = {(s.id, n.id) for s in workload.services for n in s.nodes}
    rows = {(r["service"], r["node"]): r for r in executions}
    if len(rows) != len(executions) or rows.keys() != expected:
        raise ModelError("metrics require exactly one execution per admitted node")
    services = []
    for s in sorted(workload.services, key=lambda s: s.id):
        finishes = [rows[s.id, n.id]["finish"] for n in s.nodes]
        if any(isinstance(f, bool) or not math.isfinite(f) or f < s.arrival for f in finishes):
            raise ModelError("invalid completion for metrics")
        finish = max(finishes)
        services.append(dict(service=s.id, group=s.group, finish=finish,
                             response=finish-s.arrival, missed=finish > s.deadline))
    groups = {}
    for g in ("H", "L"):
        group = [r for r in services if r["group"] == g]
        responses = [r["response"] for r in group]
        groups[g] = dict(count=len(group), dmr=sum(r["missed"] for r in group)/len(group) if group else None,
                         p50=quantile(responses, .50), p95=quantile(responses, .95),
                         p99=quantile(responses, .99), maximum=max(responses) if responses else None)
    makespan = max((r["finish"] for r in executions), default=0)
    resources = {}
    for resource in workload.resources:
        busy = sum(r["finish"]-r["start"] for r in executions if r.get("resource") == resource.id)
        resources[resource.id] = dict(busy=busy, utilization=busy/makespan if makespan else None)
    transfers, waiting = [], []
    for s in sorted(workload.services, key=lambda s: s.id):
        for n in sorted(s.nodes, key=lambda n: n.id):
            row = rows[s.id, n.id]
            dependency_time = max((rows[s.id, e.node]["finish"] for e in n.predecessors), default=s.arrival)
            data_time = dependency_time
            for edge in n.predecessors:
                pred = rows[s.id, edge.node]
                delay = communication(workload, pred["resource"], row["resource"], edge.size)
                ready = pred["finish"]+delay
                data_time = max(data_time, ready)
                transfers.append(dict(service=s.id, predecessor=edge.node, node=n.id,
                                      source=pred["resource"], destination=row["resource"], size=edge.size,
                                      start=pred["finish"], ready=ready, delay=delay))
            waiting.append(dict(service=s.id, node=n.id, dependency_ready=dependency_time, data_ready=data_time,
                                dependency_wait=dependency_time-s.arrival, communication_wait=data_time-dependency_time,
                                ready_wait=row["start"]-data_time))
    return dict(services=services, groups=groups, makespan=makespan,
                overall_mean_response=sum(r["response"] for r in services)/len(services) if services else None,
                resources=resources, transfers=transfers, waiting=waiting,
                cross_unit_data_total=sum(t["size"] for t in transfers if t["source"] != t["destination"]))

"""Offline independent oracle; imports neither engine nor runtime metric/kernel code.

Only immutable input records are shared. All timing, transfer, occupancy,
event ordering and metric calculations are independently implemented here.
"""
from __future__ import annotations

from collections import Counter
import math

from soc.model.schema import Workload


def _numeric(value) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value) and value >= 0


def _summary(workload: Workload, rows: dict) -> dict:
    services = []
    for s in sorted(workload.services, key=lambda s: s.id):
        finish = max(rows[s.id, n.id]["finish"] for n in s.nodes)
        services.append({"service": s.id, "group": s.group, "finish": finish,
                         "response": finish-s.arrival, "missed": not finish <= s.arrival+s.relative_deadline})
    groups = {}
    for group in ("H", "L"):
        selected = [s for s in services if s["group"] == group]
        values = sorted(s["response"] for s in selected)
        def percentile(p):
            if not values:
                return None
            position = (len(values)-1)*p
            i = int(position)
            return values[i]+(position-i)*(values[min(i+1, len(values)-1)]-values[i])
        groups[group] = dict(count=len(values), dmr=sum(s["missed"] for s in selected)/len(values) if values else None,
                             p50=percentile(.50), p95=percentile(.95), p99=percentile(.99),
                             maximum=values[-1] if values else None)
    makespan = max((r["finish"] for r in rows.values()), default=0)
    resources = {}
    for unit in workload.resources:
        busy = sum(r["finish"]-r["start"] for r in rows.values() if r["resource"] == unit.id)
        resources[unit.id] = {"busy": busy, "utilization": busy/makespan if makespan else None}
    kinds = {r.id: r.kind for r in workload.resources}
    links = {(l.source, l.destination): l for l in workload.links}
    transfers, waiting = [], []
    for s in sorted(workload.services, key=lambda s: s.id):
        for n in sorted(s.nodes, key=lambda n: n.id):
            row = rows[s.id, n.id]
            dep = max((rows[s.id, e.node]["finish"] for e in n.predecessors), default=s.arrival)
            data = dep
            for e in n.predecessors:
                parent = rows[s.id, e.node]
                if parent["resource"] == row["resource"]:
                    delay = 0.0
                else:
                    link = links[kinds[parent["resource"]], kinds[row["resource"]]]
                    delay = link.latency+e.size/link.bandwidth
                ready = parent["finish"]+delay
                data = max(data, ready)
                transfers.append({"service": s.id, "predecessor": e.node, "node": n.id,
                                  "source": parent["resource"], "destination": row["resource"], "size": e.size,
                                  "start": parent["finish"], "ready": ready, "delay": delay})
            waiting.append({"service": s.id, "node": n.id, "dependency_ready": dep, "data_ready": data,
                            "dependency_wait": dep-s.arrival, "communication_wait": data-dep,
                            "ready_wait": row["start"]-data})
    return {"services": services, "groups": groups, "makespan": makespan,
            "overall_mean_response": sum(r["response"] for r in services)/len(services) if services else None,
            "resources": resources, "transfers": transfers, "waiting": waiting,
            "cross_unit_data_total": sum(t["size"] for t in transfers if t["source"] != t["destination"])}


def validate_trace(workload: Workload, trace: dict) -> dict:
    errors = []
    def error(code, detail):
        errors.append({"code": code, "detail": str(detail)})
    if not isinstance(trace, dict) or trace.get("schema_version") != 1 or trace.get("origin") != "HAND_AUTHORED_CORRECTNESS_FIXTURE":
        return {"status": "FAIL", "errors": [{"code": "SCHEMA", "detail": "unsupported trace"}], "metrics": None}
    executions, events = trace.get("executions"), trace.get("events")
    if not isinstance(executions, list) or not isinstance(events, list):
        return {"status": "FAIL", "errors": [{"code": "SCHEMA", "detail": "executions/events must be lists"}], "metrics": None}
    nodes = {(s.id, n.id): (s, n) for s in workload.services for n in s.nodes}
    resources = {r.id: r.kind for r in workload.resources}
    links = {(x.source, x.destination): x for x in workload.links}
    rows = {}
    for row in executions:
        if (not isinstance(row, dict) or set(row) != {"service", "node", "resource", "start", "finish"} or
                any(not isinstance(row[k], str) for k in ("service", "node", "resource")) or
                not _numeric(row["start"]) or not _numeric(row["finish"]) or row["finish"] <= row["start"]):
            error("INTERVAL", row)
            continue
        key = row["service"], row["node"]
        if key in rows:
            error("DUPLICATE_EXECUTION", key)
            continue
        if key not in nodes:
            error("UNKNOWN_TASK", key)
            continue
        rows[key] = row
        service, node = nodes[key]
        duration = next((d for d in node.durations if d.resource == row["resource"]), None)
        if row["resource"] not in resources or duration is None:
            error("COMPATIBILITY", key)
        elif row["finish"] != row["start"] + duration.realized:
            error("DURATION", key)
        if row["start"] < service.arrival:
            error("ARRIVAL", key)
    if rows.keys() != nodes.keys():
        error("FULL_DRAIN", sorted(nodes.keys()-rows.keys()))
    for key, row in rows.items():
        service, node = nodes[key]
        for edge in node.predecessors:
            parent = rows.get((service.id, edge.node))
            if parent is None:
                error("PREDECESSOR_MISSING", key)
                continue
            if row["start"] < parent["finish"]:
                error("PRECEDENCE", key)
            if parent["resource"] in resources and row["resource"] in resources:
                if parent["resource"] == row["resource"]:
                    delay = 0.0
                else:
                    link = links[resources[parent["resource"]], resources[row["resource"]]]
                    delay = link.latency + edge.size/link.bandwidth
                if row["start"] < parent["finish"] + delay:
                    error("DATA_READINESS", key)
    for resource in resources:
        occupied = sorted((r["start"], r["finish"], key) for key, r in rows.items() if r["resource"] == resource)
        for previous, following in zip(occupied, occupied[1:]):
            if following[0] < previous[1]:
                error("RESOURCE_OVERLAP", (resource, previous[2], following[2]))
    actual_events = Counter()
    last_time = -1.0
    last_phase = -1
    for event in events:
        if (not isinstance(event, dict) or set(event) != {"time", "kind", "service", "node", "resource"} or
                not _numeric(event["time"]) or any(not isinstance(event[k], str) for k in ("kind", "service", "node", "resource")) or
                event["kind"] not in {"arrival", "start", "complete"}):
            error("EVENT_SCHEMA", event)
            continue
        phase = {"complete": 0, "arrival": 1, "start": 2}[event["kind"]]
        if event["time"] < last_time or (event["time"] == last_time and phase < last_phase):
            error("EVENT_ORDER", event)
        if event["time"] != last_time:
            last_phase = -1
        last_time, last_phase = event["time"], phase
        actual_events[(event["time"], event["kind"], event["service"], event["node"], event["resource"])] += 1
    expected_events = Counter((s.arrival, "arrival", s.id, "", "") for s in workload.services)
    for (s, n), r in rows.items():
        expected_events[(r["start"], "start", s, n, r["resource"])] += 1
        expected_events[(r["finish"], "complete", s, n, r["resource"])] += 1
    if expected_events != actual_events:
        error("EVENT_ACCOUNTING", "arrival/start/complete events must exactly match all executions")
    summary = None
    if not errors:
        summary = _summary(workload, rows)
        if trace.get("metrics") != summary:
            error("METRIC_MISMATCH", "independent service/quantile/deadline recomputation differs")
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "metrics": summary}

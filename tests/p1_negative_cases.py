"""Explicit malicious trace mutations with independently specified rejection codes."""
import copy


def negative_cases(valid):
    cases = []
    def add(name, code, change):
        trace = copy.deepcopy(valid)
        change(trace)
        cases.append((name, code, trace))
    def edit(trace, node, **fields):
        next(r for r in trace["executions"] if r["node"] == node).update(fields)
    add("duplicate_execution", "DUPLICATE_EXECUTION", lambda t: t["executions"].append(t["executions"][0].copy()))
    add("missing_node_no_drain", "FULL_DRAIN", lambda t: t["executions"].pop())
    add("unknown_node", "UNKNOWN_TASK", lambda t: t["executions"][0].update(node="unknown"))
    add("incompatible_resource", "COMPATIBILITY", lambda t: edit(t, "a", resource="GPU0"))
    add("unknown_resource", "COMPATIBILITY", lambda t: edit(t, "a", resource="CPU999"))
    add("wrong_duration", "DURATION", lambda t: edit(t, "a", finish=1))
    add("predecessor_not_finished", "PRECEDENCE", lambda t: edit(t, "b", start=1, finish=4))
    add("data_not_arrived", "DATA_READINESS", lambda t: edit(t, "b", start=2, finish=5))
    add("resource_overlap", "RESOURCE_OVERLAP", lambda t: edit(t, "e", start=1, finish=2))
    add("unaccounted_arrival", "EVENT_ACCOUNTING", lambda t: t["events"].remove(next(e for e in t["events"] if e["kind"] == "arrival")))
    add("duplicate_start_preemption", "EVENT_ACCOUNTING", lambda t: t["events"].append(next(e for e in t["events"] if e["kind"] == "start").copy()))
    add("migration_event", "EVENT_ACCOUNTING", lambda t: next(e for e in t["events"] if e["kind"] == "complete").update(resource="GPU0"))
    add("nonnumeric_nan_interval", "INTERVAL", lambda t: t["executions"][0].update(start="NaN"))
    add("invalid_interval", "INTERVAL", lambda t: t["executions"][0].update(start=3, finish=2))
    add("out_of_order_event", "EVENT_ORDER", lambda t: t["events"].reverse())
    add("false_deadline_equality_miss", "METRIC_MISMATCH", lambda t: t["metrics"]["services"][0].update(missed=True))
    add("false_group_metric", "METRIC_MISMATCH", lambda t: t["metrics"]["groups"]["L"].update(p95=0))
    add("split_execution", "DUPLICATE_EXECUTION", lambda t: t["executions"].append({**t["executions"][0], "start": 1, "finish": 2}))
    add("assignment_event_mismatch", "EVENT_ACCOUNTING", lambda t: next(e for e in t["events"] if e["kind"] == "start").update(node="other-node"))
    add("malformed_events", "EVENT_SCHEMA", lambda t: t["events"].append({"time": 0, "kind": "start"}))
    return cases

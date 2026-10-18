"""P1 evidence gate: hashes, required tests, physical traces and exact replay.

Separate from the unchanged P0 gate. Does not unlock P2 or execute science.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

from soc.model.schema import Workload, canonical_bytes
from soc.simulator.engine import simulate
from soc.validation.trace import validate_trace
from soc.validation.governance import audit_p0, relevant_source_hash, sha256_file

METHODS = ("B1", "B2", "B3", "B4", "B5")
FIXTURES = ("hand_dag", "priority", "simultaneous", "wait_scan", "overrun",
            "oeft_choice", "remapping", "empty", "minimal")
REQUIRED_TEST_MODULES = {"test_governance", "test_p1_engine", "test_p1_kernels", "test_p1_metrics",
                         "test_p1_model", "test_p1_observation", "test_p1_trace", "test_p1_gate"}


def manifest_errors(root: Path, rows: list[dict]) -> tuple[list[str], set[str]]:
    errors, seen = [], set()
    for row in rows:
        rel = row["path"]
        path = (root / rel).resolve()
        if rel in seen or not path.is_relative_to(root.resolve()) or not path.is_file():
            errors.append("invalid/duplicate/missing artifact " + rel)
            continue
        seen.add(rel)
        if sha256_file(path) != row["sha256"]:
            errors.append("artifact hash mismatch " + rel)
    return errors, seen


def declared_test_ids(root: Path) -> set[str]:
    """Check that recorded test results cover every current declared test method."""
    found = set()
    for path in (root/"tests").glob("test_*.py"):
        for cls in ast.parse(path.read_text()).body:
            if isinstance(cls, ast.ClassDef):
                for method in cls.body:
                    if isinstance(method, ast.FunctionDef) and method.name.startswith("test_"):
                        found.add(f"{path.stem}.{cls.name}.{method.name}")
    return found


def audit_p1(root: Path) -> dict:
    errors = []
    result = {"stage": "P1", "status": "BLOCKED", "errors": errors,
              "scientific_workloads_run": 0, "P2_started": False}
    def load(rel):
        path = (root / rel).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("evidence path escapes repository")
        return json.loads(path.read_text())
    try:
        p0 = audit_p0(root)
        if p0["status"] != "PASS":
            errors.append("P0 prerequisite: " + "; ".join(p0["errors"]))
        index = load("reports/P1_artifacts/index.json")
        manifest = load("checkpoints/P1_artifact_manifest.json")
        current_source = relevant_source_hash(root)
        result["source_sha256"] = current_source
        if manifest.get("source_sha256") != current_source:
            errors.append("current source/config identity differs from tested evidence")
        integrity_errors, seen = manifest_errors(root, manifest["files"])
        errors.extend(integrity_errors)
        required_paths = {"docs/P1_implementation_spec.md", "docs/P1_decisions.json",
                          "reports/P1_artifacts/index.json", "reports/P1_artifacts/negative_results.json",
                          "reports/P1_test_run.json", "reports/P1_preflight.json"}
        required_paths.update(p.relative_to(root).as_posix() for prefix in ("src", "scripts", "tests")
                              for p in (root/prefix).rglob("*.py") if "__pycache__" not in p.parts)
        if not required_paths <= seen:
            errors.append("manifest omits mandatory code/tests/spec/results")
        decisions = load("docs/P1_decisions.json")
        if decisions.get("status") != "FROZEN" or decisions.get("user_approved_ids") != ["D1", "D2", "D3", "D4", "D5"]:
            errors.append("online decisions not frozen by user")
        tests = load("reports/P1_test_run.json")
        test_rows = tests["tests"]
        ids = [row["id"] for row in test_rows]
        modules = {i.split(".")[0] for i in ids}
        if (tests.get("exit_code") != 0 or tests.get("failed") != 0 or tests.get("skipped") != 0 or
                len(ids) != len(set(ids)) or set(ids) != declared_test_ids(root) or tests.get("executed") != len(ids) or
                not REQUIRED_TEST_MODULES <= modules or
                any(row.get("status") != "PASS" or row.get("exit_code") != 0 for row in test_rows)):
            errors.append("mandatory unit/governance results incomplete or not all passed")
        preflight = load("reports/P1_preflight.json")
        for rel, expected in preflight["protected_sha256"].items():
            if sha256_file(root/rel) != expected:
                errors.append("protected protocol/seed/governance file changed " + rel)
        pairs = [(r["fixture"], r["method"]) for r in index["runs"]]
        if len(pairs) != len(set(pairs)) or set(pairs) != {(f, m) for f in FIXTURES for m in METHODS}:
            errors.append("required fixture x baseline grid incomplete")
        positive = 0
        for run in index["runs"]:
            if (run["input"] != f"reports/P1_artifacts/inputs/{run['fixture']}.json" or
                    run["trace"] != f"reports/P1_artifacts/traces/{run['fixture']}_{run['method']}.json"):
                errors.append("fixture/baseline shared-input path mismatch")
            if run["input"] not in seen or run["trace"] not in seen:
                errors.append("fixture or trace absent from manifest")
                continue
            workload = Workload.from_dict(load(run["input"]))
            trace = load(run["trace"])
            if sha256_file(root/run["input"]) != run["input_sha256"] or sha256_file(root/run["trace"]) != run["trace_sha256"]:
                errors.append("run hash identity differs from file")
            if trace.get("method") != run["method"]:
                errors.append("trace baseline identity mismatch")
            checked = validate_trace(workload, trace)
            if checked["status"] != "PASS":
                errors.append("independent trace failure " + run["trace"])
            elif canonical_bytes(simulate(workload, run["method"])) != canonical_bytes(trace):
                errors.append("exact replay mismatch " + run["trace"])
            else:
                positive += 1
        negative = load("reports/P1_artifacts/negative_results.json")
        if len(negative) < 20 or any(r.get("status") != "PASS" or r.get("actual_status") != "FAIL" or
                                    r["expected_code"] not in r["actual_codes"] for r in negative):
            errors.append("negative validator evidence incomplete")
        # Re-evaluate retained malformed traces, rather than trust PASS labels.
        negative_input = Workload.from_dict(load("reports/P1_artifacts/inputs/hand_dag.json"))
        for row in negative:
            if row["trace"] not in seen:
                errors.append("negative trace not hashed")
                continue
            checked = validate_trace(negative_input, load(row["trace"]))
            if checked["status"] != "FAIL" or row["expected_code"] not in {e["code"] for e in checked["errors"]}:
                errors.append("negative trace no longer rejected " + row["name"])
        if (root/"checkpoints/VALIDATION_UNLOCKED").exists() or (root/"checkpoints/FORMAL_UNLOCKED").exists():
            errors.append("unexpected scientific unlock artifact")
        result.update(governance_and_p1_tests=len(ids), p1_tests=sum(not i.startswith("test_governance.") for i in ids),
                      tests_failed=tests["failed"], tests_blocked=0, positive_traces=positive,
                      negative_traces=len(negative), deterministic_replay_pass=positive==len(FIXTURES)*len(METHODS),
                      independent_metric_recomputation_pass=positive==len(FIXTURES)*len(METHODS),
                      tested_git_head=index["git_head"], tested_worktree=index["worktree"],
                      seed_sha256=p0["seed_sha256"], specification_status="FROZEN")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, RuntimeError) as exc:
        errors.append("missing/invalid P1 evidence: " + str(exc))
    result["status"] = "BLOCKED" if errors else "PASS"
    result["baseline_status"] = {m: result["status"] for m in METHODS}
    return result

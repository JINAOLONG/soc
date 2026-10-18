"""Run only hand-authored P1 correctness fixtures; retain tests, traces and hashes."""
from __future__ import annotations

from datetime import datetime, timezone
import inspect
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import unittest

from soc.model.schema import canonical_bytes
from soc.simulator.engine import simulate
from soc.validation.trace import validate_trace
from soc.validation.governance import audit_p0, relevant_source_hash, sha256_file
from soc.validation.p1 import METHODS, FIXTURES

ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


class EvidenceResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = {}

    def startTest(self, test):
        super().startTest(test)
        method = getattr(test, test._testMethodName)
        source, line = inspect.getsourcelines(method)
        self.rows[test.id()] = dict(id=test.id(), status="RUNNING",
                                   test_source=Path(inspect.getsourcefile(method)).relative_to(ROOT).as_posix(),
                                   source_line=line, expected_assertions="".join(source), actual="", failures=[])

    def addSuccess(self, test):
        super().addSuccess(test)
        row = self.rows[test.id()]
        if row["status"] == "RUNNING":
            row.update(status="PASS", actual="All assertions and subtests satisfied")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.rows[test.id()].update(status="FAIL", actual=self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self.rows[test.id()].update(status="FAIL", actual=self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.rows[test.id()].update(status="SKIPPED", actual=reason)

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            row = self.rows[test.id()]
            row["status"] = "FAIL"
            row["failures"].append(dict(subtest=str(subtest), error=self._exc_info_to_string(err, test)))


def main() -> int:
    p0 = audit_p0(ROOT)
    if p0["status"] != "PASS":
        print(json.dumps(p0))
        return 2
    sys.path.insert(0, str(ROOT/"tests"))
    suite = unittest.defaultTestLoader.discover(str(ROOT/"tests"))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=EvidenceResult).run(suite)
    # unittest methods have no OS exit status of their own. Execute each named
    # case in a real child process to record the explicitly requested exit code.
    # Count unique cases, not these repeated evidence executions, as sample size.
    for row in result.rows.values():
        command = [sys.executable, "-m", "unittest", row["id"], "-v"]
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                 env={**os.environ, "PYTHONPATH": str(ROOT/"tests"),
                                      "PYTHONDONTWRITEBYTECODE": "1"})
        row.update(command=command, exit_code=process.returncode, stdout=process.stdout, stderr=process.stderr)
        if process.returncode:
            row.update(status="FAIL", actual="individual subprocess failed: " + process.stderr)
    failed = sum(r["status"] == "FAIL" for r in result.rows.values())
    skipped = sum(r["status"] == "SKIPPED" for r in result.rows.values())
    tests = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                 command=[sys.executable, "scripts/run_p1_correctness.py"],
                 tests=list(result.rows.values()), executed=result.testsRun, failed=failed, skipped=skipped,
                 exit_code=0 if result.wasSuccessful() and not skipped and not failed else 1, stdout=stream.getvalue())
    history = ROOT/"reports/P1_test_runs"
    history.mkdir(exist_ok=True)
    number = len(list(history.glob("run_*.json")))+1
    historical_path = history/f"run_{number:03}.json"
    if historical_path.exists():
        raise RuntimeError("refusing to overwrite test history")
    write(historical_path, tests)
    write(ROOT/"reports/P1_test_run.json", tests)
    print(f"unit tests={result.testsRun}, failed={failed}, skipped={skipped}, exit={tests['exit_code']}")
    if tests["exit_code"]:
        print(stream.getvalue())
        return tests["exit_code"]
    from p1_fixtures import fixture_cases, HAND_INTERVALS
    from p1_negative_cases import negative_cases
    fixtures = fixture_cases()
    if set(fixtures) != set(FIXTURES):
        raise RuntimeError("fixture grid mismatch")
    index = dict(schema_version=1, origin="HAND_AUTHORED_CORRECTNESS_FIXTURE",
                 git_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                 worktree=subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True),
                 timestamp_utc=datetime.now(timezone.utc).isoformat(), host=platform.platform(),
                 python=platform.python_version(), exact_command=[sys.executable, "scripts/run_p1_correctness.py"],
                 scientific_workloads_run=0, seed_partitions_accessed=False, runs=[])
    artifacts = ROOT/"reports/P1_artifacts"
    for name, workload in fixtures.items():
        path = artifacts/"inputs"/(name+".json")
        write(path, workload.to_dict())
        input_sha = sha256_file(path)
        for method in METHODS:
            trace = simulate(workload, method)
            replay = simulate(workload, method)
            checked = validate_trace(workload, trace)
            exact = canonical_bytes(trace) == canonical_bytes(replay)
            if checked["status"] != "PASS" or not exact:
                raise RuntimeError(f"trace/replay failure {name}/{method}: {checked}")
            if name == "hand_dag" and {r["node"]: (r["start"], r["finish"]) for r in trace["executions"]} != HAND_INTERVALS:
                raise RuntimeError("manual DAG time mismatch")
            target = artifacts/"traces"/(name+"_"+method+".json")
            write(target, trace)
            index["runs"].append(dict(fixture=name, method=method, input=path.relative_to(ROOT).as_posix(),
                                      input_sha256=input_sha, trace=target.relative_to(ROOT).as_posix(),
                                      trace_sha256=sha256_file(target), validator=checked,
                                      deterministic_replay_pass=exact, independent_metrics_equal=checked["metrics"]==trace["metrics"],
                                      exit_code=0, expected="legal deterministic full-drain trace; manual hand_dag times fixed",
                                      actual="PASS"))
    negative = []
    for name, code, trace in negative_cases(simulate(fixtures["hand_dag"], "B1")):
        checked = validate_trace(fixtures["hand_dag"], trace)
        codes = [e["code"] for e in checked["errors"]]
        target = artifacts/"negative"/(name+".json")
        write(target, trace)
        status = "PASS" if checked["status"] == "FAIL" and code in codes else "FAIL"
        negative.append(dict(name=name, expected_code=code, actual_status=checked["status"], actual_codes=codes,
                             status=status, trace=target.relative_to(ROOT).as_posix(), validator=checked, exit_code=0 if status=="PASS" else 1))
    if any(r["status"] != "PASS" for r in negative):
        raise RuntimeError("negative validator test failed")
    write(artifacts/"negative_results.json", negative)
    write(artifacts/"index.json", index)
    paths = set()
    for prefix in ("src", "scripts", "tests"):
        paths.update(p for p in (ROOT/prefix).rglob("*.py") if "__pycache__" not in p.parts)
    paths.update(p for p in artifacts.rglob("*") if p.is_file())
    for name in ("docs/P1_implementation_spec.md", "docs/P1_acceptance_matrix.md", "docs/P1_decisions.json",
                 "docs/model_spec.md", "docs/baseline_spec.md", "configs/research_protocol.json",
                 "configs/seed_partitions.json", "docs/statistical_protocol.md", "docs/metric_spec.md",
                 "reports/P1_test_run.json", "reports/P1_preflight.json", "AGENTS.md", "pyproject.toml"):
        paths.add(ROOT/name)
    manifest = dict(schema_version=1, scope="P1 synthetic correctness evidence; no science",
                    source_sha256=relevant_source_hash(ROOT), tested_git_head=index["git_head"],
                    files=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256_file(p)) for p in sorted(paths)])
    write(ROOT/"checkpoints/P1_artifact_manifest.json", manifest)
    print(f"positive traces={len(index['runs'])}, negative cases={len(negative)}, exact replay=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

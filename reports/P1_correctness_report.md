# P1 correctness audit and stop report

Actual P1 audit: **PASS**, exit **0**. P0 check-only also returned 0. The existing
P0 gate/governance function and its seed/literature checks were not changed.
This is synthetic implementation correctness evidence only. No scientific
performance result, scheduling-benefit claim or P2 authorization is produced.

## Scope and approved rules

The user authorized P1 implementation and explicitly approved D1 event ordering
and D2–D5 online semantics. See docs/P1_decisions.json and the frozen
implementation specification. Required model, event engine, read-only observation,
B1–B5, fixture metrics and independent offline validator are implemented.
No CPOP baseline, candidate method or scientific workload generator was added.

## Actual checks

- 64 unique named tests passed: 17 unchanged governance + 47 P1; zero failed,
  skipped or blocked in the final run. Each named test also ran in its own
  subprocess, with actual exit 0, stdout/stderr and exact assertions retained in
  P1_test_run.json. Repeated executions are not extra independent samples.
- Nine fixed hand inputs, five methods each: 45 full traces, independent
  validation/complete metric equality and exact replay all pass.
- Twenty deliberate malformed traces all rejected with specified error codes;
  additional unit negatives cover pre-arrival start and invalid D1 event phases.
- Source regressions: original HEFT Fig3/Table1 all ten rank values and PEFT
  Fig1/Table2 all thirty OCT cells, transcribed from the actual supplied copies.
- Eight-node DAG hand intervals and H deadline equality match; all arrived work
  drains, including the L miss. Empty/minimal, incompatible and busy resources,
  estimate overrun, gap insertion, waiting/scanning, remapping, deterministic ties,
  deadlock and immutable/no-future observations are exercised.
- Manifest verifies 122 explicit core files, including source, tests, inputs,
  model config and full traces. Formal gate rechecks hashes, exact test identities,
  all valid traces and malformed negatives; PASS text alone cannot satisfy it.

The implementation-time failure in P1_test_history.json was a wrong test literal:
expected cross-unit data total 9 instead of the hand-summed 8 MiB. It was fixed
without changing model/algorithm/thresholds; failed evidence remains retained.
Earlier and later successful runs remain in P1_test_runs/.

## Identity and reproduction

Input checkpoint: 27d90bb5cccd990f2b65d7ea48abe98c2af7218c on work.
Tested source/config SHA-256: `32860d432e7fef62f03fef64be3118c2ba260de6850d8f88a447fb7589cf412b`.
Final enclosing Git commit is resolved using `git rev-parse HEAD`; exact tested
Git HEAD/dirty state are recorded in P1_artifacts/index.json. A dirty development
run is identified as such and is not mislabeled as a committed-source run.
The delivery receipt separately records the actual committed and pushed checkpoint.

```bash
.venv/bin/python scripts/run_p1_correctness.py
.venv/bin/python scripts/run_pipeline.py --stage p1
.venv/bin/python scripts/hash_artifacts.py --verify --output checkpoints/P1_artifact_manifest.json
```

Actual commands, output and return codes are retained in P1_audit_runs/. Tests use
standard library only and hand-authored deterministic fixtures. Formal P0/P1
requires the six original source PDFs and matching hashes; no PDFs are tracked.
A fresh clone without the private supplied inputs cannot reproduce the formal
literature prerequisite until those inputs are legitimately restored. Unit tests
are independent of that private cache.

P0_protocol_audit.json, its historical source SHA, prior BLOCKED snapshots and the
old P0 artifact inventory remain unchanged. The new P1 code naturally has a new
source hash and manifest; an old P0 manifest is not rewritten to hide that change.
Eight protected protocol/seed/statistics/method/governance/license files remain
byte-identical to the preflight. No seed or scientific realization was generated.

## Limits and stop

Independent validation here means offline *trace correctness*, not use of the
reserved INDEPENDENT_VALIDATION scientific partition. That partition and formal
remain locked and untouched. No calibration, development, scientific comparison,
host timing or energy experiment ran. This finite test suite is not a proof over
all possible DAGs or a hardware/safety certification. Original static algorithms
and project online adaptations remain explicitly distinguished.

See P1_acceptance_matrix.md, P1_baseline_implementation_report.md and
P1_trace_validation_report.md for requirement-by-requirement evidence. Delivery
state is P1_delivery_status.json and the verified Git receipt. **STOP after P1**;
P2 requires a separate task. Existing later-stage pipeline branches remain
unimplemented and are not exercised by this task.

Committed-source verification: `d60b94a791580af09fc0b40827eb57de439f1916` started from a clean worktree; all 64 tests and 45/20 trace checks passed again. Code/config/tests/spec remained byte-identical afterward. See P1_committed_source_verification.json. Normal push and matching remote SHA are recorded in P1_git_checkpoint.json; the final receipt-only enclosing commit is resolved live.

# Current-cloud implementation and correctness delivery

Scope: user-authorized implementation and hand-authored correctness verification,
with results retained. No registered scientific workload or analysis was run.
Machine summary is `summary.json`; accepted decisions and precise exceptions are
in `docs/P2_design/accepted/` at repository root. Original V3 drafts remain intact.

## Implemented and exercised

* `soc.p2.identity`: exact semantic canonicalization, closed bound-schema checks,
  raw/semantic identities, binary64/rational encoding, immutable artifact store.
* `soc.p2.generation`: approved keyed arithmetic, rational-to-binary64 conversion,
  template materialization logic, controls and header-free model adapter. Loop
  tests use a literal small hand graph and fixed mocked factors; no registered
  template/seed realization is generated.
* `soc.p2.adapter`: S2 rejection/birth boundary, independent physical payload
  checks and public-call reconstruction, including missing empty/time hooks.
* `soc.p2.diagnostic`: B1 bounded remaining-H projection, fixed suffix/local L
  constraint, typed public snapshots and exact scoped dedup identities.
* `soc.p2.qualification` and `analysis`: pressure, waiting, strict RN64 feasibility,
  exact ten-seed eligibility/A-before-B selection, COARSE three-way rules, paired
  aggregation and M2 roster/contrast checks. Only constructed hand numbers and
  hand index vectors were evaluated; registered bootstrap generation was denied.
* `soc.p2.coordination`: private SQLite A primitives, unique budget root,
  reservation/admission, exact CAS, no takeover/refund, expiry/reversed-clock halt,
  explicit pre-expiry renewal, durable hand-fixture history and A2 hash closure.
* `soc.p2.recovery`: accepted two B3 closed record kinds, null/authority requirements,
  three purpose identity mappings, root/plan/source/trial checks and historical
  published reuse. Tests explicitly mock real authorization evidence; this is not
  a deployed issuer or publication authority.
* `soc.p2.provenance`: actual Git/process observations and source checks. A mode-bit
  check explicitly does not claim kernel isolation.
* `deploy/Dockerfile.correctness`: digest-pinned Python3.12.14 amd64 fixture image.
  Actual checks used nonroot UID10001, readonly root, no network/socket/capabilities,
  no-new-privileges, source-hash equality and exact host/container hand B2 trace.

## Actual checks

* Full existing P1 evidence runner: **110 tests, 0 failed, 0 skipped**. This is
  64 original tests plus46 P2 component tests, not110 scientific samples.
* Required original grid:45 positive fixture traces,20 negative cases, exact replay
  and independent metrics PASS. All updated official evidence remains at existing
  P1 paths; prior files are retained under `baseline/` and test history.
* Current-source P0 audit exit0; P1 audit exit0. Actual command outputs and expected
  scientific-entry rejection exit2 are in `final_checks/release_commands.json` and
  corresponding stdout/stderr files. Full P1 invocation/log is `full_p1_run_002.json`.
* Latest component evidence: `runs/run_006`; latest container evidence:
  `container/run_005`. Each contains raw logs and an independently hashable manifest.
* Container image ID and tested source hash are recorded in `summary.json`.
* Protected simulator/kernel/governance, scientific protocols/seeds and original
  V3 definitions were hash-checked unchanged; see `protected_release.json`.

History remains: `runs/run_001` failed because its expired-estimate fixture had no
unstarted H node and was correctly outside E0; corrected fixture was retained in
later source. `container/run_001` failed because source directories were unreadable
to the nonroot user; permissions/probe were corrected before later PASS. Intermediate
passes also remain and are not substituted for the final source checks.

## Limits and remaining production work

This is engineering evidence, not P2 PASS. The scientific entry now reports
specific fail-closed reasons; it does not execute the2520-slot plan. Production
authority/worker integration, real birth/permission evidence providers, approved
lease/profile/principals, persistent storage and full scientific orchestration
remain undeployed. The callback boundaries in adapter/recovery are trusted
integration obligations, not self-proving security checks.

SQLite crash/reopen/race fixtures do not prove host power-loss or cloud-session
durability. The Docker fixture probe does not prove every production boundary or
freeze future scientific timing. No timing/P95 measurement, candidate formula,
threshold/CI/seed change, reserved outcome access or validation/formal unlock occurred.

Source tests used the actual dirty implementation checkout. The real parent HEAD,
dirty listing and file hashes are retained; old P1 PASS was not inherited for new
bytes. The enclosing publication commit is resolved with Git, not inserted as a
fictional pre-existing tested commit. Report-only commits do not change source hash.

## Reproduction and retention

```
.venv/bin/python -B scripts/run_p2_correctness.py
.venv/bin/python -B scripts/verify_p2_container.py
.venv/bin/python -B scripts/run_p1_correctness.py
.venv/bin/python -B scripts/run_pipeline.py --stage p0 --check-only
.venv/bin/python -B scripts/run_pipeline.py --stage p1 --check-only
```

Container verification requires a usable Docker daemon and the pinned base image.
Engineering commands retain a new run directory; do not run them as science.
Small fixture inputs/traces, actual process stdout/stderr/exits, hand SQLite state,
test expectations, histories and manifests are committed with source so successful
GitHub publication preserves these results beyond the current cloud workspace.
Docker image bytes are local only; its recipe, base digest and actual image identity
are retained in Git. No private paper PDFs, credentials or reserved outcomes are added.

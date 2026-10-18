# P1 actual acceptance matrix

All rows refer to executed hand-authored correctness tests. Exact input artifacts,
assertions, actual outcomes and per-case OS exit codes are in P1_test_run.json;
historical runs (including earlier coverage) remain in P1_test_runs/.
The formal result is P1_correctness.json, not this checklist alone.

| Requirement | Implementation / test evidence | Actual status |
|---|---|---|
| P0 prerequisite and six exact original files | P1_preflight.json; unchanged P0 gate called by P1 | PASS |
| Event and online policies approved before engine | docs/P1_decisions.json; implementation_spec D1–D5 | FROZEN by user |
| DAG, six resources, uniqueness, compatible costs, valid timings | model/schema.py; all ModelTests | PASS |
| Immutable arrived-only estimates/status | model/observation.py; all ObservationTests and engine leakage callback | PASS |
| Noninterference of future arrivals/realized durations | test_noninterference_of_future_services_and_actual_durations | PASS |
| Same-time completion → arrival → dispatch | test_same_time_completions_before_arrivals_before_dispatch; validator wrong-phase negative | PASS |
| B1 EDF/EFT vs B2 H/EDF/EFT | test_b1_b2_and_b5_hand_checked_start_difference | PASS |
| B3 HEFT rank and source arithmetic | original Fig3/Table1 all ten ranks; source recurrence tests | PASS |
| B4 OCT/rank/OEFT | original PEFT Fig1/Table2 all thirty cells; EFT/OEFT root mapping differs as expected | PASS |
| B5 H first with PEFT mapping | H first in priority fixture; all shared fixtures, unchanged OEFT map | PASS |
| All B1–B5 use same model/input bytes | 9 fixed inputs × 5 baselines, same per-fixture input SHA | PASS |
| Gap insertion and busy prediction | test_insertion_uses_idle_gap_not_append_only; overrun estimate/elapsed test | PASS |
| Wait/scan without future reservation | test_waiting_does_not_reserve_idle_units_or_block_other_tasks | PASS |
| Pending remap and destination copies | test_pending_remapping_recomputes_destination_data_and_does_not_reserve_gpu | PASS |
| 8-node DAG, fan-in, communication, resource contention | hand_dag inputs, explicit HAND_INTERVALS and all methods' traces | PASS |
| Non-preemption, migration, duplicate execution | validator contiguous intervals + explicit split/migration/duplicate negatives | PASS |
| Full drain and deadline equality | H-hand finish=deadline=13 is on time; L-hand finish13>deadline12 retained miss | PASS |
| Empty system / single node / invalid empty service | test_empty_and_minimal_inputs_and_full_drain; invalid model tests | PASS |
| No-progress deadlock detection | rejecting controller with finite valid input raises DeadlockError | PASS |
| Independent physical/metric validator | validation/trace.py; patched-engine/metric/communication dependency test | PASS |
| Positive and negative traces retained | 45 positive full traces; 20 deliberate malformed traces and expected error codes | PASS |
| Exact deterministic replay | Every fixture/method repeated, canonical events/decisions/metrics bytes equal | PASS |
| Independent complete metrics | Service/group metrics, busy/utilization, transfers and waiting independently match | PASS |
| Evidence identity/fail-closed gate | manifest, source/test hashes, exact declared test IDs, tamper/duplicate/escape tests | PASS |
| Seeds, thresholds, CI protocol, P0 governance unchanged | 8 protected file SHA checks; old P0 reports/inventory/literature retained | PASS |
| P2/P3/reserved science remain unopened | No science runner invoked, results remain placeholders, unlock files absent | PASS |
| Formal P1 process result | Actual saved exit code/output in P1_audit_runs/; P1_correctness.json | See actual gate |
| Committed code and normal push | P1 delivery checkpoint receipt; live Git for final enclosing HEAD | See Git receipt |

Count named unittest methods once: full-suite execution and individual subprocess
executions are two verification modes, not additional independent samples.
These are correctness results only; no scheduling-benefit, host-latency or
scientific performance conclusion follows.

# P1 specification-to-code/test/artifact matrix

This is the implementation plan created before implementation. Actual outcome
and test counts are in reports/P1_acceptance_matrix.md and P1_correctness.json.
Original requirement sources: P1 authorization §§3–8,11; user_request §§17–31,78,99;
model_spec, metric_spec, baseline_spec; HEFT pp.262/264 and PEFT p.687.

| Requirement | Planned module | Planned tests | Evidence / dependency |
|---|---|---|---|
| DAG/resource/duration input validation | model/schema.py | test_p1_model | Invalid input cases + 8-node fixture |
| Immutable arrived-only observations | model/observation.py | test_p1_observation | Recursive immutability and noninterference |
| Communication/readiness | model/schema.py | test_p1_model | Same/cross unit, remapping, overlap |
| Source rank/OCT and insertion | scheduler/kernels.py | test_p1_kernels | Hand arithmetic, source equation refs |
| B1/B2 ordering | scheduler/kernels.py | test_p1_kernels | EDF vs H-priority fixture |
| Full B1–B5 dispatch | scheduler (pending D2–D5) | BLOCKED until decisions | No baseline PASS from kernels |
| Event engine/full drain/deadlock | simulator (pending D1,D4,D5) | BLOCKED until decisions | No implicit event policy |
| Fixture metrics | metrics/fixture.py | test_p1_metrics | Deadline equality, undefined groups, type-7 |
| Independent interval/event/communication validator | validation/trace.py | test_p1_trace | Hand-authored positive/negative traces |
| Engine/validator agreement and replay | pending engine | BLOCKED | Required for P1 PASS |
| Evidence integrity and real test results | scripts/audit_p1.py | test_p1_gate | Fails closed, source/input/test/trace hashes |
| Scientific boundaries | protected P0 files | governance + hash audit | Seeds/thresholds/CI unchanged, no unlocks |

No scientific generator, candidate, calibration or bootstrap implementation is
authorized here. P1 component tests use hand-authored fixture input exclusively.

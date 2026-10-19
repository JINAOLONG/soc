# P1 implementation scope and decisions

Status: FROZEN for P1 following the user's explicit approval of D1 and D2–D5
in this task's clarification replies. Those replies approved the concrete
suggested options below as a complete set; no alternative was selected.
P0 passed at input checkpoint
27d90bb5cccd990f2b65d7ea48abe98c2af7218c. The P1 request is preserved verbatim
in P1_authorization_request.txt. No scientific workloads or seed realizations
are permitted. Units and mandatory model/metric rules remain those in model_spec.md
and metric_spec.md. This document does not override scientific thresholds.

## Specification differences and recorded user decisions

The current model explicitly says **Proposed** event ordering. The P1 request
§3.3 forbids silently freezing that proposal. Baseline_spec explicitly leaves
online dispatch and compatibility details open. These are semantic choices,
not implementation names. The user resolved all five by approving the suggested
options below before event-engine or full-baseline implementation began.

| ID | Missing rule and effect | USER_APPROVED rule | Rejected alternative / affected scope |
|---|---|---|---|
| D1 | Same-time arrival/completion/dispatch can alter winners | All completions at t, all arrivals at t, immutable view, feasible dispatch until no further start, stable (service,node,resource) tie; then advance to next completion/arrival/data wakeup | Arrival/dispatch interleaving gives different schedules. Blocks event loop and full replay. |
| D2 | Source methods have full execution matrices, soc has incompatible units | HEFT mean execution over each task's compatible units; OCT child minimization over compatible child units, rows/rank average over the current task's compatible units; explicit destination-dependent same-unit zero | Full six-unit averages with invented incompatible costs, or another normalization; changes priorities. Blocks B3/B4/B5. |
| D3 | Source average communication does not define soc type/pair weights | For each edge average latency and bandwidth separately over ordered compatible endpoint unit pairs with different IDs, then Lbar+size/Bbar; if no such pair exists, zero | Mean of per-pair delays is generally different. Weight by resource type rather than unit is also different. Blocks B3/B4/B5. |
| D4 | Overrun makes estimated remaining busy duration ambiguous | Predicted release now+max(0,estimate-on-running-unit-elapsed), never actual event timestamp; no extra forecast padding | Another observable predictor requires explicit definition. Blocks busy-resource mapping for all B1–B5. |
| D5 | A future best mapping may intentionally leave an idle compatible unit unused | Order dependency-ready tasks; score all compatible units, including estimated busy/data-delayed starts; mapping proposals are revocable. Start only if selected unit is currently feasible; inspect lower-priority tasks when a higher one waits. Recompute after each start; no reservation of idle units | Restrict scoring to currently feasible units (work conserving) or stop scanning at first waiting task; changes schedules and fairness. Blocks all full B1–B5 dispatch. |

For either dispatch option all methods must share eligibility, information,
compatibility, transfers and tie conventions. Static gap insertion remains a
source-derived kernel; unstarted online proposals cannot reserve future slots.
Original HEFT random ties become project deterministic ties under approved D1.
No CPOP baseline is added: its source was reviewed, the formal methods remain B1–B5.

## Components independent of D1–D5

Implement immutable validated offline model records, finite positive durations,
fixed six resources, DAG checks, destination communication readiness, an explicit
public observation DTO that contains no realized duration/future services/event
queue, isolated source-formula kernels with caller-supplied mean edge costs and
complete matrices, B1/B2 public priority keys, interval gap search, fixture-only
metrics, and a separate trace validator. The validator receives complete offline
input but never calls engine legality functions or runtime metric functions.

Fixture input schema v1 uses hand-authored services/nodes/resource tables and
explicit edges (MiB), estimate/realized duration maps (ms), type-pair network
parameters (MiB/ms, ms). Trace schema v1 uses arrival/start/complete records and
full contiguous execution intervals. All identifiers are stable strings. No
seed, partition or random generator is used in these fixtures.

Empty workload is allowed as an empty-system input; an empty service DAG is
rejected because its completion is undefined. Single-node DAGs are supported.
No time epsilon is introduced; touching interval endpoints and deadline equality
are legal. Nonfinite numeric values and bool-as-number inputs are invalid.

Hand-authored trace checks are validator unit tests, not engine execution or
engine-versus-validator agreement. Source-derived arithmetic examples are not
complete B3/B4 validation. Every unimplemented mandatory requirement is reported
as BLOCKED, never silently skipped or counted as a passing baseline.

## Required completion under the approved decisions

An event engine must maintain a private queue, immutable observable snapshots,
revocable proposals, independent actual durations, deterministic event batches,
full drain and deadlock detection. Every implemented B1–B5 must run the same
stored synthetic input. Required evidence includes engine event/decision traces,
repeat identity, validator positive/negative results, independent recomputation,
manual DAG and boundary cases, and manifests binding fixture/config/test/code/trace
identities. P1_correctness.json must remain BLOCKED while any mandatory part is
missing, even if all available component tests pass. P2 and all science stay closed.

## P1 implementation conventions within the approved rules

No future planned reservations are made. The source insertion kernel finds the
first whole gap in an explicitly supplied occupied-interval list. Online EFT
uses the same kernel with only the observable predicted remainder of the running
task; absent future reservations, there are no invented scheduled intervals to
insert around. Data-delay wakeups are not reservations and can be superseded
by a new arrival. Tables are recomputed from each immutable view using complete
public arrived DAGs and their fixed estimates; completed tasks do not expose
true future costs or change those suffix labels.

Runtime output records every arrival/start/complete, contiguous execution, and
decision observation/proposal (including no-dispatch decisions). Offline true
finishes appear in full traces for validation, never in scheduler arguments.
Metrics include service responses/misses, group type-7 quantiles, full-drain
makespan, per-unit busy/utilization, per-edge destination copies, cross-unit data
total, dependency wait, communication wait and ready-to-start wait. The latter
combines scheduling/resource waiting; it does not claim an unavailable causal
decomposition. Absent groups and zero-horizon utilization are null/undefined.

No implementation complexity or host latency bound is inferred from the papers.
The straightforward compatible-pair OCT implementation can inspect a quadratic
number of processor pairs per edge; original complexity claims remain literature
statements only. No energy model, scientific aggregate or timing experiment is run.

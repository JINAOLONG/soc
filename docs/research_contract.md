# Research contract — P0 DRAFT, not scientifically unlocked

The authoritative request is [user_request.txt](user_request.txt). Repository:
`https://github.com/JINAOLONG/soc`; root = project root. This is a clean-room
project. No legacy artifacts, results, candidate parameters or seeds have been
used as new evidence. Existing Apache-2.0 LICENSE is preserved.

Question: with continuously arriving service DAGs, non-preemptive compatible
CPU/GPU/NPU execution and contention, can joint ready-node ordering and resource
mapping reduce important-service H end-to-end deadline misses while keeping
ordinary-service L P95 within 10% of B2 in every main condition?

Falsifiable mechanism hypothesis: local EFT can occupy a scarce resource needed
by another arrived H service; an online opportunity-cost rule may improve H DMR.
This is a hypothesis, not an established result. H/L denotes service importance,
not ASIL. No energy-budget, WCET-proof or deployment/certification claim is made.

P0 requires 6–8 reviewed original studies (HEFT/CPOP, PEFT and DS3 mandatory),
model/metric/baseline/statistical specifications, committed seed metadata and
passing protocol audit. P0 currently fails the primary-literature prerequisite.
Documents are drafts. User-prescribed thresholds and seed derivation cannot be
relaxed even while the protocol is a draft. Do not call this a P0 freeze.

Progression is P0 → P1 correctness → P2 baseline-only calibration → P3 development
and ablations → Development Gate → independent validation → Validation Gate →
formal → evidence closure. Every stage preserves negative/invalid evidence.
P1 correctness failure blocks science. Lack of stable P2 mapping opportunity
stops the mapping mainline. P3 allows at most one preregistered, evidence-driven
mechanism revision. Failed validation blocks formal. Failed/inconclusive formal
remains failed/inconclusive. Unknown input provenance stops execution.

P0–P2 execution is CALIBRATION only; unit tests must use synthetic fixtures.
P3 DEVELOPMENT has a fixed 10/10 search/precheck split. Metadata generation and
hashing all 70 prescribed seeds is explicitly distinct from workload access.
No reserved workload realization is generated or inspected before its gate.

Future candidate search space, workload calibration choices and timing protocol
must be registered before their dependent observations. A method formula must
not be invented before P2 diagnostics. Later missing evidence cannot be filled
with guesses or a passing smoke test. Current scientific status: BLOCKED.

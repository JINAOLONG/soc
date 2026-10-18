# Baselines — original sources reviewed; P1 online adaptation implemented

All methods share one immutable observation boundary, workload, compatibility,
communication semantics and deterministic tie rule. Root/ready eligibility never
uses future arrivals or unfinished predecessor truth. Estimated finish prediction
on a busy unit must use observable elapsed execution and estimates. A processor
selection proposal is revocable until the task starts; dispatch must recheck
actual feasibility and may not reserve an idle unit indefinitely by accident.
The user approved the precise online adaptation rules D1–D5 during the P1 task.
Their authoritative definition and acceptance dependencies are in
[P1_implementation_spec.md](P1_implementation_spec.md). They must be tested
before P1 is marked complete.

| ID | Ready-node ordering | Mapping | Status |
|---|---|---|---|
| B1 | ascending service absolute deadline | minimum estimated finish among compatible units | implemented; P1 report provides actual correctness evidence |
| B2 | H before L, then ascending service absolute deadline | same EFT rule as B1 | fixed L-budget reference; implemented |
| B3 | Online-HEFT adaptation; original upward rank source-verified | insertion/EFT with approved D1–D5 online dispatch | implemented; original static method distinguished |
| B4 | Online-PEFT adaptation; original OCT/rank source-verified | insertion/OEFT with approved D1–D5 online dispatch | implemented; original static method distinguished |
| B5 | H-priority Online-PEFT adaptation | same mapping requirement as B4 | implemented; source and adaptation kept separate |

The actual user-provided originals are now reviewed in
[heft_cpop.md](literature_reviews/heft_cpop.md) and
[peft.md](literature_reviews/peft.md), with equations, figures, page numbers and
version/provenance limits. This is an evidence-status update, not a change to any
baseline requirement or an implementation. Original HEFT rank ties are random;
PEFT OCT excludes availability while EFT includes partial-schedule availability.
Online adaptation still must explicitly specify visible DAG set, ready filtering,
compatibility, busy-resource handling, rank/OCT refresh, idle/wait behavior, ties
and boundary cases before P1 can be complete. The previous local-PDF task did
not authorize implementation; the separate P1 task and explicit D1–D5 replies
now authorize the documented adaptation. Online adaptations must never be presented
as the original static algorithms.

Required P1 evidence: distinguish B1/B2 by hand fixture; verify ranks/OCT against
source-derived worked examples; exercise incompatible/busy resources and ties;
deterministic replay; and have an independent validator reject invalid traces.
No custom candidate may replace a missing baseline or serve as its own control.

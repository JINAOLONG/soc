# Baselines — P0 draft, original-source verification pending

All methods share one immutable observation boundary, workload, compatibility,
communication semantics and deterministic tie rule. Root/ready eligibility never
uses future arrivals or unfinished predecessor truth. Estimated finish prediction
on a busy unit must use observable elapsed execution and estimates. A processor
selection proposal is revocable until the task starts; dispatch must recheck
actual feasibility and may not reserve an idle unit indefinitely by accident.
The precise online-adaptation dispatch policy must be frozen and tested after
the source methods are reviewed and before P1 is marked complete.

| ID | Ready-node ordering | Mapping | Status |
|---|---|---|---|
| B1 | ascending service absolute deadline | minimum estimated finish among compatible units | definition supplied by user; implementation NOT RUN |
| B2 | H before L, then ascending service absolute deadline | same EFT rule as B1 | fixed L-budget reference; implementation NOT RUN |
| B3 | Online-HEFT adaptation, upward-rank rule pending original review | HEFT processor-selection adaptation pending review | UNVERIFIED_SOURCE; NOT IMPLEMENTED |
| B4 | Online-PEFT adaptation, OCT/rank pending original review | PEFT processor-selection adaptation pending review | UNVERIFIED_SOURCE; NOT IMPLEMENTED |
| B5 | H-priority Online-PEFT adaptation | same mapping as reviewed B4 | UNVERIFIED_SOURCE; NOT IMPLEMENTED |

HEFT/CPOP and PEFT formulas, complexity and claimed equivalence are deliberately
not filled from memory or titles. Once original studies are available, record
equations/page references and manually verified OCT/rank examples. Then specify
visible DAG set, ready filtering, compatibility, busy-resource handling, rank/OCT
refresh, idle/wait behavior, ties and boundary cases for each online adaptation.
Online adaptations must never be presented as the original static algorithms.

Required P1 evidence: distinguish B1/B2 by hand fixture; verify ranks/OCT against
source-derived worked examples; exercise incompatible/busy resources and ties;
deterministic replay; and have an independent validator reject invalid traces.
No custom candidate may replace a missing baseline or serve as its own control.

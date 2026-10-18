# Feasibility, load and mechanism reasoning (design only)

This report supplies explicit rationale, not executed scientific results. All v1 values remain intact.
Source scope: complete proposal v1 D06–D08; model_spec.md:20–31,39–58; user_request.txt §§32–37,43–44.

## Lower-bound validity and limits

For a service with compatible set A_v and actual resource-dependent duration d(v,r), define
m_v=min_{r∈A_v} d(v,r). For edge u→v define e_uv as the minimum legal transfer delay over compatible
source/destination assignments (zero if the same unit is legal; otherwise the minimum nonnegative
L+b/B). Define ℓ_v=m_v+max_u(ℓ_u+e_uv), empty predecessor maximum0, and service LB=max_sink ℓ_v.
These are offline quantities: no true d(v,r), LB or private assignment alternatives go to the scheduler.

In the exact nonnegative time model this is a valid lower bound: each chosen duration≥m_v and chosen
edge delay≥e_uv; any legal start follows each predecessor completion plus its actual transfer. Induction
over the DAG gives completion(v)−arrival≥ℓ_v. Independently minimizing adjacent choices may be
inconsistent as a real assignment, but makes the bound more optimistic, never less optimistic.
Thus LB>D is sufficient for impossibility in that model, while LB≤D is not a feasibility proof.
B2 missing an isolated deadline also cannot establish impossibility of every other schedule.

IMPLEMENTATION NOT VERIFIED: v1 gives the recurrence in prose and does not implement it. Its final
payload and existing engine use binary64 additions; exact-real induction alone does not certify a
particular rounded relative-LB implementation. Before a future implementation, pin conservative
arithmetic and absolute-arrival/deadline comparison semantics, including equality, without adding an
arbitrary epsilon or changing thresholds. One possible route to review is a monotone absolute-time
recurrence using the same operation grouping as the approved engine, but this audit does not choose
or implement it. Future tests must include rounding boundaries. This qualification is part of the
D06/D10 numerical/metric contract gaps (V2-F07), not proof that a current scientific classification failed.

## Controls and pressure classification

H_ISOLATED changes arrival times and removes L. LOW_COMPETITION changes arrival times of all services.
Even with identical private keyed durations/deadlines, they are different workload artifacts with
different hashes from MAIN. A successful control is only a witness for its modified admissions, not
a proof that the original H-only arrival stream or mixed MAIN stream is schedulable.

The proposed G uses a conservative serial compute/communication sum plus deadline and1ms. A serial
topological schedule fits this bound in the exact model; the actual chosen B2 control must still be
checked for inter-service nonoverlap and deadlines. G's max-service domain (parent versus retained
services), floating conversion and overlap failure classification require the D04/D06 pinning in
V2-F03/V2-F07. The original registered §37 permits exclusive or low-competition checks; no extra
miss tolerance is supplied by that permission.

For valid physical intervals, clipped busy measure on each resource lies in[0,W], hence each p_s
and its mean p lie in[0,1]. Pressure intervals[0,.5),[.5,.8),[.8,1] are pairwise disjoint and cover
this valid domain. Miss/control/wait predicates can reject every bin; the correct residual is a
preserved valid-but-off-target/ineligible configuration. NaN, missing statistics or impossible p
must not be made eligible by clamping. META checks evaluate scalar boundaries, not observed loads.

Every declared target-load candidate must satisfy its own bin, not another label's bin. Both A/B
remain fully counted, with first eligible A then B across the same ten seeds. No mapping or candidate
effect is used to choose. Nevertheless, opportunity intervals on the selected B2 calibration records
remain conditional calibration descriptions, not new independent confirmation (V2-F06).

## M1 baseline membership and single-H structural limit

Under a fully pinned local append model, the greedy baseline maps every task compatibly, and its
L completion equals its own L constraints. It is therefore feasible in the enumeration; optimum≤baseline,
so Δ≥0 and b>0 follow from positive H estimates. This is a mathematical design property, NOT execution
of the unimplemented observer. Tie order, exact busy/data estimates and denominator contract still need
specification/behavioral tests. No actual M1 ratio or project outcome is computed here.

All H tasks precede L in fixed B2 order. If K contains exactly one H, that H is first. Its greedy EFT
already minimizes its own finish against the fixed public snapshot; later L assignments cannot alter
the first H's predicted finish in the append model. Therefore the constrained H optimum equals that
baseline in every such state. This is a structural statement, independent of trial results.

The original §32 correctness/explanation example exposes a different mechanism: H's CPU prefix2ms
unlocks an NPU suffix4ms; L occupies NPU6ms or idle CPU6.5ms. The ready-H prefix objective is2ms either
way, while the hand-calculated later H completion is10ms versus6ms against deadline9ms. L6.5ms also
violates the strict local L-nondegradation6ms although its point ratio13/12 is below1.10. That point
arithmetic is not a statistical L-budget pass, nor scientific evidence. No services, Workload object,
realization, scheduler or simulator was instantiated to obtain it.

Thus M1 can coherently measure a narrow local multi-ready-H mapping opportunity, but its absence
cannot establish absence of the broad registered remaining-H-path/ordinary-L resource blocking
mechanism. D08's negative mainline-stop interpretation needs revised observation coverage before
approval (V2-F01). M2 still cannot establish mapping's independent causal contribution.

## Three-state logic versus scientific interpretation

Given f>0 and valid ordered intervals, L_c≥f and U_c<f cannot both hold. K_c≥8 and K_c≤2 are likewise
disjoint. With preconditions prioritized, the written SUPPORTED/NOT_SUPPORTED/INCONCLUSIVE branches
are mutually exclusive and exhaustive; META checks include abstract boundary cases. Missing/invalid/
incomplete evidence or zero eligible views go to INCONCLUSIVE/BLOCKED, never zero opportunity.

This logical consistency does not validate what the observed quantity represents. No choice between
FINE and COARSE repairs V2-F01. Shared paired-seed indexing and pointwise percentile intervals follow
the registered method in intent; their concrete implementation and diagnostic coverage remain pending.

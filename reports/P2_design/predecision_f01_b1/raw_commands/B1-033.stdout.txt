# F01 — observation domain and negative evidence options

Status: PROPOSED_REQUIRES_APPROVAL; route UNSELECTED; D07/D08 and SP25/SP31/SP36 UNRESOLVED_BLOCKING. This document is not an executable observer. Exact source hashes and line/pointer evidence are in evidence_index.json and source_evidence_manifest.json. Original user_request §44 (lines1431–1494) permits2–4-ready local oracle; expanding to1 is a research-scope proposal, not a correction.

## Reproduced source contradiction

V2 templates ADAS8 lines378–500 and ADAS16 lines505–727 each have exactly one root. Generation arrivals lines79–90/98–108 give slot0 H/L the same jitter (no group key); slot0 arrival is <.1P, next compressed slot >=.25P. No prior work exists at the first arrival. P1 event rules (P1_implementation_spec22–26; model_spec35–42; engine47–77, read only) expose both arrivals before feasible dispatch. Whichever positive-duration compatible root starts first, another dependency-ready root remains and an arrived H service still has not-started descendants. Valid B2 starts one feasible root; a NONE on fully idle feasible work would be a correctness failure, not a way to remove this proof premise.

Exactly the next actual invocation is recorded by snapshot_spec53–63, including a NONE/wait outcome; no invented polling is needed. A start changes running/public node status, so state hash/equivalence changes even at identical virtual now. Diagnostic_spec22–26/107–115 makes this eligible but not FULL: E0 includes it, F0 does not. Thus finite valid ADAS stream E0−F0≥1. If F0=0, p undefined, precondition fails. If F0>0, F0/E0=1−(E0−F0)/E0<1. All12 loaded-condition/all10seed negative requires coverage1 everywhere;4 ADAS loaded conditions already prevent this. Invalid/missing streams close earlier. This proves current negative unreachable, not science failure, not support coverage4/5 unreachable, not actual frequency.

## Common classification rules

All raw events and original E0 states retained under all routes. Missing/corrupt expected state makes denominator unfinalizable (INCOMPLETE/INVALID), never a legitimate exclusion or zero gain. E0=0, analysis denominator0 or covered count0 gives undefined p and INCONCLUSIVE if attempted. No evaluation (current) is NOT_EVALUATED. Source selection remains B2-only A-before-B, no outcomes select route or thresholds.

Common V requires all2520 primary/replay/trace/metric artifacts valid,18 conditions selected before analysis,120 paired loaded-condition/seed cells, independent observer verification, complete M2 paired/report validity, explicit approved route and threshold before data. Common bootstrap remains10000 paired seed replicates,20261018,type7,pointwise descriptive intervals conditional on selected calibration; unchanged rejection sampling and shared index vectors. No intervals/indices computed now.

For a chosen route define p=hits/F, K=#seed(p≥f). Ordering:

| Priority | Condition | Result |
|---:|---|---|
|0|No evaluation performed|NOT_EVALUATED|
|1|Attempted but V false, required denominator zero, or support coverage condition false|INCONCLUSIVE; invalid/incomplete evidence retained separately|
|2|V, support coverage in every cell, each12 condition CI_low≥f and K≥8|SUPPORTED within route scope|
|3|V, negative coverage in every cell, each12 condition CI_high<f and K≤2|NOT_SUPPORTED within route scope|
|4|All other cases, including boundary CI_high=f|INCONCLUSIVE|

CI_low=f can support; CI_high=f cannot be negative. Support and negative cannot both hold for valid ordered CI/f>0. These conditions preserve the existing unapproved numeric proposals; no bundle selected. SUPPORTED still cannot authorize progression by itself. NOT_SUPPORTED and INCONCLUSIVE both block progression; only the former supplies the route's registered narrow negative claim.

## Route A — original population and coverage

E=E0; F=F0 original FULL. F0 requires2..4ready,≤2pending H, complete approved public graphs/calendar, predictable running release and full enumeration. All partials remain E0−F0. p=hits/F0, coverage=F0/E0. Support coverage≥4/5; negative coverage=1. No scientific definition or threshold is changed. ADAS therefore cannot support the negative branch; successful valid science can still be INCONCLUSIVE indefinitely. A route choice would explicitly accept that information limitation and blocking consequence, not assert mechanism absence. This is the least change but not a general solution to establishing negative evidence.

## Route B1 — explicit expansion of diagnostic ability

E=E0 unchanged. F=F1, exactly the original FULL predicate except1..4ready qualifies. With1ready, K contains that one task; enumerate its entire compatible resource set with the same public exact-rational calendars, H targets, fixed suffix, L node cap and ties. All other resource/target/calendar caps unchanged. Max4actions/6^4assignments/36projected nodes does not increase. Support F1/E0≥4/5, negative F1/E0=1, p=hits/F1.

This removes only the demonstrated single-ready obstruction. >4ready,>2pending H or expired running estimates still cause partials and may make global negative unreachable. No guarantee of empirical prevalence or complete coverage is claimed. It expands original§44 and SP25, so requires explicit research-scope approval; it is not selected or activated here. Fixed suffix remains fixed; no candidate or suffix optimizer is proposed. Original thresholds survive as proposed literals, not as justified values for the changed observer.

## Route B2 — explicit conditional target population

Original E0 remains the complete audit population. Define A0 before any gain calculation as eligible E0 states satisfying2≤ready≤4,1≤pending H≤2, all busy elapsed<estimate, complete approved arrived graphs/public calendars. A0 membership may use only public structural predicates; it must not depend on favorable g, projection success or analysis outcome. F_A consists of independently verified complete original projections for A0.

Preserve E0−A0 with reason codes/state refs. An error or missing record inside A0 does not change membership: it is INVALID/INCOMPLETE and blocks. Report E0,A0,F_A,excluded, A0/E0,F_A/E0,F_A/A0 separately for every seed/condition. A0=0 =>INCONCLUSIVE, not0hit.

Proposed conditional p=hits/F_A; positive coverage F_A/A0≥4/5; negative F_A/A0=1. This EXPLICITLY changes denominator meaning; original F_A/E0 is still always reported and never renamed to look complete. Under V, all A0 projections must verify, so F_A=A0 and the4/5 gate is redundant; it offers no assurance of A0 prevalence. No new prevalence cutoff is invented. Conditional negative cannot refute opportunity in excluded E0 states or the original broad mechanism. The user must separately decide whether a permanent research stop on such narrow evidence is acceptable. Otherwise reject/defer B2. The original hypothesis is retained verbatim, with a weaker observer unable to establish its global absence.

## Coverage, thresholds and tradeoffs

FINE=(tau1/100,f1/100); COARSE=(tau1/20,f1/20);8/10support,≤2/10negative,4/5positive coverage,1negative coverage remain UNAPPROVED. Source supports stable opportunity as a research condition and paired analysis, not unique numeric sufficiency. Positive witness versus exclusion evidence has a qualitative asymmetry; none of these numbers has demonstrated power. State counts are trajectory-selected and not independent time samples. Conditional FULL p does not describe excluded states. More permissive domain is not evidence of a stronger inference, and choice cannot use future outcomes.

| Route | Fairness/reproducibility | Cost | Statistical/research scope | Remaining risk |
|---|---|---|---|---|
|A|All original states/rules retained; exact existing reproducibility|No new projection type|Original narrow estimand retained|Negative impossible for ADAS; no guarantee support|
|B1|Same stream and seed pairing; exact expanded predicates must be frozen|More states analyzed, same per-state upper bound|Expands permitted oracle scope|Other exclusions still prevent negatives; power unknown|
|B2|E0 and exclusions retained; selection-before-g mandatory|No more projected states than original FULL|Conditional estimand; population claim weakened|A0 can be sparse, negative cannot refute excluded-space mechanism|

Engineering advice (UNAPPROVED): A is the least scope change; B1 is a bounded extension requiring§44 approval; B2 is interpretable only with explicitly conditional claims and accepted stop policy. No universal recommendation can replace the user's choice of scientific question/evidence strength. None is a default.

## Fixed suffix counterexample retained

Read preserved audit M1R_adversarial_cases.md Case7 lines70–101. Hand COCKPIT state now20 has two pending H suffixes and two terminal CPU-only L action tasks. All16 current K mappings yield g=0 under the fixed suffix. Move only H_A.compose fromGPU toNPU: b=1+2lambda+213/32; alternative=1+2lambda+1593/256; lambda is exact rational binary64(.05). Delta=111/256ms and Delta/b>1/20. This is hand algebra, not actual B2 reachability/frequency/science. FULL is exact within registered K/fixed-suffix space only, not all public mappings. It survives A/B1/B2; none proves mechanism absence. Local L slack also cannot prove whole-service L-P95≤1.10.

## Questions and future tests

Choose exact route A/B1/B2 or request a complete alternate before approval. For B1 explicitly decide the§44 extension; for B2 explicitly accept/reject conditional estimand and operational stop. Select FINE/COARSE only after domain choice; direction agreement does not approve unknown future values. Future authorized implementation must test actual hook completeness, duplicate states, one-ready, no-ready-H/pending-H, caps, elapsed boundaries, missing/corrupt, zero and exact tau, exact ties and prefix/suffix distinction against original P1 behavior. All runtime/scientific tests NOT_RUN.

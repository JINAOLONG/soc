# Challenge review of four emerging findings

This is a separate read-only reasoning pass within the same Codex assistant team. It is not a third-party audit. No generator, scheduler, simulator, diagnostic, statistical resampler or scientific worker was imported or executed. The examples below are logical deductions from unapproved specifications and source text. All D01–D10 and SP01–SP40 approvals remain UNAPPROVED.

The scope was to try to refute or narrow four candidate findings. Source hashes and review scope are in `challenge_source_reads.json`; commands and complete raw outputs are in `challenge_commands.json` and `raw_commands/challenge-*`.

## C1: the current all-condition NOT_SUPPORTED branch is unreachable

**Challenge result: confirmed as a specification-level derivation, conditional on implementing the current v2 rules without changing them.** It does not establish any future scientific result, the numerical opportunity rate, or whether SUPPORTED is reachable.

An ADAS argument is sufficient; there is no need to assume all scenes behave this way:

1. `P2_workload_templates_v2.json#/templates/2` and `/templates/3` have exactly one root each: ADAS.n01 and ADAS.n01.a. They have respectively seven and fifteen nonroot nodes. Both H and L use the graph. The root's preprocess role has positive compatible CPU/GPU costs (`P2_resource_profiles_v2.json#/profiles/8`).
2. `P2_generation_spec_v2.json:98–108` admits one H and one L at the same first slot time. Jitter is in [0,1/10), so the next slot is strictly later: the exact difference exceeds P(1/4−1/10)>0. At the first slot there are only the two root tasks; no previously admitted work exists. This uses only the jitter range and formula, no actual seed or draw.
3. Under `docs/model_spec.md:39–46`, all same-time arrivals are exposed before dispatch. B2 prioritizes H (`docs/baseline_spec.md:14–20`; `src/soc/scheduler/kernels.py:161–177`). All resources are initially idle, so H's root can start. Its positive execution duration prevents completion during the same zero-time dispatch cycle. If an input failed the positive representable-duration checks, it would be invalid rather than a counterexample to the valid-complete argument (`src/soc/simulator/engine.py:67–70`).
4. Before the next scheduler call, the public view contains the running H root, its unstarted descendants and the one ready L root. The engine source explicitly refreshes and calls again after each start (`src/soc/simulator/engine.py:47–77`). v2 requires exactly one observation per actual call, including after a start (`P2_public_snapshot_spec_v2.json:52–62`). The snapshot is recorded even if the next call returns NONE because L's preferred resource is occupied.
5. That view is in E: at least one ready action and an arrived H service with at least one not-started node. It is excluded from F because ready count is exactly one (`P2_diagnostic_spec_v2.json:21–27,57–61,107–113`). It cannot be removed by state deduplication: the running/status/resource content differs from the preceding two-ready view. Deduplication retains one representative of this unique state, not zero representatives (`P2_public_snapshot_spec_v2.json:51–62`).
6. Therefore each valid ADAS MAIN B2 stream has E−F≥1. If F>0, F/E<1; if F=0, the criterion precondition already fails. This is independent of A/B period choice, 8/16 size and the unknown registered draws.
7. The twelve selected medium/near conditions necessarily include ADAS-medium-{8,16} and ADAS-near-saturation-{8,16}. `P2_criterion_spec_v2.json:46–53,79–87` requires coverage exactly one for every seed/condition to classify NOT_SUPPORTED. Those four ADAS conditions defeat that conjunction for any valid complete matrix. If qualification or integrity fails, NOT_SUPPORTED also cannot be reached through the prescribed decision order.

Exculpatory possibilities considered and rejected: observing only the batch's first call (contradicts exact hook rule); dropping single-ready views from E (contradicts eligibility); treating the H target as absent while its root runs (explicitly contrary to pending-H-descendant eligibility); collapsing the post-start view with the pre-start view (public state differs); selecting B instead of A (same graph/paired arrival structure); counting replay in coverage (prohibited); skipping ADAS (violates all-condition criterion).

This is a serious decision-readiness issue: a nominal three-way scientific classification has a structurally unavailable negative branch. It is not automatically an unsound false-positive rule, and INCONCLUSIVE still fails closed. The user can intentionally choose a one-sided operational screening policy, but that would require an explicit, consistently documented decision. No replacement threshold, scope or observation policy is approved by this report.

## C2: concurrency and stale-lock semantics

**Challenge result: retain as a bounded engineering specification gap, not a demonstrated race or runtime failure.**

The design already contains meaningful protections. `P2_runner_schema_review_v2.md:46–54,79–93` requires input/run locks, immutable receipts, fsync and parent-directory persistence, atomic publication, a CAS completion pointer, conflict fail-closed behavior, preserved owner/lease/attempt receipts, explicit authorization before releasing/archiving a stale lock, and zero automatic restarts. A finding claiming those rules are entirely absent would be incorrect.

What remains unspecified is which common semantic operation the exclusion protects when authorizations/attempts differ. INPUT_LOCK_PREIMAGE includes generation_authorization_sha256; RUN_LOCK_PREIMAGE includes attempt_id; attempt identity itself includes authorization. Distinct authorization can therefore give distinct lock IDs for the same descriptor or run. An identity is not by itself a locking algorithm or shared exclusion key. There is no explicit rule making the descriptor/run the mutual-exclusion domain across authorization scopes, no typed owner/lease receipt, and no stale-owner fencing predicate for post-release publication. R1 being the sole formal entrypoint does not explicitly establish a singleton process.

CAS and immutable files can stop final overwrites while still leaving duplicate process calls or partial artifacts unless exclusion and budget reservation are also defined. The report must not claim that duplicate calls actually occur. An implementation could enforce one global single-writer or a descriptor/run exclusion policy, but choosing that policy silently would fill a missing design convention.

Future separately authorized tests should cover two simultaneous requests with identical IDs; same descriptor/run under different authorization IDs; contention before process start; stale lock release while the old owner remains alive; old owner publication after replacement; crash between fsync/receipt/CAS; and exact reuse after winner publication. Each should verify at most the permitted call count and preserved failure evidence, not only final file equality.

## C3: actual execution Git HEAD and dirty status

**Challenge result: retain as a mandatory evidence-binding gap, with an explicit limit on the claim.**

`AGENTS.md` rule 11 and `docs/user_request.txt:2506–2527` require actual run Git commit and dirty status. v2 runner prose explicitly promises that actual execution HEAD is separately recorded (`P2_runner_schema_review_v2.md:30–32`). The earlier draft schema also had required `git_commit` and `dirty_status` (`scientific_artifacts.schema.draft.json:53–70`), so this is not a newly imposed requirement.

In v2, SOURCE_BUNDLE_PREIMAGE has source_commit and a constant dirty_policy. SCIENTIFIC_RUN_RECORD and PROCESS_RESULT do not have a required actual execution HEAD or observed dirty-status value, and the associated conditional semantics do not require a typed provenance receipt. Source content can remain identical across a later documentation commit; source_commit is not necessarily the checkout HEAD that executed. A rejection policy is not an observed status.

The schema does allow generic raw_artifacts references. An implementation could place a Git-status report there, so it is too strong to claim the data cannot be represented at all. The supported finding is that its required kind/schema, membership, capture point and independent check are not bound. Generic references also permit a record with no such artifact. This must be resolved before the design claims complete machine-checkable provenance.

## C4: M2 paired completeness

**Challenge result: retain as a cross-document completeness/binding gap, not an absence of the M2 requirement.**

The v2 decision table explicitly requires M2 paired completeness (`P2_mapping_opportunity_decision_table_v2.md:20–22`). M2 is described in the main proposal (`P2_complete_design_proposal_v2.md:156–157`), is SP27, and occurs before D08 in the runner (`P2_runner_schema_review_v2.md:55–56`). Existing trial records contain the constituent methods on common input, which is useful evidence and could support future derivation.

However, `P2_criterion_spec_v2.json#/preconditions` has no explicit M2 paired-complete predicate, and `P2_stage_state_contract_v2.json#/progression_conjunction` has no bound M2 evidence membership. STAGE_RECORD permits diagnostic_report_ref and generic prerequisite_evidence; neither defines required M2 pair identities/counts/metrics, pairing-verification status, or missing-pair rejection. The generic references can carry M2 evidence, so the representational impossibility claim is refuted. The exact enforceable stage predicate remains underspecified.

All per-trial method results being present is necessary input for M2, but does not itself establish that the required cross-method pairing and summary were produced or independently checked. A later implementation task should not decide ad hoc whether an otherwise schema-valid stage with no M2 pairing report satisfies the human-facing precondition.

## Reporting limits

The command output label `closed=False` in challenge-007 prints the literal value of `additionalProperties`; it means `additionalProperties: false`, so the object is closed. It does not mean the object is open. A probe for `configurations` returned null because the actual matrix field is `configs`; challenge-008 subsequently read that correct field. Neither diagnostic probe was a scientific operation or an audit assertion.

No current documents were edited to close these gaps. The structural C1 issue warrants revision before informed approval; C2–C4 need explicit evidence/engineering bindings and runtime verification in a future separately authorized task. The current report does not approve any proposed repair or execute any classification.

## Additional hand challenge: Case 7 fixed-suffix example

The COCKPIT example in `M1R_adversarial_cases.md` Case 7 was checked against the original graph, resource costs and communication table, by hand only. No suffix enumerator or scheduler was implemented.

The example survives the earliest-whole-gap and CPU-alternative challenges. With r=21 and lambda equal to the exact binary64 encoding of 0.05, A-compose's GPU finish r+lambda+1/32+2 beats its earliest possible CPU finish r+6 and NPU finish r+lambda+1/16+3. The available GPU gap after B-display becomes data-ready and before A-compose starts is only 3/128 ms, less than display's 2 ms. B-display and B-route's fixed GPU finishes r+lambda+1/32+4 and r+lambda+1/32+7 both beat any CPU finish, whose lower bound is r+8 before accounting for K contention. For B-compose, same-GPU predecessor transfers are zero; an NPU placement incurs positive GPU-to-NPU transfers and a 3 ms duration, so it cannot beat the fixed GPU result.

Both winning H interaction tasks start after time 23. Every one of the sixteen CPU-only current-K placements finishes by 23. Thus K cannot alter the winning suffix route; any CPU candidate delayed by K was already slower than the winning GPU placement. This proves all-K invariance without enumerating a schedule in code.

Changing only A-compose to NPU frees the GPU earlier. The two mean-H finishes differ by exactly 111/256 ms; lambda cancels. Baseline remaining mean is 1+2*lambda+213/32, so the explanatory relative improvement exceeds 1/20. The alternative is outside the fixed-suffix observer's search space. This confirms an already disclosed scope limitation, not a new scientific or runtime finding. No claim is made that this public state occurs under actual B2 calibration or at any particular frequency.

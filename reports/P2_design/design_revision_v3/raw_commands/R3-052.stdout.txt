# M1R fresh adversarial review — report only

Review scope: the unapproved v2 bytes at the task starting commit. This is a coordinated review by the same assistant environment, not third-party independence. No Workload/Service, physical trace, production snapshot, diagnostic result, seed draw, bootstrap index or scientific observation was instantiated. Nine numbered cases below are logical public-state descriptions and hand calculations. Examples explain specification behavior; none is an empirical project outcome. All D01–D10 and SP01–SP40 remain UNAPPROVED.

**Blocking result: M1R-F01. The proposed global NOT_SUPPORTED branch is unreachable under the registered ADAS first-arrival and post-start observation rules.** This is separate from the disclosed limitation that FULL coverage still covers only a fixed-suffix surrogate. Do not modify v2 to resolve either issue in this report-only task.

## Definitions used by every case

Sources S3:20–61,107–119 and S4:50–63 define E as unique in-scope primary MAIN-B2 public states, F as VALID_FULL states, hits as F states with g>=the preapproved tau, and p=hits/F. A partial state contributes one to E, none to F, and no hit observation. That is an excluded observation, **not a measured zero gain**. No arbitrary epsilon. Dedup is within one primary attempt; a repeated identical body contributes no new E/F/hit; a real start changes the body. Replays never contribute.

All descriptions assume a new unique state and a complete valid primary stream unless explicitly stated. E/F/hit notation below gives the *increment* from that state, not an observed experiment total. If missing/corrupt evidence prevents deciding eligibility, E/F/hits cannot be finalized; never assign zero increments to hide the gap. S6:21–34 also requires M2 completeness; the explicit M2 predicate is absent from S5:46–53, a separate cross-document issue owned by the decision-readiness review.

## Case 1 — Exactly one ready node; H has an unready remaining path

Source: S3:22–26,58–61,108–113; S4:53–63; S10:378–500 and 505–727; S11:79–90,98–108; S18:22–26; S19:47–77; S20:88–92; S5:76–82.

Expected: IN_SCOPE, COVERAGE_INSUFFICIENT/READY_COUNT_BELOW_TWO, no enumeration. Increment E=1, F=0, no hit observation, g=null if uncomputed. A complete stream consisting only of such states has F=0 and undefined p, never p=0.

**Unavoidable ADAS prefix proof, independent of scientific draws:**

1. In ADAS-8, n01 is the sole root; in ADAS-16, n01.a is the sole root. Every service has remaining descendants.
2. MAIN slot 0 admits H and L at the same time by S11:106. With U in [0,1), a0/P<1/10, a1/P>=1/4; all later slots arrive later. Thus the earliest arrival has exactly two roots. There is no earlier running work.
3. Resources start idle; roots have positive compatible estimates/realized durations. A feasible first start exists. A conforming B2 starts H first under S17:17; an erroneous NONE despite all compatible resources being idle would be a correctness failure, not a valid way to escape the proof. The proof itself does not depend on which of the two roots starts.
4. Immediately after that one start, before positive time advances, exactly one of the two roots remains dependency-ready. No child has become dependency-ready because the started root has not completed. H still has not-started nodes whether H or L started first.
5. S18:D5 mandates recomputation after each start; existing S19:47–77 returns to the next observation/choose call immediately. S4:61 requires exactly one record per actual invocation, including this view. A sole remaining L that chooses to wait on a busy GPU does not erase the pre-call snapshot.
6. This state is uniquely in E and cannot enter F. The running set changed, so S4:56 dedup cannot collapse it with the pre-start state. Even a duplicate later event preserves its earliest representative.
7. For every finite valid ADAS MAIN-B2 stream, E-F>=1. If F>0, F/E<1; if F=0, the criterion precondition fails. The argument covers both sizes and both A/B periods and does not use actual seed values or outcomes.
8. Every selected 12-condition loaded grid includes four ADAS medium/near × 8/16 conditions. S5:81 demands coverage=1 in **every** seed/condition. Consequently the global NOT_SUPPORTED branch is unattainable in this design, including a hypothetical completely observed absence of gain in every FULL state. If A/B qualification itself fails, P2 remains blocked earlier; that does not rescue the unreachable negative branch.

This does **not** prove support coverage 4/5 is impossible, does not estimate coverage, and does not calculate an outcome. It proves a conflict between a categorical coverage condition and required event granularity. Future authority must choose a coherent estimand/negative policy before approval; report-only review cannot silently exclude the troublesome view or relax 1.

## Case 2 — Two to four ready nodes, no ready H, pending H successor

Source: S3:22–27,44–55,58; S22:131–154; original explanatory example S1:1115–1156.

Expected: a FULL observation is permitted even when every K node is L: H eligibility is based on arrived pending H descendants, not ready-H membership. With complete approved DAGs, <=2 H targets and predictable running releases, E=1,F=1; hit depends on calculated g. Case 7 gives an explicit two-L-ready/two-H-unready public-state calculation with g=0 under the current fixed suffix, so its increment is E=1,F=1,hits=0.

For intuition only, original §32's running H prefix forecast2, H NPU suffix4, L NPU6/CPU6.5 and a second harmless ready L node give forecast H10 vs6 if that current L mapping is changed and the second L has no relevant conflict; cap=max(6,12)=12 admits6.5. Hand gain is (10-6)/10=2/5. These small explanation fragments are not an approved scientific 8/16-node workload and were not submitted to an observer. They explain why the v2 *eligibility* improvement addresses historical M1's ready-H blind spot; they cannot establish frequency, real H DMR or L P95.

## Case 3 — More than four ready nodes

Source: S3:23,27,30–42,58–61; S4:54–60.

Five ready nodes and one pending H are IN_SCOPE. Select the first four by fixed B2 order only for an optional bounded description. FULL is forbidden because at least one ready action is excluded. Expected COVERAGE_INSUFFICIENT, E=1,F=0,no hit observation. An improvement in the optional subset is not a hit; failure there is not zero opportunity. Changing which fifth node is excluded after observing gains violates the proposal. State frequency is not a time-weighted occupancy rate.

## Case 4 — More than two unfinished arrived H targets

Source: S3:22,24–27,58–61; S21:1169–1300; S20:54–58,62–81.

Use two ready L actions and three arrived H services each with a not-started descendant. The first two H targets are fixed by deadline/service-ID before gain calculation. Expected COVERAGE_INSUFFICIENT; E=1,F=0,no hit observation. Omitting the third H from its recorded count or treating its absence from the projection as no impact is prohibited.

**Completion boundary:** the source counts H services with **at least one not-started node**, not every not-yet-completed H service. An H service whose only unfinished node is already running has no controllable pending node and is not a target. If two H have pending nodes and a third only has a final running node, the target count is two; that third running task still contributes its resource reservation and its expired estimate can invalidate FULL. If all H work is running/completed with no not-started H node, the state is NOT_IN_SCOPE (E=F=hits increment0), even if L ready nodes exist. This follows the exact source predicate; no completion-time truth is needed or allowed.

## Case 5 — Visible running task with elapsed >= estimate

Source: S3:26,45–46,58–61; S4:50,63; S15:48–52; S18:25; S21:1243–1300.

At equality, e.g. public estimate2 and elapsed2, a still-running task is an ordinary possible overrun, not a malformed public state. For otherwise eligible 2–4 ready / <=2 target H, expected COVERAGE_INSUFFICIENT; E=1,F=0,no hit observation. No guessed now release, epsilon or hidden completion timestamp may be used. `elapsed>estimate` has the same coverage result. A corrupt elapsed inconsistent with RN64(now-start), or a completed task falsely duplicated in running, is instead INVALID. Equality is not rescued by the max(0,estimate-elapsed) expression because the diagnostic explicitly overrides FULL when the unit is still visibly busy.

This exclusion can correlate with resource congestion and model error. No data were inspected, so its frequency or the direction/magnitude of selection bias is unknown.

## Case 6 — Missing/corrupt versus legitimate partial snapshot

Source: S3:59–61,119; S4:59–62; S5:46–53,69–72; S21:1117–1358.

Missing expected hook/body/ref/required field: INCOMPLETE. Hash mismatch, malformed/nonfinite timing, illegal predecessor identity, contradictory running/completed membership or independent recomputation mismatch: INVALID. The plan stops and stage cannot pass; the denominator remains unfinalizable. Neither means E=0/F=0/hits=0 for a silently discarded observation.

A complete valid body showing five ready nodes, three pending H targets, one ready node or a legitimate running overrun is COVERAGE_INSUFFICIENT; E=1,F=0,no hit. This retains a known denominator observation without inventing gain. `template_id` and size must derive from public IDs/node count (S4:63), not private generator fields; completed finish/resource and running start/elapsed are public facts. PUBLIC_NODE estimates/edges and completed outputs suffice to derive dependency-ready/data-ready; no future-completion field is present or needed. Template mismatch cannot be excused as an acceptable truncated sample.

## Case 7 — Fixed suffix can hide an available public mapping improvement

Source: S3:23–27,45–55,58,115; S10:COCKPIT-8 at 17–138; S12:64–187 (intent/display/route/compose/interaction profiles); S13:COCKPIT edges18–95 and links639–702; S15:20–31; S22:173–174.

This is a hand-authored public-state calculation using COCKPIT-8 topology and profile base estimates, not a generated input or proof of occurrence under a selected seed/B2 trajectory. No production snapshot or schedule artifact is created. Public history can be valid; actual complete B2 reachability/frequency is deliberately unclaimed.

Let now=20. H_A and H_B use the complete COCKPIT-8 graph; H_A sorts first by deadline/service ID. All unmentioned required predecessors have known completions early enough that the stated running-prefix completion controls readiness. H_A has route n06 on CPU0, estimate8, start13, elapsed7, forecast release21; its display n04 is already complete on GPU0. Its only not-started nodes are compose n07 and interaction n08. H_B has intent n03 on CPU1, estimate1, start20, elapsed0, forecast release21; navigation n05 is complete on CPU3. Its unstarted nodes are display n04, route n06, compose n07, interaction n08. All other H nodes are completed with compatible fixed resources and predecessor identities.

K consists only of two L terminal interaction nodes, each CPU-only estimate1 with all destination copies available by now20 and service deadline>=23. There are no other ready actions or pending H targets. L predecessors are already complete. CPU2/3 are idle. All 4² current-action assignments finish by23 (even both on a busy CPU, sequentially21..22 and22..23); they cannot delay the later H CPU suffix nodes. Thus none of the 16 K assignments alters the relevant suffix calendars. L cap admits the placements. There is no truncation or expired running estimate.

Let lambda be the **exact rational encoded by binary64 0.05**, and let r=21. Edge sizes and power-of-two bandwidths below are exactly representable. Source forecasts use rational lambda, not a hidden true duration. The source suffix order is H_A.compose, H_A.interaction, then H_B.display, H_B.route, H_B.compose, H_B.interaction. Static Kahn/service ordering places earlier-service nodes first but allows insertion in later idle gaps.

| Suffix node | Current fixed-EFT forecast finish (decimal display) | Alternative only H_A.compose→NPU (decimal display) |
|---|---:|---:|
| H_A compose | r+lambda+1/32+2 ≈23.08125, GPU | r+lambda+1/16+3 ≈24.1125, NPU |
| H_A interaction | r+2lambda+101/32 ≈24.25625 | r+2lambda+69/16 ≈25.4125 |
| H_B display | r+lambda+1/32+4 ≈25.08125, GPU | r+lambda+1/128+2 ≈23.0578125, GPU |
| H_B route | r+lambda+1/32+7 ≈28.08125, GPU | r+lambda+1/128+5 ≈26.0578125, GPU |
| H_B compose | r+lambda+1/32+9 ≈30.08125, GPU | r+lambda+1/128+7 ≈28.0578125, GPU |
| H_B interaction | r+2lambda+325/32 ≈31.25625 | r+2lambda+1041/128 ≈29.2328125 |

Why the baseline picks these resources: compose GPU2 beats NPU3 and CPU6 at its ready time; H_B display GPU2 beats CPU8 even after H_A's GPU reservation; H_B route GPU3 beats CPU8; subsequent compose remains fastest on GPU. The initial gap between H_B display's readiness r+lambda+1/128 and H_A's GPU start r+lambda+1/32 is only3/128ms, too short for display2. Changing only H_A's *suffix* mapping to NPU removes that GPU reservation. CPU tasks' later finish choices have spare identical cores; K cannot obstruct them after23. All edge copies use the source/destination bandwidths in S13, including GPU→CPU1/8 and NPU→CPU1/4 for the compose→interaction edge.

The source's fixed-suffix diagnostic reports g=0 for every K assignment: expected FULL, E=1,F=1,hits=0, NO_IMPROVEMENT_IN_TESTED_SPACE. The hand alternative lies outside that enumeration, not outside the public information boundary. It gives:

- b = 1 + 2lambda + 213/32 ≈7.75625.
- o_alt = 1 + 2lambda + 1593/256 ≈7.32265625.
- b-o_alt = 111/256ms > 0, and (111/256)/b > 1/20.

The coordinated challenge reviewer independently checked the short GPU gap, CPU/NPU alternatives, all16 current-K invariance and exact111/256 arithmetic from the source definitions. This remains same-assistant team review, not third-party independence. The report-only scalar checker `m1r_static_checks.py.txt` independently checks the closed-form equality and gain boundary without any scheduling/projection code.

These are **hand-calculated explanatory numbers**, not stored scientific gains or a new algorithm. They show FULL means complete coverage of the declared current-K/fixed-suffix space, not all public remaining-H mappings. The report does not propose implementing suffix search. Any observer change needs separate explicit UNAPPROVED design review. The current source already disclaims global absence; a permanent stop based on this surrogate is a conservative research-policy choice, not a deduction that the original mechanism is absent.

## Case 8 — Local L slack permits degradation without L-P95 compliance

Source: S3:52; S22:143–146; S16:3–11,22–26; S1:1115–1156.

The constraint is node finish <=max(baseline node finish, service absolute deadline). For baseline L-node finish6, service deadline12 and proposed finish6.5, cap12 admits degradation. If all other FULL conditions hold, E=1,F=1 and the H gain decides hits; local L admission itself is neither a hit nor a budget pass.

A hand counterexample to global implication: let an L node's finish move6→8 under cap12 and a required CPU-only L successor take2ms with no extra wait/communication. Full L response moves8→10; ratio10/8=1.25>1.10. The scalar cap holds while the full-service ratio violates the budget. This is a logical example, not a generated L sample set or actual P95. The same shift across any hypothetical identical collection leaves type-7 P95 at those values, so no quantile theorem rescues the implication. Even a point ratio<=1.10 would not establish the registered paired-seed CI upper bound. L successors/unselected L work are excluded from M1R (S3:27); the future scientific L budget still needs its full independent metric/CI evidence.

## Case 9 — Zero, exact threshold and deterministic ties

Source: S3:48–55,68–70,108–113; S5:15–29,76–87; S6:33–34.

For a complete FULL state with b>0: g=0 is NO_IMPROVEMENT_IN_TESTED_SPACE and E=1,F=1,hits=0. 0<g<tau is SUBTHRESHOLD_IMPROVEMENT, same counts. At g=tau exactly, MATERIAL_IMPROVEMENT_IN_TESTED_SPACE and E=1,F=1,hits=1 because the rule is >=. Hand scalar checks b=100,o=99 (FINE) and b=20,o=19 (COARSE) are exact rational boundary examples, not diagnostic executions. A nonpositive b contradicts the required positive-pending-H model and must not be divided or patched with epsilon.

Equal H objectives are resolved by lexicographic resource-ID tuple in K order, independently of enumeration traversal. Greedy/suffix EFT ties also use fixed resource order. If several minimizers include a different assignment but g=0, a change of mapping is still not a hit. At criterion level CI_low=f is permitted for support, CI_high=f is not negative; 7 support seeds or3 threshold-meeting seeds in the negative branch cannot qualify. No CI or seed rates were calculated here.

## Scientific interpretation and decision needed

Original mechanism (S2:16–24; S1:§32/§44): a locally fast mapping may occupy a scarce resource needed by another arrived H path; joint ordering/mapping may reduce actual H deadline misses subject to actual L P95 protection. M1R can support only that, along B2-observed public states and under estimates, changing current ready mappings with fixed order/fixed H suffix can improve mean projected completion of at most two pending H services while obeying a local L-node cap. It does not isolate a scarce-resource explanation for every hit unless the recorded blockers demonstrate it; generic projected mean improvement is the observer's numerical target.

A positive does not imply actual H DMR reduction, the full-service L budget, candidate success or independent causal mapping contribution. A negative does not establish absence under other suffix mappings, ready orderings, later arrivals, other B2-independent trajectories, excluded target/work states, true durations or the whole hypothesis. Case7 demonstrates one such gap within complete public information; Case1 demonstrates that the current negative branch cannot be reached at all under the proposed grid.

Original sources require stopping progression without stable opportunity (S1:1490–1494,2730–2738; S2:35–38), so conservative stopping is authorized in principle. They do **not** uniquely identify the v2 surrogate or validate its proposed numeric thresholds. An operational NOT_SUPPORTED stop can be justified only as an explicitly approved bounded-evidence policy with stated false-negative risks, not a theorem. Current contradictions require revision before a ready-for-approval verdict; INCONCLUSIVE continues to block progression and cannot be relabelled as scientific absence.

Unapproved options for a future documentation task: (a) retain the observation granularity but redesign how negative evidence and coverage are interpreted; (b) explicitly redefine the estimand/domain and expose excluded single-ready states separately, with no claim of broader coverage; (c) revise the bounded observer under separate scope approval; or (d) explicitly accept a one-sided support-only decision framework and remove the misleading reachable three-state claim. This audit selects none, changes no threshold/domain, and authorizes no implementation.


## Source identities

Every S-reference above/below resolves to these actual repository bytes. Line numbers are 1-based physical text lines; full bytes and numbered text are preserved in m1r-001 through m1r-005 read logs. Source code was read, never imported or executed.

| ID | Path | SHA-256 |
|---|---|---|
| S1 | `docs/user_request.txt` | `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461` |
| S2 | `docs/research_contract.md` | `8ccd2f6fce470013af89c653eb3ff84a0b66809c56d321993cd973ebc18031e4` |
| S3 | `docs/P2_design/v2/P2_diagnostic_spec_v2.json` | `9bec37d044f4c7742d931149c195c2c3ec1540d41dc3f0a899a2b29f8c7e3e90` |
| S4 | `docs/P2_design/v2/P2_public_snapshot_spec_v2.json` | `fa4ce177c2d4a49a5f8f5b30bfa44e2b0d529f1e735ddfa259ae1811edc2f1af` |
| S5 | `docs/P2_design/v2/P2_criterion_spec_v2.json` | `98a578944e7910db933f5b3b02aee4bb03de8005853024b38cc3b02630b04e38` |
| S6 | `docs/P2_design/v2/P2_mapping_opportunity_decision_table_v2.md` | `594863a579ac32fdd980454fe6e0f0d24d165729a60f1c6f6526c8688fd296f4` |
| S7 | `docs/P2_design/v2/P2_scientific_parameter_registry_v2.json` | `15ee54e75f658d5f66edb00534003d3aed642f86736b2932ae61f0692e4559c2` |
| S8 | `docs/P2_design/P2_complete_design_proposal_v1.md` | `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac` |
| S9 | `docs/P2_design/P2_mapping_opportunity_decision_table_v1.md` | `4c981f2f2303e1b1535168dd320e3c11151ea86ad35a502513893370a5906ea2` |
| S10 | `docs/P2_design/v2/P2_workload_templates_v2.json` | `f282955ab09d0110f50447269b18d0389231bed9711532853d6cdbda92d9027c` |
| S11 | `docs/P2_design/v2/P2_generation_spec_v2.json` | `33e3ccf437510986ffa401eea1ef48e995a1ad08df38a834374d4a1c483a91f2` |
| S12 | `docs/P2_design/v2/P2_resource_profiles_v2.json` | `9eea5cfd43ce50d796a00d7cac86f9a7ca8798da4a3ea0c2fd9e598d965f13ae` |
| S13 | `docs/P2_design/v2/P2_communication_profiles_v2.json` | `74f7dde644b11d0b459fb68e9f250d9799e34f09652609b63122e0de5bf6e3b8` |
| S14 | `docs/statistical_protocol.md` | `f9c0eeb6e76f68330ba3e5d8d90e58d175c3947a1948bb41b26ad50dbc041e8a` |
| S15 | `docs/model_spec.md` | `3f74116fa6cb85e4f2db1c96d246ac830a282be28847a0af21184fde2e17197b` |
| S16 | `docs/metric_spec.md` | `c4b912fc672979ddc763d882e546b7a92bf53090e5b5dddd5777e2e867df182a` |
| S17 | `docs/baseline_spec.md` | `54a1cdb86d0235671a7d1ece31e489289c026bf083f33388580b6f3fdbb42e12` |
| S18 | `docs/P1_implementation_spec.md` | `92e9c4d0472f7893f54fc54d302d38bd224092285d78cc85ec7cdb67fef4e972` |
| S19 | `src/soc/simulator/engine.py` | `977d01f3603f516e68e922542322976b813c01aad8d2dd177a5c0ac314399551` |
| S20 | `src/soc/model/observation.py` | `40554e4ba71989223b7ba8362b7d35ae7257db030fd3e1fa04e262fb5002d0cb` |
| S21 | `docs/P2_design/v2/P2_typed_identity_schema_v2.json` | `9b478cf7e96776f6cc69f29426715efed6eec2309270be1efb3dd77985ebfbc9` |
| S22 | `docs/P2_design/v2/P2_complete_design_proposal_v2.md` | `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8` |
| S23 | `reports/P2_design/design_revision_v2/diagnostic_semantics_review.md` | `3619ae7416eabf962dbd7b06e469bf132cc1c37c07c0dc5afd00c12cdc8e8191` |
| S24 | `reports/P2_design/independent_review_v2/feasibility_and_mechanism_analysis.md` | `6b485d5eb4f4f05cadf9c3db732b9d582bb1cec45821eef84b534ed1eb59879f` |
| S25 | `reports/P2_design/independent_review_v2/findings.json` | `a56925d56f431714fbdd334bee5303a3fb58234caf26c12fa98375ce0219933b` |
| S26 | `AGENTS.md` | `5435e5e690a64e0e7f432bae22b8f459f646e12233d99a7a4b1a70266d8c9a22` |
| S27 | `STATUS.md` | `5f4c9fc321d22010400f260e8ed82a714b4a19453ae7b3102e04db93211f5222` |
| S28 | `docs/workload_spec.md` | `a098008f3abe47f4cfb830685009b19bf4d3555a8e370ad242a2fce1debea606` |
| S29 | `reports/P2_design/design_revision_v2/human_decision_packet.md` | `7c54a0f17c11036e1cb7f34b82734792746c946b20f5cf021c1ced298cc04367` |

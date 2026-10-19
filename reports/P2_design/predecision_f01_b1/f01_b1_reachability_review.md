# F01-B1 targeted structural reachability review

**PROVEN_UNREACHABLE**

Scope: all-condition NOT_SUPPORTED branch under the exact B1_EXPAND_SINGLE_READY proposal,retaining original E0 and all other limits. This is a fresh sequential same-assistant static report,not an external third-party audit. It neither selects nor approves B1/A/B2 nor revises V3. Actual scientific coverage,frequency,gain,CI and mapping classification are NOT_EVALUATED. All10D/40SP remain UNAPPROVED.

## Authority,verified start and source identity

Task attachment preserved as authorization_request.txt. Actual root /workspace/soc,origin https://github.com/JINAOLONG/soc.git,branch work,HEAD and real remote work ff3db3ca5dc3a8c8a986e66d093fb3849955b690,initial worktree CLEAN. Both expected current and prior05a7c528840b9f28f07b41354edf02b5932b87c9 ancestry checks succeeded before writes. All868 old tracked files protected. Only this NEW report directory may change; task-specific prohibition overrides AGENTS general STATUS update. No setup change or subagent invocation was needed.

Git resolves requested v1 path to docs/P2_design/P2_mapping_opportunity_decision_table_v1.md,not a nonexistent v1/ directory. Source manifest records actual bytes,SHA256,Git blob,size,version and exact pointers/line scopes. Main source rules below use actual JSON pointers,not inferred labels. Full-byte reads and prior static PASS are not scientific evidence. Historical V3 artifact manifest is rechecked without editing.

## Exact question and definitions

Counterfactual: evaluate B1 as IF its exact declared ready lower-bound extension were adopted; current draft/nonexecution guards do not supply a trivial reachability answer. Original user_request§43–44 states the hypothesis and2–4-ready oracle range. B1 is an unapproved1–4-ready extension ONLY.

- E0: globally deduplicated eligible public states in one primary MAIN-B2 stream; at least one dependency-ready not-started node anywhere and an arrived H service with a not-started node. Valid partial states remain in E0.
- F_B1: E0 states passing unchanged FULL predicates except ready count1..4: all ready fit4,all candidate pending H services fit2,complete approved target graphs and calendars,predictable running release,complete independent projection/enumeration.
- Pending H population is ALL arrived H services with at least one not-started node. Selecting the first min(2,population) does not assert population≤2; truncation remains partial.
- Negative requires F_B1/E0=1 in EVERY one of10seed×12selected loaded-condition cells,plus other unchanged preconditions. F_B1=0 or E0=0 means undefined rate/insufficient evidence; not zero opportunity.

Sources: V3 diagnostic#/route_options/B1_EXPAND_SINGLE_READY and #/inherited_v2_contract/{scope,coverage,stage_denominators};V3 criterion#/route_options/B1_EXPAND_SINGLE_READY/negative_coverage;V3 snapshot#{/counting,/dedup_scope,/exact_event_rule}. Every source identity is tabulated below. B1 does not change targets,36-node bound,suffix,elapsed expiry,L cap,cutoffs or priorities.

## Mandatory residual obstruction: three pending H services

Witness condition is COCKPIT-near-saturation-8. Registered A/B periods are12/10ms (actual matrix#/configs,scenario key). Any valid all18 selection must pick one of these two for this condition; no eligible option blocks the negative precondition even earlier. This is not a claim that every light/medium/other individual stream has the same obstruction.

Let H^(j),L^(j) denote only logical service symbols for slots j=0,1,2; no service/workload instance is created. Exact arrival rule from V3 generation#/arrivals:

    a_j_exact = P*(j/4+U_j/10), j=0,1,2, with 0<=U_j<1.

Unknown U_j are universally quantified,not calculated from any seed. The first three slots' intervals are strictly ordered (0..0.1P,0.25P..0.35P,0.5P..0.6P); their positive gaps are far above binary64 rounding in P10/P12. Both groups share the slot arrival. For either configuration:

    a_2_exact < 3P/5 <=36/5=7.2ms <29/4=7.25ms.
    t_2=RN64(a_2_exact) <=29/4,

because RN64 is monotone and29/4 is exactly representable. This is a conservative bound,not an actual arrival time or scientific parameter.

Now inspect the real COCKPIT8 prerequisite chain:

    n01 audio -> n02 speech -> n03 intent -> n06 route -> n07 compose -> n08 interaction.

The first five nodes MUST finish before n08 can start. Their minimum compatible base costs are2,3,1,3,2ms (profile#/profiles indices0,1,2,5,6); all node scales are1. These minima do not assume a jointly attainable fastest mapping. Ignoring communication,resource contention and extra predecessors only weakens a lower bound.

Generation#/algorithm states estimate factor>=9/10 and separate actual factor>=9/10,exact arithmetic before one final RN64 conversion. Therefore exact duration>=81b/100 for a node with compatible base b,so rounded actual duration>=3b/4: 3b/4 is a representable dyadic below81b/100,RN64 monotonicity preserves the floor. Across the chain the conservative dyadic floors are:

|Node|Minimum base b|Duration floor3b/4|Cumulative floor before next node|
|---|---:|---:|---:|
|n01|2|3/2|3/2|
|n02|3|9/4|15/4|
|n03|1|3/4|9/2|
|n06|3|9/4|27/4|
|n07|2|3/2|33/4|

All these sums are small exact binary64 dyadics. Arrival/start times are nonnegative. Inductively if predecessor finish>=B,the successor cannot start before that finish; with duration>=d,its RN64 finish>=RN64(B+d)=B+d for these exact dyadic floors. Actual engine source uses finish=now+realized and predecessor/data-readiness guard; nonnegative communication cannot advance a start. Hence ANY valid schedule of ANY such H service has:

    start(n08) >=33/4=8.25ms >29/4 >=t_2.

This is an ABSOLUTE floor from time0,so it applies simultaneously to H^(0),H^(1),H^(2),without subtracting arrivals or assuming particular resource allocations. It avoids rounding accumulation or epsilon assumptions. The one-ms separation is a proof margin,not a new threshold.

At the first scheduler view after the full t_2 completion/arrival batch:

1. H^(0),H^(1),H^(2) have all arrived. Each retains its not-started n08 by the strict bound. Deadline misses do not drop admitted work under full-drain semantics.
2. Newly arrived H^(2),L^(2) each have two no-predecessor roots n01,n05. Before their first dispatch call these four roots are not started and dependency-ready. Thus E0's ready predicate holds,regardless of whether earlier services add more ready nodes.
3. The pending H population is at least3. Retained FULL requires the ENTIRE candidate population fit<=2. B1 only changed ready lower bound,so this state cannot enter F_B1 even if ready count is exactly4,all estimates unexpired and every other predicate ideal.

Required recording: engine drains all completions/arrivals before observe/controller; queue minimum participates in next_time,so it cannot skip this arrival. Snapshot#/exact_event_rule records each actual invocation,including NONE. No synthetic polling or between-batch observation is introduced.

Required retention: the new H^(2)/L^(2) identities and full DAGs appear in this public body and were absent earlier. Original equivalence includes arrived services/status/now; a real arrival changes the canonical state. Duplicate calls with the same body can count once,but cannot remove the one unique bad member. Cross-trial/replay pooling cannot eliminate it under the declared primary-stream scope.

Therefore every valid primary B2 stream in either registered A/B of this REQUIRED selected condition has E0\F_B1 nonempty. If F_B1=0,the negative precondition fails. If F_B1>0,the finite count gives F_B1<E0 and F_B1/E0<1. All12condition×10seed negative requires1 everywhere,so the global NOT_SUPPORTED branch remains unreachable. This proof is uniform over all admitted generation factors/registered seeds without evaluating them and does not depend on B2 tie/mapping choices.

## Failure-closure and quantifier limits

If either no valid selected A/B exists,required run/stream/M2 is invalid/incomplete or another prerequisite fails,the stage is blocked earlier; that is not a valid negative stream. Omitting the forced state,discarding a seed,renaming a condition or treating overflow H as absent violates the unchanged contract. An implementation that fails to export it has incomplete evidence,not a rescued coverage-one negative.

Mandatory root-cause count is1: pending-H cap2. Other possible barriers are reviewed below and are not double-counted. We have not established full-coverage existence/impossibility separately for every other individual condition. That is unnecessary to refute the universal all-condition branch. No specification gap blocks this particular global proof. Current mapping classification remains NOT_EVALUATED; no frequency,gain,CI or actual coverage has been calculated. The proof does not establish impossibility of support coverage4/5.

## Residual obstacle classification

See residual_blockers.csv for exact source identities and per-item derivations. One-ready is removed by B1. >4ready remains a possible disqualifier but no independent universal proof is asserted here. >2pending H is the mandatory witness above.36nodes is a derived bound K<=4 plus2×16,not another independent forced gap; selecting2 of3 never authorizes silently dropping the third. Running expiry remains possible from duration factors but no actual fixed-seed occurrence or mandatory exposure has been inspected/proved. Fixed suffix is a limitation of interpretation inside FULL,not a FULL disqualifier. Missing/illegal public data is INVALID/INCOMPLETE,not legal partial. No ready or no pending H is genuinely out-of-scope but does not describe the forced view. Six-unit running bound,positive estimates,baseline membership in its L cap and finite complete projection are not new independent universal obstacles.

The inherited fixed-suffix hand counterexample continues to limit all tested-space negatives. It is referenced only; this task computes no gain. No obstacle is called mandatory merely because an example is imaginable,and no local FULL state is presented as proof of a complete all-condition state sequence.

## Consequences for A/B1/B2 decision

B1 removes the original single-ready ADAS obstruction but DOES NOT restore global full-population negative reachability with all remaining caps unchanged. It could still yield other registered outcomes; scientific support,coverage prevalence and cost remain NOT_EVALUATED. The user may accept the restricted information/stopping boundary or separately request a new fully specified proposal. This task does not recommend new cap/denominator/threshold values.

A retains its already-known negative limitation. B2 explicitly conditions on a smaller structural domain and changes inference scope; this proof neither approves B2 nor establishes its empirical prevalence or conditional classification. No route is selected. All10D/40SP stay UNAPPROVED,F02 unselected,timing NOT_FROZEN,P2 BLOCKED. No implementation or science authorization follows this report.

## Actual checks and limitations

proof_checks.py.txt checks35 static premises/hand algebra/immutability observations (exit0). It parses existing finite tables and source TEXT,does not import any soc module,construct a workload,simulate events,generate a schedule,run an oracle/validator,draw a seed or compute coverage/gain/CI/bootstrap. It does not prove runtime correctness. A read-only preliminary source projection used the wrong matrix field scene; actual schema uses scenario. Original tool failure exit1 and its recorded reproduction B1-043 are retained in raw_commands; B1-044 correctly reads schema and verifies proof inputs. This reviewer error is not a simulator/design failure. New report structure/reference/manifest checks and publication are separately receipted.

## Source identity table

The following entries provide actual SHA256,Git blob,bytes and locator scopes for every source cited above/CSV. All at the verified starting commit; line ranges are supplementary to exact JSON pointers and named code sections.

|ID|Actual source path|Bytes|SHA256|Git blob|Locators|
|---|---|---:|---|---|---|
|S01|AGENTS.md|4586|5435e5e690a64e0e7f432bae22b8f459f646e12233d99a7a4b1a70266d8c9a22|21fd2c268b3eb14ca1bc6a984b2a1f4afc79f6cf|Full file identity/context/history check; claim-specific pointers in this report|
|S02|STATUS.md|2207|5f4c9fc321d22010400f260e8ed82a714b4a19453ae7b3102e04db93211f5222|1f525196022bbfc07c49a360f8f502ed5df3fd62|Full file identity/context/history check; claim-specific pointers in this report|
|S03|docs/user_request.txt|57544|4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461|879103b030d00025a4c938f2c3567d99f46a38f2|§43–44,lines1431–1494|
|S04|docs/model_spec.md|4381|3f74116fa6cb85e4f2db1c96d246ac830a282be28847a0af21184fde2e17197b|9f6396211e91dee615ecd5092dfe4ec5900e33d2|lines3–17 (nonnegative arrival,positive durations,resources); lines18–45 (precedence,nonpreemption,D1,full drain)|
|S05|docs/baseline_spec.md|2826|54a1cdb86d0235671a7d1ece31e489289c026bf083f33388580b6f3fdbb42e12|586b39b38cea03b718f4d59b576d70dc192f2a2f|Full file identity/context/history check; claim-specific pointers in this report|
|S06|docs/metric_spec.md|3242|c4b912fc672979ddc763d882e546b7a92bf53090e5b5dddd5777e2e867df182a|42a79f2c97bc4354e73377d71b6206b506f97b66|Full file identity/context/history check; claim-specific pointers in this report|
|S07|docs/statistical_protocol.md|3081|f9c0eeb6e76f68330ba3e5d8d90e58d175c3947a1948bb41b26ad50dbc041e8a|68b8cd775433e4d6c45d0ae4fca49fd0ddd58564|Full file identity/context/history check; claim-specific pointers in this report|
|S08|docs/workload_spec.md|1574|a098008f3abe47f4cfb830685009b19bf4d3555a8e370ad242a2fce1debea606|2438da0c809b3c6fb62caf0f5d097f666ce26043|Full file identity/context/history check; claim-specific pointers in this report|
|S09|docs/P1_implementation_spec.md|7473|92e9c4d0472f7893f54fc54d302d38bd224092285d78cc85ec7cdb67fef4e972|170dcbc8d361de40099e18e2edaf1771f3ae4b2a|lines20–26,D1–D5 event/mapping semantics|
|S10|docs/P2_design/P2_mapping_opportunity_decision_table_v1.md|4533|4c981f2f2303e1b1535168dd320e3c11151ea86ad35a502513893370a5906ea2|3bb69c483e007ff99137745c84ad753ccfa8aaaa|whole historical v1 table; not the effective B1 criterion|
|S11|docs/P2_design/v3/P2_diagnostic_spec_v3.json|18739|3fe77e0300cd86122aeebe8230cd1221b881498b54fe73f18a8db139830280dd|859bcceec7727b6fff21e3488c90821d23fe0db9|#/route_options/B1_EXPAND_SINGLE_READY; #/inherited_v2_contract/scope; #/inherited_v2_contract/coverage; #/inherited_v2_contract/limits; #/inherited_v2_contract/stage_denominators|
|S12|docs/P2_design/v3/P2_criterion_spec_v3.json|11661|ba41ec2a576158c701ca96db9f5100d4e7e6a30346708b5490ad56076984b165|8914d0623f96bca8ba4606448c4aa708b5de6ebd|#/route_options/B1_EXPAND_SINGLE_READY/negative_coverage; #/preconditions; #/bundles; #/coverage_thresholds|
|S13|docs/P2_design/v3/P2_public_snapshot_spec_v3.json|5274|4799c0663827b94d56c4dcd0da02a55c0f91dfdf967efe02ace40af40b6e85fd|d71fb07e25c479fbd9b89bea8a9fb4cd89d48d71|#/exact_event_rule; #/counting; #/included_fields; #/dedup_scope; #/missing|
|S14|docs/P2_design/v3/P2_stage_state_contract_v3.json|12256|032ec0f46018a4004a7d19b55850adf4ae4e2d116ff24d66e029452ebf4f33d7|6f3eb7695ee41daac7f00471f83fc647d1e17558|#/load_classification/selection; #/progression_conjunction; #/current_design_values|
|S15|docs/P2_design/v3/P2_typed_identity_schema_v3.json|130652|e8d6bc9b270f0f3ca07626012ef224d9b2fdd30ada4afba8a7f0f57dea916fcd|e6f70fd8e43688e8f55c0784d460e80f19e4ea83|#/$defs/PUBLIC_SNAPSHOT; #/$defs/PUBLIC_SERVICE; #/$defs/PUBLIC_NODE|
|S16|docs/P2_design/v3/P2_scientific_parameter_registry_v3.json|59359|9181c26d149bf640b9e43a6090f92f8b27808382414fd86842370631aec38c77|c56957b507f3bf70345d6d54af1e859451c25b10|#/parameters (all40 approval=UNAPPROVED);SP25/SP33/SP36/SP37|
|S17|docs/P2_design/v3/P2_generation_spec_v3.json|13930|dd8d9917d32b28376d35e376206bbce2776bf7c42ba50bb7b62de18b37ef26bb|9dfd1721b36fe73b287746152151d4f77ffcbd55|#/algorithm; #/arrivals; #/key_bindings; #/service_identity|
|S18|docs/P2_design/v3/inherited_v2_documents.json|1986|2b3f0224b5a458322642d3cc335bbf304fa07e9e6a94753460971a6966d76545|e55169e15a9210a2172bcb81e412543f2e608a91|Full file identity/context/history check; claim-specific pointers in this report|
|S19|docs/P2_design/v3/reference_bindings.json|5290|c58ab069c1204530317cc4dc2088996e8f86e2058654cdf2a4b8e76e526892c2|431d31f172dc86e037d929c8616e5cae28df9bd8|Full file identity/context/history check; claim-specific pointers in this report|
|S20|docs/P2_design/v2/P2_workload_templates_v2.json|28557|f282955ab09d0110f50447269b18d0389231bed9711532853d6cdbda92d9027c|5ce74d5e97645066c9a03e80c42a61060eb1c2e8|#/templates/0 (COCKPIT-8-v1),nodes n01,n02,n03,n06,n07,n08|
|S21|docs/P2_design/v2/P2_resource_profiles_v2.json|8858|9eea5cfd43ce50d796a00d7cac86f9a7ca8798da4a3ea0c2fd9e598d965f13ae|ecf51d4abf3c55f6acb555b235829f553161b404|#/profiles/0(audio); #/profiles/1(speech); #/profiles/2(intent); #/profiles/5(route); #/profiles/6(compose)|
|S22|docs/P2_design/v2/P2_generation_spec_v2.json|13039|33e3ccf437510986ffa401eea1ef48e995a1ad08df38a834374d4a1c483a91f2|8e0a2c0b527f128415ccc3fa909542c7a13f737a|Full file identity/context/history check; claim-specific pointers in this report|
|S23|docs/P2_design/v2/P2_trial_matrix_draft_v2.json|1327918|b58fe4c2eead01fc9b92966d557ed0bb052e7387794fc0d9b58029ffdb90af0e|f4c59610b363de1cd79305cd9c5eb9b3de83fda7|#/configs/8 and #/configs/9 (scenario field,P12/P10); #/rules/SEL-v2|
|S24|reports/P2_design/design_revision_v3/F01_observation_domain_options.md|10024|c57b37671e2f650eae3c3dfe7224338259c0770ff1a1a71552499b71ca328d9f|bb7ca79e24101d0996bd2aca91dea2cde714a75b|sections Reproduced source contradiction,Route B1,Common classification rules|
|S25|reports/P2_design/design_revision_v3/evidence_index.json|7720|d0fcf77e795abd270d662c91ae2974aea3c91f265514327dd7ad9cd85401f61b|67aa0d9b6ca9c0f1afc51636808d9ce3faae4495|Full file identity/context/history check; claim-specific pointers in this report|
|S26|reports/P2_design/design_revision_v3/source_evidence_manifest.json|39112|e0a3bd55a0b13c90b5daa977dd9e94a80f21cafb9390436bd81c799675a1c3d8|b135a59967922d307f3a1c8a91cfdd2ecb81196d|Full file identity/context/history check; claim-specific pointers in this report|
|S27|reports/P2_design/design_revision_v3/static_checks.json|8609|b1c869686663dc21b3b9313d33b3426edc4af65e5afcb0305d04f751d4652056|66c0992ee3d7f7d28984f2a2a810aa56535bcb68|Full file identity/context/history check; claim-specific pointers in this report|
|S28|reports/P2_design/design_revision_v3/artifact_manifest.json|40389|641f24705778e83fc3be5a3b4bec1f9b107f20117435c034aa87c5b0d1bb7a5d|75d518c3c2b941e957517acb47e713ccdfdef1b6|Full file identity/context/history check; claim-specific pointers in this report|
|S29|reports/P2_design/design_revision_v3/final_state.json|3522|197648992232c3820cd8790d4958ea279dc52555364f8776d35acbdd7cfeafe5|f41f2dafd1e3d665b6af748428bbd2bba5f02c2c|Full file identity/context/history check; claim-specific pointers in this report|
|S30|src/soc/simulator/engine.py|5398|977d01f3603f516e68e922542322976b813c01aad8d2dd177a5c0ac314399551|82bb89d6d437add1a88e2f34624b28ecfee8b209|lines36–51(batch/view/call); lines57–74(precedence/start/finish); lines78–101(earliest event/data wakeup)|
|S31|src/soc/model/observation.py|3661|40554e4ba71989223b7ba8362b7d35ae7257db030fd3e1fa04e262fb5002d0cb|ee90a63e26396ad75a8a5b77829c1d51382cdaeb|lines49–58(arrived services/full public graph); lines88–92(dependency-ready)|
|S32|src/soc/model/schema.py|7869|49d4cd0679bc8727ef723c146a62559d482aefd76d5aff8e931da4128a2b5bb6|4e5c4395504dfcf71d21ed090dc01f4719a5aa8e|Full file identity/context/history check; claim-specific pointers in this report|
|S33|src/soc/scheduler/kernels.py|8415|122264d53f840f2f680150ec1fa0af62710114f4cf51be422f77b07268bb86cb|fec74c5ba92a1a91056b26320a6364de4fa7091e|ordered_ready and choose (static read only)|

STOP=true. Final Git/remote/worktree resolved from actual publication receipts,not invented as a self-referential commit hash.

Final report verification B1-046:23 checks PASS,exit0;source/CSV pointer identities and all868 protected files checked. Proof35 and delivery23 are static observations,not runtime/science tests.

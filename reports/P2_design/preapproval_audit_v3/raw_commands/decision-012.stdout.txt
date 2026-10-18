# Human decision packet — P2 design revision v2

All approvals remain **UNAPPROVED**. This is a new proposed revision, not the active approved contract. v1 and the independent audit remain byte-exact. No science/implementation authorized.

40 named scientific parameter/rule groups remain unresolved: originalSP01–SP32 traced; eight split-out groupsSP33–SP40 added; none deleted/merged. Identity/lock API engineering details are reviewed underD09/D10, not counted as extra scientific scalar parameters.

## D01

Original question: 选择显式角色 DAG 还是确定性 grammar，并提供三场景的完整8/16节点拓扑、角色/H-L归属及尺寸规则。

Exact v2 proposed values/rules: Exact v1 six templates/IDs/roles/predecessors/group inheritance retained; counts COCKPIT8/9,16/17; ADAS8/9,16/17; FUSION8/7,16/15; explicit two-half expansion/internal1/16MiB.

Scientific groups: SP01,SP02,SP03. Findings: No physical-value revision; original acceptance not approval.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_workload_templates_v2.json` / v2 / SHA256 `f282955ab09d0110f50447269b18d0389231bed9711532853d6cdbda92d9027c`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准完整六模板及v1保持的尺寸/角色/H-L规则？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D02

Original question: 选择有来源的profile表或批准的合成规则，提供兼容集合、各资源估计/实际代价及全部参数/来源。

Exact v2 proposed values/rules: Exact16x6 compatibility/cost table and CPU symmetry retained; null incompatible; base*scale*uniform[.9,1.1) estimate, separate resource factor same range for actual.

Scientific groups: SP04,SP05,SP06. Findings: No physical-value revision; original acceptance not approval.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_resource_profiles_v2.json` / v2 / SHA256 `9eea5cfd43ce50d796a00d7cac86f9a7ca8798da4a3ea0c2fd9e598d965f13ae`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准原合成96单元格/兼容/CPU对称/扰动分布，并接受非硬件数据的限制？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D03

Original question: 提供边MiB与type-pair latency/bandwidth的完整表或有来源规则，保留既有通信语义。

Exact v2 proposed values/rules: Exact74 edge sizes and9 latency/bandwidth pairs retained; same-unit0 elseL+b/B; unitsms/MiB/MiB-ms; no bus contention or physical value changes.

Scientific groups: SP07,SP08,SP09. Findings: No physical-value revision; original acceptance not approval.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_communication_profiles_v2.json` / v2 / SHA256 `74f7dde644b11d0b459fb68e9f250d9799e34f09652609b63122e0de5bf6e3b8`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准原74条边及9对通信参数和既有物理语义？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D04

Original question: 确定keyed扰动/PRNG/版本、到达/突发、H-L组成、deadline、服务数或窗口及停止边界的完整定义/值。

Exact v2 proposed values/rules: Typed version2+generator_v2+domain_v2; three exact KEY fills, original10 seeds; U=q/2^64; same100-service/50slot/H2.5-L4 deadlines; parent100 exactG; bit-preserving controls; separate semantic/raw/runtime hashes and21 preimages.

Scientific groups: SP10,SP11,SP12,SP13,SP14,SP15,SP16,SP17. Findings: V2-F02,V2-F03,V2-F07.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_generation_spec_v2.json` / v2 / SHA256 `33e3ccf437510986ffa401eea1ef48e995a1ad08df38a834374d4a1c483a91f2`.
- `docs/P2_design/v2/P2_typed_identity_schema_v2.json` / v2 / SHA256 `9b478cf7e96776f6cc69f29426715efed6eec2309270be1efb3dd77985ebfbc9`.
- `docs/P2_design/v2/P2_canonical_golden_vectors_v2.json` / v2 / SHA256 `c74cd5a06f0683e28857d07fee2791bbe6c3cf384bbe863f63bcaa6e176b3160`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准v2逐字段key、编码/preimage、精确转换和parent100控制G定义？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D05

Original question: 确定枚举或有限轴展开，提供所有值/方法子集及理由/顺序/预算/seed到trial-condition-workload的精确映射。

Exact v2 proposed values/rules: 36 configs,10 seeds,2520 rows=1800MAIN+360H-only+360LOW,1080inputs,5040 maxengine withreplay,0retry/timing; sameA/B periods80/64,24/20,12/10; MAIN generation first, control execution first.

Scientific groups: SP18,SP19,SP20. Findings: V2-F02.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_trial_matrix_draft_v2.json` / v2 / SHA256 `b58fe4c2eead01fc9b92966d557ed0bb052e7387794fc0d9b58029ffdb90af0e`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准不变的完整矩阵/预算及物化MAIN先于controls、执行顺序保持的区分？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D06

Original question: 确定H可行性对照、压力/负载分类、配置选择/平局以及不达标、不可行、无效、失败、不完整的处置规则。

Exact v2 proposed values/rules: Original target bands[0,.5),[.5,.8),[.8,1], lightH/L<=.01,loadedH[.01,.8] retained; typed validity/control/target/A-before-B total order; absolute RN64 lowerbound with strict>deadline, noepsilon, control witness only.

Scientific groups: SP21,SP22,SP23,SP24,SP38,SP40. Findings: V2-F06,V2-F07.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_stage_state_contract_v2.json` / v2 / SHA256 `c64803a93c74ee9dba6a7bc61de2d2e550264f2c5d4a920e1248665fa7e86b93`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准总分类、控制见证范围、绝对RN64下界和不变的A-before-B资格规则？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D07

Original question: 选择M1机制诊断、M2基线描述或组合，确定观察量、反事实控制/视窗、信息边界和每seed/condition汇总。

Exact v2 proposed values/rules: M1R_PATH_V2: original2-4 ready enumeration; target<=2 pending arrivedH DAGs<=16nodes each; fixed public suffix EFT,<=36nodes/1296maps; L cap=max(baseline finish,deadline); exact snapshot scope/dedup/replay exclusion; no actual scheduler feedback.

Scientific groups: SP25,SP26,SP27,SP33,SP34,SP35,SP37. Findings: V2-F01,V2-F04.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_diagnostic_spec_v2.json` / v2 / SHA256 `9bec37d044f4c7742d931149c195c2c3ec1540d41dc3f0a899a2b29f8c7e3e90`.
- `docs/P2_design/v2/P2_public_snapshot_spec_v2.json` / v2 / SHA256 `fa4ce177c2d4a49a5f8f5b30bfa44e2b0d529f1e735ddfa259ae1811edc2f1af`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准M1R的目标选择、固定suffix、局部L slack、边界/截断/去重和记录范围？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D08

Original question: 确定跨seed/条件聚合、稳定性、不确定性和三向结论的全部条件/参数及缺失无效处置，保持既有CI方法。

Exact v2 proposed values/rules: FINE(.01,.01) vs COARSE(.05,.05),8/10 support and<=2/10 absence remain undecided; M1R hits/F,F/E; proposed positive coverage>=4/5,negative=1,all12conditions/10seeds; samepaired10000,type7,20261018; selected calibration descriptive only.

Scientific groups: SP28,SP29,SP30,SP31,SP32,SP36,SP39. Findings: V2-F01,V2-F04,V2-F05,V2-F06.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_criterion_spec_v2.json` / v2 / SHA256 `98a578944e7910db933f5b3b02aee4bb03de8005853024b38cc3b02630b04e38`.
- `docs/P2_design/v2/P2_mapping_opportunity_decision_table_v2.md` / v2 / SHA256 `594863a579ac32fdd980454fe6e0f0d24d165729a60f1c6f6526c8688fd296f4`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 选择FINE还是COARSE（或提出明确替代）？是否批准4/5正覆盖、1阴性覆盖、三态及条件性解释？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D09

Original question: 选择runner架构，裁决完成产物精确复用、失败/不完整默认停止、重试登记和P2源码dirty控制。

Exact v2 proposed values/rules: RecommendR1 formalrunner vsR2thinlauncher; blueprint/auth/inputlock/generate/resolve/workload/run/attempt/runlock/preinvoke withoutcycle; exactreuse,0automaticretry,append-only recovery; P2clean policy newunapproved; explicit stages/exits, timingNOT_FROZEN blocks.

Scientific groups: . Findings: V2-F02,V2-F03,V2-F05.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_runner_schema_review_v2.md` / v2 / SHA256 `fd1a59638bf1754af0a6423b57873a6691af8c3559a1c1d62ceeeffda2da5099`.
- `docs/P2_design/v2/P2_stage_state_contract_v2.json` / v2 / SHA256 `c64803a93c74ee9dba6a7bc61de2d2e550264f2c5d4a920e1248665fa7e86b93`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准R1、精确复用、零自动retry、恢复表、新增P2洁净和分离状态/出口契约？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## D10

Original question: 选择可验证的科学envelope或新schema+adapter，批准namespace、规范化、ID、provenance、引用与旧P1兼容验证范围。

Exact v2 proposed values/rules: RecommendS2typedscientificfamily+adapter vsS1envelope;21exactpreimages and closed typed records, worker argv templates currentlyunimplemented, main/control counts+singleN/A token, immutablebirthrefs, fullCOMPLETEconjunction; oldP1identity preserved and future regression required.

Scientific groups: . Findings: V2-F02,V2-F03,V2-F04,V2-F05,V2-F07.

Affected artifacts/version/hash:

- `docs/P2_design/v2/P2_typed_identity_schema_v2.json` / v2 / SHA256 `9b478cf7e96776f6cc69f29426715efed6eec2309270be1efb3dd77985ebfbc9`.
- `docs/P2_design/v2/P2_runner_schema_review_v2.md` / v2 / SHA256 `fd1a59638bf1754af0a6423b57873a6691af8c3559a1c1d62ceeeffda2da5099`.

Remaining limitations: All values synthetic/proposed, no implementation or scientific validity verified. Coverage/truncation, fixed suffix, local L cap and same-calibration selection limit interpretation; timingNOT_FROZEN blocks progression.

Precise question: 是否批准S2、typed科学家族及身份/argv/COMPLETE规范和未来血缘/P1回归范围？

Approval: **UNAPPROVED**

Selected option=null; approved values=null; reviewer=null; timestamp=null; approval evidence=null.

## Exact retained value references and additions

D01–D03 objects are identical to their v1 scientific content; all nodes/predecessors/96 profile cells/74 edges/9 links are explicit in the cited hashed JSONs. They are not literature or hardware measurements.

| Group | Name | v1 lineage | v2 rule/value | approval |
|---|---|---|---|---|
| SP01 | six_topologies | SP01 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP02 | importance_assignment | SP02 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP03 | size_expansion | SP03 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP04 | role_compatibility | SP04 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP05 | role_execution_costs | SP05 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP06 | cpu_symmetry | SP06 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP07 | edge_sizes | SP07 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP08 | link_latencies | SP08 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP09 | link_bandwidths | SP09 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP10 | key_encoding_hash_mapping | SP10 | Explicit schema_version2 + generator_version v2; all3 fields retain scenario/condition/config, only prescribed fields empty; exact typed KEY. | UNAPPROVED |
| SP11 | estimate_distribution | SP11 | Same distribution; explicit v2 field keys change future draw identity, no realization compared. | UNAPPROVED |
| SP12 | realized_distribution | SP12 | Same distribution/private boundary; exact v2 key and conversion. | UNAPPROVED |
| SP13 | arrival_jitter | SP13 | Same U/10; scenario/condition/config retained, H/L/node/resource/edge empty exactly. | UNAPPROVED |
| SP14 | arrival_burst | SP14 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP15 | service_count_and_group_mix | SP15 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP16 | deadline_multipliers | SP16 | Same multipliers, explicit pre-round E_exact reference and final binary64 absolute deadline. | UNAPPROVED |
| SP17 | arrival_window | SP17 | W unchanged; distinct arrival_end/lastarrival/lastfinish/makespan/observation_end; full-drain metric preserved. | UNAPPROVED |
| SP18 | period_axis | SP18 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP19 | main_method_set | SP19 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP20 | finite_order_budget | SP20 | Budget/order unchanged; proposal-v2 and wlref:v2 refs, MAIN materialization before controls but engine order unchanged. | UNAPPROVED |
| SP21 | control_input_transform | SP21 | G always ALL100 parent MAIN services and exact pre-round sidecar; no new draw; distinct control witness/overlap qualification. | UNAPPROVED |
| SP22 | load_pressure_bands | SP22 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP23 | load_miss_bands | SP23 | Exact same semantic proposed value; versioned document namespace only. | UNAPPROVED |
| SP24 | configuration_selection | SP24 | Same deterministic policy; validity/control/OWN target bin explicit; all off-target/unselected preserved. | UNAPPROVED |
| SP25 | M1_snapshot_subset | SP25 | M1R: K2..4 (single-ready states explicitly coverage-insufficient) and pending arrived H targets; target scope/dedup separately registered SP33/SP37. | UNAPPROVED |
| SP26 | M1_counterfactual_objective | SP26 | Mean projected completion of selected remaining-H DAGs; fixed suffix and new L slack separately SP34/SP35. | UNAPPROVED |
| SP27 | M2_measurements | SP27 | Same contrasts/noncausal interpretation; M1R onlyB2 diagnostic references; historical M1 not gate. | UNAPPROVED |
| SP28 | material_gain_cutoff | SP28 | Same candidate tau values, applied only to FULL M1R remaining-H projected gain; no selection made. | UNAPPROVED |
| SP29 | frequency_cutoff | SP29 | Same candidate frequency values; hits/F over FULL covered unique states, coverage separately F/E. | UNAPPROVED |
| SP30 | stability_requirement | SP30 | Same numeric stability on new per-seed FULL-coverage frequency, no new independent unit. | UNAPPROVED |
| SP31 | condition_aggregation | SP31 | Same condition/macro units; coverage and selected-calibration interpretation separately SP36/SP39. | UNAPPROVED |
| SP32 | bootstrap_implementation_pin | SP32 | Same algorithm/constants; exact five-field ANALYSIS_INDEX_KEY; no bootstrap indices generated. | UNAPPROVED |
| SP33 | target_H_selection | SP25 | First2 unfinished arrived H with pending nodes by deadline/service ID; truncation is coverage insufficiency. | UNAPPROVED |
| SP34 | bounded_public_suffix_rollout | SP26 | All public remaining nodes of<=2 targetH DAGs,<=16 each; fixed Kahn+B2/EFT suffix, <=36 projected nodes, <=1296 action mappings; no candidate/policy feedback. | UNAPPROVED |
| SP35 | local_L_slack_admissibility | SP26 | L action node finish <=max(baseline L finish, service deadline); no globalL budget implication, no1.10 borrowing. | UNAPPROVED |
| SP36 | coverage_and_missing_evidence | SP31 | Propose support coverage>=4/5 per seed/condition; negative requires1; E/F>0, partial neverzero, invalid/missing fail closed. | UNAPPROVED |
| SP37 | state_equivalence_denominator | SP25 | Canonical public binary64-bit snapshot; per primary MAIN-B2 attempt scope; exclude seq/wall/private data; replay excluded. | UNAPPROVED |
| SP38 | absolute_conservative_feasibility_arithmetic | SP21 | Absolute RN64 monotone lower bound, actual compatible mincost/delay offline; strict B_abs>d_abs only, equality not certified, no epsilon. | UNAPPROVED |
| SP39 | selected_calibration_interpretation | SP31 | Selected calibration pointwise intervals conditional/descriptive; not independent confirmation. This is an explicit logical limitation, not changed CI methodology. | UNAPPROVED |
| SP40 | control_NA_and_window_semantics | SP21 | MAIN100/50H50L; H-only50H; LOW100; one NOT_APPLICABLE_CONTROL enum; makespan remains lastfinish, observation_end separate. | UNAPPROVED |

New assumptions SP33–SP40 must be explicitly accepted or revised; no observed data supports choosing them. Computational checks do not confer human approval.
Single next safe action after static review: human review the concrete v2 choices and record decisions; do not implement or runP2.

# P2 v2 human decision packet after adversarial review

Current review: **DESIGN_REVIEW_REVISE_REQUIRED**. Audited source HEAD `a3680acf45c5578fc090cf53cc186f28a8e9b88a`. 同一助手环境内重新审查，不是第三方审计。

本表仅请求裁决；所有批准栏为 UNAPPROVED。不要以整包 ACCEPT 取代逐项值、版本、证据和依赖的确认。当前 5 项可裁决、5 项应先修订，仍有 10 个未获批准的决定。

## 优先明确的修订方向（均未批准）

1. D07/D08：联合重新提出观察域与阴性证据政策。可要求在原研究命题下提出可达的阴性标准；或明确把观察不足固定为 INCONCLUSIVE 并说明何种研究停机政策可被人工接受；或拒绝该 observer、要求新诊断提案。每条路线均须完整定义和再审查，不能静默删单 ready 状态、改变 E 或自选新阈值。

2. D09/D10：选择明确的共同排他域及授权替换政策。可选择每个 descriptor/run 唯一有效授权、禁止接管；或提交完整 owner/lease/fencing/CAS 契约。精确字段和失主写入/启动禁令必须可验证；不批准自动重试。

3. D10：为实际执行 HEAD 与实测 dirty 指定必需 typed 收据或运行记录字段，并绑定 COMPLETE；保留冻结源码身份与实测 checkout 的区别。

4. D07–D10：要求精确列出 M2 配对 roster/contrast/report、来源与缺失失败规则，绑定 criterion 和 stage；通用引用存在不足以证明必需报告存在。

5. D04/D10：确认现有 closed KEY 的 14 字段，只更正 All15 文案，不新增字段。

以上是 UNAPPROVED 的修订选项，不是在本轮修改提案。完整来源及影响见 `cross_document_findings.json` 的 V3-F01–F05。固定 suffix 限制、未有唯一数值依据和 timing 待冻结还需明确接受或暂缓；不应因为静态矩阵通过而隐含接受。

## 十项原始决策与精确问题

### D01 — READY_FOR_HUMAN_DECISION

原始问题：选择显式角色 DAG 还是确定性 grammar，并提供三场景的完整8/16节点拓扑、角色/H-L归属及尺寸规则。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D01：是否选择并批准所引 SHA-256 的六个显式模板、整体 H/L 继承及二分尺寸规则，并接受 16 节点同时改变通信/流水级的解释限制？若拒绝，请选择另拟完整 grammar 或修订显式模板。

可行选项：Approve exact explicit synthetic model; request revised explicit model; defer for complete sourced grammar. No option approved.

已知事实：Three scenes and exact 8/16 executable-node counts are registered. H/L are service importance; graph must be acyclic with stable node identities.

推导：Six scene/size templates; subdivision adds eight real nodes and eight internal edges. It preserves nominal base compute, not pure size scaling: communication and pipeline depth change.

新增科学假设：Exact six synthetic DAGs, role topology, whole-service H/L inheritance, two equal-cost half-nodes and 1/16 MiB internal edges.

工程约定：Explicit template representation with stable IDs and mechanical DAG/role/edge validation.

缺少的证据：No measured vehicle graph distribution or external representativeness evidence; no generator validation. Those limits are disclosed, not fabricated.

公平性、复现、成本与统计影响：Topology can favor accelerator bottlenecks; shared exact inputs support comparison fairness but cannot confer real-world generality.

阻断与依赖：D02/D03 role and edge bindings; D04 generation; P2-B1. No implementation/execution follows approval automatically. D02,D03,D04

对应参数组：SP01,SP02,SP03

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D01；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 28；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 7；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_workload_templates_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `f282955ab09d0110f50447269b18d0389231bed9711532853d6cdbda92d9027c`。

- `docs/user_request.txt` — §§33–34, lines1159–1197；immutable source at audited revision；SHA-256 `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461`。

- `docs/workload_spec.md` — lines3–12；immutable source at audited revision；SHA-256 `a098008f3abe47f4cfb830685009b19bf4d3555a8e370ad242a2fce1debea606`。

- `docs/model_spec.md` — lines4–14；immutable source at audited revision；SHA-256 `3f74116fa6cb85e4f2db1c96d246ac830a282be28847a0af21184fde2e17197b`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D02 — READY_FOR_HUMAN_DECISION

原始问题：选择有来源的profile表或批准的合成规则，提供兼容集合、各资源估计/实际代价及全部参数/来源。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D02：是否批准所引 16×6 合成兼容/代价表、CPU 对称假设与对应扰动关系，并将结论限定于合成模型？或要求取得可追踪 profile 后另交完整提案？

可行选项：Approve exact synthetic table with scope limits; defer for sourced profile; request explicit alternate synthetic values before observations.

已知事实：Four CPU units, one GPU and one NPU; positive finite estimates/realizations on compatible units; several compatibility classes; private realized durations excluded from scheduler.

推导：16 roles ×6 resource cells=96; null incompatible is distinct from zero duration; symmetrical CPU rows avoid a synthetic per-core speed hierarchy.

新增科学假设：Exact synthetic compatibility table and speedups, identical CPUs, estimate and realized distributions; no source establishes these physical values.

工程约定：Explicit typed resource table; reject invalid/null executable entries; public/private separation.

缺少的证据：No authorized hardware profiling evidence or calibrated speedup ratios; no empirical disturbance model or implementation tests.

公平性、复现、成本与统计影响：Hard NPU/GPU compatibility and synthetic acceleration can create or suppress mapping opportunities; literal table reproducibility does not establish plausibility.

阻断与依赖：D04 estimates/realizations; D06 feasibility; D07 projected costs; P2-B1. D01,D04

对应参数组：SP04,SP05,SP06

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D02；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 36；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 8；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_resource_profiles_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `9eea5cfd43ce50d796a00d7cac86f9a7ca8798da4a3ea0c2fd9e598d965f13ae`。

- `docs/model_spec.md` — lines10–14,48–58；immutable source at audited revision；SHA-256 `3f74116fa6cb85e4f2db1c96d246ac830a282be28847a0af21184fde2e17197b`。

- `docs/workload_spec.md` — lines10–12；immutable source at audited revision；SHA-256 `a098008f3abe47f4cfb830685009b19bf4d3555a8e370ad242a2fce1debea606`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D03 — READY_FOR_HUMAN_DECISION

原始问题：提供边MiB与type-pair latency/bandwidth的完整表或有来源规则，保留既有通信语义。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D03：是否批准所引全部 74 边数据量及九类 link 参数作为合成值？既有同单元/跨单元及副本语义保持约束，不由此重新投票修改。

可行选项：Approve exact synthetic tables; request revised complete tables; defer for authorized measured profile.

已知事实：Same-unit transfer zero; other-unit latency+size/bandwidth, destination-specific readiness after predecessor completion; overlapping independent transfers without shared bus contention.

推导：74 template edges and nine ordered resource-type links; CPU0→CPU1 is other-unit even though same type.

新增科学假设：All edge sizes and nine latency/bandwidth values; fixed edge sizes and per-successor copies; no measured source for their numerical strengths.

工程约定：Full edge/link tables, explicit units and finite positive bandwidth checks.

缺少的证据：No hardware link/edge-data provenance; future remapping/communication regression evidence absent.

公平性、复现、成本与统计影响：Communication intensity influences offloading advantage; same shared tables ensure paired input comparability but do not establish hardware realism.

阻断与依赖：D04 materialization, D06 feasibility and D07 projection; P2-B1. D01,D02,D04

对应参数组：SP07,SP08,SP09

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D03；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 43；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 9；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_communication_profiles_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `74f7dde644b11d0b459fb68e9f250d9799e34f09652609b63122e0de5bf6e3b8`。

- `docs/model_spec.md` — lines3,20–31；immutable source at audited revision；SHA-256 `3f74116fa6cb85e4f2db1c96d246ac830a282be28847a0af21184fde2e17197b`。

- `docs/workload_spec.md` — lines10–12；immutable source at audited revision；SHA-256 `a098008f3abe47f4cfb830685009b19bf4d3555a8e370ad242a2fce1debea606`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D04 — DEPENDENT_REVISION_REQUIRED

原始问题：确定keyed扰动/PRNG/版本、到达/突发、H-L组成、deadline、服务数或窗口及停止边界的完整定义/值。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D04：是否先要求 D09/D10 的锁域与出生/执行血缘缺口得到文档修订，再审定本版完整 key、数值转换、到达/deadline/window/control 规则？对保留科学数值可逐项给出批准、拒绝或暂缓，不授权生成。

可行选项：Request targeted identity/provenance revision then decide complete rules; defer with precise required evidence; approve specified independent numeric subgroups only with explicit exclusions.

已知事实：Method-independent keyed disturbance, shared materialized input, registered seed identities, arrived-only visibility and complete drain are original constraints.

推导：50 slots ×H/L=100 services; original-parent bit copy prevents controls redrawing disturbances; content identity must follow materialization without circular dependence.

新增科学假设：SHA-to-U keyed synthetic law, all key bindings/version; uniform factor ranges; bursts/jitter/group mix; H2.5/L4 deadline multipliers; W50P; parent100 G-domain.

工程约定：Closed typed keys, exact Decimal/Rational then RN64, separated raw/semantic/runtime hashes; staged blueprint/descriptor/resolution identity.

缺少的证据：Fresh identity review identifies concurrency/lock-domain and missing actual-HEAD/dirty typed provenance issues; actual KEY/gloss/bindings have14 fields, unlike the historical15-field summary (ID-R03). Full implementation, source lineage and numerical reproducibility remain unverified; no actual inputs exist.

公平性、复现、成本与统计影响：Changed key domain changes future input identity even with unchanged distributions; generation determinism and approved authorization cannot be inferred from static parse.

阻断与依赖：P2-B1 generation and P2-B4/B5 provenance; D09/D10 unresolved dependencies prevent complete implementation readiness. D01,D02,D03,D09,D10

对应参数组：SP10,SP11,SP12,SP13,SP14,SP15,SP16,SP17

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D04；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 49；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 10；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_generation_spec_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `33e3ccf437510986ffa401eea1ef48e995a1ad08df38a834374d4a1c483a91f2`。

- `docs/P2_design/v2/P2_runner_schema_review_v2.md` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `fd1a59638bf1754af0a6423b57873a6691af8c3559a1c1d62ceeeffda2da5099`。

- `docs/P2_design/v2/P2_typed_identity_schema_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `9b478cf7e96776f6cc69f29426715efed6eec2309270be1efb3dd77985ebfbc9`。

- `docs/user_request.txt` — §§24–25, lines854–894; §36, lines1224–1260; §41, lines1386–1404；immutable source at audited revision；SHA-256 `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461`。

- `docs/model_spec.md` — lines4–8,39–58；immutable source at audited revision；SHA-256 `3f74116fa6cb85e4f2db1c96d246ac830a282be28847a0af21184fde2e17197b`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D05 — READY_FOR_HUMAN_DECISION

原始问题：确定枚举或有限轴展开，提供所有值/方法子集及理由/顺序/预算/seed到trial-condition-workload的精确映射。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D05：在完整逐行审查记录基础上，是否批准当前 36 配置/2520 trial/1080 输入/5040 调用上限、全部主基线、两种 B2 控制、固定顺序及零自动重试？明确 timing 排除只限本校准矩阵。

可行选项：Approve exact finite roster; request explicit replacement finite roster before observations; defer pending budget/implementation evidence.

已知事实：3×3×2 main conditions; 10 CALIBRATION seeds; baseline-only tuning with B2 focal; B1–B5 meanings are registered.

推导：18×2=36 configs;36×10×7=2520 slots;1800MAIN,360+360 controls;1080 inputs;5040 maximum primary/replay calls conditional on approved policy.

新增科学假设：Two periods per load, complete method set and two B2 controls, fixed execution order, one replay and zero automatic retries; runtime/timing budget zero.

工程约定：Explicit finite roster and symbolic references; separate MAIN-first materialization from control-first engine execution.

缺少的证据：No measured affordability/runtime budget evidence, nor selected feasible configs. Matrix row-level check is in trial_matrix_row_audit.json; actual commands/workload hashes correctly remain null.

公平性、复现、成本与统计影响：Fixed method order is not randomized timing design; product counts are conditional budget arithmetic, not evidence actual run cost is acceptable.

阻断与依赖：P2-B2; downstream calibration execution still depends on D04/D06/D07–D10 and separate authorization. D04,D06,D09,D10

对应参数组：SP18,SP19,SP20

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D05；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 84；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 11；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_trial_matrix_draft_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `b58fe4c2eead01fc9b92966d557ed0bb052e7387794fc0d9b58029ffdb90af0e`。

- `docs/user_request.txt` — §§36,38–42, lines1224–1430；immutable source at audited revision；SHA-256 `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461`。

- `docs/workload_spec.md` — lines14–25；immutable source at audited revision；SHA-256 `a098008f3abe47f4cfb830685009b19bf4d3555a8e370ad242a2fce1debea606`。

- `docs/baseline_spec.md` — lines14–20；immutable source at audited revision；SHA-256 `54a1cdb86d0235671a7d1ece31e489289c026bf083f33388580b6f3fdbb42e12`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D06 — READY_FOR_HUMAN_DECISION

原始问题：确定H可行性对照、压力/负载分类、配置选择/平局以及不达标、不可行、无效、失败、不完整的处置规则。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D06：是否批准控制专属见证、严格绝对 RN64 不可行证书、现有拟议 pressure/miss bands、全十 seed 资格及 A-before-B，并保留无法选满18条件即阻断的结果？

可行选项：Approve exact qualification policy within synthetic-model scope; revise explicit bands/control definitions before observations; defer for missing rationale.

已知事实：Check H basic feasibility in isolation/low competition before treating workload misses as scheduler failure; load labels use resource pressure; preserve negatives; candidate advantage excluded.

推导：RN64 monotonic lower-bound induction is sufficient only for strict bound>absolute deadline; bound≤deadline and B2 miss do not prove feasibility/universal infeasibility. A-before-B never selects by M1R/M2 effects.

新增科学假设：Two transformed controls; precise pressure and DMR bands; each-seed resource waiting; all10 control witnesses; A-priority selection over all10 seeds.

工程约定：Explicit total classification, no relabel/clamp/drop; absolute RN64 offline arithmetic; one N/A control token and separate windows.

缺少的证据：No actual feasibility/load qualification, runtime numeric-proof test or all18 selected conditions. Source does not establish proposed band values; implementation still subject to D09/D10 fixes.

公平性、复现、成本与统计影响：Same samples used for qualification and opportunity summaries limit inference; controls with altered arrival streams do not prove original MAIN schedulability.

阻断与依赖：P2-B1/B2; configuration selection and D08 preconditions. An approval cannot assert any config will qualify. D01,D02,D03,D04,D05

对应参数组：SP21,SP22,SP23,SP24,SP38,SP40

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D06；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 100；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 12；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_generation_spec_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `33e3ccf437510986ffa401eea1ef48e995a1ad08df38a834374d4a1c483a91f2`。

- `docs/P2_design/v2/P2_stage_state_contract_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `c64803a93c74ee9dba6a7bc61de2d2e550264f2c5d4a920e1248665fa7e86b93`。

- `docs/P2_design/v2/P2_trial_matrix_draft_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `b58fe4c2eead01fc9b92966d557ed0bb052e7387794fc0d9b58029ffdb90af0e`。

- `docs/user_request.txt` — §§35–37, lines1199–1275；immutable source at audited revision；SHA-256 `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461`。

- `docs/workload_spec.md` — lines14–20；immutable source at audited revision；SHA-256 `a098008f3abe47f4cfb830685009b19bf4d3555a8e370ad242a2fce1debea606`。

- `docs/metric_spec.md` — lines3–10；immutable source at audited revision；SHA-256 `c4b912fc672979ddc763d882e546b7a92bf53090e5b5dddd5777e2e867df182a`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D07 — REVISE_BEFORE_APPROVAL

原始问题：选择M1机制诊断、M2基线描述或组合，确定观察量、反事实控制/视窗、信息边界和每seed/condition汇总。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D07：是否要求先修订 M1R 观察域/覆盖与 D08 阴性判据的结构性不相容，并明确固定 suffix、局部 L slack 和 M2 证据范围，再决定是否采用该诊断？请勿仅批准“有界诊断”而省略这些选择。

可行选项：Request jointly consistent D07/D08 proposal; defer with precise mechanism coverage requirements; reject this observer without inventing a candidate algorithm.

已知事实：Original §44 permits 2–4 ready assignment diagnostic; §43 targets scarce-resource blocking of another arrived H path. Public-only observations and no online diagnostic performance claim are source constraints.

推导：At most6^4 assignments; fixed suffix restricts counterfactual space. FULL coverage is not global optimality, and action-node L cap is not full-service L-P95 guarantee.

新增科学假设：M1R target and K limits/order, fixed suffix, H mean projected finish, local L slack cap, all in-scope E versus FULL F, public-state dedup; M2 descriptive contrasts.

工程约定：Separate event/state identities and primary/replay streams; exact rational projections, complete error/partial distinction.

缺少的证据：Fresh M1R review demonstrates mandatory ADAS post-start single-ready state makes negative full coverage unreachable for the current registered matrix. Fixed-suffix and local-L scope require explicit scientific acceptance; M2 evidence binding incomplete.

公平性、复现、成本与统计影响：Narrow projected counterfactual can miss real alternatives; endogenous coverage excludes busy/truncated states; operational stop needs explicit limited interpretation.

阻断与依赖：P2-B3 and D08 classification; implementation/diagnostic execution cannot begin under the complete current contract. D01,D02,D03,D04,D06,D08,D10

对应参数组：SP25,SP26,SP27,SP33,SP34,SP35,SP37

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D07；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 126；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 13；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_diagnostic_spec_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `9bec37d044f4c7742d931149c195c2c3ec1540d41dc3f0a899a2b29f8c7e3e90`。

- `docs/P2_design/v2/P2_public_snapshot_spec_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `fa4ce177c2d4a49a5f8f5b30bfa44e2b0d529f1e735ddfa259ae1811edc2f1af`。

- `docs/P2_design/v2/P2_stage_state_contract_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `c64803a93c74ee9dba6a7bc61de2d2e550264f2c5d4a920e1248665fa7e86b93`。

- `docs/user_request.txt` — §32, lines1113–1157; §§43–44, lines1431–1494；immutable source at audited revision；SHA-256 `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461`。

- `docs/model_spec.md` — lines48–58；immutable source at audited revision；SHA-256 `3f74116fa6cb85e4f2db1c96d246ac830a282be28847a0af21184fde2e17197b`。

- `docs/P2_design/P2_complete_design_proposal_v1.md` — D07, lines232–279；immutable source at audited revision；SHA-256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D08 — REVISE_BEFORE_APPROVAL

原始问题：确定跨seed/条件聚合、稳定性、不确定性和三向结论的全部条件/参数及缺失无效处置，保持既有CI方法。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D08：是否先要求解决阴性分支不可达及 M2 完整性绑定，再事前选择 FINE、COARSE 或另一套完整阈值/覆盖规则？是否接受仅对选中校准配置和 FULL 状态作条件性描述，禁止将其写为独立确认结论？

可行选项：Request joint rule revision, then pre-observation bundle choice; defer; reject current criterion. No implicit default or outcome-based choice.

已知事实：Seed is paired resampling unit;10000 replicates,20261018,type7 remain prescribed; no new CI method/H-L threshold borrowing. Stable opportunity criterion must precede observation.

推导：Same-calibration selection and FULL-only rates are conditional descriptive; neither independence nor unconditional coverage follows. Support/negative predicates mutually exclusive but current negative branch is structurally unreachable for mandatory ADAS conditions.

新增科学假设：FINE/COARSE gain-frequency bundles,8/10 and≤2/10,all12 loaded conditions,4/5 positive coverage and1 negative coverage; no source fixes these numbers.

工程约定：Pinned rejection-sampled SHA index implementation, saved index digest; NOT_EVALUATED separate from attempted INCONCLUSIVE; exact boundary handling.

缺少的证据：Need D07/D08 reachability revision and explicit M2 completeness binding; numerical cutoff rationale remains normative rather than empirical. No outcomes may be used to pick a bundle.

公平性、复现、成本与统计影响：Threshold changes cannot remove structural unreachability;80% covered subset may be outcome-related;10 seeds and all12 pointwise rules do not establish simultaneous confirmatory error control.

阻断与依赖：P2-B3 and progression; exact threshold choice alone cannot repair coverage reachability. D05,D06,D07,D09,D10

对应参数组：SP28,SP29,SP30,SP31,SP32,SP36,SP39

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D08；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 159；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 14；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_criterion_spec_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `98a578944e7910db933f5b3b02aee4bb03de8005853024b38cc3b02630b04e38`。

- `docs/P2_design/v2/P2_stage_state_contract_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `c64803a93c74ee9dba6a7bc61de2d2e550264f2c5d4a920e1248665fa7e86b93`。

- `docs/statistical_protocol.md` — lines3–16,34–47；immutable source at audited revision；SHA-256 `f9c0eeb6e76f68330ba3e5d8d90e58d175c3947a1948bb41b26ad50dbc041e8a`。

- `docs/user_request.txt` — §44, lines1465–1494; §100, lines2730–2741；immutable source at audited revision；SHA-256 `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461`。

- `docs/P2_design/P2_mapping_opportunity_decision_table_v1.md` — entire59lines；immutable source at audited revision；SHA-256 `4c981f2f2303e1b1535168dd320e3c11151ea86ad35a502513893370a5906ea2`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D09 — REVISE_BEFORE_APPROVAL

原始问题：选择runner架构，裁决完成产物精确复用、失败/不完整默认停止、重试登记和P2源码dirty控制。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D09：是否要求先补齐锁域、租约/旧 owner fencing、恢复与实际执行身份，再审定 R1、精确复用、零自动 retry、P2 洁净和状态/出口规则？另明确 timing 协议须在 candidate timing 前及完整 P2 推进前冻结。

可行选项：Targeted report-driven design revision then R1/R2 decision; defer; reject proposed recovery semantics. No new process or retry authorization.

已知事实：Actual identity/hash/exit/failed-artifact retention, partition guards and gated progression are source requirements. Precheck/validation/formal cleanliness source rule does not itself impose new P2 cleanliness.

推导：Blueprint-before-content avoids original first-materialization cycle; completion, support and permission are logically distinct. Timing budget0 cannot satisfy required frozen P2 timing protocol.

新增科学假设：No new candidate/scientific scalar; zero retry, exact reuse and P2 clean-source policy constrain which executions may enter planned evidence.

工程约定：R1 versus R2, locks/attempts/CAS publication, append-only recovery, actual child code and orchestrator exits, separate state fields.

缺少的证据：Lock exclusion across authorizations/attempts, stale-owner fencing and actual-HEAD/dirty typed evidence need revision (identity_recovery_review.md). Runtime failure/recovery/P1 tests pending. Timing protocol remains undefined and must be separately approved/frozen.

公平性、复现、成本与统计影响：Acyclic identity alone does not prove concurrency safety; exit0 must not bypass current-source P0/P1, complete evidence, approved criteria and timing freeze.

阻断与依赖：P2-B4 and all materialization/execution. Approval of design does not authorize implementation or P2. D04,D05,D08,D10

对应参数组：

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D09；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 176；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 15；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_runner_schema_review_v2.md` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `fd1a59638bf1754af0a6423b57873a6691af8c3559a1c1d62ceeeffda2da5099`。

- `docs/P2_design/v2/P2_stage_state_contract_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `c64803a93c74ee9dba6a7bc61de2d2e550264f2c5d4a920e1248665fa7e86b93`。

- `docs/P2_design/v2/P2_typed_identity_schema_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `9b478cf7e96776f6cc69f29426715efed6eec2309270be1efb3dd77985ebfbc9`。

- `AGENTS.md` — rules4,6–8,10–14；immutable source at audited revision；SHA-256 `5435e5e690a64e0e7f432bae22b8f459f646e12233d99a7a4b1a70266d8c9a22`。

- `docs/user_request.txt` — §§90–95；immutable source at audited revision；SHA-256 `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461`。

- `docs/P2_design/human_decisions.md` — lines32–35；immutable source at audited revision；SHA-256 `791d6efc468bcb6d1fa37692d11de2d046fa3ea37f05d6030656f0d50e52eb55`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

### D10 — REVISE_BEFORE_APPROVAL

原始问题：选择可验证的科学envelope或新schema+adapter，批准namespace、规范化、ID、provenance、引用与旧P1兼容验证范围。

批准状态：**UNAPPROVED**。当前决策状态：HUMAN_DECISION_REQUIRED。

精确问题：D10：是否先要求补齐真实执行 HEAD/dirty 血缘及完整分析证据的 typed 绑定，再审定 S2、引用/ID/argv/COMPLETE 规范和旧 P1 回归范围？

可行选项：Targeted typed-schema revision then chooseS2/S1; defer for validation plan; reject schema route. Do not approve a label-only scientific origin.

已知事实：Original P1 fixture identity cannot be relabelled into science; scientific runs need real provenance, exact inputs and independently verified trace/metrics. Source changes need renewed P1 evidence.

推导：Birth validation must precede published envelope; parser-valid origin strings cannot prove actual generation; raw/semantic identity and receipts serve different roles.

新增科学假设：No added scientific scalar here; N/A/control/window choices trace to SP40 and observer evidence to D07/D08.

工程约定：S2 new scientific family/adapter versus S1 envelope,21 identity preimages and closed typed artifacts, argv/rendering, completion references.

缺少的证据：Closed RUN_MANIFEST lacks explicit actual execution HEAD/dirty binding identified by identity review; full M2 evidence roster not bound; all runtime lineage/adapter/negative regression tests are unimplemented.

公平性、复现、成本与统计影响：Closed schema may omit required provenance even while all listed fields validate; syntactic PASS is not runtime birth/identity proof.

阻断与依赖：P2-B5 and safe scientific input/run acceptance; no fixture conversion or execution. D04,D07,D08,D09

对应参数组：

实际来源（路径、定位、版本、SHA-256）：

- `docs/P2_design/decisions.draft.json` — original question; id D10；immutable source at audited revision；SHA-256 `047c4e1d0643795d96a42dc1c3089e3c94667c56c3a6d2a1d3ff364ea04c4cbf`。

- `docs/P2_design/v2/P2_complete_design_proposal_v2.md` — D section begins line 197；v2 DRAFT_UNAPPROVED；SHA-256 `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8`。

- `docs/P2_design/v2/P2_D01_D10_approval_checklist_v2.md` — line 16；v2 DRAFT_UNAPPROVED；SHA-256 `2bde515669146fe5432118c223c62d41fe37eb848ee525df08b42dc83bbd7c3b`。

- `docs/P2_design/v2/P2_runner_schema_review_v2.md` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `fd1a59638bf1754af0a6423b57873a6691af8c3559a1c1d62ceeeffda2da5099`。

- `docs/P2_design/v2/P2_typed_identity_schema_v2.json` — exact named JSON fields; registry pointer references retained；v2 DRAFT_UNAPPROVED；SHA-256 `9b478cf7e96776f6cc69f29426715efed6eec2309270be1efb3dd77985ebfbc9`。

- `docs/user_request.txt` — §41 and §§90–93；immutable source at audited revision；SHA-256 `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461`。

- `docs/statistical_protocol.md` — lines38–47；immutable source at audited revision；SHA-256 `f9c0eeb6e76f68330ba3e5d8d90e58d175c3947a1948bb41b26ad50dbc041e8a`。

- `docs/P2_design/human_decisions.md` — lines36–39；immutable source at audited revision；SHA-256 `791d6efc468bcb6d1fa37692d11de2d046fa3ea37f05d6030656f0d50e52eb55`。


人工响应：接受所指完整版本 / 拒绝并说明替代要求 / 暂缓并列证据。未收到响应；approval=UNAPPROVED。批准某条设计不自动授权实现或科学执行。

## 四十组参数与规则

以下问题逐项沿用原 SP 编号。完整拟议值/规则的 JSON 及其精确源指针、行号、哈希、v1 血缘在 `SP01_SP40_traceability.csv` 的同 ID 行中；没有把数值改写成正式值。每组的可选回答均为：批准所引用完整值 / 拒绝并提交明确替代需求 / 暂缓并列缺证据。涉及 V3-F01–F05 者应先完成修订再对新版本回答。

| ID / 决策 | 规则名称 | 精确问题 | 当前批准 |

|---|---|---|---|

| SP01 / D01 | six_topologies | 批准完整六模板或要求明确替代拓扑？ | UNAPPROVED |

| SP02 / D01 | importance_assignment | 批准整体服务 H/L 继承及每模板两变体？ | UNAPPROVED |

| SP03 / D01 | size_expansion | 批准二分尺寸变换并披露通信/流水级变化？ | UNAPPROVED |

| SP04 / D02 | role_compatibility | 批准完整兼容集合或要求新来源？ | UNAPPROVED |

| SP05 / D02 | role_execution_costs | 批准逐单元格合成代价及外推限制？ | UNAPPROVED |

| SP06 / D02 | cpu_symmetry | 批准 CPU 对称假设？ | UNAPPROVED |

| SP07 / D03 | edge_sizes | 批准74条边数据量、固定边及复制语义？ | UNAPPROVED |

| SP08 / D03 | link_latencies | 批准九类合成 latency？ | UNAPPROVED |

| SP09 / D03 | link_bandwidths | 批准九类合成 bandwidth？ | UNAPPROVED |

| SP10 / D04 | key_encoding_hash_mapping | 批准完整 v2 key/hash/canonical 定义，还是要求逐字段修订？ | UNAPPROVED |

| SP11 / D04 | estimate_distribution | 批准节点共享资源估计因子[.9,1.1)？ | UNAPPROVED |

| SP12 / D04 | realized_distribution | 批准资源独立实际时长因子及私有边界？ | UNAPPROVED |

| SP13 / D04 | arrival_jitter | 批准 U/10 及 H/L 共享到达扰动？ | UNAPPROVED |

| SP14 / D04 | arrival_burst | 批准5slot块和1/4压缩突发？ | UNAPPROVED |

| SP15 / D04 | service_count_and_group_mix | 批准50slot及50H/50L组成？ | UNAPPROVED |

| SP16 / D04 | deadline_multipliers | 批准 H2.5/L4 deadline 及精确参考路径？ | UNAPPROVED |

| SP17 / D04 | arrival_window | 批准W=50P及窗口/排空字段区分？ | UNAPPROVED |

| SP18 / D05 | period_axis | 批准每档两周期且不按结果扩轴？ | UNAPPROVED |

| SP19 / D05 | main_method_set | 批准全部主基线及B2控制职责？ | UNAPPROVED |

| SP20 / D05 | finite_order_budget | 批准完整顺序和预算上限及零自动重试？ | UNAPPROVED |

| SP21 / D06 | control_input_transform | 批准两控制、父100 G及其有限见证解释？ | UNAPPROVED |

| SP22 / D06 | load_pressure_bands | 批准这三段pressure阈值？ | UNAPPROVED |

| SP23 / D06 | load_miss_bands | 批准miss bands及每seed资源忙等待要求？ | UNAPPROVED |

| SP24 / D06 | configuration_selection | 批准 A-before-B 和每条件完整资格选择？ | UNAPPROVED |

| SP25 / D07 | M1_snapshot_subset | 是否先修订单ready观察域与阴性覆盖的不相容？ | UNAPPROVED |

| SP26 / D07 | M1_counterfactual_objective | 批准该投影目标及有限解释，还是要求替代诊断定义？ | UNAPPROVED |

| SP27 / D07 | M2_measurements | 是否要求明确M2配对清单与必需报告后再批准？ | UNAPPROVED |

| SP28 / D08 | material_gain_cutoff | 事前选择哪套tau，或明确拒绝并要求另提完整规则？ | UNAPPROVED |

| SP29 / D08 | frequency_cutoff | 事前选择哪套f，并接受FULL条件率的范围？ | UNAPPROVED |

| SP30 / D08 | stability_requirement | 批准8/10与≤2/10稳定性界限或要求事前替代？ | UNAPPROVED |

| SP31 / D08 | condition_aggregation | 是否先修订可达性/完整性，再批准全12条件规则？ | UNAPPROVED |

| SP32 / D08 | bootstrap_implementation_pin | 批准SHA索引实现pin，保持既有CI方法不变？ | UNAPPROVED |

| SP33 / D07 | target_H_selection | 批准最多2个H目标及排序/截断，或要求明确修订？ | UNAPPROVED |

| SP34 / D07 | bounded_public_suffix_rollout | 批准固定suffix及其阴性解释限制，或要求另拟有界诊断？ | UNAPPROVED |

| SP35 / D07 | local_L_slack_admissibility | 批准局部L slack及不代表全局L合规的限制？ | UNAPPROVED |

| SP36 / D08 | coverage_and_missing_evidence | 是否先修订不可达阴性门槛，再决定覆盖及缺失规则？ | UNAPPROVED |

| SP37 / D07 | state_equivalence_denominator | 批准状态去重/事件保留/重放排除及预调用记录范围？ | UNAPPROVED |

| SP38 / D06 | absolute_conservative_feasibility_arithmetic | 批准绝对RN64证书及严格/等号边界？ | UNAPPROVED |

| SP39 / D08 | selected_calibration_interpretation | 是否接受条件性描述限制及相应强制报告措辞？ | UNAPPROVED |

| SP40 / D06 | control_NA_and_window_semantics | 批准唯一控制N/A、组计数及窗口语义？ | UNAPPROVED |


## 回答格式和执行边界

人工答复请明确 ID、选择、所审版本/哈希、例外和补证据项。任何改变的数值或机制先成为新未批准提案，再审核，不把“同意修订方向”解释为批准修订后的未知内容。

```text
ID=<Dxx 或 SPxx>
SOURCE_VERSION_AND_HASH=<所审具体文档/对象>
RESPONSE=<APPROVE_EXACT_CONTENT / REJECT / DEFER / REQUEST_REVISION>
EXACT_SCOPE_AND_EXCEPTIONS=<具体内容>
EVIDENCE_REQUIRED=<具体证据或 NONE>
```

此为可复制答复模板，不是已填写的批准记录。本报告全部 approval=UNAPPROVED。未生成/运行科学工作负载，未生成种子，未批准冻结，未解锁验证/正式分区。完成后 STOP=YES。

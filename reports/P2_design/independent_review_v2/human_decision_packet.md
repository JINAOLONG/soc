# Human decision packet — v2 independent-method review
Review target 892ce2b71fd0c89f1b241c950b597eafab894e23. All approvals below remain UNAPPROVED. ACCEPT AS PROPOSED is an auditor recommendation, not a human decision. D01–D10 and 32 named parameter groups remain unresolved.
Exact source bytes/hashes: reviewed_sources.json. The registry is preserved as groups, not counted as32 scalar values. No FINE/COARSE selection is made; first repair V2-F01, because threshold choice cannot restore a blind observation target.
## D01
Original question: 选择显式角色 DAG 还是确定性 grammar，并提供三场景的完整8/16节点拓扑、角色/H-L归属及尺寸规则。
Exact current proposal/options (v1, not edits): 显式COCKPIT/ADAS/FUSION各8/16模板；节点边数8/9→16/17、8/9→16/17、8/7→16/15；v→v.a→v.b、各半基代价；内部边1/16MiB；节点继承整服务H/L、实例ID前缀，无dummy。
Source requirements versus proposals: 三场景角色、8/16真实可执行节点及继承H/L是已有要求；六个具体拓扑/扩展边及成本拆分是新提议。 Source: docs/user_request.txt §§18,33–34; docs/workload_spec.md:3–12; docs/model_spec.md:4–14.
Auditor recommendation: **ACCEPT AS PROPOSED**.
Remaining limitations: 有限合成拓扑不代表真实车辆；16节点改变通信/流水，不能解释为纯计算规模效应。
Required changes / findings: No blocking structural change requested; future runtime/scientific validation still pending.
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.
- `docs/P2_design/P2_workload_templates_v1.json` / v1 / SHA256 `97762849c9fd4d6e715d197b553fe157a091ce2a09bce8270b8e5eba7dcbff04`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D02
Original question: 选择有来源的profile表或批准的合成规则，提供兼容集合、各资源估计/实际代价及全部参数/来源。
Exact current proposal/options (v1, not edits): 16角色×CPU0–CPU3/GPU0/NPU0完整合成表；四CPU对称；null不兼容；estimate=base*scale*[.9,1.1)，actual=estimate*独立资源[.9,1.1)，精确正下界.405ms。完整96单元逐项见原JSON。
Source requirements versus proposals: 六资源、兼容性覆盖、正值和估计/真值隔离是已有要求；所有16角色代价/兼容集合/对称性/扰动分布都是合成提议。 Source: docs/model_spec.md:10–14,48–58; docs/workload_spec.md:10–12.
Auditor recommendation: **ACCEPT AS PROPOSED**.
Remaining limitations: 合成speedup/硬加速器亲和可人为塑造机会；不是硬件测量，无功耗或WCET保证。
Required changes / findings: No blocking structural change requested; future runtime/scientific validation still pending.
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.
- `docs/P2_design/P2_resource_profiles_v1.json` / v1 / SHA256 `5e303a5b5f0c096fbc38ce1d762bc1cbf3d8e09472d2c460160bb8b88993b0a4`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D03
Original question: 提供边MiB与type-pair latency/bandwidth的完整表或有来源规则，保留既有通信语义。
Exact current proposal/options (v1, not edits): 74条显式边，9有向type pairs：同类型(.01ms,16MiB/ms)，CPU↔GPU(.05,8)，CPU↔NPU(.05,4)，GPU↔NPU(.08,4)；同单元覆盖0，跨单元L+b/B；无总线竞争。
Source requirements versus proposals: 单位、零同单元、目的地副本/因果/无总线是已有语义；全部边MiB、latency和bandwidth数值为合成提议。 Source: docs/model_spec.md:3,20–31.
Auditor recommendation: **ACCEPT AS PROPOSED**.
Remaining limitations: 无总线竞争、固定边与合成带宽限制外推；类型对角不可误当同单元。
Required changes / findings: No blocking structural change requested; future runtime/scientific validation still pending.
Artifacts/version/hash:
- `docs/P2_design/P2_communication_profiles_v1.json` / v1 / SHA256 `c3671a75ec593f1f48f731812bfbfe74f4728d48f1db419ea36605407900ebad`.
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D04
Original question: 确定keyed扰动/PRNG/版本、到达/突发、H-L组成、deadline、服务数或窗口及停止边界的完整定义/值。
Exact current proposal/options (v1, not edits): SHA256首64位q/2^64；逐字段domain key、精确有理数再一次binary64；50slot各H/L共100；5slot块内1/4压缩+U/10 jitter；W=50P；H deadline2.5*C_est、L4*C_est；两个control保留扰动、改到达/删L。
Source requirements versus proposals: method-independent key、原seed、arrived-only信息边界和full drain已有要求；hash-to-U、字段填值、分布、窗口/到达/deadline为新提议。 Source: docs/model_spec.md:39–58; docs/user_request.txt §§24–25,36,41.
Auditor recommendation: **REVISE BEFORE APPROVAL**.
Remaining limitations: 未钉死key填值会改变实际输入；同步H/L和固定突发并非实测分布；C_est非可行证明。
Required changes / findings: V2-F02 首次物化的输入守卫、run锁和内容身份形成先决循环; V2-F03 key填值与identity preimage未达到跨实现逐字节唯一; V2-F07 控制缺组状态与窗口/排空指标需统一typed语义
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.
- `docs/P2_design/P2_generation_spec_v1.json` / v1 / SHA256 `e67c6d884f61b771c7a90b3d72e75e1e6c0787eb7376c7575cbd63354de60ff3`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D05
Original question: 确定枚举或有限轴展开，提供所有值/方法子集及理由/顺序/预算/seed到trial-condition-workload的精确映射。
Exact current proposal/options (v1, not edits): 18条件×A/B=36配置×10既有calibration seed×(5 MAIN+2 B2控制)=2520；MAIN1800、控制各360；输入1080；含重放引擎最多5040；自动retry0；timing0且未冻结。周期light80/64、medium24/20、near12/10ms。
Source requirements versus proposals: 18主条件、10calibration seed、B2焦点、B1–B5身份来自已有协议；36配置、周期、2520预算/次序/两控制为新提议。 Source: docs/workload_spec.md:14–25; docs/baseline_spec.md:14–20; docs/user_request.txt §§36,41–42.
Auditor recommendation: **ACCEPT AS PROPOSED**.
Remaining limitations: 2520是计划slots而非已运行或成本可承受证明；所有A/B负面必须保留；timing未冻结。
Required changes / findings: V2-F02 首次物化的输入守卫、run锁和内容身份形成先决循环
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.
- `docs/P2_design/P2_trial_matrix_draft_v1.json` / v1 / SHA256 `a68ef6b61f0e604dfebf1500b9a36fd7db1097938ae5abf321b1bf39aac23f2f`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D06
Original question: 确定H可行性对照、压力/负载分类、配置选择/平局以及不达标、不可行、无效、失败、不完整的处置规则。
Exact current proposal/options (v1, not edits): H隔离按deadline成功为控制见证；乐观路径LB>D才是充分不可行证据；低竞争全服务串行。B2 pressure按seed max-resource窗口busy/W再均值；light[0,.5)、medium[.5,.8)、near[.8,1]；light H/L DMR≤.01，后两H DMR∈[.01,.8]且每seed有资源等待；按target资格A优先B次之，负面保留。
Source requirements versus proposals: 基本可行性先检、按实测压力分负载、负面保留和无候选选型已有要求；具体bins、control变换、A/B资格为新提议。 Source: docs/workload_spec.md:14–20; docs/user_request.txt §§35–37; docs/metric_spec.md:3–10.
Auditor recommendation: **REVISE BEFORE APPROVAL**.
Remaining limitations: 独占见证只针对改到达控制，不能声称主输入H-only流已可调度；B2 miss不是普遍不可行证明；选型后CI条件性。
Required changes / findings: V2-F06 B2选型后的机会CI需限定为校准选中样本的条件性描述; V2-F07 控制缺组状态与窗口/排空指标需统一typed语义
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.
- `docs/P2_design/P2_generation_spec_v1.json` / v1 / SHA256 `e67c6d884f61b771c7a90b3d72e75e1e6c0787eb7376c7575cbd63354de60ff3`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D07
Original question: 选择M1机制诊断、M2基线描述或组合，确定观察量、反事实控制/视窗、信息边界和每seed/condition汇总。
Exact current proposal/options (v1, not edits): B2主运行公共view，前min(4,ready_count)个、K≥2含H；fixed B2 order、greedy EFT局部基准与至多6^4 mapping枚举；L局部finish逐项不增；最小H finish均值，g=(b-o)/b；分母eligible独特view。M2为B1/B3/B4/B5对B2配对描述，非因果。
Source requirements versus proposals: 2–4 ready局部oracle、公共信息边界和机制记录已有允许；M1局部目标/截断/L限制/分母及M2列表为新提议。 Source: docs/model_spec.md:48–58; docs/user_request.txt §§32,43–44; docs/baseline_spec.md:16–20.
Auditor recommendation: **REVISE BEFORE APPROVAL**.
Remaining limitations: 单ready-H盲区和未ready后继遗漏；严格局部L限制与全局P95预算不同；B2轨迹和前4截断不覆盖所有机制。
Required changes / findings: V2-F01 当前ready-H局部目标的阴性结果不能覆盖原登记的后继H稀缺资源机制; V2-F04 M1记录身份不等于分母去重契约，snapshot与重放范围仍需定型
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D08
Original question: 确定跨seed/条件聚合、稳定性、不确定性和三向结论的全部条件/参数及缺失无效处置，保持既有CI方法。
Exact current proposal/options (v1, not edits): FINE tau=.01,f=.01,k=8/10；COARSE tau=.05,f=.05,k=8/10；12 selected medium/near条件全部检验。S:每条件CIlo≥f且K≥8；N:每条件CIhi<f且K≤2；否则INCONCLUSIVE；Nviews=0/缺失无效闭锁。10k paired bootstrap/analysis seed20261018/type7，索引实现pin仍待批。
Source requirements versus proposals: paired seed、10k、20261018、type7、不得挪用H/L阈值是已有约束；FINE/COARSE频率/幅度/stability/全12要求及索引pin为新提议。 Source: docs/statistical_protocol.md:3–16,34–47; docs/user_request.txt §§44,100.
Auditor recommendation: **REVISE BEFORE APPROVAL**.
Remaining limitations: 严格全12判据可能保守；小N可得到高度离散的seed频率；仅pointwise，不能给条件外/选型前确认性解释；阈值选择不能修复F01。
Required changes / findings: V2-F01 当前ready-H局部目标的阴性结果不能覆盖原登记的后继H稀缺资源机制; V2-F04 M1记录身份不等于分母去重契约，snapshot与重放范围仍需定型; V2-F05 执行完整性出口尚未精确绑定选择、诊断、冻结与P2门禁输出; V2-F06 B2选型后的机会CI需限定为校准选中样本的条件性描述
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.
- `docs/P2_design/P2_mapping_opportunity_decision_table_v1.md` / v1 / SHA256 `4c981f2f2303e1b1535168dd320e3c11151ea86ad35a502513893370a5906ea2`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D09
Original question: 选择runner架构，裁决完成产物精确复用、失败/不完整默认停止、重试登记和P2源码dirty控制。
Exact current proposal/options (v1, not edits): R1扩展唯一正式run_pipeline calibration入口（推荐）vs R2同守卫薄launcher；匹配全身份才复用；0自动retry；保留失败、attempt链和原子COMPLETE；新增P2相关源码洁净策略为待批工程要求，非现行合同。
Source requirements versus proposals: 真实身份/退出/复用核验/保留失败与分区守卫已有要求；R1/R2、零retry、具体锁顺序/exit/P2洁净为新提议。 Source: AGENTS.md rules4,6–8,10–14; docs/user_request.txt §§90–95; scripts/run_pipeline.py:26–39.
Auditor recommendation: **REVISE BEFORE APPROVAL**.
Remaining limitations: 首次物化依赖循环；identity/实际argv/锁域未钉死；exit0不能当P2 PASS，当前无运行时证明。
Required changes / findings: V2-F02 首次物化的输入守卫、run锁和内容身份形成先决循环; V2-F03 key填值与identity preimage未达到跨实现逐字节唯一; V2-F05 执行完整性出口尚未精确绑定选择、诊断、冻结与P2门禁输出; V2-F08 S2来源隔离与P1兼容仍需未来行为证明，不能用声明替代
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.
- `docs/P2_design/P2_runner_schema_review_v1.md` / v1 / SHA256 `21c4ccb2fbb608131ff28903fc90a60feb70111c9888d444e43165dbf3241f04`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## D10
Original question: 选择可验证的科学envelope或新schema+adapter，批准namespace、规范化、ID、provenance、引用与旧P1兼容验证范围。
Exact current proposal/options (v1, not edits): S2新namespace soc.science.p2/version1+adapter（推荐）vs S1 envelope；字段涵盖workload/run/attempt/actual seed/partition/全部hash/生成血缘/真实exit/独立trace/metrics/replay/raw refs/COMPLETE；保持P1原身份。
Source requirements versus proposals: 科学run血缘/完整性/seed和fixture隔离已有要求；S2/S1路线、ID/preimage/schema字段/COMPLETE合取为新提议。 Source: docs/user_request.txt §§41,90–93; docs/statistical_protocol.md:38–47; src/soc/model/schema.py:175–189.
Auditor recommendation: **REVISE BEFORE APPROVAL**.
Remaining limitations: 新origin不能凭标签认证；新源码会改变P1身份；缺组enum和窗口语义必须统一；静态schema不证明真实血缘。
Required changes / findings: V2-F02 首次物化的输入守卫、run锁和内容身份形成先决循环; V2-F03 key填值与identity preimage未达到跨实现逐字节唯一; V2-F04 M1记录身份不等于分母去重契约，snapshot与重放范围仍需定型; V2-F05 执行完整性出口尚未精确绑定选择、诊断、冻结与P2门禁输出; V2-F07 控制缺组状态与窗口/排空指标需统一typed语义; V2-F08 S2来源隔离与P1兼容仍需未来行为证明，不能用声明替代
Artifacts/version/hash:
- `docs/P2_design/P2_complete_design_proposal_v1.md` / v1 / SHA256 `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac`.
- `docs/P2_design/P2_runner_schema_review_v1.md` / v1 / SHA256 `21c4ccb2fbb608131ff28903fc90a60feb70111c9888d444e43165dbf3241f04`.

Human approval: **UNAPPROVED**
Selected option: null; approved values: null; reviewer: null; approval time: null; approval evidence: null.
## Exact value appendix (quoted proposal metadata, no generated samples)
### Six templates and every predecessor
- COCKPIT-8-v1 (8 executable nodes/9 edges): COCKPIT.n01[audio, group=inherited H,L, scale=1] <- ROOT; COCKPIT.n02[speech, group=inherited H,L, scale=1] <- COCKPIT.n01; COCKPIT.n03[intent, group=inherited H,L, scale=1] <- COCKPIT.n02; COCKPIT.n04[display, group=inherited H,L, scale=1] <- COCKPIT.n03,COCKPIT.n05; COCKPIT.n05[navigation, group=inherited H,L, scale=1] <- ROOT; COCKPIT.n06[route, group=inherited H,L, scale=1] <- COCKPIT.n03,COCKPIT.n05; COCKPIT.n07[compose, group=inherited H,L, scale=1] <- COCKPIT.n04,COCKPIT.n06; COCKPIT.n08[interaction, group=inherited H,L, scale=1] <- COCKPIT.n07.
- COCKPIT-16-v1 (16 executable nodes/17 edges): COCKPIT.n01.a[audio, group=inherited H,L, scale=1/2] <- ROOT; COCKPIT.n01.b[audio, group=inherited H,L, scale=1/2] <- COCKPIT.n01.a; COCKPIT.n02.a[speech, group=inherited H,L, scale=1/2] <- COCKPIT.n01.b; COCKPIT.n02.b[speech, group=inherited H,L, scale=1/2] <- COCKPIT.n02.a; COCKPIT.n03.a[intent, group=inherited H,L, scale=1/2] <- COCKPIT.n02.b; COCKPIT.n03.b[intent, group=inherited H,L, scale=1/2] <- COCKPIT.n03.a; COCKPIT.n04.a[display, group=inherited H,L, scale=1/2] <- COCKPIT.n03.b,COCKPIT.n05.b; COCKPIT.n04.b[display, group=inherited H,L, scale=1/2] <- COCKPIT.n04.a; COCKPIT.n05.a[navigation, group=inherited H,L, scale=1/2] <- ROOT; COCKPIT.n05.b[navigation, group=inherited H,L, scale=1/2] <- COCKPIT.n05.a; COCKPIT.n06.a[route, group=inherited H,L, scale=1/2] <- COCKPIT.n03.b,COCKPIT.n05.b; COCKPIT.n06.b[route, group=inherited H,L, scale=1/2] <- COCKPIT.n06.a; COCKPIT.n07.a[compose, group=inherited H,L, scale=1/2] <- COCKPIT.n04.b,COCKPIT.n06.b; COCKPIT.n07.b[compose, group=inherited H,L, scale=1/2] <- COCKPIT.n07.a; COCKPIT.n08.a[interaction, group=inherited H,L, scale=1/2] <- COCKPIT.n07.b; COCKPIT.n08.b[interaction, group=inherited H,L, scale=1/2] <- COCKPIT.n08.a.
- ADAS-8-v1 (8 executable nodes/9 edges): ADAS.n01[preprocess, group=inherited H,L, scale=1] <- ROOT; ADAS.n02[detect, group=inherited H,L, scale=1] <- ADAS.n01; ADAS.n03[segment, group=inherited H,L, scale=1] <- ADAS.n01; ADAS.n04[track, group=inherited H,L, scale=1] <- ADAS.n02; ADAS.n05[fusion, group=inherited H,L, scale=1] <- ADAS.n03,ADAS.n04; ADAS.n06[plan, group=inherited H,L, scale=1] <- ADAS.n05; ADAS.n07[render, group=inherited H,L, scale=1] <- ADAS.n05; ADAS.n08[output, group=inherited H,L, scale=1] <- ADAS.n06,ADAS.n07.
- ADAS-16-v1 (16 executable nodes/17 edges): ADAS.n01.a[preprocess, group=inherited H,L, scale=1/2] <- ROOT; ADAS.n01.b[preprocess, group=inherited H,L, scale=1/2] <- ADAS.n01.a; ADAS.n02.a[detect, group=inherited H,L, scale=1/2] <- ADAS.n01.b; ADAS.n02.b[detect, group=inherited H,L, scale=1/2] <- ADAS.n02.a; ADAS.n03.a[segment, group=inherited H,L, scale=1/2] <- ADAS.n01.b; ADAS.n03.b[segment, group=inherited H,L, scale=1/2] <- ADAS.n03.a; ADAS.n04.a[track, group=inherited H,L, scale=1/2] <- ADAS.n02.b; ADAS.n04.b[track, group=inherited H,L, scale=1/2] <- ADAS.n04.a; ADAS.n05.a[fusion, group=inherited H,L, scale=1/2] <- ADAS.n03.b,ADAS.n04.b; ADAS.n05.b[fusion, group=inherited H,L, scale=1/2] <- ADAS.n05.a; ADAS.n06.a[plan, group=inherited H,L, scale=1/2] <- ADAS.n05.b; ADAS.n06.b[plan, group=inherited H,L, scale=1/2] <- ADAS.n06.a; ADAS.n07.a[render, group=inherited H,L, scale=1/2] <- ADAS.n05.b; ADAS.n07.b[render, group=inherited H,L, scale=1/2] <- ADAS.n07.a; ADAS.n08.a[output, group=inherited H,L, scale=1/2] <- ADAS.n06.b,ADAS.n07.b; ADAS.n08.b[output, group=inherited H,L, scale=1/2] <- ADAS.n08.a.
- FUSION-8-v1 (8 executable nodes/7 edges): FUSION.n01[audio, group=inherited H,L, scale=1] <- ROOT; FUSION.n02[speech, group=inherited H,L, scale=1] <- FUSION.n01; FUSION.n03[navigation, group=inherited H,L, scale=1] <- ROOT; FUSION.n04[detect, group=inherited H,L, scale=1] <- FUSION.n05; FUSION.n05[preprocess, group=inherited H,L, scale=1] <- ROOT; FUSION.n06[fusion, group=inherited H,L, scale=1] <- FUSION.n02,FUSION.n04; FUSION.n07[compose, group=inherited H,L, scale=1] <- FUSION.n03,FUSION.n06; FUSION.n08[interaction, group=inherited H,L, scale=1] <- FUSION.n07.
- FUSION-16-v1 (16 executable nodes/15 edges): FUSION.n01.a[audio, group=inherited H,L, scale=1/2] <- ROOT; FUSION.n01.b[audio, group=inherited H,L, scale=1/2] <- FUSION.n01.a; FUSION.n02.a[speech, group=inherited H,L, scale=1/2] <- FUSION.n01.b; FUSION.n02.b[speech, group=inherited H,L, scale=1/2] <- FUSION.n02.a; FUSION.n03.a[navigation, group=inherited H,L, scale=1/2] <- ROOT; FUSION.n03.b[navigation, group=inherited H,L, scale=1/2] <- FUSION.n03.a; FUSION.n04.a[detect, group=inherited H,L, scale=1/2] <- FUSION.n05.b; FUSION.n04.b[detect, group=inherited H,L, scale=1/2] <- FUSION.n04.a; FUSION.n05.a[preprocess, group=inherited H,L, scale=1/2] <- ROOT; FUSION.n05.b[preprocess, group=inherited H,L, scale=1/2] <- FUSION.n05.a; FUSION.n06.a[fusion, group=inherited H,L, scale=1/2] <- FUSION.n02.b,FUSION.n04.b; FUSION.n06.b[fusion, group=inherited H,L, scale=1/2] <- FUSION.n06.a; FUSION.n07.a[compose, group=inherited H,L, scale=1/2] <- FUSION.n03.b,FUSION.n06.b; FUSION.n07.b[compose, group=inherited H,L, scale=1/2] <- FUSION.n07.a; FUSION.n08.a[interaction, group=inherited H,L, scale=1/2] <- FUSION.n07.b; FUSION.n08.b[interaction, group=inherited H,L, scale=1/2] <- FUSION.n08.a.
### Complete six-resource role profile (ms; null=incompatible)
| role | CPU0 | CPU1 | CPU2 | CPU3 | GPU0 | NPU0 |
|---|---:|---:|---:|---:|---:|---:|
| audio | 2 | 2 | 2 | 2 | null | null |
| speech | 12 | 12 | 12 | 12 | null | 3 |
| intent | 1 | 1 | 1 | 1 | null | null |
| display | 8 | 8 | 8 | 8 | 2 | null |
| navigation | 3 | 3 | 3 | 3 | null | null |
| route | 8 | 8 | 8 | 8 | 3 | null |
| compose | 6 | 6 | 6 | 6 | 2 | 3 |
| interaction | 1 | 1 | 1 | 1 | null | null |
| preprocess | 6 | 6 | 6 | 6 | 2 | null |
| detect | null | null | null | null | null | 4 |
| segment | 16 | 16 | 16 | 16 | 4 | 5 |
| track | 3 | 3 | 3 | 3 | null | null |
| fusion | 6 | 6 | 6 | 6 | null | 2 |
| plan | 2 | 2 | 2 | 2 | null | null |
| render | null | null | null | null | 2 | null |
| output | 1 | 1 | 1 | 1 | null | null |

### Complete communication metadata
- CPU→CPU: latency=0.01ms, bandwidth=16MiB/ms.
- CPU→GPU: latency=0.05ms, bandwidth=8MiB/ms.
- CPU→NPU: latency=0.05ms, bandwidth=4MiB/ms.
- GPU→CPU: latency=0.05ms, bandwidth=8MiB/ms.
- GPU→GPU: latency=0.01ms, bandwidth=16MiB/ms.
- GPU→NPU: latency=0.08ms, bandwidth=4MiB/ms.
- NPU→CPU: latency=0.05ms, bandwidth=4MiB/ms.
- NPU→GPU: latency=0.08ms, bandwidth=4MiB/ms.
- NPU→NPU: latency=0.01ms, bandwidth=16MiB/ms.
- COCKPIT-8-v1: COCKPIT.n01->COCKPIT.n02=0.25MiB; COCKPIT.n02->COCKPIT.n03=0.125MiB; COCKPIT.n03->COCKPIT.n04=0.0625MiB; COCKPIT.n05->COCKPIT.n04=0.125MiB; COCKPIT.n03->COCKPIT.n06=0.0625MiB; COCKPIT.n05->COCKPIT.n06=0.125MiB; COCKPIT.n04->COCKPIT.n07=1MiB; COCKPIT.n06->COCKPIT.n07=0.25MiB; COCKPIT.n07->COCKPIT.n08=1MiB.
- COCKPIT-16-v1: COCKPIT.n01.a->COCKPIT.n01.b=0.0625MiB; COCKPIT.n01.b->COCKPIT.n02.a=0.25MiB; COCKPIT.n02.a->COCKPIT.n02.b=0.0625MiB; COCKPIT.n02.b->COCKPIT.n03.a=0.125MiB; COCKPIT.n03.a->COCKPIT.n03.b=0.0625MiB; COCKPIT.n03.b->COCKPIT.n04.a=0.0625MiB; COCKPIT.n05.b->COCKPIT.n04.a=0.125MiB; COCKPIT.n04.a->COCKPIT.n04.b=0.0625MiB; COCKPIT.n05.a->COCKPIT.n05.b=0.0625MiB; COCKPIT.n03.b->COCKPIT.n06.a=0.0625MiB; COCKPIT.n05.b->COCKPIT.n06.a=0.125MiB; COCKPIT.n06.a->COCKPIT.n06.b=0.0625MiB; COCKPIT.n04.b->COCKPIT.n07.a=1MiB; COCKPIT.n06.b->COCKPIT.n07.a=0.25MiB; COCKPIT.n07.a->COCKPIT.n07.b=0.0625MiB; COCKPIT.n07.b->COCKPIT.n08.a=1MiB; COCKPIT.n08.a->COCKPIT.n08.b=0.0625MiB.
- ADAS-8-v1: ADAS.n01->ADAS.n02=4MiB; ADAS.n01->ADAS.n03=4MiB; ADAS.n02->ADAS.n04=1MiB; ADAS.n03->ADAS.n05=2MiB; ADAS.n04->ADAS.n05=0.25MiB; ADAS.n05->ADAS.n06=0.5MiB; ADAS.n05->ADAS.n07=0.5MiB; ADAS.n06->ADAS.n08=0.125MiB; ADAS.n07->ADAS.n08=1MiB.
- ADAS-16-v1: ADAS.n01.a->ADAS.n01.b=0.0625MiB; ADAS.n01.b->ADAS.n02.a=4MiB; ADAS.n02.a->ADAS.n02.b=0.0625MiB; ADAS.n01.b->ADAS.n03.a=4MiB; ADAS.n03.a->ADAS.n03.b=0.0625MiB; ADAS.n02.b->ADAS.n04.a=1MiB; ADAS.n04.a->ADAS.n04.b=0.0625MiB; ADAS.n03.b->ADAS.n05.a=2MiB; ADAS.n04.b->ADAS.n05.a=0.25MiB; ADAS.n05.a->ADAS.n05.b=0.0625MiB; ADAS.n05.b->ADAS.n06.a=0.5MiB; ADAS.n06.a->ADAS.n06.b=0.0625MiB; ADAS.n05.b->ADAS.n07.a=0.5MiB; ADAS.n07.a->ADAS.n07.b=0.0625MiB; ADAS.n06.b->ADAS.n08.a=0.125MiB; ADAS.n07.b->ADAS.n08.a=1MiB; ADAS.n08.a->ADAS.n08.b=0.0625MiB.
- FUSION-8-v1: FUSION.n01->FUSION.n02=0.25MiB; FUSION.n05->FUSION.n04=4MiB; FUSION.n02->FUSION.n06=0.125MiB; FUSION.n04->FUSION.n06=1MiB; FUSION.n03->FUSION.n07=0.125MiB; FUSION.n06->FUSION.n07=0.5MiB; FUSION.n07->FUSION.n08=1MiB.
- FUSION-16-v1: FUSION.n01.a->FUSION.n01.b=0.0625MiB; FUSION.n01.b->FUSION.n02.a=0.25MiB; FUSION.n02.a->FUSION.n02.b=0.0625MiB; FUSION.n03.a->FUSION.n03.b=0.0625MiB; FUSION.n05.b->FUSION.n04.a=4MiB; FUSION.n04.a->FUSION.n04.b=0.0625MiB; FUSION.n05.a->FUSION.n05.b=0.0625MiB; FUSION.n02.b->FUSION.n06.a=0.125MiB; FUSION.n04.b->FUSION.n06.a=1MiB; FUSION.n06.a->FUSION.n06.b=0.0625MiB; FUSION.n03.b->FUSION.n07.a=0.125MiB; FUSION.n06.b->FUSION.n07.a=0.5MiB; FUSION.n07.a->FUSION.n07.b=0.0625MiB; FUSION.n07.b->FUSION.n08.a=1MiB; FUSION.n08.a->FUSION.n08.b=0.0625MiB.

### Remaining generation/selection choices
D04 exact current distribution/window/deadline/control formulas are verbatim in the hashed P2_generation_spec_v1.json. D05 has all2520 rows in its hashed matrix; no selected configuration/outcome exists. D06 pressure/miss bands are candidates, not existing thresholds.
D08 FINE(.01 gain,.01 rate,8/10 seeds) and COARSE(.05,.05,8/10) remain UNAPPROVED. Its exact S/N/evidence-completeness predicates are in the hashed decision table. Do not choose a bundle based on results. D09 R1/R2 and D10 S1/S2 remain UNAPPROVED despite audit architecture recommendations.
## Permitted next request
A documentation-only revision can be separately authorized to address V2-F01..F07, preserve current v1/history, issue precise changed-value diffs and repeat review. Human must still approve exact values/version/hash. No implementation, generation, P2 execution or unlock follows automatically.

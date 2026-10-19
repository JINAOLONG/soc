# P2 Runner and Scientific Schema Review v1

DRAFT / UNAPPROVED。以下均是完整接口/不变量提案，IMPLEMENTATION_VALIDATION_PENDING。
不新增或修改实现，不注册schema，不调用P2，不制造scientific artifact实例。
依据：`AGENTS.md` 3、6–8、10–14；`docs/user_request.txt` §§23–25、41、90–93；
`docs/statistical_protocol.md:38–47`；`docs/P2_design/runner_and_schema.md`既有缺口表。

## D09：入口比较与唯一推荐

| 方案 | 技术含义/公平性 | 复现/成本/风险 |
|---|---|---|
| R1，推荐 | 扩展既有run_pipeline的calibration分支为唯一正式入口；调用共享guard、材料化和验证组件 | 单一审计面，避免参数漂移；未来须证明旧P0/P1调用行为不变 |
| R2 | thin launcher只转交R1/同guard，不具备独立授权、seed或路径覆盖权 | 适合批管理但多一层CLI/退出传播；当前不需要，不能绕过R1 |

推荐R1属PROPOSED工程建议；现`src/soc/validation/governance.py:181–208`只有阶段授权，
`scripts/run_pipeline.py:26–39`科学分支未实现。文档不是runner正确性验证。

未来入口拒绝DRAFT、未批准决定、未解析wlref/null必填、未通过P0/P1、身份冲突、非CALIBRATION
及未登记method/config/trial。不能从草案加一个approved=true就运行：须核对独立审批收据
含审批者/原始答复/版本/文件hash、批准值、批准计划和实现验证证据，且另有明确执行授权。
当前draft命令均null，现行pipeline完全不读取这些文件。

P2 relevant source/config已提交且洁净是**拟新增工程政策**，待D09批准；现行合同明确要求
committed clean的是precheck/validation/formal。推荐在未来P2也拒绝相关dirty/untracked输入，
允许报告输出自然变脏但不得将它们计为代码。若拒绝此建议，必须另审可完整恢复dirty字节/
补丁hash的方案，本版不隐式启用dirty执行。Git hash不能代替实际文件SHA。

### 生命周期与fail-closed

计划/审批/代码hash守卫 → 原子申请run identity锁 → 生成并核验immutable输入 →
PREPARED attempt收据 → 实际调用 → 关闭stdout/stderr/raw refs并记录exit →
独立trace验证/指标复算 → 同输入同方法重放 → 原子发布COMPLETE摘要。

保留planned_at、started_at、ended_at、monotonic_elapsed_ns和实际host/argv/cwd；
UTC ISO8601明确时区，系统墙钟回跳单记clock_anomaly，不据此改科学虚拟时间。
记录process_started、exit_code、termination_kind、signal/exception、stdout/stderr与raw输出
引用。spawn失败process_started=false、started_at/exit=null；中断未收集exit时也为null，
不得补0。预先登记状态PREPARED/RUNNING/FAILED/INVALID/INCOMPLETE/COMPLETE、错误码和
最后成功阶段。虚拟sim_end/drain独立于wall timestamps。

| 情况 | 拟定行为 |
|---|---|
| 已有COMPLETE | 精确匹配下列identity+所有ref真实hash/大小、validator与metrics/replay身份，重验证完成不变量；生成reuse receipt，零新样本/零引擎调用 |
| 相同run ID但内容/plan等值不匹配 | CONFLICT，停止，不取最新、不覆盖、不另ID隐匿冲突 |
| 未COMPLETE/进程失败/中断 | 保留部分文件并写INCOMPLETE/FAILED收据；停止整个计划，自动retry=0 |
| 代码/输入/validator/配置变了 | 不能复用；新批准plan及新run identity，旧结果保留，不暗中替换科学配对 |
| 并发/部分写入 | run锁互斥；attempt私有tmp目录，文件close+fsync后hash；末尾摘要同文件系统原子rename，冲突拒绝；不得覆盖已完成摘要 |
| 后续人工批准重跑 | 本版无自动或手动救结果预算。必须先审批修复原因/触发条件/次数/plan变更；新attempt及supersedes边保留旧失败，不能将该扩展冒充原2520计划已完整 |

attempt链以(run_id,ordinal)唯一，初始ordinal=1；重用不建新attempt，单独reuse receipt；
新attempt必须明确supersedes前一attempt/原因/授权hash，无环且不能跨run ID。不同input/source
不是“重试同一run”，而是新run并以related_run链接。没有经过审批的retry，不会有ordinal>1。
进程实际退出码原样保存；runner可另给编排码：0仅本计划完整，2前置/身份拒绝，3执行失败，
4验证非法，5中断/不完整（均PROPOSED接口码，不冒充现有返回码）。任何错误停止后续trial，
未启动记录NOT_STARTED，不能创建伪成功产物。固定一次重放是验证步骤，不是失败重试。

### 复用等值集合

必须同时匹配approved plan hash、trial/condition/config/method与method实现身份、actual seed/
CALIBRATION/scene/load/size/control variant、generator/template/profile/network/参数hash、
workload identity及payload/input hash、source file manifest/Git/dirty policy、model/metric/
diagnostic/criterion/validator/replay实现版本与hash、schema/canonicalization版本、调用argv。
host不影响纯虚拟仿真语义但仍是记录字段；本版**保守建议复用也匹配host identity**，避免
未经验证的跨host bit差异。若未来放宽须另行语义等价证明。start/end和attempt ordinal不进入
run语义identity，避免重执行每次变ID；receipt必须引用原完整attempt和本次核验时间。
timing本版不纳入，未来timing不得借此跨host复用。

## D10：S1/S2比较与字段表

S1是在已验证envelope外扩字段，P1 payload字节保留，迁移成本较低；但P1 Workload/trace/
validator均写死HAND_AUTHORED_CORRECTNESS_FIXTURE，外层包scientific标签不解决来源。
S2是新namespace/version+显式科学adapter，隔离来源更清晰，未来需实现新的科学输入/输出
路径及独立validator分派并回归P1。**推荐S2**属工程提案，不声称schema或adapter已正确。
证据：`src/soc/model/schema.py:175–189`、`simulator/engine.py:100`、
`validation/trace.py:75–79`。现有scientific_artifacts.schema.draft.json保留原样作为历史结构选项。

| 字段/类型（PROPOSED） | 必需语义/规范 |
|---|---|
| namespace/version/kind | `soc.science.p2` / `1`；kind=workload/run/attempt/validation/metrics/replay/stage/reuse，各自schema与hash |
| approval/plan refs | 不可变审批收据、提案文件SHA、解析后的批准矩阵SHA、执行授权；拒绝draft来源 |
| canonicalization/version | `soc-canonical-v1`，D04的ASCII参数JSON/分数；每个文件真实raw hash；禁止重复键、NaN、非规范分数 |
| workload_id | `urn:soc:workload:v1:<identity_preimage_sha256>`；preimage具体D04定义；method和wall time不在其中 |
| payload/input SHA | binary64运行payload按schema.canonical_bytes独立规范hash；实际输入文件另存raw SHA/大小；禁止自包含hash环 |
| run_id | `urn:soc:run:v1:<SHA256(semantic identity)>`；包括上述复用集合的语义字段及plan/trial/host，不包含attempt/timestamp/output hashes |
| attempt_id/ordinal | `run_id:attempt:0001`；正整数顺序、关联parent attempt/authorization、supersedes无环；首个无supersedes |
| actual_seed/partition | seed为注册52-bit整数同时保留十进制key表示，partition固定CALIBRATION，membership据原seed文件hash核对 |
| scenario/condition/config/method | 显式ID、load、size、variant、comparison_role，严格匹配approved trial；不得任意命令行替代 |
| source identity | Git full hash、actual branch、dirty status、相关文件清单SHA、generator/model/scheduler/validator/analysis各实现hash、Python版本 |
| configuration hashes | approved参数、模板、资源、通信、generation、matrix、statistical/metric/criterion版本及SHA，不能只有config ID |
| generator lineage | 真实generator commit/file hash、command/exit、输入参数ref、CALIBRATION来源、父main/control转换ref、完整immutable输入ref |
| invocation | exact argv数组/cwd/host，planned_at/started_at/ended_at、monotonic_elapsed_ns、process_started、exit_code、signal/exception/termination_kind |
| trace validation | trace raw ref、input ref、validator source/command/actual exit/report ref、独立status/errors、验证边界；不信任engine自报 |
| metrics/derivation | runtime指标与独立重算的ref/hash、公式/版本、输入trace/workload hash、逐字段比较报告、缺组/N/A原因；main必须H和L |
| replay | exact run semantic身份、第二次raw outputs/ref、decision/physical event/metric逐项一致性结论；不是第二科学样本 |
| diagnostic refs | 公共snapshot/ready digest、M1基准/assignment/局部约束/Δ/g、eligible分母/hits、M2配对ref、版本；不得把true private字段混入snapshot |
| provenance refs | 每ref为repo-relative允许目录path+sha256+size_bytes+media_type+kind；禁止../绝对路径/越权符号链接/公共PDF副本 |
| completeness/status/errors | expected refs和集合、存在/hash/唯一性/allowlist/配对结果；errors具code/phase/message/ref；原子COMPLETE条件见下 |
| raw output/log refs | 输入、trace、stdout/stderr、engine原始metrics、validation、replay、异常/中断日志，空文件也保存真实SHA及0字节 |
| stage record | exact expected/attempted/completed/reused/failed/not_started ID集合；每阶段完整性六项检查、选择收据、criterion ref、阴性/未定原因，不自动P3 |

参数规范分数须denominator>0、gcd=1，0写0/1；标识稳定ASCII。数组规则：资源按既有CPU0..3,
GPU0,NPU0；模板/节点/边/refs按ID字典序；服务按service_id；trial按execution_order；
事件/decision保持实际顺序不排序，防止更改事件语义。JSON字段排序不改变数组。
提案中的decimal词法值先精确解析为十进制再转最简分数（.05=1/20），不得经binary64中转；
这才是参数身份preimage。文件本身的原始SHA与规范参数SHA分别保存，不要求两者相等。
保存identity preimage raw ref，使外部可重算ID；文件hash不包括自指hash值。引用形成有向
血缘图，禁止循环：attempt终结摘要指向raw，raw头只含预先可得run/workload ID，不含摘要hash。

**COMPLETE充要合取提案**：真实进程started且exit=0、全部预期raw/log refs匹配hash/大小、
输入/允许seed/方法/plan/生成血缘全部有效、独立trace PASS、完整metrics逐字段重算一致、
重放exact-match、无error、原子结束摘要有效。H-only允许L指标为CONTROL_NA，但main不允许。
stage COMPLETE还须全部2520 expected trial的有效唯一完成/合法复用、missing/mismatch/
duplicate/unexpected seed/method/condition=0；完整性与科学SUPPORTED分开，负结果也可完整。
未知/空运行列表不能COMPLETE或PASS。现有schema注释没有强制这些行为，本版也仅写设计。

### 两层验证与fixture隔离

静态层：未来JSON Schema required/type/enum/conditional约束、规范preimage、foreign-key
和计划预算；本轮只做提案规格间静态核对，**没有科学schema实例验证通过的声明**。
运行层：真实hash/读取权限、generator出生证明、adapter数据守恒、独立trace/metrics/replay、
中断/锁/原子发布/重复冲突、允许分区访问、未来信息边界都必须另行实现并故障测试。

P1 fixture原始路径、origin和注册SHA保留。科学出生证明不能指向P1 fixture lineage；改
name/seed/origin或添加fixture_derivation=false一律不足。未来adapter不能将fixture payload
包装后当科学输入；科学入口要求可核对的批准generator真实生成日志和内容hash，control
父输入也必须科学来源。旧P1只走旧路径/旧标签，科学只走新路径，代码共享数据结构不共享
样本身份。新增回归需拒绝假标签/伪造seed/引用旧fixture/漏ref/恢复旧hash等，当前全部
IMPLEMENTATION_VALIDATION_PENDING。实际机会、可行性、负载和成本为SCIENTIFIC_EXECUTION_PENDING。

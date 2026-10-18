# P2 design proposal v2 — DRAFT / UNAPPROVED / NONEXECUTABLE

本包是对提交`79f9c245b23119ce25175d6dc6ff148e9e092461`中v1及独立审计的**拟议修订**，
不是已批准替换。v1、原审计及其失败完整保留；D01–D10全部UNAPPROVED。没有实现生成器、
runner、adapter、诊断或validator，没有物化输入或执行P2。JSON是设计文档，不接入现行pipeline。

本轮授权原文：`reports/P2_design/design_revision_v2/authorization_request.txt`。
历史问题：`reports/P2_design/independent_review_v2/findings.json` V2-F01–F07；F08仍待未来实现验证。
审计实际建议D05 ACCEPT AS PROPOSED，任务摘要把它并入REVISE；本版保留原记录，仍修订D05
身份引用/物化顺序以协调F02，不改变其轴、数值、方法、预算和引擎顺序。

## 依据与陈述身份

SOURCE_SUPPORTED：`docs/user_request.txt` §§17–25、32–37、41–44、80、90–95、100；
`docs/model_spec.md:3–58`；`docs/workload_spec.md:3–25`；`docs/baseline_spec.md:3–20`；
`docs/metric_spec.md:3–52`；`docs/statistical_protocol.md:3–47`；`AGENTS.md`规则3、6–14。
历史原文审查保持`docs/literature_matrix.md`及reviews的既有范围，未把任何合成数值归给文献。

DERIVED：预算乘积、无环身份顺序、非负模型的下界归纳、枚举含基准则最优不劣于基准。
PROPOSED：所有保留的合成参数与新增观察器、覆盖、锁/身份/数值操作规则，仍需人工批准。
IMPLEMENTATION_VALIDATION_PENDING：全部科学生成/adapter/runner/独立诊断与血缘检查。
SCIENTIFIC_EXECUTION_PENDING：可行性、实际负载、机会、成本与统计支持，全部未知。

规范优先关系：本主文解释设计；各命名JSON给出精确字段/值。typed identity schema定义字段，
generation定义填值，snapshot定义事件/状态，diagnostic定义观察量，criterion定义判据，stage
定义资格/出口。不能从示例或说明推导另一套默认值。若冲突，报告并闭锁，不自行择一。

## D01 — 保留六模板，未批准

`P2_workload_templates_v2.json`保留v1全部节点/前驱/角色/H-L继承/尺寸规则和template ID。
COCKPIT：8节点9边、16节点17边；ADAS同为8/9、16/17；FUSION为8/7、16/15。
v→v.a→v.b，各半基代价；原u→v改u.b→v.a，内部边1/16MiB；无dummy，所有节点真实计数。
局部template ID仍带v1，表示语义模板未变，不是文档版本错误。实例ID精确规则见generation。
一个服务整体H或L，节点继承，不新添ASIL语义。仍是有限合成模型，不代表实车分布。

## D02 — 保留六资源/16角色数值，未批准

`P2_resource_profiles_v2.json`保留96个资源单元格及兼容集合。CPU0–3同值，null是不兼容，
不作为可执行0代价；CPU-only、GPU/NPU-oriented、多兼容和专属加速器角色均存在。
估计因子与实际因子仍为[.9,1.1)；16节点每半节点基代价1/2；精确转换前下界81/200ms。
只有公共估计可给scheduler和M1R，真实代价仅引擎/离线验证。未增加硬件或功耗实测声明。

## D03 — 保留74边与九类通信数值，未批准

`P2_communication_profiles_v2.json`全部边与link表保持原值。单位ms、MiB、MiB/ms不变。
同单元0；不同单元L+b/B；CPU跨核非零；副本属于目的地，pending remap重算数据就绪。
不改非抢占、传输起点、重叠或无总线竞争假设。合成通信与固定边尺寸限制外部有效性。

## D04 — typed keyed生成、身份和控制

精确对象见`P2_typed_identity_schema_v2.json`的closed `$defs`，字段不得增删或省略为默认。
根schema_version=2，generator_version=`soc-p2-synthetic-v2-PROPOSED`，key domain=`soc.p2.gen.v2`。
不再有含义不明的version字段。`P2_generation_spec_v2.json#/key_bindings`以LITERAL/COPY逐字段给出三种key，context路径与类型固定；gloss不是运行实例。

每种key都保留actual seed十进制字符串、scenario、condition、config、整数slot、schema/gen版本。
arrival_jitter仅将group/node/resource/edge置空；估计因子保留group/node，resource/edge为空；
实际因子再保留resource。counter固定0。方法、run/attempt、控制到达、host、wall time、调用次数
不入扰动key。边和deadline没有随机draw，禁用未登记随机源。

SHA256规范key字节的前8字节大端q，U=q/2^64为精确有理数；因子.9+U/5，jitter=U/10。
所有计算先精确有理数，每个最终数值只一次RN64 ties-to-even；私有exact estimate/deadline
sidecar只供生成/控制核验，不进入公共视图。v2域/键绑定改变未来draw身份；没有v1 realization
可比较，也不声称v1/v2将产生同一样本。数值分布本身未变。

MAIN仍50slot，每slot一个H和L，共100服务；5slot块内压缩1/4；W=50P；全量排空，无warmup剔除。
H relative deadline=2.5*C_est、L=4*C_est，C_est从转换前E_exact取min-compatible路径，忽略通信。
它不证明可行。绝对deadline按原模型RN64(arrival+relative_deadline)计算。

服务ID：`{scenario}/{load}/{size}/{config_id}/s{slot:03d}/{H|L}`。
节点ID：`{service_id}/{preserved_template_node_id}`。condition=`{scenario}-{load}-{size}`。

控制始终从**已解析MAIN父输入**派生，保留所有被保留节点的估计/真实代价、相对deadline及
边的binary64位，不重新draw。G对父MAIN全部100服务计算，两个控制使用同一个G；精确公式
和一次ceil+1ms规则在generation JSON。H-only按原slot保留50H，LOW按slot、H在L前保留100服务。
都改为k*G到达，故与MAIN有不同descriptor/content identity，绝不复用MAIN内容hash。
先物化/解析MAIN，再派生控制；这不执行MAIN方法，也不改变D05的引擎执行顺序。

canonical语义对象只接受ASCII字符串、精确整数、bool/null、array/object；不接受浮点。
Rational为最简`{numerator:十进制字符串,denominator:正十进制字符串}`，0只用0/1，禁-0。
表中的decimal词法先精确Decimal转分数，不经binary64。键ASCII排序、紧凑JSON、UTF-8、单LF，
拒绝重复键和非ASCII身份。raw SHA计算实际文件原字节；语义SHA另算。运行payload单独使用
Python3.12 binary64 JSON规范，不能与语义参数hash混称。golden fixtures不是生产输入。

## D05 — 保留完整有限矩阵

`P2_trial_matrix_draft_v2.json`逐条列出2520条trial，保留：

- 18主条件×A/B=36配置，10个既有CALIBRATION seed；没有新seed。
- 周期：light80/64、medium24/20、near12/10ms，两尺寸不变。
- MAIN B1–B5共1800；H_ISOLATED B2和LOW_COMPETITION B2各360。
- 1080计划输入，主360+控制720；最终条件选择后主输入180。
- 每trial最多1个primary+1个注册replay，最大5040引擎调用；自动retry0。

trial ID/wlref改为v2引用，config ID/seed/method/排序不变。workload内容hash与实际command仍null，
这是未执行的符号计划，不是伪造的已完成证据。物化顺序MAIN→控制，与引擎控制→MAIN顺序分离。
所有A/B都保存、运行资格检查，不因为最终只选一个就删另一组。B2仍为焦点参考，五基线职责不变。
诊断只是离线分析：每完整view最多1296映射，每映射最多36节点，最多42日历区间；不额外调用引擎。
这些是组合上界，不是已测成本或可承受性证明。工程timing预算0、NOT_FROZEN，不隐式移除其前提。

## D06 — 总分类、选择与可行性

`P2_stage_state_contract_v2.json#/load_classification`为精确谓词来源：
REGISTERED→完整运行集→输入/trace/metric/replay有效→控制资格→本身declared target-load匹配→
ELIGIBLE或INELIGIBLE→先A后B→SELECTED_ALL_18或NO_ELIGIBLE_CONDITION。
一个候选符合另一档压力不等于符合自身目标，禁止换标签、clamp或删seed。

压力p_seed先取每资源[0,W)busy区间精确测度/W的最大值，再对10seed平均。H/L DMR各先逐run
按组计数再对seed平均。light p∈[0,.5)、H/L均值≤.01；medium p∈[.5,.8)；near p∈[.8,1]，
后两H均值∈[.01,.80]且每seed至少一个节点在data-ready之后有正的实际资源busy等待。
不把policy idle wait全部当资源忙。压力三段对有效p互斥穷尽；其他谓词可拒绝全部，保留OFF_TARGET。

所有10seed的H-only与LOW控制分别无服务重叠且所需组按原deadline完成才有资格。合法控制miss
或无隔离见证是有效负面、配置INELIGIBLE，继续既定trial；控制变换不合法、缺组、非法trace、
缺失/非有限统计、hash/重放不符是INVALID/INCOMPLETE，停止整个计划，不当作零机会。

天然不可行证书使用**离线私有真实代价**，不能进scheduler或M1R。数学实数下界与实际计算分开：
先取compatible实际duration最小值m、合法资源对通信最小值c。计算版使用与现引擎相同分组的
binary64 RN64：根从真实arrival开始；R_v=max(arrival,max_pred RN64(B_pred+c_min))；
B_v=RN64(R_v+m_v)。与RN64(arrival+relative_deadline)比较，只有严格大于才CERTIFIED_NATURALLY_INFEASIBLE。
等号不证不可行；B≤deadline不证可行；B2控制miss不证所有调度皆不可行。有限非负RN64单调，
同分组归纳得B_v≤合法执行finish；溢出/NaN直接拒绝，不用任意epsilon或相对时间减法补救。
控制成功只证明改到达控制的见证，不证明MAIN或原H-only流的可调度性。

选型后的CI是同校准seed、同选中配置下的条件性描述；不创造独立确认数据，也不更换CI算法。

## D07 — M1历史范围与M1R_PATH_V2

旧`M1_READY_PREFIX_V1`保持原定义/源hash，只是历史诊断。它的阴性不能否定remaining-H-path
稀缺资源机制。本版拟议stage观察器为`M1R_PATH_V2`，精确规范见`P2_diagnostic_spec_v2.json`。

E的在域状态：至少一个dependency-ready未开始节点，且至少一个已到达H服务有未开始节点。
先按原B2顺序选最多4 ready任务；保留原§44的2–4 ready oracle范围：只有1 ready时记覆盖不足，
不把它当零机会或执行单任务oracle。K不必含ready H，目标H可以是正在运行前驱之后的公开后继。
目标最多两个H服务，事先按deadline/service ID选定；各完整公开DAG最多16节点。

初始日历只固定可见running任务的估计释放，不查看真实finish。若任何busy任务elapsed≥estimate，
不能为已知仍busy的单元编造now释放；记覆盖不足，不加epsilon或看队列。
K固定顺序，枚举兼容映射≤6^4。基准用同有理算术的greedy EFT。K间及可见running日历都固定。
随后对选中H服务的全部未放置节点作固定Kahn顺序、deadline/service/node ties和EFT gap插入，
只投影已到达公开图。后继只作为预测，不冒充actual completed，不做suffix组合优化。
两个target+K总计≤36个投影节点，当前running上下文≤6；没有未来到达、真值或反馈到实际B2。

局部L约束改为K内每个L节点finish≤max(基准该节点finish,该服务absolute deadline)。这是新增
诊断slack规则，不是全局L-P95 1.10预算，也不证明L整个DAG结束不劣化。目标是选中H服务
投影完成时刻均值最小，同分按K资源向量字典序。最优枚举包含基准；b为基准H均值finish-now，
o为最优对应值；Δ=b-o≥0ms，g=Δ/b。全部来自公共binary64值的精确有理运算，区别于runtime浮点。

FULL：ready全部落在2..4内、所有pending H服务≤2、DAG/日历/枚举完整、running释放可预测。
截断、单ready或估计过期：COVERAGE_INSUFFICIENT；可存有限子空间描述，但不计hit或率，不补零。
真正g=0只表示该完整测试空间无改善；0<g<tau为低于实质cutoff，不与零混称。
缺snapshot/非法/独立复算不符是INCOMPLETE/INVALID证据并闭锁，不是合法覆盖不足。

非科学§32解释例：K含H前驱2与L可选NPU6/CPU6.5；固定suffix含H的NPU4，故投影完成10对6，
而新局部L cap=max(6,12)=12容纳6.5。只是检查机制定义能覆盖已登记解释，不是科学结果或CI。

M2仍为相同输入B1/B3/B4/B5相对B2的H-DMR、L-P95、资源等待等配对描述；不作为独立因果
mapping证据。旧M1不进入v2门禁，不声称M1R或M2验证了候选，也没有提出online候选公式。

## D08 — 同单位的覆盖与三态

`P2_criterion_spec_v2.json`及配套decision table为唯一判据提案。FINE(tau=.01,f=.01)、
COARSE(.05,.05)，稳定8/10、阴性≤2/10均保留候选数值，未选择、无默认，目标观测量已改变。
新增拟议覆盖要求：每seed/condition支持至少4/5，阴性必须1。它们不来自文献或H/L门槛。

E=完整primary MAIN-B2 stream中唯一在域状态数；F=FULL状态数；p=hits/F，coverage=F/E。
E或F=0则p未定义，不能写0；部分覆盖从p排除但在E保留，不悄悄消失。120个seed/loaded-condition
单元均须满足相应覆盖，且无缺失无效记录。共同seed-index paired bootstrap保持10,000/
20261018/type7不变；只分析seed p，不按view/node/100服务当独立样本；选中校准CI仍为描述。

支持：全部12条件CI下端≥f且各有≥8seed p≥f，全部coverage≥4/5。
不支持：全部coverage=1且全部12条件CI上端<f、各≤2seed p≥f。
其余INCONCLUSIVE；missing/invalid/incomplete不能当阴性。没有执行时仍NOT_EVALUATED。
阴性只是不支持此注册有界公共预测观察器下的稳定机会，按协议停止推进；不证明所有策略、
所有未观察未来或无限时域都没有mapping机制。固定suffix/局部L/截断可能损失覆盖，必须披露。

## D09 — 无环首物化、恢复与出口

R1仍推荐：未来唯一正式calibration入口。现行入口仍未实现，本轮未调用。
完整顺序、21种preimage及恢复表见runner/schema文档和报告identity_dependency_graph。

先审批不可变blueprint、符号execution plan及显式生成/执行授权；以已知descriptor/authorization
hash取得input lock，才能物化。MAIN先生成并验证解析，控制再派生；resolution receipt不改蓝图。
然后发布稳定内容workload ID，计算semantic argv、run/attempt ID、run锁，再pre-invocation守卫。
实际执行后保存原始输出，独立trace/metrics及注册replay，最后原子COMPLETE。
预调用守卫才要求resolved输入；首个生成守卫只要求已批蓝图/源/seed/授权，不能提前索要未来payload。

任何中断保留append-only证据；完整输出精确核验才复用，失败/不完整不自动续写或重试。
新attempt/重跑预算需另行明确登记，当前自动retry0；replay是原计划的一次验证，不是救结果重试。
P2相关源码洁净并已提交仍为待批工程要求，不冒充既有合同已经强制。

execution COMPLETE、integrity、identity、selection、diagnostic、mapping、timing和progression
分别记录。有效阴性可执行完整但不能推进；任一未知/缺失/未冻结闭锁。未来拟议orchestrator
code0也只表示其全部前提满足，绝不提供下一阶段授权；子进程实际code另存，不伪造0。
当前timing为NOT_FROZEN，故即使未来这份calibration-only清单完整且观察器支持，仍不得以此
宣称完整P2工程协议完成。原2ms目标保留，未测量。

## D10 — typed科学家族与P1隔离

S2仍推荐但未批准：未来新scientific输入/trace/receipt家族与显式adapter。精确字段在typed
schema中，实际实例尚未创建。原P1 schema_version1和HAND_AUTHORED_CORRECTNESS_FIXTURE
字节/样本身份保持；不改名包装为科学样本。合法科学出生要求批准generator真实过程、
descriptor、MAIN/control父关系、raw/semantic hashes和独立解析验证，origin字符串不足。

控制唯一N/A token=`NOT_APPLICABLE_CONTROL`。MAIN精确100/50H50L，H-only50H，LOW100/50H50L。
仅H-only的L组可N/A且数值null；主输入缺组是INVALID。makespan=max实际finish，与observation_end
分别命名，不替换既有指标。future source/adapter变更后须重跑原64测试、45正trace/20负trace
及信息边界/失败关闭测试；静态schema成功不证明这些行为，也不能继承旧P1哈希。

## 审批、参数与停止

`P2_scientific_parameter_registry_v2.json`保持SP01–SP32映射，新增拆出的SP33–SP40，共40组。
没有删除或合并。每组记录v1规则、v2规则、原因、finding与审批状态；这是参数/规则组，非40个标量。
D01–D10全部UNAPPROVED。新增科学假设和工程接口均未激活。v2只成为最新待审草案索引，不成为
现行批准合同。静态设计检查不能证明科学有效、runtime正确、硬件真实性或统计支持。
本轮完成文档交付即停止；下一安全动作只有人工审阅v2具体选项/值/风险并明确记录决定。

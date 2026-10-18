# P2 Complete Experimental Design Proposal v1

状态：**DRAFT / UNAPPROVED / NONEXECUTABLE**。这是人工审批对象，非生效规格或实验结果。
依据提交 `160800d9b136e953c6415cd5229ded87eae72a0f`；本轮授权原文归档于
`reports/P2_design/proposal_v1/authorization_request.txt`。全部 D01–D10 仍需人工决定。

## 证据与声明类型

| 标记 | 本提案中的含义 |
|---|---|
| SOURCE_SUPPORTED | 已有文件明确支持，后附具体定位；文献只支持所审查的概念范围 |
| DERIVED | 从已登记约束严格推导，例如 18 个主条件、预算乘积和无环性 |
| PROPOSED | 新的拓扑、合成数值、分布、选择和工程政策，全部未批准 |
| UNRESOLVED | 人工未裁决，含已有具体推荐但未获批的参数；不设隐式默认 |
| IMPLEMENTATION_VALIDATION_PENDING | 生成器、科学 adapter、runner、诊断、schema、恢复行为均未实现验证 |
| SCIENTIFIC_EXECUTION_PENDING | 可行性、负载分类、机会频率、置信区间、成本均未计算 |

JSON 中 `classification=PROPOSED` 覆盖未另行标记的新增值。每份 JSON 均标明 DRAFT、
approved/frozen/executable/execution_authorized/read_by_pipeline=false。它们位于文档目录，
没有任何现行 pipeline 的读取接线，也不具备现行 Workload 所要求的 fixture origin。
批准提案仍不授权执行：还须单独授权实现、验证、冻结和科学运行。

| 依据 | 实际定位及支持范围 |
|---|---|
| 原始需求 | `docs/user_request.txt` §§17–25、32–37、41–44、80、90–93、100；§32 数字仅为手工正确性例子，禁止作为科学 profile |
| 工作负载 | `docs/workload_spec.md:3–25`：三场景、8/16 实节点、负载诊断、B2/10 CALIBRATION、同输入和排空 |
| 模型 | `docs/model_spec.md:3–58`：单位、六资源、兼容性、非抢占、副本通信、已批准事件序和信息边界 |
| 基线 | `docs/baseline_spec.md:3–20`，`docs/P1_implementation_spec.md` D1–D5：B1–B5 既有语义不改 |
| 指标/统计 | `docs/metric_spec.md:3–52`、`docs/statistical_protocol.md:3–47`：seed 单位、10,000 paired bootstrap、固定分析 seed、type-7、H/L 及 P3 mapping 门槛 |
| 合同/配置 | `docs/research_contract.md:3–9,32–48`；`configs/research_protocol.json` 的 main_grid、resources、bootstrap_*、scientific_executions：历史 DRAFT_P0_BLOCKED 字串不代表当前 gate 失败，保留原件 |
| 原始决策 | `docs/P2_design/decisions.draft.json` 各 id/question；`human_decisions.md` 原始前49行及十二字段审查；原编号/问题不改 |
| 原文证据 | `docs/literature_matrix.md` Original technical models、Identity/version；`docs/literature_evidence.json` 各 source/review_notes；`docs/literature_reviews/heft_cpop.md:35–49`（印刷262/264/266页）、`peft.md:33–46`（683/684/687/688页）、`ds3.md:12–29`（PDF3–6）、`starpu.md:12–24`（PDF4–7） |
| 其余已审查文献 | `literature_reviews/autoware_dag.md` §IV/§V、PDF2–4；`federated_limit.md` §2、PDF3–5：汽车 DAG 和比较器限制，均未提供本提案的六资源数值 |
| 实际门禁 | `reports/P2_design/proposal_v1/repository_audit.json`：当前 P0/P1 check-only exit=0，P1 122文件 missing/mismatch=0；`reports/P1_correctness.json` 保留既有64测试、45合法/20非法 trace 证据 |
| P2 阻断 | `reports/P2_mapping_opportunity.json` status=BLOCKED / NOT_RUN；`scripts/run_pipeline.py:26–39` 科学入口未实现（本轮未调用） |

文献仅支持异构代价表、DAG、EFT/OCT 和 profile 建模的概念。本轮没有重新开展原文审查，
没有将任何新数值归给作者。六篇审查范围及出处限制沿用原证据；DS3/StarPU 的数据不能
直接代替本项目 profile，HEFT/PEFT 的静态假设也不是本项目在线规则的来源。

## D01 — 显式六模板（PROPOSED / UNRESOLVED）

原始问题沿用目录 D01：显式角色 DAG 或 grammar，以及三场景完整8/16节点、角色/H-L/尺寸规则。
推荐显式模板，见 `P2_workload_templates_v1.json#/templates`；每个节点逐一列出唯一局部 ID、
角色、完整前驱、代价比例和 H/L 继承。服务实例必须整体 H 或整体 L，两个变体均存在；
实际节点 ID=`service_id/template_node_id`，故跨实例不冲突。没有节点被隐去或免计数。

| 场景 | 8节点/边 | 16节点/边 | 拟表达的机制 |
|---|---|---|---|
| COCKPIT | 8 / 9 | 16 / 17 | 语音意图链和导航分支，显示/路线并行后合成、交互输出 |
| ADAS | 8 / 9 | 16 / 17 | 检测/分割分叉、跟踪融合、规划/显示汇合；稀缺加速器 |
| FUSION | 8 / 7 | 16 / 15 | 语音和感知融合并与导航合成；多实例共享 CPU/GPU/NPU |

尺寸规则：每个 v 明确拆为同角色 v.a→v.b，各承担基代价的一半，原 u→v 改为 u.b→v.a，
内部边为1/16 MiB。增加8个真实执行节点和8条真实边（DERIVED），不增加 dummy。
Kahn 遍历核对全部节点被取出，拒绝缺前驱、自环、重复 ID/边；FUSION 中 n04 的前驱 n05
说明 ID 不是拓扑次序，禁止用 ID 大小替代无环验证。

理由：显式模板便于审计，成本较低；grammar 是原清单的可行替代，但当前没有批准其规则。
本方案范围有限、不是车辆任务分布；16节点维持基计算总量但增加通信/流水级，不能把尺寸
差异解释为纯计算规模效应。该偏差须在未来报告披露，不按效果换拓扑。
待答：是否批准六个显式模板、全部节点继承服务 H/L 和二分尺寸规则？

## D02 — 六资源合成 profile（PROPOSED / UNRESOLVED）

原始问题：选择可追踪 profile 或批准合成规则并给兼容集、估计/实际代价、全部来源。
推荐明确合成模型，不冒充没有取得的硬件数据；`P2_resource_profiles_v1.json` 给出16角色的
**六列完整资源表**，CPU0–CPU3同值，GPU0/NPU0分别列值。null 唯一表示不兼容；对应资源
不进入 compatible_resources，禁止把0或 infinity 当可执行时长。

| 角色 | CPU0/1/2/3 各自 ms | GPU0 ms | NPU0 ms |
|---|---:|---:|---:|
| audio | 2 | — | — |
| speech | 12 | — | 3 |
| intent | 1 | — | — |
| display | 8 | 2 | — |
| navigation | 3 | — | — |
| route | 8 | 3 | — |
| compose | 6 | 2 | 3 |
| interaction | 1 | — | — |
| preprocess | 6 | 2 | — |
| detect | — | — | 4 |
| segment | 16 | 4 | 5 |
| track | 3 | — | — |
| fusion | 6 | — | 2 |
| plan | 2 | — | — |
| render | — | 2 | — |
| output | 1 | — | — |

这些数值全部是工程合成提议：CPU基代价1–16ms给出可手算的时标；加速器优势与专属角色
用于覆盖合同要求的 CPU-only、GPU/NPU-oriented、multi-compatible、limited-alternative。
不是测量、文献原值或已验证现实比例。对称 CPU 避免人为核优势，但省略缓存和频率差异。
GPU/NPU优势及专属任务可能人为增加机会，外部有效性有限；不另加未预算的敏感性扫描。

estimated=base×节点比例×[0.9,1.1) keyed因子；realized=estimated×独立资源[0.9,1.1)因子。
最小实际代价≥0.405ms（DERIVED）。全部兼容资源的私有真值在未来生成时固化，只有 estimates
进入 scheduler。角色表、版本、原始字节/hash及生成代码身份均进入血缘（D04/D10）。
替代：取得经授权 profile 后形成另一完整提案，不能无版本替换本表。
待答：是否批准合成模型、全部16×6单元、CPU对称性和估计/实际关系？

## D03 — 完整边表和九类通信（PROPOSED / UNRESOLVED）

原始问题：边MiB和type-pair latency/bandwidth完整表，保留现行通信语义。
`P2_communication_profiles_v1.json` 逐一列出六模板 **74条边** 的 ID/源/目的/数据MiB；
8节点外部边取源角色输出量，16节点保留外部边，新增内部边1/16MiB，无未指定边。
每个角色的输出量不同是新合成提案；多后继各自传相同量而非自动分摊。

| 源→目的类型 | latency ms | bandwidth MiB/ms |
|---|---:|---:|
| CPU→CPU | .01 | 16 |
| CPU→GPU | .05 | 8 |
| CPU→NPU | .05 | 4 |
| GPU→CPU | .05 | 8 |
| GPU→GPU | .01 | 16 |
| GPU→NPU | .08 | 4 |
| NPU→CPU | .05 | 4 |
| NPU→GPU | .08 | 4 |
| NPU→NPU | .01 | 16 |

不同单元：delay=L+b/B，MiB/(MiB/ms)=ms；同一单元覆盖为0（SOURCE_SUPPORTED）。
例：CPU0→GPU0传4MiB：.05+4/8=.55ms；CPU0→CPU1传1MiB：.01+1/16=.0725ms；
NPU0→NPU0即使1MiB仍为0。类型对角不等于相同单元，不能把 CPU 跨核通信清零。

目的地副本从前驱实际完成才可传输并保留；pending remap重新计算目的地就绪，不复用别处
副本，不修改已开始节点。无共享总线竞争，传输彼此及与计算重叠（model_spec:20–31）。
大边/低带宽强化局部性、加速器互传较慢可能抑制卸载，这些是敏感性风险而非已见结果。
二进制友好的尺寸/带宽便于复核，不代表SoC实测。待答：是否批准完整74边及九对参数？

## D04 — keyed 物化规范（PROPOSED / UNRESOLVED）

原始问题：key/PRNG/版本、扰动、到达、H-L、deadline、服务数/窗口和停止边界全部确定。
完整提议在 `P2_generation_spec_v1.json`。本轮只写规范，**没有实现生成器或取任何科学随机样本**。

使用 domain-separated SHA-256，字段固定且无歧义 canonical JSON，包含已登记 actual seed、
scenario、condition、config、slot/group/node/resource/edge/field/counter/version；不用字段为空串。
seed以十进制字符串编码；标识ASCII；UTF-8，键排序、紧凑分隔、尾单LF、无NaN/重复键。
digest前8字节大端 q，U=q/2^64。没有顺序PRNG状态，method/attempt/调度次数不进入key。
不同字段分别取hash。节点估计因子对资源共用；实际因子按资源独立；控制变体沿用父输入key。
所有生成计算先用精确有理数，最终一次round-to-nearest ties-to-even转binary64；正值/有限检查。
身份参数用整数或规范分数，不用浮点序列化决定参数身份；运行payload沿用模型的独立字节hash。
提案JSON为便于阅读写出的decimal数值必须先按十进制词法精确解析（如parse_float=Decimal），
转换最简有理数再形成身份preimage，禁止先转binary64再反推参数。.05对应1/20，.01对应1/100；
原提案/配置文件本身另存raw-byte SHA，不把“规范语义hash”与“文件原始hash”混称。

| 新参数组 | 具体候选值/规则 | 理由与影响（均未批准） |
|---|---|---|
| 估计/实际扰动 | 两级独立[.9,1.1)均匀，具体key见JSON | 有界且严格正；不是误差实测，分布/相关性会影响鲁棒性 |
| 到达扰动 | 每slot共享U/10 | 保持H/L配对，避免方法相关RNG；同步到达可能夸大竞争 |
| 组成/样本量 | 50 slots，每slot H+L各1，共100服务 | H/L均有50个；不当作100独立seed，L尾分位仍噪声大 |
| 突发 | 5 slots为块，压缩系数1/4 | a=P*(5*(j//5)+(j%5)/4+U_j/10)，轻量周期突发而非泊松；限制外推 |
| 周期 | light 80/64ms；medium 24/20；near 12/10；两尺寸相同 | 两个有限候选，不保证实际压力或miss符合标签，D06可拒绝全部 |
| deadline | C_est为min-compatible估计路径下界；H=2.5 C_est，L=4 C_est | 方法无关且正；忽略通信不构成可行性证明，须先控验 |
| 窗口 | W=50P，半开[0,W)，全量排空 | 没有warmup剔除；未来运行结束=max(W,last_finish)，利用率分母需区分 |
| 边扰动 | 无，边值固定D03 | 避免额外自由度；不覆盖数据尺寸随机性 |

H/L deadline差异也属于PROPOSED，不是重要性定义自带。alternative为另行提供有出处到达/
profile规则，或修改上述具体候选后重出完整版本；本轮不悄然使用。未来workload ID由参数/
generator/seed/条件/variant/内容hash决定，独立method；矩阵中的wlref只是未物化计划引用，
其hash仍null。替换wlref必须保存解析收据，不能将符号字符串冒充实际内容SHA256。
待答：是否批准JSON所有编码、字段、数值、分布、构造及窗口？

## D05 — 有限矩阵、方法职责与预算（PROPOSED / UNRESOLVED）

原始问题：完整轴/值、方法集合/理由、顺序/预算、seed到trial映射。
推荐 `P2_trial_matrix_draft_v1.json`，**2520条显式trial**，每条含实际CALIBRATION seed、
scene/condition/config/method/variant/workload计划ID、角色、顺序、预算和选择/平局/失败规则引用。
每条command/hash=null，因为没有执行命令或科学输入；这些不是缺失的已运行证据。

注册3×3×2只定义18个最终主条件（SOURCE_SUPPORTED）。本提案每条件有A/B两个arrival候选，
共36配置；每个10seed做5方法主运行+2个B2控制。故
36×10×(5+1+1)=2520 trial slots（DERIVED），主1800、H独占360、低竞争360；
输入1080份，主360份、控制720份；最终选择18条件×10=180主输入，所有尝试保留。
每trial需1次严格重放且不增加样本数，最大全引擎调用5040。暂停/失败后的未启动格保持
NOT_STARTED，2520是完整成功执行时的计划数/上界，不是已花成本或达到时间预算。

B1是重要性排序对照；B2为全部配置/控制的焦点参考、负载选型及固定L预算参照；B3为
rank/EFT；B4为OCT前瞻；B5为H-priority OCT强基线。主网格全纳入，避免预期胜负筛选。
控制仅B2用于获得可行性见证和基准诊断，B2失败不能证明其他方法皆失败。无候选、消融
A1–A3、severe-overload、保留分区实验。基线比较仍有排序/映射混杂，D07另界定。

执行顺序：COCKPIT→ADAS→FUSION；light→medium→near；8→16；A→B；seed索引0..9；
H_ISOLATED B2→LOW_COMPETITION B2→MAIN B1..B5。trial记录execution_order唯一连续。
主方法顺序固定便于审计；主仿真无host timing结论，因此不将顺序当timing随机化。
选择规则SEL-v1只按D06 B2负载/可行性，先A后B；不以M1/M2效果挑配置，选后机会失败不回退
另一个配置救结论。保留全部seed/失败。若某条件无合格配置，P2 BLOCKED，不扩轴。

有限预算替代SMALL=2160（去B1，会损失重要性排序对照），不推荐；WIDE=3780是再加一候选
的预算说明，第三周期数值UNRESOLVED，未列为本版trial，不授权扩大。推荐全基线2520，
属于工程/研究设计建议，无文献能证明其最优或计算时间可承受。实际运行时长未知。

**工程timing不纳入本版矩阵**，预算0，inputs/warmup/repetitions/timer/aggregation全部
UNRESOLVED，不取默认，也不冻结为“不测”。固定P95≤2ms目标保留。需未来另行审批的
timing登记并在candidate timing前冻结；不影响当前明确不做timing的校准提案完整性。
待答：是否批准36配置/2520 slots/5040最大调用、全B1–B5、两个控制和固定顺序/选择？

## D06 — 可行性、负载和失败分类（PROPOSED / UNRESOLVED）

原始问题：H基础可行性、负载标签、试验选择/平局/失败继续停止规则。
推荐同时做H_ISOLATED与LOW_COMPETITION。控制从父主输入派生，保留原service/node/key/
duration/deadline，只有删L或改到达；不得复用不同内容hash。G在generation JSON中用
保守串行上界计算，各服务完全隔离；两个控制分别50/100服务、每份仍为单一trial，
不隐藏额外独占运行。H-only不要求有L，L指标为NOT_APPLICABLE_CONTROL，不能进入主统计。

| 类别 | 预先规定的证据/判定 | 继续、停止与保留 |
|---|---|---|
| H基础可行见证 | 合法H_ISOLATED控制内每个H完成≤自身原deadline，无服务重叠 | 这是注册deadline的直接比较，无新增容忍阈值；保留逐服务见证 |
| 天然不可行的充分证据 | 每个H的乐观路径LB：min兼容真实代价 + max前驱(LB+边最小合法通信)；若任一个LB>D | 即使允许不一致最优资源仍超期，是下界证据；保留，不归为调度器正确性失败；配置不准入 |
| 未证明可行/不可行 | B2独占miss但LB≤D，或无独占有效见证 | 不宣称天然不可行，不调deadline补救；不准入，可继续既定负面诊断 |
| 低竞争对照 | 全100服务串行隔离、来源有效，记录每个H/L deadline结果 | 不以低竞争标签自动断言可行；B2 miss单列，主配置不准入 |
| 合法但未达负载目标 | trace合法、完整，但以下压力/miss bands不符 | 保留并继续剩余既定trial；不可换标签或删seed |
| invalid | 输入/trace/血缘/配对不合法，或独立复算不一致 | 全计划停止，保留原件和诊断，缺格阻断完整性 |
| failed | 进程启动失败、非零、引擎deadlock或未完成命令 | 全计划停止；spawn未开始exit=null，不填0 |
| incomplete | 中断、缺文件/校验/重放、终结标记缺失 | 全计划停止；不续写、不自动重试，不与合法负结果混合 |

上述LB是真值的离线控制审计，不能传给scheduler。LB≤D不证明可行；独占B2 miss也不证明
全算法不可行（DERIVED）。这种区分遵循user_request §37和federated review的比较器限制。

以下是**新的待批准负载分箱数值，绝不是现行H可行性阈值或科学收益门槛**：对B2主运行，
逐seed计算p_s=max_r(busy_r∩[0,W])/W，再对10seed取均值p；不使用full-drain利用率来冒充
到达窗口压力，同时保留每资源、每seed、队列/就绪等待和窗口末backlog。Hmiss也先逐seed
再均值。light要求0≤p<.50且H/L平均DMR均≤.01；medium要求.50≤p<.80；near要求.80≤p≤1；
后两类H平均DMR在[.01,.80]且每seed至少存在一次ready-node资源等待。全部10seed控制必须
有效且H/低竞争见证满足deadline才可准入。未定数值均须批准；.80 miss上界用于排除接近
全miss，本提案没有把它变成H收益或mapping阈值。样本少时分箱可能拒绝全部配置，这是
预先允许的BLOCKED结局。额外severe-overload仅敏感性，未纳入本版trial。

按每条件A优先、B次之选第一个合格配置，不按miss最低或映射收益最高。一个条件无合格即
全P2 BLOCKED；不重新解释自然不可行/有效负结果、不静默增加试验。合法但不可行试验
可以按已列清单完成用于诊断，但绝不可选作“合理压力且基本可行”的正式条件。
待答：是否批准两个控制、充分/未证明区分、候选负载分箱和A/B选择/停止政策？

## D07 — M1机制观察与M2描述（PROPOSED / UNRESOLVED）

原始问题：M1/M2、可观察量、对照边界、单位、条件/seed分母。
推荐M1作为局部机制证据、M2作为补充描述，两者不能作为候选算法。
SOURCE_SUPPORTED：原始需求§44允许2–4 ready任务的局部枚举diagnostic oracle；
原需求§23禁止未来信息。下述具体目标/截断/记录点都是新增提案。

M1在B2主运行每次公共view刷新、派发调用前记录（包括一次派发后的新view），以
(run_id,decision_seq,public_view_digest)标识，纯重复无状态改变的view只记一次；记录全部
已到达公共图、ready集合、估计、可见running elapsed、已完成数据及闲忙状态。
用既有B2 ready次序前min(4,ready_count)个组成K；K≥2且至少含一个H即eligible，
不因没有替代资源删掉此状态。分母N_cs是该条件/seed主B2的全部eligible独特view数，
另记总view数、截断次数、K分布；N=0是缺乏观察而非机会率0。

固定K和顺序，只枚举兼容mapping（最多6^4=1296），不排列任务顺序。以同一公共估计
busy release=now+max(0,estimate−elapsed)、真实已完成前驱的目的地就绪，串行追加每个
resource上K任务的预计占用，允许预测等待但不执行/不保留资源。基准是同固定序的局部
greedy EFT追加；枚举集合包含此基准。反事实只允许每个L局部预计finish≤基准相应finish，
目标为最小K内H预计finish均值，平局按resource ID元组。不存在未来到达、未ready节点或
后继运行；不会反馈到实际B2调度。这是离线局部比较，非新online policy或真实反事实轨迹。

记b=基准H预计finish均值−now>0，o=可行枚举最优对应值，Δ=b−o≥0（ms），g=Δ/b（无量纲）。
比较使用binary64输入值对应的精确有理数，不加未注册epsilon；枚举的具体传输/预计排队
也用这些公共有理数进行，保持内部基准与反事实完全同一算术。不能声称与浮点runtime
局部预测逐bit相同，未来须报告差异；无真实收益担保。记录最优assignment/基准/约束/
成本/截断，审计者可独立复算。M1只证明当前K/估计/约束下有局部映射余量；看不到尚未
ready的稀缺H需求，估计误差和选择B2轨迹都限制解释。

辅助离线trace描述：逐服务以最长实际依赖/通信路径标识H critical path（同长按node ID），
逐节点记录CPU/GPU/NPU等待、完成前驱后data-ready等待、实际资源/兼容数、替代预计代价，
单位ms/计数，参考trace与公共view。完成后的关键路径不能喂给scheduler或用于调选trial。
具体定义为：dep=max(arrival,各前驱finish)，data=max(arrival,各前驱finish+实际目的地delay)，
data_wait=data−dep，post_wait=start−data；assigned_busy_wait为[data,start)内已分配单元
被其他节点占用的区间测度，policy_idle_wait=post_wait−assigned_busy_wait，均ms且不重叠。
post_wait包含策略选择的空闲等待，不能全称为物理资源阻塞。CPU/GPU/NPU等待分项按实际
目的单元类型累加assigned_busy_wait，逐服务分母为1、跨服务分母为该组50，注明node-ms求和
可能在并行分支上重叠。关键路径采用node权重duration+post_wait、edge权重实际delay，根从
arrival起，最长路径长度应等于服务response；同长按完整node-ID路径字典序。H critical-path
blocking为这条事后路径的assigned_busy_wait之和(ms)，另报policy_idle_wait/compute/transfer，
不得与全图节点wait和混为同一个端到端分解。每次实际start同时引用最近公共view，记录
compatible数以及每个替代资源的预测EFT−实际所选资源在同view的预测EFT（ms，可为负；无
替代记NONE），不拿私有真值比较替代资源。以上恒等式/区间测度需未来独立复算验证。

M2用同workload的B1/B3/B4/B5逐一配对B2；每seed/condition报告H-DMR差（比例点）、
L-P95差(ms)、每服务资源等待均值差(ms)、M1机会率及eligible数（只B2）和兼容性分布。
主服务分母每类50；控制不混入；实际trace等待分解须先验证恒等式，零/缺失不可编0。
可用既有paired-seed CI，不能按100个服务或数千view重采样。B3/B4或B2/B5同时改变
ordering/lookahead/mapping，M2**不能单独支持映射独立因果贡献**，也不替代P3 A3–A1检验。
待答：是否批准K/截断/基准/局部L约束/目标、分母及M1+M2解释边界？

## D08 — 三态判据（PROPOSED / UNRESOLVED）

原始问题：可观察量聚合、稳定性、不确定性、三态条件、无效/缺失处理。
完整三态表、两套有限候选和精确边界在 `P2_mapping_opportunity_decision_table_v1.md`。
推荐讨论FINE方案，理由为不要求5%局部估计收益才能观察弱机会；这不是来源证明，也不能
保证稳健。COARSE更保守；两者必须**在看结果前二选一**，不能逐结果挑最容易通过者。
tau/frequency/stability及bootstrap实现pin全部UNRESOLVED，32组参数登记中单列。
所有既有H/L、P3 mapping阈值和CI算法保持原件不变；不把统计门槛从它们挪来。
任何方案通过只能支持所定义局部机会，不等于H收益/L合规/候选成功。待答：选FINE、COARSE，
还是拒绝并给另一套完整规则？批准条件覆盖/缺失/稳定性/paired-seed实现pin吗？

## D09 — 唯一runner与恢复（PROPOSED / UNRESOLVED）

原始问题：唯一入口或同守卫薄launcher，身份/源码/恢复/重试/退出等。
推荐扩展现有 `scripts/run_pipeline.py --stage calibration` 为未来唯一正式入口；
完整比较、复用等值条件、状态机、attempt链和洁净策略在 `P2_runner_schema_review_v1.md`。
此命令仅为未来接口定位，本轮没调用。R2可作为无独立权力的薄launcher，当前不需要。
自动重试预算0；不完整不续写、重新执行必须新的审批和新attempt而不能救统计结果。
P2相关源码/配置已提交且洁净是新增工程推荐，**不是现行已批准P2规则**；现合同明确强制
洁净的是precheck/validation/formal。待答：是否批准R1、精确复用、零自动重试和P2洁净政策？

## D10 — 科学schema/adapter（PROPOSED / UNRESOLVED）

原始问题：envelope或新版本schema+adapter，以及血缘、COMPLETE、P1兼容。
推荐S2新scientific v1+显式adapter，理由为现代码硬编码fixture origin，外包envelope本身
无法证明科学来源。S1保留为经未来兼容性证据支持的备选。本版给完整规范字段表和不变量，
不修改现有schema草案/模型、engine或validator。见 `P2_runner_schema_review_v1.md` D10。
static字段/规范检查不等于运行时hash/血缘/恢复已验证；科学输入原始字节、generator出生
证明和P1负例回归都需未来实现验证。待答：是否批准S2、ID/canonicalization/引用规范及
COMPLETE必须同时成立的条件？

## 跨决策一致性、已知风险与停止

| 核对项 | 结论/仍待验证 |
|---|---|
| D01↔D02身份 | 六模板角色均存在profile；所有节点兼容集非空；两尺寸比例明确，未来实例ID须唯一 |
| D01↔D03 | 六模板前驱与74边一一对应；9类型对完整；单位同引擎，未生成网络实例 |
| D04↔D10 hash | 参数精确有理身份与运行binary64 payload分开hash；控制变体不同hash但扰动key保留；无自引用hash |
| D05 seeds/budget | 只引用既有10 CALIBRATION值；36配置/18条件/2520条/1080输入；5040含重放；无新seed |
| D06公平性 | B2和独占见证决定选型；不按候选/机会结果挑选；独占miss不冒充不可行证明 |
| D07↔D08 | per-seed机会率、共同重采样索引；非节点/view独立CI，全部12 loaded条件检查 |
| D09↔D10复用 | 全语义身份及raw refs/hash/validator/metrics/replay/COMPLETE核对；receipt不增样本 |
| P1隔离 | 旧origin拒绝当前科学输入；S2未实现；P1字节/测试/审计不改，不能改标签充样本 |
| 封存 | 不创建unlock、不生成非calibration realization/outcome；元数据校验不是访问结果 |
| 设计≠证据 | B1–B3仍UNRESOLVED；B4/B5仍DESIGNED_UNAPPROVED，代码/行为与科学检验均待做 |

明确保留的冲突/不足：旧draft矩阵与schema只是历史选项；本v1是它们的**具体提案层**，
未取代生效文件。旧schema缺开始/结束与COMPLETE行为，本版补设计，未修实现。现P1
硬编码origin与科学读取不兼容，须先S2及P1回归，不能直接运行。source代码/配置哈希为
P1已验证身份；任何未来adapter会改变它，必须重新验证，不继承当前PASS作为新代码保证。
timing不在本矩阵，不能宣称P2所有未来输出均已可冻结。多条件CI为pointwise，三态表没有
同时置信覆盖保证。FUSION/硬兼容/合成speedup和固定突发都可能人为塑造机会。

`P2_scientific_parameter_registry_v1.json` 枚举**32个未批准科学参数组**（不是32个标量或
10个决定）；全部有明确提案或有限选项，批准值仍null。工程runner/schema另由D09/D10
审批，不混计科学参数。D01–D10提案覆盖完整不等于已解决：resolved=0、human=10。
人工应在v1 checklist逐项选择并记录版本/文件hash/批准值或修改意见，不能仅回答“同意P2”。
随后只能启动另行授权的实现验证任务；P2保持BLOCKED，当前science=0，STOP=YES。

# P2-B1：逐字段规格缺口

全部方案为 `PROPOSED_REQUIRES_APPROVAL`，所有未确定的数值均 `UNRESOLVED`。
依据 E01–E08（见 evidence_and_traceability.md）。表中没有隐藏的默认分布、比例或边界。

| 字段 | 已有约束 | 未知值/规则 | 可考虑选项（不选定数值） | 决定 |
|---|---|---|---|---|
| COCKPIT 模板 | 包含 speech/display/navigation/interaction | 各角色节点数、边、并行/汇合、业务实例组成 | 显式列举的角色化 DAG；或批准确定性 DAG grammar | D01 |
| ADAS 模板 | preprocessing/perception/fusion/output | 同上，无真实车辆 profile | 显式角色化 DAG；或批准 grammar，不假称硬件测量 | D01 |
| FUSION 模板 | cockpit+ADAS 共享加速器产生跨业务竞争 | 两族如何组合、业务混合/H-L 归属、实例角色 | 明确列举两族共享资源的组成；或注册组合 grammar | D01 |
| 8/16 节点定义 | 每服务恰好 8/16 个可执行节点；无隐藏 dummy | 每个尺寸实际 node/edge 清单，大小变化怎样保持语义 | 两份独立明列模板；或审批角色细分变换且证明节点计数 | D01 |
| 兼容集合 | CPU-only/GPU-oriented/NPU-oriented/multi-compatible/limited-alternative 均须覆盖，非全兼容 | 每角色/节点的合法单元；类型出现频率 UNRESOLVED | 显式 per-node 集合；或预先审定角色到集合的确定性表 | D02 |
| 计算估计 | 各兼容单元正且有限；四 CPU+GPU+NPU | 估计表值、CPU 核间关系、跨资源差异来源 | 合法来源的可追踪 profile 表；或经批准的合成参数表/生成规则 | D02 |
| 实际执行时长 | 正且有限，不能给 scheduler；方法无关 | 实际值怎样由估计/扰动得到，单位/舍入/版本 | 已授权实际时长表的键控查表；或冻结 PRNG 的键控物化规则 | D02、D04 |
| 边大小 | MiB、非负、前驱输出依赖 | 每条边数值或生成规则 UNRESOLVED | 显式边表；或有来源且参数已批准的角色对映射 | D03 |
| 网络参数 | ms、MiB/ms；same-unit=0；cross latency+size/bandwidth；九个 directed type pair | 各 latency/bandwidth 值、来源 UNRESOLVED | 明列 type-pair 参数表；或有出处的测量/公开 profile 表 | D03 |
| 副本/重映射/竞争 | 目的地副本保留；重新映射重算 readiness；无共享总线竞争；允许 compute/transfer overlap | 物化/记录格式待实现，语义本身已定 | 直接沿用模型；共享总线不是本轮可选主模型 | D03、D10 |
| 扰动独立性 | keyed(seed,service,node,resource,disturbance-version)，不依赖调度调用次数 | PRNG/映射算法、参数、正值保障、序列化/舍入 UNRESOLVED | 冻结带版本 PRNG+键编码；或审批表驱动 keyed lookup；不借此新增 seed 身份 | D04 |
| 到达过程 | 在线，只暴露已到达业务；可校准 intensity/burst | 过程种类、参数、H/L 组成与关联、burst 构造 UNRESOLVED | 注册的确定性时序；或由现有 calibration seed 决定的到达/突发过程 | D04 |
| Deadline | absolute=arrival+relative，relative>0，equality on-time | 每业务基值、tightness 轴/值、与路径代价关系 UNRESOLVED | 明列 service-relative 表；或先审批可审计路径规则，禁止事后追随结果改写 | D04、D06 |
| 观察窗口/服务数 | 停止到达后排空所有已到达工作，miss 不删除 | 有限 arrival horizon/服务实例数、停止边界、具体值 UNRESOLVED | 批准有限时间窗；或有限服务实例清单，两者均保留 full drain | D04 |
| H 先行可行性 | 先在独占或低竞争下确认基本可行 | 选择独占/低竞争的对照、方法、条件和可行判定 UNRESOLVED | 独占逐业务核对；或明确定义的低竞争基线输入，不使用候选方法 | D06 |
| 负载命名 | light/medium/near-saturation；按 CPU/GPU/NPU pressure，非 arrival rate 单独命名 | 具体压力度量、分档边界、可接受 miss 范围 UNRESOLVED | 用既有 busy/utilization 与服务 miss 描述，再预先批准分类规则；不能看结果才定义边界 | D06 |
| 科学输入身份 | scene/load/size/seed/generator/config/workload SHA；所有方法同一物化输入 | 科学 origin、ID 编码、hash canonicalization、文件组织与证明链待审批 | 版本化科学 envelope（见 schema 草案）；不得从 P1 fixture 改标签 | D10 |

**条件性建议，不是决定：**优先考虑显式模板、显式参数表和固定键编码，因为便于人工
审查、逐版本比较。代价是模板覆盖范围有限，并可能人为放大稀缺资源竞争；必须公开来源与
选择理由，不能假称代表真实车辆。Grammar 可扩大覆盖，但参数自由度与选择偏差更大，
需要在任何观察前冻结完整规则。当前没有证据推荐具体模板、参数值或概率分布。

关闭证据：人工批准上述字段的完整定义/值及来源；有限配置可展开；另行授权的实现通过
模板计数、DAG、兼容、正值、因果、扰动独立、确定性和身份/哈希验证。随后实际 H 可行性
仍需在未来执行中核验，文档批准不能冒充可行性结果。

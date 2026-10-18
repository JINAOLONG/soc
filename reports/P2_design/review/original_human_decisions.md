# 人工决定清单：十个决定组，均未答复/未批准

类别：**S**=SOURCE_SUPPORTED；**P**=PROPOSED_REQUIRES_APPROVAL；
**U**=UNRESOLVED_BLOCKING；**V**=IMPLEMENTATION_VALIDATION_PENDING；
**X**=SCIENTIFIC_EXECUTION_PENDING。人工批准 P 不替代补齐 U，也不替代 V 或 X。
来源 E 编号见 evidence_and_traceability.md；选项详情见 blocker_decisions.md。

1. **D01（B1，E01/E02/E03；P/U）**：三场景采用显式角色 DAG，还是确定性 grammar？
   请给每场景 8/16 节点的完整拓扑、角色/H-L 归属及尺寸变换定义。明确节点/边计数，
   不得引入隐藏 dummy。推荐先审显式模板的可追踪性，不推荐任何未有来源的拓扑值。
2. **D02（B1，E02/E03；P/U）**：兼容集合与各资源估计/实际执行成本采用可追踪 profile
   表，还是批准的合成参数规则？请给各角色/节点集合、代价值或全部参数及来源、正值保障。
   固定六资源与兼容类型覆盖为 S；具体值/类型频率为 U。
3. **D03（B1，E02/E03；P/U）**：采用何种有出处的边数据表及 type-pair 网络参数表？
   请给数据 MiB、时延 ms、带宽 MiB/ms 下全部值/来源。same-unit=0、无共享总线竞争、目的地副本与
   remapping 语义是 S，不再投票；表值是 U。
4. **D04（B1，E01/E02/E03/E08；P/U）**：批准哪种 keyed 扰动/到达物化方式？
   请给 PRNG/键编码/舍入/版本、分布及参数、到达/突发过程、H-L 组成、relative deadline
   构造、服务数或 arrival window 与停止边界。完全排空是 S；不能只批准“用随机扰动”。
5. **D05（B2，E01/E02/E04/E08；P/U）**：校准采用完整显式 trial 列表，还是有限轴展开？
   请给各轴全部合法值、每 trial 的 B1–B5 方法子集及理由、B2 焦点角色、顺序/预算，以及
   十个已登记 seed 到每 config/condition/workload 的精确映射；不能把 18 条件当完整列表。
6. **D06（B1/B2，E01/E02/E05/E06；P/U）**：H 独占还是明定低竞争对照？请给可行性、
   pressure/miss 负载分类、最终配置选择与确定性平局规则，以及合法但不合目标、天然
   不可行、invalid/failed/incomplete 的分类/继续/停止规则。所有结果保留是 S；不填阈值
   或“看结果再定”不能解阻；不允许 candidate advantage 参与选择。
7. **D07（B3，E01/E03/E04/E07；P/U）**：采用 M1 同状态机制诊断、M2 基线配对描述，
   或明定的组合？请给机会观察量、合法比较/反事实的控制/视窗、信息边界、记录单位及
   每 seed/condition 分母/summary。M2 存在排序与映射混杂，不能单独作 mapping 因果结论。
8. **D08（B3，E05/E06/E07；P/U）**：机会判据如何聚合条件/seed、定义稳定性与不确定性，
   并区分 SUPPORTED、NOT_SUPPORTED、INCONCLUSIVE？请填全部判定参数、足够证据和
   无效/缺失处置。若用 CI，沿用既有 paired-seed 方法；不能新设 CI 方法或挪用 H/L 门槛。
9. **D09（B4，E07/E09/E11/E14；P）**：批准唯一正式 calibration runner 扩展，还是共用
   同一守卫的薄 launcher？是否采纳完成产物身份/hash 全匹配才复用、失败/不完整默认
   停止且无自动 retry 的提案？另请明确 P2 源码 dirty 的允许/洁净控制。更严格洁净建议
   不是现行普遍 P2 规则；任何 retry 必须事先登记条件/预算/attempt 链。
10. **D10（B5，E03/E07/E10/E11；P）**：科学身份采用经可行性验证的 envelope，还是
    新版本 scientific schema+adapter？请批准 namespace、canonicalization、workload/run/
    attempt ID、必填字段、provenance/ref 规则与 P1 兼容测试范围。拒绝 fixture 改标签是 S；
    当前 schema 仅为 DRAFT，JSON parse 不等于 V 通过。

**V（后续实现验证，不是本轮人工文字可替代）：**生成器、有限矩阵编译、seed 隔离、
validator/metric/replay、恢复/损坏/幂等、schema 血缘和旧 P1 回归的测试与审计。
**X（后续科学执行）：**实际 H 可行性、负载分类、映射机会稳定性、各 trial 全部完整结果。
这些任务均需另行授权。本轮不会因任何一项建议写下“推荐”就自动冻结、实现或执行。

原有工程 timing 协议仍 NOT_FROZEN；上述 D05 若包括 runtime/timing 工作，还须提交
inputs/warmup/repetitions/timer/aggregation 的完整登记，不能从当前草案推断默认值。
此提醒不新增决定编号，不改变既有 2ms 目标。

# P2-B4/B5：未来科学 runner 与产物设计（DRAFT，未实现）

依据 E03、E06–E11、E14。当前 calibration 入口未实现；下述均为提案，不是接口已存在
或科学运行已获准的声明。执行命令留为 null；本轮不调用 P2，不新增 Python/实现文件。

## R1 / R2 与入口防线（D09 待批）

建议 R1：在另行授权任务中扩展唯一正式 calibration 入口，读取批准的完整执行 manifest；
R2 是薄 launcher 调用同一守卫的替代，不可独立绕过门禁。未来入口应依次验证：

1. 实际 repo/branch/source/config/test 身份与已批准 plan/hash；P0/P1 真实门禁及原文可读。
2. 草案已通过明确审批且全部字段已解析，没有 DRAFT/NON_EXECUTABLE/null 必填项。
3. 每个 workload seed 属于已提交 CALIBRATION allowlist，实际值不来自自由命令行替代；
   所有分区 realization/outcome 的访问仅限明确的 calibration 路径。
4. 已批准 generator/template/扰动版本与有限 trial/config/condition/method 清单；禁止候选。
5. 新 schema、内容哈希与物化 lineage 已通过单测；同 workload hash 被所有方法共用。

source Git commit 与 dirty status 必须实记。建议进一步要求 P2 执行前 relevant source/config
洁净并已提交，以降低复现歧义；这是**待批工程控制**，现行合同明确强制洁净的阶段是
precheck/validation/formal，不能谎称当前已普遍强制 P2 洁净。若允许 calibration dirty，
则必须明确可解释变更和可恢复字节身份，不准只记父 commit 冒充实际代码。

## 建议状态机（未批准）

计划身份校验 → 物化不可变输入 → 保存准备记录 → 调用引擎 → 保存真实进程结果 →
独立 trace 验证 → 独立指标复算 → 确定性重放 → 完整产物提交。
任何一步失败/损坏/身份不符均停止相关运行、保存状态及原始日志，不写 COMPLETE。
工作负载内容身份必须独立于 method；run identity 可包括 method，attempt identity 另记。
具体 ID 编码/哈希规范由 D10 批准，不在此按时间或随机数生成实际 ID。

| 情况 | 已有要求 / 建议处置 | 尚需批准/验证 |
|---|---|---|
| 未调用进程或 spawn 失败 | 没有实际 exit code；用未启动/启动错误及异常原文表示，绝不补 0 | schema 的错误分类和字段，D09/D10 |
| 进程非零或输出残缺 | 留 stdout/stderr、exit、半成品清单；停止，不能算 valid | 原子完成标记/中断恢复测试 |
| trace 非法、引擎与 validator 不符 | 用户已要求立即停止受影响实验；保留全部证据，单独修复任务 | 不允许实验中修改 simulator/scheduler 来补救 |
| H 天然不可行 | 与引擎错误/算法 failure 分开；保留 feasibility 结果 | 判定与后续 trial 允许范围由 D06 批准 |
| 合法但校准未达目标 | 仍保留运行，不删不利 seed/条件 | 是否继续剩余已列 trial 与最终配置选择由 D06 明确 |
| 完全相同且已完成的输出存在 | 建议精确校验所有身份/hash/有效性后复用，并记 reuse receipt，不能增加样本数 | D09；恢复测试验证，不默认再次运行 |
| 同 run identity 内容不同/重复输出 | fail closed，保留冲突；不覆盖旧文件或“取最新” | 冲突诊断与禁止覆盖测试 |
| 不完整/失败运行存在 | 建议默认停止、不自动续写/重试；缺恢复规则时不得重跑 | 若批准 retry，先给触发条件、预算、new attempt ID、supersedes 链，不能看结果加次数 |

阶段终结只按批准 plan 检查完整 expected identity 集：missing/mismatch/duplicate/
unexpected seed/method/condition 均不得被忽略。P2_mapping_opportunity.json 未来只能由
已批准判据及完整证据决定；不因空列表或 parser 成功而 PASS。不自动调用 P3。

## 科学产物设计与 P1 兼容（D10 待批）

`scientific_artifacts.schema.draft.json` 是拟议的结构约束，不是已批准/已验证 schema，
也没有创建科学实例。它包括 workload identity、run、lineage、invocation、validation、
metrics derivation、raw references、completion/error。所有实际参数/路径/哈希未来才产生。

S1 envelope：保留旧 P1 payload 与标签，增加独立科学 envelope 和 generator 出生证明。
但当前 engine/schema/validator 写死 fixture origin，envelope 是否足以避免语义冲突
尚 UNVERIFIED；不能因外面包一个 scientific 标签就当科学数据。
S2 新版本 schema：独立 scientific input/trace family 与显式 adapter，旧 P1 身份和字节
保持。语义清晰，但需未来授权的接口扩展、P1 新回归与新的来源冻结。当前未选 S1/S2。

两条路线均必须满足：

- Workload 由批准的 generator commit/config/template 与现有 calibration seed 物化，
  保存 generation command/真实 exit/输出 hash，不能引用 P1 fixture 的生成名义。
- 强制 generator lineage 与 plan-approved ID 联合核查；仅 origin 字符串、输入格式相同、
  hash 不同或登记 JSON 通过均不足以证明科学来源。
- 旧 fixture 的已登记路径/内容/血缘不得重新作为科学样本；改变 scene/seed/origin 标签
  不会消除该事实。若内容碰巧相同，也需可独立验证的真实生成过程，不能通过改 label 得到。
- 科学输入与离线完整真值只能给引擎/validator；scheduler 仍只有既有 immutable view。
- 每份 raw 输入/trace/stdout/stderr/validation/metrics 引用有 path、hash、实际大小及类型；
  stage 汇总引用 exact run identity、source/model/config/input、seed/condition/method。
- Metrics record 同时引用 runtime 结果、独立复算结果、协议/计算实现身份；invalid 或
  未复算不能成为 usable sample。完整性状态与机会/收益结论分开。

## 未来验证范围，当前均 IMPLEMENTATION_VALIDATION_PENDING

结构：字段类型、required、schema 版本与 reference；语义：允许 seed/模板/方法/条件、
时间单位、正值/兼容/DAG、文件引用、真实哈希和来源；执行：中断、spawn 错误、非零、
重复/损坏/缺失、幂等复用、禁止重试；科学身份：拒绝 fixture 改标签、伪造 seed、无
generator 证据、跨方法不同输入；回归：旧 P0/P1 原始文件不改，批准适配器不泄漏未来信息。
之后还需要未来科学 execution 验证真实 plan 与完整输出吻合。本轮只做文档一致性和
JSON 结构审阅，绝不宣称以上行为验证通过。

# P2 设计决定包：DRAFT，未批准、未冻结、不可执行

本包是对既有 P2-B1–P2-B5 的文档性设计分析，不替代已批准模型、基线、指标或统计协议。
本轮授权原文为 authorization_request.txt。P0/P1 仍 PASS；P2 preflight 仍 BLOCKED。
没有生成工作负载、运行 P2、计算映射机会或改动任何实现。

阅读顺序：

1. evidence_and_traceability.md：已有依据、原始证据可恢复性和需求追踪。
2. blocker_decisions.md：逐个阻断的事实、选项、风险、建议与关闭证据。
3. workload_gaps.md：科学工作负载逐字段缺口及可考虑的替代方案。
4. calibration_options.md、calibration_matrix.draft.json：选项及有明确 null/UNRESOLVED 的 NON_EXECUTABLE 矩阵。
5. mapping_criterion_options.md：映射机会定义的备选方案及未决定的判定规则。
6. runner_and_schema.md、scientific_artifacts.schema.draft.json：未来 runner 和科学产物设计。
7. human_decisions.md：复用原文件作为完整十二字段决策说明（等价于
   P2_D01_D10_human_decision_brief.md），保留原清单原文。每组须补齐值/规则，
   不能仅回答“同意开展 P2”。P2_D01_D10_traceability.csv 提供逐来源行追踪；
   P2_decision_dependency_map.md 说明依赖与可并行讨论项；
   P2_human_approval_checklist.md 分开记录批准/拒绝/暂缓/待补证据，均不预选。
8. ../../reports/P2_design/design_status.json 与 delivery_index.json：机器状态与交付索引。

本包用以下类别区分陈述：`SOURCE_SUPPORTED` 已有协议明确；`PROPOSED_REQUIRES_APPROVAL`
是本次建议；`UNRESOLVED_BLOCKING` 缺定义；`IMPLEMENTATION_VALIDATION_PENDING` 是未来
实现与测试；`SCIENTIFIC_EXECUTION_PENDING` 是未来科学观察。存在 JSON/文档不意味着已批准，
JSON 可解析也不证明 schema 正确。未提供数值的科学字段一律为 null/UNRESOLVED，无隐式默认值。

人工决定并登记具体定义后，仍须另行授权实现、验证以及最终执行；本包不批准任何这些步骤。
后续必须保持既有 seed、H/L 门槛、CI 方法、B1–B5 编号和信息边界。若拟议方案需要改变
这些固定规则，应拒绝该方案或停下来单独处理冲突，不能把批准草案解释为批准变更冻结规则。

当前结论：B1/B2/B3 的科学定义仍 UNRESOLVED；B4/B5 已有 **未批准的文档设计**，可标为
DESIGNED，但依然没有实现、语义验证或执行准入。历史 P2 gate 继续为 BLOCKED。

## Complete proposal v1（当前人工审批层）

本轮授权已允许提出具体合成值；旧“无数值/不推荐数值”的段落描述此前审查范围，
不是对本轮提案的禁止。入口为[P2_complete_design_proposal_v1.md](P2_complete_design_proposal_v1.md)。
新增六模板/profile/通信/generation/2520条matrix及三态/runner-schema/approval材料，
完整路径见reports/P2_design/delivery_index.json。32个科学参数组全部未批准，D01–D10
仍待人工决定。v1不取代原模型/基线/指标/统计规格，也没有成为可执行配置。
旧matrix/schema保留为历史选项，当前具体提议由v1索引明确关联；DRAFT不是scientific PASS。

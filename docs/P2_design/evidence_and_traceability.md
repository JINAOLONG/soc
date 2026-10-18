# 证据登记与追踪矩阵

以下引用均针对起始提交 d016ad8d8b2be6fbeb80fadfee6194d9aa9bd0ae。旧文件不改，
因此行号/节号保持可追踪；repository_audit.json 绑定实际文件 SHA-256。

| 引用 | 实际文件与位置 | 已确立的事实 |
|---|---|---|
| E01 | docs/user_request.txt §§17–25、33–37、41–42 | 服务/DAG、六个资源、非抢占、在线边界、通信、排空；三场景与 8/16 节点；baseline-only/B2 焦点；H 低竞争可行性先查；同输入用于各方法。 |
| E02 | docs/workload_spec.md:3–25 | 主条件是设计约束，具体代价、兼容、边大小、到达律、deadline 未给；按资源压力标负载，保存所有 trial，P2 后冻结 workload。 |
| E03 | docs/model_spec.md:3–62 | 时间 ms、数据 MiB、带宽 MiB/ms；正时长、DAG 有效；通信目的地副本/重映射；批准的事件顺序；调度器无未来真值；扰动由 seed/service/node/resource/version 确定。 |
| E04 | docs/baseline_spec.md，B1–B5 表及 P1 适配段；docs/P1_decisions.json | 五个正式基线及批准的 D1–D5；B2 是 L 对照。不能新增 CPOP 或把诊断算法变为正式第六基线。 |
| E05 | docs/metric_spec.md:3–52 | 服务级响应/miss，等 deadline 不 miss；type-7 分位数；H/L 已有门槛；能耗可选；host 2ms 目标，计时输入等须先登记。 |
| E06 | docs/statistical_protocol.md:3–16、34–47 | paired seed 为重采样单位、10,000 次、固定分析 seed、type-7 percentile；P2 判据先于诊断选择；科学完整性要求，无不利条件/seed 删减。 |
| E07 | docs/user_request.txt §§32、80、90–92、100 | 手工 mapping 示例仅解释/正确性；P2 产物要求；run manifest 字段与完整性；无稳定映射机会时停止该假设。 |
| E08 | configs/seed_partitions.json，partitions.CALIBRATION；configs/research_protocol.json，main_grid/resources/threshold 字段 | 已提交 calibration 列表十个；其余 seed 无权用于本轮；固定主网格与阈值不能重写。仅核对元数据。 |
| E09 | scripts/run_pipeline.py:26–39；src/soc/workload/__init__.py:1 | calibration 入口没有科学执行实现；没有 workload generator。未调用此入口。 |
| E10 | src/soc/model/schema.py:175–189；src/soc/simulator/engine.py:100–102；src/soc/validation/trace.py:71–79 | 序列化身份限定手工正确性 fixture；现有科学 schema/adapter 不存在。 |
| E11 | src/soc/validation/governance.py:119–145、181–208；src/soc/validation/p1.py，audit_p1 | P0/P1 gate 真实实现；科学阶段 seed 守卫；后续阶段需要 P2_mapping_opportunity.json PASS，但没有科学 P2 判据实现。 |
| E12 | reports/P2_preflight.json，commands；reports/P2_calibration.md，P2-B1–B5；reports/P2_execution_manifest.json | 前次真实 Git/门禁/测试输出已保存；实验参数与命令为 null；工作负载零。 |
| E13 | reports/P2_delivery_index.json、P2_git_checkpoint.json、P2_evidence_checks.json | 旧交付/推送记录及 264 项旧检查快照；当前 P2 清单实际是 266 项，历史数量不冒充当前清单。 |
| E14 | AGENTS.md §§4–15；docs/research_contract.md，P1 handoff annotation 与 progression | 保留历史、状态、禁止科学伪证、不可改冻结规则；历史 DRAFT_P0_BLOCKED 文字不否定实际门禁 PASS。 |

## 原始命令记录恢复情况

P2_preflight.json 的 13 条实际命令、完整 stdout/stderr、退出码均在仓库；没有根据摘要重建。
本轮 repository_audit.json 重新记录只读 Git、旧清单和 P0/P1 check-only 输出。
后者包含 P1 手工 fixture 验证，不是本轮科学样本。

实际检查了 `/tmp/soc-p2-document-checks.json` 与 `/tmp/soc-p2-first-push.json`：
它们均存在，解析后与旧仓库中的对应记录一致，无须重复存两套。另找到实际存在的
`/tmp/soc-p2-final-delivery.json`，按原始字节复制到
reports/P2_design/evidence_recovery/soc-p2-final-delivery.json；实际 SHA-256/大小保存在
repository_audit.json。它补齐前次最终 d016ad8d 推送的原始回执。没有遗失原始记录被虚构补齐。

## 从缺口到未来验证

| 阻断 | 人工决定 | 设计文档 | 实现验证（未执行） | 科学执行证据（未产生） |
|---|---|---|---|---|
| P2-B1 | D01–D04、D06 | workload_gaps.md | 模板/键控扰动/隔离/物化哈希测试；输入身份与兼容正值检查 | 审定输入的 DAG/代价/通信/到达证据、H 可行性 |
| P2-B2 | D05–D06 | calibration_options.md、calibration_matrix.draft.json | 完整 trial 展开、唯一身份、10 个允许 seed、缺失/重复检测 | 全部允许 trial/config/condition/seed/method 结果及失败 |
| P2-B3 | D07–D08 | mapping_criterion_options.md | 人工已知的正/负/不确定/无效诊断例与独立复核 | 判据规定的原始观察与 seed/条件聚合，不是候选胜利 |
| P2-B4 | D09，并依赖 D01–D08 | runner_and_schema.md | 守卫、幂等、损坏、恢复/禁止重试、完整性故障测试 | 真正 invocation/exit/log/trace/validator/replay 记录 |
| P2-B5 | D10，并依赖 D01–D09 | scientific_artifacts.schema.draft.json | schema 正反例、语义/哈希/引用/血缘/标签拒绝测试、P1 不变回归 | 科学 provenance、完整文件链及真实性复核 |

没有一行可以因“草案存在”而转为科学 PASS。后续若批准只涉及部分决定，其他项仍保持阻断。

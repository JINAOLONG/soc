# P2 v2 pre-approval adversarial review v3

**DESIGN_REVIEW_REVISE_REQUIRED**

本轮是同一 Codex 环境内重新开展、分工交叉挑战的对抗性文档审查，不是第三方独立审计。结论针对现有 v2 提案能否完整支持人工批准；不是实验结论，也不是 P2 科学执行失败。没有批准、冻结、实现或执行任何 P2 内容。

## 实际审查对象与授权

仓库 `/workspace/soc`；分支 `work`；origin `https://github.com/JINAOLONG/soc.git`。开始时 HEAD 与实际远端 work 均为 `a3680acf45c5578fc090cf53cc186f28a8e9b88a`，工作树 CLEAN。原始授权逐字保存在 `authorization_request.txt`。`protected_baseline.json` 固定开始时全部 462 个受保护文件的 SHA-256/大小；本轮只在 `reports/P2_design/preapproval_audit_v3/` 新建报告，既有 STATUS、v1/v2、源码、测试、协议、种子与失败历史保持原字节。

P0/P1 原有 PASS 记录与历史证据身份已核对；本轮没有重新运行 P0/P1 gate 或测试。P2 preflight/progression 仍 BLOCKED；B1/B2/B3 UNRESOLVED，B4/B5 DESIGNED_UNAPPROVED 并有下述待修订问题。当前全部 10 个决策、40 组参数仍 UNAPPROVED。旧 STATUS 的 32 组明确属于 v1 历史范围，不能作为当前 v2 数量。

## 五项具体修订问题

| 发现 | 严重性 | 原因、影响及必须明确的内容 |
|---|---|---|
| V3-F01 / M1R-F01 | CRITICAL | ADAS 强制记录的单 ready 状态进入 E、不进入 F，导致全条件阴性要求覆盖率 1 永远无法成立。须联合修订 D07 观察域和 D08 阴性证据政策，明确能支持的命题；不能仅选 FINE/COARSE 或静默删状态。 |
| V3-F02 / ID-R01 | MAJOR | 已有冲突关闭、lease、授权恢复和 CAS 文字，但跨授权替换的共同排他域、失主 fencing 或禁止接管政策、CAS 期望值没有精确定义。锁身份不同不等于已证明运行时重复执行；这是实现前契约缺口。 |
| V3-F03 / ID-R02 | MAJOR | 原始需求及 runner 要求记录实际执行 HEAD/实测 dirty，但闭合类型未规定其必填字段或必须存在的 provenance 收据。冻结 source_commit/dirty_policy 不能代替观测记录。通用 artifact 能承载它，缺的是强制绑定。 |
| V3-F04 / DECISION-M2-COMPLETENESS | MEDIUM | Markdown V 明确要求 M2 配对分析完整，但 criterion/stage 机器先决条件未绑定精确配对报告清单与缺失失败规则。原始单次指标齐全只代表可计算 M2，不代表配对分析已产生。 |
| V3-F05 / ID-R03 | LOW | KEY 和三种 binding 实际均为 14 字段，文案却称 All15。应在另获授权的修订中只更正数量；不得猜测或新增第十五字段。 |

每项包含实际文件 SHA-256、行号/JSON 定位、事实与推导、限定反证和待回答问题，见 `cross_document_findings.json`。这些问题尚未写回 v2。

V3-F01 的推导不依赖任何随机种子取值或观测结果：ADAS 8/16 均仅一个根；首次同刻 H/L 到达只有两个根 ready。一个有效、符合 B2 规则的正时长首次派发后，同刻剩一个 ready 根，H 仍有未开始后继。事件/快照协议要求下次派发前记录该状态，且 running 集变化使其不能按相同公共状态去重。因此每个有效 ADAS 流 E−F≥1；F>0 时 F/E<1，F=0 时先决条件也不满足。全 12 个 loaded 条件的阴性分类要求每个 seed/condition 覆盖率 1，故现行 NOT_SUPPORTED 分支不可达。无效或未完成运行会更早失败关闭，不能挽救该分支。本证明不声称支持覆盖率 4/5 不可达，也未计算实际覆盖率。

## 四项解释或待决事项

- V3-F06 / INFO：固定 suffix 的 FULL 只覆盖当前 K 的枚举空间，可能漏掉 suffix 映射机会。案例 7 以合法公共字段手算：所有 16 个当前 K 映射 g=0，仅调整一个后继映射可改善 H 平均预测完成时间 111/256 ms、相对 gain>1/20。该限制已被 v2 披露，故不是额外阻断；没有声称该手工状态实际出现在 B2/校准中，也不是科学结果或新候选算法。
- V3-F07 / INFO：FINE(1/100,1/100)、COARSE(1/20,1/20)、覆盖率 4/5 与 1、8/10 与 2/10 是待人工选择的科学假设，原始资料没有唯一数值依据。阳性见证和阴性证据要求不同有逻辑理由，但不证明数字有足够功效。按 FULL 状态条件化、同校准样本选配置再解释区间均限制外推；不能写成独立确认。
- V3-F08 / INFO：历史 v1 的 32 组、上一轮 READY 建议/静态检查与当前 v2 的 40 组和本轮 REVISE 结论必须按对象和时间区分。旧记录保留；旧 ACCEPT 不是批准。
- V3-F09 / INFO：timing 仍 NOT_FROZEN。原始 P95≤2 ms 目标保留；精确输入、warmup、重复次数、timer、聚合、P95 定义、host 必须在候选计时前及完整 P2 推进前冻结。没有依据把这一要求扩大成所有实现准备或 baseline-only calibration 前必须冻结；本轮仍无任何实现或执行授权。

配对 seed bootstrap、10000 replicates、分析 seed 20261018、type-7 区间定义原样保留。未计算 bootstrap 索引、置信区间、mapping 分类或任何科学结果。

## 实际矩阵及静态验证

读取并解析完整 `docs/P2_design/v2/P2_trial_matrix_draft_v2.json`：1,327,918 bytes，SHA-256 `b58fe4c2eead01fc9b92966d557ed0bb052e7387794fc0d9b58029ffdb90af0e`。按原始 3×3×2、v1 D05 轴/顺序和已有 CALIBRATION metadata 独立重建预期，没有复用旧检查器或从实际行直接复制预期。

| 检查 | 实际结果 | 限定 |
|---|---|---|
| 矩阵 | 36 配置×11 字段=396 比较；2520 行×20 字段=50400 比较；2520 行 PASS；37 汇总项 PASS，0 FAIL | 包含类型、key、引用、角色、方法、种子、顺序、重复与预算；仅静态一致性。 |
| 角色/预算 | 1800 MAIN、360 H_ISOLATED、360 LOW_COMPETITION；1080 唯一符号输入引用；5040 最大未来 engine calls；自动 retry=0 | 未物化任何输入，未解析成实际科学内容身份；不是本轮调用数。 |
| 选型 | A/B 全保留；只使用 B2 控制与自身负载资格，不能依据候选优势或 M1R/M2 结果选型 | 不证明任一配置实际合格。 |
| 身份 | 47 观察断言 PASS；35 节点/40 边图和独立 21 类 preimage 依赖图无环 | 检查也验证缺口存在，不等于设计通过；18 项未来 runtime tests 均未执行。 |
| M1R | 9 个必查案例齐全；27 来源前提/手算断言 PASS | 不执行诊断器、调度器或模拟器。 |
| 决策追溯 | 10 原始问题与 40 SP 精确匹配；653 必填单元/来源引用检查通过 | 无任何批准。 |
| 仓库 | 15 观察项 PASS；四份旧 manifest 分别核对 122/315/24/120 引用，12 份 v2 JSON 严格解析 | 不替代语义审查或 P0/P1 新运行。 |

最新上述检查实际退出码均为 0。检查计数是不同范围，不能相加宣称科学测试数。命令 `decision-010` 曾因审查读取表达式缺方括号退出 1，`decision-011` 修正后退出 0；原失败输出保留。发现阶段 `/tmp` 广域搜索权限错误和一次报告尚未生成时的读取失败也在命令记录范围说明中保留，不是被审计源码失败。

最终新增报告一致性检查 `final-004`：21 项 PASS、0 FAIL，实际退出码 **2**。其含义是报告完整且保留 CRITICAL 设计问题，因此返回 REVISE；这是本轮报告检查器，绝不是现有 P0/P1/P2 正式门禁。所有最终报告的文件哈希在汇总结束后另行核对。

本轮报告封装过程的失败也完整保留：`final-001` 因 SP27 的 `_json` 单元原先含普通文字而退出 1；仅把该新报告单元改成包含原文摘录的合法 JSON 后，`final-002` 的 653 项核对退出 0。`final-003` 在追加命令后、尚未刷新汇总 ledger 时发现 ledger 哈希过期，退出 1；刷新汇总后 `final-004` 所有完整性项通过。未跳过失败检查、修改原提案或已有审计逻辑。另将本轮 STATUS 引用从越界的 1–66 改为实际 1–56，原文件保持不变。

## 人工裁决与后续边界

可供单项人工裁决：D01、D02、D03、D05、D06，共 5 项。先修订或受修订依赖：D04、D07、D08、D09、D10，共 5 项。全部仍需要人工决策、批准数为 0；40 SP 批准数为 0。完整问题、选项、证据、假设与影响见 `human_decision_packet.md` 和两个 CSV。

建议下一步只授权针对 V3-F01–F05 的文档修订：联合解决观察域/阴性解释，再补锁/恢复、实际执行身份、M2 强制证据和 14 字段文案。不要把本报告当作接受任何新阈值的批准；不应直接开始 P2 或实现 runner。设计修订、人工批准、实现验证、科学执行授权是分别需要满足的事项。

全部必交付物在同一新目录；`review_evidence_manifest.json` 记录本轮文件的实际哈希，排除自身避免自引用。`actual_commands_and_exit_codes.json` 合并实质命令与原始输出；报告最终一致性和发布命令有各自明确范围。发布后实际 SHA/远端/工作树以 Git 实测和交付回执为准，不在报告内伪造自引用提交哈希。

SCIENTIFIC_WORKLOADS_GENERATED=0；SCIENTIFIC_WORKLOADS_RUN=0；NEW_SEEDS_GENERATED=NO；NON_CALIBRATION_REALIZATIONS_ACCESSED=NO；SOURCE_CHANGED=NO；THRESHOLDS_CHANGED=NO；CI_METHOD_CHANGED=NO；SEED_PARTITIONS_CHANGED=NO；VALIDATION_UNLOCKED=NO；FORMAL_UNLOCKED=NO；STOP=YES。

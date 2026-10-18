# P2 前置核验：实验开始前 BLOCKED

P0 与 P1 仍为 PASS；本轮未开始科学校准。用户本轮要求只有现有 P2 规格、实验矩阵、
输入与正式入口均可执行时才能运行；发现缺失时必须在生成科学工作负载前停止。
本报告记录该停止条件，不补写未经批准的实验设计，也不把 P1 手工 fixture 变成 P2 样本。

## 已实际完成的核验

起始 HEAD 为 `5310208b141e66ab6e3e6dbf002d16237e81b9e7`，分支 `work`，
远程为 `https://github.com/JINAOLONG/soc.git`；远端 work 与起始 HEAD 一致，工作树干净。
`d60b94a791580af09fc0b40827eb57de439f1916` 是当前历史中的 P1 实现检查点，
其后的源码、脚本、配置、测试、规格没有改变。

`P2_preflight.json` 保存逐条命令、完整输出与真实退出码：

- P0 正式入口 `--stage p0 --check-only`：退出码 0，PASS。
- P1 正式入口 `--stage p1 --check-only`：退出码 0，PASS。门禁重放的是既有 P1 手工
  正确性 fixture；不计为 P2 校准或科学运行。
- P1 的 122 项核心证据清单：退出码 0，missing=[]、mismatch=[]。
- 现有 64 项测试：退出码 0，全部通过，未改测试或验收条件。
- 六份实际原文 PDF SHA-256 全部吻合，仍为忽略缓存；没有下载或跟踪 PDF。
- 实际 source/config SHA-256 为
  `32860d432e7fef62f03fef64be3118c2ba260de6850d8f88a447fb7589cf412b`，
  与 P1 通过时相同。
- 直接读取已提交 seed 元数据：CALIBRATION 注册数 10，精确列表在 execution manifest 中；
  使用数 0。元数据核对不是读取任何分区的 workload realization/outcome。

## 触发停止的缺口

| ID | 实际证据 | 对执行的影响 / 需要补齐的决定 |
|---|---|---|
| P2-B1 | `docs/workload_spec.md:10–12` 明确 durations、兼容集、边数据量、到达律与 deadline 为 NOT AVAILABLE；`src/soc/workload/__init__.py` 仍仅为未实现声明；configs/calibration 只有 .gitkeep | 缺科学生成器与具体输入定义。须先登记三个场景的 8/16 节点模板、资源代价/兼容性、通信参数、扰动实现、到达/截止期/窗口及 H 基础可行性对照。不能临时填写参数后直接运行。 |
| P2-B2 | 原始要求第 35–37 节只有负载/校准目标和允许调整的参数类别；没有有限的试验列表、参数取值、试验预算、顺序、选择与平局规则、精确方法/条件组合 | 主网格 3×3×2 是研究约束，不是完整校准 trial matrix。需要预先批准实际校准矩阵和基线方法子集；B2 是已有焦点，B1–B5 仅是允许的方法范围。 |
| P2-B3 | `docs/statistical_protocol.md:34–36` 要求先发布稳定 mapping-opportunity 判据；现有材料没有对应可执行定义、阈值/聚合/稳定性规则或 P2 计算门禁 | 不能根据看过的诊断结果补选判据，不能把 H 改善 10% 或 L 1.10 直接当作映射机会判据。须先裁决观察量、比较/反事实方式、跨 seed/条件的稳定性及失败/不确定规则。 |
| P2-B4 | `scripts/run_pipeline.py:34–39` 对 calibration 仅检查 P0 后打印 NOT IMPLEMENTED；无校准执行路径或科学运行/恢复实现 | 不存在可运行的已注册 P2 pipeline。代码中的 return 3 仅是静态检查结果，本轮没有执行该入口，不能记录为实际 P2 退出码。 |
| P2-B5 | `model/schema.py:176–181`、`simulator/engine.py:100`、`validation/trace.py:75` 的输入/输出身份为 HAND_AUTHORED_CORRECTNESS_FIXTURE | 现有 P1 schema 不能被重贴标签冒充科学运行身份。科学物化、run ID/来源、输入/配置哈希与完整性 schema 尚未登记和实现；须在实验前单独处理该基础设施范围。本轮不修改引擎或调度器。 |

这些缺口与历史 `DRAFT_P0_BLOCKED` 状态字符串不同。后者不否定实际 P0 PASS；
本轮阻断依据是具体缺失规格和未实现执行路径。

## 执行计数与结论边界

已冻结可执行 P2 工作负载计划为 **0**，完成 **0**，失败 **0**，非法 P2 trace **0**。
上述零失败不表示有效性通过；P2 trace 验证和科学指标均为 NOT_RUN。
18 个主条件 × 10 个 calibration seed 可形成 180 个条件/seed 标识，但在生成器、
试验参数与对照范围缺失时，不能将其登记为已经批准的 180 个校准工作负载；校准还
可能需要另外明确的 trial/config 与 H 独占可行性检查。

没有运行手工 mapping 示例作为科学证据。原始要求第 32 节明确该示例仅用于
correctness/explanation。没有生成候选方法、H/L 收益结论、mapping 机会数值或图表。
Mapping opportunity 为 NOT_RUN，不能判为 NOT_SUPPORTED；P2 为执行前 BLOCKED，
不是已运行实验后的 FAIL。未发现新的模拟器正确性缺陷。

`P2_mapping_opportunity.json` 是记录上述前置阻断的状态文件，status=BLOCKED；
本轮没有运行或新建正式 P2 判定程序，其进程退出码为 NOT_RUN。未来守卫读取该
状态时仍会失败关闭，不会因本报告解锁 P3。

## 下一安全动作与停止

需要先独立批准并登记：具体科学生成器/校准 trial matrix、稳定映射机会规则及
科学运行 schema/runner 的实现范围。已有负载类别、seed 分区、H/L 门槛、CI 方法、
候选定义和基线比较关系应全部保持。若 P2 要输出未来 candidate 的工程 timing 协议，
还需在计时观察前登记精确 inputs、warmup、repetitions、timer 和 aggregation；
本轮没有自行确定任何数值。

不能用“允许执行 P2”代替缺失实验定义的批准。完成阻断证据的正常提交/推送后停止；
不自动进入 P3。正式 delivery index 指向本轮所有原始核验和元数据文件。

# P2-B2：有限 trial 的逐字段选项（DRAFT）

依据 E01 §§35–37、E02、E04、E06、E08。下述为待批解释，没有选择参数值、方法子集
或样本；机器矩阵所有未知项均显式 UNRESOLVED/null。

| 字段 | 当前已定 | 待决定的选项/缺口 | 可复现性、偏差与所需证据 |
|---|---|---|---|
| 参数轴与合法值 | 可调整 intensity、deadline tightness、burst、service count、window | 哪些轴参与、完整有限值与单位未知；显式 tuple 列表或有限轴表 | 值需有来源/假设标记；事后扩轴会增加选择空间，禁止 |
| 完整试验列表 | 主条件标签 3×3×2 | 全部试验逐行明列，或按批准轴机械展开；不以现有主网格代替 | 前者易人工复查、可能漏项；后者易覆盖核查但会组合膨胀；两者都需完整 list hash |
| 各 trial 的方法 | baseline-only、B2 focal；正式编号 B1–B5 不改 | 全部基线，或观察前给理由的子集；当前不选任何子集 | 全部成本高但减少方法挑选；子集成本低但可能丢失比较信息；缺失方法不得看结果再补 |
| B2 角色 | 负载校准焦点、L 预算参照 | 具体在哪些 feasibility/pressure/selection 步骤用 B2，需逐 trial 指明 | 不能将 candidate 优势或最佳 baseline 的结果用于选择 workload |
| trial 顺序 | 须可复现，不能按有利结果临时改 | 人工预列顺序，或稳定 tuple/ID 排序 | 人工顺序可能编码偏好；ID 顺序也可能相关于参数大小，先声明，不能结果后改 |
| run budget | 必须有限、保存所有尝试 | 逐项总预算及 H-feasibility、diagnostic、replay、批准 attempt 的计数规则未知 | 先展开计划预算并批准，不填写虚假的运行数；重放不增加独立 seed 数 |
| 配置选择 | H 先可行，light 低 miss，其他负载有压力/竞争且非全部 miss；不能按候选优势 | 可考虑“预列顺序首个符合预定要求”或“按预定的已有可行性/pressure/miss 要求匹配”；具体标准未给 | 前者顺序影响大；后者灵活但必须先填完整判据，不能引入未批准新评分/权重 |
| 配置平局 | 运行调度 tie 已批准，但配置选择 tie 未批准 | 预列 trial 优先级，或 canonical config ID | 两者均需先定义编码/顺序并测试；不能套用 scheduler tie 宣称已覆盖配置选择 |
| seed 映射 | 只能使用已提交的十个 CALIBRATION identity，禁止替代/重抽 | 每 config/condition 的完整 seed→workload 映射、与 feasibility 控制的关系未知 | 明确 seed 与 ID/key/version 的作用；每方法必须共用同一物化文件，而非仅 seed 一样 |
| 无效/失败/不完整 | 保留证据，正确性缺陷停止，未经许可不重试 | D06/D09 需区分 spawn/process/trace 错误、天然不可行、合法但离校准目标；明确允许继续剩余预列 trial 的范围 | 不能删掉不利结果或只统计有效子集就宣称完整；原因与影响分开记录 |
| 冻结出口 | P2 后冻结 workload/config，稳定映射机会须先定义 | 哪个 trial/config 被冻、必要全覆盖和判据版本尚未知 | 保存全搜索记录和选择的可审计理由，未观察前不能预测一定能通过 |

推荐最终批准对象为完整有限 trial list 与参数/方法/seed/config 的全部解析结果，
而非“允许做一些校准”。这只是审计组织建议，不批准矩阵、不指定预算，也不新增指标。
若仍有 null，未来 runner 应拒绝作为 executable manifest；若只有空 trial 列表，也
不得以零 missing/failed 伪造科学完成。

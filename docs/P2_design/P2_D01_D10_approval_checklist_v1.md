# D01–D10 v1 approval checklist

DRAFT，全部UNRECORDED。原目录`decisions.draft.json`仍是编号/审批记录的唯一目录；
本表是其v1提案审批视图，不建立第二套编号/审批权。没有预先勾选任何动作。
依据`P2_complete_design_proposal_v1.md` D01–D10及列出的JSON/附件；审批前须记录
本次实际commit与`checkpoints/P2_design_artifact_manifest.json`中对应文件SHA。

| ID | 明确批准 | 拒绝 | 暂缓 | 待补证据 | 必须回答的具体范围（不能只批方向） |
|---|---|---|---|---|---|
| D01 | [ ] | [ ] | [ ] | [ ] | 六个显式8/16模板、全部ID/角色/前驱/H-L继承、二分尺寸/真实内部边；接受合成外部有效性限制吗？ |
| D02 | [ ] | [ ] | [ ] | [ ] | 批准16角色×六资源合成兼容/代价表、CPU对称、半代价及估计/实际两级因子吗？ |
| D03 | [ ] | [ ] | [ ] | [ ] | 批准74条边MiB及9对latency/bandwidth数值吗？同单元零、目的地副本/无总线等已定语义不重批。 |
| D04 | [ ] | [ ] | [ ] | [ ] | 批准SHA256 key/canonical/有理数转换、[.9,1.1)扰动、50×H/L、突发/到达、deadline2.5/4及全窗口规则吗？ |
| D05 | [ ] | [ ] | [ ] | [ ] | 批准A/B周期、36配置、B1–B5、2520 slots/5040含重放调用、控制和顺序；明确本版timing预算0且协议仍未定吗？ |
| D06 | [ ] | [ ] | [ ] | [ ] | 批准H隔离/全低竞争控制、LB与见证区分、候选压力/miss bands、A优先选择及失败停/合法负面保留吗？ |
| D07 | [ ] | [ ] | [ ] | [ ] | 批准B2公共view、固定前4 ready、局部greedy/枚举/L约束/H均值目标、eligible分母及M2非因果解释吗？ |
| D08 | [ ] | [ ] | [ ] | [ ] | 选择FINE还是COARSE（或拒绝并给完整替代）；批准tau/f/k、12条件规则、缺失三态和bootstrap实现pin吗？ |
| D09 | [ ] | [ ] | [ ] | [ ] | 批准R1唯一正式入口、全身份复用、0自动retry、失败停、attempt链/原子发布及新增P2相关源码洁净政策吗？ |
| D10 | [ ] | [ ] | [ ] | [ ] | 批准S2科学schema+adapter、完整字段/ID/规范hash/COMPLETE合取、P1来源隔离和未来验证范围吗？ |

每项动作原始答复需要保存：decision_id、action、selected_option、approved_values（或
逐字段修改）、提案version/commit/文件SHA、reviewer、明确带时区的时间、reason/evidence refs、
依赖决定、影响分析。批准方向却漏数值/规则不能关闭决定；修改后须重出内容hash并核对矩阵。
批准0、拒绝0、暂缓0、待补证据0、未记录10。不得把本文件的“推荐”当作人工答复。

依赖沿用`P2_decision_dependency_map.md`：D01–D04→D05/D06联合→D07→D08；D09/D10联合
依赖全部科学身份/规则。可并行审阅，最终必须一致。参数注册表32个科学参数组目前均
UNRESOLVED/approval=null；工程选择单独在D09/D10，不与科学参数数量混淆。
全部审批之后仍待IMPLEMENTATION_VALIDATION_PENDING，不自动运行P2、不解锁任何保留分区。

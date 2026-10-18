# D08 v2 — proposed three-state decision table

DRAFT / UNAPPROVED / NOT_EVALUATED。精确机器规范为`P2_criterion_spec_v2.json`。
来源：原`docs/statistical_protocol.md:3–16,34–47`及需求§44/§100；新cutoff/coverage均PROPOSED。
本任务没有计算项目的mapping-opportunity结果。

| 参数 | FINE | COARSE | 状态 |
|---|---:|---:|---|
| M1R实质相对预计gain tau | 1/100 | 1/20 | UNAPPROVED，无默认 |
| seed内FULL状态hit频率f | 1/100 | 1/20 | UNAPPROVED |
| 支持稳定seed数 | ≥8/10 | ≥8/10 | UNAPPROVED |
| 阴性稳定seed数 | ≤2/10达到p≥f | 同左 | UNAPPROVED |
| 支持覆盖 | 每个seed/condition F/E≥4/5 | 同左 | 新增UNAPPROVED |
| 阴性覆盖 | 每个seed/condition F/E=1 | 同左 | 新增UNAPPROVED |
| 条件覆盖 | 全部选定12个medium/near条件 | 同左 | 不用宏均值补缺条件 |

E含所有唯一在域状态，包含单ready、截断和估计释放未知的合法覆盖不足；F只含完整FULL。
p=hits/F；E=0或F=0时null，不是0。partial可有辅助投影但不得计hit/率，也不作零。
期望snapshot/事件/记录缺失是INCOMPLETE，错误是真INVALID，二者不能混成合法partial。

先决V：全部2520计划trial完整有效、18条件经固定B2资格选定、全120个seed/loaded-condition
单元配对且E/F>0、所有M1R记录独立核验、无invalid/incomplete、M2配对完整，所有定义在观察前批准。
每条件对10个seed p作注册paired bootstrap，记CI端点L/U及K=#seed(p≥f)。

| 优先级 | 条件 | 分类 | 推进 |
|---:|---|---|---|
| 0 | 没有执行科学判定（当前） | NOT_EVALUATED | BLOCKED |
| 1 | 判定已尝试，V=false或任何coverage<4/5 | INCONCLUSIVE | BLOCKED |
| 2 | V=true，coverage全部≥4/5，每条件L≥f且K≥8 | SUPPORTED | 仍须其余P2前提，不自动PASS |
| 3 | V=true，coverage全部=1，每条件U<f且K≤2 | NOT_SUPPORTED | 保留阴性，停止推进 |
| 4 | 其他全部情况 | INCONCLUSIVE | 不能PASS，不能按结果改规则 |

L=f可支持；U=f不能归阴性；K=7不能支持、K=3不能归阴性。因L≤U、f>0且8>2，支持与阴性
互斥；剩余情况全落INCONCLUSIVE。有partial覆盖时即使FULL子集全零，也不能判NOT_SUPPORTED。
“没有稳定支持”与“证明所有mapping不存在”不同；后者不在本观察器证据能力内。

bootstrap仍为10000次、analysis seed20261018、paired seed、共同索引向量、percentile95%、
type7(.025/.975)。ANALYSIS_INDEX_KEY精确字段为domain/analysis_seed/replicate/position/counter；
domain保持`soc.p2.analysis.bootstrap.v1`。SHA256前64位q，q≥18446744073709551610时counter+1
重取，否则q mod10；每replicate的10个索引在所有方法/条件共用，保存索引/digest。
本轮不生成索引。CI是选中校准配置及FULL状态条件下的pointwise描述，不是独立确认或同时覆盖。

不选择FINE/COARSE：它们的幅度/频率定义各有取舍，原来源不能唯一决定。新增覆盖门槛也无
实测依据，可能造成较多INCONCLUSIVE，必须人工审议。不能用非科学解释例选择阈值。
M1R支持只说明有界公共预测空间中的remaining-H机会，不等于实际H收益、L合规或独立因果贡献。
原10% H、1.10 L、P3 A3–A1及2ms门槛全部保持，不借作机会cutoff。

描述性macro必须报告：每seed先等权平均12个选中loaded条件的p，再跨seed均值；所有bootstrap使用同一索引向量。macro不参与补偿单条件失败。

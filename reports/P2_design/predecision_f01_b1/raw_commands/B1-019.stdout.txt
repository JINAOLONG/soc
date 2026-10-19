# P2 Mapping-opportunity decision table v1

DRAFT / UNAPPROVED / NOT COMPUTED。D07观察按complete proposal同名章节；本文件为D08
具体候选。SOURCE_SUPPORTED：`docs/statistical_protocol.md:3–16,34–47`、
`docs/user_request.txt` §44、§100；源文件没有给出以下机会阈值，不冒充注册值。

## 参数

| 参数 | FINE（建议供讨论） | COARSE（有限替代） | 状态/含义 |
|---|---:|---:|---|
| tau，单view实质预计相对收益 | .01 | .05 | PROPOSED，g≥tau是hit；并非H收益门槛 |
| f，最低hit频率 | .01 | .05 | PROPOSED，每seed/condition p=hits/N，N为D07 eligible view |
| 稳定seed数k | 8/10 | 8/10 | PROPOSED，每条件至少k seed有p≥f |
| 观察范围 | 每个选定medium/near条件，共12 | 同左 | 12范围由注册主条件推导；要求全覆盖为新增提案 |
| 宏聚合 | seed内等权12条件平均，再跨seed平均 | 同左 | 描述用，不补偿任何条件不支持 |
| CI | 每条件p的seed均值及宏均值的95% percentile CI | 同左 | 沿用paired-seed 10,000/type-7/分析seed20261018，不另创算法 |
| 额外最低N | 无 | 无 | 只要求每个seed/condition N>0；小N稳定性/区间限制须报告 |

tau/f/k/覆盖仍UNRESOLVED；FINE能捕捉弱局部机会、也可能使合成微小差异看似实质；
COARSE要求更大的局部收益/频率，保守但可能拒绝弱效应。不存在来源证明哪组正确。
不得运行两套后选通过者；人工必须在任何结果生成前选定一套或拒绝本版。
没有从10% H收益、1.10 L预算、P3 A3–A1 CI>0推导这些参数。

bootstrap具体实现pin为**PROPOSED**：不改变既定resampling方法，只固定索引产生。
对replicate=0..9999、position=0..9，用domain=`soc.p2.analysis.bootstrap.v1`和
analysis_seed（整数）=20261018、replicate/position/counter（整数），依D04的canonical JSON取
SHA-256前8字节q。令limit=floor(2^64/10)*10；q≥limit时counter递增重取，否则index=q mod10。
每replicate的同一10索引向量复用于全部条件、方法和seed配对统计，保存索引文件/digest。
这些是分析索引，不生成/替换workload seed。现统计协议要求pin实现但未指定PRNG；
本实现pin仍待人工批准和未来统计验证，不能假称已有实现完成。

## 决策表

先决V：18条件均有按D06预选的配置；所有2520计划trial完整有效（若提前停止则V=false）；
输入/运行/重放/验证/指标/预选收据身份匹配；每个选定12条件×10seed的M1 N>0、g与hit可
独立复算，全部M2配对完整。不得临时缩条件、删零机会seed或用剩余样本继续。

对每个loaded条件c，定义L_c/U_c为seed机会率均值CI端点，K_c=#seed(p_cs≥f)。
S：**每个**12条件 L_c≥f 且K_c≥8。
N：**每个**12条件 U_c<f 且K_c≤2。
f>0且CI有序，因此S/N不可能同时成立（DERIVED）；出现同时成立为实现/数据错误。

| 优先级 | 条件 | 三态输出 | 协议处置 |
|---:|---|---|---|
| 1 | 设计未批准/未实施/本任务 | INCONCLUSIVE，reason=NOT_RUN | P2 BLOCKED；本文件不创建实际判据结果 |
| 2 | V=false，任何missing/invalid/failed/incomplete或N=0 | INCONCLUSIVE，reason=EVIDENCE_INCOMPLETE | P2 BLOCKED，不把缺失当0或负面机会证据 |
| 3 | V=true，S=true | SUPPORTED | 仅支持所定义局部机制，仍须其他P2冻结/准入条件，不自动进P3 |
| 4 | V=true，N=true | NOT_SUPPORTED | 保留阴性并停止mapping主线，不按结果扩预算 |
| 5 | V=true，S/N都false（混合场景、跨界、seed不稳等） | INCONCLUSIVE | 不能PASS；停止推进，不按观察结果另选阈值 |

临界L=f允许支持，U=f不能归N；K=7不能归S、K=3不能归N。宏均值即使漂亮也不能覆盖
单条件缺口。NOT_SUPPORTED要求明确的低机会证据，不等于“没有通过S”。这套负面边界
和跨条件严格性都是PROPOSED，需批准；其他定义不能默认为同义。

每条件保存10个N/hits/p、CI/seed计数、每view理由/assignment/ref、截断覆盖率、全量
bootstrap索引digest、M2原始配对/描述、条件与宏结果、缺失诊断、选择收据、规则及输入hash。
不做node/view bootstrap、不跨seedpooling、不p值过滤、不改CI。所有CI是pointwise，
12条件共同判断没有同时覆盖保证；本设计的局部预计量不推出实际deadline收益或因果贡献。
本轮不计算上述任何数值，实际gate仍为既有BLOCKED/NOT_RUN。

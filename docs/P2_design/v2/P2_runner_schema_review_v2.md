# D09/D10 v2 — proposed lifecycle, recovery and typed artifacts

DRAFT / UNAPPROVED / IMPLEMENTATION_VALIDATION_PENDING。仅设计，不创建任何科学实例或执行入口。
R1唯一正式runner、S2新scientific family仍是建议，R2薄launcher/S1 envelope是未选替代。
现行P1身份和代码不改。真实字段定义、closed对象与21个preimage在`P2_typed_identity_schema_v2.json`。

## Hash与字段作用域

每个`*_PREIMAGE`的精确字段、类型、required、nullability与namespace是typed schema中的对象；
不得自行加own_id、hash、未来结果或省略字段。ID prefix以preimage_registry为准。
SEMANTIC_CANON_V2处理无float的身份/参数；RUNTIME_CANON_PY312_F64_V2处理运行数值payload。
原始文件另存raw SHA/size；raw与semantic值可以相等但字段和验证责任不能混称。

| 记录 | 在何时已有全部preimage字段 | 禁止依赖 |
|---|---|---|
| Blueprint | 源码实现经另行验证冻结、科学参数明确批准之后，生成之前 | payload、receipt、run/attempt、结果 |
| Symbolic execution plan | Blueprint及批准的完整符号trial/method/observer/statistical定义已知 | resolved输入与任何结果 |
| Execution authorization | 独立明确授权与blueprint/plan/source已知 | 不以文档生成本身充当授权 |
| Input descriptor | blueprint/config/seed/variant已知；control只引用已知MAIN descriptor | parent真实payload或未来run |
| Generation authorization / input lock / generation attempt | 上述descriptor及明确生成授权已知 | 内容hash、workload ID、run锁 |
| Generation receipt | 真实生成过程完成，payload/logs/exact sidecar已有hash | 未来resolution/workload/completion ID |
| Materialized content identity | descriptor+canonical payload及control父content已知 | 自身ID或最终科学envelope |
| Input-resolution receipt | generation receipt、独立输入验证、control父resolution已知 | 未来workload/run ID |
| Workload identity | descriptor+blueprint+materialized content已知，且resolution已核验 | generation时间/attempt/未来run |
| Semantic argv / Run ID | workload ID、plan、source/environment/observer等已知 | attempt ID、输出路径、wall time |
| Attempt ID / run锁 | run ID、明确execution authorization和ordinal1已知 | 实际退出、trace/未来completion |
| Replay ID | primary trace、run/attempt及注册replay协议已知 | 未来replay比较结果 |
| Completion receipt | 全部raw、验证、指标、重放与不含自身的artifact inventory已有hash | 自身receipt/hash或未来stage结论 |

Blueprint的generation/config语义内容不含method/criterion结果，运行计划单独绑定方法与观察器。
source bundle只含已冻结源码/依赖/原模型协议及其source commit，不含blueprint实例/结果/本身的
外层metadata提交hash。实际执行HEAD另实记；不得伪装dirty字节。P2相关源码洁净是新增待批工程规则。

输入验证分两层：resolution前检查raw payload、descriptor、generator receipt、父MAIN和变换，
其报告不得引用未来workload/envelope；resolution后才发布workload ID和scientific envelope，
pre-invocation再次验证完整血缘。这样不通过“先要科学envelope才能验证输入”制造新循环。

Workload语义ID不含generation时间/receipt attempt，重建相同语义内容不因此改变内容身份。
但不能用新birth receipt覆盖旧run所引用的原始raw refs；复用必须核验原complete bundle。
旧refs丢失/不同不能因新内容相似就修补成COMPLETE，须保留冲突并闭锁。

## 确切操作顺序与先决条件

1. 拒绝DRAFT、未批准决定、未知source、非CALIBRATION seed或未授权生成。此时允许合法的符号wlref，
   不要求未来payload hash。当前文件就是DRAFT，因此不具备通过该守卫的资格。
2. 用已知blueprint/descriptor/generation authorization取得input锁和generation attempt1。
3. 每config/seed先物化MAIN并保存真实过程/精确sidecar；独立验证，形成MAIN resolution。
4. 从该MAIN派生两个control，同位保留数值/身份，不重新draw；分别保存和核验独立resolution。
5. 发布resolved workload ID及科学envelope；形成semantic argv、run ID、attempt1、run锁。
6. pre-invocation要求所有resolved hash、source/approval/seed/plan/variant/lineage符合，拒绝未解析wlref。
7. 实际引擎顺序仍按矩阵：H-only B2、LOW B2、MAIN B1..B5。物化MAIN不等于先执行MAIN。
8. 保存raw process/code/logs/trace，独立trace验证与指标复算，执行一次注册replay并逐项比较。
9. 所有COMPLETE合取满足才原子发布trial completion。先close/fsync数据及父目录，再发布immutable
   receipt，最后CAS更新完成指针；artifact inventory不含自身或未来receipt，不覆盖旧文件。
10. 全2520完整证据后先做B2-only资格/选择，保存全部A/B记录；之后做M1R/M2及D08分类，再写分离
    stage状态和P2 gate出口。任何结果不能反向改input、选择或判据。

hash依赖和授权/可用性依赖分开标记：resolution必须先核验才能发布workload ID，但workload
语义preimage无需包含带时间的receipt hash。报告DAG展示两条variant分支的合并；MAIN不需要
control resolution。所有instance源hash/命令/日志未来才产生，未实现值在本版没有伪造实例。

## Invocation与attempt

未来拟议worker接口`python -m soc.execution_worker_v2`尚不存在，不能调用。本设计仅登记角色、
method、workload、source和semantic options；actual input/output paths按已知ID在批准CALIBRATION
根内确定性渲染。RUN只hash semantic argv；actual argv包含已算出的attempt路径并逐字保存，
pre-invocation验证渲染完全符合模板。不得把任意flag列入“忽略字段”，不能把actual argv反向放进run ID。

attempt ID由run_id、execution_authorization_sha、ordinal1得到；run锁含run/attempt均已知。
replay是同trial的注册子执行，单独ID/过程/日志，不产生第二科学样本，也不是失败重试。
当前无ordinal>1或额外retry授权。source/参数变了必须另审plan与身份，禁止静默混样本。

PROCESS_RESULT明确process_started、actual exit或null、termination、signal/exception、planned/start/end
UTC与monotonic elapsed、actual argv/cwd/host及raw stdout/stderr。spawn失败start/exit=null；
进程开始但中断未收集exit也为null，不能补0。墙钟异常单独记录，不改变虚拟时间。

## 中断与幂等恢复

| 中断点 | 必须保留 | 允许的幂等动作 / 禁止动作 |
|---|---|---|
| Blueprint/authorization未通过 | 拒绝原因与所见hash | 只读复查；不得生成、取得运行身份或伪造批准 |
| 输入锁/GEN PREPARED后未启动 | owner/lease/attempt收据、process_started=false | 检查lease，显式授权才释放/归档；不自动重启过程 |
| 生成中或payload缺receipt | 部分payload/log/实际退出 | INCOMPLETE/FAILED停；不覆盖、删残件或追加draw |
| payload/GEN receipt完整，resolution未成 | 完整immutable bytes、原验证进度 | 可核验已有材料；不得假造验证PASS。若需恢复验证/发布，先明确授权、仅新增收据、不增加过程次数 |
| resolution完整、run未启动 | 已解析输入与出生链 | 只复用原输入；若旧execution attempt已标INCOMPLETE，不把它改回PREPARED |
| primary执行中或退出非零 | 原始日志/trace/exit/attempt | 停整个计划，不自动retry；新过程需要另审触发条件/次数/plan |
| primary完成但验证/重放未完整 | 全部原始输出/已有检查 | 未满足合取不能COMPLETE；缺replay不得写exact-match；恢复步骤需显式批准且不重复已完成过程 |
| 所有验证/replay已有、原子指针未发布 | 原immutable收据/hash/CAS进度 | 显式只读核验和授权的仅发布恢复可新增recovery receipt，零引擎调用，旧终态不覆盖 |
| COMPLETE已发布 | 原完整bundle和指针 | 全身份/原始refs再次精确核验才复用，另写reuse receipt，零新增样本/引擎调用 |
| 相同ID不同字节、锁冲突或旧refs丢失 | 冲突双方与诊断 | fail closed；不取最新，不改ID隐匿冲突，不以重建相似数据补旧证据 |

所有状态变化为append-only新phase receipt，不原地重写终态。当前自动重试0；上述恢复是规则
设计，不等于当前授权恢复，更不允许扩大2520/5040预算。任何新增实际调用都须另行事前登记。

## COMPLETE、科学分类、gate与退出

typed GATE_STATE强制分离execution、integrity、identity、selection、diagnostic、mapping、timing、
progression。stage JSON给出每字段enum及合法转移、所需证据和退出表；错误不能靠改标签变VALID。
有效阴性可以执行COMPLETE，但NOT_SUPPORTED/INCONCLUSIVE/NO_ELIGIBLE/TIMING_NOT_FROZEN均闭锁。
子进程原exit与orchestrator出口分开：拟议0仅全前提满足，2拒绝、3过程失败、4非法、5不完整、
6完整但科学/冻结前提阻断；这些不是现行入口的实测code。当前没有调用入口。
mapping支持不是H/L或候选通过；即使未来全前提满足，也仅“待明确下一阶段授权”，不创建unlock。

## S2 schema、数值与P1隔离

输入body仅resources/links/services，避免自指ID；科学envelope另含descriptor/workload/receipt refs。
body单独的SCIENTIFIC标签不构成来源证明。闭合字段表包含全部run/attempt/source/seed/config/
process/raw refs、独立trace/metrics/replay、error/completion及stage记录。每ref为允许repo-relative
path+SHA+实际size+kind/media type；禁止目录穿越/越权symlink、重复身份及未注册seed/method。

MAIN必须100服务/50H50L；H-only50H，LOW100/50H50L。只有H-only的L组status可以
NOT_APPLICABLE_CONTROL，count=0、指标null；主输入缺组、错误N/A或NaN均INVALID，不填0。
各窗口/makespan语义和绝对RN64可行性证书见generation/stage，不用observation_end改原利用率。

S2未来测试必须保留旧P1原始身份/serialization，拒绝fixture改名/改seed/换origin/伪造generator
receipt、缺父链和错误payload哈希；仅fixture_derivation=false不够。adapter必须逐项守恒图、
duration、兼容和通信，并保持D1–D5与只读公共信息边界。新source必须重新验证原64测试、45正
trace/20负trace及新血缘/故障/原子发布/恢复负例，不能继承当前P1 PASS。全部仍待未来授权实现。

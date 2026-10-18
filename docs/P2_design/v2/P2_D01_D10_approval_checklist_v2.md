# D01–D10 v2 human approval checklist

v2为新草案，不批准替换v1。每项需明确版本/hash、具体值/修改、审批者/时间及原始答复；方向同意不能代替缺失参数。

| ID | approval | Exact proposed decision | Required answer |
|---|---|---|---|
| D01 | UNAPPROVED | Exact v1 six templates/IDs/roles/predecessors/group inheritance retained; counts COCKPIT8/9,16/17; ADAS8/9,16/17; FUSION8/7,16/15; explicit two-half expansion/internal1/16MiB. | 是否批准完整六模板及v1保持的尺寸/角色/H-L规则？ |
| D02 | UNAPPROVED | Exact16x6 compatibility/cost table and CPU symmetry retained; null incompatible; base*scale*uniform[.9,1.1) estimate, separate resource factor same range for actual. | 是否批准原合成96单元格/兼容/CPU对称/扰动分布，并接受非硬件数据的限制？ |
| D03 | UNAPPROVED | Exact74 edge sizes and9 latency/bandwidth pairs retained; same-unit0 elseL+b/B; unitsms/MiB/MiB-ms; no bus contention or physical value changes. | 是否批准原74条边及9对通信参数和既有物理语义？ |
| D04 | UNAPPROVED | Typed version2+generator_v2+domain_v2; three exact KEY fills, original10 seeds; U=q/2^64; same100-service/50slot/H2.5-L4 deadlines; parent100 exactG; bit-preserving controls; separate semantic/raw/runtime hashes and21 preimages. | 是否批准v2逐字段key、编码/preimage、精确转换和parent100控制G定义？ |
| D05 | UNAPPROVED | 36 configs,10 seeds,2520 rows=1800MAIN+360H-only+360LOW,1080inputs,5040 maxengine withreplay,0retry/timing; sameA/B periods80/64,24/20,12/10; MAIN generation first, control execution first. | 是否批准不变的完整矩阵/预算及物化MAIN先于controls、执行顺序保持的区分？ |
| D06 | UNAPPROVED | Original target bands[0,.5),[.5,.8),[.8,1], lightH/L<=.01,loadedH[.01,.8] retained; typed validity/control/target/A-before-B total order; absolute RN64 lowerbound with strict>deadline, noepsilon, control witness only. | 是否批准总分类、控制见证范围、绝对RN64下界和不变的A-before-B资格规则？ |
| D07 | UNAPPROVED | M1R_PATH_V2: original2-4 ready enumeration; target<=2 pending arrivedH DAGs<=16nodes each; fixed public suffix EFT,<=36nodes/1296maps; L cap=max(baseline finish,deadline); exact snapshot scope/dedup/replay exclusion; no actual scheduler feedback. | 是否批准M1R的目标选择、固定suffix、局部L slack、边界/截断/去重和记录范围？ |
| D08 | UNAPPROVED | FINE(.01,.01) vs COARSE(.05,.05),8/10 support and<=2/10 absence remain undecided; M1R hits/F,F/E; proposed positive coverage>=4/5,negative=1,all12conditions/10seeds; samepaired10000,type7,20261018; selected calibration descriptive only. | 选择FINE还是COARSE（或提出明确替代）？是否批准4/5正覆盖、1阴性覆盖、三态及条件性解释？ |
| D09 | UNAPPROVED | RecommendR1 formalrunner vsR2thinlauncher; blueprint/auth/inputlock/generate/resolve/workload/run/attempt/runlock/preinvoke withoutcycle; exactreuse,0automaticretry,append-only recovery; P2clean policy newunapproved; explicit stages/exits, timingNOT_FROZEN blocks. | 是否批准R1、精确复用、零自动retry、恢复表、新增P2洁净和分离状态/出口契约？ |
| D10 | UNAPPROVED | RecommendS2typedscientificfamily+adapter vsS1envelope;21exactpreimages and closed typed records, worker argv templates currentlyunimplemented, main/control counts+singleN/A token, immutablebirthrefs, fullCOMPLETEconjunction; oldP1identity preserved and future regression required. | 是否批准S2、typed科学家族及身份/argv/COMPLETE规范和未来血缘/P1回归范围？ |

批准/拒绝/暂缓/待证据动作均未记录；全部approval=UNAPPROVED。FINE/COARSE无默认。
所有10项裁决后仍需单独授权实现/行为验证及最终生成/执行，不能从本表推断许可。

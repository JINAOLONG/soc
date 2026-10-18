# Required changes before approval / future implementation

These are review recommendations, not authorization or already applied proposal edits. Existing v1 files/values remain byte-for-byte unchanged.

## Approval-blocking documentation work

### V2-F01 (CRITICAL)

保留M1为窄局部诊断；在同一已到达公共DAG/估计边界内，先提出有限、可复算、能观察已登记remaining-H-path阻塞的诊断定义，并用非科学§32解释例及反例验证覆盖。明确严格局部L约束与全局L-P95预算的不同作用。D08必须只对其实际覆盖的机制下结论；不得更改既有H/L/CI门槛，不在本审计中实现或批准新观察器。

Acceptance evidence: 修订D07/D08文本、参数登记及适用/不适用案例，人工重新裁决；未来另行实现验证。

### V2-F02 (CRITICAL)

明确两层身份/守卫：批准的不可变blueprint与生成授权在前，以blueprint/config/seed/variant取得临时输入锁；授权后物化并保存generation receipt；再解析wlref形成独立不可变input-resolution receipt、实际workload/run ID与运行锁，最后做pre-invocation守卫。蓝图hash不得包含未来resolved payload/run ID，已批蓝图不回填改hash。精确argv的身份部分不得反向包含自身run ID；此为待审修订建议而非已批准流程。

Acceptance evidence: D04/D05/D09/D10共同给出无环身份图、首次/复用/中断三条顺序、明确字段与hash范围，另行人工批准。

### V2-F03 (MAJOR)

增加逐随机字段的完整typed-key填值表，逐一固定version绑定和空字段；固定control父身份及G的集合范围、整型/分数字段规范；列出workload/run preimage精确对象、raw/semantic/plan/argv hash范围及数组顺序。使用无真实科学seed的静态golden byte vectors检验规范，后续实现再验证；不生成新seed。

Acceptance evidence: 同一批准规格下两种独立编码实现必须输出相同golden bytes；审批明确涵盖会改变key的选择。

### V2-F04 (MEDIUM)

分开record_id和state_key；规定B2主attempt的何种view计数、失败/空派发、连续重复/非连续相同状态、now/elapsed参与规则、replay不进入分母。给出相同状态重复计1与同刻真实start后状态改变计2的静态验收例。

Acceptance evidence: D07/D08与schema共同固定state bytes、scope和expected denominator；未来独立复算测试。

### V2-F05 (MAJOR)

提供字段级出口真值表：execution_completion、input_integrity、selection_status、diagnostic_validity、mapping_status、freeze/timing prerequisite与p2_progression_status分别记录。明确有效阴性可COMPLETE但不准推进，缺失一律闭锁；现有P2 gate消费接口与不同退出码语义需在实现任务前登记。timing留为未关闭前提，不能靠预算0宣称已完成原P2输出；不在本任务编写gate。

Acceptance evidence: D08/D09/D10联合审查完整的stage出口规范，任何COMPLETE→PASS快捷路径均应有负例拒绝。

### V2-F06 (MEDIUM)

补充明确的总分类谓词：先validity、control witness、declared target-load匹配，再A/B选择；NaN/越域/控制重叠/缺组的出口须定型，不能clamp。明确P2区间仅为选中校准配置的描述，全部A/B资格和原始统计保留，不声称调整选择后的确认性覆盖。不更换CI方法、不加seed、不按结果改阈值。

Acceptance evidence: 审定分类伪代码/边界表及报告措辞，保持已提出数值和原研究契约未变或另行显式审批修订。

### V2-F07 (MEDIUM)

统一一个待批控制N/A枚举及其适用kind，main强制精确100/50/50计数、control分别50H或100H/L；给出absence/nonfinite/invalid矩阵。分别命名arrival_window_end、drain_completion、observation_end、busy_window_pressure与既有full-drain makespan/utilization，不改变原公式；定义G域与control overlap失败类型。 给出与现行binary64事件/绝对deadline一致的保守LB算术和等号边界测试，不引入任意epsilon；此为待批定义，不宣称已实现。

Acceptance evidence: 字段类型/enum/必填-null条件及独立指标验收例在D04/D06/D10一致，未来实现回归。

## Required future P1 compatibility and negative tests (NOT RUN for S2)

1. Preserve original fixture origins, serialization and known input bytes; round-trip legacy schema unchanged. New scientific namespace routes separately, unknown versions fail closed.

2. Re-run all existing 64 governance/P1 tests and independent P1 gate after any authorized source/adapter change; account for all 45 positive traces, 20 malformed cases and exact replay. Do not inherit the current source hash/PASS.

3. Reject renamed/relabelled P1 payloads, forged generator receipts, changed origin/seed, fixture parent lineage and cross-variant input/hash swaps. A boolean fixture_derivation=false is not evidence.

4. Prove adapter conserves every service/node/predecessor/resource/duration/link/group/deadline without hidden dummy or altered units; MAIN exactly100 services/50H+50L, controls50H or100H/L.

5. Freeze canonical typed-key/preimage golden vectors using non-scientific synthetic metadata; no reserved realization generation. Independently rederive IDs/hash and verify perturbation reuse across methods/control transformations in a separately authorized generator test.

6. Scheduler public DTO regression: no realized duration, future arrival/queue, private random factor or future completion truth; D1 event order and D2–D5 baseline semantics unchanged.

7. First-materialization, reuse and interruption traces of the orchestration state machine must match the revised acyclic spec; wrong approval/plan/seed/condition/method or unknown stage stops before generation/invocation.

8. Fault injection: spawn failure, signal/no exit, nonzero engine, malformed trace, missing/corrupt refs, metric mismatch, replay mismatch, lock conflict, same-ID/different-bytes, partial publication; never COMPLETE/PASS. Preserve all raw evidence; zero automatic retries.

9. Reuse only after full identity/hash/validity checks, without new sample or engine invocation. New authorized attempts preserve supersedes; different source/input is a new run with linkage.

10. Independently verify deadline equality, full drain, arrival-window clipping, makespan versus observation_end, control group-N/A and main missing-group rejection. No arbitrary epsilon/clamp.

11. M1 observer tests: duplicate state counts once, real same-time state change counts separately, replay excluded, exact eligible K/truncation and deterministic ties, local greedy belongs to feasible set, no future truth. Revised mechanism coverage must pass positive/negative explanation cases without scientific samples.

12. Stage-completion/criterion truth table: valid negative may be execution COMPLETE but never progression PASS; INCONCLUSIVE/missing/invalid/timing-unfrozen/unknown-lineage remain closed. Complete outputs with NOT_SUPPORTED cannot bypass the unchanged scientific stop contract.

All the above are requirements to register for a future separately authorized task. This review implements none of them and does not claim they passed.

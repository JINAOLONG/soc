# V3 exact human decision packet

All approvals UNAPPROVED. Documentation revision is not acceptance/freezing/implementation or scientific execution. Read final artifact_manifest.json hashes before answering; enclosing HEAD resolved live.

## F01

Decisions: D07 D08; parameters: SP25 SP31 SP36; approval=UNAPPROVED.

选择 A_KEEP_ORIGINAL 并接受 ADAS 下不能成立完整阴性；或 B1_EXPAND_SINGLE_READY 并明确批准偏离原§44的单ready扩展；或 B2_CONDITIONAL_DOMAIN 并接受条件estimand/完整排除记录和更弱阴性、明确是否可据此停止主线；或拒绝/暂缓并列替代要求。不得仅回答“批准修复不可达”。

完整方案、具体语义、改动/保留规则、风险、静态证据和未运行测试见 `F01_observation_domain_options.md`；对应机器规范在 docs/P2_design/v3。

## F02

Decisions: D04 D09 D10; parameters: 工程细节；依赖SP10 SP20; approval=UNAPPROVED.

选择 A_NO_TAKEOVER 的唯一不可替换授权/失联闭锁，或 B_FENCED 的共享域/单调epoch/权威admission与publication契约；或暂缓。部署lease与可信后端必须明确，不能把方向同意当作批准未知参数。

完整方案、具体语义、改动/保留规则、风险、静态证据和未运行测试见 `F02_lock_recovery_contract.md`；对应机器规范在 docs/P2_design/v3。

## F03

Decisions: D04 D09 D10; parameters: 工程细节；依赖SP10; approval=UNAPPROVED.

是否批准完整 V3 execution-context/provenance 类型、采集来源/时点、sealed source、新run/context身份与COMPLETE/复用绑定？可以拒绝或要求另一套完整 typed 字段，不能只批准“记录HEAD”。

完整方案、具体语义、改动/保留规则、风险、静态证据和未运行测试见 `F03_execution_provenance_contract.md`；对应机器规范在 docs/P2_design/v3。

## F04

Decisions: D07 D08 D09 D10; parameters: SP27 SP31; approval=UNAPPROVED.

是否批准所列720配对、四个方法相对B2、18条件的精确roster/contrast/报告/验证/独立状态与缺失闭锁规则？原统计协议保持；不批准任何科学分析执行。

完整方案、具体语义、改动/保留规则、风险、静态证据和未运行测试见 `F04_M2_artifact_contract.md`；对应机器规范在 docs/P2_design/v3。

## F05

Decisions: D04 D10; parameters: SP10; approval=UNAPPROVED.

是否确认14字段closed KEY及三种binding，以现有字段为准仅修正All15文案，不新增字段或随机输入？

完整方案、具体语义、改动/保留规则、风险、静态证据和未运行测试见 `F05_key_count_correction.md`；对应机器规范在 docs/P2_design/v3。

## Ten original decisions

- D01 — UNAPPROVED — original question: 选择显式角色 DAG 还是确定性 grammar，并提供三场景的完整8/16节点拓扑、角色/H-L归属及尺寸规则。

- D02 — UNAPPROVED — original question: 选择有来源的profile表或批准的合成规则，提供兼容集合、各资源估计/实际代价及全部参数/来源。

- D03 — UNAPPROVED — original question: 提供边MiB与type-pair latency/bandwidth的完整表或有来源规则，保留既有通信语义。

- D04 — UNAPPROVED — original question: 确定keyed扰动/PRNG/版本、到达/突发、H-L组成、deadline、服务数或窗口及停止边界的完整定义/值。

- D05 — UNAPPROVED — original question: 确定枚举或有限轴展开，提供所有值/方法子集及理由/顺序/预算/seed到trial-condition-workload的精确映射。

- D06 — UNAPPROVED — original question: 确定H可行性对照、压力/负载分类、配置选择/平局以及不达标、不可行、无效、失败、不完整的处置规则。

- D07 — UNAPPROVED — original question: 选择M1机制诊断、M2基线描述或组合，确定观察量、反事实控制/视窗、信息边界和每seed/condition汇总。

- D08 — UNAPPROVED — original question: 确定跨seed/条件聚合、稳定性、不确定性和三向结论的全部条件/参数及缺失无效处置，保持既有CI方法。

- D09 — UNAPPROVED — original question: 选择runner架构，裁决完成产物精确复用、失败/不完整默认停止、重试登记和P2源码dirty控制。

- D10 — UNAPPROVED — original question: 选择可验证的科学envelope或新schema+adapter，批准namespace、规范化、ID、provenance、引用与旧P1兼容验证范围。


## Forty original parameter/rule groups

Exact values/options/pointers and v2 lineage in P2_scientific_parameter_registry_v3.json. Table is an index,not a substitute for full source content.

| ID | Decision | Name | Approval |

|---|---|---|---|

|SP01|D01|six_topologies|UNAPPROVED|

|SP02|D01|importance_assignment|UNAPPROVED|

|SP03|D01|size_expansion|UNAPPROVED|

|SP04|D02|role_compatibility|UNAPPROVED|

|SP05|D02|role_execution_costs|UNAPPROVED|

|SP06|D02|cpu_symmetry|UNAPPROVED|

|SP07|D03|edge_sizes|UNAPPROVED|

|SP08|D03|link_latencies|UNAPPROVED|

|SP09|D03|link_bandwidths|UNAPPROVED|

|SP10|D04|key_encoding_hash_mapping|UNAPPROVED|

|SP11|D04|estimate_distribution|UNAPPROVED|

|SP12|D04|realized_distribution|UNAPPROVED|

|SP13|D04|arrival_jitter|UNAPPROVED|

|SP14|D04|arrival_burst|UNAPPROVED|

|SP15|D04|service_count_and_group_mix|UNAPPROVED|

|SP16|D04|deadline_multipliers|UNAPPROVED|

|SP17|D04|arrival_window|UNAPPROVED|

|SP18|D05|period_axis|UNAPPROVED|

|SP19|D05|main_method_set|UNAPPROVED|

|SP20|D05|finite_order_budget|UNAPPROVED|

|SP21|D06|control_input_transform|UNAPPROVED|

|SP22|D06|load_pressure_bands|UNAPPROVED|

|SP23|D06|load_miss_bands|UNAPPROVED|

|SP24|D06|configuration_selection|UNAPPROVED|

|SP25|D07|M1_snapshot_subset|UNAPPROVED|

|SP26|D07|M1_counterfactual_objective|UNAPPROVED|

|SP27|D07|M2_measurements|UNAPPROVED|

|SP28|D08|material_gain_cutoff|UNAPPROVED|

|SP29|D08|frequency_cutoff|UNAPPROVED|

|SP30|D08|stability_requirement|UNAPPROVED|

|SP31|D08|condition_aggregation|UNAPPROVED|

|SP32|D08|bootstrap_implementation_pin|UNAPPROVED|

|SP33|D07|target_H_selection|UNAPPROVED|

|SP34|D07|bounded_public_suffix_rollout|UNAPPROVED|

|SP35|D07|local_L_slack_admissibility|UNAPPROVED|

|SP36|D08|coverage_and_missing_evidence|UNAPPROVED|

|SP37|D07|state_equivalence_denominator|UNAPPROVED|

|SP38|D06|absolute_conservative_feasibility_arithmetic|UNAPPROVED|

|SP39|D08|selected_calibration_interpretation|UNAPPROVED|

|SP40|D06|control_NA_and_window_semantics|UNAPPROVED|


D01–D03/D05/D06 remain unapproved even if unchanged. FINE/COARSE,coverage,stability,load bands and all scientific values remain unapproved. No implicit new threshold or outcome-based choice.

## Approval record requirements

Answer exact ID,selected option,version/file/hash,scope/exceptions,and evidence still required. Agreeing to a revision direction does not approve its future unknown values. Timing seven fields remain NOT_FROZEN;2ms unchanged. All runtime/fault/analysis validation NOT_RUN. After design approval, implementation correctness and scientific generation/execution still each need separately explicit authorization. STOP after this package.

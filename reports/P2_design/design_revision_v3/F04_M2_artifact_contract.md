# F04 — explicit M2 roster, contrast and completion binding

D07/D08/D09/D10, SP27/SP31; PROPOSED_REQUIRES_APPROVAL. Original v1 D07 lines275–279, v2 D07 lines156–157 and statistical_protocol3–47 preserve B1/B3/B4/B5 individually versus B2 on same workload. Exact new membership/layout is an engineering proposal; no new method/statistic is approved. Machine design: docs/P2_design/v3/P2_M2_artifact_contract_v3.json; new closed M2 types and STAGE_RECORD_V3 in typed schema.

## Roster and pairs

After B2-only configuration selection fixed all18 conditions and before diagnostic/M2 effects inspected: expected selected18 × registered CALIBRATION10 × (B1,B3,B4,B5 versus B2)=720 pairs. This is a symbolic product/derived count, not720 executed observations or materialized IDs. Original2520 trials and both A/B raw sets remain. Controls/replays excluded as independent M2 samples. Original18-condition descriptive scope retained; diagnostic12loaded conditions are not silently substituted for M2's18. If selection fails any condition, roster unavailable/INCOMPLETE and progression BLOCKED; do not shrink it.

Pair key=(condition_id,actual_seed_decimal_string,selected_config_id,method_id,reference B2,workload_id). Both records require identical materialized MAIN workload SHA/identity, not merely same seed label, plus correct selection/config/condition and valid original complete trace/metric/replay/provenance. Exactly one row per expected key. Missing/duplicate/unexpected/cross-seed/wrong-workload/wrong-method/mismatched refs or invalid metric closes analysis; no zero filling, averaging duplicate pairs or dropping failures.

## Exact contrast and auxiliary membership

- H_DMR_DIFF = method H-DMR minus B2 H-DMR, proportion points (0..1 input; signed difference), not a relative gain or100-times percent rescale.
- L_P95_DIFF = method L P95 minus B2 L P95,ms. Existing within-run type7 quantile unchanged; no ratio substitution.
- H_WAIT_DIFF and L_WAIT_DIFF = respective per-service mean assigned_busy_wait differences,ms/service; each MAIN group50. Sum node busy-wait measures then divide by50, not by node count or all100. Preserve overall100-service summary as auxiliary if emitted; no changed primary inference.
- Preserve CPU/GPU/NPU components, H critical-path blocking and compute/transfer/policy idle decomposition, public compatible counts and alternative predicted EFT differences. v1 defines dep,data,post_wait,assigned_busy_wait and policy_idle; independent trace checks verify identities before metrics accepted. Node-ms can overlap across parallel branches and is not an end-to-end causal decomposition.
- Compatibility report contains source-node records and counts by group/resource-compatible count1..6, denominator50×registered size for each MAIN group, not all seeds pooled. Public alternative EFT differences retain unitsms and NONE where no alternative; never use future truth for substitute cost.
- B2-only M1R summary references the selected route's E0/A0/F/hits and complete snapshot/recompute evidence. Historical M1 not restored. It is attached for mechanism interpretation, not a contrast against another method's nonexistent observer or an independent causal test.

Exact source metric values remain immutable binary64/rational artifacts; contrast bodies encode their exact rational decoded differences. No epsilon, clipping or new threshold. New layout/directional subtraction convention is explicitly proposed, sources retain original meaning/units.

## Required artifact inventory

FIXED_SELECTION_REPORT; EXPECTED_M2_PAIR_ROSTER; M2_PAIR_ROWS; M2_CONTRAST_TABLE; TRACE_WAIT_DECOMPOSITION; COMPATIBILITY_AND_SUBSTITUTION_REPORT; B2_OBSERVER_SUMMARY; PAIRED_SEED_CONDITION_AND_EQUAL_WEIGHT_MACRO_SUMMARY; RESAMPLING_PROTOCOL; RESAMPLING_INDICES_OR_REPRODUCIBLE_DIGEST; M2_REPORT_INVENTORY; INDEPENDENT_M2_ANALYSIS_VALIDATION.

Each inventory entry: exact kind,repo-relative safe path,raw SHA,size,namespace/schema/spec identity and source refs. Every pair row binds both original completion refs,independent metric refs,wait decomposition refs,contrast and compatibility refs,B2 observer ref. Each aggregate binds exact pair roster/rows/protocol and relevant run/metric refs. A report cannot cite a self-containing inventory: produce member bodies first, inventory excluding itself and final report, then report references inventory; stage references report and independent validation. Semantic recomputation not only existence checks is required.

To avoid a report↔validation hash cycle, report inventory ALSO excludes independent validation. M2_ANALYSIS_REPORT_V3 cannot contain its later validation ref; its completed status is COMPLETE_PENDING_INDEPENDENT_VALIDATION,never self-declared VALID. After report finalizes, M2_ANALYSIS_VALIDATION_V3 references that report/expected roster and records independent verification MATCH/MISMATCH/INCOMPLETE with exact discrepancy counts. Stage explicitly binds both refs and requires MATCH/all0; m2_report_status COMPLETE is only member completeness,while m2_analysis_validity VALID requires the later verifier. The overall stage evidence includes validation separately; omission remains blocking.

Bootstrap remains seeds as paired independent units,10000 replicates,analysis seed20261018,type7 percentile95%,shared index vector for every method/condition. Per-condition M2 descriptors retained all18; H macro and M1R macro retain original12loaded equal-weight conditions, L per-condition reporting all18. No conditional/macro result can compensate for a missing pair or failed condition. Any additional aggregation not already registered remains unresolved and cannot be invented in implementation. No resampling indices or intervals generated now. Selected-calibration CI is descriptive/pointwise, not independent confirmation or pure causal mapping evidence.

## Separate states and predicates

| Layer | Evidence needed | Missing/invalid consequence |
|---|---|---|
|Raw execution complete|Original2520 per-trial conjunctions|Execution incomplete/failed; no analysis PASS|
|Single-run metric MATCH|Independent trace and exact recomputation|Invalid run retained, no valid pair|
|M2 roster COMPLETE|Expected720 exact key multiset,all inputs valid|INCOMPLETE or INVALID|
|M2 contrasts COMPLETE|All720 typed contrast records and source matching|INCOMPLETE or INVALID|
|M2 reports COMPLETE|Every required inventory member verified|INCOMPLETE or INVALID|
|M2 analysis VALID|Independent semantic pair/contrast/aggregation/statistical protocol verification|INVALID/INCOMPLETE/NOT_CHECKED,never default VALID|

V3 GATE_STATE adds m2_roster_status,m2_contrast_status,m2_report_status,m2_analysis_validity. STAGE_RECORD_V3 explicitly requires m2_roster_ref,m2_analysis_report_ref,m2_validation_ref (null only before completion/failure states); criterion V and progression require nonnull verified exact members and valid states. Raw execution COMPLETE does not imply M2 COMPLETE. All outputs present but validation NOT_CHECKED still blocks.

Future tests NOT_RUN: all raw runs but no M2 reports; one missing pair; duplicate pair; wrong workload/same seed; unexpected method/control/replay; zero-filled absent group; hash corruption; wrong contrast direction/unit/group denominator; omitted wait identity; changed bootstrap vector/replicate/type7; report missing validation; counts correct but keys wrong; outcome-based selection. All should fail closed without computing or running anything in this task.

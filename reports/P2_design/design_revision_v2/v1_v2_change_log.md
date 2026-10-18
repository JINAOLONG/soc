# v1 → proposed v2 change log

Source checkpoint 79f9c245b23119ce25175d6dc6ff148e9e092461. Old files immutable; no active contract replaced. D05 audit-summary discrepancy is recorded in reviewed_sources.json.

## Preserved exact scientific values

D01 six templates/IDs/predecessors/group inheritance; D02 all role/resource costs/compatibility; D03 all edges/links; original arrival/perturbation/deadline numbers;36config/10seed/B1–B5/2520/5040; target-load bands and A-before-B selection. No scientific realization compared.

## Changed or made explicit

v2 typed key/version binding changes future draw identity even where distributions remain identical; no claim of sample preservation. M1R replaces only the proposed stage observer, preserving historicalM1 separately. Source2–4-ready limit retained; single-ready is explicit insufficient coverage, not an unregistered1-ready oracle. Coverage4/5 support and1 negative, target2 H, fixed public suffix and localL slack are new UNAPPROVED rules.

| ID | Change | v1 value/rule | v2 proposed value/rule | Findings | Approval |
|---|---|---|---|---|---|
| SP01 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_workload_templates_v1.json#/templates | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP02 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_workload_templates_v1.json#/group_rule | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP03 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_workload_templates_v1.json#/expansion | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP04 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_resource_profiles_v1.json#/profiles | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP05 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_resource_profiles_v1.json#/profiles | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP06 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_resource_profiles_v1.json#/profiles | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP07 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_communication_profiles_v1.json#/edge_tables | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP08 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_communication_profiles_v1.json#/links | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP09 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_communication_profiles_v1.json#/links | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP10 | CHANGED_TYPED_KEY_AND_VERSION | v1 conceptual version/empty-field list | Explicit schema_version2 + generator_version v2; all3 fields retain scenario/condition/config, only prescribed fields empty; exact typed KEY. | V2-F03 | UNAPPROVED |
| SP11 | UNCHANGED_DISTRIBUTION_CHANGED_KEY_BINDING | [.9,1.1) keyed node factor | Same distribution; explicit v2 field keys change future draw identity, no realization compared. | V2-F03 | UNAPPROVED |
| SP12 | UNCHANGED_DISTRIBUTION_CHANGED_KEY_BINDING | [.9,1.1) keyed resource factor | Same distribution/private boundary; exact v2 key and conversion. | V2-F03 | UNAPPROVED |
| SP13 | UNCHANGED_DISTRIBUTION_CHANGED_KEY_BINDING | slot U/10 with other IDs ambiguous | Same U/10; scenario/condition/config retained, H/L/node/resource/edge empty exactly. | V2-F03 | UNAPPROVED |
| SP14 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_generation_spec_v1.json#/arrivals | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP15 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_generation_spec_v1.json#/arrivals | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP16 | CLARIFIED_WITHOUT_NUMERIC_CHANGE | H2.5*C_est,L4*C_est; exactness implicit | Same multipliers, explicit pre-round E_exact reference and final binary64 absolute deadline. | V2-F07 | UNAPPROVED |
| SP17 | CLARIFIED_SPLIT_WINDOW_SEMANTICS | W=50P and run_end=max(W,lastfinish) | W unchanged; distinct arrival_end/lastarrival/lastfinish/makespan/observation_end; full-drain metric preserved. | V2-F07 | UNAPPROVED |
| SP18 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_trial_matrix_draft_v1.json#/configs | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP19 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_trial_matrix_draft_v1.json#/methods | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP20 | UNCHANGED_BUDGET_VERSIONED_IDENTITIES | 36*10*7=2520;5040 with replay | Budget/order unchanged; proposal-v2 and wlref:v2 refs, MAIN materialization before controls but engine order unchanged. | V2-F02 | UNAPPROVED |
| SP21 | CLARIFIED_CONTROL_DOMAIN_AND_QUALIFICATION | G max_service domain ambiguous; controls retain parent values | G always ALL100 parent MAIN services and exact pre-round sidecar; no new draw; distinct control witness/overlap qualification. | V2-F03,V2-F07 | UNAPPROVED |
| SP22 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_complete_design_proposal_v1.md#D06 | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP23 | UNCHANGED_PROPOSED_VALUE | Exact v1 value in P2_complete_design_proposal_v1.md#D06 | Exact same semantic proposed value; versioned document namespace only. | NONE | UNAPPROVED |
| SP24 | CLARIFIED_TOTAL_PREDICATES | A-before-B based on B2 eligibility | Same deterministic policy; validity/control/OWN target bin explicit; all off-target/unselected preserved. | V2-F06 | UNAPPROVED |
| SP25 | SPLIT_AND_CHANGED | Historical M1: K2..4 containing H, ready-prefix only | M1R: K2..4 (single-ready states explicitly coverage-insufficient) and pending arrived H targets; target scope/dedup separately registered SP33/SP37. | V2-F01,V2-F04 | UNAPPROVED |
| SP26 | SPLIT_AND_CHANGED | Mean ready-prefix H finish, strict localL nondegradation | Mean projected completion of selected remaining-H DAGs; fixed suffix and new L slack separately SP34/SP35. | V2-F01 | UNAPPROVED |
| SP27 | UNCHANGED_MEASURES_CHANGED_DIAGNOSTIC_REFERENCE | M2 B1/B3/B4/B5 vsB2 descriptive | Same contrasts/noncausal interpretation; M1R onlyB2 diagnostic references; historical M1 not gate. | V2-F01 | UNAPPROVED |
| SP28 | UNCHANGED_NUMBERS_CHANGED_OBSERVABLE | FINE tau.01/COARSE.05 on v1 local gain | Same candidate tau values, applied only to FULL M1R remaining-H projected gain; no selection made. | V2-F01 | UNAPPROVED |
| SP29 | UNCHANGED_NUMBERS_CHANGED_DENOMINATOR | FINE frequency.01/COARSE.05 over v1 eligible views | Same candidate frequency values; hits/F over FULL covered unique states, coverage separately F/E. | V2-F01,V2-F04 | UNAPPROVED |
| SP30 | UNCHANGED_NUMBERS_CHANGED_OBSERVABLE | Support8/10,absence<=2/10 | Same numeric stability on new per-seed FULL-coverage frequency, no new independent unit. | V2-F01 | UNAPPROVED |
| SP31 | SPLIT_AND_CLARIFIED | All12 selected loaded conditions; missing->inconclusive | Same condition/macro units; coverage and selected-calibration interpretation separately SP36/SP39. | V2-F05,V2-F06 | UNAPPROVED |
| SP32 | CLARIFIED_WITHOUT_CI_CHANGE | SHA256 rejection index,10000,type7,20261018 | Same algorithm/constants; exact five-field ANALYSIS_INDEX_KEY; no bootstrap indices generated. | V2-F03 | UNAPPROVED |
| SP33 | ADDED_SPLIT_OUT_EXPLICIT_RULE | Previously embedded/unspecified scope in SP25 | First2 unfinished arrived H with pending nodes by deadline/service ID; truncation is coverage insufficiency. | V2-F01 | UNAPPROVED |
| SP34 | ADDED_SPLIT_OUT_EXPLICIT_RULE | Previously embedded/unspecified scope in SP26 | All public remaining nodes of<=2 targetH DAGs,<=16 each; fixed Kahn+B2/EFT suffix, <=36 projected nodes, <=1296 action mappings; no candidate/policy feedback. | V2-F01 | UNAPPROVED |
| SP35 | ADDED_SPLIT_OUT_EXPLICIT_RULE | Previously embedded/unspecified scope in SP26 | L action node finish <=max(baseline L finish, service deadline); no globalL budget implication, no1.10 borrowing. | V2-F01 | UNAPPROVED |
| SP36 | ADDED_SPLIT_OUT_EXPLICIT_RULE | Previously embedded/unspecified scope in SP31 | Propose support coverage>=4/5 per seed/condition; negative requires1; E/F>0, partial neverzero, invalid/missing fail closed. | V2-F01,V2-F04 | UNAPPROVED |
| SP37 | ADDED_SPLIT_OUT_EXPLICIT_RULE | Previously embedded/unspecified scope in SP25 | Canonical public binary64-bit snapshot; per primary MAIN-B2 attempt scope; exclude seq/wall/private data; replay excluded. | V2-F04 | UNAPPROVED |
| SP38 | ADDED_SPLIT_OUT_EXPLICIT_RULE | Previously embedded/unspecified scope in SP21 | Absolute RN64 monotone lower bound, actual compatible mincost/delay offline; strict B_abs>d_abs only, equality not certified, no epsilon. | V2-F07 | UNAPPROVED |
| SP39 | ADDED_SPLIT_OUT_EXPLICIT_RULE | Previously embedded/unspecified scope in SP31 | Selected calibration pointwise intervals conditional/descriptive; not independent confirmation. This is an explicit logical limitation, not changed CI methodology. | V2-F06 | UNAPPROVED |
| SP40 | ADDED_SPLIT_OUT_EXPLICIT_RULE | Previously embedded/unspecified scope in SP21 | MAIN100/50H50L; H-only50H; LOW100; one NOT_APPLICABLE_CONTROL enum; makespan remains lastfinish, observation_end separate. | V2-F07 | UNAPPROVED |

No deleted/merged groups. v1SP25 splits scope/target/dedup;SP26 splits objective/suffix/L slack;SP31 splits criterion/coverage/interpretation;SP21 splits controls/numerics/N-A-window. Originals remain traced, making40 current named groups.
Engineering changes:21closed preimages, source/argv/lock identities, separate stage states/exits and append-only recovery; these are proposals underD09/D10, not additional scientific scalar counts.
New source code, real generator/workload IDs, actual timing parameters/measurements and scientific results remain unavailable by task boundary, not filled with fake values.

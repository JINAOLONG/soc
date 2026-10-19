# D09/D10 V3 — proposed runner, provenance and recovery contract

DRAFT_UNAPPROVED_NONEXECUTABLE. No implementation, no process execution authorization. Read immutable base runner ../v2/P2_runner_schema_review_v2.md and its exact hash in inherited_v2_documents.json/reference_bindings. This V3 overlay takes precedence ONLY as an unapproved proposal for the findings named here. All base physical/source/lineage/replay/count/zero-retry conditions remain.

## Effective contract and choices

F01 observer route=null; F02 coordination policy=null; threshold bundle=null. Any unknown/unselected/unapproved route fails pre-materialization guards; never default to inherited v2 negative rule or a lock based solely on attempt ID. Typed V3 effective_family maps new required context/run/process/generation/completion/stage records. All legacy definitions remain for reuse of unchanged components and historical comparison, not an alternative acceptance path. No current pipeline consumes this document.

Detailed normative proposals:

- ../../../reports/P2_design/design_revision_v3/F01_observation_domain_options.md and P2_diagnostic_spec_v3.json define three unselected routes and all denominator/negative limits.
- ../../../reports/P2_design/design_revision_v3/F02_lock_recovery_contract.md defines shared budget/domain,CAS exact expected tuple,phases,A no-takeover and B fencing,consumed-spawn uncertainty and immutable recovery.
- ../../../reports/P2_design/design_revision_v3/F03_execution_provenance_contract.md defines mandatory observed context/raw evidence,sealed source and pre/post provenance/hash binding.
- P2_M2_artifact_contract_v3.json and ../../../reports/P2_design/design_revision_v3/F04_M2_artifact_contract.md define exact720 selected M2 pairs,required members,separate states and semantic checks.

Future order: exact approvals/source/contract freeze→root auth/budget+symbolic plan→source context→input descriptor/shared domain→generation reservation and preprovenance→actual generation→postprovenance/receipt→independent input validation/resolution→workload→RUN_PREIMAGE_V3→attempt and primary domain→preprovenance/admission→actual primary/postprovenance→independent trace/metrics and exactly one registered replay→provenance/artifact inventory→verified completion receipt/pointer. Source context has no future run/workload/own hash; domains exclude transient auth/attempt. Validation/publish-only recovery never fabricates missing child/replay evidence. MAIN generation still precedes control derivation; engine sequence remains controls then MAIN B1..B5.

Future stage order: all2520 trial artifacts valid→fixed B2-only qualification/selection all18→M1R route diagnostic and M2 exact pair analysis→independent analysis validity→criterion classification→separate stage fields and timing verification. M2 completeness is now explicit. Unselected routes,NOT_FROZEN,missing/invalid evidence or unknown conjunction all BLOCKED. Child0 or execution COMPLETE never provides progression permission.

Original preimage/body canonicalization unchanged for reused V2 components. New V3 records have explicit namespaces/schema3/new names and no silent legacy acceptance; closure/required fields alone do not prove referential integrity or truthful observation. Future worker entrypoint remains NOT_IMPLEMENTED and must not be called. Frozen contract and approved exact route must bind the actual future execution plan,guard and receipt inventories. No fixture-to-science conversion,seed redraw,outcome-based selection or extra retry.

All detailed future fault/runtime tests in F02/F03/F04 reports plus original P1 regression remain NOT_RUN. Approval of this design alone will not authorize their implementation or scientific execution. The2ms host timing goal is unchanged; seven timing parameters remain NOT_FROZEN and must be approved before candidate timing/full P2 progression, not inferred for preparatory engineering.

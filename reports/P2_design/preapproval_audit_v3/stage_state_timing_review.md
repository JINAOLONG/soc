# Stage-state, timing and status reconciliation — fresh report-only audit

Audited revision: `a3680acf45c5578fc090cf53cc186f28a8e9b88a`, branch `work`.
This review reads current bytes and performs field/enum comparisons only. No gate was called, no workload or timing input was generated, and no scientific result or confidence interval was computed by this subreview. All design approvals remain UNAPPROVED. This is collaborating Codex review, not external independent personnel review.

## Actual state dimensions

The eight substantive state dimensions and required reason-code field in stage JSON exactly match the closed typed `GATE_STATE` properties and required names. Current literal values belong to their enums. Structural consistency does not establish semantic completeness of the downstream evidence contract.

| Field | Enumerated states | Current design literal |
|---|---|---|
| `execution_completion` | `NOT_STARTED`, `RUNNING`, `COMPLETE`, `FAILED`, `INCOMPLETE` | `NOT_STARTED` |
| `artifact_integrity` | `NOT_CHECKED`, `VALID`, `MISSING`, `CORRUPT`, `INVALID` | `NOT_CHECKED` |
| `input_seed_identity` | `NOT_CHECKED`, `VALID`, `INVALID` | `NOT_CHECKED` |
| `selection_status` | `NOT_EVALUATED`, `SELECTED_ALL_18`, `NO_ELIGIBLE_CONDITION`, `INVALID_EVIDENCE` | `NOT_EVALUATED` |
| `diagnostic_validity` | `NOT_RUN`, `VALID`, `POSITIVE_COVERAGE_ONLY`, `INSUFFICIENT_COVERAGE`, `INVALID`, `INCOMPLETE` | `NOT_RUN` |
| `mapping_classification` | `NOT_EVALUATED`, `SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE` | `NOT_EVALUATED` |
| `engineering_timing_prerequisite` | `NOT_FROZEN`, `FROZEN_PROTOCOL_VERIFIED`, `INVALID` | `NOT_FROZEN` |
| `p2_progression_status` | `BLOCKED`, `REQUIREMENTS_MET_PENDING_EXPLICIT_NEXT_STAGE_AUTHORIZATION` | `BLOCKED` |

`reason_codes` currently lists DESIGN_UNAPPROVED, IMPLEMENTATION_NOT_VALIDATED, EXECUTION_NOT_AUTHORIZED and TIMING_PROTOCOL_NOT_FROZEN. These are draft-state reasons, not results of a scientific stage run.

The distinctions are substantively necessary:

1. A child actually exiting zero is a process observation. It is not the orchestrator's stage verdict.
2. Per-trial COMPLETE requires primary exit zero, source/input/approval lineage, raw-reference integrity, independent physical-trace PASS, exact independently derived metrics, one exact registered replay, no errors and an atomically published completion receipt.
3. Stage execution COMPLETE requires the full 2520 trial identities, matching exact reused artifacts where permitted, and zero missing/mismatched/duplicate/unexpected identities. Both A and B remain represented.
4. Complete execution does not establish all18 selected conditions, valid diagnostic coverage, mapping support or frozen timing.
5. Mapping SUPPORTED concerns the registered public projected observer, not actual candidate H benefit, full-service L-budget compliance, causal mapping contribution or the 2 ms target.
6. The proposed overall progression state requires all listed approvals, separately valid execution authorization, exact-source P0/P1 evidence, complete and valid artifacts/identity, all18 selected, valid positive coverage/support, frozen timing and verified freeze receipts. The terminal label is REQUIREMENTS_MET_PENDING_EXPLICIT_NEXT_STAGE_AUTHORIZATION, not an unlock.

## Boundary cases and remaining completeness gap

The following are hand-authored Boolean contract cases, not scientific samples, measured outcomes or execution results:

| Hypothetical evidence state | Required consequence under current prose |
|---|---|
| Child exited0 but replay or required raw reference missing | Per-trial COMPLETE prohibited; missing/incomplete evidence closes stage, proposed exit5 where incomplete applies. |
| All2520 trials valid but a declared condition has no eligible A/B | Execution may be COMPLETE; selection NO_ELIGIBLE_CONDITION, progression BLOCKED, proposed exit6. Mapping remains NOT_EVALUATED if analysis was not attempted; an attempted criterion with failed precondition is INCONCLUSIVE. |
| Full listed evidence supports mapping but timing NOT_FROZEN | Mapping support may be retained; overall progression BLOCKED, proposed exit6. |
| Valid complete negative/inconclusive analysis | COMPLETE does not authorize progression; proposed exit6. The NOT_SUPPORTED case is a logical enum case only: the fresh M1R review proves this branch unreachable under the present mandatory ADAS sampling/coverage definitions. |
| All progression conjunctions eventually proven | Future proposed orchestrator0 means requirements met pending explicit next-stage authorization; it does not itself authorize P3. |
| Corruption, illegal trace or recomputation mismatch | Invalid evidence closes stage, proposed exit4; not a valid negative opportunity. |

The original typed state enums are coherent, but generic reference fields are not a complete evidence membership contract. In particular:

- D08 markdown lines21–23 says V requires **M2 paired completeness**.
- Criterion JSON `preconditions` enumerates full trial artifacts, selection and M1R snapshot/recomputation evidence but omits produced M2 paired analyses.
- Stage progression lists valid execution and diagnostic/support but no exact M2 analysis inventory. `STAGE_RECORD` has generic `diagnostic_report_ref` and `prerequisite_evidence`; it does not specify mandatory M2 membership there.
- Therefore a design implementation could preserve all listed machine predicates after skipping M2 paired-report production, even though markdown V would be false. All raw per-run metrics merely make M2 computable. Generic references could carry M2, so this is an **incomplete normative binding**, not proof of an existing executable bypass.

Local finding DECISION-M2-COMPLETENESS is MEDIUM and remains open. A separately authorized revision must bind the exact M2 paired roster/contrasts/report evidence and missing-output behavior to the criterion/stage contract. Do not add methods or change statistical definitions. Other reviewers' major lifecycle findings and critical negative-branch reachability finding also prevent full D07–D10 approval. This report does not alter v2 to repair them.

The table of `legal_transitions` is a partial phase guide: it explicitly lists execution, integrity and mapping transitions, with immutable terminal evidence. It does not purport to enumerate every cross-product of all state enums. A future implementation task must test all failure paths against the semantic conjunction, not infer acceptance from enum validity alone. Missing evidence, APPROVAL=false or unknown conditions must never become passing state by relabeling. Recovery and concurrency tests are specified in the identity review, not implemented here.

## Timing authority and exact freeze order

Original user requirement §59 retains **decision P95 ≤2 ms**, explicitly a development-host engineering target, not automotive hardware latency. It requires the engineering timing protocol to be frozen **at P2, before candidate timing**. Required items are exact inputs, warm-up, repetitions, timer, aggregation, P95 definition and host environment. `metric_spec.md:48–52` additionally defines measured scheduler scope: preprocessing/path updates/urgency/candidate generation and sorting/scoring/mapping/selection; virtual execution/communication is separate. `research_contract.md:45–48` requires registration before dependent observations. §80 requires the engineering timing protocol among P2 outputs.

The source does **not** establish an ordering of timing-protocol freeze before any implementation or before baseline-only calibration. It does establish that dependent candidate timing cannot precede freeze, and v2 makes verified timing freeze a prerequisite to full P2 progression. A calibration-only plan may explicitly budget zero timing while retaining the open timing requirement; it cannot then claim full P2 completion. Candidate formulas themselves wait for P2 diagnostics (§45), so no candidate timing is appropriate now.

| Boundary | Required authority/evidence | Current status |
|---|---|---|
| Design content approval | Explicit decisions on versioned/hash-identified D01–D10 and SP01–SP40, including any revised definitions | All UNAPPROVED |
| Implementation authorization | Separate concrete scope for source changes, manual correctness/negative fixtures and P1 regression; design acceptance alone is insufficient | Not granted by this report-only task |
| Calibration generation/execution authorization | Approved and registered applicable workload/matrix/observer/criterion definitions, validated implementation/lineage/guards and explicit generation/engine budget authorization | No input generated; no scientific execution |
| Timing implementation preparation | May be a separately authorized design/engineering task; source does not require every preparatory implementation to wait for frozen measurement parameters | No such authorization or implementation in this task |
| Candidate timing measurement | Exact timing protocol approved/frozen before observations, including all seven original fields and committed input/source/host identities | NOT_FROZEN; NOT_MEASURED |
| Full P2 progression | Calibration/design/identity/selection/diagnostic requirements plus verified workload/config/generator/criterion/engineering protocol freeze receipts | BLOCKED |
| Next scientific stage | Explicit next-stage authorization after verified stage prerequisites; no automatic progression from an exit code | Not authorized |

No warm-up count, repetition count, timer, excluded run policy, host selection, aggregation procedure or timing input default is inferred. Type-7 service-response quantiles in the existing metric protocol do not silently complete a separate missing timing P95 protocol. The original2ms target remains; timing implementation/measurement proof remains pending. D09/D10 approval should acknowledge the open timing predecessor, without treating a scientific/measurement unknown as proof of a design defect by itself.

## STATUS reconciliation without edits

`STATUS.md` identifies its scope as the concrete **v1** proposal checkpoint: unresolved scientific parameter groups32, root `RESULT_PATHS` points to v1, and historical tested/source/push checkpoint values are explicitly qualified. It also reports P0/P1 PASS, P2 BLOCKED, zero execution and B1/B2/B3 UNRESOLVED, B4/B5 DESIGNED. `reports/P2_design/design_status.json` similarly preserves the v1 design layer. These files were required to remain byte-identical in the v2/report-only tasks.

The current v2 registry has originalSP01–SP32 plus eight split-out groupsSP33–SP40, no deletion or merge, for **40 UNRESOLVED/UNAPPROVED groups**. The old32 is therefore historical truth for v1 and stale if quoted as the current v2 count. It is not evidence that8 groups are approved, deleted or untracked. Original decision catalog has ten unanswered decisions; both v2 approval checklist and human packet retain all ten UNAPPROVED. Historical reviewer recommendations ACCEPT for D01/D02/D03/D05 were never approval records.

Authority should be reported by claim scope:

| Claim | Authoritative scope/evidence |
|---|---|
| Original research constraints, thresholds, CI, partitions | `docs/user_request.txt` and corresponding source specifications; v2 draft cannot override them. |
| Latest proposed values and parameter count | Current hash-identified v2 definitions/registry; 40 proposed groups, not an active frozen contract. |
| Historical v1 status and prior audit conclusions | Preserved STATUS/design_status/v1 reports; do not overwrite their historical counts or recommendation history. |
| Current Git root/branch/HEAD/remote/worktree | This task's actual Git command receipts; neither an old embedded checkpoint nor `starting_commit` equals a fresh live verification. |
| Current runtime/scientific status | Existing verified gate evidence plus explicit actual command records; no v2 static-review conclusion supplies scientific PASS. |
| Present preapproval review conclusion | This new report package, with findings retained and all approvals UNAPPROVED. |

No existing STATUS/design file is changed. P2-B1/B2/B3 remain UNRESOLVED; P2-B4/B5 remain DESIGNED_UNAPPROVED with the newly identified design issues and unimplemented runtime verification. Source/scheduler/threshold/statistical/seed/unlock files remain outside this subtask's mutation scope. Scientific observations and new seeds remain zero.

## Decision readiness and review limits

`D01_D10_decision_readiness.csv` restores every original question verbatim and separates source facts, derivations, new scientific assumptions, engineering conventions, missing evidence, concrete alternatives, precise human questions and blockers. `SP01_SP40_traceability.csv` does this for every named group, resolving actual JSON pointers and recording exact proposed values, actual SHA256 and source lines. Five decision proposals D01/D02/D03/D05/D06 remain sufficiently concrete for human acceptance/rejection within their synthetic scope; D04 is dependent-revision required, D07/D08 require scientific-definition revision, D09/D10 require lifecycle/schema revision. This is review advice, never approval. Implementation/scientific unknowns are not automatically treated as current design failures.

Actual key/gloss/binding schemas contain14 fields; historical15-field summary is inaccurate (identity review ID-R03). No fifteenth field is invented here. Existing approval packet hashes are references to unapproved bytes, not signatures of approval.

This subreview's `decision-010` read command had a Python missing-bracket SyntaxError (exit1), with no mutation; corrected `decision-011` exited0. Both raw records remain. No substantive check failure is hidden. Full-byte parsing is distinguished from semantic review focus in `decision_source_reads.json`; the matrix, M1R adversarial cases and identity proofs have separately owned reports. Team review is not external third-party independence.

## Exact source identities

All hashes below are computed from actual current files at the audited revision. Line/section pointers describe reviewed claims; no source is modified.

| Source | Locator | SHA-256 |
|---|---|---|
| `docs/user_request.txt` | §59 lines1833–1860; §80 lines2332–2344; §100 lines2730–2741 | `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461` |
| `docs/metric_spec.md` | lines48–52 | `c4b912fc672979ddc763d882e546b7a92bf53090e5b5dddd5777e2e867df182a` |
| `docs/research_contract.md` | lines32–48 | `8ccd2f6fce470013af89c653eb3ff84a0b66809c56d321993cd973ebc18031e4` |
| `docs/statistical_protocol.md` | lines3–23,34–47 | `f9c0eeb6e76f68330ba3e5d8d90e58d175c3947a1948bb41b26ad50dbc041e8a` |
| `STATUS.md` | full historical v1 declaration | `5f4c9fc321d22010400f260e8ed82a714b4a19453ae7b3102e04db93211f5222` |
| `reports/P2_design/design_status.json` | proposal_v1 block | `95f27100ef7e02a883115b1dea2a87e6a94b2a6ddc4920c5a73da955737edcc4` |
| `docs/P2_design/v2/P2_stage_state_contract_v2.json` | state_fields,current_design_values,per_trial_complete,progression_conjunction,timing,proposed_orchestrator_exits | `c64803a93c74ee9dba6a7bc61de2d2e550264f2c5d4a920e1248665fa7e86b93` |
| `docs/P2_design/v2/P2_typed_identity_schema_v2.json` | $defs/GATE_STATE and STAGE_RECORD | `9b478cf7e96776f6cc69f29426715efed6eec2309270be1efb3dd77985ebfbc9` |
| `docs/P2_design/v2/P2_criterion_spec_v2.json` | preconditions,decision_order | `98a578944e7910db933f5b3b02aee4bb03de8005853024b38cc3b02630b04e38` |
| `docs/P2_design/v2/P2_mapping_opportunity_decision_table_v2.md` | lines21–33 | `594863a579ac32fdd980454fe6e0f0d24d165729a60f1c6f6526c8688fd296f4` |
| `docs/P2_design/v2/P2_scientific_parameter_registry_v2.json` | count_scope,all40parameters | `15ee54e75f658d5f66edb00534003d3aed642f86736b2932ae61f0692e4559c2` |
| `reports/P2_design/independent_review_v2/D01_D10_review_matrix.csv` | recommendation and human approval columns | `750738fec2d2f90e89fe0000a21d55e71ae427b69b5626e90e22c0c4c9450181` |

# Coverage and threshold decision support — no scientific calculation

Recommendation: revise D07/D08 coverage/negative reachability before asking humans to approve a supposedly complete three-state rule. All options remain UNAPPROVED. This is a fresh coordinated same-assistant review, not external independence. Exact source bytes/line references resolve through the source identities below and `M1R_adversarial_cases.md`.

## Meaning, rationale, bias and numeric provenance

| Rule | Scientific meaning and cost of the choice | Source and status |
|---|---|---|
| FINE tau=1/100 | A FULL state is a hit for at least1% relative reduction of mean projected H remaining completion under the surrogate. Greater sensitivity to small modeled differences; no assurance that estimate error or actual DMR is comparably small. | S5:17–21; S6:9–14; S9:11–22. PROPOSED; no original-source or empirical justification for1%. |
| FINE f=1/100 | Each seed's hits/F is compared with1%, then seed mean CI and stability checks apply. This is a conditional state frequency, not a probability of meeting deadlines. | S5:36–44,76–82; S7 SP29. PROPOSED; no numeric provenance beyond v1 proposal. |
| COARSE tau=f=1/20 | Requires both a5% modeled gain and5% conditional frequency. Harder to support than FINE on identical complete observations, but can miss repeated small gains. Varying both axes simultaneously does not separate amplitude sensitivity from frequency sensitivity. | Same sources; no default selection and no source proving5% appropriate. |
| Support coverage F/E>=4/5 | Up to one fifth of in-scope states may have valid but uncomputed opportunity. Hits/F describes only the covered subset. Required separately in all120 selected seed/loaded-condition cells, not just average coverage. | S3:107–115; S5:31–44,76; S6:13,17–34. New unapproved numeric choice; no supplied empirical or literature evidence validating4/5. |
| Negative coverage F/E=1 | Avoids calling excluded states negative. It is complete state coverage only relative to this observer's FULL definition; it still excludes alternative suffix maps/orders from the search itself. | S5:33,81; S3:53,115. Qualitative conservatism is logically understandable, but Case1 proves this condition unattainable for all registered ADAS streams. |
| Support at least8/10 seeds with p>=f | Prevents a high mean driven by too few seed units; says eight observed calibration seeds meet the proposed rate. It is not an80% population guarantee or power calculation. | S5:20,27,76; S9:13,39. Unapproved engineering/research choice; no source determines8. |
| Negative at most2/10 seeds with p>=f | Along with CI_high<f, asks for consistently low conditional rates in the observed ten seeds. It does not prove eight seeds have zero hits, nor that future seeds lack opportunity. | S5:21,28,81; S9:40,52–53. Unapproved choice, no source determines2. |

The asymmetry has an *implicit logical rationale*: an observed valid improvement can witness a bounded opportunity despite some unobserved states, while absence cannot be inferred by imputing those states to zero. S3:115 and S6:34–44 express that limitation. The files explicitly identify4/5 and1 as proposed and without empirical basis (S22:161–174). There is no original requirement that uniquely supplies these values or proves their adequacy. The audit must not invent a literature/power rationale. Moreover, the categorical negative coverage rule conflicts with its own stream definition, not merely with uncertain statistical power.

## Structural negative-branch failure

The exact proof and hashes are in Case1. The first paired ADAS arrival has two roots; any first positive-duration start leaves one ready root and pending H work. The required post-start snapshot adds an E-only observation. Therefore E-F>=1 in each finite valid ADAS run. Negative coverage1 across every selected seed/condition is impossible. This survives both sizes, both arrival candidates and either first-root choice, and uses no random draw or actual workload. Consequently a completely observed zero-gain FULL subset can never yield the specified global NOT_SUPPORTED result. It can only remain INCONCLUSIVE or fail an earlier precondition.

This is a CRITICAL design consistency issue (M1R-F01), not evidence that science has failed. No threshold was changed. Choosing FINE instead of COARSE cannot repair a coverage predicate that is unreachable independently of tau/f.

## Coverage selection and state weighting

Single-ready states, >4-ready congestion, >2 pending H services and estimate overruns are structurally different from FULL states. Their exclusion may correlate with the scarce-resource mechanism. The direction/magnitude of bias is UNKNOWN; no outcome was inspected. Dedup removes exact repeated states but does not make different states independent, equal-duration observations or a uniform sample of time. More dispatch transitions can create more states; long residual paths and congestion can alter the eligible population. State hashes include now/elapsed, so time advances legitimately alter identity.

A purely algebraic illustration: if E=1000, F=800 and hits=8, the covered conditional rate is1%, while hits/E=0.8%. If the200 uncovered states had been eligible for a comparable opportunity definition, the all-E rate could lie between0.8% and20.8%; that is a logical bound, not a replacement estimator or observed dataset. The current rule chooses the conditional estimand. Coverage4/5 does not by itself prove that conditional hits/F represents all states. No missing-state sensitivity analysis or new statistic is enacted here.

There is no extra minimum F in v1 (S9:17); v2 requires E>0,F>0 but no larger minimum (S5:52). Frequency resolution is1/F: for F=10, either bundle needs at least one hit, so their f choices are numerically indistinguishable at that denominator, though their gain cutoffs differ. Ten seed-level resampling units remain ten; thousands of states cannot replace independent seeds. These are design limitations, not reasons to invent a new sample budget.

## Exact decision boundaries and interpretation

The *abstract* decision table is mutually exclusive and exhaustive when its inputs exist: CI_low>=f cannot coexist with CI_high<f for ordered intervals; seed counts>=8 and<=2 cannot coincide. Boundary CI_low=f supports only with all other conditions; CI_high=f is not negative. Other values are INCONCLUSIVE, and no execution is NOT_EVALUATED. Logical exhaustiveness over arbitrary Boolean inputs does not establish that every branch is attainable under this specific workload/observer design. M1R-F01 is the concrete counterexample to relying on table-only tests.

S14:3–16 supplies the existing paired-seed bootstrap:10000 replicates, analysis seed20261018, shared seed-index vector across compared methods/conditions, percentile95%, type7(.025,.975). S5:55–61 pins the proposed index algorithm and mandates the descriptive equal-condition macro. All are retained. This report neither creates indices nor calculates CIs, and does not propose changing resampling or seed partitions.

A calibration-stage operational decision can say whether the preregistered synthetic workload and bounded observer supply enough evidence to spend further research effort. It can choose to stop when support is absent/inconclusive, but must disclose the surrogate's sensitivity limitations. It is not an independent confirmatory statement that all mappings lack a mechanism. A-before-B qualification and the opportunity analysis use the same ten calibration seeds; the CI is pointwise and conditional on the selected configuration and FULL subset. It does not quantify selection uncertainty, simultaneous12-condition coverage, hardware validity or future-population effect. S14:34–42 and S5:61,90 make those limits explicit. M2 comparisons change multiple baseline features and cannot independently identify mapping's causal contribution; P3 ablation requirements remain untouched.

## Parameter registry review

All40 records SP01–SP40 are present, unique, UNRESOLVED and UNAPPROVED in S7. SP01–SP24 supply the synthetic topology/cost/arrival/control/selection population; their unchanged values do not become approved by this audit. SP25/26/33/34/35/37 specify the changed observer/target/suffix/L cap/dedup; SP28–SP31 andSP36 define thresholds, stability, aggregation and coverage; SP32 pins the existing bootstrap method's index implementation; SP39 states conditional-interpretation limits. SP27 remains descriptive M2, SP38 offline feasibility arithmetic andSP40 control/window semantics. None independently supplies a numeric scientific justification for tau/f/8/2/4/5. The parent SP01_SP40 traceability report covers every individual record; this review preserves every group.

## Exact unanswered human questions — all UNAPPROVED

1. D07/SP25,SP33–SP37: after the documented Case1 contradiction is resolved in a new proposal, what exact population of public states and admissible bounded decisions should the opportunity statement cover? Which excluded mechanisms and false-negative risks are acceptable? No default domain change is authorized.
2. D07/SP34–SP35: is the fixed-suffix/current-L-node-cap observer an acceptable *operational proxy* after reviewing the complete-information Case7 counterexample and Case8 global-L limitation, or is additional documentation needed before approval? Approval would not assert global absence or L-budget compliance.
3. D08/SP28–SP31: choose FINE, COARSE, or reject both pending an explicit prior scientific rationale for amplitude/frequency/stability. Explain the minimum practically relevant surrogate effect before any observations; do not choose by outcomes or by which option might pass.
4. D08/SP36: what coherent negative-evidence/coverage policy replaces or explicitly acknowledges the unreachable coverage1 branch? Possible report-only alternatives include revising domain, revising negative interpretation/requirements with an independently justified rule, or explicitly adopting support-only decision semantics. Each changes scientific rules and must remain UNAPPROVED until a complete revision is reviewed. No new number is supplied here.
5. D08/SP39: confirm that any future selected-calibration CI is conditional descriptive evidence only, with shared paired-seed resampling unchanged; no independent confirmation claim follows.

Until these questions have a consistent written object, D07/D08 cannot be treated as resolved. No implementation, candidate formula, calibration invocation, freeze or unlock is authorized by this report.


## Source identities

Every S-reference above/below resolves to these actual repository bytes. Line numbers are 1-based physical text lines; full bytes and numbered text are preserved in m1r-001 through m1r-005 read logs. Source code was read, never imported or executed.

| ID | Path | SHA-256 |
|---|---|---|
| S1 | `docs/user_request.txt` | `4c3481f0c67553eaa6d2dd6f181cc8d3f792e40fdc9586547c1c2e91fb52b461` |
| S2 | `docs/research_contract.md` | `8ccd2f6fce470013af89c653eb3ff84a0b66809c56d321993cd973ebc18031e4` |
| S3 | `docs/P2_design/v2/P2_diagnostic_spec_v2.json` | `9bec37d044f4c7742d931149c195c2c3ec1540d41dc3f0a899a2b29f8c7e3e90` |
| S4 | `docs/P2_design/v2/P2_public_snapshot_spec_v2.json` | `fa4ce177c2d4a49a5f8f5b30bfa44e2b0d529f1e735ddfa259ae1811edc2f1af` |
| S5 | `docs/P2_design/v2/P2_criterion_spec_v2.json` | `98a578944e7910db933f5b3b02aee4bb03de8005853024b38cc3b02630b04e38` |
| S6 | `docs/P2_design/v2/P2_mapping_opportunity_decision_table_v2.md` | `594863a579ac32fdd980454fe6e0f0d24d165729a60f1c6f6526c8688fd296f4` |
| S7 | `docs/P2_design/v2/P2_scientific_parameter_registry_v2.json` | `15ee54e75f658d5f66edb00534003d3aed642f86736b2932ae61f0692e4559c2` |
| S8 | `docs/P2_design/P2_complete_design_proposal_v1.md` | `e378e85071d6c97fb6cd5801d9449eef176a90baddcd786181c6685eaa29feac` |
| S9 | `docs/P2_design/P2_mapping_opportunity_decision_table_v1.md` | `4c981f2f2303e1b1535168dd320e3c11151ea86ad35a502513893370a5906ea2` |
| S10 | `docs/P2_design/v2/P2_workload_templates_v2.json` | `f282955ab09d0110f50447269b18d0389231bed9711532853d6cdbda92d9027c` |
| S11 | `docs/P2_design/v2/P2_generation_spec_v2.json` | `33e3ccf437510986ffa401eea1ef48e995a1ad08df38a834374d4a1c483a91f2` |
| S12 | `docs/P2_design/v2/P2_resource_profiles_v2.json` | `9eea5cfd43ce50d796a00d7cac86f9a7ca8798da4a3ea0c2fd9e598d965f13ae` |
| S13 | `docs/P2_design/v2/P2_communication_profiles_v2.json` | `74f7dde644b11d0b459fb68e9f250d9799e34f09652609b63122e0de5bf6e3b8` |
| S14 | `docs/statistical_protocol.md` | `f9c0eeb6e76f68330ba3e5d8d90e58d175c3947a1948bb41b26ad50dbc041e8a` |
| S15 | `docs/model_spec.md` | `3f74116fa6cb85e4f2db1c96d246ac830a282be28847a0af21184fde2e17197b` |
| S16 | `docs/metric_spec.md` | `c4b912fc672979ddc763d882e546b7a92bf53090e5b5dddd5777e2e867df182a` |
| S17 | `docs/baseline_spec.md` | `54a1cdb86d0235671a7d1ece31e489289c026bf083f33388580b6f3fdbb42e12` |
| S18 | `docs/P1_implementation_spec.md` | `92e9c4d0472f7893f54fc54d302d38bd224092285d78cc85ec7cdb67fef4e972` |
| S19 | `src/soc/simulator/engine.py` | `977d01f3603f516e68e922542322976b813c01aad8d2dd177a5c0ac314399551` |
| S20 | `src/soc/model/observation.py` | `40554e4ba71989223b7ba8362b7d35ae7257db030fd3e1fa04e262fb5002d0cb` |
| S21 | `docs/P2_design/v2/P2_typed_identity_schema_v2.json` | `9b478cf7e96776f6cc69f29426715efed6eec2309270be1efb3dd77985ebfbc9` |
| S22 | `docs/P2_design/v2/P2_complete_design_proposal_v2.md` | `7f929b85554193ef1256deb3f7cc184e47c362f91e93950896a80450c9eb5fe8` |
| S23 | `reports/P2_design/design_revision_v2/diagnostic_semantics_review.md` | `3619ae7416eabf962dbd7b06e469bf132cc1c37c07c0dc5afd00c12cdc8e8191` |
| S24 | `reports/P2_design/independent_review_v2/feasibility_and_mechanism_analysis.md` | `6b485d5eb4f4f05cadf9c3db732b9d582bb1cec45821eef84b534ed1eb59879f` |
| S25 | `reports/P2_design/independent_review_v2/findings.json` | `a56925d56f431714fbdd334bee5303a3fb58234caf26c12fa98375ce0219933b` |
| S26 | `AGENTS.md` | `5435e5e690a64e0e7f432bae22b8f459f646e12233d99a7a4b1a70266d8c9a22` |
| S27 | `STATUS.md` | `5f4c9fc321d22010400f260e8ed82a714b4a19453ae7b3102e04db93211f5222` |
| S28 | `docs/workload_spec.md` | `a098008f3abe47f4cfb830685009b19bf4d3555a8e370ad242a2fce1debea606` |
| S29 | `reports/P2_design/design_revision_v2/human_decision_packet.md` | `7c54a0f17c11036e1cb7f34b82734792746c946b20f5cf021c1ced298cc04367` |

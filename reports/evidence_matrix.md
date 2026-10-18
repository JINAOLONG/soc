# Evidence matrix

| Claim | Evidence stage | Comparison | Config / partition | Raw or direct evidence | Summary / statistic / CI | Status | Limitation |
|---|---|---|---|---|---|---|---|
| Checkout matches JINAOLONG/soc and original LICENSE retained | P0 engineering audit | NOT APPLICABLE | original work branch | P0_repository_audit.txt, P0_environment.json, Git diff | direct Git observations; CI NOT APPLICABLE | VERIFIED | final live HEAD must be queried with Git |
| Seeds follow the prescribed deterministic rule, 10/20/10/30 and disjoint | P0 metadata audit | independent derivation test | configs/seed_partitions.json | seed metadata and tests/test_governance.py | 70 unique metadata values; no workloads | VERIFIED | seed metadata auditing does not validate a generator |
| Tooling rejects invalid partition/stage entry and forged empty unlocks | P0 engineering tests | synthetic fixtures | no scientific workload | P0_checks_001.json, tests | 17 tests passed in final run (includes other governance tests); no CI | VERIFIED_FOR_TESTED_CASES | no simulator or production scientific runner yet |
| Four source manuscripts support scoped literature descriptions | P0 source review | NOT APPLICABLE | docs/literature_evidence.json | source URL/SHA256 and literature_reviews notes | four reviewed; no quantitative soc comparison | PARTIAL | required HEFT/CPOP and PEFT originals missing |
| P0 prerequisites pass | P0 audit | required minimum vs current | research_protocol.json | P0_protocol_audit.json | 4 < 6; 2 required originals unverified | BLOCKED | no P0 freeze claimed |
| H main benefit / mapping contribution / L budget / B5 comparison | P2–P5 NOT RUN | B2/B5/A1/A2/A3 NOT RUN | all scientific execution partitions untouched | NONE | estimates and 95% CI NOT AVAILABLE | NOT RUN | cannot infer a scientific outcome from tooling tests or literature |
| Decision P95 <=2 ms | engineering NOT RUN | NOT RUN | timing protocol not frozen | NONE | NOT AVAILABLE | NOT RUN | cloud host metadata is not latency evidence |
| Independent/formal evaluation supports hypothesis | P4/P5 NOT RUN | NOT RUN | reserved workload partitions locked | NONE | NOT AVAILABLE | NOT RUN | development and prior gates did not run |

No chart is generated because no performance dataset exists. A placeholder plot
would not be evidence. Hypothesis status is BLOCKED, not NOT_SUPPORTED.

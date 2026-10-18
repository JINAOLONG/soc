# Current evidence matrix

| Claim | Stage and scope | Direct evidence | Result | Limitation |
|---|---|---|---|---|
| Current repository matches soc and starts at actual 1b36f39 | P0 repository audit | P0_local_pdf_repository_audit.json | Verified; work branch initially clean | Final live delivery HEAD resolves through Git |
| User HEFT/CPOP original matches intended article | P0 actual local source | P0_source_acquisition_014.json, heft_cpop review | Identity, 15 pages, actual file SHA256, full-paper/page evidence verified | Original download provenance/unmodified publisher binary not authenticated |
| User PEFT original matches intended article | P0 actual local source | Same acquisition record, peft review | Identity, 13 pages, actual file SHA256, full-paper/page evidence verified | Same provenance limitation; issue 2014 vs online 2013 recorded |
| Six original studies meet existing literature rule | P0 primary review | literature_evidence.json, literature_matrix.md, P0_local_pdf_prior_sources_recheck.json | Two new full-paper reviews plus four requalified scoped original reviews | No secondary metadata counted; four scopes not upgraded |
| Existing P0 audit passes | P0, current instance with six source files | P0_protocol_audit.json/.md and P0_local_pdf_checks.json | Actual exit 0/PASS, no errors | Not P1 or scientific validation; cache is needed |
| Existing lightweight tooling tests pass | P0 governance | P0_local_pdf_checks.json | 17 passed, zero failed/skipped | No simulator correctness inferred |
| Scientific definitions/source/config/seed unchanged | P0 scope audit | 35 initial hashes and boundary checks | No protected-file changes; source and seed digests match | Documentation status/source references updated separately |
| H benefit, mapping contribution, L budget, B5 comparison | Scientific stages NOT RUN | No scientific data | NOT RUN; point estimates and 95% CI NOT AVAILABLE | Literature results are not soc samples |
| Decision latency and hardware claims | Engineering NOT RUN | No timing/hardware dataset | NOT RUN | Host/profiling/safety claims unsupported |
| Validation/formal results | P4/P5 NOT RUN | No unlocks or reserved workload artifacts | LOCKED / NOT RUN | No progression allowed by this task |

No performance plots are generated. The scientific hypothesis remains
INCONCLUSIVE because no scientific workload has run. P0's source blocker is
closed without changing acceptance criteria. Historical matrix is archived.

# P0 literature blocker remediation decision

**P0_STATUS=BLOCKED.** This task attempted the supplied original-source leads
and reasonable lawful alternatives, verified bibliographic identities and the
four existing source artifacts, and reran the unchanged tests/audit. Neither
mandatory target original was acquired. No original algorithm page was reviewed
for HEFT/CPOP or PEFT; their required formulas and complexity remain UNVERIFIED.

## Live repository and scope

Task-start HEAD: `ebab07e008745aa4200f2f7ac156275400532c36`; branch `work`;
origin `https://github.com/JINAOLONG/soc.git`; worktree clean. The task-start
audit, protected-file hashes and commands are in
P0_literature_closure_repository_audit.json. Prior audits, inventory/matrix,
STATUS, blocker report and artifact manifest were copied byte-for-byte into
history/p0_before_literature_closure_ebab07e/ before changing active records.

Authorization was limited to literature acquisition/review, documentation,
existing lightweight tests and P0 audit. No P1 command, simulator/scheduler
implementation, workload generator, scientific stage, unlock or performance
experiment was executed. All 25 protected source/script/config/test file hashes
match the initial audit, including seed partitions and existing gate code.

## Acquisition results

| Target/route | Actual result | Accepted original? |
|---|---|---|
| HEFT Marmara institution record and supplied bitstream PDF | Proxy `Tunnel connection failed: 403 Forbidden`, including recorded retry | NO |
| HEFT correct IEEE record / ordinary PDF endpoint | HTTP 202 with zero bytes / HTTP 418 | NO |
| PEFT supplied ResearchGate author-upload listing | Proxy CONNECT 403, including recorded retry | NO |
| PEFT IEEE record / ordinary PDF endpoint | HTTP 202 with zero bytes / HTTP 418 | NO |
| OpenAlex DOI lookup for both targets | Public metadata/locations retrieved; no original PDF | NO |
| Crossref DOI lookup for both targets | Full target bibliography confirmed; metadata only | NO |
| PEFT Porto institutional record from OpenAlex | Proxy CONNECT 403 | NO |
| HEFT RIT institutional course-copy lead from OpenAlex | Proxy CONNECT 403 | NO |
| Publisher PDF links explicitly advertised by Crossref | Proxy CONNECT 403 | NO |
| HEFT institutional persistent-handle route | HTTP 500 | NO |
| PEFT Semantic Scholar author-copy discovery | HTTP 429; no workaround/repeated rate-limit probing | NO |
| UMinho public repository UI/config/API | HTML shell inspected; published public REST endpoint discovered; exact-title search returned 0 records | NO |

All 25 request attempts, including bibliographic/UI discovery and the existing
sources' bibliography checks, are preserved in P0_source_acquisition_006.json
through _013.json. A successful metadata request, HTML shell, OA flag or empty
response never counts as a retrieved original. Ordinary HTTPS GETs kept TLS
verification enabled. No login, authentication, paywall, challenge or download
restriction was bypassed.

Marmara, ResearchGate (bare/WWW), Porto, RIT and the Crossref publisher-PDF host
were added to the environment network draft, preserving earlier domains and
package-manager presets. There are six additions and 24 total custom domains.
Draft persistence was read back; it does not prove runtime access or publication.
P0_literature_network_requirements.json lists the exact hosts and pending action.
No script, secret requirement or runtime variable was changed.

## Original review and literature integrity

The existing inventory schema was enriched without changing source status:

- HEFT/CPOP and PEFT remain UNVERIFIED_SOURCE, with no accepted artifact path,
  PDF hash, version or page numbers asserted. Their linked review files list
  every required technical item and explicitly mark original-page evidence
  NOT AVAILABLE. No recurrence or complexity claim is inferred from other papers.
- The four already reviewed originals retain their prior scoped-review status.
  Each PDF hash matches the recorded identity; pdfinfo and pdftotext open the
  actual files. Viewer-page mappings and complete available bibliography/version
  fields were added, with unknowns and metadata/manuscript discrepancies stated.
- Accepted original artifacts still total four. No scoped review is upgraded to
  complete-page review, and no secondary/metadata source becomes a primary study.
- Copyrighted PDFs stay in ignored cache, never staged or redistributed. The
  source inventory, hashes, lawful URLs, notes and acquisition metadata are tracked.

See docs/literature_evidence.json, docs/literature_matrix.md,
docs/literature_reviews/heft_cpop.md, docs/literature_reviews/peft.md and
P0_literature_source_hashes.json. The latter distinguishes four inspected source
files from the two unavailable mandatory originals; empty-response SHA256 values
are only response diagnostics, never paper hashes.

## Existing audit and test outcome

The original command `.venv/bin/python -m unittest discover -s tests -v` passed
all **17 tests**, with zero failures/skips. The original command
`.venv/bin/python scripts/run_pipeline.py --stage p0` returned **exit 2** and
reported BLOCKED with exactly these evidence gaps:

1. Original studies verified: 4; required: at least 6.
2. Required originals unverified: heft_cpop, peft.

Actual stdout, stderr, exit codes, hashes and boundary checks are in
P0_literature_closure_checks.json; the active P0_protocol_audit.json/.md were
regenerated by the original runner. The prior audit remains archived. No audit
code, exit behavior, acceptance criteria or required count was edited.

Scientific workloads run: **0**. The results directories contain only their
existing .gitkeep files. Calibration/development/validation/formal outcomes were
not opened; reserved workload realizations were not generated. Seed metadata
was only checked by existing governance tests; its file hash is unchanged.
VALIDATION_UNLOCKED and FORMAL_UNLOCKED remain absent. Simulator correctness
remains NOT RUN, and no simulator implementation was started.

## Next safe action and stop

Enable the lawful source routes through reviewed/saved/published environment
settings and retry after a relevant runtime change, or provide lawfully obtained
HEFT/CPOP and PEFT originals. Then verify file/version, inspect the required
algorithm pages, complete the six-source matrix, and rerun **P0 only**. No
threshold relaxation, secondary-source replacement or reserved-partition access
is proposed. Even a future P0 PASS requires this task to stop before P1.

This report is written before its enclosing commit and cannot embed that commit's
own hash. Task-start provenance above is literal. The tested documentation
checkpoint/push audit is recorded in P0_literature_closure_git_checkpoint.json;
the final live delivery hash is obtained with `git rev-parse HEAD` and reported
to the user, not inferred from an older scientific/source checkpoint.

```text
PROJECT_NAME=soc
CURRENT_STAGE=P0
P0_STATUS=BLOCKED
HEFT_CPOP_ORIGINAL_RETRIEVED=NO
HEFT_CPOP_FULL_TEXT_REVIEWED=NO
PEFT_ORIGINAL_RETRIEVED=NO
PEFT_FULL_TEXT_REVIEWED=NO
PRIMARY_SOURCE_PAGE_EVIDENCE_COMPLETE=NO
REVIEWED_SOURCE_COUNT=4
LITERATURE_REQUIREMENT_PASS=NO
P0_AUDIT_EXIT_CODE=2
P0_GOVERNANCE_TESTS=17 PASSED
SCIENTIFIC_WORKLOADS_RUN=0
SIMULATOR_IMPLEMENTATION_STARTED=NO
SEED_PARTITIONS_CHANGED=NO
RESERVED_PARTITIONS_ACCESSED=NO
VALIDATION_UNLOCKED=NO
FORMAL_UNLOCKED=NO
GIT_COMMIT=cb29fe7a04a6582b76268778fa071ea8d5b5eb9e
GIT_COMMIT_SCOPE=REMOTE_VERIFIED_DOCUMENTATION_CHECKPOINT_BEFORE_REPORT_ONLY_CLOSURE
FINAL_DELIVERY_HEAD_COMMAND=git rev-parse HEAD
GITHUB_PUSH_STATUS=SUCCESS_FOR_RECORDED_CHECKPOINT
WORKTREE=CLEAN_AT_RECORDED_CHECKPOINT
FINAL_DELIVERY_WORKTREE_COMMAND=git status --short
NEXT_SAFE_ACTION=Obtain lawful HEFT/CPOP and PEFT originals, inspect algorithm pages, rerun P0 only
STOP=YES
```

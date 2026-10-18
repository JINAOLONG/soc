# P0 literature blocker closure — actual local originals reviewed

**P0_STATUS=PASS.** The unchanged formal P0 command returned exit **0** after
actual review of the two supplied PDFs and requalification of the existing four
primary reviews. Existing governance tests: **17 passed, 0 failed, 0 skipped**.
This result applies to P0 in the current instance with all six source files
available. No simulator, scheduler, scientific workload or P1 stage was started.

## Repository and preserved baseline

The live task began at commit
1b36f391224d64f9f477bfb0d4c1a0948aa81baf, branch work, clean worktree, with
origin https://github.com/JINAOLONG/soc.git. The earlier BLOCKED audit exited 2,
counted four sources and lacked the two required originals. It is not rewritten
as a past PASS: matrix, inventory, source notes, audit, STATUS, previous closure,
hash manifest and relevant reports are archived under
reports/history/p0_before_local_pdf_review_1b36f39/ and remain in Git history.

P0_local_pdf_repository_audit.json records the actual start SHA and baseline
checks. All 35 protected code/config/test/scientific-definition files remain
byte-identical, including the P0 audit logic, seed partitions, statistical
protocol and thresholds. docs/baseline_spec.md only updates source-review
status/references; its baseline requirements are unchanged.

## Actual PDF identities and provenance

| Target | Actual input file | Bytes / pages | SHA256 | Version/identity conclusion |
|---|---|---|---|---|
| HEFT/CPOP | /workspace/attachments/b3bdf00a-9211-4180-a198-d2b3c7a28d17/Performance-effective_and_low-complexity_task_scheduling_for_heterogeneous_computing.pdf | 652304 / 15; printed 260–274 | 186bcf6a9fefb25c99cfd4d247e92f3fabc91cef5c3555ccb4d2d04ba6fec694 | Target identity verified against title/authors/header/pagination and PDF Subject DOI; publisher-formatted journal copy |
| PEFT | /workspace/attachments/a587bb22-0000-435f-af70-ab3c8f3325eb/List_Scheduling_Algorithm_for_Heterogeneous_Systems_by_an_Optimistic_Cost_Table.pdf | 1492291 / 13; printed 682–694 | 51c5036310ea4f4deb9f2e6c65730fc1b2321dd1e2975bc3940285b03ede5fc8 | Target identity verified against title/authors/header/pagination and printed DOI; publisher-formatted journal copy |

HEFT/CPOP is Topcuoglu, Hariri and Wu, IEEE TPDS 13(3), 260–274, March 2002,
DOI 10.1109/71.993206. PEFT is Arabnejad and Barbosa, IEEE TPDS 25(3), 682–694,
March 2014, DOI 10.1109/TPDS.2013.57; its first page states online publication
in February 2013. Filename differences from the suggested aliases did not
determine identity; the actual contents did.

Both carry provenance USER_PROVIDED_LOCAL_COPY_SOURCE_UNVERIFIED. The user
provided reading copies; no original download URL was supplied. Real sediment
attachment locators identify the inputs in the existing primary_url field;
download_url is null. They are not fabricated publisher download endpoints.
The pages are publisher-formatted and have licensed IEEE Xplore footers, but
metadata also records later 2018 iText modification. Unchanged/authenticated
publisher binaries and upstream chain of custody are not claimed.

All pages opened through pdfinfo/pdftotext and rendered successfully. Full text
of every page was read; contact sheets were checked, with enlarged HEFT PDF
5/7 and PEFT PDF 6 inspected for algorithm/equation details. Fontconfig emitted
cache warnings during rendering, but both renders exited 0 and produced all
15/13 pages; the enlarged pages were legible. No render warning was relabelled
as source-verification evidence on its own.

P0_source_acquisition_014.json preserves actual file paths, hashes, sizes,
metadata, continuous printed-page checks, page-text identities and review scope.
Private byte-identical copies live at:

- .cache/literature/HEFT_CPOP_Topcuoglu_2002.pdf
- .cache/literature/PEFT_Arabnejad_Barbosa_2014.pdf

Both are Git-ignored. No PDF, full extracted text, page image or contact sheet is
tracked or uploaded to a public location. No redistribution license is inferred.

## Technical conclusions grounded in original pages

| Required evidence | Original page(s), PDF page(s) | Conclusion |
|---|---|---|
| HEFT mean computation / transfer cost | p.262 / PDF3, Eqs.(1)–(3) | Arithmetic mean execution over processors; transfer startup+data/bandwidth, same-unit zero; rank communication uses mean-startup/mean-rate expression |
| HEFT rank and priority | p.264 / PDF5, Eqs.(8),(9), Fig.2 | Upward rank includes current mean execution plus maximum successor edge/rank; exit base is exit mean execution; nonincreasing rank, source rank ties random |
| HEFT availability, EFT and insertion | pp.262,264 / PDF3,5, Eqs.(4)–(6), Fig.2 | Account for data readiness and resource feasibility; insertion searches an adequate idle gap; minimize insertion EFT rather than append-only finish |
| CPOP priority and path processor | pp.264–266 / PDF5–7, Eq.(10), Fig.5 | Upward+downward rank; one connected critical path; processor minimizes cumulative path computation; noncritical tasks use insertion EFT |
| HEFT/CPOP assumptions and complexity | pp.261–262,264,266 / PDF2–3,5,7 | Static known DAG, bounded heterogeneous fully connected no-contention platform, overlap and non-preemption; authors state HEFT O(e q)/dense O(v²p), CPOP O(e p) |
| PEFT OCT and rank | p.687 / PDF6, Eqs.(7),(8) | max over children of min over child processors of suffix+child execution+transfer; same-processor transfer zero; exit OCT zero; rank is processor-average OCT |
| PEFT processor selection and look-ahead | pp.687–688 / PDF6–7, Eq.(9), Algorithm1 | Insertion EFT plus OCT gives OEFT; select minimum OEFT over processors; stored suffixes provide descendant look-ahead |
| PEFT availability and communication | pp.683–684,687 / PDF2–3,6 | OCT explicitly ignores processor availability; EFT includes partial-schedule availability; mean communication, same-unit zero, simplified network |
| PEFT complexity | p.688 / PDF7, §4.4 | Authors state OCT O(p(e+v)), assignment O(v²p), total O(p(e+v)+v²p), dense O(v²p); not a measured or independently proved bound for future soc code |
| PEFT versus HEFT and limits | pp.687,691–693 / PDF6,10–12 | OCT mean/OEFT differs from original HEFT rank_u/EFT; authors report worse/FFT cases; original resources are not shared across jobs |

Detailed recurrences, base cases, tie qualifications, algorithm steps and source
limits are in docs/literature_reviews/heft_cpop.md and peft.md. Items not explicit
in the source (e.g., particular processor tie conventions and detailed OCT
construction implementation) are marked NOT_EXPLICITLY_SPECIFIED_IN_SOURCE.
They are not filled from memory or silently assigned project rules.

Original static definitions are distinguished from soc's future online mapping.
No H-priority, fairness rule, compatibility-mask policy, online dispatch behavior,
new baseline, candidate or parameter is introduced. Paper results remain source
literature, not this project's performance data.

## Six-source qualification

The authoritative matrix remains docs/literature_matrix.md and the inventory
remains docs/literature_evidence.json. No competing second matrix was created.

| Source | Actual evidence checked | Count decision |
|---|---|---|
| HEFT/CPOP | Actual 15-page input, matching identity/hash, full-paper review and mandatory algorithm pages | 1 verified original |
| PEFT | Actual 13-page input, matching identity/hash, full-paper review and mandatory algorithm pages | 1 verified original |
| DS3 | Same original preprint/hash, original model/lifecycle notes and valid page references; substantive recheck PDF3,5 | Existing scoped primary review retained, 1 |
| StarPU | Same HAL original/hash and source notes; substantive recheck PDF4,6 | Existing scoped primary review retained, 1 |
| Autoware multi-deadline DAG | Same original/hash, defined review scope/page evidence; substantive recheck PDF3 | Existing scoped primary review retained, 1 |
| Federated lower bound | Same original/hash and theorem/comparator review; substantive recheck PDF1,5 | Existing scoped primary review retained, 1 |

P0_local_pdf_prior_sources_recheck.json explicitly records the four prior
qualifications. Their scoped reviews are not upgraded to all-page review or
replication. The current protocol counts reviewed original studies; it does not
require each optional paper to be a publisher version or to have known final
journal pagination. Those unknowns remain visible. Count is **6 qualifying
originals**, not a count of table rows or metadata records. Required originals
heft_cpop, peft and ds3 are all covered. No remaining mandatory-original/count
blocker appears in the existing audit.

## Unchanged audit, actual outputs and boundary

- Evidence checker literature_errors(root): empty error list.
- All six actual PDF SHA256 values rechecked against the inventory; note hashes
  are in the existing P0_literature_source_hashes.json.
- Existing command: .venv/bin/python -m unittest discover -s tests -v
  Result: 17 executed, 17 passed, 0 failed, 0 skipped.
- Formal existing command: .venv/bin/python scripts/run_pipeline.py --stage p0
  Result: **exit 0, PASS**, with no audit errors.
- Existing fetch_primary_sources.py verified all six already present cached
  files by SHA256; it made no download request.

Raw stdout/stderr/exit codes, exact protected-file comparisons and boundary checks
are in P0_local_pdf_checks.json. Active P0_protocol_audit.json/.md are the original
runner's actual outputs. Source/config hash and seed SHA256 remain unchanged.
No audit, test or scheduler code was modified and no acceptance rule was weakened.

Scientific workloads run: 0. No P1/P2/P3/validation/formal stage command ran.
Results contain only the original .gitkeep files. Seed metadata was only checked
by existing governance tests. Validation/formal unlock files remain absent.
Simulator correctness, scientific benefit and engineering timing remain NOT RUN.

## Limitations, commit provenance and stop

P0 PASS closes the literature prerequisite in this instance; it is not a new
research-performance conclusion or a full protocol-freeze/publication claim.
The immutable draft declaration in configs/research_protocol.json was not edited
to change its old status string; current gate evidence is the actual P0 audit.
Any future online-adaptation specification/implementation belongs to a separate
task. This task stops here and creates no unlocks.

A fresh checkout without private cache needs the two user PDFs supplied again
and checked by their exact hashes. The existing HTTP helper cannot fetch
sediment attachments when cache is missing. The notes, metadata and source
identities are on GitHub; the copyrighted PDFs are not. No six-PDF fresh-clone
restoration, environment publication or future-task readiness is asserted.

The actual final delivery SHA is read with git rev-parse HEAD, not guessed from
an older source checkpoint or embedded self-referentially. The tested review
checkpoint and its push outcome are recorded after committing in
P0_local_pdf_git_checkpoint.json; the user's final response reports the final
live SHA and post-push worktree state.

PROJECT_NAME=soc
CURRENT_STAGE=P0
INPUT_PDFS_ACCESSIBLE=YES
HEFT_CPOP_IDENTITY_VERIFIED=YES
HEFT_CPOP_FULL_TEXT_REVIEWED=YES
HEFT_CPOP_PAGE_EVIDENCE_COMPLETE=YES
PEFT_IDENTITY_VERIFIED=YES
PEFT_FULL_TEXT_REVIEWED=YES
PEFT_PAGE_EVIDENCE_COMPLETE=YES
REVIEWED_SOURCE_COUNT=6
LITERATURE_REQUIREMENT_PASS=YES
P0_AUDIT_EXIT_CODE=0
P0_STATUS=PASS
P0_GOVERNANCE_TESTS=17 PASSED
SCIENTIFIC_WORKLOADS_RUN=0
SIMULATOR_IMPLEMENTATION_STARTED=NO
SEED_PARTITIONS_CHANGED=NO
RESERVED_PARTITIONS_ACCESSED=NO
VALIDATION_UNLOCKED=NO
FORMAL_UNLOCKED=NO
GIT_COMMIT=RESOLVE_WITH_git_rev-parse_HEAD
GITHUB_PUSH_STATUS=PENDING_THIS_TASK
WORKTREE=QUERY_LIVE_git_status_--short
NEXT_SAFE_ACTION=Separate authorized P1 specification/correctness task; no P1 action in this task
STOP=YES

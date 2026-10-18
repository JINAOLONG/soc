# HEFT/CPOP original-source review — NOT COMPLETE

## Bibliographic identity

H. Topcuoglu, S. Hariri and M.-Y. Wu, “Performance-Effective and Low-Complexity
Task Scheduling for Heterogeneous Computing,” IEEE Transactions on Parallel and
Distributed Systems, 13(3), 260–274, March 2002. DOI: 10.1109/71.993206.
The title, author identities, venue, date, volume, issue, pages and DOI were checked
against Crossref in reports/P0_source_acquisition_008.json. This establishes the
bibliographic target, not review of its algorithm definitions.

## Acquisition and version status

ORIGINAL_RETRIEVED=NO. FULL_TEXT_REVIEWED=NO. SOURCE_VERSION=NOT VERIFIED.
No accepted PDF artifact, PDF SHA256 or inspected-page number exists for this
paper in the current evidence inventory. A DOI, metadata response, OA flag or empty
publisher response is not treated as a manuscript.

The user-supplied Marmara institution record and PDF endpoint were attempted with
normal TLS-verified GETs and returned proxy `Tunnel connection failed: 403 Forbidden`:

- https://openaccess.marmara.edu.tr/entities/publication/feba5344-0457-405a-8cb2-1d26f8963e33
- https://openaccess.marmara.edu.tr/bitstreams/d1584f1e-5066-47a6-8c04-15607a53960f/download

The IEEE record returned HTTP 202 with zero bytes; the official PDF returned 418.
OpenAlex disclosed the same Marmara repository and an institutional RIT course-copy
lead; the latter was proxy-denied. A handle request returned 500, and the Crossref
publisher-PDF link was also proxy-denied. Attempts, dates and response hashes
(where a response body existed) are in P0_source_acquisition_006–009 and _012.
The source leads are not evidence of a successfully inspected original version.

## Required page-specific technical evidence

| Required original-paper item | Verification | Supporting original page |
|---|---|---|
| Upward-rank definition and recurrence | UNVERIFIED | NOT AVAILABLE |
| Average computation costs | UNVERIFIED | NOT AVAILABLE |
| Average communication costs | UNVERIFIED | NOT AVAILABLE |
| HEFT task-priority ordering | UNVERIFIED | NOT AVAILABLE |
| HEFT processor selection / EFT | UNVERIFIED | NOT AVAILABLE |
| Insertion-based scheduling behavior | UNVERIFIED | NOT AVAILABLE |
| CPOP priority from upward/downward ranks | UNVERIFIED | NOT AVAILABLE |
| CPOP critical-path processor selection | UNVERIFIED | NOT AVAILABLE |
| Heterogeneous-platform assumptions | UNVERIFIED | NOT AVAILABLE |
| Communication and processor availability assumptions | UNVERIFIED | NOT AVAILABLE |
| Authors' stated computational complexity | UNVERIFIED | NOT AVAILABLE |

No recurrence, complexity claim or source page is reconstructed from memory,
abstracts or later literature. Original static definitions, later reports and this
project's future online adaptation remain distinct. Baseline requirements are
unchanged, and no scheduler implementation is authorized in this task.

Next safe action: obtain a lawfully accessible original/author manuscript, verify
its identity and complete file, record SHA256 and version, inspect every page
needed for this checklist, then replace UNVERIFIED cells with exact evidence.
Do not redistribute the PDF in Git without explicit redistribution permission.

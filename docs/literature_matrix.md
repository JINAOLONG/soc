# Literature verification matrix — P0 INCOMPLETE

Four original manuscripts have been reviewed in the scoped notes below. The
minimum is 6–8 and HEFT/CPOP, PEFT and DS3 are mandatory. HEFT/CPOP and PEFT
bibliographic identities are confirmed through Crossref, but their original
algorithms remain UNVERIFIED_SOURCE: official landing responses contain no body,
PDF endpoints return HTTP 418, and tried alternatives did not yield the papers.
Metadata alone is not original-paper verification. P0 remains BLOCKED.

| Paper | Model | Static/online | Single/multi DAG | Deadline | Priority | Heterogeneity | Mapping | Communication | Contention | Objective | Complexity | Code | Difference / scope |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [HEFT/CPOP](literature_reviews/heft_cpop.md), Topcuoglu/Hariri/Wu, DOI 10.1109/71.993206 (metadata confirmed) | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT VERIFIED | Cannot implement claimed-faithful baseline without original review |
| [PEFT](literature_reviews/peft.md), Arabnejad/Barbosa, DOI 10.1109/TPDS.2013.57 (metadata confirmed) | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT VERIFIED | Same blocker; no guessed OCT formula |
| [DS3](literature_reviews/ds3.md), arXiv:2003.09016v1 | Profile-driven SoC simulator | Runtime scheduling plus offline table support | Multiple streaming applications | H/L budget not specified in reviewed definitions | Scheduler dependent | Configurable general/special PEs | Ready-task PE assignment | Analytical NoC and memory models | Explicit network/memory modeling | Performance, power/thermal, energy, DSE | Empirical scalability, no general bound inferred | Paper links segemena/DS3; README retrieved | Our proposed strict observation boundary, independent validator and H/L protocol are separate, not replications |
| [StarPU](literature_reviews/starpu.md), HAL inria-00550877v1 / DOI 10.1002/cpe.1631 | Runtime task/data abstractions | Dynamic ready-task push/pop policies | Concurrent computations supported | H/L deadline budget absent in reviewed policies | Optional task priority | CPU/GPU/Cell | Per-worker/shared queues, prediction-based policies | Software MSI and automatic transfers | Locality/load balancing; no equivalent fixed-delay model assumed | HPC throughput/performance | Policy-specific; no bound inferred | Modern code not retrieved | Reviewed policies commit ready-task queue assignments; our pending proposals may be revoked |
| [Multi-Deadline DAG / Autoware WiP](literature_reviews/autoware_dag.md), arXiv:2505.06780v2 | Periodic callback sub-DAGs, multiple sink deadlines | Repeated jobs; extended GEDF | Multiple DAG tasks | Sink-specific relative deadlines | Reference Absolute Deadline | Homogeneous multicores in evaluated model | No heterogeneous mapping rule | Queue/feedback boundaries abstracted | Shared homogeneous cores | Timing/acceptance ratio | NOT VERIFIED | Linked footnote, not retrieved/run | Does not provide CPU/GPU/NPU H/L-budget validation or hardware safety proof for soc |
| [Federated lower bound](literature_reviews/federated_limit.md), Chen, arXiv:1510.07254v2 | Sporadic constrained-deadline DAG tasks | Theoretical schedule comparison | Task systems | Constrained deadlines | Comparator-specific | Identical processors | Exclusive federated assignment | Not part of constructed counterexample | Exclusive resource ownership | Speedup lower bound vs optimal unrestricted schedule | Theorem, not implementation cost | NOT APPLICABLE | Negative theoretical result is not transferable as our scheduler's bound |

These are scoped source comparisons, not an exhaustive novelty claim. All
performance numbers in those papers belong to the papers; none is counted as
this clean-room project's experiment. Reviews identify the sections actually
examined and their limitations. Four reviewed papers do not satisfy P0.

Acquisition history:

- Initial ad hoc probes were denied by the proxy for DOI/arXiv/author destinations.
- P0_source_acquisition_001.json: later probes reached arXiv/Crossref/HAL; IEEE
  returned empty 202 responses. One initially guessed HEFT DOI was 404. It was
  corrected from Crossref to **10.1109/71.993206**; the wrong lead is preserved.
- P0_source_acquisition_002.json: DS3 and StarPU PDFs retrieved; attempted
  alternative URLs failed. The speculative UMD URL was not a confirmed author
  source, and no evidence is inferred from it.
- P0_source_acquisition_003.json: correct HEFT DOI and both official IEEE PDF
  requests still did not supply primary text; PEFT alternatives did not resolve.
- P0_source_acquisition_004.json: two additional arXiv original manuscripts.

Source PDF SHA256, URLs, review timestamps and reviewed scope are in
literature_evidence.json. PDFs are held in ignored .cache/literature; they are
third-party copyrighted works, not relicensed under the repository's Apache
LICENSE. scripts/fetch_primary_sources.py restores those exact recorded bytes
through TLS and checks SHA256. The authoritative tracked record is the notes,
identity and regeneration code, rather than a dependency on /tmp.

## Targeted P0 remediation — acquisition and page evidence

The latest task is limited to acquisition, source review, documentation, existing
governance tests and P0 audit. It does not authorize P1 or any scientific workload.
The original technical-model matrix above is retained; no unverified algorithm
cell is filled from metadata. Four primary scoped reviews remain counted, not six.

| Source | Bibliographic identity | Source type/version | Access and original-full-text inspection | Supporting PDF pages |
|---|---|---|---|---|
| HEFT/CPOP | H. Topcuoglu, S. Hariri, M.-Y. Wu; IEEE TPDS 13(3), 260–274, 2002; DOI 10.1109/71.993206 (Crossref confirmed) | Original version NOT AVAILABLE | Original not retrieved or reviewed; supplied institutional endpoint proxy-denied; IEEE empty 202/PDF 418 | NOT AVAILABLE; every algorithm item UNVERIFIED in linked review checklist |
| PEFT | Hamid Arabnejad, Jorge G. Barbosa; IEEE TPDS 25(3), 682–694, 2014; DOI 10.1109/TPDS.2013.57 (Crossref confirmed) | Original version NOT AVAILABLE | Original not retrieved or reviewed; RG/Porto routes proxy-denied; IEEE empty 202/PDF 418; UMinho exact-title public query zero records | NOT AVAILABLE; every algorithm item UNVERIFIED in linked review checklist |
| DS3 | Full nine-author identity in inventory; IEEE Transactions on Computers association, DOI 10.1109/TC.2020.2986963 | arXiv:2003.09016v1, 19 March 2020, 14 PDF pages | Existing original preprint opened, hash reverified; prior scoped review retained | 1 identity; 3–6 model/lifecycle/policies; 12–13 scalability/conclusion |
| StarPU | Augonnet, Thibault, Namyst, Wacrenier; Concurrency and Computation: Practice and Experience 23(2), 187–198, 2011; DOI 10.1002/cpe.1631 | HAL inria-00550877v1 author manuscript; 16 PDF pages including cover | Existing original opened, hash reverified; prior scoped review retained | 1 bibliography; 4–7 model/policies; 8 evaluation design (printed page = PDF page − 1 after cover) |
| Multi-Deadline DAG / Autoware | Atsushi Yano, Takuya Azumi; 2024 RTSS, 451–454; DOI 10.1109/RTSS62706.2024.00049 | Work-in-progress arXiv:2505.06780v2, 13 May 2025; 4 PDF pages | Existing original opened, hash reverified; prior scoped review retained | 1 identity; 2–3 model/RAD; 4 evaluation |
| Federated lower bound | Jian-Jia Chen; arXiv:1510.07254v2, 2016; publication venue/DOI NOT VERIFIED; volume/issue NOT APPLICABLE for preprint | Author preprint, v2 22 June 2016; 6 PDF pages | Existing original opened, hash reverified; prior scoped review retained | 1–2 model/comparator; 3–5 construction/lemmas/theorem; 5 discussion |

DS3 final volume/issue/pagination are NOT VERIFIED: the retrieved Crossref record
has no volume/issue and placeholder pages 1–1. That placeholder is not treated as
final pagination or as a one-page manuscript. Its author order also differs from
the examined arXiv title page for Mack/Kumbhare; the reviewed PDF identity/order
is recorded explicitly. StarPU's HAL cover publication year is 2011 while its
manuscript template says 2009. Autoware's proceedings record is 2024, while the
examined arXiv v2/copyright says 2025. These are recorded version differences,
not fabricated bibliographic completions. The full structured fields are in
literature_evidence.json; explicit unknowns do not alter primary-review count.

The new acquisition attempts are P0_source_acquisition_006.json through _013.json.
Only lawful public institutional, publisher and author-upload routes were tried;
no authentication, paywall or download restriction was bypassed. OpenAlex and
Crossref were discovery/metadata sources only and add zero reviewed papers.
UMinho's HTML shell was followed through its published public API configuration;
the exact-title search returned zero records, rather than a PDF. No challenge or
rate limit was worked around. The original audit and inventory are retained in
reports/history/p0_before_literature_closure_ebab07e/.

**Decision: literature requirement remains unmet.** Obtain and inspect the two
mandatory originals before completing the six-source gate. No later-source
formula or project online adaptation replaces those originals. No new baseline,
candidate, threshold, partition or unlock condition is defined in this task.

# Literature verification matrix — six primary studies reviewed

The two mandatory HEFT/CPOP and PEFT papers are now reviewed from the actual
user-provided PDFs, with page/figure/equation evidence. The earlier four original
manuscripts were requalified by checking their actual files, hashes, declared
review scope, page references and substantive primary-source notes. Six counted
studies are distinct; the minimum remains six and required IDs remain
heft_cpop, peft, ds3. Metadata databases and failed HTTP responses count as zero.
The existing formal P0 audit determines the gate outcome; see
reports/P0_protocol_audit.json and reports/P0_local_pdf_checks.json.

## Original technical models

| Paper | Model | Static/online | Single/multi DAG | Deadline | Priority | Heterogeneity | Mapping | Communication | Contention | Objective | Complexity | Code | Difference / scope |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [HEFT/CPOP](literature_reviews/heft_cpop.md), Topcuoglu/Hariri/Wu, DOI 10.1109/71.993206 | Known-cost, non-preemptive application graph | Static | Single application DAG | No service H/L deadline budget | HEFT mean-cost rank_u; CPOP rank_u+rank_d | Bounded heterogeneous processor set and task×processor costs | HEFT insertion/min-EFT; CPOP connected critical path on minimum cumulative-compute processor, others min-EFT | Startup+data/bandwidth; same processor zero; mean costs for ranking | Fully connected, no transfer contention; compute/transfer overlap | Minimize makespan with low scheduling cost | Authors state HEFT O(e q), dense O(v² p); CPOP O(e p), pp.264,266 | Original pseudocode Figs.2/5; implementation availability UNVERIFIED | Source definitions verified; online visibility, compatibility and H/L behavior still require separate project adaptation |
| [PEFT](literature_reviews/peft.md), Arabnejad/Barbosa, DOI 10.1109/TPDS.2013.57 | Known-cost, non-preemptive single job, processors not shared during job | Static | Single application DAG | No H/L deadline or L-P95 budget | Average processor-column OCT rank; highest ready rank | Task×processor execution matrix; CPU/GPU discussed | Insertion EFT plus OCT, minimizing OEFT | Mean transfer cost between different processors; same processor zero; simplified uniform bandwidth | No contention; OCT excludes availability, EFT includes partial-schedule availability | Makespan; source evaluates SLR/efficiency/slack | Authors state OCT O(p(e+v)), assignment O(v²p), total O(p(e+v)+v²p), p.688 | Original Algorithm 1; algorithm code UNVERIFIED | Look-ahead baseline source verified; no cross-service opportunity cost or online fairness mechanism is supplied |
| [DS3](literature_reviews/ds3.md), arXiv:2003.09016v1 | Profile-driven SoC simulator | Runtime scheduling plus offline tables | Multiple streaming applications | H/L budget not specified in reviewed definitions | Scheduler dependent | Configurable general/special PEs | Ready-task PE assignment | Analytical NoC and memory models | Network/memory modeled | Performance, power/thermal, energy, DSE | Empirical scalability; no general bound inferred | Paper links segemena/DS3; prior README retrieval | Existing scoped original review requalified; no claim to reproduce hardware validation or its information boundary |
| [StarPU](literature_reviews/starpu.md), HAL inria-00550877v1 | Runtime task/data abstractions | Dynamic ready-task push/pop | Concurrent computations supported | No H/L deadline budget in reviewed policies | Optional task priority | CPU/GPU/Cell | Queue/prediction-based policies | Software MSI and automatic transfers | Locality/load balance; no equivalence to fixed-delay model assumed | HPC throughput/performance | Policy specific; no bound inferred | Modern code not retrieved | Existing scoped review requalified; reviewed policies commit ready queue assignments |
| [Multi-Deadline DAG / Autoware WiP](literature_reviews/autoware_dag.md), arXiv:2505.06780v2 | Periodic callback sub-DAGs, multiple sink deadlines | Repeated jobs, extended GEDF | Multiple DAG tasks | Sink-specific deadlines | Reference Absolute Deadline | Homogeneous multicores in evaluated model | No heterogeneous mapping rule | Queue/feedback boundaries abstracted | Shared homogeneous cores | Timing/acceptance ratio | NOT VERIFIED | Source footnote linked, not run | Existing scoped review requalified; no CPU/GPU/NPU H/L-budget or safety-certificate conclusion for soc |
| [Federated lower bound](literature_reviews/federated_limit.md), Chen, arXiv:1510.07254v2 | Constrained-deadline sporadic DAG tasks | Theoretical schedule comparison | Task system | Constrained deadlines | Comparator specific | Identical processors | Exclusive federated assignment | Not in constructed counterexample | Exclusive ownership | Speedup lower bound vs optimal unrestricted scheduling | Theorem, not implementation cost | NOT APPLICABLE | Existing scoped original review requalified; no bound is transferred to soc's scheduler |

These compare source formulations, not a completed novelty search. Source-paper
performance numbers are never soc experiments or samples. Original definitions,
later literature and future online adaptations remain separate. This task changes
no baseline requirement, candidate definition, seed, statistical method or gate.

## Identity, version, access and page evidence

| Source | Bibliography | Actual reviewed version/access | Review coverage and supporting pages |
|---|---|---|---|
| HEFT/CPOP | Haluk Topcuoglu, Salim Hariri, Min-You Wu; IEEE TPDS 13(3), 260–274, March 2002; DOI 10.1109/71.993206 | User-provided publisher-formatted journal copy, 15 PDF pages; original download URL unknown; later iText modification | FULL PAPER PDF 1–15; Eq.(1)–(7) p.262/PDF3; Eq.(8)–(10), HEFT Fig.2 p.264/PDF5; CPOP Fig.5 p.266/PDF7; contextual limitations pp.272–273/PDF13–14 |
| PEFT | Hamid Arabnejad, Jorge G. Barbosa; IEEE TPDS 25(3), 682–694, March 2014; DOI 10.1109/TPDS.2013.57 | User-provided publisher-formatted journal copy, 13 PDF pages; online 2013 vs issue 2014; later iText modification | FULL PAPER PDF 1–13; model/EST/EFT pp.683–684/PDF2–3; Eq.(7)–(9), Algorithm1 p.687/PDF6; complexity p.688/PDF7; limitations pp.691–693/PDF10–12 |
| DS3 | Nine-author identity in inventory; IEEE Transactions on Computers association, DOI 10.1109/TC.2020.2986963 | arXiv:2003.09016v1, 19 March 2020; 14 PDF pages, hash reverified | Existing scoped primary review retained; PDF1 identity, 3–6 model/lifecycle/policies, 12–13 scalability/conclusion; substantive recheck PDF3,5 |
| StarPU | Augonnet, Thibault, Namyst, Wacrenier; Concurrency and Computation: Practice and Experience 23(2), 187–198, 2011; DOI 10.1002/cpe.1631 | HAL inria-00550877v1 author manuscript; 16 PDF pages including cover | Existing scoped review retained; PDF1 bibliography, 4–7 model/policies, 8 evaluation; substantive recheck PDF4,6. Printed manuscript page = PDF page−1 after cover |
| Multi-Deadline DAG / Autoware | Atsushi Yano, Takuya Azumi; 2024 RTSS, 451–454; DOI 10.1109/RTSS62706.2024.00049 | arXiv:2505.06780v2, 13 May 2025, 4 PDF pages | Existing scope retained; PDF1 identity, 2–3 model/RAD, 4 evaluation; substantive recheck PDF3 |
| Federated lower bound | Jian-Jia Chen; arXiv:1510.07254v2 (2016); publication venue/DOI NOT VERIFIED; volume/issue N/A for preprint | Author preprint, v2 22 June 2016, 6 PDF pages | Existing scoped review retained; PDF1–2 comparator/model, 3–5 construction/proof, 5 discussion; substantive recheck PDF1,5 |

The two new inputs carry provenance status
USER_PROVIDED_LOCAL_COPY_SOURCE_UNVERIFIED. Their identity/content is verified,
but no publisher authentication of unchanged binary or original download URL is
claimed. Their real sediment attachment locators occupy primary_url in the
existing schema; download_url is null. This records an actual supplied source,
not a fabricated HTTP download. Files remain in ignored private cache.

DS3 volume/issue and final pagination remain NOT VERIFIED: earlier Crossref has
placeholder 1–1, which is not a one-page manuscript. Its title-page author order
also differs from Crossref's Mack/Kumbhare order. StarPU's HAL cover cites 2011
while its manuscript template says 2009. Autoware's proceedings year is 2024
while its arXiv v2/copyright says 2025. These limitations are retained; primary
preprint review is not silently upgraded to verified journal bibliographic data.

## Count decision and retained history

reports/P0_local_pdf_prior_sources_recheck.json explains why each existing
scoped primary review remains eligible under the unchanged protocol; their
scope is not upgraded to full-paper coverage. reports/P0_source_acquisition_014.json
records actual user-input paths, file SHA256/size, pdfinfo, all-page opening and
rendering, and the new full-paper reviews. reports/P0_literature_source_hashes.json
binds all six actual files and notes. Count is six because these evidence chains
qualify, not because six table rows exist.

Previous failed acquisitions _001 through _013 and old audits remain unchanged.
The immediately prior matrix/inventory/audit/checklist are archived under
reports/history/p0_before_local_pdf_review_1b36f39/. Network failures are historical
facts; the current acquisition route for the two originals is the user's inputs.

No copyrighted PDF, extracted full text, page image or contact sheet is committed.
Only metadata, hashes, bibliographic identities and original-source review notes
are versioned. In a new checkout lacking private cache, the two exact local inputs
must be supplied again and checked against recorded SHA256; the existing HTTP
fetch helper does not download sediment attachments. No six-PDF fresh-clone
restoration or scientific readiness is claimed by the current P0 audit.

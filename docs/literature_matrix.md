# Literature verification matrix — P0 INCOMPLETE

Four original manuscripts have been reviewed in the scoped notes below. The
minimum is 6–8 and HEFT/CPOP, PEFT and DS3 are mandatory. HEFT/CPOP and PEFT
bibliographic identities are confirmed through Crossref, but their original
algorithms remain UNVERIFIED_SOURCE: official landing responses contain no body,
PDF endpoints return HTTP 418, and tried alternatives did not yield the papers.
Metadata alone is not original-paper verification. P0 remains BLOCKED.

| Paper | Model | Static/online | Single/multi DAG | Deadline | Priority | Heterogeneity | Mapping | Communication | Contention | Objective | Complexity | Code | Difference / scope |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HEFT/CPOP, Topcuoglu/Hariri/Wu, DOI 10.1109/71.993206 (metadata confirmed) | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT VERIFIED | Cannot implement claimed-faithful baseline without original review |
| PEFT, Arabnejad/Barbosa, DOI 10.1109/TPDS.2013.57 (metadata confirmed) | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT VERIFIED | Same blocker; no guessed OCT formula |
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

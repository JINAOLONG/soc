# StarPU primary-source review

Reviewed by: Codex (this clean-room task). Scope: HAL cover metadata, manuscript
§1–3.4 and §4.1–4.2. This is a reviewed primary manuscript, not a runtime replication.

Source: https://inria.hal.science/inria-00550877/document. HAL cover identifies
Cédric Augonnet, Samuel Thibault, Raymond Namyst and Pierre-André Wacrenier;
Concurrency and Computation: Practice and Experience 23(2), 187–198 (2011),
DOI 10.1002/cpe.1631. The manuscript template itself says 2009; this difference
is recorded rather than silently treating template year as publication year.

- Model: §2.2 represents a task by available implementations on heterogeneous
  targets, declared data accesses and dependencies. Tasks launch asynchronously.
- Dynamic ready filtering: §3.2 schedules ready tasks when dependencies are
  fulfilled, using push/pop queues; it explicitly contrasts this with scheduling
  not-yet-ready tasks. Earlier queue assignments in these policies are not
  reconsidered. Our planned revocable pending mapping differs from this choice.
- Heterogeneity/mapping: CPU, CUDA GPU and Cell support are described (§2.2).
  §3.3 uses per-architecture performance models; §3.4/Table I lists greedy,
  no-prio, work-stealing, weighted-random and heft-tm policies. This is not a
  primary substitute for reviewing Topcuoglu et al.'s HEFT/CPOP paper.
- Communication: §2.1 describes software MSI data caching and transfers;
  §3.1 discusses locality and concurrent problems as motivations for scheduling.
  It is not our parameterized delay-only communication model.
- Priority/deadline: optional programmer priorities (§3.3); no service-level
  H/L deadline miss objective or L-P95 constraint in these reviewed policies.
- Evaluation: §4.1–4.2 uses matrix multiplication and factorizations on multicore
  CPU/GPU systems, emphasizing performance models/load imbalance. We do not
  reproduce its performance numbers or transfer them to automotive hardware.
- Complexity: no unified policy-independent complexity bound is established by
  this review. Code availability of today's runtime is NOT VERIFIED here.

Relevance: separation of runtime, data management and pluggable scheduling;
resource-specific prediction and the cost of naive offloading. Differences are
scoped to the reviewed formulation, not an exhaustive novelty claim.

## P0 remediation: explicit page map and version checks

Page references below are 1-based PDF viewer pages. They preserve the prior
scoped review; they do not claim every manuscript page has been reviewed.

| PDF page(s) | Evidence scope |
|---|---|
| 1 | HAL cover bibliography |
| 4, 5 | Printed pages 3–4: Section 2 model/data and Section 3.1 |
| 6, 7 | Printed pages 5–6: ready-task policies, priority, prediction and Table I |
| 8 | Printed page 7: Sections 4.1–4.2 evaluation design |

Bibliographic/version check: HAL cover cites 2011 publication; deposited manuscript template says 2009, not the same pagination as the journal.

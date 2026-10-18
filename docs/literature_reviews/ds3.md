# DS3 primary-source review

Reviewed by: Codex (this clean-room task). Scope: primary manuscript title/abstract,
§3, §4.1–4.4, §5.1–5.2, §6 opening validation design and §7.6/§8. This is a
source-model review, not a replication of the paper's hardware validation.

Source: https://arxiv.org/pdf/2003.09016 (manuscript identifies v1, 19 March 2020).
Title and author list were checked on PDF page 1. Crossref independently resolves
the title to DOI 10.1109/TC.2020.2986963. PDF byte hash is in
docs/literature_evidence.json; use scripts/fetch_primary_sources.py to restore it.

- Model and online behavior: §3/p.3 describes concurrent streaming of multiple
  application jobs, resource profiles and scheduling at decision epochs. §4.2/p.4
  describes application DAGs, exponential injection and application mixtures.
- Compatibility/heterogeneity: §4.1/Table 1 includes resource types, supported-task
  execution profiles, capacity, utilization and state. This is a configurable
  SoC abstraction, not our fixed 4 CPU + GPU + NPU model.
- Mapping/lifecycle: §4.4/Fig.4 and p.5 distinguish outstanding, ready, executable
  and completed queues. PE assignment precedes satisfying communication and
  starting execution. §5.1/p.5–6 describes MET, ETF and a table-based schedule;
  the table schedule's single-job optimality does not generalize to multi-job use.
- Communication/contention: p.5 describes analytical mesh-NoC latency and
  memory bandwidth/latency modeling. Our version-1 delay-only model is simpler
  and cannot claim to reproduce those contention mechanisms.
- Objective/evaluation: performance, power/temperature/energy and design-space
  exploration (§3, §5.2). §6 uses Odroid-XU3 and ZCU-102 validation; those results
  are the authors' evidence, not measurements made in this repository.
- Deadline/priority: a service-level H-DMR objective and an L-P95 budget are not
  specified in the reviewed scheduler definitions. No claim is made about every
  later version of the DS3 code. The interface is described as loosely defined;
  it does not establish our intended strict scheduler information isolation.
- Complexity: §7.6 reports empirical scalability studies. That is not a general
  proof of algorithmic complexity; none is inferred here.
- Code: PDF p.3 footnote 1 names https://github.com/segemena/DS3. Its README and
  scheduler file were separately retrieved and hashed as code-access diagnostics;
  no code was copied into our implementation.

Relevance: architecture modularity, task lifecycle and source-based baseline
context. Difference: our planned tests require immutable online observations,
independent trace validation and the specified paired-seed H/L budget experiment.
This scoped comparison does not prove novelty. No DS3 reported number is used as
new experimental evidence or as a workload calibration target.

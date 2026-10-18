# Federated-scheduling lower bound primary-source review

Reviewed by: Codex (this clean-room task). Scope: abstract, §1, §2 counterexample
and Lemmas 1–2/Theorem 1, and §3 discussion. Source:
https://arxiv.org/pdf/1510.07254v2. Title: Federated Scheduling Admits No Constant
Speedup Factors for Constrained-Deadline DAG Task Systems. Author Jian-Jia Chen.
Manuscript identifies v2 dated 22 June 2016. Publication venue/DOI NOT VERIFIED.

- Model: sporadic DAG tasks with constrained deadlines on identical processors.
  Federated tasks either execute sequentially on one processor or exclusively
  own their assigned multiple processors (§1). This is not our compatible
  CPU/GPU/NPU shared online resource model.
- Theoretical result: §2 constructs tasks with independent subtasks, so even a
  DAG special case suffices. Lemma 1 establishes a feasible nonfederated schedule;
  Lemma 2 bounds exclusive processor requirements. Theorem 1 yields an
  Omega(min(M,N)) speedup lower bound versus an optimal unrestricted scheduler.
- The paper distinguishes optimal federated schedules from optimal unrestricted
  schedules (§1, §3). Its negative result does not contradict constant bounds
  relative to an optimal federated comparator; comparator scope matters.
- No resource-specific mapping, transfer-delay contention model or H/L budget is
  studied. Evaluation is a mathematical construction, not an empirical SoC
  experiment. Implementation code and operational runtime complexity are
  NOT APPLICABLE to the reviewed counterexample proof.

Relevance: precise comparator definitions and preserving negative results.
This theorem is not a complexity, feasibility or speedup theorem about the planned
non-preemptive heterogeneous scheduler in soc. No numerical experimental claim
is drawn from it.

## P0 remediation: explicit page map and version checks

Page references below are 1-based PDF viewer pages. They preserve the prior
scoped review; they do not claim every manuscript page has been reviewed.

| PDF page(s) | Evidence scope |
|---|---|
| 1, 2 | model, comparator scope and definitions |
| 3, 4, 5 | construction, Lemmas 1–2 and Theorem 1 |
| 5 | Section 3 interpretation and limitations |

Bibliographic/version check: v2 is 22 June 2016; identifier originates in 2015. No journal/publication identity inferred.

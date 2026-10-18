# Multi-deadline DAG / Autoware primary-source review

Reviewed by: Codex (this clean-room task). Scope: §I–IV and the experimental design
in §V, with emphasis on §III and §IV.A–B. Source:
https://arxiv.org/pdf/2505.06780v2. Title: Work-in-Progress: Multi-Deadline DAG
Scheduling Model for Autonomous Driving Systems. Authors Atsushi Yano and
Takuya Azumi. PDF identifies arXiv v2 (13 May 2025) and DOI
10.1109/RTSS62706.2024.00049; the DOI was read from the primary manuscript,
not independently resolved. Work-in-progress status is retained.

- Model: §II–III describes timer/subscription/sync callbacks, non-FIFO queue
  consumption and feedback that complicate cause-effect-chain modeling.
- §IV segments the callback graph into periodic DAG tasks. Each task has a
  period, a DAG and one or more sink-relative deadlines. Queue propagation
  beyond those DAG outputs is outside the analysis scope. Deadline assignment
  is left to the system designer; the paper does not derive those values.
- §IV.B defines Reference Absolute Deadline for each vertex as its own sink
  deadline, or the earliest deadline among its descendant sinks. It uses that
  value in an extended GEDF. This is not our joint heterogeneous mapping rule.
- §V uses Autoware-derived synthetic DAGs and fixed per-trial durations sampled
  from measured callback data. It explicitly simulates homogeneous multicores
  and reports acceptance ratio. No GPU/NPU compatibility or mapping rule is
  supplied by that experiment. Its sample counts are not this project's samples.
- Communication is an abstraction around callback/queue semantics, not our
  destination-specific transfer-delay model. The reviewed formulation has no
  two-class H/L service budget. An online heterogeneous deadline guarantee
  cannot be imported from this source.
- Evaluation code is linked in a footnote (not retrieved or run; its URL is not
  independently checked here).
  No algorithmic complexity bound is claimed in this review.

Relevance: automotive DAG/deadline modeling and explicit model limitations.
The source's discussion of safety assumptions does not turn our H/L importance
labels into a safety-certification model. No source figure or performance number
is used as new evidence.

## P0 remediation: explicit page map and version checks

Page references below are 1-based PDF viewer pages. They preserve the prior
scoped review; they do not claim every manuscript page has been reviewed.

| PDF page(s) | Evidence scope |
|---|---|
| 1 | title/authors/DOI and abstract |
| 2, 3 | trigger modeling, problem, multi-deadline DAG and RAD definition |
| 4 | evaluation design, code footnote and limitations |

Bibliographic/version check: Journal/conference record year 2024; reviewed arXiv v2 is 13 May 2025 and PDF copyright says 2025. No identity change inferred.

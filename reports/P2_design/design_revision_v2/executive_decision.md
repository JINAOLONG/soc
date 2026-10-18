# P2 design revision v2 — delivery verdict

**DESIGN_REVISION_READY_FOR_HUMAN_DECISION**

This is a documentation/static-review delivery verdict only. It does not approve any decision,
activate v2, establish scientific validity, freeze the full engineering protocol, or authorize
implementation/execution. P0/P1 check-only PASS; P2 preflight remains BLOCKED/NOT_RUN.

## Scope and evidence

Starting repository/branch: https://github.com/JINAOLONG/soc.git / work; actual starting HEAD and
origin/work: 79f9c245b23119ce25175d6dc6ff148e9e092461. Initial worktree CLEAN. All341 starting tracked
files remain byte-identical, including v1, old audit/failures, STATUS.md, design_status, source,
tests, thresholds/statistics, seed metadata and gates. Only the two authorized new namespaces added.
The actual old D05 recommendation was ACCEPT, differing from the request summary; historical record
is preserved. Its axes/budget remain unchanged and its future identity references are clarified.

Fresh v2 review: **351 PASS /0 FAIL**, CMD-025 exit0. Five synthetic canonical vectors agree across
two generic encoders and external GNU sha256sum (CMD-031 exit0). No scientific key/seed realization,
workload, bootstrap index, observer rollout, comparison or timing measurement was generated.
P0/P1 check-only both exit0 (CMD-026/027); P1 reports historical64 tests/47 P1,0failed, not a new test
execution. P1/v1/prior-audit manifests:122/315/24 files,0missing/0mismatch (CMD-028..030).

## What changed in proposed documents

V2-F01: M1R_PATH_V2 observes bounded remaining arrived-H paths using public estimates; fixed suffix
projection is not an optimal scheduler or candidate. New local L slack cap, complete/partial coverage
and scope restrictions are explicit assumptions. V1 M1 retains its limited negative interpretation.
V2-F02: lifecycle has35 nodes/40 edges and is acyclic; blueprint/auth/inputlock precede materialization;
content resolution precedes workload/run/attempt identity and execution. Recovery is append-only.
V2-F03:61 closed typed definitions,21 exact identity preimages, all15 keyed fields explicitly bound;
semantic/raw/runtime hash scopes separated; G covers all100 parent-MAIN services. New version changes
future random identity while preserving distributions. V2-F04: event records and state equivalence
separate; repeat states deduplicate within primary attempt, replay excluded, missing is not zero.
V2-F05: execution, integrity, identity, selection, diagnostic, classification, timing and progression
separate; timing NOT_FROZEN always blocks. COMPLETE/exit0/support alone cannot authorize P2/P3.
V2-F06: A-before-B retained; all candidates/off-target records retained; selected-calibration CIs
labelled conditional, pointwise and descriptive. V2-F07:100/50/100 controls, one control N/A token,
full-drain makespan unchanged, strict absolute RN64 feasibility certificate; no epsilon or truth leak.
Resolution matrix records all seven as addressed in proposed design/static review, not runtime closure.
Historical F08 lineage/adapter implementation risk remains NOT_VERIFIED, with future regression required.

## Unapproved decisions and limitations

D01–D10 all UNAPPROVED. Original SP01–SP32 trace into **40 unresolved groups SP01–SP40**;
eight split-out additions SP33–SP40, no deletion/merge. D01–D03 scientific tables preserved exactly.
New rules are proposals, not source-supported/hardware measurements. Choose FINE versus COARSE
explicitly; neither is default. Proposed support coverage4/5 and negative coverage1 require approval.
Bounded observation can still miss opportunities; partial coverage cannot establish absence.
No macro compensates a failing condition. Same-seed selection cannot justify confirmatory inference.
No runtime generator/worker/adapter/validator was implemented or validated; engineering timing
protocol remains NOT_FROZEN and decision-P95 target remains2ms, not measured. These do not disappear
when the design packet is accepted. Future implementation and execution need separate authorization.

## Failure history, integrity and publication

The initial authoring field-collision exception is preserved and reproduced as CMD-008 exit1.
CMD-021 had301 passing checks and one exact-prose assertion failure; structured selection fields
were added and the check corrected. CMD-023 then passed302; the final typed-binding review passes351.
CMD-033 delivery-metadata review also stopped on a Path-join authoring typo; original traceback/checker
and caller parse failure are disclosed in authoring_error_history.md. Its correction affects no design
rule. CMD-034 then caught an incorrect reviewer expectation of18 packet references; actual16
references to13 files all hash-match. Corrected the reviewer count only; final31 metadata checks pass.
All original failure outputs/checker/results remain archived. This report is a fresh method review by the
same assistant, not an external independent human review. Command ledger scope explicitly excludes
initial discovery/wrappers; raw stdout/stderr references/hashes and actual nonzero exits are preserved.

See review_evidence_manifest.json for all new artifact hashes. first_publication_receipt.json records
actual first normal commit 3f81bc6c69d30c16b9ed350c5dfab6111759987e and verified push/CLEAN worktree;
18 design files and102 report files were added in that commit. This receipt is now added in the final
report-only metadata commit (18 design/103 report files total). The38-command audit ledger has
4 nonzero subprocess exits (CMD-008/021/033/034),3 unexpected; all failures retained. Publication
commands are preserved separately in the receipt, not added to those38. The first final-publication
precheck stopped before staging because wrapper strip() lost a porcelain leading space; its actual
commands/error and rstrip correction are preserved in the publication receipt. No scope or rule changed. The final enclosing commit cannot contain its own hash and is verified externally
in /tmp/soc-design-revision-v2-final-delivery.json and the final user handoff. No force/history rewrite.

**Single next safe action:** user reviews human_decision_packet.md and records explicit approval,
rejection or requested revision for the hash-identified v2 D01–D10, including every scientific group
and FINE/COARSE choice. This task stops without implementation or P2 execution.

# Independent design audit v2 — executive decision

**DESIGN_REVIEW_REVISE_REQUIRED**

Audit target: `892ce2b71fd0c89f1b241c950b597eafab894e23`, branch `work`, repository `https://github.com/JINAOLONG/soc.git`.
This is report-only adversarial design review. Independence refers to new checks/proofs rather than
reuse of v1's94-check result; the same collaborating assistant performed the review, so no external
personnel/institutional independence is claimed. No scientific sample, comparison or P2 execution.

The matrix and topology arithmetic are sound, but complete human approval is premature. The two
critical findings are V2-F01 (ready-H local objective does not cover the registered later-H blocking
mechanism for negative inference) and V2-F02 (first materialization is behind guards/locks requiring
its own content identity). V2-F03/F05 require exact key/identity and stage-exit contracts. V2-F04/F06/F07
pin denominator, selected-calibration interpretation and typed control/metric semantics. V2-F08 is
known future P1/scientific-lineage verification, not a newly demonstrated implementation defect.

Recommendations:4 ACCEPT AS PROPOSED (D01,D02,D03,D05);6 REVISE BEFORE APPROVAL
(D04,D06,D07,D08,D09,D10);0 REJECT decisions. These are review recommendations only.
Findings:2 CRITICAL,2 MAJOR,3 MEDIUM,1 INFO. All10 human approvals remain UNAPPROVED;
all32 named scientific parameter groups remain unresolved. Neither FINE nor COARSE selected.

Actual evidence:

- CMD-064 P0 check-only exit0; CMD-065 P1 check-only exit0 (existing manual correctness fixtures only).
- CMD-066 P1 inventory122 files matches; CMD-067 v1 inventory315 files matches.
- CMD-068 independent metadata checks60 PASS/0 FAIL: exact36 configs/10 calibration seeds,
  2520 rows=1800 MAIN+360 H_ISOLATED+360 LOW_COMPETITION;1080 planned input references;
  replay-inclusive maximum5040 engine invocations. All actual scientific counts remain0.
- CMD-073 final adversarial check exit2 as expected:7 proof checks verified,2 design acceptance
  failures ADV-01/ADV-02. This is a negative design audit, not a test crash/P1 or scientific failure.
- CMD-069 initial adversarial exit2 is preserved; ADV-03 was corrected from FAIL to NOT_VERIFIED
  because v1 already requires repeated-state dedup. See review_method_notes.md and initial snapshots.

No protected proposal/source/config/test/seed/gate/history/STATUS bytes may change. This user task's
report-only scope overrides the general AGENTS instruction to sync STATUS. Therefore the existing
STATUS/design_status v1 declarations remain historical/current v1 statements; this directory carries
the new v2 review verdict. A proposal_complete=true flag does not establish approval or executability.

P0/P1 remain PASS for the current unchanged source. P2 remains BLOCKED/NOT_RUN. B1–B3 unresolved,
B4/B5 designed but unapproved/unimplemented. Timing is out of matrix, budget0 and still unfrozen;
it cannot be silently counted as a completed P2 freeze output.

Read D01_D10_review_matrix.csv for exact version/hash and all eight requested decision fields,
critical_findings.md for reproducible consequences, required_changes.md for precise revisions and
future regression requirements, human_decision_packet.md for unchanged values and UNAPPROVED fields.
Actual commands/exits and source/protection hashes are separate evidence, not simulated results.
Publication checkpoint/status will be recorded in delivery_checkpoint.json; final enclosing HEAD
and remote SHA are resolved with git rev-parse HEAD / git ls-remote origin refs/heads/work.

Next safe action: separately authorize documentation-only revision of the findings, then repeat
static review and human decisions. Do not implement, generate, run P2 or create unlocks. STOP=YES.

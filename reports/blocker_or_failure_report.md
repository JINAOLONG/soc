# P0 blocker / preserved failure record

STOP_STAGE=P0
STOP_REASON=Mandatory HEFT/CPOP and PEFT primary texts unavailable; 4 reviewed original studies, minimum 6 required
AFFECTED_CLAIMS=Faithful B3/B4/B5 definitions and every downstream scientific claim
VALID_EVIDENCE_REMAINING=Repository audit, four scoped primary reviews, seed derivation metadata, tested governance tooling and recorded access responses
INVALIDATED_EVIDENCE=NONE; no scientific evidence has been generated
GITHUB_COMMIT=4d67240c827bdfeaae7831ecc3fd76a3eef36d5a (tested source checkpoint; final report-only closure HEAD resolves live)
GITHUB_PUSH_STATUS=SUCCESS (source checkpoint pushed and remote SHA verified; see P0_push_checkpoint.json)
NEXT_SAFE_ACTION=Obtain lawfully accessible HEFT/CPOP and PEFT original papers, review formulas with page references, complete P0 and rerun audit before P1

HEFT correct DOI is 10.1109/71.993206 (confirmed through Crossref); PEFT is
10.1109/TPDS.2013.57. Metadata is not algorithm verification. IEEE landing pages
returned empty HTTP 202; official PDF requests returned HTTP 418. The UMinho
institutional route redirects to a new host, which was denied by the proxy on
the recorded attempt; an author-page lead was 404. OA-discovery API requests were
also proxy-denied. Complete responses are preserved in acquisition records.

This is a source-access blocker, not evidence that the research hypothesis is
false. No request to relax the literature requirement, substitute guessed
formulas or open reserved partitions is made. Provide these two primary texts or
a working lawful source-access route to resume. Review all newly obtained
originals before counting them toward P0.

The initial setup test failure (15/16 passing) is retained in P0_test_history.json.
Its cause was a test coupled to an unfinished STATUS.md, not a scientific defect.
It was corrected with an isolated fixture; the final tooling run passes 17 tests.
Simulator correctness remains NOT RUN.


## Targeted literature remediation (following delivery ebab07e)

The task-start live HEAD was ebab07e008745aa4200f2f7ac156275400532c36, branch
work, clean worktree, correct JINAOLONG/soc remote. This new task authorizes only
source acquisition/review/documentation, the existing governance tests and P0
audit. The previous report and audit are archived under
reports/history/p0_before_literature_closure_ebab07e/ before active updates.

P0 remains BLOCKED. Newly supplied Marmara and ResearchGate routes failed with
proxy CONNECT 403. Lawful OpenAlex discovery found institutional alternatives;
Porto/RIT/crossref publisher-PDF routes did not supply full text. IEEE landing
responses are empty 202 and PDF endpoints 418. UMinho's public exact-title search
returned zero records. Crossref verified the two bibliographic identities, but
no mandatory original PDF was acquired. Source logs 006–013 preserve each attempt.

The existing 17 governance tests pass; the unchanged P0 audit returns 2 with
four originals counted and heft_cpop/peft unverified. Page-specific checklists
explicitly mark unavailable evidence; no formula was filled from secondary
sources. All 25 protected source/script/config/test files match the task-start
hashes. Scientific workloads run: 0. No simulator implementation, seed change,
reserved realization, or unlock file was created. The six new source domains are
saved as a network draft; runtime access/publication are not inferred from that.

NEXT_SAFE_ACTION=Supply lawful originals or apply the required source access,
then inspect their algorithm pages and rerun P0; stop without starting P1.

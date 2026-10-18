# P0 blocker / preserved failure record

STOP_STAGE=P0
STOP_REASON=Mandatory HEFT/CPOP and PEFT primary texts unavailable; 4 reviewed original studies, minimum 6 required
AFFECTED_CLAIMS=Faithful B3/B4/B5 definitions and every downstream scientific claim
VALID_EVIDENCE_REMAINING=Repository audit, four scoped primary reviews, seed derivation metadata, tested governance tooling and recorded access responses
INVALIDATED_EVIDENCE=NONE; no scientific evidence has been generated
GITHUB_COMMIT=Resolve live HEAD with git rev-parse HEAD; source checkpoint recorded after first commit
GITHUB_PUSH_STATUS=NOT ATTEMPTED at this report's initial creation
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

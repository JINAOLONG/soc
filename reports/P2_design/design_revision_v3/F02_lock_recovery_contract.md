# F02 — two unapproved coordination and recovery contracts

D04/D09/D10; SP10/SP20 as dependencies, no new SP numbering. Both alternatives PROPOSED_REQUIRES_APPROVAL; selected policy null. Existing v2 fail-closed/fsync/immutable evidence/replay/zero retry preserved. Different authorization IDs distinguish receipt identities, not exclusion domains; no runtime duplicate execution has been demonstrated.

## Shared exclusion and identities

Exact schemas: P2_typed_identity_schema_v3.json BUDGET_SCOPE_PREIMAGE_V3,COORDINATION_DOMAIN_PREIMAGE_V3,COORDINATION_RECORD_V3. Budget scope binds already-known blueprint, untouched matrix SHA, registered CALIBRATION metadata and immutable root execution authorization. Registry enforces ONE root authorization for the blueprint/matrix/partition scientific budget tuple; a new hash alone cannot create another budget. Replacement authorizations under B descend from that root and cannot change budget/counts. A new scientific plan needs separate explicit review and budget registration, never automatic recovery.

Domain=(budget_scope_sha,purpose,semantic_target_id), where INPUT_GENERATION uses descriptorID, PRIMARY_EXECUTION uses exact symbolic trialID, REGISTERED_REPLAY uses that same trialID with different purpose. All known before materialization/spawn. No attempt,replaceable authorization,lease owner,content SHA or future run result participates in exclusion key. MAIN and controls have different descriptors but one scope; primary/replay have separate registered single-use slots. Replay still belongs to same scientific sample, not retry.

All mutations go through one authoritative linearizable coordinator and trusted admission/publication authority; workers cannot bypass it. This is a deployment trust assumption requiring later implementation proof, not an existing service. Registry and data persist durably. State observations use server monotonic ticks and clock_id including server boot identity, never host wall-clock expiry. Lease deadline is an explicit positive future tick chosen by an approved deployment profile; no duration default here. Clock identity loss/reboot makes lease validity UNKNOWN and closes admission pending explicit recovery; it does not imply expiration/permission.

Every immutable coordination body includes domain,policy,revision,parent record hash,active authorization,owner,epoch,clock/deadline,phase,spawn_reserved_ever,original attempt,inventory/receipt refs and optional explicit recovery authorization. No own hash in body. Parent hash null only at first record, revision increments1. CAS expected value is EXACT (domain,current_record_sha,revision,owner,epoch,active_authorization,phase,clock_id) plus current server time within lease; compare whole pointer/version, not just owner name. Mismatches preserve conflicts and reject. All staged/receipt writes are domain/owner/epoch authenticated. Invalid/failed/incomplete artifacts never accepted COMPLETE.

## Common phase transitions and CAS prerequisites

| Transition | Required expected state / extra predicates | Effect |
|---|---|---|
|ABSENT→PREPARED|Domain absent; approved root/plan/authorization; no prior slot record, unique effective policy|Atomic create owner,epoch0,revision0,spawn_reserved_ever=false|
|PREPARED→SPAWN_RESERVED|Exact current pointer; valid owner/lease/auth; no spawn ever; source/input/provenance preguards valid|Durably consume ONE slot before authoritative process admission; flag permanently true|
|SPAWN_RESERVED→RUNNING|Same current epoch/owner; trusted admission admits original attempt once; no uncertainty|Append actual start evidence; never second admission|
|RUNNING→OUTPUT_READY|Same owner/epoch; actual child exit0 and complete immutable raw output refs|Append output inventory; preserve actual nonzero/unknown exit separately as failure|
|OUTPUT_READY→VERIFIED|Same owner/epoch; independent validation/metrics and registered replay/provenance requirements all valid|Append verified inventory; no science classification inferred|
|VERIFIED→PUBLISHED|Same owner/epoch; exact expected prior pointer; all raw bytes/inventory durably closed/fsynced; receipt hash known|CAS publish completion pointer binding immutable receipt and original verified-record hash|
|Any nonterminal→HALTED/FAILED/INCOMPLETE|Actual lease/auth/source/process/error evidence; append-only CAS against current record|No automatic reset to PREPARED, no count refund|
|PUBLISHED→reuse observation|Original full refs/identities exact and immutable|New read-only reuse receipt; original pointer not rewritten,0new engine calls|

Completion receipt references the VERIFIED record, not its own PUBLISHED record or pointer; write bytes/fsync, immutable receipt/fsync, then CAS pointer. If CAS loses ownership, bytes remain quarantined and do not constitute COMPLETE. Hash cycles are avoided: domain→prepared→reserved→output→verified→completion receipt→published pointer; the pointer is outside its own receipt inventory.

SPAWN_RESERVED is conservative: a crash before known admission consumes the allowance and becomes INCOMPLETE. Unknown started status never authorizes another spawn. This sacrifices liveness to protect the registered maximum budget. One primary+one replay remain maximum, automatic retry0. Verification/publish-only recovery is not a new engine run and requires explicit scope authorization; it cannot fill missing outputs by regeneration.

## Alternative A — unique immutable authorization, no takeover

Once domain PREPARED exists, authorization and owner are immutable for its lifetime, epoch remains0. Concurrent same-authority requests observe existing record but cannot acquire another owner/admit another process. Different active authorization is rejected. Lease is a health/admission bound; expiration/owner loss closes admission and records HALTED. No ownership transfer, automatic extension, active authorization replacement or deletion to recreate the domain. Renewal, if explicitly preauthorized by the unchanged profile, requires original owner exact CAS before expiry and cannot reset spawn history. After expiry no renewal/resume of scientific process.

Archive/release is explicit terminal evidence, never making the original key ABSENT or replenishing budget. If owner is unavailable, source creation/execution remains blocked. Authorized verification/publish-only recovery uses a separate receipt; original attempt remains immutable and only existing complete bytes may be verified/published by the authority under explicit recovery permission. No stale owner may publish after HALTED; authority enforces that state. This is simpler safety with no takeover/liveness guarantee.

## Alternative B — fenced transfer under fixed budget

If server clock validity known and lease expires, explicit signed recovery/replacement authorization under SAME root/domain may CAS the exact prior pointer to new owner,epoch+1,revision+1. Current phase,original attempt,spawn_reserved_ever and byte inventories remain. No reset/refund. New authorization must cite old and new epoch/owner, allowed actions and original artifacts; policy change not allowed.

Old epoch cannot admit processes, stage authoritative writes or publish. This must be checked at the trusted authority's actual linearization point, not just a worker's earlier client check. A worker with direct ungated spawn/write is outside the trust contract and invalid. Recovered owner may reserve/admit only if prior phase PREPARED and spawn_reserved_ever=false with independently known no earlier admission. If flag true, phase RUNNING, actual start uncertain or process may still be alive, takeover permits only inspection/verification/publish existing data, never new materialization/primary/replay. An original process already admitted must be contained/terminated or remain unaccepted until identity/immutability checks; no overlapping accepted writers or fabricated COMPLETE.

If coordinator cannot establish exclusive control, epoch/clock persistence or one-use admission, fail closed. Fencing does not prove a dead worker cannot run CPU instructions; it rejects unauthorized admission and authoritative publication and does not restart after admitted/uncertain process. Lost partition authority cannot autonomously declare itself current. This route costs a durable linearizable service, fencing enforcement and more fault tests; these capabilities do not currently exist in this project.

## Hand-authored adversarial sequences (no lock/runtime code)

| Sequence | A | B | Invariant |
|---|---|---|---|
|Two auths seek same domain|Second rejected|Replacement only exact CAS/explicit recovery; otherwise reject|One owner/admission domain|
|Crash after PREPARED, definitely before reservation|HALTED, no takeover|Explicit fenced transfer possible; prior false flag preserved|No silent retry|
|Crash after reservation, before known spawn|INCOMPLETE; slot consumed|Transfer cannot spawn|Uncertainty does not refund|
|Network pause; old owner wakes after expired/changed epoch|HALTED owner rejected|Old epoch rejected at authority|No stale authoritative write|
|Two claimants race expected revision|At most one atomic create/CAS|At most one CAS; loser conflict retained|Linearizable uniqueness assumed/test pending|
|Crash after immutable receipt, before pointer|Explicit publish-only recovery|Same plus current fencing|No new engine call|
|Same ID with different bytes|Conflict/INVALID|Conflict/INVALID|Never latest-wins|
|Server monotonic clock reboot unknown|Block|Block; no inferred timeout takeover|No cross-clock expiry inference|
|Completed artifact missing original raw refs|Reject reuse|Reject reuse|No rebuilding similar data as old COMPLETE|
|Replay absent after primary0|INCOMPLETE|INCOMPLETE; no extra primary|Replay not science sample/retry|

Typed dependency graph is acyclic because root authorization and descriptors/trial labels exist before domains/owner receipts; provenance for completed processes comes after their starts; verified/completion/published reference only earlier bodies. A future separately authorized implementation must verify coordinator durability/linearizability, duplicate admission, lease renewal/expiry/clock reboot, two auths, partitioned old worker, stale writes, crash at every fsync/CAS boundary, immutable parent records, consumed-unknown spawn, no extra replay and complete-bundle reuse. All NOT_RUN. Static case tables do not prove runtime atomicity.

Human choice: A_NO_TAKEOVER or B_FENCED for the exact contract/version/hash, or defer/request revision. Deployment lease profile, trusted executor/publication backend and its proof must be separately specified before implementation readiness. Neither branch approved/default. Automatic retry remains0 in both.

Fenced transfer is allowed only from nonterminal PREPARED/SPAWN_RESERVED/RUNNING/OUTPUT_READY/VERIFIED. PUBLISHED/HALTED/FAILED/INCOMPLETE cannot transfer or return to an active phase; any read-only recovery diagnosis is separate append-only evidence,never a relabeled COMPLETE scientific attempt. Publish-only recovery is limited to still-valid VERIFIED with original full artifacts. Renewal is not a new admission and cannot reset history.

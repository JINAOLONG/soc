# Identity, generation and recovery — fresh adversarial report

Review target: the unchanged v2 proposal at starting commit
`a3680acf45c5578fc090cf53cc186f28a8e9b88a`. This is a coordinated fresh review by the
same assistant, not a third-party audit. D04/D09/D10 remain **UNAPPROVED**.

The first-materialization circularity identified in historical V2-F02 is removed
at the specified hash/availability level. The declared 35-node/40-edge graph is
acyclic, and an independently assembled dependency inventory for all 21 typed
preimages is acyclic. This supports the documented first-use order; it does not
verify process orchestration. Two approval-readiness gaps remain: the coordination
domain and stale-owner publication contract (ID-R01), and the exact mandatory
binding of actual executing Git/dirty provenance (ID-R02). ID-R03 is a count-text
defect: the KEY contains 14 fields, although the generation contract says 15.

`identity_findings.json` gives each finding's exact source paths, line ranges,
actual SHA-256, severity, facts, missing evidence and human question.
`identity_source_reads.json` records 19 source-file byte hashes. The static
inspection in `identity_static_review.py.txt` returned exit 0 with **47 observation
assertions verified / 0 assertion failures**. Several assertions deliberately
verify the existence of unresolved design gaps, so this count is not a design
acceptance verdict. No scientific key, draw, payload, trace, run or seed was created.

## First required use and hash dependency audit

The exact object field sets are in
`docs/P2_design/v2/P2_typed_identity_schema_v2.json#/$defs`; the registry has 21
closed preimages. All local schema references resolve among 61 definitions. Their
raw/semantic conventions are read jointly with the runner, not inferred from the
names of hash fields.

| Preimage / identity | Earliest available prerequisites | First required use / conclusion |
|---|---|---|
| SOURCE_BUNDLE | Frozen code/dependency/model files and their earlier source commit | Authorization/run identity; explicitly excludes its own instance and later metadata commit. No semantic self-cycle. Actual invoking Git provenance remains ID-R02. |
| ENVIRONMENT | Actual pinned interpreter/numeric/dependency/host facts | Run identity, before spawn; no results required. |
| BLUEPRINT | Frozen generator/model/parameter tables and committed calibration metadata/allowlist hashes | Plan/descriptor; no payload, resolution, run or result hash. |
| EXECUTION_PLAN | Blueprint, symbolic roster/method bindings, approved analysis/observer/stage definitions and approval evidence | Authorization; symbolic input references are legal here. |
| INPUT_DESCRIPTOR | Blueprint, registered condition/config/seed/variant; control additionally has already-known MAIN descriptor | Generation authorization/input lock; no future parent payload. Parent MAIN descriptor is a separate instance, not recursive self-reference. |
| EXECUTION_AUTH | Blueprint, plan, frozen source bundle and independent explicit authorization evidence | Generation and run attempts; not produced by a design PASS. |
| GENERATION_AUTH | Descriptor, blueprint/plan and execution authorization | Input-lock acquisition and generation attempt. |
| INPUT_LOCK | Blueprint, descriptor and generation authorization | Pre-materialization exclusion; contains no payload/workload/run identity. Exclusion semantics across authorization replacement remain ID-R01. |
| GENERATION_ATTEMPT | Descriptor, generation authorization, input-lock identity, ordinal 1 | Actual generation invocation/log paths, before process start. |
| GENERATION_RECEIPT | Actual successful generation process record, payload raw/content hashes, exact-estimate sidecar reference | Input resolution; produced after process/output preservation, never required before generation. Failure has no successful receipt. |
| MATERIALIZED_INPUT | Descriptor, actual content hash, control parent MAIN content when applicable | Independent input validation/resolution; no own ID or envelope hash. |
| INPUT_RESOLUTION | Materialized content, generation receipt and independent pre-envelope validation; control MAIN resolution/transform report | Workload publication. Validation report must not reference the future workload/envelope. |
| WORKLOAD | Blueprint, descriptor, materialized input/content | Published only after resolution verifies; excludes resolution time and receipt/attempt IDs from semantic preimage. Availability requirement is not a hash self-cycle. |
| SEMANTIC_ARGV | Worker protocol/source, role/method, resolved workload; semantic options exactly empty | RUN semantic identity; actual output/attempt paths are rendered later. |
| RUN | Plan/trial, workload, method/source/environment, primary semantic argv, observer/validator/metrics/replay protocols | Attempt/run lock and later raw output headers; no attempt or result hash. |
| ATTEMPT | Run, execution authorization and ordinal 1 | Actual argv/path rendering/run-lock identity before invocation. |
| RUN_LOCK | Run and attempt | Pre-invocation mutual exclusion; ID-R01 applies to the actual coordination domain. |
| DENOMINATOR_SCOPE | Run, primary attempt and observer specification | Primary observation deduplication scope; independent of later state outcomes. |
| STATE_KEY | Scope hash and public state hash | First unique-state record; event sequence is separate, not a scientific result. |
| REPLAY | Run, primary attempt, actual primary trace hash, registered replay protocol and ordinal 1 | Registered replay after primary output exists; no replay comparison result required in advance. |
| COMPLETION | Original process/input/validation/metrics/replay/inventory references already preserved | Immutable COMPLETE receipt and pointer publication. Inventory excludes itself and future completion receipt. CAS/ownership detail remains ID-R01. |

The report graph is explicitly a union of MAIN and control branches. Its two
arrows into `resolved_workload_ID` do not require MAIN to wait for its own controls.
MAIN resolves first; each control then resolves against that original MAIN. The
typed registry, not an unlabeled interpretation of the union graph, defines hash
dependencies (`identity_dependency_graph.json:211–220`, runner `:58–60`).

Two availability checks address hidden cycles:

1. Input validation occurs before the scientific envelope. It reads payload,
   descriptor, original generation receipt and parent/transform, not the future
   workload ID (runner `:34–36`). Thus the envelope cannot be demanded by that
   validation step. Full lineage is checked again at pre-invocation.
2. RUN hashes semantic argv only; actual argv contains run/attempt paths rendered
   after their IDs exist (runner `:64–71`). Actual argv must still match the exact
   template; excluding it from the hash is not permission to add ignored flags.

No hidden hash cycle was established in the current documents. A future
implementation could violate these rules; the tests below must catch that.

## Generation and MAIN/control inheritance

Generation JSON `:78–90,98–128,141–327` specifies the following without requiring
runtime observations:

- The three bindings exactly match the closed **14-field** KEY. `LITERAL` copies a
  fixed value and `COPY` reads only a declared typed MAIN context path. No omission,
  coercion or extra operation is allowed. Method, run/attempt, host, wall time,
  scheduler calls and control variant do not enter the draw key. No production
  KEY or hash-to-U operation was executed during this review.
- Arrival jitter clears group/node/resource/edge; the estimate factor retains
  group/node and clears resource/edge; realized-duration factor additionally
  retains resource. Domains and schema/generator versions are explicit.
- Decimal parameter lexemes are exact rationals before one final binary64
  conversion. Relative deadlines use pre-round estimated costs. Absolute deadline
  uses the model's RN64 addition at actual admission. Scientific/runtime byte
  reproduction remains untested.
- Both controls derive from the same independently resolved MAIN and preserve
  each retained service/node ID, graph, all compatible estimate/realized bit
  patterns, edges and relative-deadline bits. They change arrivals, and H_ISOLATED
  removes L. They have separate descriptor/content identities.
- G takes the maximum over all **100 parent MAIN services**, including L for the
  H-only control, from hashed pre-round estimate/deadline sidecars and exact
  communication values. Both controls use the same integer G. Actual G was not
  evaluated. No feasibility or isolation success is inferred from the formula:
  the future control trace must demonstrate nonoverlap and the required deadline
  witness.
- Materialization order MAIN→controls is independent of engine order
  H_ISOLATED B2→LOW_COMPETITION B2→MAIN B1–B5. Original draw values must never be
  regenerated from changed control arrivals.

ID-R03 is a literal text/count discrepancy, not evidence that any field is missing
from the matching schema/bindings. Adding a guessed fifteenth field is forbidden.

## Concurrency, stale owners and publication

The v2 runner already gives substantial fail-closed rules. It rejects draft or
unknown provenance before generation; retains failed/partial evidence; requires
explicit authority for stale-lock release; refuses same-ID/different-bytes and
missing original refs; publishes immutable receipts only after data preservation;
requires a final CAS completion pointer; and prohibits automatic retries.
These requirements must be retained. An unimplemented lock is not itself a defect
in a report-only design.

ID-R01 concerns missing semantics within those rules. No current v2 specification
binds the coordination exclusion domain independently of authorization replacement,
or states that only one authorization for a semantic descriptor/run can ever be
active. There is no exact owner/lease/fencing record, expiry-clock rule, lost-owner
write/spawn rule or CAS expected-version contract. These omissions matter before
one can approve the promise of at-most-once invocation under concurrent recovery.

A hand-authored metadata example changes only an arbitrary authorization digest.
The typed input-lock and run-lock identities then differ while the arbitrary
descriptor/run label stays fixed. The example is saved inside static results. It
does **not** instantiate a production descriptor, authorization, workload or lock.
It also does not establish that lock IDs are used as storage keys: the current
documents never specify that mapping. The demonstrated issue is that a designer
still has to choose an exclusion domain and authority-replacement policy.

Consider a paused owner A, lease expiry, and an explicitly authorized owner B
performing publication-only recovery. "Check lease" and "CAS" alone leave open
whether A is allowed to resume a write/process start, what version B compares, and
whether a partially durable pointer can be accepted. Either an explicit no-takeover
policy or a fully specified fenced takeover protocol can be a viable future
choice. Neither is silently adopted by this review, and no lock is implemented.

## Failure, reuse, recovery and zero retry

| Case | Current specified disposition | Remaining boundary |
|---|---|---|
| Before valid blueprint/authorization | Reject before generation; preserve rejection | Future guard tests, not a current execution. |
| Input lock/GEN PREPARED, process not started | Keep owner/lease/attempt and `process_started=false`; explicit release/archive authority only | ID-R01: exact stale-owner semantics. |
| Generation incomplete or payload without receipt | FAILED/INCOMPLETE; preserve partial bytes/logs; stop, no extra draw | No reuse as COMPLETE. |
| Payload and original generation receipt complete; validation unfinished | Existing bytes may be reverified under explicit recovery authority; append new receipt, no extra generation | Do not invent successful validation or replace birth refs. |
| Resolved input but engine not started | Preserve original resolution; no resetting an INCOMPLETE attempt to PREPARED | A new actual invocation requires separate preregistration/authority. |
| Primary failure or unknown/interrupted exit | Stop plan, retain actual/null exit; no automatic retry | An actual new call cannot be hidden as recovery. |
| Primary complete, replay/verification incomplete | Not COMPLETE; explicit authority may finish only missing registered steps without repeating completed processes | Replay remains the one preregistered subexecution; if it had already started and failed, an additional replay is a new call requiring changed authority/budget. |
| All evidence exists, completion pointer missing | Explicit publication-only recovery may add a receipt, zero engine calls | ID-R01: owner/fencing/CAS and pointer reconciliation need precision. |
| Existing COMPLETE | Recheck every original identity/hash/reference and invariant; new reuse receipt, zero calls/samples | Rebuilt similar content cannot patch missing original provenance. |
| Same ID different bytes, lost refs or conflicting owner | Preserve conflict and fail closed | Do not select newest evidence, silently overwrite, or invent a new ID to conceal conflict. |

The automatic retry budget is zero. Primary and registered replay have separately
declared budgets of 2520 each; replay is not a scientific sample, repair retry or
permission to rerun after a failed replay. Append-only recovery is consistent with
zero retry only when no already-started process is repeated. The v2 prose states
that any new actual call requires separate advance registration; this review does
not expand the original budget or authorize recovery.

## Actual checkout provenance gap

Original contract `docs/user_request.txt:2506–2527` and `AGENTS.md:45–49` require an
actual Git commit and dirty status for each scientific run. Runner `:30–32`
explicitly says frozen source commit and actual execution HEAD are separate.
`SOURCE_BUNDLE_PREIMAGE` contains `source_commit` and a rejection `dirty_policy`;
`SCIENTIFIC_RUN_RECORD` and `PROCESS_RESULT` contain neither observed execution
HEAD nor observed dirty state. Their closed field sets cannot accept an invented
field. A generic `raw_artifacts` array could carry another report, but no mandatory
provenance kind/body schema or completion binding is specified.

This does not permit omission: the prose requirement remains authoritative.
It means the exact typed design leaves implementers to invent the required record.
A metadata-only commit can legitimately move actual HEAD while frozen relevant
source bytes stay unchanged, so substituting `source_commit` would lose information.
Similarly, `REJECT_RELEVANT_DIRTY_OR_UNTRACKED` is a policy, not the actual check
result. D10 needs an explicit required record/ref or fields before full approval.

## Future separately authorized runtime acceptance tests — NOT EXECUTED

These are test requirements, not implemented fault-injection code. Use designated
non-scientific correctness fixtures during implementation verification; do not use
registered scientific realizations merely to exercise failure paths.

| Test | Required observation |
|---|---|
| IR-RT01 Initial MAIN materialization | Pre-generation guard succeeds only on approved/frozen identities and explicit authority; it does not demand nonexistent payload/workload/run IDs. Inspect operation order. |
| IR-RT02 Control first-use | Control cannot derive before original MAIN resolution verifies; control uses that MAIN's numeric bits and sidecar, never new keys. |
| IR-RT03 Independent identity reconstruction | A separately written decoder recomputes every preimage/raw/content identity; self-ID, missing/extra field, type/coercion, duplicate JSON key and incompatible canonical version reject. |
| IR-RT04 Source/argv boundary | Attempt/output path changes do not silently alter scientific semantics; actual argv must match deterministic rendering, and extra flags/direct-worker bypass reject. |
| IR-RT05 Same descriptor concurrent request | After D09 coordination policy is specified, two requesters for the same semantic input cause at most one materialization start, with both requests recorded. |
| IR-RT06 Authorization replacement race | Reissued authorization cannot bypass descriptor/run exclusion or budget accounting. Reject nonregistered supersession and preserve old authorization/attempt evidence. |
| IR-RT07 Lost/stale owner | Pause an owner before each mutating phase, expire/resolve according to the approved policy, and resume it. It must be unable to start another process or alter the accepted pointer/bytes after losing authority. No automatic takeover is inferred. |
| IR-RT08 Durable publication cuts | Interrupt before/after each payload fsync, directory durability step, immutable receipt publication and pointer CAS. Only an entirely verified original bundle may resolve COMPLETE; partial/contradictory pointers fail closed. |
| IR-RT09 Wrong CAS version/conflict | A competing publisher or same-ID/different-bytes artifact cannot overwrite the original. Preserve both conflict diagnoses and permit no silent newest-wins selection. |
| IR-RT10 Spawn/process failure | Spawn failure, signal, interruption without exit, nonzero child and clock anomaly retain truthful process fields/logs. Unknown exit remains null; no later trial or retry starts automatically. |
| IR-RT11 Original-reference loss | Delete/corrupt a required original ref in a correctness fixture; recreating equivalent payload under a new birth receipt cannot repair that old run to COMPLETE. |
| IR-RT12 Reuse and publication-only recovery | Verify zero new generator/engine/replay calls, no new scientific sample, new append-only reuse/recovery receipt and exact original identity checks. |
| IR-RT13 Replay accounting | One registered replay after primary; exact required decision/physical/metric comparisons and separate raw process record. Failed/already-started replay cannot be repeated under the initial budget. |
| IR-RT14 Completion conjunction | Missing validation, metric mismatch, missing replay, corrupt ref or unresolved lineage rejects COMPLETE even with child exit 0. A valid negative may complete execution but cannot unlock progression. |
| IR-RT15 Actual checkout provenance | Move only report metadata HEAD while source bundle stays fixed: both identities and actual dirty state must remain recorded distinctly. Dirty relevant source must reject under the approved policy; generic policy text is not the observed record. |
| IR-RT16 P1/scientific separation | Preserve original P1 origin/serialization and rerun its required correctness evidence after implementation changes. Reject renamed/relabelled fixture payloads, forged birth receipts and control-parent swaps. |
| IR-RT17 Budget interruption accounting | At each failure/recovery point, independently count generator/primary/replay process starts; no hidden additional attempt and no duplicated sample. Any extension requires new explicit preregistered authority. |
| IR-RT18 Protected reference paths | Reject traversal, unauthorized symlinks, wrong root/partition, malformed raw hash/size, and inaccessible required references before invocation or reuse. |

No tests in this table were executed. The current worker remains a proposed absent
module; schema parsing and hash arithmetic cannot validate concurrency or science.

## Required human decisions and stop

1. D09/D10: specify the authorization-independent coordination domain or strict
   single-active-authorization policy, stale-owner disposition, exact ownership
   record and publication-CAS invariants before approving the recovery promise.
2. D10: specify a mandatory typed actual-execution provenance record/ref and its
   COMPLETE binding, retaining frozen source and actual checkout identity separately.
3. D04/D10: correct the KEY field-count text to the existing 14-field set without
   inventing another field or changing keyed draws.

All options above are **UNAPPROVED** recommendations for a separately authorized
documentation revision. No implementation, workload generation, P2 execution,
parameter freeze or validation/formal unlock follows from this report.

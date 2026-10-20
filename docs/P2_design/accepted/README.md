# Accepted conversation decisions and engineering scope

The user explicitly accepted D01–D08 and SP01–SP40, the five scoped D10
provisions, six D09 runtime rules, and the six-part A2 and B3 contracts in the
current conversation. `decisions.json` preserves the answers, source hashes,
exceptions, and the implementation authorization. Historical V1/V2/V3 draft
files and failed reviews are intentionally unchanged.

Selected definitions: F01 `B1_EXPAND_SINGLE_READY`, F02 `A_NO_TAKEOVER`,
criterion `COARSE`, scientific adapter `S2`. All synthetic numbers remain
synthetic; no hardware profiling claim follows. The corrected FUSION source
edges govern SP07, not the earlier erroneous dialogue table.

The B1 global coverage-one negative remains structurally unreachable under
the registered model. A supported bounded observation is not candidate benefit;
failure to meet support without complete negative coverage is INCONCLUSIVE.
No scientific observations have been made.

## A2 accepted publication overlay

R is the prior VERIFIED coordination body; Q is the original purpose-specific
completion artifact; I is the complete artifact inventory; P is the authoritative
PUBLISHED body. P binds R by exact parent raw SHA and revision+1, Q by receipt
SHA, and I by inventory SHA. Immutable domain/owner/auth/epoch/attempt/history
constraints remain. R and P bind the same I. A provenance-only inventory is not I.

Primary Q's existing artifact-inventory field must agree with I. Generation
and replay Q retain their existing layouts; no nonexistent inventory/VERIFIED
field is invented. R does not prefill a future Q SHA. I excludes itself, R, Q,
P and reverse/future references. Bytes and directories are persisted before
publication; a failed CAS leaves unaccepted materials, not COMPLETE evidence.

This explicitly supersedes the direct Q→VERIFIED wording in historical F02
line28 without editing its bytes. Current state/auth/lease must be checked at
the authority operation. Hash closure alone never proves actual publication.
Historical published reuse does not require the historical lease still be alive.
Terminal scientific attempts cannot be reactivated.

## B3 accepted restricted records

Only two new record kinds:

* `F02_RECOVERY_AUTHORIZATION_V1`, namespace
  `soc.p2.f02.recovery-authorization.v1`, ID prefix
  `urn:soc:f02:recovery-authorization:v1:`.
* `F02_OPERATION_RECEIPT_V1`, namespace
  `soc.p2.f02.operation-receipt.v1`, ID prefix
  `urn:soc:f02:operation-receipt:v1:`.

Both use schema_version1 and SEMANTIC_CANON_V2 over the complete closed body;
ID is prefix+SHA256(body). Own ID/hash stays outside the body. Raw file byte
references have separate verification responsibility.

Authorization required fields: namespace, schema_version, profile_ref,
issuer_id, executor_id, action, budget_scope_ref, root_authorization_ref,
domain_ref, expected_record_ref, subject, inventory_ref, completion_ref,
validity, issued_at_utc, authorization_evidence_ref. completion_ref may be null
only for VERIFY_EXISTING before Q exists. validity is the closed object
{clock_id,not_before_tick,not_after_tick}; effective interval is [start,end),
start<end, trusted clock identity required. UTC is audit metadata, not lease time.

Subject unions:

* INPUT_GENERATION: purpose, descriptor_ref, generation_attempt_ref.
* PRIMARY_EXECUTION: purpose, trial_id, run_identity_ref, attempt_ref.
* REGISTERED_REPLAY: purpose, trial_id, primary_run_identity_ref,
  primary_attempt_ref, primary_trace_ref, replay_identity_ref.

Generation domain target/attempt bind original descriptor/generation attempt.
Primary binds original trial/attempt. Replay binds same trial with distinct
purpose and original registered replay identity, not a new attempt. Replay
does not require parent primary PUBLISHED, avoiding a dependency cycle.

Operation required fields: namespace, schema_version, profile_ref, request_ref,
authorization_ref, actor_id, action, authority_evidence_refs, validation,
process, started_at_utc, ended_at_utc, result, error_refs. Results are SUCCESS,
REJECTED, FAILED, INCOMPLETE. Unparseable authorization/actor/action, unfinished
validation and unknown timestamps may be null only without claiming SUCCESS.
Process may be null when none started or no trustworthy process record exists;
unknown start requires INCOMPLETE and retained observations. No fabricated exit0.
SUCCESS requires the matching grant, PASS report and actual authority evidence.

VERIFY_EXISTING checks existing complete data and explicitly authorized unfinished
checks; it cannot regenerate missing science data or repeat completed processes.
PUBLISH_EXISTING applies only to still-valid VERIFIED with complete materials.
REUSE_OBSERVATION appends an exact-reuse observation, not new samples/calls.
No action changes owner/auth, refunds budget, revives terminal state or restarts
reserved/started/uncertain calls. Grant references precede operation; P may bind
an existing grant, never the later operation receipt. Conflicts remain append-only.

Exact structural checks are in `soc.p2.recovery.b3_schemas`; referential checks
are separate. This adds no signature envelope or third authority-proof type.

## Engineering authorization and outstanding deployment evidence

User instruction: “直接使用当前云环境做实现与正确性验证，运行结果需要保存”.
This authorizes implementation, hand-authored correctness tests, retained
reports, normal commits and GitHub publication within the existing project
workflow. It does not authorize registered input materialization, scientific
bootstrap/CI/results, restricted outcomes or later-stage unlocks.

SQLite authority tests use literal hand domains, artificial clocks and temporary
databases. They do not freeze lease values or prove host power-loss durability.
Source mode-bit checks do not prove kernel isolation. Deployment profile,
persistent storage, actual authority principals, lease values, sealed worker
validation and separate science authorization remain required. Production
calibration fails closed with explicit reasons; there is no force flag.

Use `.venv/bin/python -B scripts/run_p2_correctness.py` for the engineering
suite. Each invocation retains a new report directory, real child exits/logs,
hand fixture traces/replays, a SQLite fixture/history and SHA256 manifest.
P0/P1 official audit commands remain separate; no engineering PASS implies P2 PASS.

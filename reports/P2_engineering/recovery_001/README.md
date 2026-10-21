# One-time local recovery: engineering verification

The user instructed continuation directly after the exact one-recovery-call
proposal. The accepted overlay preserves original input, code, result and
unknown-state evidence, with unique result slots2520 and total call cap5041.

All125 tests passed, zero failures/skips.8 new hand-authored recovery tests
check exact one-use accounting, no overwrites/repeated completed calls, rejection
of wrong input/unapproved unknown/second uncertain recovery, fixed source roster,
no regeneration of partial inputs, and bounded config-target admission.
P0/P1 official audits both exit0. All49 original scientific execution files
match original commit bytes and the original no-LF source-inventory digest.
The new orchestration source identity is recorded separately.

The initial new inventory comparison used payload canonicalization with an
extra LF and failed before science. It was corrected to the existing source
canonicalization; the failed check is retained in preflight_history.json.
This did not change any original scientific file or execute a science call.

Baseline status and P0/P1 evidence were copied before updated verification.
Scientific continuation is separate and must use committed execution source,
explicit immutable per-call reservations and actual foreground process exits.

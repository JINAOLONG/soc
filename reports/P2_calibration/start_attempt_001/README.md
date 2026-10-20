# CALIBRATION start check — blocked before scientific generation

The user instructed “进入下一步实验”. This is recorded as authorization for the
next registered CALIBRATION stage, within the accepted B1/COARSE/A_NO_TAKEOVER
scope. No later partition is authorized. This report records a real preflight
check, not an experimental trial or a scientific sample.

Observed checkpoint: `5166111a4cc295c007848402ec7918d0348e803c`, branch `work`,
remote work equal to HEAD, parent `dc87865e4217198e8646603ce57f1c94462ff246`.
The worktree was clean before report creation. `commands.json` and individual
stdout/stderr files retain actual Git, storage and audit observations, commands,
timestamps, host and process exit codes. The captured Git status after this
directory was created contains only this newly created report.

P0 and P1 existing-evidence audits both exited 0. The unchanged scientific entry
exited 2. The 110-test correctness evidence was audited, not rerun. No source,
protocol, scientific threshold, seed or partition was modified. All previously
accepted source-definition hashes were recomputed and matched.

The raw entry report still contains `SCIENTIFIC_EXECUTION_NOT_AUTHORIZED` and
`scientific_execution_authorized: false`: these are hardcoded in the current
runner and stale relative to the new instruction. They must not be cited as
evidence that the user withheld permission. See the later conversation scope
note in `docs/P2_design/accepted/calibration_authorization_001.json`. The raw
output is preserved; no source guard was removed to manufacture readiness.

The production CALIBRATION entry currently returns preflight only. It does not
implement the fixed 2520-primary-slot execution loop, concrete authority/worker
integration or complete scientific artifact closure. The prior image validated
hand fixtures, not a deployed scientific worker. No approved lease duration,
clock/principal/storage profile or verified durable storage was found. The
observed overlay mount and SQLite engineering fixtures do not prove persistence
after environment destruction. GitHub publication of code/reports does not prove
live authoritative state durability.

`summary.json` separates user authorization from these actual prerequisites.
AGENTS.md rule10 requires stopping scientific progression on missing prerequisites.
Scientific workload generation/run counts remain 0/0; no registered analysis,
new seeds, non-CALIBRATION outcomes or unlocks occurred. No scientific result or
P2 PASS is claimed. Existing failed checks and engineering evidence are retained.

Next work is concrete production integration plus approval/verification of the
minimal deployment profile; it is not another scientific design review or B1
proof. Recheck readiness afterward under the received CALIBRATION authorization.

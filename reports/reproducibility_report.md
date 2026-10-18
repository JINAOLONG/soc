# Reproducibility report — before checkpoint clone test

P0 setup has been executed and repeated in /workspace/soc. Installation creates
a local .venv, pins setuptools 80.9.0, installs the editable package, verifies
four primary PDFs and runs the standard-library tests. Final tooling checks and
stage-entry exit codes are in P0_checks_001.json. P0 returns 2 / BLOCKED; P1,
validation and formal entry also refuse execution before any workload generation.

Seed generation is deterministic and repeatable: the second invocation verifies
the existing file without rewriting it. Metadata SHA256 is recorded in the P0
audit. No absolute /tmp path is used by repository code or saved setup commands.
Reviewed sources can be fetched from their recorded URLs and must match SHA256;
the ignored cache is a convenience, not the authority for scientific claims.

A clean local clone installation/reproduction check is pending the first commit.
Remote clone reproducibility and publication into a new cloud task are NOT YET
VERIFIED. P1 simulation reproduction is NOT APPLICABLE because no engine exists.

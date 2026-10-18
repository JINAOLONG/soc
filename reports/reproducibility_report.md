# Current P0 reproduction scope with user-provided originals

The current instance has six actual primary files with matching SHA256 and notes.
The original audit returns 0/PASS and the original 17 governance tests pass.
P0_local_pdf_checks.json contains the actual commands and outputs.

Two files are user-supplied, not redistributed on GitHub. A fresh checkout must
receive them again at the cache paths in literature_evidence.json and validate
SHA256 before installation/audit. Their sediment primary_url entries identify
actual attachments, not urllib endpoints; the unchanged helper cannot fetch
missing private copies. It verified all six existing files in this task without
network access. No six-file fresh-clone or new-cloud-task restoration is claimed.

The older clean-clone result below is specifically for the earlier four-source
P0 tooling checkpoint; it is historical and does not establish new private-source
restoration. Scientific source/config hash remains unchanged. No P1 was run.

---

# Reproducibility report

**PASS FOR P0 TOOLING ONLY.** Tested GitHub source checkpoint:
`4d67240c827bdfeaae7831ecc3fd76a3eef36d5a` on `work`. No scientific workflow or new-cloud-task
publication is claimed. Full commands, outputs and exit statuses are in
P0_clean_clone_reproduction.json.

A fresh `git clone --branch work --single-branch
https://github.com/JINAOLONG/soc.git` was installed in a new temporary checkout.
It had no literature cache before setup. The repository's actual setup script
installed the package, restored all four primary PDFs from their public URLs and
verified their recorded SHA256. The 17 governance tests completed successfully.
P0 check-only audit returned its expected exit 2 / BLOCKED. The 68-file checkpoint
inventory verified with missing=0 and mismatch=0. `git status --porcelain` after
installation was empty. No simulator or scientific seed partition was executed.

P0 setup was also repeated in /workspace/soc. Seed generation verifies existing
metadata without rewriting it. Build-generated egg-info and bytecode are excluded
from source identity. Source/configuration digest at this checkpoint:
`d222e1dae96743c890bba98abb28acea5321c0a5a4d504e0e8d458476d6add0d`.

The raw original request is archived byte-for-byte, including CRLF line endings.
The initial plain Git whitespace check flagged those CRLF endings; the
CRLF-aware `git -c core.whitespace=cr-at-eol diff --check HEAD^ HEAD` passed.
The imported request was not rewritten to satisfy a formatting check. Initial
setup's one test failure is retained in P0_test_history.json, and later complete
17-test outputs are in P0_checks_001.json and P0_checks_002.json.

Temporary clone paths in the audit are execution provenance only. All setup,
review notes, source identities and fetch code are tracked in soc; none uses a
future /tmp dependency. Source-host changes/unavailability cause an explicit
hash/access failure rather than substitution. Source PDFs remain third-party
copyrighted works in ignored cache, reproducible by URL and SHA256.

Normal GitHub push of this checkpoint succeeded, and ls-remote independently
matched its SHA (P0_push_checkpoint.json). Evidence-closure commits only update
reports/STATUS/manifests; their final live SHA can be read with git rev-parse HEAD.
The current cloud configuration draft contains install_script, start_skill and
18 explicit source-domain additions while preserving package-manager presets.
Draft persistence is confirmed; publication and restore in a separate cloud task
are NOT VERIFIED. The user reviews/saves the settings and publishes through the UI.

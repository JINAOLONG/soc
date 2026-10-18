# Exact finite-matrix reconstruction — fresh report-only review

This is a new static review by the same Codex environment, not an external
third-party audit. No scheduler, workload generator, scientific runner, PRNG,
bootstrap, engine or calibration entry point was called. Reading registered
seed metadata does not inspect seed realizations or outcomes. All approvals
remain UNAPPROVED.

The actual matrix file was read in full from the repository, decoded strictly,
and parsed with duplicate-object-key and nonfinite-JSON rejection. Its byte
size, SHA-256 and every reviewed source are recorded in `matrix_source_reads.json`.
The primary comparison does not use an old checker, the old matrix as an
expected roster, declared counts, or manifest presence as proof.

## Sources and independent construction

| Fact or proposal | Exact source |
|---|---|
| Three scenarios, three loads, 8/16 nodes; B2 focal; 10 CALIBRATION seeds | `docs/workload_spec.md:3–25`; original `docs/user_request.txt` §§33–38, 80; these impose conditions, not a full trial matrix |
| B1–B5 baseline roles | `docs/baseline_spec.md:14–20` |
| Full v1 D05 proposal and explicit nesting order | `docs/P2_design/P2_complete_design_proposal_v1.md:162–194` |
| v2 preservation of axes, periods, methods, budget and order | `docs/P2_design/v2/P2_complete_design_proposal_v2.md:84–98` |
| Existing seed values and their list order | `configs/seed_partitions.json#/partitions/CALIBRATION` |
| All exact config and row values | `docs/P2_design/v2/P2_trial_matrix_draft_v2.json#/configs` and `#/trials`; rows begin at line 588 |
| All A/B and all ten seeds; B2-only control/own-load qualification | matrix `#/rules` (line 502), `#/selection_policy` (line 569); `P2_stage_state_contract_v2.json:146–149` |
| MAIN materialization before controls; controls' engine trials before MAIN | matrix line 557; `P2_generation_spec_v2.json:124`; `P2_runner_schema_review_v2.md:47–55` |
| All 2520 identities required for execution completion, separate from progression | `P2_stage_state_contract_v2.json:193` |

Expected configurations are built independently as the ordered Cartesian
product COCKPIT/ADAS/FUSION × light/medium/near-saturation × 8/16 × A/B. Periods
are 80/64, 24/20 and 12/10 ms respectively. These concrete values are unapproved
design choices, not values established by the original three-by-three-by-two
requirement or empirical hardware evidence.

For each configuration, iterate the ten existing CALIBRATION seeds in their
registered list order. For each seed, expected slots are H_ISOLATED B2,
LOW_COMPETITION B2, then MAIN B1, B2, B3, B4, B5. Each expected row independently
specifies all 20 fields, including trial ID, condition/config mapping, seed and
index, role, symbolic input reference, ordinal, budget count, null command/hash
and all three rule references. All 11 fields of each config are also compared.
Comparison rejects missing or extra keys and type differences, including
bool-versus-int. Every array position receives its own result and actual versus
expected audit digest; its JSON pointer and source line are recorded.

Secondary checks establish uniqueness of trial IDs and semantic tuples;
matching config/template references; exact seed-index pairing; complete methods
on the same MAIN input reference; only B2 on each control; identical count per
seed/config/condition and balanced A/B representation. Separate cross-version
checks corroborate that v1 values changed only at declared versioned references.
They do not substitute for the independent reconstruction.

## Arithmetic and interpretation

36 configs × 10 seeds × (5 MAIN methods + 2 B2 controls) = 2520 planned slots.
MAIN has 1800 slots and each control 360. Each config/seed has one shared MAIN
input and two derived control inputs, giving 36 × 10 × 3 = 1080 **symbolic**
input references. One primary plus one registered replay gives an upper bound
of 5040 future engine calls. Automatic retries are zero; replay is not a retry
or a second sample. Valid off-target/control-failure evidence is retained;
invalid, failed or incomplete execution stops the plan and leaves later slots
NOT_STARTED. This means these counts are a complete planned roster, never a
claim that all calls have occurred.

All A/B records are represented. The declared choice is the first eligible A
else B across all ten B2 seeds using controls and the config's own declared
load predicates. Candidate advantage, M1R gain/classification and M2 advantage
are excluded; there is no result-dependent fallback after the opportunity
analysis. SMALL/WIDE are unselected alternatives, not active trial subsets or
permission to expand the matrix. Timing runs remain zero in this roster and
the timing protocol remains unresolved.

The inherited `source_checkpoint` denotes v1 provenance, and `starting_commit`
denotes v2 authoring provenance. Neither field is a claim about the current
checkout. Similarly `wlref:v2:...` is a symbolic plan reference: it is not a
resolved content-addressed workload ID, and the future invocation guard must
reject it until the separate generation/resolution lifecycle is satisfied.

The numerical diagnostic limits 6^4=1296 assignments and 2×16+4=36 projected
nodes are combinatorial maxima per view, not a timing measurement or a bound
on the number of views. Static matrix agreement does not validate feasibility,
load bands, physical truth, runtime behavior, external validity or scientific
support. This report approves no decision or parameter group.

## Execution evidence

`matrix_commands.json` and its raw command files record the actual subprocess
calls and exits. `matrix_static_audit.py.txt` is the exact audit-only source.
`trial_matrix_row_audit.json` contains the actual latest check counts, all 36
config results and all 2520 row results. No critical matrix inconsistency was
found in this review; other review domains determine the package-wide verdict.

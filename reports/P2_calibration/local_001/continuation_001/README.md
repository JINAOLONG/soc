# Foreground CALIBRATION checkpoint through trial350

Last scientific segment ended at 2026-10-21T20:43:15.149138+08:00 (Asia/Shanghai). Both actual foreground CLI exit codes are0. No simulation or background finalizer remains running.

This continuation completed original trials247–350:104 primary calls and104 registered replays. Trial247 used exactly the separately accepted one-time recovery recomputation from its unchanged saved input; the old unknown reservation/manifest are unchanged. That recovery supplies one existing result slot and is not an additional independent sample. No original completed246 result was rerun or overwritten.

Cumulative:350 validated primary results and350 exact registered replays, five complete configurations with all10 CALIBRATION seeds,150 generated inputs (42 added this turn).2170 original trials and930 registered inputs remain. Primary invocation count is bounded350..351 and total engine count700..701 because the original interrupted call remains unknown. The separately accepted lifetime engine cap is5041; the one extra-primary recovery allowance is consumed. All other retries remain prohibited.

The49 original scientific execution files still match original commit b248effe1ff925bc43f3eef280dcaaffbe19a557 and frozen source digest dc9e7c35bb6033fc558b10409ba3bcf3b6927b7b752e2554b972234000b21f07. The new orchestration source digest is350eaf8e1435d6f97c2f4ba60f776b44915726b79b4ad3e3beadc4b75fe4f14d. New run/segment contexts bind the actual committed code, exact interpreter argv, host, PID, raw input/config hashes, permission and real return timestamps.

All125 correctness tests passed before admission; P0/P1 audits exited0. Post-run closure independently rechecked every new primary/replay physical trace and metric result, exact byte hashes, newly generated inputs and inherited controls. Within each config/seed, all five MAIN methods use the identical workload-content hash and H/L service counts50/50. No seed, scientific threshold, statistics, simulator or scheduler implementation was changed. No non-CALIBRATION outcome, bootstrap/CI, candidate, validation or formal execution occurred.

## First medium-load configuration: actual descriptive results

COCKPIT-medium-8-A,10 seeds per method. H/L DMR columns are seed means. P95 columns are means of ten per-seed service-response P95 values in virtual milliseconds; they are not pooled P95s, decision latency, confidence intervals or hardware measurements.

|Method|H DMR|L DMR|H P95 ms|L P95 ms|
|---|---:|---:|---:|---:|
|B1|6.0%|58.6%|30.561|54.218|
|B2|0.0%|73.0%|23.514|54.296|
|B3|75.6%|20.2%|54.805|56.592|
|B4|74.4%|20.0%|55.329|55.968|
|B5|6.8%|35.2%|31.118|61.101|

B2 pressure seed mean=0.571557844; H-DMR mean=0.000000, L-DMR mean=0.730000. Its zero H-DMR is below the registered medium-load H-DMR minimum1/100. This is a single-predicate descriptive check, not official global config selection or mechanism evidence. No parameter/deadline/threshold was changed. The next registered configuration is B, not a new tuned condition.

The full2520-result roster is still incomplete, so global qualification, M1R mapping diagnostics, M2 analyses and mapping classification remain NOT_EVALUATED. P2 is not PASS; there is no candidate-benefit, independent-confirmatory or formal conclusion from this partial calibration table.

## Reconstructing retained evidence

The interrupted-campaign base archives and metadata index remain in ../interruption_001. Delta archives listed in delta_archive_index.json preserve all1072 new raw files. Every delta member was read back and SHA256-compared. All2543 original raw files remain unchanged; the cumulative_raw_manifest.json inventories all3615 current raw files. No local raw file was removed. Extract base archives and then delta archives at repository root to restore their original relative paths.

command.json and process_002/command.json retain actual process commands/times/exits; closure_command.json retains the actual read-only verification exit. Scientific contexts/results live in results/calibration/local_001/segments/segment_001 and segment_002 after extraction. The old root progress.json says RUNNING because it is deliberately retained interruption evidence; it is not the live state. Current checkpoint is segment_002/summary.json.

Next safe action: continue original trials351–420 (COCKPIT-medium-8-B) using the same committed bounded foreground CLI and call ledger. This is already within the granted CALIBRATION continuation scope. Do not rerun completed slots, create a second campaign, consume another recovery exception, retune or progress to P3.

`.venv/bin/python -B scripts/resume_local_calibration.py --end-trial 420 --seconds 600`

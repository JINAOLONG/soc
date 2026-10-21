# Foreground CALIBRATION checkpoint through trial420

Original trials351–420 (COCKPIT-medium-8-B) completed at 2026-10-21T21:05:52.531362+08:00 (Asia/Shanghai). The actual foreground exit code is0; total process wall time was 390.970 seconds including preflight. The separately recorded post-run closure exit code is0. No scientific process remains running.

## Actual execution and identity

This continuation added70 primary calls,70 registered replays and30 registered inputs. All70 new primary/replay pairs passed independent physical and metric validation and exact content-hash comparison. Ten new MAIN inputs and20 inherited controls passed independent input checks. No completed trial was rerun. No additional recovery recomputation occurred.

Cumulative:420 valid primary results and420 exact registered replays,180 inputs, six complete configurations of70 trials each, all ten registered CALIBRATION seeds. The fixed roster remains2520 unique result slots;2100 trials and900 registered inputs remain. The completed fraction is1/6. Registered replays are verification calls, not extra independent samples. Each MAIN method uses the identical workload-content hash within its config/seed, with50 H and50 L services.

The original trial247 invocation remains UNKNOWN. Its separately accepted one-time recovery was consumed previously, supplies the existing result slot and adds no independent sample. Cumulative actual primary calls are bounded420..421, total engine calls840..841; the accepted lifetime engine ceiling remains5041. No additional unknown-call retry is permitted.

Execution began from committed HEAD cb9fab5a53e081eea7f9742da365022903f38261. The49 original scientific execution files still match commit b248effe1ff925bc43f3eef280dcaaffbe19a557, frozen digest dc9e7c35bb6033fc558b10409ba3bcf3b6927b7b752e2554b972234000b21f07. Current orchestration digest remains350eaf8e1435d6f97c2f4ba60f776b44915726b79b4ad3e3beadc4b75fe4f14d. The two orchestration additions were committed at0d0c1f73f4449f69c6955be0ebfed74098a22623. Actual commands, host, PID, source/config/workload hashes and start/return times are retained in command.json, segment_003/context.json and individual run manifests.

The execution preflight reran existing P0/P1 audits: both PASS. Existing current-source correctness evidence is125 passed,0 failed,0 skipped; the full test suite was not rerun in this results-only continuation. Source identity and the new scientific artifacts were checked instead. No simulator, scheduler, seed partition, scientific threshold or statistical method changed. No non-CALIBRATION outcome, bootstrap/CI, candidate execution, validation or formal work occurred.

## Actual descriptive result: COCKPIT-medium-8-B

Ten seeds per method. DMR is the mean of per-seed service deadline-miss fractions. P95 columns are means of ten per-seed response P95s in virtual milliseconds; they are not pooled P95s, measured hardware latency or confidence intervals.

|Method|H DMR|L DMR|H P95 ms|L P95 ms|
|---|---:|---:|---:|---:|
|B1|6.2%|77.0%|30.004|58.284|
|B2|0.2%|86.6%|26.628|58.284|
|B3|83.6%|25.8%|58.298|56.726|
|B4|82.8%|25.0%|56.206|56.112|
|B5|17.8%|41.0%|35.276|59.904|

B2 mean pressure=0.6908207406124626, inside the registered medium band[1/2,4/5). Its exact mean H DMR=1/500 (0.2%), below the registered minimum1/100 (1%). Mean L DMR=433/500 (86.6%). Positive assigned busy wait holds for10/10 seeds. H_ISOLATED and LOW_COMPETITION constructive witnesses each pass10/10.

The prior A configuration's B2 mean H DMR was0; thus both fixed A/B configurations for COCKPIT-medium-8 fail this registered H-DMR predicate. This is a real calibration qualification gap; executing other configurations cannot make these saved values satisfy the predicate. No threshold, deadline, seed or configuration was adjusted. These are descriptive registered-predicate checks, not an executed global selection, M1R/M2 analysis, significance claim or proof that the scientific mechanism is absent. Global qualification/selection and mapping classification remain NOT_EVALUATED because the2520-result roster is incomplete. P2 remains BLOCKED.

## Preserved results and reconstruction

All3615 previously inventoried raw files are byte-for-byte unchanged. The724 new files are preserved in two archives listed in delta_archive_index.json (720 config files,4 segment metadata files); every archive member was read back and SHA256-compared. The cumulative inventory now has4339 files. No raw working file was removed.

Restore at repository root, in order: the interruption_001 base per-config archives plus metadata archive; continuation_001 delta archives; then this continuation_002 delta archives. The cumulative manifest links the required indexes. Hash-check all archives against those indexes before extraction and check restored files against cumulative_raw_manifest.json. The raw input references preserve the original /workspace/soc execution location.

command.json and stdout/stderr.log record the actual scientific process; closure_command.json and closure_stdout/stderr.log record post-run verification. new_trial_checks.json has70 verified pairs; new_input_checks.json has10 parent groups. all_completed_results.json and baseline_summary.csv/json contain420 cumulative results and six complete configurations. medium_B_descriptive_checks.json records the exact predicate observations above. process_exit_observation.json confirms no matching active scientific process.

The historical root progress.json is deliberately unchanged and still says RUNNING; it is interruption history. The current checkpoint is results/calibration/local_001/segments/segment_003/summary.json. This checkpoint is PAUSED_AT_COMPLETE_TRIAL_BOUNDARY, not campaign completion.

Next registered slice, if continuing the authorized fixed roster: trials421–490, COCKPIT-medium-16-A. Retain the medium-8 qualification failure. Do not rerun completed slots, retry unknown calls, retune, create a second campaign or automatically progress to P3.

`.venv/bin/python -B scripts/resume_local_calibration.py --end-trial 490 --seconds 600`

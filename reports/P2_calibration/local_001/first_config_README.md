# First complete configuration — live CALIBRATION checkpoint

The full fixed 2520-primary-trial campaign is RUNNING; this is a saved partial
result, not P2 PASS or a mapping-opportunity conclusion. The first config is
COCKPIT-light-8-A: all10 registered CALIBRATION seeds,20 control trials and50
MAIN baseline trials,70 exact registered replays. All70 primary/replay physical
checks and metric recomputations passed. No retries or extra scientific calls.

first_config_summary.csv contains actual seed means for every B1-B5 method.
The P95 columns are means of ten per-seed service-response P95s in milliseconds,
not pooled percentiles, decision latency, confidence intervals or hardware
measurements. H/L deadline miss rates are zero for these light-load samples;
this does not establish loaded-condition behavior or algorithm superiority.

first_config_raw.tar.gz retains the complete inputs/exact sidecars and all70
trial manifests/reservations/primary and replay traces/independent validations.
All archived file contents were read back and SHA256-compared to actual local
files. Extract at repository root with:

tar -xzf reports/P2_calibration/local_001/first_config_raw.tar.gz

first_config_results.json and first_config_snapshot.json bind exact identities
and raw references. context.json and preflight.json retain actual code, host,
command, authorization scope and successful prerequisite checks.

The active process writes results/calibration/local_001/progress.json and
reports/P2_calibration/local_001/stdout.txt. Do not launch a second campaign or
retry a reserved/uncertain invocation. Finalize_snapshot.py is a non-scientific
report watcher; after the actual command ends, it validates/archives completed
results, records the real exit and attempts normal GitHub publication. Its
future success has not yet been claimed. Validation/formal remain locked.

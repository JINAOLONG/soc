# Statistical protocol — P0 draft

Seeds are the independent resampling units. Every method within a condition/seed
uses the exact same materialized workload, not merely the same arrival seed.
Pair methods and workloads. Use 10,000 bootstrap replicates, analysis PRNG seed
20261018, percentile 95% intervals using the type-7 0.025 and 0.975 quantiles.
When implemented, pin the PRNG implementation/version and save resampling indices
or their reproducible digest. No statistical result is currently available.

To preserve seed effects across conditions, sample the seed indices once per
replicate and use the same vector in all compared methods and conditions. Within
each replicate compute condition seed means followed by equal-weight condition
macro means, then the registered contrasts. For L resample paired Q values and
recompute each ratio of means. Do not average individual ratios or treat nodes
as independent replicates. Report descriptive per-condition contrasts as well
as primary macro estimates. No unregistered p-value filtering.

User constraints: H relative gain >=10% with positive Delta_B2 CI; L upper CI
<=1.10 in every main condition; positive mapping contribution CI; B5 comparison
classification; correctness and decision P95 <=2 ms. Proposed all-gates progression
requires all these criteria and no confirmed B5 superiority. A boundary-crossing
CI is INCONCLUSIVE, not PASS. Macro gain cannot compensate for L condition failure.
The intersection of all L conditions is required; individual CIs are pointwise,
not simultaneous-coverage claims. Report this limitation explicitly.

Development seeds [0:10] are parameter-search data. Seeds [10:20] are development
precheck only and cannot be used for choosing a search trial. No expansion of a
registered search space after observing results. A permitted one-time mechanism
revision must be preregistered first, preserve thresholds/partitions, and be
reported as further development rather than independent validation. If revision
addresses L/engineering after a previous H gain, enforce the user's strict
non-degradation test: M_revision-M_previous point <=0 and CI upper <=0 (delta=0).

P2 workload tuning uses baselines, especially B2, and CALIBRATION only, never
candidate advantage. P2 must publish a stable mapping-opportunity criterion before
diagnostic selection is used to pass the stage. No candidate formula at P0.

Independent validation has 180 workloads (18×10); formal has 540 (18×30).
No tuning, new baselines, threshold/statistic changes, unfavorable-seed removal
or selective conditions. Every run needs independent trace validity. Invalid runs
are preserved and diagnosed; any rerun receives a new ID and a supersession link.
Missing/invalid pairings block a complete stage; do not silently drop them.

All scientific stages require SHA256 manifests plus missing=0, mismatch=0,
duplicate identity=0, unexpected seed/method=0 and missing expected condition=0.
This project has zero scientific runs; those scientific completeness checks are
NOT APPLICABLE yet, not a passing experiment.

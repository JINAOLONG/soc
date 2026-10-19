# soc research rules

Read this file and STATUS.md at the beginning of every task. The complete user
contract is preserved in docs/user_request.txt. It takes precedence over summaries.

1. The only project repository is JINAOLONG/soc; its root is the project root.
   Use the existing isolated checkout; do not create nested repositories or
   worktrees unless explicitly requested. Check the remote before every push.
2. Research question: online, non-preemptive, multi-service DAG scheduling on
   four CPU cores, one GPU unit and one NPU unit. Joint ordering and mapping
   should reduce important-service H deadline misses while keeping every main
   condition's ordinary-service L P95 ratio to B2 at or below 1.10. H/L are
   service importance labels, not ASIL or safety certification.
3. Keep engine, scheduler, workload generator, metrics, independent validator,
   and analysis separate. A scheduler receives immutable observations of arrived
   services only; never reveal future arrivals, true future durations, random
   disturbances, or the private event queue. Planned is not started.
4. Preserve LICENSE and user work. No destructive Git operations, history
   rewriting, broad restore/clean/reset, or force push. Commit relevant tested
   changes at stage boundaries. Attempt a normal push on the actual task branch
   and record the precise result; a local commit is not a GitHub backup.
5. All scientific numbers and claims must come from actual clean-room runs.
   Do not reuse legacy results, candidate parameters or profiling conclusions.
   Use UNKNOWN, UNVERIFIED, NOT RUN or NOT APPLICABLE where appropriate.
6. Seeds in configs/seed_partitions.json use the user-prescribed deterministic
   derivation and cannot be redrawn. P0–P2 allow only CALIBRATION execution;
   P3 uses DEVELOPMENT, first 10 for search, last 10 for precheck. Metadata
   generation/auditing is not workload execution. Do not inspect reserved
   workload realizations or outcomes before unlock.
7. Independent validation requires Development Gate PASS, committed freeze
   manifest and checkpoints/VALIDATION_UNLOCKED. Formal requires the corresponding
   validation gate, committed freeze and checkpoints/FORMAL_UNLOCKED. Never
   create tokens to bypass missing evidence. An unknown stage fails closed.
8. Never change user thresholds, remove losing seeds/configurations, discard
   slow timing runs, select favorable conditions, or relabel development as
   independent evidence. Retain all valid failures and invalid-run diagnoses.
   No candidate formula before P2. At most one preregistered mechanism revision.
9. P0 cannot pass without reviewing 6–8 original studies, including HEFT/CPOP,
   PEFT and DS3. Retrieval of code or a title alone is not paper verification.
   B3/B4/B5 are explicitly online adaptations, not the original static methods.
10. Stop scientific progression on any unmet stage prerequisite. Correctness
    failure must be fixed before science; absent stable P2 mapping opportunity
    stops that hypothesis; failed validation blocks formal; provenance uncertainty
    blocks execution. Preserve reports and commits even when blocked.
11. Every scientific run needs run ID, timestamp, Git commit and dirty status,
    source/config/workload SHA256, partition/seed/scene/load/size/method, host,
    exact command, result path and independently determined validity. Resume
    only after matching all identities. Precheck/validation/formal require
    committed, clean relevant source/configuration.
12. Keep profiling separate from scientific sample counts. Any purported
    semantics-preserving optimization needs profiler evidence and exact old/new
    decision, physical trace and event regression with zero mismatches. A mismatch
    stops that optimization; it cannot retroactively rescue frozen results.
13. Update STATUS.md after meaningful changes. Record executed and unexecuted
    stages separately. CURRENT_GIT_HEAD is resolved at read time if a static
    file cannot contain its own enclosing commit hash; record tested source
    commits explicitly in manifests. Never invent a hash.
14. Run applicable tests and audits before committing. CI is lightweight only:
    never launch calibration, development, validation, formal or large benchmarks.
15. Track code, protocols, configs, scripts, reports, small summaries/manifests.
    Keep large raw data compressed with identity, hash and regeneration commands;
    do not introduce LFS infrastructure without need/authorization. No secrets
    in files, outputs, commits or setup instructions.

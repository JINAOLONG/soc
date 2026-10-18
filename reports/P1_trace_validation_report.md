# Independent P1 Trace validation

`src/soc/validation/trace.py` imports immutable offline model records only. It does
not import the engine, scheduler kernels, runtime communication helper or metric
implementation. It independently checks all executions against actual resource
durations, arrivals, DAG predecessors and destination communication. It rejects
overlap, incompatible or unknown units, missing/duplicate execution, split
execution and assignment/event disagreement. Arrival/start/complete event
multisets must match the full admitted input exactly, in chronological D1 phases.

For valid traces it independently recomputes service completion, response,
deadline equality, group DMR/quantiles, full-drain makespan, busy/utilization,
per-edge transfer start/ready, total cross-unit data and waiting components.
It compares the entire metric object against runtime output; no tolerance hides
a physical mismatch. Display-rounding tolerance is used only for the paper's
three-decimal published rank table, not for event replay or trace legality.

Actual retained evidence: 45 valid traces (9 manual inputs × B1–B5), each checked
again by the formal gate and regenerated for exact replay. `P1_artifacts/index.json`
links each input, method, trace/hash, validator result and metric comparison.
`P1_artifacts/negative_results.json` records 20 explicit malformed traces, expected
rejection code, actual error codes and result; all were rejected with their
specified error. Additional unit negatives cover pre-arrival start and reversed
same-time completion/arrival order. None are scientific workload samples.

The 8-node H DAG plus one L service has fixed expected intervals:
a 0–2; b 3–6; c 2–4; d 7–9; e 5–6; f 10–11; g 9–10; h 12–13;
L node 0–13. Every baseline matches these hand calculations. H's deadline=13
counts on time; L's deadline=12 is a retained miss. Cross-unit data sum=8 MiB.
Other inputs isolate ranking, OEFT, busy overrun, remapping, waiting/scanning,
simultaneous events, empty-system and single-node behavior.

The source-level independence test patches engine/runtime metric/communication/
scheduler functions to raise errors and still validates an already obtained trace.
This is an implementation independence check, not a claim of mathematical proof,
hardware validation or exhaustive coverage of every possible DAG.

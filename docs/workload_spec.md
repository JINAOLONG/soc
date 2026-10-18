# Workloads — design constraints, not a frozen generator

No workload generator or scientific workload has been executed. Main conditions
are 3 scenes × 3 loads × 2 sizes. Size means exactly 8 or 16 executable nodes per
service instance, excluding neither sources nor sinks. No hidden dummy task may
change these counts.

COCKPIT templates must cover speech, display, navigation and interaction;
ADAS covers preprocessing, perception, fusion and output. FUSION mixes the two
families under shared accelerators to expose cross-service competition. Concrete
durations, compatible sets, edge sizes, arrival laws and deadlines await source
review and a baseline-only calibration protocol. They are NOT AVAILABLE yet.

Calibrate with 10 CALIBRATION seeds, B2 as the focal reference. Label loads by
measured CPU/GPU/NPU bottleneck pressure, not arrival rate alone. Light should
have low misses; medium/near-saturation should expose contention, nontrivial
misses and mapping alternatives without nearly universal miss. Severe-overload
is sensitivity only. Verify H feasibility in isolation or low competition first.
Save every tried calibration configuration and its diagnosis; do not select
workloads by candidate advantage. Freeze generator/config after P2.

Identity = scene, load, size, seed, generator version, config SHA256 and the
canonical artifact SHA256. Every method consumes the same stored realization.
Execution disturbances use keyed hashes/PRNG independent of scheduler calls.
Do not materialize validation/formal realizations during calibration or unit tests.

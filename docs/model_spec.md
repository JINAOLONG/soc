# System model — P0 draft

Virtual time uses milliseconds, data sizes MiB, bandwidth MiB/ms and power W.
Service g has arrival a_g >= 0, relative deadline D_g > 0, absolute deadline
d_g = a_g + D_g, importance H or L and a finite acyclic task graph. Completion
F_g is the last node completion. Nodes inherit service importance. Instance,
node and resource IDs are unique stable strings. Reject cycles, empty compatible
sets, nonfinite/negative timing inputs and missing predecessor identities.

Resources are CPU0, CPU1, CPU2, CPU3, GPU0, NPU0. Each unit executes at most one
node. GPU/NPU internal parallelism is abstracted by execution time. Compatible
sets must include CPU-only, GPU-oriented, NPU-oriented, multi-compatible and
limited-alternative types; universal compatibility is not an acceptable workload.
Every resource-specific node has positive estimated and realized durations.

Execution is non-preemptive: a started node keeps its resource and contiguous
execution interval until completion. No migration, replication or replanning of
that interval is allowed. Pending nodes may be reordered/remapped.

Communication version 1 has no shared-bus contention. For edge u→v with size b,
transfer to destination r can start at u's completion C_u. Same unit: delay 0.
Different units: latency(type(u),type(r)) + b / bandwidth(type(u),type(r)); all
parameters nonnegative with strictly positive bandwidth. Independent transfers
overlap with each other and with compute. Data readiness on r is
max over predecessors of C_u + delay(u,r); a root is ready at service arrival.
These logical copies are destination-specific and retained after transfer.
Remapping a pending node recomputes readiness for the new destination; it cannot
reuse a copy at another unit or backdate transfer before predecessor completion.
The implementation may calculate copy readiness lazily from immutable completed
outputs; this is not a reservation or a started execution. No future predecessor
completion is treated as an actual completed output.

States are distinct: dependency_ready (all predecessors completed), data_ready
(copies arrived on a specified destination), planned (nonbinding proposal),
resource_ready (destination idle), started, running, completed. A proposal may
wait or be replaced. Actual start >= arrival, all predecessor completions,
destination-specific data readiness and resource availability.

Proposed deterministic event ordering, to be tested in P1: at virtual time t,
process all completions, expose all arrivals at t, then refresh the immutable
scheduler view and dispatch only feasible starts; repeat zero-time dispatch
until no start is chosen. Ties use stable (service_id,node_id,resource_id).
No positive-length execution interval overlaps another on the same unit; touching
endpoints are legal. When no start is possible, advance to the next true event
or feasible data-readiness wakeup. Detect a deadlock rather than silently dropping
jobs. After stopping arrivals, drain all admitted work, even after deadline miss.

Scheduler boundary: only arrived public DAGs, estimates, deadlines, H/L, completed
outputs, running task start/elapsed observations, idle/busy state and observable
data readiness. Never disclose the private event queue, future arrivals, true
remaining running durations or future disturbances. Busy-unit release prediction
must use estimates and elapsed time, never actual queued completion timestamps.

Execution disturbances must be scheduler-independent deterministic functions of
(workload seed, service ID, node ID, resource ID, disturbance version). The
generator materializes the same workload artifact for every compared method.
No RNG call sequence may depend on scheduler decisions. Exact event, trace and
metric reproducibility is required for identical code/config/workload identities.

P1 must independently validate legal traces and reject crafted violations of
precedence, data readiness, compatibility, overlaps, duration, unique execution,
non-preemption, assignment, completion and full arrival accounting. It must include
a 6–8-node hand-checkable DAG, simultaneous events, equality at deadline and drain.
No engine or validator is claimed implemented in this P0 draft.

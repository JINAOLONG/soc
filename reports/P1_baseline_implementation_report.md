# P1 baseline implementation and source boundaries

The user's P1 clarification explicitly approved D1–D5. Approval wording and
scope are retained in docs/P1_decisions.json. The versioned implementation spec
states the exact compatible-cost and communication averages, observable busy
prediction and revocable waiting/scanning policy. No arbitrary incompatible
execution costs, actual future finishes or unseen arrivals enter the algorithms.

| Baseline | Ready priority | Resource score | Evidence |
|---|---|---|---|
| B1 | Absolute service deadline, stable IDs | insertion EFT over compatible units | L-root before H-root in priority fixture |
| B2 | H before L, then absolute deadline, IDs | same EFT | H-root before L-root on identical input |
| B3 | descending compatible mean-cost upward rank, IDs | same EFT | source table ten ranks + manual source recurrence |
| B4 | descending compatible-row mean OCT, IDs | insertion EFT+OCT | original table thirty cells; OEFT selects GPU where EFT selects CPU |
| B5 | H before L, then same OCT rank, IDs | same OEFT as B4 | H-priority fixture + all shared input/trace checks |

Ready means arrived, unstarted and all predecessors completed. The lowest score
mapping may still wait for estimated busy/data readiness; dispatch verifies
actual idle/data feasibility, scans remaining tasks when one waits, and refreshes
after every start. A waiting proposal reserves nothing. Overrun predictions use
only estimate and elapsed time; actual completion is visible only when it occurs.
Resource ties use stable resource IDs. Equal task priorities use service/node IDs.

Tables are rebuilt from the public arrived DAGs and fixed estimates at each
decision. OCT never receives availability. PEFT uses child execution costs,
max-child/min-child-unit recurrence, zero exit row, and mean OCT rank; it does
not add the current task's execution to OCT. Insertion finds a complete free
gap; online occupied predictions contain only currently running intervals,
because future proposals are not reservations under the approved adaptation.

Original regressions were transcribed by reading the actual supplied copies:
HEFT PDF6/printed265 Fig3 and PDF7/266 Table1 (all 10 ranks), PEFT PDF2/683 Fig1
and PDF6/687 Table2 (all 30 OCT cells). Numeric inputs/checks live in
tests/p1_source_examples.py and test_p1_kernels.py; no PDF or page image is tracked.
The source's random ties and static full-matrix model differ from this approved
online deterministic compatible-resource extension. These tests do not claim
to reproduce published makespan/performance experiments or complexity bounds.
CPOP remains reviewed literature, not a sixth formal baseline.

All five baselines run all 9 identical manual input artifacts. Result hashes,
independent checks and replay identities are in P1_artifacts/index.json. A passing
baseline here means correctness on this defined test suite, not superiority,
deadline feasibility for all workloads or support for the research hypothesis.

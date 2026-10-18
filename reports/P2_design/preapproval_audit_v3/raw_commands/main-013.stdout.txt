# Metrics — user thresholds retained; P0 draft

Statistical observation is a service instance, not a node. Response T_g = F_g-a_g.
A miss is F_g > a_g+D_g; equality is on time. H-DMR and L-DMR are the miss count
divided by the number of arrived instances in the respective group, including
all drained work. An absent group is invalid/undefined, never zero by default.

Within each run, calculate L P50/P95/P99/max over all L service responses,
including missed services. Use linear-interpolated quantiles (Hyndman–Fan type 7):
sorted x[0:n], h=(n-1)p, interpolate floor(h) and ceil(h); n=1 returns x[0].
Do not pool L responses across seeds to replace the prescribed ratio of means.

There are 18 main conditions: {COCKPIT,ADAS,FUSION} ×
{light,medium,near-saturation} × {8,16} nodes per service DAG.
For H primary benefit, first average each method's H-DMR across seeds within
each condition, then take the equal-weight condition macro mean over the 12
medium/near-saturation conditions. Let these means be M_B2 and M_F.
G=(M_B2-M_F)/M_B2 must be >=0.10 and paired seed-bootstrap CI for
Delta_B2=M_B2-M_F must have lower endpoint strictly >0. M_B2=0 makes relative
benefit undefined and cannot pass. Do not substitute task- or service-weighting.

For L, Q_m(c,s)=within-run L P95. For each of all 18 main conditions,
R_c=mean_s Q_F(c,s)/mean_s Q_B2(c,s). Point >1.10 is FAIL;
point <=1.10 and paired-bootstrap upper endpoint <=1.10 is SUPPORTED;
otherwise it is INCONCLUSIVE. A zero/nonfinite denominator or missing run is
invalid; do not clip or add arbitrary epsilons to manufacture a ratio.

Mapping contribution is Delta_A1=M_A1-M_A3 on the same 12-condition H macro;
point >0 and CI lower >0 are required to claim support. A3 is full urgency and
mapping; A1 uses new urgency with EFT; A2 uses B2 ordering with new mapping.
No positive mapping claim from A3 vs B2 alone.

Strong-baseline contrast is Delta_B5=M_B5-M_F with paired seed CI:
lower >0 => SUPPORTED_SUPERIOR; upper <0 => B5_SUPERIOR;
otherwise NO_CONFIRMED_DIFFERENCE. Equality is not superiority. Report every
condition as well as the macro estimate. The proposed progression rule blocks
confirmed B5 superiority; absence of confirmed difference is explicitly not a
claim of equivalence/noninferiority. This rule is a disclosed P0 design choice,
not a user-supplied B5 effect-size target, and remains draft until P0 passes.

Secondary outputs: group DMR, L P50/P95/P99/max, group/overall mean response,
per-resource busy time divided by full-drain makespan, transfer totals and
waiting breakdowns. No undocumented warm-up exclusion in scientific metrics.
If energy is later implemented: sum active_power*busy_duration plus
idle_power*idle_duration with explicit ms→s conversion and declared power inputs;
label model-estimated energy, never a hardware measurement.

Engineering decision latency is host wall computation covering preprocessing,
path updates, urgency, candidate generation/sorting, scoring, mapping and selection;
virtual execution/communication time is separate. P95 <=2 ms is a host target,
not automotive hardware evidence. Exact warmup/repetitions/inputs must be frozen
at P2 before candidate timing; no timing has been measured in this project.

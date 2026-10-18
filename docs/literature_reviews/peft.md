# PEFT — verified local original and page-level review

Status: VERIFIED_PRIMARY. All 13 PDF pages (printed 682–694) were read.
All pages rendered successfully and their contact sheet was checked; enlarged
PDF page 6 was inspected for Eq.(7)–(9), Table 2 and Algorithm 1. This is original
source review, not an implementation or a scientific experiment. Earlier failed
acquisition/checklist records remain in history/p0_before_local_pdf_review_1b36f39/.

## Identity, version and actual input

Hamid Arabnejad and Jorge G. Barbosa, “List Scheduling Algorithm for Heterogeneous
Systems by an Optimistic Cost Table,” IEEE Transactions on Parallel and
Distributed Systems 25(3), 682–694, March 2014; DOI 10.1109/TPDS.2013.57.
PDF page 1 shows the title, authors, journal header, issue and printed DOI.
It states online publication on 27 February 2013; the issue year remains 2014.

- Actual input: /workspace/attachments/a587bb22-0000-435f-af70-ab3c8f3325eb/List_Scheduling_Algorithm_for_Heterogeneous_Systems_by_an_Optimistic_Cost_Table.pdf
- Ignored copy: .cache/literature/PEFT_Arabnejad_Barbosa_2014.pdf
- Actual attachment locator: sediment://file_000000004a808211b0e2e492db0ac541
- File size: 1492291 bytes; PDF pages: 13.
- SHA256: 51c5036310ea4f4deb9f2e6c65730fc1b2321dd1e2975bc3940285b03ede5fc8
- Provenance: USER_PROVIDED_LOCAL_COPY_SOURCE_UNVERIFIED. No original download
  URL was supplied. The real attachment locator is not a claimed publisher URL.
- Version: publisher-formatted journal copy with continuous journal pagination,
  copyright and licensed IEEE Xplore footer. Metadata reports iText modification
  in 2018. Unchanged publisher-binary authentication/chain of custody remain
  UNVERIFIED. Redistribution permission is not established; the PDF is not tracked.

Actual file/opening/hash information is in P0_source_acquisition_014.json.
Viewer PDF page = printed page minus 681. The original definitions, normalized
below, are distinguished from any future online adaptation.

## Original model, formulas and page evidence

| Item | Original evidence | Verification and relationship to soc |
|---|---|---|
| Static single-job model | pp.683–684, PDF 2–3, §2 | All DAG/system parameters known before scheduling; processors available to that single job and not shared during execution. Non-preemptive tasks, fully connected network, overlapping compute/communication without contention. No online H/L budget. |
| Transfer model | p.683, PDF 2, Eq.(2); p.684, PDF 3 | cbar_i,j = Lbar + data_i,j/Bbar; same-processor actual cost zero. Target discussion treats latency differences as negligible and bandwidth as uniform. Not a detailed shared-bus model. |
| EST/EFT foundation | p.684, PDF 3, Eqs.(5),(6) | EST accounts for processor availability and predecessor data arrivals; EFT=EST+w_i,j. These are partial-schedule constraints, not the OCT optimism. |
| OCT recurrence/base | p.687, PDF 6, §4.1, Eq.(7) | Maximum over immediate successors of minimum successor processor suffix cost, including child execution and transfer. Traversal exit-to-entry; OCT(exit,processor)=0. Formula below. |
| OCT rank | p.687, PDF 6, §4.2, Eq.(8) | Mean OCT across processors. Algorithm 1 lines 2–4 selects highest rank_oct from ready-list. Do not add the current mean execution cost or silently replace it with rank_u. |
| Processor choice | p.687, PDF 6, §4.3, Eq.(9), Algorithm 1 lines 5–10 | Compute insertion EFT on each processor, then choose minimum EFT+OCT (OEFT); update ready-list. |
| Look-ahead | pp.686–688, PDF 5–7, §4 | Descendant suffix costs are precomputed; evaluating immediate children can use their already computed OCT. OEFT may sacrifice current EFT to improve expected later completion. |
| Availability in OCT | p.687, PDF 6, §4.1; pp.692–693, PDF 11–12, conclusion | Explicitly excluded from OCT; the source calls the table optimistic for that reason. Availability enters EFT, not OCT. |
| Complexity | p.688, PDF 7, §4.4 | Authors state OCT O(p(e+v)), assignment O(v²p), total O(p(e+v)+v²p), dense-DAG O(v²p). Source bounds are not measured latency or an independent proof for unimplemented soc code. |
| Limits and negative cases | p.691, PDF 10, Table 4; pp.692–693, PDF 11–12, §5.3.2/§6 | Reported results include worse cases and FFT/all-critical-path cases without advantage; no universal dominance is established. These are the paper's results only. |

Let t_i/n_i denote a task, p_k a processor, p the processor count, v the task
count and e the edge count. The following writes the source's processor-dependent
zero-transfer condition explicitly as cbar_i,j(k,w); it does not alter Eq.(7):

    OCT(t_i,p_k) = max over t_j in succ(t_i)
                    min over p_w in P
                      [OCT(t_j,p_w) + w(t_j,p_w) + cbar_i,j(k,w)]      (7)
    cbar_i,j(k,w) = 0 if p_w = p_k;
                   otherwise the source's average edge cost
    OCT(t_exit,p_k) = 0 for all p_k
    rank_oct(t_i) = sum over p_k in P of OCT(t_i,p_k) / p               (8)
    OEFT(t_i,p_j) = EFT(t_i,p_j) + OCT(t_i,p_j)                         (9)

OCT excludes the current task's own execution; it includes child execution and
child OCT. It is neither a sum of all branches nor a resource-independent scalar
rank. The all-zero exit row of Table 2 (p.687/PDF 6) agrees with the base case.
Algorithm 1 line 6 expressly uses insertion-based EFT. Line 9 minimizes OEFT,
not immediate EFT. Table 3 and Fig.2 (p.688/PDF 7) illustrate that distinction.

Section 3.1 (p.684/PDF 3) states random ties for generic list-task priorities.
An explicit PEFT processor-tie rule is NOT_EXPLICITLY_SPECIFIED_IN_SOURCE in
Algorithm 1/§4. A detailed implementation accounting for the quoted OCT-building
bound is also NOT_EXPLICITLY_SPECIFIED_IN_SOURCE in its high-level “Compute OCT”
step. Those omissions are recorded without filling them from model knowledge.
The source assumes the complete execution matrix; compatibility-mask handling
is not specified as part of this algorithm.

## Difference from original HEFT and project scope

The independently reviewed 2002 original HEFT uses mean-cost upward rank and
minimum insertion EFT. Original PEFT uses a task×processor optimistic suffix
table, its across-processor mean for rank and minimum EFT+OCT for placement.
rank_u(exit) is mean exit execution; OCT(exit,processor) is zero. PEFT §4.2
discusses rank_u as an alternative but retains rank_oct in the proposed method;
that discussion is not permission to substitute another OCT/rank variant.

PDF 1–3 cover identity/model; 4–5 related/comparator algorithms and motivation;
6–7 original PEFT and its example; 8–11 experimental design/results; 12–13
conclusions/references/biographies. All were read. The negative FFT cases and
pairwise worse cases remain part of the review; no performance number is
reused as a new soc result.

The source defines static known-DAG look-ahead, with resources reserved for one
job, not cross-service opportunity cost, H-priority or the L-P95 bound. Applying
it to arrived DAGs, compatibility sets and shared online resources requires a
separately specified project adaptation. No new baseline rule, candidate,
parameter or scheduler is defined or implemented in this task. Algorithm-code
availability is UNVERIFIED; its cited random-DAG generator is not PEFT code.

# HEFT/CPOP — verified local original and page-level review

Status: VERIFIED_PRIMARY. All 15 PDF pages (printed 260–274) were read.
All pages rendered successfully; the full-document contact sheet and enlarged
algorithm figures on PDF pages 5 and 7 were inspected. This is literature review,
not algorithm implementation or scientific validation. The earlier failed-source
checklist is retained in reports/history/p0_before_local_pdf_review_1b36f39/.

## Identity, version and actual input

Haluk Topcuoglu, Salim Hariri and Min-You Wu, “Performance-Effective and
Low-Complexity Task Scheduling for Heterogeneous Computing,” IEEE Transactions
on Parallel and Distributed Systems 13(3), 260–274, March 2002.
DOI: 10.1109/71.993206. Title/authors/issue are on PDF page 1 and printed
pagination is continuous. DOI is in the actual PDF Subject metadata, consistent
with the prior Crossref record; it is not claimed printed on page 260.

- Actual input: /workspace/attachments/b3bdf00a-9211-4180-a198-d2b3c7a28d17/Performance-effective_and_low-complexity_task_scheduling_for_heterogeneous_computing.pdf
- Ignored local copy: .cache/literature/HEFT_CPOP_Topcuoglu_2002.pdf
- Actual attachment locator: sediment://file_0000000083fc8207bc8eb1d928f7ae6c
- File size: 652304 bytes; PDF pages: 15.
- SHA256: 186bcf6a9fefb25c99cfd4d247e92f3fabc91cef5c3555ccb4d2d04ba6fec694
- Provenance: USER_PROVIDED_LOCAL_COPY_SOURCE_UNVERIFIED. The user reports a local
  download; no original download URL was supplied or invented.
- Version: publisher-formatted journal copy, with journal headers, copyright,
  licensed IEEE Xplore footer and complete reference/biography pages. Metadata
  reports later iText modification in 2018. Untouched publisher-binary
  authentication and upstream chain of custody are UNVERIFIED. Producer software
  metadata does not license redistribution of this article. PDF is not tracked.

P0_source_acquisition_014.json records actual paths, pdfinfo and per-page text
identities. Viewer PDF page = printed page minus 259. Mathematical transcriptions
below use normalized plain-text notation and preserve the original definitions.

## Original definitions and page evidence

| Item | Original evidence | Verification and relationship to soc |
|---|---|---|
| Model | pp.261–262, PDF 2–3, §2 | Static known application DAG; bounded heterogeneous processors, fully connected network; transfers without contention; compute/communication overlap; non-preemptive tasks. These do not establish continuous online multi-service behavior. |
| Average computation | p.262, PDF 3, Eq.(1) | wbar_i = sum_j w_i,j / q, with q processors and a full task×processor cost matrix. No compatibility-mask policy is defined. |
| Actual and mean transfer costs | p.262, PDF 3, Eqs.(2),(3) | Across processors m,n: c_i,k = L_m + data_i,k / B_m,n; same-processor transfer is zero. Rank labels use cbar_i,k = Lbar + data_i,k / Bbar. Do not substitute an unregistered mean of pairwise delays. Exact diagonal/pair-weight averaging convention is NOT_EXPLICITLY_SPECIFIED_IN_SOURCE here. |
| Upward rank | p.264, PDF 5, Eqs.(8),(9), §4.1 | Mean-cost longest suffix including the current node; recurrence and base below. It is not a deadline or actual remaining runtime. |
| HEFT priority | p.264, PDF 5, §4.2 and Fig.2 steps 1–5 | Nonincreasing rank_u; the prose explicitly uses random rank-tie breaking. A deterministic project tie rule must be identified as adaptation. |
| HEFT EFT choice | pp.262,264, PDF 3,5, Eqs.(4)–(6), Fig.2 steps 6–8 | Evaluate each processor with insertion; choose minimum EFT. Pred finish/data arrival and destination availability constrain the start. |
| Insertion | p.264, PDF 5, §4.2 | Search from task data-ready time for the first idle gap capable of holding the complete execution while preserving precedence. Not append-only assignment or preemption. |
| CPOP ranks/priority | pp.264–266, PDF 5–7, Eq.(10), Fig.5 steps 2–5 | Priority = rank_u + rank_d, with entry rank_d=0; CP length is entry priority. |
| CPOP path/processor | p.266, PDF 7, Fig.5 steps 6–13 | Select one connected entry-to-exit critical path; Fig.5 selects successors whose priority equals CP length, and prose resolves path ties by first highest-priority successor. Select processor minimizing cumulative computation cost of tasks on that path. |
| CPOP ready tasks | p.266, PDF 7, Fig.5 steps 14–21 | Highest-priority ready task; path tasks on the path processor, others on minimum-EFT processor; both insertion based. Heap costs stated: insert/delete O(log v), retrieve O(1). |
| Complexity | p.264, PDF 5, §4.2; p.266, PDF 7, §4.3 | Authors state HEFT O(e×q), dense-graph O(v²×p), and CPOP O(e×p). The source alternates q/p for processor count. These are source bounds, not measured or independently proved costs of future soc code. |

Here w_i,j is expected execution on processor j, e counts edges and v counts
tasks. Exact rank equations:

    rank_u(n_i) = wbar_i
                  + max over n_j in succ(n_i)[cbar_i,j + rank_u(n_j)]   (8)
    rank_u(n_exit) = wbar_exit                                        (9)
    rank_d(n_i) = max over n_j in pred(n_i)
                      [rank_d(n_j) + wbar_j + cbar_j,i]                (10)
    rank_d(n_entry) = 0

Source priority and processor expressions, from Fig.5 (not numbered Eq.(11)):

    priority(n_i) = rank_u(n_i) + rank_d(n_i)
    CP_length = priority(n_entry)
    p_CP minimizes sum over n_i in SET_CP of w_i,j

Fig.5 constructs one connected path. Treating every node on any tied critical
path as SET_CP would not transcribe that figure.

The source start/finish definitions on p.262 (PDF 3) are:

    EST(n_entry,p_j) = 0                                              (4)
    EST(n_i,p_j) = max(avail[j],
                      max over n_m in pred(n_i)[AFT(n_m)+c_m,i])      (5)
    EFT(n_i,p_j) = w_i,j + EST(n_i,p_j)                                (6)

All predecessors must already have been scheduled to evaluate these values.
The prose qualifies avail[j] as last assigned task completion for a noninsertion
policy; HEFT instead performs the slot search described on p.264. Static partial
schedule finish times are not permission to expose true future durations to
an online scheduler. Makespan is the objective, Eq.(7), p.262.

Equal-EFT processor tie behavior and CPOP ready-queue equal-priority tie details
are NOT_EXPLICITLY_SPECIFIED_IN_SOURCE in the cited definitions; this does not
change the explicitly stated random HEFT rank ties or CPOP path-tie rule.

## Full-paper coverage and limits

PDF 1–4: problem/model/related work; 5–7: algorithms and worked example;
8–12: reported random/application-graph experiments; 13 (§6, printed 272):
alternate policies; 14–15: conclusion/references/biographies. All were read.
The algorithm figures were inspected visually because extraction omits pseudocode.
The paper's §6 labels A1–A3 and B1–B3 are unrelated to soc baseline/ablation IDs.

The original assumptions support the definitions above, not soc's H/L budgets,
compatibility masks, continuous arrivals or a host-latency guarantee. Online
adaptation still needs separate, explicit implementation semantics within soc's
existing information boundary. No policy, extra CPOP baseline or scheduler is
defined or implemented here. The authors' results are literature findings,
never new clean-room runs, sample counts or evidence that soc's hypothesis wins.

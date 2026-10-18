# P0 environment

The original selected repository was audited before writing project code:
`/workspace/soc`, origin `https://github.com/JINAOLONG/soc.git`, branch `work`,
HEAD `0834f21afa07ce361970a011b4cd327f7c5ddc79`. It contained only LICENSE;
initial status was clean and no AGENTS.md existed. The original LICENSE is retained.
The origin identity matches JINAOLONG/soc. No git init, nested repository,
worktree, reset, clean or destructive operation was performed.

Detailed machine observations are in P0_environment.json. Initial observations:
Python 3.12.14, Linux x86_64, 5 visible vCPUs, Intel Xeon Platinum 8573C,
approximately 33 GiB memory and no swap. These are cloud-host observations, not
automotive hardware specifications. No scheduler timing result exists.

P0 code/tests use the Python standard library. Editable package installation
uses setuptools 80.9.0 and a repository-local .venv. Tests and setup are
noninteractive; no application service, external DB, GPU driver or credential
is required for P0. GitHub native read authentication already worked through
the existing platform configuration; no new token was requested.

Initial DOI/arXiv/author probes failed with proxy 403. Later retries retrieved
arXiv/Crossref/HAL content and four original manuscripts were reviewed. HEFT/CPOP
and PEFT remain unavailable as primary text: correct official IEEE landing pages
returned empty 202, PDF endpoints returned 418, and tried alternatives did not
supply the papers. UMinho's old domain redirects to repositorium.uminho.pt;
that destination and OA-discovery APIs also remain blocked on the recorded try.

The saved network draft preserves package-manager presets and adds 18 explicit
custom destinations: doi.org, arxiv.org, export.arxiv.org, ieeexplore.ieee.org,
dl.acm.org, api.crossref.org, inria.hal.science, hal.science, icl.utk.edu,
www.cs.umd.edu, cs.umd.edu, di.uminho.pt, www.di.uminho.pt,
repositorium.sdum.uminho.pt, hdl.handle.net, repositorium.uminho.pt,
api.openalex.org and api.semanticscholar.org. Some are exploratory source leads,
not verified paper hosts. Runtime readiness is based on the recorded responses,
not inferred from the draft. No secret/environment-variable requirements were
added. Saving the draft does not itself establish publication or fresh-task restore.

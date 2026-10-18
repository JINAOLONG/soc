"""Small numeric equation-regression inputs transcribed from the actual papers.

Not a workload generator, performance replication or redistributed page image.
Paper hashes and exact version provenance remain in literature_evidence.json.
"""
from soc.scheduler.kernels import source_tables


def _tables(rows, edges):
    costs = {str(i): dict(zip(("P1", "P2", "P3"), row)) for i, row in enumerate(rows, 1)}
    means = {(str(a), str(b)): v for a, b, v in edges}
    successors = {u: tuple(v for a, v in means if a == u) for u in costs}
    return source_tables(costs, successors, means)


def heft_example():
    # Topcuoglu et al.: PDF6/printed265 Fig3 input; PDF7/266 Table1 ranks.
    rows = [(14,16,9),(13,19,18),(11,13,19),(13,8,17),(12,13,10),
            (13,16,9),(7,15,11),(5,11,14),(18,12,20),(21,7,16)]
    edges = [(1,2,18),(1,3,12),(1,4,9),(1,5,11),(1,6,14),(2,8,19),(2,9,16),
             (3,7,23),(4,8,27),(4,9,23),(5,9,13),(6,8,15),(7,10,17),(8,10,11),(9,10,13)]
    return _tables(rows, edges)


def peft_example():
    # Arabnejad/Barbosa PDF2/printed683 Fig1; PDF6/687 Table2 OCT/ranks.
    rows = [(22,21,36),(22,18,18),(32,27,43),(7,10,4),(29,27,35),
            (26,17,24),(14,25,30),(29,23,36),(15,21,8),(13,16,33)]
    edges = [(1,2,17),(1,3,31),(1,4,29),(1,5,13),(1,6,7),(2,8,3),(2,9,30),
             (3,7,16),(4,8,11),(4,9,7),(5,9,57),(6,8,5),(7,10,9),(8,10,42),(9,10,7)]
    return _tables(rows, edges)

"""B1 bounded public remaining-H projection. No simulator/kernel imports.

All arithmetic below uses exact rationals decoded from public binary64 facts.
This offline observer never feeds back into scheduling or consumes private truth.
"""
from __future__ import annotations

from fractions import Fraction as F
import itertools

from soc.model.observation import Observation
from soc.p2.identity import EvidenceError, bits, digest, rational, semantic_bytes

RESOURCE_ORDER = ('CPU0', 'CPU1', 'CPU2', 'CPU3', 'GPU0', 'NPU0')


def snapshot(view: Observation, templates: dict[str, str]) -> dict:
    """Caller supplies independently checked public ID-derived template labels."""
    services = []
    for s in sorted(view.services, key=lambda x: x.id):
        if len(s.nodes) not in {8, 16} or s.id not in templates:
            raise EvidenceError('scientific snapshot requires approved public template/size')
        services.append(dict(service_id=s.id, template_id=templates[s.id], size=len(s.nodes),
            arrival_bits=bits(s.arrival), absolute_deadline_bits=bits(s.deadline), group=s.group,
            nodes=[dict(node_id=n.id,
                        estimates=[dict(resource_id=r, duration_bits=bits(dict(n.estimates)[r]))
                                   for r in RESOURCE_ORDER if r in dict(n.estimates)],
                        predecessors=[dict(node_id=p, size_bits=bits(b)) for p, b in sorted(n.predecessors)])
                   for n in sorted(s.nodes, key=lambda x: x.id)]))
    return dict(namespace='soc.p2.public-state.v2', schema_version=2, now_bits=bits(view.now), services=services,
        running=[dict(service_id=r.service, node_id=r.node, resource_id=r.resource,
                      start_bits=bits(r.start), elapsed_bits=bits(r.elapsed)) for r in view.running],
        completed=[dict(service_id=r.service, node_id=r.node, resource_id=r.resource,
                        finish_bits=bits(r.finish)) for r in view.completed],
        resources=[dict(resource_id=r, resource_type=next(x.kind for x in view.resources if x.id == r)) for r in RESOURCE_ORDER],
        links=[dict(source_type=l.source, destination_type=l.destination,
                    latency_bits=bits(l.latency), bandwidth_bits=bits(l.bandwidth))
               for l in sorted(view.links, key=lambda x: (x.source, x.destination))])


def unique_states(scope: dict, events: list[dict]) -> list[dict]:
    """Validate contiguous events; retain all events and mark first representatives."""
    required_scope = {'run_id', 'primary_attempt_id', 'observer_spec_sha256'}
    if set(scope) != required_scope:
        raise EvidenceError('invalid primary denominator scope')
    scope_body = dict(namespace='soc.p2.denominator-scope.v2',schema_version=2,**scope)
    scope_sha = digest(semantic_bytes(scope_body))
    seen, ids, result = {}, set(), []
    for seq, e in enumerate(events):
        if e['event_seq'] != seq or e['decision_seq'] != seq or e['event_id'] in ids or e['stream_role'] != 'PRIMARY':
            raise EvidenceError('duplicate/discontinuous/nonprimary snapshot stream')
        ids.add(e['event_id'])
        sha = digest(semantic_bytes(e['snapshot']))
        if sha != e['state_sha256']:
            raise EvidenceError('snapshot hash mismatch')
        key = digest(semantic_bytes({'namespace':'soc.p2.state-key.v2','schema_version':2,
                                    'denominator_scope_sha256': scope_sha, 'state_sha256': sha}))
        first = seen.setdefault(key, seq)
        result.append({**e, 'state_key': key, 'counted_as_event_seq': first})
    return result


def _gap(ready: F, duration: F, occupied: list[tuple[F, F]]) -> F:
    t = ready
    for a, b in sorted(occupied):
        if t+duration <= a:
            break
        if t < b: t = b
    return t


def evaluate(view: Observation) -> dict:
    """Evaluate one public view, with the accepted 1..4 B1 action scope."""
    now = F(view.now)
    services = {s.id: s for s in view.services}
    nodes = {n.id: (s, n) for s in view.services for n in s.nodes}
    done = {r.node: r for r in view.completed}
    running = {r.node: r for r in view.running}
    if len(nodes) != sum(len(s.nodes) for s in view.services):
        raise EvidenceError('duplicate public node identity')
    occupied = set(done) | set(running)
    ready = sorted((n.id for s in view.services for n in s.nodes if n.id not in occupied and
                    all(p in done for p, _ in n.predecessors)),
                   key=lambda nid: (nodes[nid][0].group != 'H', nodes[nid][0].deadline, nodes[nid][0].id, nid))
    pending = sorted((s for s in view.services if s.group == 'H' and any(n.id not in occupied for n in s.nodes)),
                     key=lambda s: (s.deadline, s.id))
    if not ready or not pending:
        return {'status': 'NOT_IN_SCOPE'}
    partial = []
    if len(ready) > 4: partial.append('READY_CAP')
    if len(pending) > 2: partial.append('PENDING_H_CAP')
    if any(len(s.nodes) > 16 for s in pending): partial.append('DAG_CAP')
    for r in view.running:
        if r.node not in nodes or r.resource not in dict(nodes[r.node][1].estimates):
            raise EvidenceError('invalid running identity')
        estimate = dict(nodes[r.node][1].estimates)[r.resource]
        if r.elapsed >= estimate: partial.append('ESTIMATE_EXHAUSTED')
    if partial:
        return {'status': 'COVERAGE_INSUFFICIENT', 'reasons': sorted(set(partial)),
                'all_ready_count': len(ready), 'all_pending_H': len(pending)}
    actions = ready[:4]
    targets = pending[:2]
    kinds = {r.id: r.kind for r in view.resources}
    links = {(l.source, l.destination): (F(l.latency), F(l.bandwidth)) for l in view.links}
    def transfer(src, dst, size):
        if src == dst: return F(0)
        lat, bandwidth = links[kinds[src], kinds[dst]]
        return lat+F(size)/bandwidth
    initial = {r: [] for r in kinds}
    placed = {r.node: (F(r.finish), r.resource) for r in view.completed}
    for r in view.running:
        remaining = F(dict(nodes[r.node][1].estimates)[r.resource])-F(r.elapsed)
        release = now+max(F(0), remaining)
        initial[r.resource].append((now, release))
        placed[r.node] = (release, r.resource)
    suffix = {n.id for s in targets for n in s.nodes if n.id not in placed and n.id not in actions}
    def project(assignment=None):
        calendars = {r: list(rows) for r, rows in initial.items()}
        finishes = dict(placed)
        action_finishes = {}
        def place(nid, forced=None):
            s, n = nodes[nid]
            if any(p not in finishes for p, _ in n.predecessors):
                raise EvidenceError('projection lacks public predecessor')
            options = []
            for resource, estimate in n.estimates:
                if forced is not None and resource != forced: continue
                at = max([now, F(s.arrival)]+[finishes[p][0]+transfer(finishes[p][1], resource, b)
                                             for p, b in n.predecessors])
                start = _gap(at, F(estimate), calendars[resource])
                options.append((start+F(estimate), resource, start))
            if not options: raise EvidenceError('empty compatible projection')
            finish, resource, start = min(options)
            calendars[resource].append((start, finish))
            finishes[nid] = finish, resource
            return finish
        for index, nid in enumerate(actions):
            action_finishes[nid] = place(nid, assignment[index] if assignment is not None else None)
        todo = set(suffix)
        while todo:
            available = [n for n in todo if all(p in finishes for p, _ in nodes[n][1].predecessors)]
            if not available: raise EvidenceError('invalid/cyclic suffix')
            nid = min(available, key=lambda n: (nodes[n][0].deadline, nodes[n][0].id, n))
            place(nid)
            todo.remove(nid)
        objective = sum((max(finishes[n.id][0] for n in s.nodes) for s in targets), F(0))/len(targets)
        return objective, action_finishes
    baseline, base_actions = project()
    best, best_assignment = baseline, None
    assignments = 0
    for assignment in itertools.product(*(sorted(dict(nodes[n][1].estimates)) for n in actions)):
        assignments += 1
        objective, finished = project(assignment)
        if any(finished[n] > max(base_actions[n], F(nodes[n][0].deadline))
               for n in actions if nodes[n][0].group == 'L'):
            continue
        if objective < best or (objective == best and (best_assignment is None or assignment < best_assignment)):
            best, best_assignment = objective, assignment
    b, o = baseline-now, best-now
    if b <= 0 or o > b: raise EvidenceError('invalid projected objective')
    return {'status': 'FULL', 'action_nodes': actions, 'target_H': [s.id for s in targets],
            'assignments': assignments, 'baseline': rational(b), 'optimal': rational(o),
            'delta': rational(b-o), 'gain': rational((b-o)/b),
            'best_assignment': list(best_assignment) if best_assignment is not None else None}

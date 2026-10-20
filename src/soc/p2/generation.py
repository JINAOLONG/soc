"""Exact approved generation arithmetic; no registered materialization at import.

The public scientific entry requires a live authority permit. Correctness tests
exercise arithmetic using manually specified keys and graphs, never CAL seeds.
"""
from __future__ import annotations

from dataclasses import asdict
from decimal import Decimal
from fractions import Fraction as F
import json
import math
from pathlib import Path

from soc.model.schema import Dependency, Duration, Link, Node, Service, Workload, topological_order
from soc.p2.identity import EvidenceError, digest, rational, fraction, semantic_bytes


GENERATOR = 'soc-p2-synthetic-v2-PROPOSED'
KEY_FIELDS = {'domain', 'schema_version', 'generator_version', 'actual_seed_decimal_string',
              'scenario', 'condition_id', 'config_id', 'service_slot', 'service_group',
              'template_node_id', 'resource_id', 'edge_id', 'field', 'counter'}


def decimal_table(path: Path):
    return json.loads(path.read_bytes(), parse_float=Decimal)


def exact(value) -> F:
    if type(value) is bool or isinstance(value, float):
        raise EvidenceError('binary64 cannot be a proposed exact decimal')
    return F(value)


def rn64(value: F, *, positive=False) -> float:
    try:
        v = float(value)
    except OverflowError as exc:
        raise EvidenceError('binary64 conversion overflow') from exc
    if not math.isfinite(v) or v < 0 or (positive and v <= 0):
        raise EvidenceError('invalid converted duration/time')
    return v if v else 0.0


def field_key(seed: str, config: dict, slot: int, field: str,
              group='', node='', resource='') -> dict:
    if type(seed) is not str or not seed.isascii() or not seed.isdecimal() or str(int(seed)) != seed:
        raise EvidenceError('noncanonical seed text')
    if type(slot) is not int or not 0 <= slot < 50:
        raise EvidenceError('invalid service slot')
    if field not in {'arrival_jitter', 'service_role_factor', 'duration_factor'}:
        raise EvidenceError('unregistered random field')
    if field == 'arrival_jitter':
        group = node = resource = ''
    elif field == 'service_role_factor':
        resource = ''
    if field != 'arrival_jitter' and (group not in {'H', 'L'} or not node):
        raise EvidenceError('node key requires group/node')
    if field == 'duration_factor' and resource not in {'CPU0', 'CPU1', 'CPU2', 'CPU3', 'GPU0', 'NPU0'}:
        raise EvidenceError('actual factor requires resource')
    return dict(domain='soc.p2.gen.v2', schema_version=2, generator_version=GENERATOR,
                actual_seed_decimal_string=seed, scenario=config['scenario'],
                condition_id=config['condition_id'], config_id=config['config_id'],
                service_slot=slot, service_group=group, template_node_id=node,
                resource_id=resource, edge_id='', field=field, counter=0)


def uniform(key: dict) -> F:
    if set(key) != KEY_FIELDS:
        raise EvidenceError('random key field mismatch')
    return F(int.from_bytes(bytes.fromhex(digest(semantic_bytes(key)))[:8], 'big'), 2**64)


def factor(key: dict) -> F:
    return F(9, 10)+uniform(key)/5


def arrival(period: F, slot: int, u: F) -> F:
    if period <= 0 or type(slot) is not int or not 0 <= slot < 50 or not 0 <= u < 1:
        raise EvidenceError('invalid arrival parameters')
    return period*(5*(slot//5)+F(slot % 5, 4)+u/10)


def critical_estimate(nodes: list[dict], estimates: dict[str, dict[str, F]]) -> F:
    done = {}
    todo = {n['id']: n for n in nodes}
    while todo:
        ready = sorted(k for k, n in todo.items() if all(p in done for p in n['predecessors']))
        if not ready:
            raise EvidenceError('cyclic/missing exact DAG')
        for k in ready:
            row = estimates[k]
            if not row or any(v <= 0 for v in row.values()):
                raise EvidenceError('invalid exact estimates')
            done[k] = min(row.values())+max((done[p] for p in todo[k]['predecessors']), default=F(0))
            del todo[k]
    return max(done.values(), default=F(0))


class Generator:
    def __init__(self, root: Path):
        self.root = root
        base = root/'docs/P2_design/v2'
        self.templates = {x['template_id']: x for x in decimal_table(base/'P2_workload_templates_v2.json')['templates']}
        self.profiles = {x['role']: x for x in decimal_table(base/'P2_resource_profiles_v2.json')['profiles']}
        self.network = decimal_table(base/'P2_communication_profiles_v2.json')
        self.edges = {x['template_id']: x['edges'] for x in self.network['edge_tables']}

    def materialize(self, config: dict, seed: str, permit) -> tuple[Workload, dict]:
        """Production entry: no numeric work precedes trusted authorization."""
        permit.authorize_generation(config, seed)
        return self._build(config, seed)

    def _build(self, config: dict, seed: str, *, slots=50) -> tuple[Workload, dict]:
        template = self.templates[config['template_id']]
        edges = self.edges[config['template_id']]
        links = tuple(Link(x['source_type'], x['destination_type'], rn64(exact(x['latency_ms'])),
                           rn64(exact(x['bandwidth_mib_per_ms']), positive=True)) for x in self.network['links'])
        services, sidecar = [], {}
        period = exact(config['period_ms'])
        for slot in range(slots):
            at = rn64(arrival(period, slot, uniform(field_key(seed, config, slot, 'arrival_jitter'))))
            for group in ('H', 'L'):
                sid = f"{config['scenario']}/{config['load']}/{config['size']}/{config['config_id']}/s{slot:03d}/{group}"
                estimates, built = {}, []
                for n in template['nodes']:
                    shared = factor(field_key(seed, config, slot, 'service_role_factor', group, n['id']))
                    row = {r: exact(c)*F(n['cost_scale'])*shared for r, c in
                           self.profiles[n['role']]['estimated_base_ms'].items() if c is not None}
                    estimates[n['id']] = row
                    costs = tuple(Duration(r, rn64(e, positive=True), rn64(e*factor(field_key(
                        seed, config, slot, 'duration_factor', group, n['id'], r)), positive=True))
                                  for r, e in sorted(row.items()))
                    deps = tuple(Dependency(sid+'/'+e['source'], rn64(exact(e['size_mib'])))
                                 for e in edges if e['destination'] == n['id'])
                    built.append(Node(sid+'/'+n['id'], costs, deps))
                deadline = (F(5, 2) if group == 'H' else F(4))*critical_estimate(template['nodes'], estimates)
                services.append(Service(sid, at, rn64(deadline, positive=True), group, tuple(built)))
                sidecar[sid] = {'estimates': {sid+'/'+n: {r: rational(v) for r, v in row.items()}
                                            for n, row in estimates.items()}, 'deadline': rational(deadline)}
        return Workload(tuple(services), links), sidecar

    def control_gap(self, parent: Workload, sidecar: dict) -> int:
        if {s.id for s in parent.services} != sidecar.keys():
            raise EvidenceError('control exact sidecar membership mismatch')
        bounds = []
        for s in parent.services:
            rows = sidecar[s.id]['estimates']
            if rows.keys() != {n.id for n in s.nodes}:
                raise EvidenceError('sidecar node membership mismatch')
            total = sum((max(F(11, 10)*fraction(v) for v in row.values()) for row in rows.values()), F(0))
            for n in s.nodes:
                for edge in n.predecessors:
                    # Edge sizes in the approved tables are dyadic, so the
                    # binary64 input is exact; no table-decimal round trip.
                    b = F(edge.size)
                    total += max(exact(x['latency_ms'])+b/exact(x['bandwidth_mib_per_ms'])
                                 for x in self.network['links'])
            bounds.append(total+fraction(sidecar[s.id]['deadline']))
        return math.ceil(max(bounds, default=F(0)))+1

    def derive_control(self, parent: Workload, sidecar: dict, variant: str) -> tuple[Workload, int]:
        if variant not in {'H_ISOLATED', 'LOW_COMPETITION'}:
            raise EvidenceError('unknown control')
        gap = self.control_gap(parent, sidecar)
        # Parent materialization is slot-major, H then L. Preserve that order.
        kept = [s for s in parent.services if variant != 'H_ISOLATED' or s.group == 'H']
        result = tuple(Service(s.id, rn64(F(k*gap)), s.relative_deadline, s.group, s.nodes)
                       for k, s in enumerate(kept))
        return Workload(result, parent.links, parent.resources), gap


def payload(workload: Workload) -> dict:
    """Header-free runtime family; never relabel a P1 fixture envelope."""
    return asdict(workload)


def parse_payload(value: dict) -> Workload:
    if set(value) != {'services', 'resources', 'links'}:
        raise EvidenceError('unexpected runtime payload header')
    for service in value['services']:
        if set(service) != {'id','arrival','relative_deadline','group','nodes'}:
            raise EvidenceError('unexpected service field')
        for node in service['nodes']:
            if set(node) != {'id','durations','predecessors'}:
                raise EvidenceError('unexpected node field')
            if any(set(d)!={'resource','estimate','realized'} for d in node['durations']) or any(set(e)!={'node','size'} for e in node['predecessors']):
                raise EvidenceError('unexpected duration/dependency field')
    from soc.model.schema import Resource
    return Workload(tuple(Service(s['id'], s['arrival'], s['relative_deadline'], s['group'],
                    tuple(Node(n['id'], tuple(Duration(**d) for d in n['durations']),
                               tuple(Dependency(**e) for e in n['predecessors'])) for n in s['nodes']))
                          for s in value['services']), tuple(Link(**x) for x in value['links']),
                    tuple(Resource(**x) for x in value['resources']))

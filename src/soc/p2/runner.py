"""Finite plan inspection and fail-closed scientific entry.

Correctness execution is deliberately separate from scientific admission.
The present implementation authorization never grants science permission.
"""
from __future__ import annotations

import json
from pathlib import Path

from soc.p2.identity import EvidenceError, digest, strict_json


class ScientificExecutionUnavailable(EvidenceError):
    pass


def inspect_plan(root: Path) -> dict:
    """Read existing symbolic matrix only; do not fetch/materialize seed data."""
    path=root/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json'
    matrix=strict_json(path.read_bytes())
    if digest(path.read_bytes())!='b58fe4c2eead01fc9b92966d557ed0bb052e7387794fc0d9b58029ffdb90af0e':
        raise EvidenceError('approved matrix byte identity changed')
    trials=matrix['trials']
    ids=[r['trial_id'] for r in trials]
    if len(trials)!=2520 or len(set(ids))!=2520 or len(matrix['configs'])!=36:
        raise EvidenceError('finite roster count/identity mismatch')
    counts={}
    workloads=set()
    for order,row in enumerate(trials,1):
        if (row['partition']!='CALIBRATION' or row['execution_order']!=order or row['budget_count']!=1 or
                row['method'] not in {'B1','B2','B3','B4','B5'} or
                row['workload_sha256'] is not None or row['command'] is not None):
            raise EvidenceError('invalid/unexpected symbolic trial')
        if row['variant']!='MAIN' and row['method']!='B2': raise EvidenceError('invalid control method')
        counts[row['variant']]=counts.get(row['variant'],0)+1
        workloads.add(row['workload_id'])
    if counts!={'H_ISOLATED':360,'LOW_COMPETITION':360,'MAIN':1800} or len(workloads)!=1080:
        raise EvidenceError('finite roster product mismatch')
    return {'trial_slots':2520,'symbolic_inputs':1080,'engine_call_limit':5040,
            'automatic_retries':0,'materialized_inputs':0,'scientific_workloads_run':0,
            'matrix_sha256':digest(path.read_bytes())}


def preflight(root: Path) -> dict:
    reasons=[]
    accepted=root/'docs/P2_design/accepted/decisions.json'
    if not accepted.exists():
        reasons.append('ACCEPTED_DECISIONS_NOT_RECORDED')
    else:
        record=strict_json(accepted.read_bytes())
        if record.get('selected_observation_route')!='B1_EXPAND_SINGLE_READY' or record.get('selected_coordination_policy')!='A_NO_TAKEOVER' or record.get('selected_threshold_bundle')!='COARSE':
            reasons.append('ACCEPTED_ROUTE_BINDING_MISMATCH')
        for path,sha in record.get('source_sha256',{}).items():
            target=root/path
            if not target.is_file() or digest(target.read_bytes())!=sha:
                reasons.append('ACCEPTED_DEFINITION_HASH_MISMATCH:'+path)
    # No default profile, boolean flag or command-line option may manufacture
    # missing deployment proofs or a separately issued scientific grant.
    reasons += ['SCIENTIFIC_EXECUTION_NOT_AUTHORIZED', 'PERSISTENT_STORAGE_NOT_VERIFIED',
                'DEPLOYMENT_PROFILE_NOT_FROZEN', 'SEALED_WORKER_NOT_VALIDATED',
                'PRODUCTION_ADMISSION_NOT_DEPLOYED']
    return {'stage':'P2','status':'BLOCKED','reasons':reasons,
            'implementation_authorized':True,'scientific_execution_authorized':False,
            'scientific_workloads_generated':0,'scientific_workloads_run':0}


def run_calibration(root: Path) -> dict:
    report=preflight(root)
    # A live production authority adapter must replace this boundary only after
    # deployment validation and a new explicit science authorization. There is
    # intentionally no force/fixture flag that turns off these prerequisites.
    return report


class NoScientificPermit:
    def authorize_execution(self,*args,**kwargs):
        raise ScientificExecutionUnavailable('scientific engine execution is not authorized')

    def authorize_generation(self,*args,**kwargs):
        raise ScientificExecutionUnavailable('registered generation is not authorized')

    def authorize_analysis(self,*args,**kwargs):
        raise ScientificExecutionUnavailable('scientific analysis is not authorized')

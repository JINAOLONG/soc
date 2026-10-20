"""Single-host research simulation, distinct from V3 production deployment.

Fixed CALIBRATION roster, exclusive local ownership, immutable call reservations,
zero retry, independent input/physical checks and one exact registered replay.
No service, lease or distributed publication authority is claimed or required.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback

from soc.model.schema import canonical_bytes
from soc.p2.adapter import validate_physical_payload
from soc.p2.generation import Generator, payload
from soc.p2.identity import EvidenceError
from soc.p2.local_input_validation import validate_main, validate_control
from soc.p2.qualification import busy_pressure, controls_witness, classify_config, select_configs, feasibility
from soc.p2.runner import inspect_plan
from soc.simulator.engine import simulate
from soc.validation.governance import audit_p0, relevant_source_hash
from soc.validation.p1 import audit_p1


def utc():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def sha(data): return hashlib.sha256(data).hexdigest()


def write_new(path, value, *, compressed=False):
    data=canonical_bytes(value)
    stored=gzip.compress(data,compresslevel=6,mtime=0) if compressed else data
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:
        f.write(stored);f.flush();os.fsync(f.fileno())
    fd=os.open(path.parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    return {'path':str(path),'sha256':sha(stored),'content_sha256':sha(data),'size_bytes':len(stored)}


def compact(trace):
    return {k:v for k,v in trace.items() if k not in {'schema_version','origin'}}


def positive_busy_wait(workload, trace):
    # Exact predicate equivalent to existence of positive assigned_busy_wait;
    # use independently recomputed data_ready and physical intervals, not total
    # ready_wait (which also includes idle policy waiting).
    rows={(r['service'],r['node']):r for r in trace['executions']}
    by_resource=defaultdict(list)
    for r in trace['executions']: by_resource[r['resource']].append(r)
    for w in trace['metrics']['waiting']:
        own=rows[w['service'],w['node']]
        if any(r is not own and min(own['start'],r['finish'])>max(w['data_ready'],r['start'])
               for r in by_resource[own['resource']]): return True
    return False


def inspect_local(root):
    checks={'p0':audit_p0(root),'p1':audit_p1(root)}
    errors=[]
    for key,value in checks.items():
        if value['status']!='PASS': errors.append(key.upper()+'_NOT_PASS')
    accepted=json.loads((root/'docs/P2_design/accepted/decisions.json').read_text())
    for name,expected in accepted['source_sha256'].items():
        if sha((root/name).read_bytes())!=expected: errors.append('ACCEPTED_HASH_MISMATCH:'+name)
    scope=root/'docs/P2_design/accepted/local_simulation_scope_001.json'
    if not scope.exists() or not json.loads(scope.read_text()).get('local_simulation_authorized'):
        errors.append('LOCAL_SIMULATION_SCOPE_NOT_RECORDED')
    repo=subprocess.check_output(['git','remote','get-url','origin'],cwd=root,text=True).strip()
    if repo!='https://github.com/JINAOLONG/soc.git': errors.append('WRONG_REPOSITORY')
    source_paths=['src','scripts','configs']
    dirty=subprocess.check_output(['git','status','--porcelain','--',*source_paths],cwd=root,text=True)
    if dirty: errors.append('SOURCE_CONFIG_NOT_COMMITTED')
    plan=inspect_plan(root)
    return {'status':'BLOCKED' if errors else 'READY_FOR_LOCAL_SIMULATION','errors':errors,
            'checks':checks,'plan':plan,'mode':'LOCAL_RESEARCH_SIMULATION',
            'v3_production_contract_claimed':False,'production_deployment_required':False}


class LocalPermit:
    def __init__(self, matrix):
        self.allowed={(c['config_id'],str(s)) for c in matrix['configs'] for s in matrix['registered_seeds']}
    def authorize_generation(self,config,seed):
        if (config['config_id'],seed) not in self.allowed: raise EvidenceError('unregistered local input')


def run(root: Path, output: Path):
    readiness=inspect_local(root)
    if readiness['errors']: return readiness
    if output.exists(): raise EvidenceError('Refusing a second campaign or retry into an existing directory')
    output.mkdir(parents=True)
    lock=(output/'owner.lock').open('xb')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    matrix=json.loads((root/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json').read_text())
    seed_meta=json.loads((root/'configs/seed_partitions.json').read_text())
    if matrix['registered_seeds']!=seed_meta['partitions']['CALIBRATION']:
        raise EvidenceError('registered CALIBRATION seed mismatch')
    config_map={c['config_id']:c for c in matrix['configs']}
    source_sha=relevant_source_hash(root)
    context={'mode':'LOCAL_RESEARCH_SIMULATION','started_at_utc':utc(),'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
             'dirty_status':subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True),
             'source_sha256':source_sha,'host':platform.node(),'platform':platform.platform(),
             'python':sys.version,'pid':os.getpid(),'command':[sys.executable,*sys.argv],
             'matrix_sha256':sha((root/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json').read_bytes()),
             'seed_metadata_sha256':sha((root/'configs/seed_partitions.json').read_bytes()),
             'scope_sha256':sha((root/'docs/P2_design/accepted/local_simulation_scope_001.json').read_bytes()),
             'expected_primary_runs':2520,'expected_replays':2520,'automatic_retries':0,
             'production_contract_compliance':'NOT_CLAIMED','storage_guarantee':'Local fsync plus GitHub publication; environment-loss durability NOT_CLAIMED',
             'decision_storage':'Time/proposal per invocation; full public views reconstructible from retained input and prior actual starts/completions'}
    write_new(output/'context.json',context)
    write_new(output/'preflight.json',readiness)
    generator=Generator(root);permit=LocalPermit(matrix)
    inputs={}; records=[]; primary_calls=replay_calls=0; valid_count=0; generated_inputs=0
    started=time.monotonic()
    progress_path=output/'progress.json'
    def progress(status, **extra):
        data={'status':status,'updated_at_utc':utc(),'primary_calls':primary_calls,'replay_calls':replay_calls,
              'valid_trials':valid_count,'expected_trials':2520,'generated_inputs':generated_inputs,
              'elapsed_seconds':time.monotonic()-started,**extra}
        temp=output/'progress.next.json';temp.write_bytes(canonical_bytes(data));os.replace(temp,progress_path)
    try:
        for trial in matrix['trials']:
            if trial['partition']!='CALIBRATION': raise EvidenceError('non-CALIBRATION trial')
            config=config_map[trial['config_id']];seed=str(trial['calibration_seed']);variant=trial['variant']
            cid=config['config_id'];input_key=(cid,seed,variant)
            # Parent materialization is always before both control derivations.
            if (cid,seed,'MAIN') not in inputs:
                parent_key=(cid,seed,'MAIN')
                input_dir=output/'inputs'/cid/f"s{trial['seed_index']:02d}"
                write_new(input_dir/'generation_reserved.json',{'config':config,'seed':seed,'partition':'CALIBRATION','reserved_at_utc':utc(),'retry_allowed':False})
                parent,sidecar=generator.materialize(config,seed,permit)
                parent_ref=write_new(input_dir/'MAIN.json.gz',payload(parent),compressed=True)
                generated_inputs+=1
                write_new(input_dir/'exact_sidecar.json.gz',sidecar,compressed=True)
                birth=validate_main(root,config,seed,parent)
                write_new(input_dir/'MAIN.validation.json',birth)
                inputs[parent_key]=(parent,parent_ref,birth)
                for control in ('H_ISOLATED','LOW_COMPETITION'):
                    child,gap=generator.derive_control(parent,sidecar,control)
                    if gap!=birth['independent_control_gap']: raise EvidenceError('control gap independent mismatch')
                    child_ref=write_new(input_dir/(control+'.json.gz'),payload(child),compressed=True)
                    generated_inputs+=1
                    validated=validate_control(parent,child,control,gap)
                    write_new(input_dir/(control+'.validation.json'),{'parent_ref':parent_ref,'child_ref':child_ref,**validated})
                    inputs[cid,seed,control]=(child,child_ref,validated)
            workload,input_ref,birth=inputs[input_key]
            run_dir=output/'trials'/trial['trial_id']
            manifest={**trial,'run_id':trial['trial_id']+':LOCAL_SIMULATION_V1','mode':'LOCAL_RESEARCH_SIMULATION',
                      'timestamp_utc':utc(),'git_commit':context['git_commit'],'source_sha256':source_sha,
                      'config_sha256':sha(canonical_bytes(config)),'workload_sha256':input_ref['content_sha256'],
                      'input_ref':input_ref,'host':context['host'],'command':context['command'],
                      'dirty_status_at_campaign_start':context['dirty_status'],'process_id':os.getpid()}
            write_new(run_dir/'manifest.json',manifest)
            write_new(run_dir/'primary.reserved.json',{'timestamp_utc':utc(),'call':primary_calls+1,'no_retry':True})
            primary_calls+=1
            t0=time.monotonic(); at=utc()
            trace=compact(simulate(workload,trial['method'],compact_decisions=True))
            trace_ref=write_new(run_dir/'primary.trace.json.gz',trace,compressed=True)
            write_new(run_dir/'primary.returned.json',{'started_at_utc':at,'ended_at_utc':utc(),'wall_seconds':time.monotonic()-t0,'function_returned':True,'trace_ref':trace_ref})
            checked=validate_physical_payload(workload,trace)
            write_new(run_dir/'primary.validation.json',checked)
            if checked['status']!='PASS': raise EvidenceError('independent primary physical/metric failure')
            write_new(run_dir/'replay.reserved.json',{'timestamp_utc':utc(),'call':replay_calls+1,'no_retry':True,'same_sample_not_new_seed':True})
            replay_calls+=1
            t0=time.monotonic(); at=utc()
            replay=compact(simulate(workload,trial['method'],compact_decisions=True))
            replay_ref=write_new(run_dir/'replay.trace.json.gz',replay,compressed=True)
            check_replay=validate_physical_payload(workload,replay)
            exact=trace_ref['content_sha256']==replay_ref['content_sha256']
            write_new(run_dir/'replay.validation.json',{'started_at_utc':at,'ended_at_utc':utc(),'wall_seconds':time.monotonic()-t0,
                      'function_returned':True,'physical':check_replay,'exact_primary_match':exact,'trace_ref':replay_ref})
            if not exact or check_replay['status']!='PASS': raise EvidenceError('registered replay or physical failure')
            groups=checked['metrics']['groups']; services=checked['metrics']['services']
            row={**trial,'run_id':manifest['run_id'],'input_ref':input_ref,'primary_ref':trace_ref,'replay_ref':replay_ref,
                 'validity':'VALID','exact_replay':True,'groups':groups,'makespan':checked['metrics']['makespan'],
                 'H_dmr_exact':str(F(sum(s['missed'] for s in services if s['group']=='H'),50)),
                 'L_dmr_exact':str(F(sum(s['missed'] for s in services if s['group']=='L'),50)) if variant!='H_ISOLATED' else None}
            if variant=='MAIN' and trial['method']=='B2':
                pressure=busy_pressure(workload,trace['executions'],50*config['period_ms'])
                row['pressure_exact']=str(pressure);row['positive_assigned_busy_wait']=positive_busy_wait(workload,trace)
                natural=feasibility(workload)
                row['natural_infeasibility']={g:sum(s.group==g and natural[s.id]['classification']=='CERTIFIED_NATURALLY_INFEASIBLE' for s in workload.services) for g in ('H','L')}
                write_new(run_dir/'feasibility.json',natural)
            elif variant!='MAIN':
                row['control_witness']=controls_witness(workload,trace['executions'],{'H'} if variant=='H_ISOLATED' else {'H','L'})
            write_new(run_dir/'result.json',row)
            records.append(row);valid_count+=1
            progress('RUNNING',last_completed_trial=trial['trial_id'])
            if valid_count%7==0:
                print(json.dumps({'completed':valid_count,'total':2520,'primary':primary_calls,'replay':replay_calls,'elapsed_s':round(time.monotonic()-started,1),'last':trial['trial_id']}),flush=True)
            # A/B seed groups are contiguous. Do not retain whole campaign
            # runtime objects; the immutable persisted inputs remain authoritative.
            next_index=trial['execution_order']
            if next_index==len(matrix['trials']) or (matrix['trials'][next_index]['config_id'],str(matrix['trials'][next_index]['calibration_seed']))!=(cid,seed):
                inputs={}
                # Count on disk for progress is generated input count, not cache.
        if primary_calls!=2520 or replay_calls!=2520: raise EvidenceError('fixed roster not complete')
        by_key={(r['config_id'],str(r['calibration_seed']),r['variant'],r['method']):r for r in records}
        qualification=[];eligibility=defaultdict(dict)
        for config in matrix['configs']:
            cells=[]
            for seed_value in matrix['registered_seeds']:
                seed=str(seed_value);cid=config['config_id']
                main=by_key[cid,seed,'MAIN','B2'];h=by_key[cid,seed,'H_ISOLATED','B2'];low=by_key[cid,seed,'LOW_COMPETITION','B2']
                cells.append(dict(seed=seed,validity='VALID',pressure=main['pressure_exact'],H_dmr=main['H_dmr_exact'],L_dmr=main['L_dmr_exact'],
                                  H_control_witness=h['control_witness'],LOW_control_witness=low['control_witness'],positive_assigned_busy_wait=main['positive_assigned_busy_wait']))
            eligible=classify_config(config['load'],cells,{str(s) for s in matrix['registered_seeds']})
            eligibility[config['condition_id']][config['arrival_candidate']]=eligible
            qualification.append({'config':config,'eligible':eligible,'mean_pressure':float(sum(F(c['pressure']) for c in cells)/10),
                                  'mean_H_dmr':float(sum(F(c['H_dmr']) for c in cells)/10),'mean_L_dmr':float(sum(F(c['L_dmr']) for c in cells)/10),'seed_cells':cells})
        selection=select_configs(dict(eligibility))
        write_new(output/'qualification.json',{'configs':qualification,'selection':selection,'all_eligibility':dict(eligibility)})
        write_new(output/'all_results.json',records)
        if relevant_source_hash(root)!=source_sha: raise EvidenceError('source changed during scientific run')
        result={'mode':'LOCAL_RESEARCH_SIMULATION','execution_completion':'COMPLETE','artifact_integrity':'PENDING_FINAL_MANIFEST',
                'primary_runs':primary_calls,'registered_replays':replay_calls,'valid_trials':valid_count,'expected_trials':2520,
                'workloads_generated':1080,'input_seed_identity':'VALID','new_seeds_generated':False,
                'selection_status':selection['status'],'eligible_configs':sum(c['eligible'] for c in qualification),
                'ineligible_conditions':[c for c,v in eligibility.items() if not any(v.values())],
                'mapping_classification':'NOT_EVALUATED','diagnostic_validity':'NOT_RUN','m2_analysis':'NOT_RUN',
                'reason':'NO_ELIGIBLE_CONDITION' if selection['status']!='SELECTED_ALL_18' else 'QUALIFICATION_COMPLETE_DIAGNOSTIC_PENDING',
                'p2_status':'BLOCKED','v3_production_contract_compliance':'NOT_CLAIMED',
                'elapsed_seconds':time.monotonic()-started,'source_sha256':source_sha,'git_commit':context['git_commit'],
                'validation_unlocked':False,'formal_unlocked':False,'stop':True}
        write_new(output/'summary.json',result);progress('COMPLETE',selection_status=selection['status'])
        return result
    except BaseException as exc:
        failure={'status':'FAILED_OR_INCOMPLETE','error_type':type(exc).__name__,'error':str(exc),'traceback':traceback.format_exc(),
                 'primary_calls':primary_calls,'replay_calls':replay_calls,'valid_trials':valid_count,'p2_status':'BLOCKED','retry_allowed':False,'timestamp_utc':utc()}
        write_new(output/'failure.json',failure);progress('FAILED_OR_INCOMPLETE',error=str(exc))
        raise
    finally:
        lock.close()

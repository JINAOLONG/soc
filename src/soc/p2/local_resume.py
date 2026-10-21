"""Bounded foreground continuation of the existing local CALIBRATION campaign.

One explicitly approved exception for the already unknown trial247. Old
reservations and results remain immutable; every other call is single-use.
Scientific files from the original execution commit are verified byte-for-byte.
Only this orchestration module and its CLI may be additional execution files.
"""
from __future__ import annotations

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
from soc.p2.generation import Generator, parse_payload, payload
from soc.p2.identity import EvidenceError
from soc.p2.local_input_validation import validate_main, validate_control
from soc.p2.local_run import LocalPermit, compact, positive_busy_wait, sha, utc, write_new
from soc.p2.qualification import busy_pressure, controls_witness, feasibility
from soc.p2.runner import inspect_plan
from soc.simulator.engine import simulate
from soc.validation.governance import audit_p0, relevant_source_hash, canonical_bytes as source_canonical_bytes
from soc.validation.p1 import audit_p1

ADDITIONS={'src/soc/p2/local_resume.py','scripts/resume_local_calibration.py'}
AUTHORIZATION='docs/P2_design/accepted/local_recovery_001.json'


def load(path): return json.loads(path.read_bytes())


def compare_core(expected, actual, expected_digest):
    if set(expected)!=set(actual): raise EvidenceError('frozen scientific file roster changed')
    rows=sorted(expected.items())
    if sha(source_canonical_bytes(rows))!=expected_digest: raise EvidenceError('original source digest not reconstructed')
    if any(actual[k]!=v for k,v in expected.items()): raise EvidenceError('frozen scientific file bytes changed')
    return {'status':'PASS','files':len(rows),'original_source_sha256':expected_digest}


def frozen_core(root, context):
    commit=context['git_commit']
    raw=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'--','src','scripts','configs'],cwd=root,text=True)
    def in_scope(p):
        return '__pycache__' not in p.parts and not any(x.endswith('.egg-info') for x in p.parts) and p.suffix!='.pyc'
    paths=[p for p in raw.splitlines() if in_scope(Path(p))]
    expected={p:sha(subprocess.check_output(['git','show',commit+':'+p],cwd=root)) for p in paths}
    actual={str(p.relative_to(root)):sha(p.read_bytes()) for prefix in ('src','scripts','configs')
            for p in (root/prefix).rglob('*') if p.is_file() and in_scope(p) and str(p.relative_to(root)) not in ADDITIONS}
    return compare_core(expected,actual,context['source_sha256'])


def inspect_resume(root):
    out=root/'results/calibration/local_001';errors=[]
    context=load(out/'context.json');auth=load(root/AUTHORIZATION)
    if not (auth.get('approved') is True and auth.get('allowed_recovery_trial')=='proposal-v2-t0247'
            and auth.get('extra_primary_call_limit')==1 and auth.get('total_engine_call_ceiling')==5041
            and auth.get('expected_unique_trial_results')==2520):
        raise EvidenceError('exact scoped recovery authorization missing')
    if sha((root/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json').read_bytes())!=context['matrix_sha256']:
        raise EvidenceError('matrix changed')
    if sha((root/'configs/seed_partitions.json').read_bytes())!=context['seed_metadata_sha256']:
        raise EvidenceError('seed metadata changed')
    if sha((root/'docs/P2_design/accepted/local_simulation_scope_001.json').read_bytes())!=context['scope_sha256']:
        raise EvidenceError('original local scope changed')
    decisions=load(root/'docs/P2_design/accepted/decisions.json')
    for name,digest in decisions['source_sha256'].items():
        if sha((root/name).read_bytes())!=digest: raise EvidenceError('accepted definition changed: '+name)
    core=frozen_core(root,context)
    prior=root/'reports/P2_calibration/local_001/interruption_001/preserved_raw_manifest.json'
    if sha(prior.read_bytes())!=auth['prior_raw_manifest_sha256']:
        raise EvidenceError('prior interruption inventory changed')
    for entry in load(prior)['files']:
        p=root/entry['path']
        if p.stat().st_size!=entry['size_bytes'] or sha(p.read_bytes())!=entry['sha256']:
            raise EvidenceError('preserved interrupted-campaign bytes changed: '+entry['path'])
    checks={'p0':audit_p0(root),'p1':audit_p1(root)}
    for k,v in checks.items():
        if v['status']!='PASS': errors.append(k+'_NOT_PASS')
    if subprocess.check_output(['git','status','--porcelain','--','src','scripts','configs'],cwd=root,text=True):
        errors.append('EXECUTION_SOURCE_NOT_COMMITTED')
    if subprocess.check_output(['git','remote','get-url','origin'],cwd=root,text=True).strip()!='https://github.com/JINAOLONG/soc.git':
        errors.append('WRONG_REPOSITORY')
    plan=inspect_plan(root)
    return {'status':'BLOCKED' if errors else 'READY_FOR_FOREGROUND_CONTINUATION','errors':errors,
            'core_byte_identity':core,'preserved_original_files':len(load(prior)['files']),
            'checks':checks,'plan':plan,'recovery_authorization_sha256':sha((root/AUTHORIZATION).read_bytes()),
            'source_sha256':relevant_source_hash(root)}


def read_ref(ref, root):
    path=Path(ref['path'])
    if not path.is_absolute(): path=root/path
    if not path.is_relative_to(root/'results/calibration/local_001'): raise EvidenceError('artifact path outside campaign')
    data=path.read_bytes()
    if len(data)!=ref['size_bytes'] or sha(data)!=ref['sha256']: raise EvidenceError('retained raw artifact changed')
    body=gzip.decompress(data)
    if sha(body)!=ref['content_sha256']: raise EvidenceError('retained content hash mismatch')
    return json.loads(body)


def complete_prefix(out, trials, root):
    rows=[]
    for t in trials:
        p=out/'trials'/t['trial_id']/'result.json'
        if not p.exists(): break
        r=load(p)
        if r['trial_id']!=t['trial_id'] or r['validity']!='VALID' or r['exact_replay'] is not True:
            raise EvidenceError('invalid saved result')
        for key in ('config_id','calibration_seed','method','variant','workload_id','partition'):
            if r[key]!=t[key]: raise EvidenceError('saved result differs from registered roster')
        for field in ('input_ref','primary_ref','replay_ref'): read_ref(r[field],root)
        if r['primary_ref']['content_sha256']!=r['replay_ref']['content_sha256']:
            raise EvidenceError('saved replay differs from primary')
        rows.append(r)
    if len(list((out/'trials').glob('*/result.json')))!=len(rows): raise EvidenceError('noncontiguous saved results')
    return rows


def ledger(out):
    return {'original_primary_reservations':len(list((out/'trials').glob('*/primary.reserved.json'))),
            'recovery_primary_reservations':len(list((out/'trials').glob('*/recovery_001/primary.reserved.json'))),
            'replay_reservations':len(list((out/'trials').glob('*/replay.reserved.json')))}


def check_budget(counts, purpose, *, recovery=False):
    original=counts['original_primary_reservations'];extra=counts['recovery_primary_reservations'];replays=counts['replay_reservations']
    if not (0<=original<=2520 and 0<=extra<=1 and 0<=replays<=2520 and original+extra+replays<=5041):
        raise EvidenceError('campaign call reservation budget exceeded')
    if purpose=='PRIMARY':
        if recovery and extra: raise EvidenceError('one recovery recomputation already consumed')
        if not recovery and original>=2520: raise EvidenceError('original primary budget exhausted')
    elif purpose=='REPLAY':
        if replays>=2520: raise EvidenceError('replay budget exhausted')
    else: raise EvidenceError('unknown engine-call purpose')
    if original+extra+replays>=5041: raise EvidenceError('total engine-call cap exhausted')


def inputs_for(root, out, config, trial, generator, permit):
    directory=out/'inputs'/config['config_id']/f"s{trial['seed_index']:02d}"
    seed=str(trial['calibration_seed'])
    if directory.exists():
        # Never regenerate saved or partially created input generations.
        parent=parse_payload(json.loads(gzip.decompress((directory/'MAIN.json.gz').read_bytes())))
        main_check=validate_main(root,config,seed,parent)
        result={'MAIN':parent}
        for variant in ('H_ISOLATED','LOW_COMPETITION'):
            child=parse_payload(json.loads(gzip.decompress((directory/(variant+'.json.gz')).read_bytes())))
            validate_control(parent,child,variant,main_check['independent_control_gap'])
            result[variant]=child
        for variant in result:
            if load(directory/(variant+'.validation.json'))['status']!='PASS': raise EvidenceError('saved birth check missing')
    else:
        write_new(directory/'generation_reserved.json',{'config':config,'seed':seed,'partition':'CALIBRATION','reserved_at_utc':utc(),'retry_allowed':False})
        parent,sidecar=generator.materialize(config,seed,permit)
        parent_ref=write_new(directory/'MAIN.json.gz',payload(parent),compressed=True)
        write_new(directory/'exact_sidecar.json.gz',sidecar,compressed=True)
        main_check=validate_main(root,config,seed,parent)
        write_new(directory/'MAIN.validation.json',main_check);result={'MAIN':parent}
        for variant in ('H_ISOLATED','LOW_COMPETITION'):
            child,gap=generator.derive_control(parent,sidecar,variant)
            if gap!=main_check['independent_control_gap']: raise EvidenceError('new control gap mismatch')
            child_ref=write_new(directory/(variant+'.json.gz'),payload(child),compressed=True)
            check=validate_control(parent,child,variant,gap)
            write_new(directory/(variant+'.validation.json'),{'parent_ref':parent_ref,'child_ref':child_ref,**check})
            result[variant]=child
    variant=trial['variant'];path=directory/(variant+'.json.gz');data=path.read_bytes()
    return result[variant],{'path':str(path),'sha256':sha(data),'content_sha256':sha(gzip.decompress(data)),'size_bytes':len(data)}


def execute_trial(root, out, trial, config, workload, input_ref, context, auth):
    directory=out/'trials'/trial['trial_id']
    recovery=(directory/'primary.reserved.json').exists()
    if (directory/'result.json').exists(): raise EvidenceError('completed trial cannot execute again')
    if recovery:
        if trial['trial_id']!=auth['allowed_recovery_trial']: raise EvidenceError('unapproved uncertain invocation')
        old=load(directory/'manifest.json')
        if old['input_ref']!=input_ref or old['method']!=trial['method'] or old['workload_id']!=trial['workload_id']:
            raise EvidenceError('recovery input/method identity differs')
        if {p.name for p in directory.iterdir()}!={'manifest.json','primary.reserved.json'}:
            raise EvidenceError('recovery exception only covers the exact previously observed unknown state')
        primary_dir=directory/'recovery_001'
    else:
        if directory.exists(): raise EvidenceError('unexpected incomplete/unreserved trial directory')
        primary_dir=directory
    check_budget(ledger(out),'PRIMARY',recovery=recovery)
    manifest={**trial,'run_id':trial['trial_id']+':LOCAL_SIMULATION_V1','mode':context['mode'],
              'timestamp_utc':utc(),'git_commit':context['git_commit'],'source_sha256':context['source_sha256'],
              'original_frozen_source_sha256':context['original_frozen_source_sha256'],
              'config_sha256':sha(canonical_bytes(config)),'workload_sha256':input_ref['content_sha256'],
              'input_ref':input_ref,'host':platform.node(),'command':context['command'],'process_id':os.getpid(),
              'dirty_status_at_segment_start':context['dirty_status'],'segment_context':context['segment_context'],
              'one_time_recovery':recovery,'recovery_authorization_sha256':context['recovery_authorization_sha256']}
    if recovery:
        manifest['original_reservation_sha256']=sha((directory/'primary.reserved.json').read_bytes())
        manifest['original_manifest_sha256']=sha((directory/'manifest.json').read_bytes())
        manifest['extra_independent_sample']=False
    write_new(primary_dir/'manifest.json',manifest)
    write_new(primary_dir/'primary.reserved.json',{'timestamp_utc':utc(),'no_retry':True,'purpose':'RECOVERY_RECOMPUTATION' if recovery else 'PRIMARY_EXECUTION'})
    start=utc();tick=time.monotonic()
    primary=compact(simulate(workload,trial['method'],compact_decisions=True))
    primary_ref=write_new(primary_dir/'primary.trace.json.gz',primary,compressed=True)
    write_new(primary_dir/'primary.returned.json',{'started_at_utc':start,'ended_at_utc':utc(),'wall_seconds':time.monotonic()-tick,'function_returned':True,'trace_ref':primary_ref})
    checked=validate_physical_payload(workload,primary)
    write_new(primary_dir/'primary.validation.json',checked)
    if checked['status']!='PASS': raise EvidenceError('independent primary validation failed')
    check_budget(ledger(out),'REPLAY')
    write_new(directory/'replay.reserved.json',{'timestamp_utc':utc(),'no_retry':True,'same_sample_not_new_seed':True})
    start=utc();tick=time.monotonic()
    replay=compact(simulate(workload,trial['method'],compact_decisions=True))
    replay_ref=write_new(directory/'replay.trace.json.gz',replay,compressed=True)
    replay_check=validate_physical_payload(workload,replay)
    exact=primary_ref['content_sha256']==replay_ref['content_sha256']
    write_new(directory/'replay.validation.json',{'started_at_utc':start,'ended_at_utc':utc(),'wall_seconds':time.monotonic()-tick,
              'function_returned':True,'physical':replay_check,'exact_primary_match':exact,'trace_ref':replay_ref})
    if replay_check['status']!='PASS' or not exact: raise EvidenceError('replay validation/match failed')
    metrics=checked['metrics'];services=metrics['services'];variant=trial['variant']
    def dmr(group):
        selected=[s for s in services if s['group']==group]
        return str(F(sum(s['missed'] for s in selected),len(selected))) if selected else None
    row={**trial,'run_id':manifest['run_id'],'input_ref':input_ref,'primary_ref':primary_ref,'replay_ref':replay_ref,
         'validity':'VALID','exact_replay':True,'groups':metrics['groups'],'makespan':metrics['makespan'],
         'H_dmr_exact':dmr('H'),'L_dmr_exact':dmr('L'),'one_time_recovery':recovery,
         'executed_source_sha256':context['source_sha256'],'segment_context':context['segment_context']}
    if variant=='MAIN' and trial['method']=='B2':
        row['pressure_exact']=str(busy_pressure(workload,primary['executions'],50*config['period_ms']))
        row['positive_assigned_busy_wait']=positive_busy_wait(workload,primary)
        natural=feasibility(workload)
        row['natural_infeasibility']={g:sum(s.group==g and natural[s.id]['classification']=='CERTIFIED_NATURALLY_INFEASIBLE' for s in workload.services) for g in ('H','L')}
        write_new(directory/'feasibility.json',natural)
    elif variant!='MAIN':
        row['control_witness']=controls_witness(workload,primary['executions'],{'H'} if variant=='H_ISOLATED' else {'H','L'})
    write_new(directory/'result.json',row)
    return row


def resume(root, *, end_trial, seconds):
    if type(end_trial) is not int or not 0<end_trial<=2520 or end_trial%70 or not 0<seconds<=900:
        raise EvidenceError('segment must target an original config boundary with <=900-second admission window')
    out=root/'results/calibration/local_001';auth=load(root/AUTHORIZATION)
    lock_path=out/'foreground.lock'
    with lock_path.open('a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        preflight=inspect_resume(root)
        if preflight['errors']: return preflight
        matrix=load(root/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json')
        rows=complete_prefix(out,matrix['trials'],root)
        if len(rows)>=end_trial: return {'status':'ALREADY_AT_REQUESTED_BOUNDARY','valid_trials':len(rows),'new_primary_calls':0,'new_replay_calls':0}
        # There may only be the one explicitly authorized unknown trial, never
        # an unrelated incomplete call, later result or unregistered slot.
        pending=[p for p in (out/'trials').iterdir() if not (p/'result.json').exists()]
        if pending and (len(pending)!=1 or pending[0].name!=auth['allowed_recovery_trial']):
            raise EvidenceError('another incomplete slot blocks continuation')
        batch_root=out/'segments';batch_root.mkdir(exist_ok=True)
        number=len(list(batch_root.glob('segment_*')))+1
        segment=batch_root/f'segment_{number:03d}';segment.mkdir(exist_ok=False)
        original=load(out/'context.json')
        context={'mode':'LOCAL_RESEARCH_SIMULATION','started_at_utc':utc(),'pid':os.getpid(),'host':platform.node(),
                 'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
                 'source_sha256':preflight['source_sha256'],'original_frozen_source_sha256':original['source_sha256'],
                 'recovery_authorization_sha256':preflight['recovery_authorization_sha256'],
                 'command':list(sys.orig_argv),
                 'dirty_status':subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True),
                 'segment_context':str((segment/'context.json').relative_to(root)),
                 'previous_complete_trials':len(rows),'target_trial':end_trial,'admission_window_seconds':seconds}
        write_new(segment/'context.json',context);write_new(segment/'preflight.json',preflight)
        start=time.monotonic();new_rows=[];generator=Generator(root);permit=LocalPermit(matrix)
        config_map={c['config_id']:c for c in matrix['configs']};cache={}
        try:
            for trial in matrix['trials'][len(rows):end_trial]:
                if new_rows and time.monotonic()-start>=seconds: break
                if relevant_source_hash(root)!=context['source_sha256']: raise EvidenceError('source changed during segment')
                key=(trial['config_id'],trial['seed_index'],trial['variant'])
                if key not in cache:
                    cache[key]=inputs_for(root,out,config_map[trial['config_id']],trial,generator,permit)
                workload,ref=cache[key]
                row=execute_trial(root,out,trial,config_map[trial['config_id']],workload,ref,context,auth)
                rows.append(row);new_rows.append(row)
                print(json.dumps({'segment':segment.name,'completed_trial':row['trial_id'],'valid_total':len(rows),'new_primary_calls':len(new_rows),
                                  'new_replays':len(new_rows),'elapsed_seconds':round(time.monotonic()-start,2)}),flush=True)
            counts=ledger(out)
            check_budget(counts,'REPLAY') if counts['replay_reservations']<2520 else None
            summary={'status':'PAUSED_AT_COMPLETE_TRIAL_BOUNDARY','whole_campaign_complete':len(rows)==2520,
                     'valid_trials':len(rows),'registered_replays_complete':len(rows),'expected_trials':2520,
                     'new_primary_calls':len(new_rows),'new_replay_calls':len(new_rows),
                     'one_time_recovery_total':counts['recovery_primary_reservations'],
                     'actual_primary_invocations':{'minimum':len(rows),'maximum':len(rows)+counts['recovery_primary_reservations']},
                     'total_engine_invocations':{'minimum':2*len(rows),'maximum':2*len(rows)+counts['recovery_primary_reservations']},
                     'reservation_counts':counts,'generated_inputs':len(list((out/'inputs').glob('*/*/MAIN.json.gz')))*3,
                     'remaining_unique_trials':2520-len(rows),'elapsed_seconds':time.monotonic()-start,
                     'target_config_boundary_reached':len(rows)>=end_trial,'updated_at_utc':utc(),
                     'source_sha256':context['source_sha256'],'original_frozen_source_sha256':original['source_sha256'],
                     'p2_status':'BLOCKED','mapping_classification':'NOT_EVALUATED','validation_unlocked':False,'formal_unlocked':False}
            write_new(segment/'summary.json',summary);write_new(segment/'new_results.json',new_rows)
            return summary
        except BaseException as exc:
            write_new(segment/'failure.json',{'error':str(exc),'type':type(exc).__name__,'traceback':traceback.format_exc(),
                       'last_complete_trial_count':len(rows),'new_complete_trials':len(new_rows),'timestamp_utc':utc(),'automatic_retry':False})
            raise

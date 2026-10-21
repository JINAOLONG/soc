"""Verify, summarize and archive finished foreground calls; never run a simulator."""
from collections import defaultdict
from datetime import datetime,timezone
from fractions import Fraction
import csv,gzip,hashlib,io,json,subprocess,tarfile
from pathlib import Path

from soc.p2.adapter import validate_physical_payload
from soc.p2.generation import parse_payload
from soc.p2.local_input_validation import validate_main,validate_control
from soc.p2.local_resume import frozen_core,ledger,read_ref
from soc.validation.governance import relevant_source_hash

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'results/calibration/local_001'
HERE=Path(__file__).resolve().parent

def sha(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_bytes())
def dump(name,value):
    with (HERE/name).open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')

def main():
    commands=[load(p) for p in [HERE/'command.json',*sorted(HERE.glob('process_*/command.json'))]]
    if not commands or any(c['exit_code']!=0 for c in commands):raise RuntimeError('foreground process did not exit successfully')
    segments=sorted((OUT/'segments').glob('segment_*'))
    summaries=[load(p/'summary.json') for p in segments]
    if any(s['status']!='PAUSED_AT_COMPLETE_TRIAL_BOUNDARY' for s in summaries):raise RuntimeError('incomplete segment')
    last=summaries[-1]
    if last['valid_trials']!=420:raise RuntimeError('predetermined current milestone420 not complete')
    old=load(OUT/'context.json');core=frozen_core(ROOT,old)
    if relevant_source_hash(ROOT)!=last['source_sha256']:raise RuntimeError('source changed')
    prior=load(ROOT/'reports/P2_calibration/local_001/continuation_001/cumulative_raw_manifest.json')['files']
    original={r['path']:r for r in prior}
    for name,ref in original.items():
        data=(ROOT/name).read_bytes()
        if len(data)!=ref['size_bytes'] or sha(data)!=ref['sha256']:raise RuntimeError('old evidence overwritten: '+name)
    matrix=load(ROOT/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json');configs={c['config_id']:c for c in matrix['configs']}
    rows=[];checks=[];workloads={}
    for trial in matrix['trials'][:420]:
        directory=OUT/'trials'/trial['trial_id'];r=load(directory/'result.json')
        if r['trial_id']!=trial['trial_id'] or r['validity']!='VALID' or not r['exact_replay']:raise RuntimeError('invalid result')
        for key in ('config_id','calibration_seed','variant','method','workload_id','partition'):
            if r[key]!=trial[key]:raise RuntimeError('roster mismatch')
        rows.append(r)
        if trial['execution_order']<=350:continue
        path=r['input_ref']['path']
        if path not in workloads:workloads[path]=parse_payload(read_ref(r['input_ref'],ROOT))
        w=workloads[path];a=read_ref(r['primary_ref'],ROOT);b=read_ref(r['replay_ref'],ROOT)
        if r['primary_ref']['content_sha256']!=r['replay_ref']['content_sha256']:raise RuntimeError('primary/replay exact byte hashes differ')
        va=validate_physical_payload(w,a);vb=validate_physical_payload(w,b)
        if va['status']!='PASS' or vb['status']!='PASS' or a!=b:raise RuntimeError('new physical/replay verification failed')
        if va['metrics']['groups']!=r['groups']:raise RuntimeError('new result metrics differ')
        primary_dir=Path(r['primary_ref']['path']).parent
        if load(primary_dir/'primary.validation.json')!=va:raise RuntimeError('stored primary validation differs')
        if not load(primary_dir/'primary.returned.json')['function_returned']:raise RuntimeError('missing actual return')
        if load(directory/'replay.validation.json')['physical']!=vb:raise RuntimeError('stored replay validation differs')
        manifest=load(primary_dir/'manifest.json')
        if manifest['source_sha256']!=last['source_sha256'] or manifest['original_frozen_source_sha256']!=old['source_sha256']:raise RuntimeError('new context/source binding mismatch')
        checks.append(dict(trial_id=r['trial_id'],primary_physical='PASS',replay_physical='PASS',exact_replay='PASS',metrics='MATCH',recovery=r['one_time_recovery']))
    if len(list((OUT/'trials').glob('*/result.json')))!=420:raise RuntimeError('unexpected result outside prefix')
    if len(checks)!=70 or any(r['recovery'] for r in checks):raise RuntimeError('unexpected additional calls')
    counts=ledger(OUT)
    if counts!={'original_primary_reservations':420,'recovery_primary_reservations':1,'replay_reservations':420}:raise RuntimeError('budget ledger differs')
    dump('new_trial_checks.json',checks)
    dump('all_completed_results.json',rows)
    # Recheck only newly materialized MAIN births and their control inheritance.
    new_input_checks=[]
    for p in sorted((OUT/'inputs').glob('*/*/MAIN.json.gz')):
        if str(p.relative_to(ROOT)) in original:continue
        reserved=load(p.parent/'generation_reserved.json');config=reserved['config'];seed=reserved['seed']
        if config!=configs[config['config_id']] or int(seed) not in matrix['registered_seeds']:raise RuntimeError('new seed/config mismatch')
        parent=parse_payload(json.loads(gzip.decompress(p.read_bytes())))
        birth=validate_main(ROOT,config,seed,parent)
        for variant in ('H_ISOLATED','LOW_COMPETITION'):
            child=parse_payload(json.loads(gzip.decompress((p.parent/(variant+'.json.gz')).read_bytes())))
            validate_control(parent,child,variant,birth['independent_control_gap'])
        new_input_checks.append(dict(config_id=config['config_id'],seed=seed,variants=3,status='PASS'))
    if len(new_input_checks)!=10:raise RuntimeError('expected exactly10 new registered parent groups')
    dump('new_input_checks.json',new_input_checks)
    config_rows=defaultdict(list)
    for r in rows:config_rows[r['config_id']].append(r)
    if len(config_rows)!=6 or any(len(v)!=70 for v in config_rows.values()):raise RuntimeError('six complete configs required')
    for cid,cells in config_rows.items():
        for seed in matrix['registered_seeds']:
            main=[r for r in cells if r['variant']=='MAIN' and r['calibration_seed']==seed]
            if len(main)!=5 or {r['method'] for r in main}!={'B1','B2','B3','B4','B5'}:raise RuntimeError('baseline method fairness roster mismatch')
            if len({r['input_ref']['content_sha256'] for r in main})!=1:raise RuntimeError('same-seed baseline inputs differ')
            if any(r['groups']['H']['count']!=50 or r['groups']['L']['count']!=50 for r in main):raise RuntimeError('MAIN group count mismatch')
    csvdata=io.StringIO();writer=csv.writer(csvdata)
    writer.writerow(['config_id','variant','method','completed_seeds','H_DMR_seed_mean','L_DMR_seed_mean','H_P95_ms_seed_mean','L_P95_ms_seed_mean'])
    baseline_rows=[]
    for cid,cells in sorted(config_rows.items()):
        for variant,methods in [('H_ISOLATED',['B2']),('LOW_COMPETITION',['B2']),('MAIN',['B1','B2','B3','B4','B5'])]:
            for method in methods:
                c=[r for r in cells if r['variant']==variant and r['method']==method]
                if len(c)!=10 or {r['calibration_seed'] for r in c}!=set(matrix['registered_seeds']):raise RuntimeError('seed/method product incomplete')
                def mean(group,metric):
                    values=[r['groups'][group][metric] for r in c]
                    return sum(values)/10 if all(x is not None for x in values) else 'NOT_APPLICABLE'
                values=[mean(g,m) for g,m in [('H','dmr'),('L','dmr'),('H','p95'),('L','p95')]]
                writer.writerow([cid,variant,method,10,*values])
                if variant=='MAIN':baseline_rows.append(dict(config_id=cid,method=method,H_DMR=values[0],L_DMR=values[1],H_P95_ms=values[2],L_P95_ms=values[3]))
    (HERE/'baseline_summary.csv').write_text(csvdata.getvalue());dump('baseline_summary.json',baseline_rows)
    # Archive all additions; the original interrupted-campaign archives remain
    # the immutable base; continuation001 deltas are also required. No raw working file is removed.
    current={str(p.relative_to(ROOT)):p for p in OUT.rglob('*') if p.is_file()}
    added={name:p for name,p in current.items() if name not in original}
    buckets=defaultdict(list)
    for name,p in sorted(added.items()):
        parts=p.relative_to(OUT).parts
        if parts[0]=='inputs':bucket=parts[1]
        elif parts[0]=='trials':bucket=load(OUT/'trials'/parts[1]/'manifest.json')['config_id']
        else:bucket='segment_metadata'
        buckets[bucket].append(p)
    archives=[]
    for bucket,paths in sorted(buckets.items()):
        target=HERE/(bucket+'.delta.tar.gz');expected={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths}
        with tarfile.open(target,'w:gz',compresslevel=6) as tar:
            for p in paths:tar.add(p,arcname=str(p.relative_to(ROOT)),recursive=False)
        with tarfile.open(target,'r:gz') as tar:
            actual={m.name:sha(tar.extractfile(m).read()) for m in tar.getmembers() if m.isfile()}
        if actual!=expected or target.stat().st_size>=100_000_000:raise RuntimeError('delta archive mismatch or oversize')
        archives.append(dict(path=str(target.relative_to(ROOT)),sha256=sha(target.read_bytes()),size_bytes=target.stat().st_size,raw_files=len(paths),roundtrip='PASS'))
    dump('delta_archive_index.json',archives)
    dump('cumulative_raw_manifest.json',{'previous_cumulative_manifest':'reports/P2_calibration/local_001/continuation_001/cumulative_raw_manifest.json','prior_delta_indexes':['reports/P2_calibration/local_001/continuation_001/delta_archive_index.json'],'current_delta_index':'reports/P2_calibration/local_001/continuation_002/delta_archive_index.json','base_archive_index':'reports/P2_calibration/local_001/interruption_001/archive_index.json','base_metadata_archive':'reports/P2_calibration/local_001/interruption_001/metadata_archive.json','files':[dict(path=name,size_bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for name,p in sorted(current.items())]})
    dump('closure_summary.json',{'closed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'COMPLETED_PREDECLARED_FOREGROUND_MILESTONE','last_completed_trial':'proposal-v2-t0420','valid_primary_results':420,'valid_registered_replays':420,'new_primary_calls':70,'new_replays':70,'recovery_recomputations':0,'new_independent_samples_due_to_recovery':0,'primary_invocations':{'minimum':420,'maximum':421},'engine_invocations':{'minimum':840,'maximum':841},'engine_call_ceiling':5041,'unique_result_roster_size':2520,'remaining_unique_trials':2100,'total_generated_inputs':180,'new_inputs':len(new_input_checks)*3,'complete_configs':6,'core_identity':core,'resumed_source_sha256':last['source_sha256'],'original_unknown_call_status':'UNKNOWN_RETAINED; trial247 result supplied by RECOVERY_001','foreground_process_exit_codes':[c['exit_code'] for c in commands],'whole_campaign_status':'PAUSED_INCOMPLETE','p2_status':'BLOCKED','mapping_classification':'NOT_EVALUATED','global_qualification':'NOT_EVALUATED_INCOMPLETE_ROSTER','no_background_execution_requested':True,'new_seeds_generated':False,'non_calibration_outcomes_accessed':False,'validation_unlocked':False,'formal_unlocked':False,'raw_files':len(current),'new_raw_files':len(added),'old_files_preserved':len(original)})
    print('Closure PASS:',len(rows),'results;',len(checks),'new pairs;',len(added),'new raw files; all original files unchanged')

if __name__=='__main__':main()

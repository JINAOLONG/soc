"""Retain a live local simulation's results; never invoke a scientific engine."""
from collections import defaultdict
from datetime import datetime,timezone
import csv,gzip,hashlib,io,json,os,subprocess,tarfile,time,traceback
from pathlib import Path
ROOT=Path('/workspace/soc')
OUT=ROOT/'results/calibration/local_001'
REPORT=ROOT/'reports/P2_calibration/local_001'

def utc(): return datetime.now(timezone.utc).isoformat()
def digest(data): return hashlib.sha256(data).hexdigest()
def dump(p,data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def git(args):
    p=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True)
    return dict(argv=['git',*args],exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
def sha(p): return digest(p.read_bytes())

def report_rows(rows,target):
    groups=defaultdict(list)
    for row in rows:
        if row['variant']=='MAIN': groups[(row['config_id'],row['method'])].append(row)
    buf=io.StringIO();w=csv.writer(buf)
    w.writerow(['config_id','method','completed_seeds','H_DMR_seed_mean','L_DMR_seed_mean','H_P95_ms_seed_mean','L_P95_ms_seed_mean'])
    for (config,method),cells in sorted(groups.items()):
        w.writerow([config,method,len(cells)] + [sum(c['groups'][g][m] for c in cells)/len(cells) for g,m in [('H','dmr'),('L','dmr'),('H','p95'),('L','p95')]])
    target.write_text(buf.getvalue())

def check_rows(rows):
    roster=json.loads((ROOT/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json').read_text())['trials']
    assert [r['trial_id'] for r in rows]==[r['trial_id'] for r in roster[:len(rows)]]
    checked={}
    for row,expected in zip(rows,roster):
        for name in ('trial_id','config_id','calibration_seed','partition','variant','method','workload_id'):
            assert row[name]==expected[name],name
        assert row['validity']=='VALID' and row['exact_replay'] is True
        for name in ('input_ref','primary_ref','replay_ref'):
            ref=row[name];p=Path(ref['path']);assert p.is_relative_to(OUT)
            if str(p) not in checked:
                data=p.read_bytes();assert digest(data)==ref['sha256']
                assert digest(gzip.decompress(data))==ref['content_sha256']
                checked[str(p)]={'path':str(p.relative_to(ROOT)),'sha256':digest(data),'size_bytes':len(data)}
        assert row['primary_ref']['content_sha256']==row['replay_ref']['content_sha256']
    return list(checked.values())

def snapshot_first_config():
    files=[OUT/'trials'/f'proposal-v2-t{i:04d}'/'result.json' for i in range(1,71)]
    if not all(p.is_file() for p in files): return False
    rows=[json.loads(p.read_text()) for p in files]
    checked=check_rows(rows);config=rows[0]['config_id']
    archive=REPORT/'first_config_raw.tar.gz'
    with tarfile.open(archive,'w:gz',compresslevel=6) as tar:
        tar.add(OUT/'inputs'/config,arcname=str((OUT/'inputs'/config).relative_to(ROOT)))
        for p in files: tar.add(p.parent,arcname=str(p.parent.relative_to(ROOT)))
    dump(REPORT/'first_config_results.json',rows)
    report_rows(rows,REPORT/'first_config_summary.csv')
    dump(REPORT/'first_config_snapshot.json',dict(snapshot_at_utc=utc(),scope='First fixed config, complete 10-seed results, not a full calibration conclusion',config_id=config,primary_trials=70,replays=70,verified_raw_references=checked,archive_sha256=sha(archive),archive_size_bytes=archive.stat().st_size,full_campaign_status='RUNNING'))
    return True

def finalize():
    command=json.loads((REPORT/'command.json').read_text())
    failure=OUT/'failure.json';summary=OUT/'summary.json'
    rows=[json.loads(p.read_text()) for p in sorted((OUT/'trials').glob('*/result.json'))]
    checked=check_rows(rows)
    state=json.loads(summary.read_text()) if summary.exists() else json.loads(failure.read_text())
    complete=command['exit_code']==0 and state.get('execution_completion')=='COMPLETE' and len(rows)==2520
    if complete:
        assert len({r['trial_id'] for r in rows})==2520
        assert len(list((OUT/'inputs').glob('*/*/*.validation.json')))==1080
        assert len(list((OUT/'trials').glob('*/primary.reserved.json')))==2520
        assert len(list((OUT/'trials').glob('*/replay.reserved.json')))==2520
    report_rows(rows,REPORT/'baseline_summary.csv')
    files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='owner.lock']
    raw_manifest=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'size_bytes':p.stat().st_size} for p in sorted(files)]
    dump(REPORT/'raw_artifact_manifest.json',dict(scope='Actual local simulation files before archival; extract archives to restore these paths',files=raw_manifest))
    config_trials=defaultdict(list)
    for p in sorted((OUT/'trials').glob('*')):
        manifest=p/'manifest.json'
        if manifest.exists(): config_trials[json.loads(manifest.read_text())['config_id']].append(p)
    archive_dir=OUT/'archives';archive_dir.mkdir(exist_ok=False)
    archives=[]
    for config,dirs in sorted(config_trials.items()):
        target=archive_dir/(config+'.tar.gz')
        included=[p for p in sorted((OUT/'inputs'/config).rglob('*')) if p.is_file()]
        included += [p for d in dirs for p in sorted(d.rglob('*')) if p.is_file()]
        expected={str(p.relative_to(ROOT)):sha(p) for p in included}
        with tarfile.open(target,'w:gz',compresslevel=6) as tar:
            for p in included: tar.add(p,arcname=str(p.relative_to(ROOT)),recursive=False)
        with tarfile.open(target,'r:gz') as tar:
            actual={m.name:digest(tar.extractfile(m).read()) for m in tar.getmembers() if m.isfile()}
        assert actual==expected,'Archive byte mismatch'
        archives.append({'config_id':config,'path':str(target.relative_to(ROOT)),'sha256':sha(target),'size_bytes':target.stat().st_size,'raw_file_count':len(expected),'roundtrip_hash_check':'PASS'})
    dump(OUT/'archive_index.json',{'archives':archives,'raw_manifest':'reports/P2_calibration/local_001/raw_artifact_manifest.json'})
    qpath=OUT/'qualification.json';q=json.loads(qpath.read_text()) if qpath.exists() else None
    reason=state.get('reason',state.get('error','NOT_COMPLETE'))
    body=['# Local CALIBRATION simulation results','',f'Execution: {"COMPLETE" if complete else "FAILED_OR_INCOMPLETE"}; actual CLI exit {command["exit_code"]}.',f'Validated primary trials: {len(rows)}/2520. Registered replay calls: {state.get("registered_replays",state.get("replay_calls","UNKNOWN"))}.',f'Reason: {reason}. P2 remains BLOCKED; no later stage was started.','',
          'This is single-host virtual-time simulation under the user\'s later scope instruction. V3 production authority/lease/publication compliance is not claimed. Synthetic costs are not hardware measurements. Registered seeds, model, methods and thresholds are unchanged. No automatic retry or new seed occurred.','',
          'baseline_summary.csv contains per-config/method seed means. A mean of seed P95 values is labelled as such; it is not a pooled P95 or a confidence interval. All fixed A/B configs and all valid unfavorable results are retained. Missing qualification cannot be relabelled as supported mapping opportunity.','']
    if q:
        body+=['|Config|Eligible|Pressure mean|H DMR mean|L DMR mean|','|---|---|---:|---:|---:|']
        for r in q['configs']:
            body.append(f'|{r["config"]["config_id"]}|{r["eligible"]}|{r["mean_pressure"]:.6f}|{r["mean_H_dmr"]:.6f}|{r["mean_L_dmr"]:.6f}|')
    body+=['','Mapping diagnostic and M2 have not been executed. If all18 conditions are not selected, do not compute them or claim a scientific mechanism conclusion. If selected, diagnostics remain a separate pending calculation; execution COMPLETE alone is not P2 PASS.','',
           'Raw input, exact sidecars, reservations, traces, independent validations and run manifests are retained in per-config archives under results/calibration/local_001/archives. Each archive was extracted in-memory and every member SHA256 compared with the originals. No raw file was deleted locally. To restore tracked raw paths from a fresh clone, run tar -xzf <archive> from the repository root for each archive. The archive index and raw manifest bind the bytes.','']
    (REPORT/'README.md').write_text('\n'.join(body))
    status=ROOT/'STATUS.md'
    assert sha(status)==START_STATUS_SHA, 'Status changed in another task; do not overwrite it'
    values=dict(line.split('=',1) for line in status.read_text().splitlines() if '=' in line)
    values.update({
        'CURRENT_STAGE':'P2_LOCAL_SIMULATION_RESULTS',
        'SCIENTIFIC_WORKLOADS_GENERATED':str(state.get('workloads_generated',json.loads((OUT/'progress.json').read_text()).get('generated_inputs','UNKNOWN'))),
        'SCIENTIFIC_WORKLOADS_RUN':str(state.get('primary_runs',state.get('primary_calls','UNKNOWN'))),
        'P2_PREFLIGHT_STATUS':'READY_FOR_LOCAL_SIMULATION','P2_STATUS':'BLOCKED','STOP':'YES',
        'NEXT_SAFE_ACTION':'Review actual fixed-roster qualification and local simulation evidence; do not tune or progress automatically',
        'RESULT_PATHS':'results/calibration/local_001;reports/P2_calibration/local_001;reports/P2_engineering/local_simulation_001',
        'LOCAL_SIMULATION_EXECUTION':'COMPLETE' if complete else 'FAILED_OR_INCOMPLETE',
        'LOCAL_SIMULATION_EXIT_CODE':str(command['exit_code']),
        'LOCAL_SIMULATION_VALID_TRIALS':str(len(rows)),
        'LOCAL_SIMULATION_REGISTERED_REPLAYS':str(state.get('registered_replays',state.get('replay_calls','UNKNOWN'))),
        'LOCAL_SIMULATION_SELECTION_STATUS':str(state.get('selection_status','NOT_EVALUATED')),
        'LOCAL_SIMULATION_MAPPING_CLASSIFICATION':'NOT_EVALUATED'})
    status.write_text('\n'.join(k+'='+v for k,v in values.items())+'\n')
    # Only the intended results/status paths are added; running source/config
    # changes from a different user task are never staged here.
    files_to_add=['STATUS.md',str(REPORT.relative_to(ROOT)),str(archive_dir.relative_to(ROOT)),str((OUT/'archive_index.json').relative_to(ROOT))]
    files_to_add += [str(p.relative_to(ROOT)) for p in OUT.glob('*.json')]
    staged=git(['diff','--cached','--name-only'])
    assert staged['exit_code']==0 and not staged['stdout'], 'Pre-existing staged work; do not commit another task'
    results=[]
    for args in [['add','--',*files_to_add],['commit','--quiet','-m','Preserve actual fixed-roster local CALIBRATION simulation results'],['push','origin','HEAD:work']]:
        r=git(args);results.append(r)
        if r['exit_code']:break
    result_head=git(['rev-parse','HEAD']);remote=git(['ls-remote','origin','refs/heads/work'])
    dump(REPORT/'publication_receipt.json',{'observed_at_utc':utc(),'commands':results,'result_commit':result_head,'remote_readback':remote,'raw_archive_integrity':'PASS','complete':complete,'scientific_trials':len(rows)})
    # Receipt publication is a separate normal history-preserving commit.
    for args in [['add','--',str((REPORT/'publication_receipt.json').relative_to(ROOT))],['commit','--quiet','-m','Record publication of local CALIBRATION result archives'],['push','origin','HEAD:work']]:
        r=git(args);print(json.dumps(r),flush=True)
        if r['exit_code']:break
    print(json.dumps({'finalization':'COMPLETE','results_complete':complete,'valid_trials':len(rows),'head':git(['rev-parse','HEAD'])}),flush=True)

if __name__=='__main__':
    START_STATUS_SHA=sha(ROOT/'STATUS.md')
    try:
        snap=(REPORT/'first_config_snapshot.json').exists()
        while not (REPORT/'command.json').exists():
            if not snap:snap=snapshot_first_config()
            time.sleep(10)
        finalize()
    except BaseException:
        (REPORT/'finalization_failure.txt').write_text(traceback.format_exc())
        raise

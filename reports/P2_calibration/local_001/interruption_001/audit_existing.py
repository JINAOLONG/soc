"""Read and independently validate existing results; never invoke an engine or generator."""
from collections import Counter,defaultdict
from datetime import datetime,timezone
from fractions import Fraction
import csv,gzip,hashlib,io,json,subprocess,tarfile,traceback
from pathlib import Path

from soc.model.schema import canonical_bytes
from soc.p2.adapter import validate_physical_payload
from soc.p2.generation import parse_payload
from soc.p2.local_input_validation import validate_main,validate_control
from soc.p2.qualification import classify_config
from soc.validation.governance import relevant_source_hash

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'results/calibration/local_001'
HERE=Path(__file__).resolve().parent

def digest(data):return hashlib.sha256(data).hexdigest()
def dump(name,value):
    with (HERE/name).open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def load(path):return json.loads(path.read_bytes())
def capture(name,argv):
    p=subprocess.run(argv,cwd=ROOT,capture_output=True)
    (HERE/(name+'.stdout.txt')).write_bytes(p.stdout);(HERE/(name+'.stderr.txt')).write_bytes(p.stderr)
    return dict(argv=argv,exit_code=p.returncode,stdout_file=name+'.stdout.txt',stderr_file=name+'.stderr.txt')

def main():
    context=load(OUT/'context.json');matrix=load(ROOT/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json')
    assert context['source_sha256']==relevant_source_hash(ROOT),'scientific source identity changed'
    assert digest((ROOT/'configs/seed_partitions.json').read_bytes())==context['seed_metadata_sha256']
    assert digest((ROOT/'docs/P2_design/v2/P2_trial_matrix_draft_v2.json').read_bytes())==context['matrix_sha256']
    assert digest((ROOT/'docs/P2_design/accepted/local_simulation_scope_001.json').read_bytes())==context['scope_sha256']
    configs={c['config_id']:c for c in matrix['configs']}
    commands=[]
    for name,argv in [('head',['git','rev-parse','HEAD']),('branch',['git','branch','--show-current']),('origin',['git','remote','get-url','origin']),('remote',['git','ls-remote','origin','refs/heads/work']),('status',['git','status','--porcelain']),('original_process',['pgrep','-af',r'^(/workspace/soc/\.venv/bin/python|\.venv/bin/python|python[0-9.]*) (-u )?-B (scripts/run_local_calibration.py|/tmp/soc_finalize_local.py)$'])]:
        commands.append(capture(name,argv))
    assert commands[-1]['exit_code']==1,'matching simulation/report process still exists; stop audit'
    for stage in ('p0','p1'):
        commands.append(capture(stage,[str(ROOT/'.venv/bin/python'),'-B','scripts/run_pipeline.py','--stage',stage,'--check-only']))
        assert commands[-1]['exit_code']==0,'correctness audit blocked'
    dump('commands.json',commands)
    inputs={};input_checks=[]
    for main_file in sorted((OUT/'inputs').glob('*/*/MAIN.json.gz')):
        directory=main_file.parent
        reservation=load(directory/'generation_reserved.json')
        config=reservation['config'];seed=reservation['seed']
        assert config==configs[config['config_id']]
        assert int(seed) in matrix['registered_seeds'] and reservation['partition']=='CALIBRATION'
        parent=parse_payload(json.loads(gzip.decompress(main_file.read_bytes())))
        checked=validate_main(ROOT,config,seed,parent)
        inputs[str(main_file)]=parent
        for variant in ('H_ISOLATED','LOW_COMPETITION'):
            path=directory/(variant+'.json.gz')
            child=parse_payload(json.loads(gzip.decompress(path.read_bytes())))
            validate_control(parent,child,variant,checked['independent_control_gap'])
            inputs[str(path)]=child
        input_checks.append(dict(config_id=config['config_id'],seed=seed,status='PASS',variants=3))
    dump('independent_input_checks.json',input_checks)
    rows=[];checks=[];all_dirs=sorted((OUT/'trials').glob('*'))
    unknown=[]
    for index,directory in enumerate(all_dirs):
        manifest=load(directory/'manifest.json');expected=matrix['trials'][index]
        assert manifest['trial_id']==expected['trial_id']
        for key,value in expected.items():
            if key not in {'workload_sha256','command'}:assert manifest[key]==value,(directory,key)
        assert manifest['source_sha256']==context['source_sha256']
        assert manifest['git_commit']==context['git_commit']
        assert manifest['config_sha256']==digest(canonical_bytes(configs[manifest['config_id']]))
        if not (directory/'result.json').exists():
            unknown.append(dict(trial_id=manifest['trial_id'],config_id=manifest['config_id'],seed=manifest['calibration_seed'],variant=manifest['variant'],method=manifest['method'],files=sorted(p.name for p in directory.iterdir()),classification='RESERVED_EXECUTION_STATE_UNKNOWN',reexecution_allowed=False))
            continue
        row=load(directory/'result.json');assert not unknown,'completed rows are not a contiguous prefix'
        assert row['trial_id']==expected['trial_id'] and row['validity']=='VALID' and row['exact_replay']
        for key in ('input_ref','primary_ref','replay_ref'):
            ref=row[key];path=Path(ref['path']);assert path.is_relative_to(OUT)
            data=path.read_bytes();assert digest(data)==ref['sha256'] and len(data)==ref['size_bytes']
            assert digest(gzip.decompress(data))==ref['content_sha256']
        w=inputs[row['input_ref']['path']]
        primary=json.loads(gzip.decompress(Path(row['primary_ref']['path']).read_bytes()))
        replay=json.loads(gzip.decompress(Path(row['replay_ref']['path']).read_bytes()))
        a=validate_physical_payload(w,primary);b=validate_physical_payload(w,replay)
        assert a['status']==b['status']=='PASS'
        assert a['metrics']['groups']==row['groups']
        assert canonical_bytes(primary)==canonical_bytes(replay)
        assert load(directory/'primary.validation.json')==a
        stored_replay=load(directory/'replay.validation.json')
        assert stored_replay['physical']==b and stored_replay['exact_primary_match'] is True
        assert load(directory/'primary.returned.json')['function_returned'] is True
        rows.append(row);checks.append(dict(trial_id=row['trial_id'],primary_physical='PASS',replay_physical='PASS',metric_recompute='PASS',exact_replay='PASS',raw_sha256='MATCH'))
        if len(rows)%50==0:print('Verified retained trial',len(rows),flush=True)
    dump('independent_trial_checks.json',checks);dump('unknown_calls.json',unknown)
    primary_reservations=len(list((OUT/'trials').glob('*/primary.reserved.json')))
    replay_reservations=len(list((OUT/'trials').glob('*/replay.reserved.json')))
    counts=Counter((r['config_id'],r['variant'],r['method']) for r in rows)
    buf=io.StringIO();writer=csv.writer(buf)
    writer.writerow(['config_id','variant','method','completed_seeds','expected_seeds','H_DMR_seed_mean','L_DMR_seed_mean','H_P95_ms_seed_mean','L_P95_ms_seed_mean','config_complete'])
    by_config=defaultdict(list)
    for row in rows:by_config[row['config_id']].append(row)
    for (cid,variant,method),count in sorted(counts.items()):
        cells=[r for r in by_config[cid] if r['variant']==variant and r['method']==method]
        def mean(group,metric):
            values=[r['groups'][group][metric] for r in cells]
            return sum(values)/len(values) if values and all(x is not None for x in values) else 'NOT_APPLICABLE'
        writer.writerow([cid,variant,method,count,10,mean('H','dmr'),mean('L','dmr'),mean('H','p95'),mean('L','p95'),len(by_config[cid])==70])
    (HERE/'partial_baseline_summary.csv').write_text(buf.getvalue())
    partial_qualification=[]
    for cid,cells in sorted(by_config.items()):
        if len(cells)!=70:continue
        seed_rows=[]
        for seed in matrix['registered_seeds']:
            records={(r['variant'],r['method']):r for r in cells if r['calibration_seed']==seed}
            main=records['MAIN','B2'];h=records['H_ISOLATED','B2'];low=records['LOW_COMPETITION','B2']
            seed_rows.append(dict(seed=str(seed),validity='VALID',pressure=main['pressure_exact'],H_dmr=main['H_dmr_exact'],L_dmr=main['L_dmr_exact'],H_control_witness=h['control_witness'],LOW_control_witness=low['control_witness'],positive_assigned_busy_wait=main['positive_assigned_busy_wait']))
        eligible=classify_config(configs[cid]['load'],seed_rows,{str(s) for s in matrix['registered_seeds']})
        partial_qualification.append(dict(config_id=cid,eligibility=eligible,seed_count=10,pressure_mean=float(sum(Fraction(r['pressure']) for r in seed_rows)/10),H_DMR_mean=float(sum(Fraction(r['H_dmr']) for r in seed_rows)/10),L_DMR_mean=float(sum(Fraction(r['L_dmr']) for r in seed_rows)/10)))
    dump('complete_config_checks.json',{'scope':'Only existing complete configurations; no global selection or mapping conclusion', 'configs':partial_qualification})
    # Bind every pre-existing campaign byte, including the unresolved reservation.
    raw_files=[p for p in OUT.rglob('*') if p.is_file()]
    raw_manifest=[dict(path=str(p.relative_to(ROOT)),size_bytes=p.stat().st_size,sha256=digest(p.read_bytes())) for p in sorted(raw_files)]
    dump('preserved_raw_manifest.json',{'files':raw_manifest})
    archived=[]
    for cid in sorted({load(d/'manifest.json')['config_id'] for d in all_dirs}):
        included=[p for p in sorted((OUT/'inputs'/cid).rglob('*')) if p.is_file()]
        included.extend(p for d in all_dirs if load(d/'manifest.json')['config_id']==cid for p in sorted(d.rglob('*')) if p.is_file())
        target=HERE/(cid+'.tar.gz')
        expected={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in included}
        with tarfile.open(target,'w:gz',compresslevel=6) as tar:
            for p in included:tar.add(p,arcname=str(p.relative_to(ROOT)),recursive=False)
        with tarfile.open(target,'r:gz') as tar:
            actual={m.name:digest(tar.extractfile(m).read()) for m in tar.getmembers() if m.isfile()}
        assert actual==expected,'archive round-trip mismatch'
        assert target.stat().st_size<100_000_000,'archive exceeds single-file publication limit'
        archived.append(dict(config_id=cid,archive=str(target.relative_to(ROOT)),size_bytes=target.stat().st_size,sha256=digest(target.read_bytes()),raw_members=len(included),roundtrip='PASS'))
    dump('archive_index.json',archived)
    for name in ('context.json','preflight.json','progress.json'):
        (HERE/('original_'+name)).write_bytes((OUT/name).read_bytes())
    original_report=ROOT/'reports/P2_calibration/local_001'
    for name in ('stdout.txt','stderr.txt'):
        (HERE/('original_'+name)).write_bytes((original_report/name).read_bytes())
    summary=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),checked_git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),scientific_source_sha256=context['source_sha256'],
        original_scientific_commit=context['git_commit'],process_status='NOT_RUNNING',original_cli_exit_code='UNKNOWN_NOT_RECORDED',termination_cause='UNKNOWN',
        expected_primary_trials=2520,validated_complete_primary_trials=len(rows),validated_complete_registered_replays=len(rows),primary_slots_reserved=primary_reservations,replay_slots_reserved=replay_reservations,
        actual_primary_invocation_count={'minimum':len(rows),'maximum':primary_reservations},actual_replay_invocation_count={'minimum':len(rows),'maximum':replay_reservations},
        generated_input_count=len(inputs),independently_validated_input_count=len(inputs),complete_configs=len(partial_qualification),partial_configs=len(by_config)-len(partial_qualification),
        unreserved_primary_slots=2520-primary_reservations,unknown_reserved_calls=unknown,execution_completion='INCOMPLETE',artifact_integrity='VALID_FOR_RETAINED_COMPLETE_TRIALS_ONLY',
        selection_status='NOT_EVALUATED_INCOMPLETE_ROSTER',mapping_classification='NOT_EVALUATED',p2_status='BLOCKED',
        recovery_policy_source='docs/P2_design/accepted/local_simulation_scope_001.json unchanged: No retries, owner takeover, reserved-call restart or sample removal',
        additional_scientific_primary_calls=0,additional_registered_replays=0,new_scientific_inputs_generated=0,new_seeds_generated=False,non_calibration_outcomes_accessed=False,validation_unlocked=False,formal_unlocked=False,
        next_safe_action='Preserve this incomplete campaign. Obtain an explicit local-simulation recovery exception before any recomputation of trial247 or restart of this fixed plan; do not count recovery recomputation as a new independent sample.',stop=True)
    dump('summary.json',summary)
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException:
        (HERE/'audit_failure.txt').write_text(traceback.format_exc());raise

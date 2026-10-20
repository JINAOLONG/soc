"""Save P2 engineering correctness evidence; never run registered science.

Every invocation gets a new directory. Failed runs are retained. Only literal
hand-authored P1 fixtures enter child engines; registered generation/analysis
permits remain denied. No deployment/durability PASS is inferred.
"""
from __future__ import annotations

from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import unittest

from soc.model.schema import canonical_bytes
from soc.p2.adapter import validate_physical_payload, verify_decision_views
from soc.p2.coordination import SQLiteAuthority
from soc.p2.identity import ArtifactStore, digest, semantic_bytes
from soc.p2.provenance import capture_process
from soc.p2.runner import inspect_plan, preflight

ROOT=Path(__file__).resolve().parents[1]


def main():
    base=ROOT/'reports/P2_engineering/implementation_001/runs'
    base.mkdir(parents=True,exist_ok=True)
    ordinal=1
    while (base/f'run_{ordinal:03d}').exists(): ordinal+=1
    out=base/f'run_{ordinal:03d}'
    out.mkdir()
    store=ArtifactStore(out)
    def save(name,value,kind='ENGINEERING_EVIDENCE'):
        return store.put(name,canonical_bytes(value),kind)
    record={'origin':'HAND_AUTHORED_CORRECTNESS_FIXTURE','scope':'P2 engineering; not a scientific stage result',
            'timestamp_utc':datetime.now(timezone.utc).isoformat(),'host':platform.platform(),
            'python':sys.version,'command':[sys.executable,*sys.argv],
            'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'worktree':subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'],cwd=ROOT,text=True),
            'scientific_workloads_generated':0,'scientific_workloads_run':0,
            'registered_bootstrap_indices_generated':False,'new_seeds_generated':False,
            'deployment_verified':False,'scientific_execution_authorized':False}
    source_files=sorted({p for prefix in ('src','scripts','tests') for p in (ROOT/prefix).rglob('*.py') if '__pycache__' not in p.parts})
    record['source_sha256']={p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in source_files}
    sys.path.insert(0,str(ROOT/'tests'))
    from run_p1_correctness import EvidenceResult
    stream=io.StringIO()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_p2*.py')
    result=unittest.TextTestRunner(stream=stream,verbosity=2,resultclass=EvidenceResult).run(suite)
    save('unit_results.json',dict(tests=list(result.rows.values()),executed=result.testsRun,
          failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped)))
    store.put('unit_stdout.txt',stream.getvalue().encode(),'TEST_LOG','text/plain')
    exit_code=0 if result.wasSuccessful() and not result.skipped else 1
    record.update(tests_run=result.testsRun,tests_failed=len(result.failures)+len(result.errors),tests_skipped=len(result.skipped))
    if exit_code==0:
        from p1_fixtures import fixture_cases
        fixture_rows=[]
        for name,w in fixture_cases().items():
            input_bytes=canonical_bytes(w.to_dict())
            input_ref=store.put('fixtures/inputs/'+name+'.json',input_bytes,'HAND_FIXTURE_INPUT')
            for method in ('B1','B2','B3','B4','B5'):
                prefix=f'fixtures/{name}/{method}'
                argv=[sys.executable,'-B','-m','soc.p2.fixture_worker','--method',method]
                env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
                primary=capture_process(argv,ROOT,store,prefix+'/primary',env=env,input_bytes=input_bytes)
                replay=capture_process(argv,ROOT,store,prefix+'/replay',env=env,input_bytes=input_bytes)
                raw=store.get(primary['stdout'])
                row={'fixture':name,'method':method,'input_ref':input_ref,'primary':primary,'replay':replay,
                     'exact_replay':raw==store.get(replay['stdout'])}
                if primary['exit_code']!=0 or replay['exit_code']!=0:
                    row['status']='FAIL';exit_code=1
                else:
                    trace=json.loads(raw)
                    body={k:v for k,v in trace.items() if k not in {'origin','schema_version'}}
                    row['independent_validation']=validate_physical_payload(w,body)
                    try: verify_decision_views(w,body)
                    except Exception as exc:row['view_error']=repr(exc)
                    row['status']='PASS' if row['exact_replay'] and row['independent_validation']['status']=='PASS' and 'view_error' not in row else 'FAIL'
                    if row['status']!='PASS':exit_code=1
                fixture_rows.append(row)
                save(prefix+'/result.json',row)
        save('fixture_results.json',fixture_rows)
        record['hand_fixture_baseline_pairs']=len(fixture_rows)
        record['hand_fixture_engine_child_invocations']=2*len(fixture_rows)
        database=out/'fixture_authority.sqlite'
        a=SQLiteAuthority(database,lambda:10,'HAND-AUTHORITY-CLOCK')
        scope=a.register_scope('1'*64,'2'*64,'3'*64,'4'*64)
        sha,row=a.prepare(scope,'PRIMARY_EXECUTION','HAND-TRIAL','HAND-OWNER','4'*64,'HAND-ATTEMPT',100)
        sha,row=a.transition(row['domain_sha256'],sha,'HAND-OWNER','4'*64,'SPAWN_RESERVED')
        a.claim_admission(row['domain_sha256'],sha,'HAND-OWNER','4'*64)
        sha,row=a.transition(row['domain_sha256'],sha,'HAND-OWNER','4'*64,'INCOMPLETE')
        save('fixture_authority_history.json',[dict(sha=s,body=json.loads(b)) for s,b in a.db.execute('SELECT sha,body FROM history ORDER BY revision')])
        a.close()
        record['fixture_database_sha256']=digest(database.read_bytes())
        record['symbolic_plan']=inspect_plan(ROOT)
        record['scientific_preflight']=preflight(ROOT)
    record['exit_code']=exit_code
    save('summary.json',record)
    # Manifest excludes itself; enclosing commit is resolved after this run.
    rows=[{'path':p.relative_to(out).as_posix(),'sha256':digest(p.read_bytes()),'size_bytes':p.stat().st_size}
          for p in sorted(out.rglob('*')) if p.is_file()]
    save('artifact_manifest.json',{'scope':'engineering only','files':rows,'self_excluded':True})
    print(json.dumps({'result_directory':str(out.relative_to(ROOT)),'tests':result.testsRun,
                      'failed':record['tests_failed'],'fixture_pairs':record.get('hand_fixture_baseline_pairs',0),
                      'exit_code':exit_code,'scientific_workloads_run':0},indent=2))
    if exit_code: print(stream.getvalue())
    return exit_code


if __name__=='__main__':raise SystemExit(main())

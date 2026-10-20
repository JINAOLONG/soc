"""Retain actual Docker build/isolation/hand-fixture checks; zero science."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys

from soc.model.schema import canonical_bytes
from soc.p2.identity import ArtifactStore,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    base=ROOT/'reports/P2_engineering/implementation_001/container'
    n=1
    while (base/f'run_{n:03d}').exists():n+=1
    out=base/f'run_{n:03d}';store=ArtifactStore(out)
    commands=[]
    docker=['docker','-H','unix:///var/run/docker.sock']
    def run(argv,*,data=None,timeout=180):
        num=len(commands)+1
        try:
            p=subprocess.run(argv,cwd=ROOT,input=data,capture_output=True,timeout=timeout)
            row={'argv':argv,'exit_code':p.returncode,'timeout':False}
            stdout,stderr=p.stdout,p.stderr
        except subprocess.TimeoutExpired as e:
            row={'argv':argv,'exit_code':None,'timeout':True};stdout=e.stdout or b'';stderr=e.stderr or b''
        row['stdout']=store.put(f'{num:02d}/stdout.txt',stdout,'COMMAND_STDOUT','text/plain')
        row['stderr']=store.put(f'{num:02d}/stderr.txt',stderr,'COMMAND_STDERR','text/plain')
        commands.append(row)
        return row,stdout
    # Tag is engineering-only and not a scientific source/image freeze.
    source={p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in sorted((ROOT/'src').rglob('*.py')) if '__pycache__' not in p.parts}
    build_identity={'source':source,'dockerfile':digest((ROOT/'deploy/Dockerfile.correctness').read_bytes())}
    tag='soc-p2-correctness:'+digest(canonical_bytes(build_identity))[:16]
    build,_=run(docker+['build','--platform','linux/amd64','-f','deploy/Dockerfile.correctness','-t',tag,'.'],timeout=180)
    status='BLOCKED'
    details={}
    if build['exit_code']==0:
        inspected,raw=run(docker+['image','inspect',tag,'--format','{{json .}}'])
        if inspected['exit_code']==0:
            details['image']=json.loads(raw)
        flags=['run','--rm','--read-only','--network','none','--cap-drop','ALL',
               '--security-opt','no-new-privileges','--user','10001:10001',
               '--tmpfs','/tmp:rw,nosuid,nodev,noexec,size=16m']
        probe=('import os,json,sys,hashlib,errno;expected=json.load(sys.stdin);'
               'p="/opt/soc/src/soc/p2/identity.py";'
               'observed={r:hashlib.sha256(open("/opt/soc/"+r,"rb").read()).hexdigest() for r in expected};'
               'print(json.dumps({"uid":os.getuid(),"python":sys.version,"docker_socket":os.path.exists("/var/run/docker.sock"),"source_write_access":os.access(p,os.W_OK),"source_hashes":observed}));'
               'assert observed==expected;'
               'assert os.path.isfile(p);'
               'assert os.getuid()!=0;assert not os.path.exists("/var/run/docker.sock");'
               'assert not os.access(p,os.W_OK);'
               'status=open("/proc/self/status").read();'
               'assert "NoNewPrivs:\\t1" in status;'
               'assert "CapEff:\\t0000000000000000" in status;'
               'assert os.listdir("/sys/class/net")==["lo"]')
        check,_=run(docker+flags+['-i','--entrypoint','python',tag,'-B','-c',probe],data=canonical_bytes(source))
        sys.path.insert(0,str(ROOT/'tests'))
        from p1_fixtures import hand_dag
        from soc.simulator.engine import simulate
        w=hand_dag()
        child,raw=run(docker+flags+['-i',tag,'--method','B2'],data=canonical_bytes(w.to_dict()))
        details['hand_fixture_exact_host_match']=child['exit_code']==0 and raw==canonical_bytes(simulate(w,'B2'))
        status='PASS' if check['exit_code']==0 and details['hand_fixture_exact_host_match'] else 'FAIL'
    result={'origin':'HAND_AUTHORED_CORRECTNESS_FIXTURE','timestamp_utc':datetime.now(timezone.utc).isoformat(),
            'status':status,'scope':'container fixture isolation only; no production profile or storage durability proof',
            'commands':commands,'details':details,'build_identity':build_identity,
            'scientific_workloads_run':0,'scientific_workloads_generated':0}
    store.put('result.json',canonical_bytes(result),'ENGINEERING_CONTAINER_RESULT')
    rows=[{'path':p.relative_to(out).as_posix(),'sha256':digest(p.read_bytes())} for p in sorted(out.rglob('*')) if p.is_file()]
    store.put('artifact_manifest.json',canonical_bytes({'files':rows,'self_excluded':True}),'ENGINEERING_MANIFEST')
    print(json.dumps({'result_directory':str(out.relative_to(ROOT)),'status':status,'scientific_workloads_run':0}))
    return 0 if status=='PASS' else 2


if __name__=='__main__':raise SystemExit(main())

"""Actual Git/process observations and sealed-source verification primitives."""
from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

from soc.p2.identity import ArtifactStore, EvidenceError, digest, safe_path, semantic_bytes


def utc():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def observe_git(root: Path, source_paths: list[str]) -> dict:
    commands = [['git','rev-parse','--show-toplevel'],['git','remote','get-url','origin'],
                ['git','rev-parse','HEAD'],['git','rev-parse','HEAD^{tree}'],
                ['git','symbolic-ref','--quiet','--short','HEAD'],
                ['git','status','--porcelain=v1','--untracked-files=all']]
    records = []
    for argv in commands:
        started=utc()
        p = subprocess.run(argv,cwd=root,capture_output=True)
        records.append(dict(argv=argv,cwd=str(root),host=platform.node(),started_at_utc=started,ended_at_utc=utc(),
                            exit_code=p.returncode,stdout=p.stdout.decode(),stderr=p.stderr.decode()))
        if p.returncode and not (argv[1]=='symbolic-ref' and p.returncode==1):
            raise EvidenceError('required Git observation failed')
    if Path(records[0]['stdout'].strip()).resolve() != root.resolve() or records[1]['stdout'].strip() != 'https://github.com/JINAOLONG/soc.git':
        raise EvidenceError('actual repository mismatch')
    if source_paths != sorted(set(source_paths)):
        raise EvidenceError('source scope must be unique ASCII ordered paths')
    files = []
    for relative in source_paths:
        p = safe_path(root,relative)
        if not p.is_file() or p.is_symlink(): raise EvidenceError('missing/symlink source')
        git = subprocess.run(['git','ls-files','-s','--',relative],cwd=root,capture_output=True,text=True)
        if git.returncode: raise EvidenceError('source blob observation failed')
        entries = git.stdout.splitlines()
        if len(entries)>1: raise EvidenceError('conflicted source index')
        files.append({'path':relative,'sha256':digest(p.read_bytes()),
                      'git_blob':entries[0].split()[1] if entries else None})
    relevant = subprocess.run(['git','status','--porcelain=v1','--untracked-files=all','--',*source_paths],
                              cwd=root,capture_output=True,text=True)
    if relevant.returncode: raise EvidenceError('dirty-scope observation failed')
    return dict(actual_head=records[2]['stdout'].strip(),actual_tree=records[3]['stdout'].strip(),
                branch=records[4]['stdout'].strip() or None,whole_dirty=bool(records[5]['stdout']),
                relevant_dirty=bool(relevant.stdout),relevant_untracked=any(x.startswith('??') for x in relevant.stdout.splitlines()),
                files=files,raw_git_observations=records,
                dirty_scope_observation={'argv':['git','status','--porcelain=v1','--untracked-files=all','--',*source_paths],
                    'exit_code':relevant.returncode,'stdout':relevant.stdout,'stderr':relevant.stderr})


def verify_sealed_files(root: Path, manifest: dict[str,str]):
    if not manifest: raise EvidenceError('empty sealed source manifest')
    for relative, sha in manifest.items():
        p = safe_path(root,relative)
        if p.is_symlink() or not p.is_file() or digest(p.read_bytes())!=sha:
            raise EvidenceError('sealed source/dependency mismatch')
        if os.stat(p).st_mode & 0o222:
            raise EvidenceError('source not read-only')
    # chmod is checked, but kernel isolation/non-bypass is separate deployment
    # evidence. Never claim an execution image is sealed from this check alone.
    return {'files':'MATCH','kernel_isolation':'NOT_ESTABLISHED_BY_MODE_BITS'}


def capture_process(argv: list[str], cwd: Path, store: ArtifactStore, prefix: str, *, env=None, input_bytes=None) -> dict:
    """Actual process/code/log receipt. Caller owns authorization and admission."""
    planned, start_tick = utc(), time.monotonic_ns()
    started, start, end, code, error = False,None,None,None,None
    out=err=b''
    try:
        p=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
        started,start=True,utc()
        out,err=p.communicate(input=input_bytes)
        code=p.returncode
        end=utc()
    except OSError as exc:
        error=type(exc).__name__+': '+str(exc)
    return dict(process_started=started,exit_code=code,planned_at_utc=planned,started_at_utc=start,
                ended_at_utc=end,elapsed_ns=time.monotonic_ns()-start_tick,argv=argv,cwd=str(cwd),
                host=platform.node(),exception=error,
                stdout=store.put(prefix+'/stdout.txt',out,'PROCESS_STDOUT','text/plain'),
                stderr=store.put(prefix+'/stderr.txt',err,'PROCESS_STDERR','text/plain'))

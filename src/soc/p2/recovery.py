"""Accepted B3 closed record checks. Never launches or retries a process.

Authority identity/evidence verification is supplied by the trusted deployment,
not inferred from hashes or from a SUCCESS string inside a record.
"""
from __future__ import annotations

from datetime import datetime
from soc.p2.identity import EvidenceError, digest, semantic_bytes, strict_json

AUTH_NS = 'soc.p2.f02.recovery-authorization.v1'
OP_NS = 'soc.p2.f02.operation-receipt.v1'
ACTIONS = {'VERIFY_EXISTING', 'PUBLISH_EXISTING', 'REUSE_OBSERVATION'}
AUTH_FIELDS = {'namespace','schema_version','profile_ref','issuer_id','executor_id','action',
               'budget_scope_ref','root_authorization_ref','domain_ref','expected_record_ref',
               'subject','inventory_ref','completion_ref','validity','issued_at_utc','authorization_evidence_ref'}
OP_FIELDS = {'namespace','schema_version','profile_ref','request_ref','authorization_ref','actor_id',
             'action','authority_evidence_refs','validation','process','started_at_utc','ended_at_utc','result','error_refs'}
SUBJECT_FIELDS = {
    'INPUT_GENERATION': {'purpose','descriptor_ref','generation_attempt_ref'},
    'PRIMARY_EXECUTION': {'purpose','trial_id','run_identity_ref','attempt_ref'},
    'REGISTERED_REPLAY': {'purpose','trial_id','primary_run_identity_ref','primary_attempt_ref','primary_trace_ref','replay_identity_ref'}}


def b3_schemas():
    ref={'$ref':'#/$defs/ARTIFACT_REF'}
    ident={'$ref':'#/$defs/ID'}
    nullable=lambda shape:{'anyOf':[shape,{'type':'null'}]}
    props={k:ref for k in AUTH_FIELDS if k.endswith('_ref')}
    props.update(namespace={'const':AUTH_NS},schema_version={'const':1},issuer_id=ident,executor_id=ident,
                 action={'enum':sorted(ACTIONS)},completion_ref=nullable(ref),
                 issued_at_utc={'$ref':'#/$defs/UTC'})
    branches=[]
    for purpose,fields in SUBJECT_FIELDS.items():
        fieldspec={k:(ref if k.endswith('_ref') else ident) for k in fields}
        fieldspec['purpose']={'const':purpose}
        branches.append({'type':'object','additionalProperties':False,'required':sorted(fields),'properties':fieldspec})
    props['subject']={'oneOf':branches}
    props['validity']={'type':'object','additionalProperties':False,
        'required':['clock_id','not_before_tick','not_after_tick'],
        'properties':{'clock_id':ident,'not_before_tick':{'$ref':'#/$defs/UINT'},'not_after_tick':{'$ref':'#/$defs/UINT'}}}
    auth={'type':'object','additionalProperties':False,'required':sorted(AUTH_FIELDS),'properties':props}
    op={'namespace':{'const':OP_NS},'schema_version':{'const':1},'profile_ref':ref,'request_ref':ref,
        'authorization_ref':nullable(ref),'actor_id':nullable(ident),'action':nullable({'enum':sorted(ACTIONS)}),
        'authority_evidence_refs':{'type':'array','items':ref},
        'validation':nullable({'$ref':'#/$defs/VALIDATION_RESULT'}),
        'process':nullable({'$ref':'#/$defs/PROCESS_RESULT_V3'}),
        'started_at_utc':nullable({'$ref':'#/$defs/UTC'}),'ended_at_utc':nullable({'$ref':'#/$defs/UTC'}),
        'result':{'enum':['SUCCESS','REJECTED','FAILED','INCOMPLETE']},'error_refs':{'type':'array','items':ref}}
    return auth,{'type':'object','additionalProperties':False,'required':sorted(OP_FIELDS),'properties':op}


def record_identity(body: dict) -> tuple[str, str]:
    name = {AUTH_NS:'recovery-authorization', OP_NS:'operation-receipt'}.get(body.get('namespace'))
    if not name or type(body.get('schema_version')) is not int or body.get('schema_version') != 1:
        raise EvidenceError('unknown B3 record identity')
    sha = digest(semantic_bytes(body))
    return f'urn:soc:f02:{name}:v1:'+sha, sha


def validate_authorization(store, body, *, profile_ref, clock_id, tick, issuer,
                           executor, current_record_ref, verify_authority, types):
    types._validate(b3_schemas()[0],body)
    if set(body) != AUTH_FIELDS or body['namespace'] != AUTH_NS or type(body['schema_version']) is not int or body['schema_version'] != 1:
        raise EvidenceError('B3 authorization closed schema mismatch')
    record_identity(body)
    if body['profile_ref'] != profile_ref or body['issuer_id'] != issuer or body['executor_id'] != executor:
        raise EvidenceError('B3 profile/principal mismatch')
    if body['action'] not in ACTIONS or body['expected_record_ref'] != current_record_ref:
        raise EvidenceError('B3 action/expected state mismatch')
    v = body['validity']
    if (set(v) != {'clock_id','not_before_tick','not_after_tick'} or v['clock_id'] != clock_id or
            any(type(v[k]) is not int for k in ('not_before_tick','not_after_tick')) or
            not 0 <= v['not_before_tick'] <= tick < v['not_after_tick']):
        raise EvidenceError('B3 authorization expired/unknown clock')
    subject = body['subject']
    purpose = subject.get('purpose')
    if purpose not in SUBJECT_FIELDS or set(subject) != SUBJECT_FIELDS[purpose]:
        raise EvidenceError('B3 purpose fields mismatch')
    for k, ref in body.items():
        if k.endswith('_ref') and ref is not None:
            store.get(ref)
    for k, ref in subject.items():
        if k.endswith('_ref'): store.get(ref)
    if body['completion_ref'] is None and body['action'] != 'VERIFY_EXISTING':
        raise EvidenceError('completion required for publish/reuse')
    scope = strict_json(store.get(body['budget_scope_ref']))
    domain = strict_json(store.get(body['domain_ref']))
    current = strict_json(store.get(current_record_ref))
    root = strict_json(store.get(body['root_authorization_ref']))
    for kind,value in [('BUDGET_SCOPE_PREIMAGE_V3',scope),('COORDINATION_DOMAIN_PREIMAGE_V3',domain),
                       ('COORDINATION_RECORD_V3',current),('EXECUTION_AUTH_PREIMAGE',root)]:
        types.validate(kind,value)
    if scope['blueprint_sha256']!=root['blueprint_sha256']:
        raise EvidenceError('B3 root blueprint mismatch')
    if scope['root_authorization_sha256'] != types.identity('EXECUTION_AUTH_PREIMAGE',root)[1]:
        raise EvidenceError('B3 root budget mismatch')
    if (domain['budget_scope_sha256'] != types.identity('BUDGET_SCOPE_PREIMAGE_V3',scope)[1] or domain['purpose'] != purpose or
            current['domain_sha256'] != types.identity('COORDINATION_DOMAIN_PREIMAGE_V3',domain)[1] or current['policy'] != 'A_NO_TAKEOVER' or current['epoch'] != 0):
        raise EvidenceError('B3 domain/immutable policy mismatch')
    if current['inventory_sha256'] != body['inventory_ref']['sha256']:
        raise EvidenceError('B3 existing inventory mismatch')
    if purpose == 'INPUT_GENERATION':
        descriptor = strict_json(store.get(subject['descriptor_ref']))
        attempt = strict_json(store.get(subject['generation_attempt_ref']))
        if descriptor['blueprint_sha256']!=scope['blueprint_sha256']:
            raise EvidenceError('B3 generation blueprint mismatch')
        if domain['semantic_target_id']!=types.identity('INPUT_DESCRIPTOR_PREIMAGE',descriptor)[0] or current['original_attempt_id']!=types.identity('GENERATION_ATTEMPT_PREIMAGE',attempt)[0]:
            raise EvidenceError('B3 generation original identity mismatch')
        if attempt['input_descriptor_sha256'] != types.identity('INPUT_DESCRIPTOR_PREIMAGE',descriptor)[1]:
            raise EvidenceError('B3 generation descriptor mismatch')
    else:
        if domain['semantic_target_id'] != subject['trial_id']:
            raise EvidenceError('B3 trial identity mismatch')
        if purpose=='PRIMARY_EXECUTION':
            attempt=strict_json(store.get(subject['attempt_ref']))
            run=strict_json(store.get(subject['run_identity_ref']))
            if attempt['run_id']!=types.identity('RUN_PREIMAGE_V3',run)[0] or current['original_attempt_id']!=types.identity('ATTEMPT_PREIMAGE',attempt)[0]:
                raise EvidenceError('B3 primary original identity mismatch')
        else:
            replay=strict_json(store.get(subject['replay_identity_ref']))
            run=strict_json(store.get(subject['primary_run_identity_ref']))
            attempt=strict_json(store.get(subject['primary_attempt_ref']))
            if (replay['run_id']!=types.identity('RUN_PREIMAGE_V3',run)[0] or
                    replay['primary_attempt_id']!=types.identity('ATTEMPT_PREIMAGE',attempt)[0] or
                    replay['primary_trace_sha256']!=subject['primary_trace_ref']['sha256'] or
                    current['original_attempt_id']!=types.identity('REPLAY_PREIMAGE',replay)[0]):
                raise EvidenceError('B3 registered replay original identity mismatch')
            if replay['replay_protocol_sha256']!=run['replay_protocol_sha256']:
                raise EvidenceError('B3 replay protocol mismatch')
        if (run['trial_id']!=subject['trial_id'] or run['execution_plan_sha256']!=root['execution_plan_sha256'] or
                run['source_bundle_sha256']!=root['source_bundle_sha256'] or
                attempt['run_id']!=types.identity('RUN_PREIMAGE_V3',run)[0] or
                attempt['execution_authorization_sha256']!=types.identity('EXECUTION_AUTH_PREIMAGE',root)[1]):
            raise EvidenceError('B3 cross-trial/plan/source/root attempt mismatch')
    allowed_phase = {'VERIFY_EXISTING':{'OUTPUT_READY','VERIFIED'}, 'PUBLISH_EXISTING':{'VERIFIED'},
                     'REUSE_OBSERVATION':{'PUBLISHED'}}[body['action']]
    if current['phase'] not in allowed_phase:
        raise EvidenceError('B3 cannot reactivate terminal attempt')
    if body['action']=='REUSE_OBSERVATION' and current['receipt_sha256']!=body['completion_ref']['sha256']:
        raise EvidenceError('B3 reuse must cite original published completion')
    if body['action'] != 'REUSE_OBSERVATION' and (current['lease_clock_id'] != clock_id or tick >= current['lease_deadline_ticks']):
        raise EvidenceError('B3 original lease invalid')
    if not verify_authority(body['authorization_evidence_ref'], issuer, body):
        raise EvidenceError('B3 actual authority evidence not verified')
    return body


def validate_operation(store, body, types, *, verify_authority):
    types._validate(b3_schemas()[1],body)
    if set(body) != OP_FIELDS or body['namespace'] != OP_NS or type(body['schema_version']) is not int or body['schema_version'] != 1:
        raise EvidenceError('B3 operation closed schema mismatch')
    record_identity(body)
    if body['result'] not in {'SUCCESS','REJECTED','FAILED','INCOMPLETE'}:
        raise EvidenceError('B3 operation result mismatch')
    for k in ('profile_ref','request_ref'):
        store.get(body[k])
    for refs in ('authority_evidence_refs','error_refs'):
        if type(body[refs]) is not list: raise EvidenceError('B3 evidence array required')
        for ref in body[refs]: store.get(ref)
    if body['validation'] is not None:
        types.validate('VALIDATION_RESULT', body['validation'])
        if body['validation']['report_ref'] is not None: store.get(body['validation']['report_ref'])
    if body['process'] is not None:
        types.validate('PROCESS_RESULT_V3', body['process'])
    if body['result'] != 'SUCCESS':
        if not body['error_refs']: raise EvidenceError('failed/unknown operation needs retained error evidence')
        return body
    if any(body[k] is None for k in ('authorization_ref','actor_id','action','started_at_utc','ended_at_utc','validation')):
        raise EvidenceError('B3 success cannot have unknown required facts')
    types.validate('UTC',body['started_at_utc']);types.validate('UTC',body['ended_at_utc'])
    def utc_key(text):
        try: datetime.fromisoformat(text)
        except ValueError as exc: raise EvidenceError('invalid UTC calendar value') from exc
        parts=text[:-1].split('.')
        return parts[0],int((parts[1] if len(parts)==2 else '0').ljust(9,'0'))
    if utc_key(body['ended_at_utc']) < utc_key(body['started_at_utc']):
        raise EvidenceError('B3 operation time reversed')
    auth = strict_json(store.get(body['authorization_ref']))
    types._validate(b3_schemas()[0],auth)
    if auth['namespace'] != AUTH_NS or auth['executor_id'] != body['actor_id'] or auth['action'] != body['action'] or auth['profile_ref'] != body['profile_ref']:
        raise EvidenceError('B3 operation/grant mismatch')
    if body['validation']['status'] != 'PASS' or body['validation']['report_ref'] is None:
        raise EvidenceError('B3 success requires actual validation report')
    if body['process'] is not None and (not body['process']['process_started'] or body['process']['exit_code'] != 0):
        raise EvidenceError('B3 success process not successful')
    if not body['authority_evidence_refs'] or not verify_authority(body['authority_evidence_refs'],body):
        raise EvidenceError('B3 hash consistency is not authority authenticity')
    return body

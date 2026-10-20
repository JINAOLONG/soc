import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

from soc.p2.identity import ArtifactStore, EvidenceError, Types, digest, semantic_bytes
from soc.p2.provenance import capture_process, verify_sealed_files
from soc.p2.recovery import AUTH_NS, OP_NS, record_identity, validate_authorization, validate_operation

ROOT=Path(__file__).resolve().parents[1]


class P2RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.store=ArtifactStore(Path(self.temp.name))
        self.types=Types(ROOT/'docs/P2_design/v3/P2_typed_identity_schema_v3.json')
        self.ref=lambda name,body:self.store.put(name,semantic_bytes(body))
        profile=self.ref('profile.json',{'origin':'HAND_AUTHORED_CORRECTNESS_FIXTURE'})
        root=self.ref('root.json',dict(namespace='soc.p2.execution-authorization.v2',schema_version=2,
            blueprint_sha256='a'*64,execution_plan_sha256='b'*64,source_bundle_sha256='c'*64,
            authorization_evidence_raw_sha256='d'*64,authority_id='HAND-ISSUER',issued_at_utc='2026-10-20T00:00:00Z',
            partition='CALIBRATION',max_materialization_attempts=1080,max_primary_engine_invocations=2520,
            max_replay_engine_invocations=2520,automatic_retry_budget=0))
        scope=self.ref('scope.json',dict(namespace='soc.p2.budget-scope.v3',schema_version=3,blueprint_sha256='a'*64,
            matrix_sha256='b'*64,calibration_metadata_sha256='c'*64,root_authorization_sha256=root['sha256']))
        descriptor=dict(namespace='soc.p2.input-descriptor.v2',schema_version=2,blueprint_sha256='a'*64,
                        partition='CALIBRATION',actual_seed_decimal_string='0',scenario='COCKPIT',condition_id='HAND',
                        config_id='HAND',load='light',size=8,control_variant='MAIN',parent_main_descriptor_sha256=None)
        desc=self.ref('descriptor.json',descriptor)
        attempt=dict(namespace='soc.p2.generation-attempt.v2',schema_version=2,input_descriptor_sha256=desc['sha256'],
                     generation_authorization_sha256='a'*64,input_lock_sha256='b'*64,ordinal=1)
        att=self.ref('attempt.json',attempt)
        domain=self.ref('domain.json',{'namespace':'soc.p2.coordination-domain.v3','schema_version':3,
                                      'budget_scope_sha256':scope['sha256'],'purpose':'INPUT_GENERATION',
                                      'semantic_target_id':self.types.identity('INPUT_DESCRIPTOR_PREIMAGE',descriptor)[0]})
        inventory=self.store.inventory([self.ref('existing.json',{'hand':1})])
        current=self.ref('current.json',{'namespace':'soc.p2.coordination-record.v3','schema_version':3,
            'revision':3,'parent_record_sha256':'b'*64,'owner_id':'HAND-OWNER','active_authorization_sha256':root['sha256'],
            'spawn_reserved_ever':True,'inventory_sha256':inventory['sha256'],'receipt_sha256':None,'recovery_authorization_sha256':None,
            'domain_sha256':domain['sha256'],'policy':'A_NO_TAKEOVER','epoch':0,
            'phase':'OUTPUT_READY','original_attempt_id':self.types.identity('GENERATION_ATTEMPT_PREIMAGE',attempt)[0],
            'lease_clock_id':'HAND-CLOCK','lease_deadline_ticks':100})
        evidence=self.ref('grant-evidence.json',{'manual_approval':'HAND-FIXTURE-ONLY'})
        self.auth=dict(namespace=AUTH_NS,schema_version=1,profile_ref=profile,issuer_id='hand-issuer',executor_id='hand-executor',
            action='VERIFY_EXISTING',budget_scope_ref=scope,root_authorization_ref=root,domain_ref=domain,
            expected_record_ref=current,subject={'purpose':'INPUT_GENERATION','descriptor_ref':desc,'generation_attempt_ref':att},
            inventory_ref=inventory,completion_ref=None,validity={'clock_id':'HAND-CLOCK','not_before_tick':0,'not_after_tick':100},
            issued_at_utc='2026-10-20T00:00:00Z',authorization_evidence_ref=evidence)
        self.kw=dict(profile_ref=profile,clock_id='HAND-CLOCK',tick=10,issuer='hand-issuer',executor='hand-executor',
                     current_record_ref=current,verify_authority=lambda *args:True,types=self.types)

    def tearDown(self): self.temp.cleanup()

    def test_b3_closed_grant_and_versioned_id(self):
        self.assertEqual(validate_authorization(self.store,self.auth,**self.kw),self.auth)
        ident,sha=record_identity(self.auth)
        self.assertEqual(ident,'urn:soc:f02:recovery-authorization:v1:'+sha)
        self.assertEqual(sha,digest(semantic_bytes(self.auth)))
        with self.assertRaises(EvidenceError):validate_authorization(self.store,{**self.auth,'extra':True},**self.kw)

    def test_semantic_root_digest_not_confused_with_raw_serialization(self):
        root=json.loads(self.store.get(self.auth['root_authorization_ref']))
        other=self.store.put('root-pretty.json',(json.dumps(root,indent=2)+'\n').encode())
        self.assertNotEqual(other['sha256'],self.auth['root_authorization_ref']['sha256'])
        # This checks hash duties only; original-byte provenance still belongs
        # to the real authority verifier, mocked explicitly for this fixture.
        self.assertEqual(validate_authorization(self.store,{**self.auth,'root_authorization_ref':other},**self.kw)['root_authorization_ref'],other)

    def test_expired_revoked_unknown_clock_and_executor_rejected(self):
        for change in ({'tick':100},{'clock_id':'UNKNOWN'},{'executor':'other'},{'verify_authority':lambda *args:False}):
            with self.subTest(change=str(change)),self.assertRaises(EvidenceError):
                validate_authorization(self.store,self.auth,**{**self.kw,**change})

    def test_publish_requires_original_completion_and_valid_verified_state(self):
        auth={**self.auth,'action':'PUBLISH_EXISTING'}
        with self.assertRaises(EvidenceError):validate_authorization(self.store,auth,**self.kw)
        auth['completion_ref']=self.ref('completion.json',{'hand':True})
        with self.assertRaises(EvidenceError):validate_authorization(self.store,auth,**self.kw)

    def test_primary_and_replay_bind_original_trial_plan_and_attempt(self):
        root=json.loads(self.store.get(self.auth['root_authorization_ref']))
        run=dict(namespace='soc.p2.run-identity.v3',schema_version=3,execution_plan_sha256=root['execution_plan_sha256'],
            trial_id='HAND-TRIAL',workload_id='HAND-WORKLOAD',method_id='B2',source_bundle_sha256=root['source_bundle_sha256'],
            environment_semantic_sha256='a'*64,primary_semantic_argv_sha256='b'*64,observer_spec_sha256='c'*64,
            validator_identity_sha256='d'*64,metric_spec_sha256='e'*64,replay_protocol_sha256='f'*64,
            execution_context_sha256='a'*64,execution_contract_sha256='b'*64)
        runref=self.ref('run.json',run);runid=self.types.identity('RUN_PREIMAGE_V3',run)[0]
        attempt=dict(namespace='soc.p2.attempt-identity.v2',schema_version=2,run_id=runid,
                     execution_authorization_sha256=self.types.identity('EXECUTION_AUTH_PREIMAGE',root)[1],ordinal=1)
        attref=self.ref('primary-attempt.json',attempt);attid=self.types.identity('ATTEMPT_PREIMAGE',attempt)[0]
        trace=self.ref('trace.json',{'origin':'HAND_AUTHORED_CORRECTNESS_FIXTURE'})
        replay=dict(namespace='soc.p2.replay-execution.v2',schema_version=2,run_id=runid,primary_attempt_id=attid,
                    primary_trace_sha256=trace['sha256'],replay_protocol_sha256='f'*64,ordinal=1)
        replayref=self.ref('replay.json',replay)
        for purpose in ('PRIMARY_EXECUTION','REGISTERED_REPLAY'):
            dom=dict(namespace='soc.p2.coordination-domain.v3',schema_version=3,
                     budget_scope_sha256=self.auth['budget_scope_ref']['sha256'],purpose=purpose,semantic_target_id='HAND-TRIAL')
            domref=self.ref(purpose+'-domain.json',dom)
            old=json.loads(self.store.get(self.auth['expected_record_ref']))
            current={**old,'domain_sha256':domref['sha256'],'original_attempt_id':attid if purpose=='PRIMARY_EXECUTION'
                     else self.types.identity('REPLAY_PREIMAGE',replay)[0]}
            currentref=self.ref(purpose+'-current.json',current)
            subject={'purpose':purpose,'trial_id':'HAND-TRIAL'}
            if purpose=='PRIMARY_EXECUTION':subject.update(run_identity_ref=runref,attempt_ref=attref)
            else:subject.update(primary_run_identity_ref=runref,primary_attempt_ref=attref,primary_trace_ref=trace,replay_identity_ref=replayref)
            auth={**self.auth,'domain_ref':domref,'expected_record_ref':currentref,'subject':subject}
            kw={**self.kw,'current_record_ref':currentref}
            self.assertEqual(validate_authorization(self.store,auth,**kw)['subject']['purpose'],purpose)
            with self.assertRaises(EvidenceError):validate_authorization(self.store,{**auth,'subject':{**subject,'trial_id':'OTHER'}},**kw)

    def test_published_reuse_uses_current_grant_not_historical_lease(self):
        completion=self.ref('original-completion.json',{'hand_completion':True})
        current=json.loads(self.store.get(self.auth['expected_record_ref']))
        published=self.ref('published-old.json',{**current,'phase':'PUBLISHED','lease_clock_id':'OLD-BOOT',
                         'lease_deadline_ticks':0,'receipt_sha256':completion['sha256']})
        auth={**self.auth,'action':'REUSE_OBSERVATION','expected_record_ref':published,'completion_ref':completion}
        kw={**self.kw,'current_record_ref':published}
        self.assertEqual(validate_authorization(self.store,auth,**kw)['action'],'REUSE_OBSERVATION')
        wrong=self.ref('wrong-completion.json',{'hand_completion':False})
        with self.assertRaises(EvidenceError):validate_authorization(self.store,{**auth,'completion_ref':wrong},**kw)

    def test_terminal_cannot_become_publishable_and_purpose_cannot_change(self):
        current=json.loads(self.store.get(self.auth['expected_record_ref']))
        halted=self.ref('halted.json',{**current,'phase':'HALTED'})
        auth={**self.auth,'expected_record_ref':halted}
        with self.assertRaises(EvidenceError):validate_authorization(self.store,auth,**{**self.kw,'current_record_ref':halted})
        auth=copy.deepcopy(self.auth);auth['subject']['purpose']='PRIMARY_EXECUTION'
        with self.assertRaises(EvidenceError):validate_authorization(self.store,auth,**self.kw)

    def test_success_operation_requires_evidence_not_just_label(self):
        report=self.ref('validation.json',{'hand_assertion':'MATCH'})
        authref=self.ref('grant.json',self.auth)
        op=dict(namespace=OP_NS,schema_version=1,profile_ref=self.auth['profile_ref'],request_ref=self.ref('request.json',{'hand_request':True}),
            authorization_ref=authref,actor_id='hand-executor',action='VERIFY_EXISTING',authority_evidence_refs=[self.auth['authorization_evidence_ref']],
            validation={'status':'PASS','implementation_sha256':'1'*64,'report_ref':report},process=None,
            started_at_utc='2026-10-20T00:00:00Z',ended_at_utc='2026-10-20T00:00:01Z',result='SUCCESS',error_refs=[])
        self.assertEqual(validate_operation(self.store,op,self.types,verify_authority=lambda *a:True),op)
        for change in ({'authorization_ref':None},{'actor_id':None},{'validation':None},{'authority_evidence_refs':[]}):
            with self.subTest(change=change),self.assertRaises(EvidenceError):
                validate_operation(self.store,{**op,**change},self.types,verify_authority=lambda *a:True)
        with self.assertRaises(EvidenceError):validate_operation(self.store,op,self.types,verify_authority=lambda *a:False)
        with self.assertRaises(EvidenceError):
            validate_operation(self.store,{**op,'started_at_utc':'2026-10-20T00:00:00.000000002Z',
                                'ended_at_utc':'2026-10-20T00:00:00.000000001Z'},self.types,verify_authority=lambda *a:True)

    def test_actual_child_exit_stdout_and_spawn_failure_saved(self):
        p=capture_process([sys.executable,'-B','-c','import sys;print("hand-fixture");sys.exit(7)'],ROOT,self.store,'child')
        self.assertEqual(p['exit_code'],7)
        self.assertTrue(p['process_started'])
        self.assertEqual(self.store.get(p['stdout']),b'hand-fixture\n')
        failed=capture_process(['/definitely/missing/hand-fixture-program'],ROOT,self.store,'spawn-failed')
        self.assertFalse(failed['process_started'])
        self.assertIsNone(failed['exit_code'])
        self.assertIsNotNone(failed['exception'])

    def test_mode_bits_are_not_claimed_as_kernel_isolation(self):
        p=Path(self.temp.name)/'sealed.py';p.write_bytes(b'hand');p.chmod(0o444)
        result=verify_sealed_files(Path(self.temp.name),{'sealed.py':digest(b'hand')})
        self.assertEqual(result['kernel_isolation'],'NOT_ESTABLISHED_BY_MODE_BITS')
        p.chmod(0o644)
        with self.assertRaises(EvidenceError):verify_sealed_files(Path(self.temp.name),{'sealed.py':digest(b'hand')})

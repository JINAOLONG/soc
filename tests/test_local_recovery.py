from pathlib import Path
import hashlib
import json
import tempfile
import unittest
from unittest.mock import Mock,patch

from soc.p2.generation import payload
from soc.p2.identity import EvidenceError
from soc.p2.local_resume import compare_core,check_budget,execute_trial,inputs_for,ledger,resume
from soc.p2.local_run import write_new
from soc.simulator.engine import simulate
from soc.validation.governance import canonical_bytes
from p1_fixtures import hand_dag


class LocalRecoveryTests(unittest.TestCase):
    def test_core_identity_uses_existing_no_newline_inventory_and_rejects_changes(self):
        expected={'src/manual.py':'a'*64,'configs/manual.json':'b'*64}
        digest=hashlib.sha256(canonical_bytes(sorted(expected.items()))).hexdigest()
        self.assertEqual(compare_core(expected,dict(expected),digest)['status'],'PASS')
        for changed in ({**expected,'src/manual.py':'c'*64},{**expected,'src/extra.py':'d'*64}):
            with self.assertRaises(EvidenceError):compare_core(expected,changed,digest)
        with self.assertRaises(EvidenceError):compare_core(expected,expected,'0'*64)

    def test_one_extra_primary_and_total_budget_are_enforced(self):
        counts=dict(original_primary_reservations=247,recovery_primary_reservations=0,replay_reservations=246)
        check_budget(counts,'PRIMARY',recovery=True)
        counts['recovery_primary_reservations']=1
        with self.assertRaises(EvidenceError):check_budget(counts,'PRIMARY',recovery=True)
        full=dict(original_primary_reservations=2520,recovery_primary_reservations=1,replay_reservations=2520)
        with self.assertRaises(EvidenceError):check_budget(full,'REPLAY')
        with self.assertRaises(EvidenceError):check_budget({**full,'recovery_primary_reservations':2},'PRIMARY')

    def case(self,root,*,unknown):
        out=root/'results/calibration/local_001';out.mkdir(parents=True)
        w=hand_dag();ref=write_new(out/'inputs/manual.json.gz',payload(w),compressed=True)
        trial=dict(trial_id='manual-trial',workload_id='manual-workload',variant='LOW_COMPETITION',
                   method='B2',partition='HAND_AUTHORED_CORRECTNESS_FIXTURE')
        context=dict(mode='HAND_AUTHORED_CORRECTNESS_FIXTURE',git_commit='manual',source_sha256='a'*64,
                     original_frozen_source_sha256='b'*64,command=['manual-engineering-test'],dirty_status='',
                     segment_context='manual-context',recovery_authorization_sha256='c'*64)
        directory=out/'trials'/trial['trial_id']
        if unknown:
            write_new(directory/'manifest.json',{'input_ref':ref,'method':'B2','workload_id':trial['workload_id']})
            write_new(directory/'primary.reserved.json',{'manual_unknown':True,'no_retry':True})
        return out,w,ref,trial,context,directory

    def test_recovery_preserves_original_unknown_evidence_and_calls_only_once_plus_replay(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out,w,ref,t,context,directory=self.case(root,unknown=True)
            original={p.name:p.read_bytes() for p in directory.iterdir()}
            with patch('soc.p2.local_resume.simulate',wraps=simulate) as engine:
                row=execute_trial(root,out,t,{},w,ref,context,{'allowed_recovery_trial':'manual-trial'})
                self.assertEqual(engine.call_count,2)
                self.assertTrue(row['one_time_recovery']);self.assertTrue(row['exact_replay'])
                self.assertEqual(row['validity'],'VALID')
                for name,data in original.items():self.assertEqual((directory/name).read_bytes(),data)
                with self.assertRaises(EvidenceError):execute_trial(root,out,t,{},w,ref,context,{'allowed_recovery_trial':'manual-trial'})
                self.assertEqual(engine.call_count,2)
            self.assertEqual(ledger(out),dict(original_primary_reservations=1,recovery_primary_reservations=1,replay_reservations=1))

    def test_wrong_saved_input_or_unapproved_trial_never_executes(self):
        for wrong_input in (True,False):
            with self.subTest(wrong_input=wrong_input),tempfile.TemporaryDirectory() as d:
                root=Path(d);out,w,ref,t,context,directory=self.case(root,unknown=True)
                auth={'allowed_recovery_trial':'manual-trial' if wrong_input else 'different-trial'}
                with patch('soc.p2.local_resume.simulate') as engine:
                    with self.assertRaises(EvidenceError):execute_trial(root,out,t,{},w,{**ref,'sha256':'0'*64} if wrong_input else ref,context,auth)
                    engine.assert_not_called()
                self.assertFalse((directory/'recovery_001').exists())

    def test_another_partial_recovery_is_not_retried(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out,w,ref,t,context,directory=self.case(root,unknown=True)
            write_new(directory/'recovery_001/primary.reserved.json',{'manual_extra_unknown':True})
            with patch('soc.p2.local_resume.simulate') as engine:
                with self.assertRaises(EvidenceError):execute_trial(root,out,t,{},w,ref,context,{'allowed_recovery_trial':'manual-trial'})
                engine.assert_not_called()

    def test_fresh_unreserved_trial_does_not_consume_the_recovery_exception(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out,w,ref,t,context,directory=self.case(root,unknown=False)
            row=execute_trial(root,out,t,{},w,ref,context,{'allowed_recovery_trial':'different-trial'})
            self.assertFalse(row['one_time_recovery']);self.assertTrue(row['exact_replay'])
            self.assertEqual(ledger(out)['recovery_primary_reservations'],0)

    def test_partial_input_generation_is_never_regenerated(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out=root/'results/calibration/local_001'
            (out/'inputs/manual/s00').mkdir(parents=True)
            generator=Mock()
            with self.assertRaises(FileNotFoundError):
                inputs_for(root,out,{'config_id':'manual'},{'seed_index':0,'calibration_seed':0},generator,Mock())
            generator.materialize.assert_not_called()

    def test_segment_rejects_non_config_boundaries_and_excessive_admission_windows(self):
        for end,seconds in ((281,600),(0,600),(2590,600),(280,901),(280,0)):
            with self.subTest(end=end,seconds=seconds),self.assertRaises(EvidenceError):
                resume(Path('/nonexistent-manual-root'),end_trial=end,seconds=seconds)

import json
from pathlib import Path
import tempfile
import unittest

from soc.validation.p1 import audit_p1, manifest_errors, declared_test_ids
from soc.validation.governance import sha256_file


class P1GateTests(unittest.TestCase):
    def test_manifest_detects_actual_tampering_duplicate_and_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root/"trace.json"
            path.write_text("original")
            row = dict(path="trace.json", sha256=sha256_file(path))
            self.assertEqual(manifest_errors(root, [row])[0], [])
            path.write_text("tampered")
            self.assertIn("hash mismatch", manifest_errors(root, [row])[0][0])
            self.assertTrue(manifest_errors(root, [row, row])[0])
            self.assertTrue(manifest_errors(root, [dict(path="../outside", sha256="0"*64)])[0])

    def test_declared_test_identity_is_not_just_a_passing_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/"tests").mkdir()
            (root/"tests/test_example.py").write_text("class Checks:\n    def test_required(self): pass\n    def helper(self): pass\n")
            self.assertEqual(declared_test_ids(root), {"test_example.Checks.test_required"})

    def test_missing_evidence_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            result = audit_p1(Path(directory))
            self.assertEqual(result["status"], "BLOCKED")
            self.assertTrue(result["errors"])

    def test_forged_pass_label_cannot_replace_inputs_tests_or_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/"reports/P1_artifacts").mkdir(parents=True)
            (root/"reports/P1_correctness.json").write_text('{"status":"PASS"}')
            (root/"reports/P1_artifacts/index.json").write_text('{"status":"PASS","runs":[]}')
            result = audit_p1(root)
            self.assertEqual(result["status"], "BLOCKED")

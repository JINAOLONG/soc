"""Protocol tests use metadata/synthetic fixtures, never scientific workloads."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from soc.validation.governance import (
    MASTER, COUNTS, ProtocolError, derive_partitions, check_partitions,
    authorize, audit_p0, literature_errors, relevant_source_hash,
)

ROOT = Path(__file__).resolve().parents[1]


class SeedMetadataTests(unittest.TestCase):
    def test_exact_prescribed_derivation_and_metadata(self):
        self.assertEqual(json.loads((ROOT / "configs/seed_partitions.json").read_text()),
                         derive_partitions())

    def test_independent_first_seed_calculation(self):
        digest = hashlib.sha256(f"{MASTER}|CALIBRATION|0".encode()).hexdigest()
        expected = int(digest, 16) % (1 << 52)
        self.assertEqual(derive_partitions()["partitions"]["CALIBRATION"][0], expected)

    def test_partition_counts_ranges_disjointness_and_split(self):
        metadata = derive_partitions()
        seeds = metadata["partitions"]
        self.assertEqual({k: len(v) for k, v in seeds.items()}, COUNTS)
        flat = [seed for values in seeds.values() for seed in values]
        self.assertEqual(len(set(flat)), 70)
        self.assertTrue(all(0 <= seed < 2**52 for seed in flat))
        self.assertEqual(metadata["development_split"], {
            "parameter_development": [0, 10], "development_precheck": [10, 20]})

    def test_tampered_seed_metadata_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "configs").mkdir()
            data = copy.deepcopy(derive_partitions())
            data["partitions"]["CALIBRATION"][0] += 1
            (root / "configs/seed_partitions.json").write_text(json.dumps(data))
            self.assertTrue(check_partitions(root))

    def test_seed_generation_repeats_without_rewriting(self):
        path = ROOT / "configs/seed_partitions.json"
        before = path.read_bytes(), path.stat().st_mtime_ns
        result = subprocess.run([sys.executable, str(ROOT / "scripts/generate_seeds.py")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, (path.read_bytes(), path.stat().st_mtime_ns))


class GuardTests(unittest.TestCase):
    def test_cross_partition_and_unknown_stage_rejected_before_seed_read(self):
        missing = Path("/path-that-does-not-exist-soc-tests")
        for stage in ["p0", "p1", "calibration", "development", "mystery"]:
            for partition in ["INDEPENDENT_VALIDATION", "FORMAL_EVALUATION"]:
                with self.subTest(stage=stage, partition=partition):
                    with self.assertRaisesRegex(ProtocolError, "unknown|not allowed"):
                        authorize(missing, stage, partition, 0)

    def test_reserved_partition_without_gate_never_reads_seed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for stage, partition in [("validation", "INDEPENDENT_VALIDATION"),
                                     ("formal", "FORMAL_EVALUATION")]:
                with self.subTest(stage=stage):
                    with self.assertRaisesRegex(ProtocolError, "missing/invalid evidence"):
                        authorize(root, stage, partition, 0)

    def test_forged_unlock_file_is_insufficient(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "checkpoints").mkdir()
            (root / "checkpoints/VALIDATION_UNLOCKED").write_text("PASS")
            with self.assertRaisesRegex(ProtocolError, "P3_gate"):
                authorize(root, "validation", "INDEPENDENT_VALIDATION", 0)

    def test_fake_pass_gate_without_freeze_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "reports").mkdir()
            (root / "reports/P3_gate.json").write_text('{"status":"PASS"}')
            with self.assertRaisesRegex(ProtocolError, "freeze_manifest"):
                authorize(root, "validation", "INDEPENDENT_VALIDATION", 0)

    def test_calibration_metadata_authorization_does_not_run_workload(self):
        seed = authorize(ROOT, "p1", "CALIBRATION", 0)
        self.assertIsInstance(seed, int)
        self.assertFalse((ROOT / "checkpoints/VALIDATION_UNLOCKED").exists())
        self.assertFalse((ROOT / "checkpoints/FORMAL_UNLOCKED").exists())

    def test_invalid_indices_rejected(self):
        for index in [-1, 10, True, 1.5]:
            with self.subTest(index=index):
                with self.assertRaisesRegex(ProtocolError, "index"):
                    authorize(ROOT, "p1", "CALIBRATION", index)

    def test_science_blocked_by_unreviewed_literature(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ProtocolError, "P0 prerequisite"):
                authorize(root, "calibration", "CALIBRATION", 0)


class AuditTests(unittest.TestCase):
    def test_unverified_literature_is_not_treated_as_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs/literature_evidence.json").write_text(json.dumps({
                "papers": [{"id": "heft_cpop", "status": "UNVERIFIED_SOURCE"}]}))
            errors = literature_errors(root)
            self.assertTrue(any("original studies verified: 0" in e for e in errors))

    def test_corrupted_primary_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            item = {"id": "heft_cpop", "title": "synthetic test fixture",
                    "status": "VERIFIED_PRIMARY", "primary_url": "https://example.invalid/",
                    "artifact_path": "docs/not-found", "sha256": "0" * 64,
                    "review_notes_path": "docs/not-found", "reviewed_at_utc": "synthetic",
                    "reviewer": "synthetic"}
            (root / "docs/literature_evidence.json").write_text(json.dumps({"papers": [item]}))
            self.assertTrue(any("missing/mismatched" in e for e in literature_errors(root)))

    def test_p0_block_is_explicit_and_missing_files_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = audit_p0(Path(tmp))
            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("missing STATUS.md", result["errors"])
            self.assertEqual(result["scientific_partitions_executed"], [])
            self.assertFalse(result["legacy_results_used_as_new_evidence"])

    def test_source_hash_changes_when_source_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ["src", "scripts", "configs"]:
                (root / name).mkdir()
            path = root / "src/example.py"
            path.write_text("one\n")
            first = relevant_source_hash(root)
            path.write_text("two\n")
            self.assertNotEqual(first, relevant_source_hash(root))

    def test_build_metadata_does_not_change_scientific_source_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src/example.egg-info").mkdir(parents=True)
            (root / "src/example.py").write_text("source\n")
            first = relevant_source_hash(root)
            (root / "src/example.egg-info/PKG-INFO").write_text("generated\n")
            self.assertEqual(first, relevant_source_hash(root))


if __name__ == "__main__":
    unittest.main()

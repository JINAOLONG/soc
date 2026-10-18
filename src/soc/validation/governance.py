"""Fail-closed protocol gates; no simulator or scheduler implementation lives here."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

MASTER = "vehicle-soc-dag-scheduler-cleanroom-soc-v1"
COUNTS = {"CALIBRATION": 10, "DEVELOPMENT": 20,
          "INDEPENDENT_VALIDATION": 10, "FORMAL_EVALUATION": 30}
STAGES = {"p0", "p1", "calibration", "development", "validation", "formal"}


class ProtocolError(RuntimeError):
    """A prerequisite is unmet; no scientific workload may be materialized."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive_partitions() -> dict:
    """Index starts at zero. Nonce suffix exists only on a collision retry."""
    used: set[int] = set()
    partitions: dict[str, list[int]] = {}
    nonces: dict[str, int] = {}
    for name, count in COUNTS.items():
        partitions[name] = []
        for index in range(count):
            nonce = 0
            while True:
                text = f"{MASTER}|{name}|{index}"
                if nonce:
                    text += f"|nonce={nonce}"
                seed = int.from_bytes(hashlib.sha256(text.encode()).digest(), "big") % 2**52
                if seed not in used:
                    break
                nonce += 1
            if nonce:
                nonces[f"{name}:{index}"] = nonce
            used.add(seed)
            partitions[name].append(seed)
    return {"schema_version": 1, "master": MASTER, "index_origin": 0,
            "integer_mapping": "unsigned big-endian SHA256 integer modulo 2**52",
            "collision_rule": "append |nonce=N for N=1,2,... only after collision",
            "collision_nonces": nonces, "partitions": partitions,
            "development_split": {"parameter_development": [0, 10],
                                  "development_precheck": [10, 20]}}


def check_partitions(root: Path) -> list[str]:
    try:
        actual = json.loads((root / "configs/seed_partitions.json").read_text())
    except (OSError, ValueError) as error:
        return [f"seed metadata unreadable: {error}"]
    return [] if actual == derive_partitions() else ["seed derivation/metadata mismatch"]


def relevant_source_hash(root: Path) -> str:
    paths = []
    for prefix in ("src", "scripts", "configs"):
        for path in (root / prefix).rglob("*"):
            if (path.is_file() and "__pycache__" not in path.parts and
                    not any(part.endswith(".egg-info") for part in path.parts) and
                    path.suffix != ".pyc"):
                paths.append(path)
    rows = [(p.relative_to(root).as_posix(), sha256_file(p)) for p in sorted(paths)]
    return hashlib.sha256(canonical_bytes(rows)).hexdigest()


def literature_errors(root: Path) -> list[str]:
    """Downloaded bytes alone cannot certify scientific source review."""
    try:
        evidence = json.loads((root / "docs/literature_evidence.json").read_text())
    except (OSError, ValueError) as error:
        return [f"literature evidence unreadable: {error}"]
    verified = []
    errors = []
    for paper in evidence.get("papers", []):
        if paper.get("status") != "VERIFIED_PRIMARY":
            continue
        required = ("id", "title", "primary_url", "artifact_path", "sha256",
                    "review_notes_path", "reviewed_at_utc", "reviewer")
        if any(not paper.get(field) for field in required):
            errors.append(f"incomplete primary review: {paper.get('id', 'UNKNOWN')}")
            continue
        artifact = (root / paper["artifact_path"]).resolve()
        notes = (root / paper["review_notes_path"]).resolve()
        if not artifact.is_relative_to(root.resolve()) or not notes.is_relative_to(root.resolve()):
            errors.append("primary evidence paths must remain in repository")
            continue
        if not artifact.is_file() or sha256_file(artifact) != paper["sha256"]:
            errors.append(f"missing/mismatched primary artifact: {paper['id']}")
            continue
        if not notes.is_file() or not notes.read_text().strip():
            errors.append(f"missing review notes: {paper['id']}")
            continue
        verified.append(paper["id"])
    if len(set(verified)) < 6:
        errors.append(f"original studies verified: {len(set(verified))}; required: at least 6")
    if len(verified) != len(set(verified)):
        errors.append("duplicate primary study identity")
    missing = {"heft_cpop", "peft", "ds3"} - set(verified)
    if missing:
        errors.append("required originals unverified: " + ", ".join(sorted(missing)))
    return errors


def audit_p0(root: Path) -> dict:
    required = ["AGENTS.md", "README.md", "STATUS.md", "pyproject.toml",
                "docs/research_contract.md", "docs/model_spec.md",
                "docs/literature_matrix.md", "docs/baseline_spec.md",
                "docs/metric_spec.md", "docs/statistical_protocol.md",
                "configs/research_protocol.json", "configs/seed_partitions.json"]
    errors = ["missing " + path for path in required if not (root / path).is_file()]
    errors += check_partitions(root) + literature_errors(root)
    return {"stage": "P0", "status": "BLOCKED" if errors else "PASS",
            "errors": errors, "partition_counts": COUNTS,
            "seed_sha256": sha256_file(root / "configs/seed_partitions.json")
            if (root / "configs/seed_partitions.json").is_file() else None,
            "source_sha256": relevant_source_hash(root),
            "scientific_partitions_executed": [],
            "legacy_results_used_as_new_evidence": False}


def _load(root: Path, path: str) -> dict:
    try:
        data = json.loads((root / path).read_text())
    except (OSError, ValueError) as error:
        raise ProtocolError(f"missing/invalid evidence {path}") from error
    if not isinstance(data, dict):
        raise ProtocolError(f"evidence must be an object: {path}")
    return data


def _gate(root: Path, path: str) -> None:
    if _load(root, path).get("status") != "PASS":
        raise ProtocolError(f"gate has not passed: {path}")


def _frozen(root: Path, label: str) -> None:
    """A token is insufficient: link it to a committed, clean freeze record."""
    manifest_path = f"checkpoints/{label}_freeze_manifest.json"
    record = _load(root, manifest_path)
    token_name = "VALIDATION_UNLOCKED" if label == "development" else "FORMAL_UNLOCKED"
    token = _load(root, f"checkpoints/{token_name}")
    if token.get("freeze_sha256") != sha256_file(root / manifest_path):
        raise ProtocolError("unlock token is not bound to the freeze manifest")
    if record.get("source_sha256") != relevant_source_hash(root):
        raise ProtocolError("frozen source/configuration hash mismatch")
    commit = record.get("git_commit", "")
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise ProtocolError("invalid frozen Git commit identity")
    try:
        subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=root,
                       check=True, capture_output=True)
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all", "--",
             "src", "scripts", "configs"], cwd=root, text=True)
        if dirty:
            raise ProtocolError("relevant source/configuration is dirty")
        # Require evidence and source files to be tracked in the actual checkout.
        for path in (manifest_path, f"checkpoints/{token_name}"):
            subprocess.run(["git", "ls-files", "--error-unmatch", path], cwd=root,
                           check=True, capture_output=True)
        if subprocess.check_output(["git", "status", "--porcelain", "--",
                                    manifest_path, f"checkpoints/{token_name}"],
                                   cwd=root, text=True):
            raise ProtocolError("freeze/token must be committed")
    except subprocess.CalledProcessError as error:
        raise ProtocolError("freeze evidence is not committed or commit is unavailable") from error


def authorize(root: Path, stage: str, partition: str, index: int) -> int:
    """Authorize before obtaining a seed. This never generates a workload."""
    if stage not in STAGES or partition not in COUNTS:
        raise ProtocolError("unknown stage or partition")
    expected = {"p0": "CALIBRATION", "p1": "CALIBRATION", "calibration": "CALIBRATION",
                "development": "DEVELOPMENT", "validation": "INDEPENDENT_VALIDATION",
                "formal": "FORMAL_EVALUATION"}[stage]
    if partition != expected:
        raise ProtocolError("partition is not allowed for this stage")
    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < COUNTS[partition]:
        raise ProtocolError("seed index outside partition")
    if stage == "validation":
        _gate(root, "reports/P3_gate.json")
        _frozen(root, "development")
    if stage == "formal":
        _gate(root, "reports/P4_validation_gate.json")
        _frozen(root, "validation")
    if stage in {"calibration", "development", "validation", "formal"}:
        audit = audit_p0(root)
        if audit["status"] != "PASS":
            raise ProtocolError("P0 prerequisite has not passed: " + "; ".join(audit["errors"]))
        _gate(root, "reports/P1_correctness.json")
    if stage in {"development", "validation", "formal"}:
        _gate(root, "reports/P2_mapping_opportunity.json")
    errors = check_partitions(root)
    if errors:
        raise ProtocolError("; ".join(errors))
    return _load(root, "configs/seed_partitions.json")["partitions"][partition][index]

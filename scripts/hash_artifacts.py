"""Create or verify an explicit relative-path SHA256 evidence inventory."""
from pathlib import Path
import argparse
import json
from soc.validation.governance import sha256_file


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", default="checkpoints/P0_artifact_manifest.json")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    target = (root / args.output).resolve()
    if not target.is_relative_to(root):
        p.error("manifest must remain inside repository")
    if args.verify:
        data = json.loads(target.read_text())
        missing, mismatch, seen = [], [], set()
        for row in data["files"]:
            rel = row["path"]
            path = (root / rel).resolve()
            if not path.is_relative_to(root) or rel in seen:
                raise SystemExit("invalid/duplicate manifest path")
            seen.add(rel)
            if not path.is_file():
                missing.append(rel)
            elif sha256_file(path) != row["sha256"]:
                mismatch.append(rel)
        print(json.dumps({"files": len(seen), "missing": missing, "mismatch": mismatch}))
        return 1 if missing or mismatch else 0
    files = []
    for prefix in ["src", "scripts", "configs", "docs", "reports", "tests", ".github"]:
        for path in (root / prefix).rglob("*"):
            if (path.is_file() and path.resolve() != target and
                    "__pycache__" not in path.parts and
                    not any(part.endswith(".egg-info") for part in path.parts) and
                    path.suffix != ".pyc"):
                files.append(path)
    files += [root / n for n in ["AGENTS.md", "README.md", "STATUS.md", "pyproject.toml", ".gitignore", "LICENSE"]]
    rows = [{"path": path.relative_to(root).as_posix(), "sha256": sha256_file(path)}
            for path in sorted(set(files))]
    target.write_text(json.dumps({"schema_version": 1, "scope": "explicit P0 evidence inventory; no scientific runs",
                                  "files": rows}, indent=2) + "\n")
    print(json.dumps({"manifest": str(target.relative_to(root)), "files": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

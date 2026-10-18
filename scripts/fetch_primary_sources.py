"""Restore reviewed primary PDFs by TLS and their recorded SHA256 identities."""
from pathlib import Path
import json
import urllib.request
from soc.validation.governance import sha256_file


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "docs/literature_evidence.json").read_text())
    for row in data["papers"]:
        if row["status"] != "VERIFIED_PRIMARY":
            continue
        path = (root / row["artifact_path"]).resolve()
        if not path.is_relative_to(root / ".cache/literature"):
            raise SystemExit("Refusing source artifact outside repository literature cache")
        if path.exists():
            if sha256_file(path) != row["sha256"]:
                raise SystemExit("Existing source artifact has unexpected SHA256: " + row["id"])
            print("VERIFIED_EXISTING " + row["id"])
            continue
        with urllib.request.urlopen(row["primary_url"], timeout=30) as response:
            body = response.read(20_000_001)
        import hashlib
        if len(body) > 20_000_000 or hashlib.sha256(body).hexdigest() != row["sha256"]:
            raise SystemExit("Source response does not match reviewed artifact: " + row["id"])
        if not body.startswith(b"%PDF-"):
            raise SystemExit("Reviewed primary response must be a PDF")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as output:
            output.write(body)
        print("RESTORED_VERIFIED " + row["id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

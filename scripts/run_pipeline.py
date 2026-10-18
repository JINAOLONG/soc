"""P0/P1 correctness audits and fail-closed scientific stage entry."""
from pathlib import Path
import argparse
import json
import sys
from soc.validation.governance import audit_p0, authorize, ProtocolError


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=[
        "p0", "p1", "calibration", "development", "validation", "formal", "report"])
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.stage == "report":
        print("Evidence closure is in reports/final_report.md; no scientific result generated.")
        return 0
    if args.stage == "p1":
        from soc.validation.p1 import audit_p1
        result = audit_p1(root)
        if not args.check_only:
            (root / "reports/P1_correctness.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "PASS" else 2
    if args.stage != "p0":
        if args.stage in {"validation", "formal"}:
            partition = "INDEPENDENT_VALIDATION" if args.stage == "validation" else "FORMAL_EVALUATION"
            try:
                authorize(root, args.stage, partition, 0)
            except ProtocolError as error:
                print("BLOCKED: " + str(error), file=sys.stderr)
                return 2
        result = audit_p0(root)
        if result["status"] != "PASS":
            print("BLOCKED: P0 has not passed; " + "; ".join(result["errors"]), file=sys.stderr)
            return 2
        print("NOT IMPLEMENTED: stage " + args.stage + "; no workload executed", file=sys.stderr)
        return 3
    result = audit_p0(root)
    if not args.check_only:
        (root / "reports/P0_protocol_audit.json").write_text(json.dumps(result, indent=2) + "\n")
        (root / "reports/P0_protocol_audit.md").write_text(
            "# P0 protocol audit\n\nStatus: " + result["status"] +
            "\n\n" + "\n".join("- " + item for item in result["errors"]) +
            "\n\nSeed counts/derivation are audited as metadata only. No scientific workload has run.\n"
            "\nSee P0_protocol_audit.json for source and seed hashes.\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())

"""Read-only, TLS-verified acquisition diagnostics; never certifies paper review."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.error

URLS = [
    ("ds3_official_readme", "https://raw.githubusercontent.com/segemena/DS3/master/README.md"),
    ("ds3_official_scheduler", "https://raw.githubusercontent.com/segemena/DS3/master/scheduler.py"),
    ("heft_doi_lead", "https://doi.org/10.1109/TPDS.2002.1000340"),
    ("peft_doi_lead", "https://doi.org/10.1109/TPDS.2013.57"),
    ("heft_publisher_lead", "https://ieeexplore.ieee.org/document/1000340"),
    ("peft_metadata_lead", "https://api.crossref.org/works/10.1109/TPDS.2013.57"),
    ("arxiv_discovery", "https://export.arxiv.org/api/query?search_query=ti:heterogeneous+AND+ti:scheduling&max_results=2"),
    ("arxiv_site", "https://arxiv.org/"),
    ("starpu_author_manuscript_lead", "https://inria.hal.science/inria-00550877/document"),
    ("parsec_author_site", "https://icl.utk.edu/parsec/"),
]


def probe(item: tuple[str, str]) -> dict:
    label, url = item
    result = {"id": label, "url": url,
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "scientific_verification": "UNVERIFIED_SOURCE"}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "soc-cleanroom-P0-source-probe/0.1"})
        with urllib.request.urlopen(request, timeout=20) as response:
            # A bounded diagnostic fetch, not a full-paper downloader.
            body = response.read(2_000_001)
            result.update(http_status=response.status, final_url=response.url,
                          content_type=response.headers.get("Content-Type"),
                          bytes_read=len(body), truncated=len(body) > 2_000_000,
                          response_sha256=hashlib.sha256(body).hexdigest(),
                          outcome="RETRIEVED_NOT_REVIEWED" if body else "EMPTY_RESPONSE")
            if label == "ds3_official_readme":
                text = body.decode("utf-8")
                result["observed_code_documentation"] = {
                    "entrypoint_DASH_Sim_v0": "DASH_Sim_v0.py" in text,
                    "resource_compatibility_format": "num_supported_functionalities" in text,
                    "DAS_framework_section": "Dynamic Adaptive Scheduling" in text}
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        result.update(outcome="ACCESS_FAILED", error=str(error))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="new output path inside reports/")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    path = (root / args.output).resolve()
    if not path.is_relative_to(root / "reports") or path.exists():
        parser.error("use a new output path inside reports; preserve prior failures")
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(probe, URLS))
    record = {"purpose": "P0 primary source acquisition diagnostics, not paper review",
              "tls_verification": "ENABLED (Python default trust)", "attempts": rows}
    with path.open("x") as output:
        json.dump(record, output, indent=2)
        output.write("\n")
    print(json.dumps({"attempts": len(rows),
                      "retrieved": sum(r["outcome"] == "RETRIEVED_NOT_REVIEWED" for r in rows),
                      "empty_responses": sum(r["outcome"] == "EMPTY_RESPONSE" for r in rows),
                      "failed": sum(r["outcome"] == "ACCESS_FAILED" for r in rows),
                      "primary_studies_verified": 0, "output": str(path.relative_to(root))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

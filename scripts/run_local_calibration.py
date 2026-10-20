"""Run the accepted fixed CALIBRATION simulation without production deployment."""
import argparse
import json
from pathlib import Path

from soc.p2.local_run import inspect_local, run


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    result=inspect_local(root) if args.check_only else run(root,root/'results/calibration/local_001')
    print(json.dumps(result,indent=2))
    return 2 if result.get('errors') or result.get('execution_completion') not in (None,'COMPLETE') else 0


if __name__=='__main__': raise SystemExit(main())

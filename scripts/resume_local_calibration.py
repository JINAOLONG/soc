"""Continue an existing CALIBRATION campaign in a bounded foreground segment."""
import argparse
import json
from pathlib import Path

from soc.p2.local_resume import inspect_resume, resume


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only',action='store_true')
    parser.add_argument('--end-trial',type=int,default=280)
    parser.add_argument('--seconds',type=float,default=600)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    result=inspect_resume(root) if args.check_only else resume(root,end_trial=args.end_trial,seconds=args.seconds)
    print(json.dumps(result,indent=2))
    return 2 if result.get('errors') else 0


if __name__=='__main__': raise SystemExit(main())

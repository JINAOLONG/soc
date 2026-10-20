"""One hand-authored correctness invocation. Not a scientific worker."""
import argparse
import json
import sys

from soc.model.schema import Workload, canonical_bytes
from soc.simulator.engine import simulate


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--method',required=True,choices=['B1','B2','B3','B4','B5'])
    args=parser.parse_args()
    workload=Workload.from_dict(json.load(sys.stdin))
    sys.stdout.buffer.write(canonical_bytes(simulate(workload,args.method)))
    return 0


if __name__=='__main__':
    raise SystemExit(main())

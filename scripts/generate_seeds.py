"""Create prescribed seed metadata once; never overwrite existing partitions."""
from pathlib import Path
import json
from soc.validation.governance import derive_partitions, check_partitions

root = Path(__file__).resolve().parents[1]
path = root / "configs/seed_partitions.json"
if path.exists():
    errors = check_partitions(root)
    if errors:
        raise SystemExit("REFUSED: " + "; ".join(errors))
    print("EXISTING_SEED_METADATA_UNCHANGED")
else:
    with path.open("x") as output:
        json.dump(derive_partitions(), output, indent=2)
        output.write("\n")
    print("CREATED_70_SEEDS_METADATA_ONLY; NO_WORKLOAD_EXECUTED")

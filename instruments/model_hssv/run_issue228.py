"""Run the issue #228 structural audit and write its machine receipt."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cosmological_redshift_audit

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "H-SSV" / "results" / "issue-228"
PREREGISTRATION = RESULTS / "00-preregistration.md"
DATASETS = RESULTS / "02-datasets-and-likelihoods.md"
R4_ADDENDUM = RESULTS / "03-information-area-expansion-addendum.md"
RECEIPT = RESULTS / "receipt.json"


def run_all() -> dict[str, object]:
    report = cosmological_redshift_audit.run()
    report["preregistration_sha256"] = hashlib.sha256(PREREGISTRATION.read_bytes()).hexdigest()
    report["dataset_registry_sha256"] = hashlib.sha256(DATASETS.read_bytes()).hexdigest()
    report["r4_addendum_sha256"] = hashlib.sha256(R4_ADDENDUM.read_bytes()).hexdigest()
    report["evidential_boundary"] = (
        "No cosmological outcome vector or H-SSV galaxy result was loaded; "
        "the preregistered analytic stopping rule prevented parameter fitting. "
        "The owner-supplied R4 hypothesis is separately hash-pinned."
    )
    return report


def main() -> None:
    report = run_all()
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"Wrote {RECEIPT}")


if __name__ == "__main__":
    main()

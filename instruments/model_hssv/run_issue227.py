"""Run issue #227 controls and write the H-SSV-II machine receipt."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import screen_response_audit

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "H-SSV" / "results" / "issue-227"
PREREGISTRATION = RESULTS / "00-preregistration.md"
RECEIPT = RESULTS / "receipt.json"


def run_all() -> dict[str, object]:
    report = screen_response_audit.run()
    report["preregistration_sha256"] = hashlib.sha256(
        PREREGISTRATION.read_bytes()
    ).hexdigest()
    report["evidential_boundary"] = (
        "No issue-225 galaxy outcome, residual, fitted amplitude or core radius "
        "was loaded; only the externally fixed BTFR exponent target was used."
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

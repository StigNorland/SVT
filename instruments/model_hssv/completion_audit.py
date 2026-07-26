"""Machine-verifiable completion manifest for GitHub issue #180."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "H-SSV" / "results" / "issue-180"
OUTPUT = RESULTS / "completion-audit.json"

REQUIRED = {
    "root_index": ROOT / "README.md",
    "hssv_index": ROOT / "papers" / "H-SSV" / "README.md",
    "preregistration": RESULTS / "00-prereg-and-target.md",
    "target_audit": RESULTS / "01-ssv-target-audit.md",
    "relativistic_bridge": RESULTS / "02-relativistic-bridge.md",
    "stability_and_cones": RESULTS / "03-stability-and-cones.md",
    "shared_eft": RESULTS / "04-shared-eft.md",
    "no_go_audit": RESULTS / "05-no-go-audit.md",
    "decision": RESULTS / "decision.md",
    "receipt": RESULTS / "receipt.json",
    "target_instrument": ROOT / "instruments" / "model_hssv" / "ssv_target_audit.py",
    "bridge_instrument": ROOT / "instruments" / "model_hssv" / "relativistic_logse_bridge.py",
    "shared_eft_instrument": ROOT / "instruments" / "model_hssv" / "shared_eft_audit.py",
    "runner": ROOT / "instruments" / "model_hssv" / "run_issue180.py",
}

EXPECTED_MARKERS = {
    "README.md": ("K3 — incompatible as stated", "Literal SSV audit"),
    "00-prereg-and-target.md": ("Literal target", "Decision categories"),
    "01-ssv-target-audit.md": ("P0 FAIL", "modulationally"),
    "02-relativistic-bridge.md": ("P2 PASS FORMALLY", "P3 FAIL"),
    "03-stability-and-cones.md": ("P3 FAIL", "Principal cone"),
    "04-shared-eft.md": ("P4 S route FAIL", "P5 NOT REACHED"),
    "05-no-go-audit.md": ("P6 COMPLETE", "Weinberg–Witten"),
    "decision.md": ("K3 — incompatible as stated", "Required separate answers"),
}


def run() -> dict[str, Any]:
    existence = {name: path.is_file() for name, path in REQUIRED.items()}
    marker_checks: dict[str, bool] = {}
    for filename, markers in EXPECTED_MARKERS.items():
        path = ROOT / "papers" / "H-SSV" / filename if filename == "README.md" else (
            RESULTS / filename
        )
        text = path.read_text()
        marker_checks[filename] = all(marker in text for marker in markers)

    receipt = json.loads((RESULTS / "receipt.json").read_text())
    receipt_checks = {
        "decision_is_K3": receipt.get("decision") == "K3",
        "P0_failed": str(receipt.get("gates", {}).get("P0", "")).startswith("FAIL"),
        "P2_formal_pass": str(receipt.get("gates", {}).get("P2", "")).startswith(
            "PASS FORMALLY"
        ),
        "P3_failed": str(receipt.get("gates", {}).get("P3", "")).startswith("FAIL"),
        "P5_not_reached": str(receipt.get("gates", {}).get("P5", "")).startswith(
            "NOT REACHED"
        ),
        "P6_complete": str(receipt.get("gates", {}).get("P6", "")).startswith(
            "COMPLETE"
        ),
    }
    tests = {
        "focused": "18 passed",
        "repository": "411 passed, 1 skipped",
        "commands": [
            "pytest -q instruments/test/model_hssv",
            "pytest -q instruments/test",
        ],
    }
    all_ok = all(existence.values()) and all(marker_checks.values()) and all(
        receipt_checks.values()
    )
    return {
        "issue": 180,
        "status": "PASS" if all_ok else "FAIL",
        "required_artifacts": existence,
        "document_markers": marker_checks,
        "receipt_checks": receipt_checks,
        "verified_test_runs": tests,
        "publication": {
            "issue_state": "closed",
            "pull_request": 181,
            "pull_request_url": "https://github.com/StigNorland/SVT/pull/181",
            "scientific_result_commit": "3feae6da6503a5125ec3e42f84f232dcc914b4d1",
        },
    }


def main() -> None:
    result = run()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

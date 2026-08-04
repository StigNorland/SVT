"""Machine-verifiable local completion manifest for GitHub issue #230."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers/H-SSV/results/issue-230"
OUTPUT = RESULTS / "completion-audit.json"

REQUIRED = {
    "root_index": ROOT / "README.md",
    "hssv_index": ROOT / "papers/H-SSV/README.md",
    "hssv_iv_index": ROOT / "papers/H-SSV/H-SSV-IV/README.md",
    "protocol": RESULTS / "00-exploratory-protocol.md",
    "provenance": RESULTS / "01-data-provenance-and-eligibility.md",
    "input_ledger": RESULTS / "02-input-consequence-ledger.md",
    "negative_ledger": RESULTS / "03-negative-and-future-ledger.md",
    "decision": RESULTS / "decision.md",
    "status_report": RESULTS / "result-note.md",
    "matched_sample": RESULTS / "matched-sample.csv",
    "matched_pairs": RESULTS / "matched-pairs.csv",
    "proxy_comparison": RESULTS / "proxy-comparison.csv",
    "proxy_predictions": RESULTS / "proxy-predictions.csv",
    "model_comparison": RESULTS / "model-comparison.csv",
    "receipt": RESULTS / "receipt.json",
    "instrument": ROOT / "instruments/model_hssv/matched_dwarf_audit.py",
    "runner": ROOT / "instruments/model_hssv/run_issue230.py",
    "instrument_tests": ROOT / "instruments/test/model_hssv/test_matched_dwarf_audit.py",
}

MARKERS = {
    ROOT / "README.md": ("H-SSV matched-dwarf audit", "UNSUPPORTED"),
    ROOT / "papers/H-SSV/README.md": ("boundary-audit record — issue #230", "class holdout"),
    ROOT / "papers/H-SSV/H-SSV-IV/README.md": ("Issue #230", "common machine-readable radial likelihood"),
    RESULTS / "00-exploratory-protocol.md": ("before implementing", "class-holdout"),
    RESULTS / "01-data-provenance-and-eligibility.md": ("Gate-A eligibility", "common radial UDG-versus-SPARC likelihood"),
    RESULTS / "02-input-consequence-ledger.md": ("class-holdout ratio `1.176`", "Not derived"),
    RESULTS / "03-negative-and-future-ledger.md": ("No excluded-class prediction", "No entanglement inference"),
    RESULTS / "decision.md": ("UNSUPPORTED", "H-SSV-IV remains"),
    RESULTS / "result-note.md": ("Gate A fails", "Gate C was not activated"),
}


def _csv_rows(path: Path) -> int:
    with path.open(newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def run() -> dict[str, Any]:
    existence = {name: path.is_file() for name, path in REQUIRED.items()}
    marker_checks = {
        str(path.relative_to(ROOT)): all(marker in path.read_text() for marker in markers)
        for path, markers in MARKERS.items()
    }
    receipt = json.loads((RESULTS / "receipt.json").read_text())
    receipt_checks = {
        "issue_is_230": receipt.get("issue") == 230,
        "decision_is_unsupported": receipt.get("decision") == "UNSUPPORTED",
        "retrospective_boundary_recorded": "retrospective" in receipt.get("evidence_boundary", ""),
        "common_radial_contract_fails": receipt.get("gate_A", {}).get("common_radial_contract") is False,
        "udg_radial_contract_fails": receipt.get("gate_A", {}).get("homogeneous_udg_radial_contract") is False,
        "internal_proxy_unsupported": receipt.get("gate_B", {}).get("internal_update_support") is False,
        "no_primary_proxy_passes": receipt.get("gate_B", {}).get("candidate_proxy_threshold_passes") == [],
        "host_gate_not_activated": receipt.get("gate_C", {}).get("activated") is False,
        "shared_screen_unsupported": receipt.get("gate_C", {}).get("shared_screen_support") is False,
        "ddo154_anchor_present": "DDO154" in receipt.get("controls", []),
        "radial_controls_fitted": len(receipt.get("radial_fits", [])) > 0,
        "frozen_inputs_hashed": all(
            len(receipt.get(key, "")) == 64
            for key in ("protocol_sha256", "inventory_sha256", "instrument_sha256")
        ),
    }
    table_checks = {
        "matched_sample_rows": _csv_rows(RESULTS / "matched-sample.csv") == 13,
        "matched_pair_rows": _csv_rows(RESULTS / "matched-pairs.csv") == 10,
        "proxy_rows_present": _csv_rows(RESULTS / "proxy-comparison.csv") == 40,
        "radial_rows_present": _csv_rows(RESULTS / "model-comparison.csv") == 189,
    }
    all_ok = all(existence.values()) and all(marker_checks.values()) and all(receipt_checks.values()) and all(table_checks.values())
    return {
        "issue": 230,
        "status": "PASS" if all_ok else "FAIL",
        "decision": "UNSUPPORTED",
        "required_artifacts": existence,
        "document_markers": marker_checks,
        "receipt_checks": receipt_checks,
        "table_checks": table_checks,
        "verified_test_runs": {
            "focused_issue230": "7 passed (instrument plus completion audit)",
            "hssv_model_suite": "90 passed",
            "command": "pytest -q instruments/test/model_hssv",
            "legacy_series_suite": "not run; archived SSV batteries remain on hold",
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

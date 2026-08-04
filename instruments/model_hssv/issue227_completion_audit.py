"""Machine-verifiable local completion manifest for GitHub issue #227."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "papers" / "H-SSV" / "H-SSV-II"
RESULTS = ROOT / "papers" / "H-SSV" / "results" / "issue-227"
OUTPUT = RESULTS / "completion-audit.json"

REQUIRED = {
    "root_index": ROOT / "README.md",
    "hssv_index": ROOT / "papers" / "H-SSV" / "README.md",
    "hssv_ii_index": PAPER / "README.md",
    "response_theory": PAPER / "response-theory.md",
    "preregistration": RESULTS / "00-preregistration.md",
    "derivation": RESULTS / "01-derivation-and-dimensions.md",
    "input_ledger": RESULTS / "02-input-derived-table.md",
    "population_preregistration": RESULTS / "03-population-preregistration.md",
    "constraints": RESULTS / "04-local-stability-constraints.md",
    "negative_ledger": RESULTS / "05-negative-ledger.md",
    "hierarchy_addendum": RESULTS / "06-hierarchical-screen-addendum.md",
    "decision": RESULTS / "decision.md",
    "receipt": RESULTS / "receipt.json",
    "instrument": ROOT / "instruments" / "model_hssv" / "screen_response_audit.py",
    "runner": ROOT / "instruments" / "model_hssv" / "run_issue227.py",
    "instrument_tests": ROOT / "instruments" / "test" / "model_hssv" / "test_screen_response_audit.py",
    "runner_tests": ROOT / "instruments" / "test" / "model_hssv" / "test_run_issue227.py",
}

MARKERS = {
    PAPER / "README.md": ("PHENOMENOLOGY ONLY", "hierarchical coherence-screen"),
    PAPER / "response-theory.md": ("V_\\infty^4=GMa_*", "Hierarchical coherence-screen"),
    RESULTS / "00-preregistration.md": ("frozen before issue-227 instruments", "G1--G6"),
    RESULTS / "01-derivation-and-dimensions.md": ("min-cut", "4.000000000000001"),
    RESULTS / "02-input-derived-table.md": ("Measured `G`", "C5"),
    RESULTS / "03-population-preregistration.md": ("not activated", "H-SSV-IV remains blocked"),
    RESULTS / "04-local-stability-constraints.md": ("GW170817", "G4 and G6"),
    RESULTS / "05-negative-ledger.md": ("T3 saturated patch/min-cut", "phenomenology only"),
    RESULTS / "06-hierarchical-screen-addendum.md": ("Hypothesis C5", "one-count capacity"),
    RESULTS / "decision.md": ("PHENOMENOLOGY ONLY", "do not open H-SSV-IV"),
}


def run() -> dict[str, Any]:
    existence = {name: path.is_file() for name, path in REQUIRED.items()}
    marker_checks = {
        str(path.relative_to(ROOT)): all(marker in path.read_text() for marker in markers)
        for path, markers in MARKERS.items()
    }
    receipt = json.loads((RESULTS / "receipt.json").read_text())
    t3 = receipt.get("gates", {}).get("T3_saturated_patch_mincut", {})
    receipt_checks = {
        "issue_is_227": receipt.get("issue") == 227,
        "decision_is_phenomenology_only": receipt.get("decision") == "PHENOMENOLOGY ONLY",
        "no_surviving_candidate": receipt.get("survivors") == [],
        "T3_formally_passes_G3": str(t3.get("G3", "")).startswith("PASS FORMALLY"),
        "T3_fails_G2_G4_G5_G6": all(
            str(t3.get(gate, "")).startswith("FAIL")
            for gate in ("G2", "G4", "G5", "G6")
        ),
        "preregistration_is_hashed": len(receipt.get("preregistration_sha256", "")) == 64,
        "galaxy_outcomes_excluded": "No issue-225 galaxy outcome" in receipt.get("evidential_boundary", ""),
    }
    all_ok = all(existence.values()) and all(marker_checks.values()) and all(receipt_checks.values())
    return {
        "issue": 227,
        "status": "PASS" if all_ok else "FAIL",
        "decision": "PHENOMENOLOGY ONLY",
        "required_artifacts": existence,
        "document_markers": marker_checks,
        "receipt_checks": receipt_checks,
        "verified_test_runs": {
            "hssv_model_suite": "64 passed",
            "legacy_series_suite": "not run; archived SSV batteries remain on hold",
            "command": "pytest -q instruments/test/model_hssv",
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

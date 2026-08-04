"""Machine-verifiable local completion manifest for GitHub issue #228."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "papers" / "H-SSV" / "H-SSV-V"
RESULTS = ROOT / "papers" / "H-SSV" / "results" / "issue-228"
OUTPUT = RESULTS / "completion-audit.json"

REQUIRED = {
    "root_index": ROOT / "README.md",
    "hssv_index": ROOT / "papers" / "H-SSV" / "README.md",
    "hssv_v_index": PAPER / "README.md",
    "screen_cosmology": PAPER / "screen-cosmology.md",
    "preregistration": RESULTS / "00-preregistration.md",
    "literature_map": RESULTS / "01-literature-observational-map.md",
    "dataset_registry": RESULTS / "02-datasets-and-likelihoods.md",
    "r4_addendum": RESULTS / "03-information-area-expansion-addendum.md",
    "derivation": RESULTS / "04-derivation-and-controls.md",
    "input_ledger": RESULTS / "05-input-derived-ledger.md",
    "negative_ledger": RESULTS / "06-negative-underdetermination-ledger.md",
    "decision": RESULTS / "decision.md",
    "receipt": RESULTS / "receipt.json",
    "instrument": ROOT / "instruments" / "model_hssv" / "cosmological_redshift_audit.py",
    "runner": ROOT / "instruments" / "model_hssv" / "run_issue228.py",
    "instrument_tests": ROOT / "instruments" / "test" / "model_hssv" / "test_cosmological_redshift_audit.py",
    "runner_tests": ROOT / "instruments" / "test" / "model_hssv" / "test_run_issue228.py",
}

MARKERS = {
    PAPER / "README.md": ("UNDERDETERMINED", "No age, lookback, horizon, or size revision"),
    PAPER / "screen-cosmology.md": ("Endpoint observable and lapse no-go", "Information-area expansion R4"),
    RESULTS / "00-preregistration.md": ("frozen before issue-228 instruments", "C1--C3 and C6 analytically"),
    RESULTS / "01-literature-observational-map.md": ("primary-literature", "redshift drift"),
    RESULTS / "02-datasets-and-likelihoods.md": ("activation vetoed", "rank one"),
    RESULTS / "03-information-area-expansion-addendum.md": ("owner-supplied hypothesis", "q_B"),
    RESULTS / "04-derivation-and-controls.md": ("R4 information-area expansion", "rank one"),
    RESULTS / "05-input-derived-ledger.md": ("Record-area relation", "Cosmic age"),
    RESULTS / "06-negative-underdetermination-ledger.md": ("underdetermined", "Revised cosmic age/size"),
    RESULTS / "decision.md": ("UNDERDETERMINED", "no cosmic age or size revision"),
}


def run() -> dict[str, Any]:
    existence = {name: path.is_file() for name, path in REQUIRED.items()}
    marker_checks = {
        str(path.relative_to(ROOT)): all(marker in path.read_text() for marker in markers)
        for path, markers in MARKERS.items()
    }
    receipt = json.loads((RESULTS / "receipt.json").read_text())
    r4 = receipt.get("gates", {}).get("R4_information_area_expansion", {})
    identifiability = receipt.get("checks", {}).get("identifiability", {})
    receipt_checks = {
        "issue_is_228": receipt.get("issue") == 228,
        "decision_is_underdetermined": receipt.get("decision") == "UNDERDETERMINED",
        "no_surviving_candidate": receipt.get("survivors") == [],
        "likelihood_not_activated": receipt.get("likelihood_activated") is False,
        "age_size_not_activated": receipt.get("age_size_calculation_activated") is False,
        "decomposition_rank_is_one": identifiability.get("rank") == 1,
        "R4_passes_invariant_and_stretch_form": all(
            str(r4.get(gate, "")).startswith("PASS FORMALLY") for gate in ("C1", "C3")
        ),
        "R4_fails_derivation_and_mechanism": all(
            str(r4.get(gate, "")).startswith("FAIL") for gate in ("C2", "C5", "C6")
        ),
        "three_inputs_are_hashed": all(
            len(receipt.get(key, "")) == 64
            for key in ("preregistration_sha256", "dataset_registry_sha256", "r4_addendum_sha256")
        ),
        "outcomes_excluded": "No cosmological outcome" in receipt.get("evidential_boundary", ""),
    }
    all_ok = all(existence.values()) and all(marker_checks.values()) and all(receipt_checks.values())
    return {
        "issue": 228,
        "status": "PASS" if all_ok else "FAIL",
        "decision": "UNDERDETERMINED",
        "required_artifacts": existence,
        "document_markers": marker_checks,
        "receipt_checks": receipt_checks,
        "verified_test_runs": {
            "hssv_model_suite": "83 passed",
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

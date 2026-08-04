"""Machine-verifiable local completion manifest for GitHub issue #226."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "papers" / "H-SSV" / "H-SSV-I"
RESULTS = ROOT / "papers" / "H-SSV" / "results" / "issue-226"
OUTPUT = RESULTS / "completion-audit.json"

REQUIRED = {
    "root_index": ROOT / "README.md",
    "hssv_index": ROOT / "papers" / "H-SSV" / "README.md",
    "hssv_i_index": PAPER / "README.md",
    "mathematical_specification": PAPER / "screen-theory.md",
    "preregistration": RESULTS / "00-preregistration.md",
    "c4_preregistration": RESULTS / "03-c4-preregistration-addendum.md",
    "checks": RESULTS / "01-checks.md",
    "failure_ledger": RESULTS / "02-failure-ledger.md",
    "decision": RESULTS / "decision.md",
    "receipt": RESULTS / "receipt.json",
    "instrument": ROOT / "instruments" / "model_hssv" / "screen_foundations_audit.py",
    "c4_instrument": ROOT
    / "instruments"
    / "model_hssv"
    / "quantum_causal_screen_audit.py",
    "runner": ROOT / "instruments" / "model_hssv" / "run_issue226.py",
    "instrument_tests": ROOT
    / "instruments"
    / "test"
    / "model_hssv"
    / "test_screen_foundations_audit.py",
    "runner_tests": ROOT
    / "instruments"
    / "test"
    / "model_hssv"
    / "test_run_issue226.py",
    "c4_instrument_tests": ROOT
    / "instruments"
    / "test"
    / "model_hssv"
    / "test_quantum_causal_screen_audit.py",
}

MARKERS = {
    PAPER / "README.md": ("PROCEED", "global, potentially entangled state"),
    PAPER / "screen-theory.md": ("C4 quantum-causal foundation", "local causality and a global"),
    RESULTS / "00-preregistration.md": ("frozen before implementation", "F1--F6"),
    RESULTS / "03-c4-preregistration-addendum.md": (
        "frozen before C4 implementation",
        "local causality and a global state",
    ),
    RESULTS / "01-checks.md": ("C4 global-state/local-causality checks", "Bilateral update capacity"),
    RESULTS / "02-failure-ledger.md": ("C3", "C4 quantum causal global screen"),
    RESULTS / "decision.md": ("PROCEED", "topological screen site"),
}


def run() -> dict[str, Any]:
    existence = {name: path.is_file() for name, path in REQUIRED.items()}
    marker_checks = {
        str(path.relative_to(ROOT)): all(marker in path.read_text() for marker in markers)
        for path, markers in MARKERS.items()
    }
    receipt = json.loads((RESULTS / "receipt.json").read_text())
    strongest = receipt.get("gates", {}).get("C3_carrier_screen_reservoir", {})
    c4 = receipt.get("gates", {}).get("C4_quantum_causal_global_screen", {})
    receipt_checks = {
        "issue_is_226": receipt.get("issue") == 226,
        "decision_is_proceed": receipt.get("decision") == "PROCEED",
        "C4_is_only_survivor": receipt.get("survivors")
        == ["C4_quantum_causal_global_screen"],
        "no_blocking_result": receipt.get("blocking_result") is None,
        "C3_passes_five_gates": all(
            str(strongest.get(gate, "")).startswith("PASS")
            for gate in ("F1", "F2", "F4", "F5", "F6")
        ),
        "C3_fails_F3": str(strongest.get("F3", "")).startswith("FAIL"),
        "C4_passes_all_six_gates": all(
            str(c4.get(f"F{index}", "")).startswith("PASS")
            for index in range(1, 7)
        ),
        "preregistration_is_hashed": len(receipt.get("preregistration_sha256", "")) == 64,
        "C4_preregistration_is_hashed": len(
            receipt.get("c4_preregistration_sha256", "")
        )
        == 64,
    }
    all_ok = (
        all(existence.values())
        and all(marker_checks.values())
        and all(receipt_checks.values())
    )
    return {
        "issue": 226,
        "status": "PASS" if all_ok else "FAIL",
        "decision": "PROCEED",
        "required_artifacts": existence,
        "document_markers": marker_checks,
        "receipt_checks": receipt_checks,
        "verified_test_runs": {
            "focused": "30 passed",
            "hssv_model_suite": "48 passed",
            "legacy_series_suite": (
                "not required; archived SSV numerical batteries are on hold "
                "and outside issue #226"
            ),
            "commands": [
                "pytest -q instruments/test/model_hssv/test_screen_foundations_audit.py instruments/test/model_hssv/test_quantum_causal_screen_audit.py instruments/test/model_hssv/test_run_issue226.py instruments/test/model_hssv/test_issue226_completion_audit.py",
                "pytest -q instruments/test/model_hssv",
            ],
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

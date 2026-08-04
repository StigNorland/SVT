"""Receipt tests for the issue-226 runner."""

import os
import sys

SRC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv"
)
sys.path.insert(0, os.path.abspath(SRC))

import run_issue226  # noqa: E402


def test_issue226_receipt_has_both_preregistration_hashes_and_c4_survivor():
    report = run_issue226.run_all()
    assert report["issue"] == 226
    assert report["decision"] == "PROCEED"
    assert report["survivors"] == ["C4_quantum_causal_global_screen"]
    assert len(report["preregistration_sha256"]) == 64
    assert len(report["c4_preregistration_sha256"]) == 64
    assert report["blocking_result"] is None
    assert report["gates"]["C4_quantum_causal_global_screen"]["F3"].startswith(
        "PASS"
    )
    assert "No galaxy" in report["evidential_boundary"]

"""Receipt tests for issue #227."""

import os
import sys

SRC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv"
)
sys.path.insert(0, os.path.abspath(SRC))

import run_issue227  # noqa: E402


def test_issue227_receipt_is_hash_pinned_and_does_not_open_galaxy_data():
    report = run_issue227.run_all()
    assert report["issue"] == 227
    assert report["decision"] == "PHENOMENOLOGY ONLY"
    assert report["survivors"] == []
    assert len(report["preregistration_sha256"]) == 64
    assert "No issue-225 galaxy outcome" in report["evidential_boundary"]

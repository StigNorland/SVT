"""Receipt tests for issue #228."""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import run_issue228  # noqa: E402


def test_runner_hashes_frozen_inputs_and_excludes_outcomes():
    report = run_issue228.run_all()
    assert report["issue"] == 228
    assert report["decision"] == "UNDERDETERMINED"
    assert len(report["preregistration_sha256"]) == 64
    assert len(report["dataset_registry_sha256"]) == 64
    assert len(report["r4_addendum_sha256"]) == 64
    assert "No cosmological outcome" in report["evidential_boundary"]
    assert not report["likelihood_activated"]

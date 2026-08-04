"""Ensure the issue-228 artifact set is locally complete."""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import issue228_completion_audit  # noqa: E402


def test_issue228_completion_manifest_passes():
    report = issue228_completion_audit.run()
    assert report["status"] == "PASS"
    assert report["decision"] == "UNDERDETERMINED"
    assert all(report["required_artifacts"].values())
    assert all(report["document_markers"].values())
    assert all(report["receipt_checks"].values())

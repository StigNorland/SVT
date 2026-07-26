"""Ensure the issue-180 promised artifact set is complete."""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import completion_audit  # noqa: E402


def test_completion_manifest_passes():
    report = completion_audit.run()
    assert report["status"] == "PASS"
    assert all(report["required_artifacts"].values())
    assert all(report["document_markers"].values())
    assert all(report["receipt_checks"].values())
    assert report["publication"]["issue_state"] == "closed"
    assert report["publication"]["pull_request"] == 181

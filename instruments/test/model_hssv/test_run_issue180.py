"""End-to-end receipt decision test for issue #180."""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import run_issue180  # noqa: E402


def test_combined_decision_propagates_upstream_failures():
    report = run_issue180.run_all()
    assert report["decision"] == "K3"
    assert report["gates"]["P0"].startswith("FAIL")
    assert report["gates"]["P1"].startswith("FAIL")
    assert report["gates"]["P2"].startswith("PASS FORMALLY")
    assert report["gates"]["P3"].startswith("FAIL")
    assert report["gates"]["P5"].startswith("NOT REACHED")

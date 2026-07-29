"""Regression tests for the issue #166 reconstruction audit."""

import os
import sys


SRC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_screen"
)
sys.path.insert(0, os.path.abspath(SRC))

import reconstruction_audit as audit  # noqa: E402


def test_blind_null_control_detects_changed_supplied_kernel():
    result = audit.data_dependency_probe(L=32)
    assert result["control_detects_supplied_kernel_change"] is True
    assert abs(result["control_massless_power"] - 2.0) < 0.35
    assert result["control_gapped_yukawa_rate"] > 0.3


def test_subcalc4_t2_does_not_invert_measured_screen_polarisation():
    result = audit.data_dependency_probe(L=32)
    assert result["greens_function_kernel_arguments_in_run"] == [
        "k2",
        "M * M + k2",
    ]
    assert result["measured_screen_polarisation_enters_T2"] is False
    assert result["claimed_T2_change"] == 0.0


def test_theorem_artifact_search_is_reproducible_and_complete():
    ledger = audit.theorem_premise_ledger()
    assert ledger["corpus_file_count"] == 8
    assert len(ledger["queries"]) == 4
    assert ledger["missing_premises"]


def test_calculations_mix_dimensions_without_a_state_map():
    premise = audit.theorem_premise_ledger()["premises"][
        "one_common_state_space_and_dimension"
    ]
    assert premise["present"] is False
    assert premise["dimensions_mixed"] is True


def test_preregistered_negative_decisions_fire():
    report = audit.run(L=32)
    assert report["controls_ok"] is True
    assert report["D1_clean_negative_subcalc4"] is True
    assert report["D2_theorem_not_applicable"] is True
    assert report["decision"].startswith("D1+D2")

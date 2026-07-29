"""Fast interpretation tests for the stored SSV-VIII Kibble--Zurek scan."""

import json
import math
from pathlib import Path

from paper_viii.kibble_zurek_gpe import summarize_scan


RECEIPT = (
    Path(__file__).resolve().parents[2]
    / "paper_viii"
    / "kibble_zurek_results.json"
)


def test_stored_scan_fit_and_uncertainty_are_reproducible_without_rerunning():
    stored = json.loads(RECEIPT.read_text(encoding="utf-8"))
    summary = summarize_scan(stored["scan"])

    assert math.isclose(
        summary["fitted_alpha_2D"],
        stored["fitted_alpha_2D"],
        rel_tol=1e-12,
    )
    assert math.isclose(
        summary["fitted_alpha_2D_std_error"],
        stored["fitted_alpha_2D_std_error"],
        rel_tol=1e-12,
    )


def test_observation_inversion_is_never_labelled_as_a_prediction():
    stored = json.loads(RECEIPT.read_text(encoding="utf-8"))
    summary = summarize_scan(stored["scan"])

    assert summary["eta_status"] == (
        "observational input; not predicted by this scan"
    )
    assert summary["scaling_status"].startswith("inconclusive")
    assert "eta_predicted_MF" not in stored
    assert "cosmological_tau_Q_over_tau_0" not in stored

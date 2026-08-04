"""Tests for the preregistered H-SSV-I foundation gates."""

import os
import sys

import pytest

SRC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv"
)
sys.path.insert(0, os.path.abspath(SRC))

import screen_foundations_audit as audit  # noqa: E402


def test_dimensions_close_and_information_quantities_are_distinct():
    result = audit.dimensional_audit()
    assert result["equation_consistent"]
    assert result["memory_law_consistent"]
    assert result["capacity_is_not_rate"]
    assert len({tuple(value) for value in result["equation_terms"].values()}) == 1


def test_screen_principal_cone_is_hyperbolic_and_subluminal():
    result = audit.characteristic_audit()
    assert result["hyperbolic"]
    assert result["subluminal"]
    assert result["screen_speed"] == pytest.approx(0.5)


@pytest.mark.parametrize(
    "kwargs", [{"inertia": 0.0}, {"tension": 0.0}, {"light_speed": 0.0}]
)
def test_characteristic_audit_rejects_nonpositive_inputs(kwargs):
    with pytest.raises(ValueError):
        audit.characteristic_audit(**kwargs)


def test_undamped_candidate_has_resonant_secular_growth():
    result = audit.resonant_control()
    assert result["secular"]
    assert result["amplitude_at_t20"] == pytest.approx(
        2.0 * result["amplitude_at_t10"]
    )


def test_positive_damping_bounds_static_and_periodic_response_at_resonance():
    result = audit.damped_response_audit()
    assert result["bounded_static"]
    assert result["bounded_periodic"]
    assert result["denominator_sq"] > 0.0


def test_reservoir_closes_the_damping_energy_ledger():
    result = audit.conservation_ledger_audit()
    assert result["closes"]
    assert abs(result["total_rate"]) <= 1.0e-12
    assert not result["damping_without_reservoir_closes"]
    assert result["reservoir_rate"] > 0.0


def test_saturating_memory_is_bounded_and_reaches_exact_equilibrium():
    result = audit.memory_audit()
    assert result["bounded"]
    assert result["converged"]
    assert result["equilibrium"] == pytest.approx(result["analytic_equilibrium"])
    assert 0.0 <= result["minimum_sample"] <= result["maximum_sample"] <= 5.0


@pytest.mark.parametrize(
    "kwargs",
    [
        {"capacity": 0.0},
        {"write_rate": -1.0},
        {"relaxation_time": 0.0},
        {"initial": 6.0},
    ],
)
def test_memory_audit_rejects_unphysical_inputs(kwargs):
    with pytest.raises(ValueError):
        audit.memory_audit(**kwargs)


def test_coordinate_speed_fails_but_screen_relative_scalar_is_invariant():
    result = audit.observer_audit()
    assert not result["coordinate_source_invariant"]
    assert result["relative_gamma_invariant"]
    assert result["preferred_structure_remains"]


def test_positive_sources_do_not_phase_cancel_and_make_falsifier():
    result = audit.sign_and_prediction_audit()
    assert result["all_positive"]
    assert not result["phase_cancellation_possible"]
    assert result["null_result_falsifies_relocation_loading_if_g_r_positive"]


def test_no_candidate_survives_all_six_gates():
    report = audit.run()
    assert report["decision"] == "REVISE"
    assert report["survivors"] == []
    assert report["blocking_result"]["gate"] == "F3"
    assert report["gates"]["C3_carrier_screen_reservoir"]["F3"].startswith(
        "FAIL"
    )
    for gate in ("F1", "F2", "F4", "F5", "F6"):
        assert report["gates"]["C3_carrier_screen_reservoir"][gate].startswith(
            "PASS"
        )

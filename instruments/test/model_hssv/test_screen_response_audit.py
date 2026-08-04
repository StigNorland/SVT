"""Tests for the preregistered issue-227 screen-response controls."""

import os
import sys

import numpy as np
import pytest

SRC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv"
)
sys.path.insert(0, os.path.abspath(SRC))

import screen_response_audit as audit  # noqa: E402


def test_capacity_construction_dimensions_close():
    result = audit.dimensional_audit()
    assert result["accelerations_match"]
    assert result["velocity_squared_matches"]
    assert result["service_acceleration"] == [0, 1, -2]
    assert result["core_radius"] == [0, 1, 0]


def test_local_three_dimensional_flux_is_inverse_square_and_conserved():
    result = audit.local_flux_control()
    assert result["conserved"]
    assert result["radial_power"] == -2
    assert result["gauss_reconstruction"] == pytest.approx(result["demand"])
    assert audit.local_3d_acceleration(4.0, 2.0, G=3.0) == pytest.approx(3.0)


@pytest.mark.parametrize(
    "mass,radius,G", [(0.0, 1.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 0.0)]
)
def test_local_acceleration_rejects_nonpositive_inputs(mass, radius, G):
    with pytest.raises(ValueError):
        audit.local_3d_acceleration(mass, radius, G)


def test_linear_two_dimensional_source_has_wrong_btfr_exponent():
    result = audit.mass_scaling_audit()
    assert result["linear_2d_velocity_mass_exponent"] == pytest.approx(0.5)
    assert result["linear_2d_M_vs_V_slope"] == pytest.approx(2.0)
    assert result["linear_2d_fails_btfr"]


def test_saturated_two_dimensional_mincut_has_btfr_exponent_four():
    result = audit.mass_scaling_audit()
    assert result["mincut_velocity_mass_exponent"] == pytest.approx(0.25)
    assert result["mincut_M_vs_V_slope"] == pytest.approx(4.0)
    assert result["mincut_passes_btfr_exponent"]


def test_matched_capacity_scales_close_btfr_identity():
    masses = np.logspace(7, 12, 9)
    a_star = 2.3
    G = 4.7
    radii, v2 = audit.matched_capacity_scales(masses, a_star, G)
    assert np.allclose(radii**2, G * masses / a_star)
    assert np.allclose(v2**2, G * masses * a_star)
    assert np.allclose(v2**2 / (G * masses), a_star)


def test_microscopic_closure_can_be_stated_but_is_not_automatic():
    ell = 2.0
    mass_site = 5.0
    nu = 3.0
    G = 1.0
    a_capacity = np.pi * G * mass_site / ell**2
    tau_match = a_capacity * ell / (audit.C_LIGHT**2 * nu)
    matched = audit.microscopic_capacity_scales(
        mass=100.0,
        ell_site=ell,
        mass_site=mass_site,
        nu_site=nu,
        response_time=tau_match,
        G=G,
    )
    assert matched["closure_ratio_a_service_over_a_capacity"] == pytest.approx(1.0)
    unmatched = audit.microscopic_capacity_scales(
        mass=100.0,
        ell_site=ell,
        mass_site=mass_site,
        nu_site=nu,
        response_time=2.0 * tau_match,
        G=G,
    )
    assert unmatched["closure_ratio_a_service_over_a_capacity"] == pytest.approx(2.0)


def test_two_positive_normalized_regulators_share_limits_but_differ_at_core():
    result = audit.regulator_nonuniqueness_audit()
    assert result["cored_log_kernel_norm"] == pytest.approx(1.0, rel=2.0e-7)
    assert result["gaussian_kernel_norm"] == pytest.approx(1.0, rel=2.0e-7)
    assert result["both_linear_at_origin"]
    assert result["both_flat_curve_asymptote"]
    assert result["relative_difference_at_core"] > 0.2
    assert result["C4_does_not_select_regulator"]


def test_exact_availability_respects_c4_identity_on_finite_domain():
    result = audit.exact_availability_audit()
    assert result["potential_nonpositive"]
    assert result["availability_valid"]
    assert result["load_valid"]
    assert result["exact_C4_identity"]
    assert result["acceleration"] > 0.0


def test_conditional_solar_scale_is_not_misreported_as_derivation():
    result = audit.conditional_solar_audit()
    assert result["comparison_only_a_star_m_s2"] == audit.A_COMPARISON
    assert 6.0e3 < result["solar_core_radius_AU"] < 8.0e3
    assert result["rows"]["Earth"]["screen_fraction"] < 1.0e-11
    assert result["external_field_Q2_prediction"] is None


def test_gw_speed_upper_bound_does_not_pass_measured_equality_constraint():
    result = audit.dynamic_constraint_audit()
    assert result["C4_speed_statement"] == "c_screen <= c"
    assert not result["speed_equality_derived"]
    assert not result["binary_radiation_action_supplied"]
    assert not result["G6_pass"]


def test_issue227_decision_is_phenomenology_only():
    report = audit.run()
    assert report["decision"] == "PHENOMENOLOGY ONLY"
    assert report["survivors"] == []
    assert report["gates"]["T3_saturated_patch_mincut"]["G3"].startswith(
        "PASS FORMALLY"
    )
    assert report["gates"]["T3_saturated_patch_mincut"]["G2"].startswith(
        "FAIL DERIVATION"
    )
    assert "a_s = a_c closure" in report["input_vs_derived"]["not_derived"]

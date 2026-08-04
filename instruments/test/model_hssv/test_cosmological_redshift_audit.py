"""Focused tests for the issue-228 invariant redshift audit."""

import os
import sys

import numpy as np
import pytest

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import cosmological_redshift_audit as audit  # noqa: E402


def test_dimensions_distinguish_energy_flux_from_write_rate():
    result = audit.dimensional_audit()
    assert result["sqrt_G_u_over_c2_is_rate"]
    assert result["energy_flux_is_not_write_rate"]


def test_homogeneous_lapse_is_removable_and_has_no_redshift():
    first = audit.lapse_only_audit(0.2, 3.0)
    second = audit.lapse_only_audit(2.0, 0.4)
    assert first["one_plus_z"] == second["one_plus_z"] == 1.0
    assert first["coordinate_removable"]
    assert not first["C1_pass"]


@pytest.mark.parametrize("bad", [0.0, -1.0])
def test_lapse_rejects_nonpositive_values(bad):
    with pytest.raises(ValueError):
        audit.lapse_only_audit(bad, 1.0)


def test_energy_only_redshift_fails_time_stretching_and_duality():
    result = audit.energy_only_path_loss(3.0, np.log(2.0) / 3.0)
    assert result["one_plus_z"] == pytest.approx(2.0)
    assert result["duration_ratio_observed_over_emitted"] == 1.0
    assert not result["C3_pass"]
    assert result["distance_duality_eta"] == pytest.approx(2.0 ** -1.5)
    assert result["surface_brightness_exponent"] == -1


def test_coherent_dilation_stretches_but_needs_spatial_response():
    result = audit.coherent_wavepacket_dilation(3.0, distance=2.0)
    assert result["frequency_ratio_observed_over_emitted"] == pytest.approx(1 / 3)
    assert result["duration_ratio_observed_over_emitted"] == 3.0
    assert result["wavepacket_norm_ratio"] == 1.0
    assert result["distance_duality_eta"] == pytest.approx(1 / 3)
    assert result["surface_brightness_exponent"] == -2
    assert result["spatial_completion_required"]


def test_scalar_energy_ledger_closes_but_does_not_supply_hamiltonian():
    result = audit.photon_screen_energy_ledger(12.0, 4.0)
    assert result["photon_energy_final"] == 3.0
    assert result["screen_energy_gain"] == 9.0
    assert result["scalar_energy_closes"]
    assert not result["screen_hamiltonian_derived"]
    assert not result["C2_pass"]


def test_spatial_metric_redshift_uses_B_not_removable_lapse():
    first = audit.spatial_metric_response(1.0, 2.5, 0.2, 4.0)
    second = audit.spatial_metric_response(1.0, 2.5, 5.0, 0.1)
    assert first["one_plus_z"] == second["one_plus_z"] == 2.5
    assert first["duration_ratio"] == 2.5
    assert first["distance_duality_eta"] == 1.0
    assert first["surface_brightness_exponent"] == -4


def test_blackbody_shape_is_only_conditionally_preserved():
    result = audit.blackbody_mapping(8.175, 3.0)
    assert result["temperature_observed"] == pytest.approx(2.725)
    assert result["planck_dimensionless_frequency_invariant"]
    assert "condition" in result


def test_information_area_growth_sets_redshift_and_stretch():
    result = audit.information_area_redshift(4.0, 36.0)
    assert result["one_plus_z"] == 3.0
    assert result["duration_ratio"] == 3.0
    assert not result["record_growth_law_derived"]
    assert not result["global_entropy_interpretation_allowed"]


def test_constant_record_production_is_decelerating_with_q_one():
    result = audit.information_area_kinematics(20.0, 3.0, 0.0)
    assert result["decelerating"]
    assert result["q_screen"] == pytest.approx(1.0)
    assert result["constant_record_rate"]


@pytest.mark.parametrize(
    ("p", "expected_q", "decelerating"),
    [(1.0, 1.0, True), (2.0, 0.0, False), (4.0, -0.5, False)],
)
def test_power_law_record_growth_has_frozen_acceleration_sign(p, expected_q, decelerating):
    result = audit.power_law_record_kinematics(p)
    assert result["q_screen"] == pytest.approx(expected_q)
    assert result["decelerating"] is decelerating


def test_geometry_wake_decomposition_is_rank_deficient():
    result = audit.identifiability_audit()
    assert result["rank"] == 1
    assert result["parameters"] == 2
    assert not result["full_rank"]
    assert result["BW_gauge_invariance"]
    assert not result["C6_pass"]


def test_redshift_drift_depends_only_on_effective_sum():
    first = audit.redshift_drift(2.0, 0.7 + 0.3, 1.1 + 0.4)
    second = audit.redshift_drift(2.0, 0.2 + 0.8, 0.6 + 0.9)
    assert first == pytest.approx(second)


def test_decision_is_underdetermined_and_age_gate_stays_closed():
    result = audit.run()
    assert result["decision"] == "UNDERDETERMINED"
    assert result["survivors"] == []
    assert result["strongest_candidate"] == "R3_optical_spatial_completion"
    assert not result["likelihood_activated"]
    assert not result["age_size_calculation_activated"]

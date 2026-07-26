"""Closure tests for the minimal covariant LogSE parent (#180)."""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import relativistic_logse_bridge as bridge  # noqa: E402


def test_covariant_interaction_maps_exactly_to_target_coefficient():
    m, B, q0 = 3.0, 0.2, 1.7
    q = 2.3
    mapped = bridge.interaction_derivative(q, m, B, q0) / (2.0 * m)
    assert np.isclose(mapped, -B * np.log(q / q0), rtol=0.0, atol=1e-14)
    assert bridge.nr_log_coefficient(m, B) == -B


def test_exact_target_sign_makes_parent_unbounded():
    assert bridge.potential_bounded_below(0.1) is False
    qs = np.array([1e2, 1e4, 1e8])
    values = bridge.interaction_potential(qs, 1.0, 0.1)
    assert np.all(np.diff(values) < 0.0)


def test_relativistic_target_background_has_unstable_goldstone():
    m, B = 1.0, 0.1
    assert bridge.massive_gap2(m, B) > 0.0
    assert bridge.goldstone_c2(m, B) < 0.0
    ks = np.array([1e-4, 1e-3, 1e-2])
    gapless, gapped = bridge.dispersion_omega2(ks, m, B)
    assert np.all(gapless < 0.0)
    assert np.all(gapped > 0.0)


def test_closed_form_roots_satisfy_independent_fluctuation_determinant():
    m, B = 1.7, 0.2
    ks = np.array([0.05, 0.2, 0.4, 0.8])
    gapless, gapped = bridge.dispersion_omega2(ks, m, B)
    scale = (m * m + ks * ks) ** 2
    for branch in (gapless, gapped):
        residual = bridge.dispersion_polynomial_residual(ks, m, B, branch)
        assert np.max(np.abs(residual) / scale) < 1e-12


def test_no_quadratically_silent_saturation_term_can_reverse_compressibility():
    # Literal target has mu'(n0)<0. Preserving it forces delta mu'=0, which
    # cannot make the sum positive.
    assert bridge.saturation_can_preserve_target_and_stabilize(-0.2, 0.0) is False
    # A large enough correction stabilizes only by changing the target.
    assert bridge.saturation_can_preserve_target_and_stabilize(-0.2, 0.3) is False


def test_sign_reversed_control_is_stable_but_not_literal_ssv():
    m, B = 1.0, -0.1
    assert bridge.potential_bounded_below(B) is True
    assert 0.0 < bridge.goldstone_c2(m, B) < 1.0
    ks = np.linspace(0.0, 0.5, 20)
    gapless, gapped = bridge.dispersion_omega2(ks, m, B)
    assert np.all(gapless >= -1e-14)
    assert np.all(gapped > 0.0)


def test_stable_control_cannot_share_light_cone_in_controlled_nr_regime():
    assert bridge.common_cone_possible_in_controlled_nr_limit(1.0, -0.01) is False
    assert bridge.goldstone_c2(1.0, -1e6) < 1.0


def test_envelope_remainder_has_expected_linear_suppression():
    ratios = [bridge.envelope_remainder_ratio(e, 1.0)
              for e in (0.2, 0.1, 0.05, 0.025)]
    assert np.allclose(np.array(ratios[:-1]) / np.array(ratios[1:]), 2.0)

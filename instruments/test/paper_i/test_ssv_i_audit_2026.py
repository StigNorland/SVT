"""Tests for #183 — every SSV-I E-gate finding, machine-checked.

These lock in *negative* results. A failure here means either the finding was
wrong or the paper changed; both require re-opening the damage report, never a
silent edit of the tolerance.
"""

import sys
from pathlib import Path

import mpmath as mp
import pytest

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from ssv_i_audit_2026 import (  # noqa: E402
    ALPHA,
    A_BOHR,
    M_E,
    R_E_CLASSICAL,
    b_rho0_from_source_constraint,
    elliptic_leading_constant,
    elliptic_residual_coefficient,
    healing_length,
    lamb_ring_energy_bracket,
    lambda_param,
    rho0_as_printed,
    rho0_asserted_value,
    rho0_natural_units,
    sound_speed_squared,
    ssv_elliptic_bracket,
    stationary_radius,
    xi_over_alpha,
)


# ---------------------------------------------------------------- D1
def test_d1_both_sound_speed_routes_agree_identically():
    """The 'thermodynamic vs Bogoliubov factor-2 discrepancy' does not exist."""
    bog, thermo = sound_speed_squared(mp.mpf("3.7"), mp.mpf("1.3"))
    assert bog == thermo


def test_d1_printed_sign_gives_negative_sound_speed_squared():
    """SSV-I's printed sign makes the uniform vacuum modulationally unstable."""
    bog, _ = sound_speed_squared(mp.mpf("3.7"), mp.mpf("1.3"), sign=-1)
    assert bog < 0


def test_d1_source_constraint_has_no_factor_two():
    """rho|F'| = m c^2  =>  |b| rho_0 = m_0 c^2, not m_0 c^2 / 2."""
    from ssv_i_audit_2026 import C
    assert b_rho0_from_source_constraint(M_E) == M_E * C**2


def test_d1_healing_length_is_compton_over_sqrt2():
    """xi = hbar/sqrt(2 m |b| rho_0) with |b|rho_0 = m c^2 gives hbar/(sqrt2 m c),
    NOT the printed hbar/(m c)."""
    from ssv_i_audit_2026 import C, HBAR
    xi = healing_length(b_rho0_from_source_constraint(M_E), M_E)
    assert mp.almosteq(xi, HBAR / (mp.sqrt(2) * M_E * C), rel_eps=mp.mpf("1e-25"))


# ---------------------------------------------------------------- E1
@pytest.mark.parametrize("t,places", [("1e-3", 7), ("1e-4", 8), ("1e-5", 9)])
def test_e1_next_order_coefficient_is_three_sixteenths(t, places):
    """Not the printed 1/8, and it multiplies (ln(8R/a) - 1), so it is not a
    'pure geometric constant'."""
    got = elliptic_residual_coefficient(mp.mpf(t))
    assert mp.almosteq(got, mp.mpf(3) / 16, abs_eps=mp.mpf(10) ** (-places))


def test_e1_C_is_negligible_for_the_alpha_result():
    """r* is insensitive to C at the O(alpha^2) level: even C=1 moves it <2e-4."""
    chiral = lambda_param() + 1
    r_none = stationary_radius(chiral, C_coeff=mp.mpf(0))
    r_one = stationary_radius(chiral, C_coeff=mp.mpf(1))
    assert abs(r_one - r_none) / r_none < mp.mpf("2e-4")


# ---------------------------------------------------------------- E2
def test_e2_appendix_leading_term_is_minus_two_not_minus_seven_quarters():
    """The appendix's elliptic formula cannot recover eq:Ekin: different core."""
    t = mp.mpf("1e-6")
    leading = ssv_elliptic_bracket(t) - mp.log(8 / t)
    assert mp.almosteq(leading, -elliptic_leading_constant(), abs_eps=mp.mpf("1e-10"))
    assert elliptic_leading_constant() != lamb_ring_energy_bracket()


def test_e2_lamb_constant_is_seven_quarters():
    """Lamb Art. 163 (6), uniform-vorticity circular core -- matches eq:Ekin."""
    assert lamb_ring_energy_bracket() == mp.mpf(7) / 4


# ---------------------------------------------------------------- E3
def test_e3_as_printed_the_functional_does_not_give_one_over_alpha():
    """eq:Etotal applies alpha^2 twice; its stationary point is ~0.57."""
    r = stationary_radius((lambda_param() + 1) * ALPHA**2, guess=mp.mpf("0.5"))
    assert r < 1
    assert abs(r - mp.mpf("0.5706")) < mp.mpf("1e-3")


def test_e3_removing_the_spurious_alpha_squared_restores_the_result():
    r = stationary_radius(lambda_param() + 1)
    assert abs(r - 1 / ALPHA) / (1 / ALPHA) < mp.mpf("2e-5")


# ---------------------------------------------------------------- E4
def test_e4_xi_over_alpha_is_the_bohr_radius():
    assert mp.almosteq(xi_over_alpha(), A_BOHR, rel_eps=mp.mpf("1e-8"))


def test_e4_xi_over_alpha_is_not_the_classical_electron_radius():
    """They differ by exactly 1/alpha^2."""
    ratio = xi_over_alpha() / R_E_CLASSICAL
    assert mp.almosteq(ratio, 1 / ALPHA**2, rel_eps=mp.mpf("1e-6"))
    assert ratio > 1e4


# ---------------------------------------------------------------- E5
def test_e5_route1_rho0_value():
    """Route 1: rho_0 = alpha/(2 pi^2 Lambda) in units m_e^4 c^3/hbar^3."""
    expected = ALPHA / (2 * mp.pi**2 * lambda_param())
    assert mp.almosteq(rho0_natural_units(), expected, rel_eps=mp.mpf("1e-20"))


def test_e5_printed_formula_is_four_lambda_squared_too_large():
    ratio = rho0_as_printed() / rho0_natural_units()
    assert mp.almosteq(ratio, 4 * lambda_param() ** 2, rel_eps=mp.mpf("1e-12"))


def test_e5_asserted_number_matches_neither():
    """1.9 agrees with neither its own formula nor the correct inversion."""
    assert rho0_asserted_value() / rho0_as_printed() > 100
    assert rho0_asserted_value() / rho0_natural_units() > 1e4


def test_e5_d1_sqrt2_moves_rho0_by_sqrt2_only():
    """The D1 correction cannot account for the E5 discrepancy."""
    ratio = rho0_natural_units(sqrt2_corrected=True) / rho0_natural_units()
    assert mp.almosteq(ratio, mp.sqrt(2), rel_eps=mp.mpf("1e-20"))

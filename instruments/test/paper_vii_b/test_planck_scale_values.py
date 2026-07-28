"""Tests for SSV-VII-b's Planck-scale identifications (#190, #198 Part A).

Guards the one place in the series where Paper I's D1 sqrt(2) correction reaches
a stated number, and the four values the paper prints for it.

Comparisons go through :func:`rel_close` rather than ``mp.almosteq``: with only
``rel_eps`` supplied, mpmath sets ``abs_eps`` to the same value, so for
quantities of order 1e-35 *every* comparison passes on the absolute test alone
and the assertions prove nothing.  The negative controls below caught exactly
that, which is the reason they are here.
"""

import mpmath as mp
import pytest

from planck_scale_values import (
    C, G_NEWTON, HBAR, correction_factor, fundamental_mass, healing_length,
    planck_length, planck_mass, uncorrected_mass_would_be,
    xi_equals_planck_length,
)


def rel_close(a, b, tol) -> bool:
    """|a/b - 1| < tol.  Purely relative — no absolute-tolerance escape hatch."""
    return abs(mp.mpf(a) / mp.mpf(b) - 1) < mp.mpf(tol)


def test_rel_close_is_not_trivially_true():
    """Guard on the guard: the comparator must distinguish two tiny numbers that
    differ by a factor sqrt(2).  This is the check mp.almosteq silently failed."""
    assert not rel_close(mp.mpf("1e-35"), mp.mpf("1e-35") * mp.sqrt(2), "1e-6")
    assert rel_close(mp.mpf("1e-35"), mp.mpf("1e-35"), "1e-6")


def test_planck_length_matches_codata():
    assert rel_close(planck_length(), "1.616255e-35", "1e-6")


def test_planck_mass_matches_codata():
    assert rel_close(planck_mass(), "2.176434e-8", "1e-6")


def test_fundamental_mass_is_planck_mass_over_root_two():
    assert rel_close(fundamental_mass(), planck_mass() / mp.sqrt(2), "1e-25")
    # the value SSV-VII-b prints
    assert rel_close(fundamental_mass(), "1.538971e-8", "1e-6")


def test_xi_equals_planck_length_after_the_correction():
    """The #190 E1 result: xi = ell_P survives D1 intact, because the sqrt(2) in
    the corrected healing length cancels the one in m_0 = m_P/sqrt(2)."""
    assert xi_equals_planck_length()
    assert rel_close(healing_length(fundamental_mass()), planck_length(), "1e-25")


def test_the_correction_is_exactly_root_two():
    """m_P/m_0 = sqrt(2) — not approximately, and not some other factor."""
    assert rel_close(correction_factor(), mp.sqrt(2), "1e-25")


def test_uncorrected_healing_length_does_not_equal_planck_length():
    """NEGATIVE control.  If the sqrt(2) is dropped, xi(m_0) misses ell_P by
    exactly sqrt(2).  Without this, the test above would pass for a formula that
    had quietly lost the correction."""
    xi_bad = healing_length(fundamental_mass(), sqrt2_corrected=False)
    assert not rel_close(xi_bad, planck_length(), "1e-6")
    assert rel_close(xi_bad / planck_length(), mp.sqrt(2), "1e-25")


def test_m0_is_not_the_planck_mass():
    """NEGATIVE control.  The claim the paper withdrew — 'm_0 = m_P' — is false,
    and false by exactly sqrt(2)."""
    assert not rel_close(fundamental_mass(), uncorrected_mass_would_be(), "1e-6")
    assert rel_close(uncorrected_mass_would_be() / fundamental_mass(),
                     mp.sqrt(2), "1e-25")


def test_G_is_an_input_not_a_derivation():
    """G is a conceded sub-grain input (#155).  It is read from CODATA, and
    ell_P/m_P are derived FROM it — not the other way round.  This test exists so
    the direction of the dependency stays visible in the test suite."""
    assert rel_close(planck_length(), mp.sqrt(HBAR * G_NEWTON / C**3), "1e-25")
    assert rel_close(planck_mass(), mp.sqrt(HBAR * C / G_NEWTON), "1e-25")


@pytest.mark.parametrize("G_alt", ["6.6740e-11", "6.6746e-11"])
def test_identification_is_stable_under_G_uncertainty(G_alt):
    """G's experimental spread does not move the identification: xi = ell_P holds
    for any G, because both sides scale together."""
    G = mp.mpf(G_alt)
    m0 = planck_mass(G) / mp.sqrt(2)
    assert rel_close(healing_length(m0), planck_length(G), "1e-25")

"""Tests for #81 cheap route: the chirality-locking cross term ∫ω_c·ω_w is NOT
forced to vanish (no #76-style selection rule), is positive, and equals the
diagonal L_perp self-energy density when the colour and weak cores coincide."""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

SRC_ROOT = Path(__file__).resolve().parents[1]
for sub in ("paper_i", "paper_ii"):
    p = str(SRC_ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

from vortex_profile import VortexProfile  # noqa: E402
from lr_su4_cross_term_audit import (  # noqa: E402
    R_MAX_RELIABLE,
    analytic_tail,
    compute_cross_integral,
    diagonal_vs_antidiagonal_split,
    sector_cross_energy,
)


@pytest.fixture(scope="module")
def profile():
    vp = VortexProfile.solve(n=2000, x_max=R_MAX_RELIABLE)
    return np.array(vp.xs), np.array(vp.fs), np.array(vp.fps)


def test_cross_integral_is_positive_and_nonzero(profile):
    """(A) The term is ALLOWED — no selection rule kills it (cf. #76 null)."""
    r, f, fp = profile
    i_cross = compute_cross_integral(r, f, fp, R_MAX_RELIABLE)
    assert i_cross > 0.0
    assert i_cross > 1.0          # O(1), not a vanishing remnant


def test_tail_is_negligible(profile):
    """The r>15ξ tail is a tiny fraction of the core integral (reliability bound)."""
    r, f, fp = profile
    i_cross = compute_cross_integral(r, f, fp, R_MAX_RELIABLE)
    assert analytic_tail(R_MAX_RELIABLE) / i_cross < 1.0e-3


def test_cross_equals_diagonal_lperp_density(profile):
    """(B) With f_c=f_w, I_cross equals the diagonal straight-vortex L_perp density
    I_curl = ∫(2ff'/r)²·2πr dr — the locking term is the SAME order as the self-terms."""
    r, f, fp = profile
    mask = r <= R_MAX_RELIABLE
    r_s = np.maximum(r[mask], 1e-12)
    curl_j = 2.0 * f[mask] * fp[mask] / r_s
    i_curl = float(np.trapezoid(curl_j**2 * 2.0 * math.pi * r[mask], r[mask]))
    i_cross = compute_cross_integral(r, f, fp, R_MAX_RELIABLE)
    assert i_cross == pytest.approx(i_curl, rel=1e-12)


def test_diagonal_and_antidiagonal_have_opposite_sign(profile):
    """The ℤ₂×ℤ₂ structure: diagonal (m_c m_w=+1) and anti-diagonal (=−1) are split,
    opposite sign, equal magnitude — so sign(λ_cw) alone picks the ground state."""
    r, f, fp = profile
    i_cross = compute_cross_integral(r, f, fp, R_MAX_RELIABLE)
    split = diagonal_vs_antidiagonal_split(i_cross)
    assert split["diagonal (16)"] == pytest.approx(-split["anti-diagonal"])
    assert split["split |anti−diag|"] == pytest.approx(2.0 * i_cross)


def test_sector_sign_follows_winding_product():
    """ε_cw/λ_cw = m_c m_w I_cross: the diagonal members (++ and −−) agree, the
    anti-diagonal members (+− and −+) agree and are opposite — the ℤ₂×ℤ₂ degeneracy
    the spec predicts."""
    ic = 3.0
    assert sector_cross_energy(+1, +1, ic) == sector_cross_energy(-1, -1, ic)
    assert sector_cross_energy(+1, -1, ic) == sector_cross_energy(-1, +1, ic)
    assert sector_cross_energy(+1, +1, ic) == -sector_cross_energy(+1, -1, ic)

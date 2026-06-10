"""Tests for #119 H9 -- the circulation-halo G triangle vs the BTFR.

Pins (i) the exact Poisson factor in v_flat^2 = G rho0 Gamma^2/(2 pi c^2)
by direct numerical integration of the spherical Poisson equation, (ii) the
alpha_G target identity, and (iii) that the pre-registered verdicts are not
artifacts of the literature inputs: the magnitude gap survives +-50% in the
Fall normalisation and +-30% in the BTFR normalisation, and the slope gap
is exact algebra.
"""

import math
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_iv")
if p not in sys.path:
    sys.path.insert(0, p)

import h9_circulation_halo_triangle as h9  # noqa: E402


def test_poisson_factor_is_one_over_two_pi():
    """Integrate the spherical Poisson equation
    (1/r^2) d/dr (r^2 dPhi/dr) = 4 pi G e/c^2 with e = rho0 Gamma^2/
    (8 pi^2 r^2) numerically (midpoint rule, c = 1 units) and check the
    asymptotic circular speed v^2 = r dPhi/dr against the closed form
    G rho0 Gamma^2/(2 pi)."""
    g, rho0, gamma = 1.3, 2.7, 0.9          # arbitrary positive values
    r0, r1, n = 1.0, 1.0e4, 200_000
    dr = (r1 - r0) / n
    flux = 0.0                              # flux(r) = r^2 Phi'(r)
    for i in range(n):
        r_mid = r0 + (i + 0.5) * dr
        e_mid = rho0 * gamma**2 / (8.0 * math.pi**2 * r_mid**2)
        flux += 4.0 * math.pi * g * e_mid * r_mid**2 * dr
    v_sq_numeric = flux / r1                # v^2 = r Phi' = flux / r
    v_sq_closed = g * rho0 * gamma**2 / (2.0 * math.pi)
    # finite inner boundary contributes O(r0/r1); 1e-4 here
    assert abs(v_sq_numeric - v_sq_closed) / v_sq_closed < 1.0e-3


def test_triangle_inverts_consistently():
    v = h9.v_btfr(h9.M_REF)
    gam = h9.gamma_natural(h9.M_REF, h9.FALL_BETA_PREREG)
    g = h9.g_solved(h9.RHO_GRAIN, gam, v)
    v_back = math.sqrt(h9.v_flat_sq_from_triangle(g, h9.RHO_GRAIN, gam))
    assert abs(v_back - v) / v < 1.0e-12


def test_alpha_g_target_is_the_known_input():
    assert abs(h9.alpha_g(h9.G_NEWTON) - 5.9e-39) / 5.9e-39 < 0.02


def test_reference_velocity_is_btfr_consistent():
    v = h9.v_btfr(h9.M_REF) / 1.0e3
    assert 170.0 < v < 210.0, f"v_BTFR(6e10 Msun) = {v:.1f} km/s out of band"


def test_rule_a_magnitude_gap_is_robust_to_literature_inputs():
    """The pre-registered PASS window is 10^+-2 around 5.9e-39.  The gap on
    the natural chain must remain a FAIL under +-50% Fall normalisation and
    +-30% BTFR normalisation simultaneously -- i.e. the verdict is not an
    artifact of the chosen literature digits."""
    for fall_scale in (0.5, 1.0, 1.5):
        for btfr_scale in (0.7, 1.0, 1.3):
            v = h9.v_btfr(h9.M_REF * btfr_scale)
            gam = h9.gamma_natural(h9.M_REF, h9.FALL_BETA_PREREG) * fall_scale
            a_g = h9.alpha_g(h9.g_solved(h9.RHO_GRAIN, gam, v))
            orders = math.log10(a_g / h9.ALPHA_G_TARGET)
            assert abs(orders) > 2.0, (
                f"magnitude verdict unstable: {orders:+.1f} orders at "
                f"fall x{fall_scale}, btfr x{btfr_scale}")


def test_rule_b_slope_algebra():
    out = h9.run()
    sl = out["rule_b_slope"]
    assert sl["prereg J~M^{5/3}"]["implied_btfr_slope"] == 1.5
    assert not sl["prereg J~M^{5/3}"]["pass_4p0_pm_0p5"]
    assert abs(sl["empirical j~M^{0.55}"]["implied_btfr_slope"]
               - 1.0 / 0.55) < 1.0e-12
    inv = sl["inverse_requirement"]
    assert abs(inv["J_exponent_required"] - 1.25) < 1.0e-12
    assert inv["exponent_gap"] > 0.4


def test_verdict_recorded_as_falsification():
    out = h9.run()
    assert out["verdict"]["rule_a_magnitude"] == "FAIL"
    assert out["verdict"]["rule_b_slope"] == "FAIL"
    assert "FALSIFIED" in out["verdict"]["route"]

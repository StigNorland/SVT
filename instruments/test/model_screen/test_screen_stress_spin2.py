"""Tests for #166 sub-calculation 2 -- the screen spin-2 stress sector.

Validates the instrument, then checks the result:
  (i)   CONTROL C1: the free-scalar stress two-point function is conserved
        (Ward identity / transverse) away from coincidence;
  (ii)  CONTROL C2: massless <TT> ~ 1/r^{2D} (conformal / C_T structure);
  (iii) CONTROL C3: a nonzero spin-2 sector whose plus/cross polarisations swap
        under a 45 deg rotation of the separation (the |n|=2 law);
  (iv)  CONTROL C4: the massive propagator is Yukawa (short-range) with the
        lattice mass -> W and <TT> ~ e^{-2 mu r};
  (v)   the spin-2 two-point is genuinely nonzero (not a named bilinear).
"""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_screen")
sys.path.insert(0, os.path.abspath(SRC))

import screen_stress_spin2 as s  # noqa: E402


def test_control_C1_ward_conservation():
    for rv in (np.array([1.0, 0.3, 0.2, 0.0]), np.array([2.0, -0.5, 0.1, 0.4])):
        assert s.ward_ratio(rv) < 1e-4


def test_control_C2_conformal_power_law():
    vals = [np.abs(s.TT_correlator(s.W_massless(np.array([r, 0, 0, 0.0])))).max()
            * r**(2 * s.D) for r in (1.0, 2.0, 3.0, 5.0)]
    assert np.std(vals) / np.mean(vals) < 1e-6      # constant -> 1/r^{2D}


def test_control_C3_spin2_two_polarisations_swap():
    spp0, sxx0, _ = s.spin2_components(
        s.TT_correlator(s.W_massless(np.array([1.0, 0, 0, 0.0]))))
    spp45, sxx45, _ = s.spin2_components(
        s.TT_correlator(s.W_massless(np.array([np.cos(np.pi / 4),
                                               np.sin(np.pi / 4), 0, 0.0]))))
    assert abs(spp0) > 1e-6                          # spin-2 sector nonzero
    assert abs(spp0 - sxx45) < 1e-9 * abs(spp0)      # plus(0) == cross(45): |n|=2
    assert abs(sxx0 - spp45) < 1e-9 * abs(spp0)


def test_control_C4_massive_is_yukawa_short_range():
    mu, target = s.propagator_yukawa_rate(L=24, m=0.4)
    assert mu > 0.0                                  # short-range (decays)
    assert abs(mu - target) / target < 0.15          # Yukawa mass ~ lattice mass


def test_verdict_controls_pass():
    rep = s.run()
    assert rep["controls_ok"] is True
    assert rep["verdict"].startswith("CONTROL ONLY")
    assert "does not model corrected SSV" in rep["verdict"]

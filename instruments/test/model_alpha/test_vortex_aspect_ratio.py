"""Tests for #163 -- alpha as a vortex aspect ratio (the circularity test).

Checks the load-bearing pieces of the R2 verdict:
  (i)   POSITIVE CONTROL: the thin-core ring energy matches the classic
        Kelvin form E(r) = r(ln 8r - 2);
  (ii)  (B) the pure-LogSE ring energy is monotone increasing for all physical
        r >= 1 -- no stable large-radius equilibrium (collapse);
  (iii) (C) the reduced tension-vs-stabiliser balance sets r* FROM the input
        coupling: coupling_for_target inverts equilibrium_radius, and a small
        coupling = alpha yields no large ring;
  (iv)  (A) circularity: the SSV machinery's aspect ratio is exactly its input
        nondimensionalisation alpha^{-1};
  (v)   the pre-registered verdict is R2 (R1 not met).
"""

import math
import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_alpha")
sys.path.insert(0, os.path.abspath(SRC))

import vortex_aspect_ratio as v  # noqa: E402


def test_positive_control_ring_energy_classic_form():
    for r in (1.0, 5.0, 50.0, 137.0):
        assert abs(v.logse_ring_energy(r) - r * (math.log(8 * r) - 2.0)) < 1e-12


def test_pure_logse_ring_collapses():
    # dE/dr > 0 for every physical radius -> shrinks -> no large stable ring
    r = np.geomspace(1.0, 1e4, 500)
    assert np.all(v.logse_ring_denergy(r) > 0.0)
    assert v.pure_logse_has_stable_large_ring() is False


def test_reduced_balance_r_star_is_set_by_coupling():
    # put a coupling in, get a radius out; invert to recover the same coupling
    for r_target in (10.0, 137.0, 500.0):
        g = v.coupling_for_target(r_target, p=1.0)
        r_star = v.equilibrium_radius(g, p=1.0)
        assert r_star is not None
        assert abs(r_star - r_target) / r_target < 1e-3
    # the coupling needed for 137 is large -- NOT the small alpha
    assert v.coupling_for_target(v.ALPHA_INV) > 1e4
    # a small coupling = alpha does not open a large ring
    assert v.equilibrium_radius(v.ALPHA_TRUE, p=1.0) is None


def test_circularity_aspect_ratio_is_inserted_alpha_inv():
    assert v.circularity_holds() is True
    assert abs(v.ssv_inserted_aspect_ratio(v.ALPHA_TRUE) - v.ALPHA_INV) < 1e-6


def test_verdict_is_R2():
    vd = v.verdict()
    assert vd["R1_derived"] is False
    assert vd["R2_negative"] is True
    assert vd["pure_logse_collapses"] is True
    assert vd["aspect_ratio_is_inserted_alpha_inv"] is True

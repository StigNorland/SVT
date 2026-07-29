"""Tests for #166 sub-calculation 3 -- the induced gravitational polarisation.

Validates the instrument, then checks the result:
  (i)   CONTROL C1: the separated-point <TT> is transverse (Ward) -- the
        precondition for masslessness-by-symmetry (reused from sub-calc 2);
  (ii)  CONTROL C3: the polynomial fit recovers a KNOWN k^2 slope (blind guard,
        so a nonzero c2 is trusted);
  (iii) the raw k^2 coefficient c2(m) is cutoff-DOMINATED (nearly m-independent)
        -- which is WHY the physical part must be isolated as the m^2 term;
  (iv)  the isolated induced Einstein coefficient B = dc2/dm^2 is POSITIVE and
        the k^2 coefficient is LINEAR in m^2 (1/16piG proportional to 1/xi^2);
  (v)   B is stable across lattice size (physical, not a finite-size artifact);
  (vi)  the massive screen's <TT>(x) is exponentially short-range (locality ->
        a LOCAL induced action), and the run-level verdict/controls hold.
"""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_screen")
sys.path.insert(0, os.path.abspath(SRC))

import induced_polarization as ip  # noqa: E402


def test_control_C1_ward_precondition():
    assert ip.control_C1_ward() < 1e-4


def test_control_C3_slope_recovery():
    hat, true = ip.control_C3_slope_recovery()
    assert abs(hat - true) / true < 1e-6


def test_raw_c2_is_cutoff_dominated():
    # The m^2 span is small compared with the lattice contact piece.
    f = ip.mass_slope_fit(32, nwin=4)
    assert f["cutoff_domination_span"] < 0.2
    assert f["A_cutoff"] < 0.0            # raw c2 dominated by the cutoff piece


def test_mass_slope_is_positive_and_linear_in_m2():
    f = ip.mass_slope_fit(32, nwin=4)
    assert f["B_mass_slope"] > 0.0
    assert f["R2_m2"] > 0.99


def test_B_lattice_stable():
    b32 = ip.mass_slope_fit(32, nwin=4)["B_mass_slope"]
    b24 = ip.mass_slope_fit(24, nwin=4)["B_mass_slope"]
    assert abs(b32 - b24) / abs(b32) < 0.05


def test_locality_massive_tail_exponential():
    # short-range <TT> = a FEATURE (local induced action)
    assert ip.tail_decay_rate(32, 0.40) > 0.3


def test_verdict_controls_pass():
    rep = ip.run(L=32, nwin=4)
    assert rep["controls_ok"] is True
    assert rep["mass_slope_positive"] is True
    assert rep["m2_fit_confirmed"] is True
    assert rep["verdict"].startswith("CONTROL ONLY")
    assert "m is not 1/xi" in rep["verdict"]

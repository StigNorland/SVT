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
    # the m^2 (physical) part is a small fraction of the cutoff (contact) piece,
    # so the raw c2 sign/value is NOT physical -- isolation is required
    f = ip.einstein_coefficient(32, nwin=4)
    assert f["cutoff_domination_span"] < 0.2
    assert f["A_cutoff"] < 0.0            # raw c2 dominated by the cutoff piece


def test_induced_einstein_positive_and_m2_law():
    f = ip.einstein_coefficient(32, nwin=4)
    assert f["B_phys"] > 0.0              # positive / healthy induced 1/G
    assert f["R2_m2"] > 0.99             # c2 linear in m^2 -> 1/G ~ 1/xi^2


def test_B_lattice_stable():
    b32 = ip.einstein_coefficient(32, nwin=4)["B_phys"]
    b24 = ip.einstein_coefficient(24, nwin=4)["B_phys"]
    assert abs(b32 - b24) / abs(b32) < 0.05


def test_locality_massive_tail_exponential():
    # short-range <TT> = a FEATURE (local induced action)
    assert ip.tail_decay_rate(32, 0.40) > 0.3


def test_verdict_controls_pass():
    rep = ip.run(L=32, nwin=4)
    assert rep["controls_ok"] is True
    assert rep["einstein_positive"] is True
    assert rep["m2_scaling_confirmed"] is True
    assert "1/xi^2" in rep["verdict"]

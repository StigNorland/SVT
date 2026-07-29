"""Tests for #166 sub-calculation 4 -- supplied-kernel control.

Validates the instrument, then checks the result:
  (i)   CONTROL C1: the response is transverse (Ward, reuse sub-calc 2);
  (ii)  CONTROL C2: a known 1/khat^2 kernel FFTs to G(r) ~ 1/r^2 in 4D (the
        Green's-function machinery recovers the massless power);
  (iii) CONTROL C3: a gapped ("imposed", #162-like) kernel is short-range Yukawa
        -> the test discriminates long-range (follows-from) from short (imposed);
  (iv)  T1 determinacy: the screen polarisation Pi2 is invertible (!= 0);
  (v)   T2 propagation: the physical response is long-range (~1/r^2), and the
        run-level verdict/controls hold.
"""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_screen")
sys.path.insert(0, os.path.abspath(SRC))

import reconstruction_response as r  # noqa: E402


def test_control_C1_ward_transverse():
    assert r.control_C1_ward() < 1e-4


def test_control_C2_massless_machinery_gives_inverse_square():
    L = 32
    G = r.greens_function(L, r.khat2(L))
    rs, prof = r.radial_profile(G, L)
    assert abs(r.fit_power(rs, prof) - 2.0) < 0.35        # 4D massless ~ 1/r^2


def test_control_C3_gapped_is_short_range():
    L = 32
    G = r.greens_function(L, 0.6 ** 2 + r.khat2(L))
    rs, prof = r.radial_profile(G, L)
    assert r.fit_yukawa_rate(rs, prof) > 0.3             # imposed = short-range


def test_T1_determinacy_polarisation_invertible():
    assert r.determinacy_min_abs_Pi2() > 1e-6


def test_T2_long_range_vs_imposed_short_range():
    L = 32
    p_long = r.fit_power(*r.radial_profile(r.greens_function(L, r.khat2(L)), L))
    rate_short = r.fit_yukawa_rate(
        *r.radial_profile(r.greens_function(L, 0.6 ** 2 + r.khat2(L)), L))
    assert abs(p_long - 2.0) < 0.35                       # follows-from: long-range
    assert rate_short > 0.3                               # imposed: short-range


def test_verdict_is_scoped_as_control_after_reconstruction_audit():
    rep = r.run(L=40)
    assert rep["controls_ok"] is True
    assert rep["T1_determined"] is True
    assert rep["T2_long_range"] is True
    assert rep["measured_screen_polarisation_enters_T2"] is False
    assert rep["verdict"].startswith("CONTROL ONLY")
    assert "does NOT establish" in rep["verdict"]

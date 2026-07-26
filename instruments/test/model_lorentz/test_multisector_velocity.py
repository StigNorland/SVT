"""Tests for #174 No-go map (II) -- bosonic superfluid universal-c (tree level).

Validates the instrument, then checks the result:
  (i)   CONTROL C1: decoupled + identical components are degenerate (c+ = c-);
  (ii)  CONTROL C2: numeric BdG sound speeds match the analytic c_pm formula;
  (iii) CONTROL C3: high-k branch -> z=2 free particle (omega ~ k^2/2m);
  (iv)  two coupled bosonic sectors have DIFFERENT sound speeds (large split);
  (v)   coupling increases the split, zero only at the fully tuned point;
  (vi)  the run-level verdict (no natural universal c) holds.
"""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_lorentz")
sys.path.insert(0, os.path.abspath(SRC))

import multisector_velocity as mv  # noqa: E402


def test_control_C1_degenerate_when_tuned():
    tuned = dict(mv.DEF, g12=0.0)
    cp, cm = mv.sound_speeds_analytic(tuned)
    assert abs(cp - cm) < 1e-12                       # identical + decoupled -> one c


def test_control_C2_numeric_matches_analytic():
    cp_a, cm_a = mv.sound_speeds_analytic(mv.DEF)
    cp_n, cm_n = mv.sound_speeds_numeric(mv.DEF)
    assert max(abs(cp_a - cp_n), abs(cm_a - cm_n)) / cp_a < 1e-3


def test_control_C3_highk_is_z2():
    import numpy as np
    khi = 50.0
    wp, _ = mv.omega_pm(np.array([khi]), mv.DEF)
    ratio = wp[0] / (khi * khi / (2.0 * min(mv.DEF["m1"], mv.DEF["m2"])))
    assert abs(ratio - 1.0) < 0.05                    # free-particle z=2 UV


def test_coupled_sectors_split():
    # identical components but coupled -> a large sector velocity difference
    assert mv.splitting(mv.DEF) > 0.3


def test_coupling_increases_split_zero_only_when_tuned():
    s0 = mv.splitting(dict(mv.DEF, g12=0.0))
    s1 = mv.splitting(dict(mv.DEF, g12=0.3))
    s2 = mv.splitting(dict(mv.DEF, g12=0.6))
    assert s0 < 1e-12                                 # zero only at g12=0 (tuned)
    assert s0 < s1 < s2                               # coupling worsens it


def test_verdict_no_universal_c():
    rep = mv.run()
    assert rep["controls_ok"] is True
    assert rep["no_natural_universal_c"] is True
    assert "NO natural universal c" in rep["verdict"]

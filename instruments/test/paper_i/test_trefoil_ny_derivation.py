"""Tests for #92 sub-problem B — N_Y = 3 from the (2,3)-trefoil topology.

Pre-registered claims (plan on #92):
  C1  crossing number = 3 for every generic projection and geometry (topological)
  C2  writhe → 3.000 as core a → 0 (self-linking number; finite a adds O(a²))
  C3  braid word σ₁³ ⇒ standard-diagram writhe = crossing number = 3
  C4  l_curve/(4π) is NOT an invariant (floats with geometry; paper candidate 2 rejected)
  C5  inter-strand min distance = 2a exactly (geometric cutoff R; sub-problem A)
"""

import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from trefoil_ny_derivation import (  # noqa: E402
    braid_word_writhe,
    crossing_number,
    interstrand_min_distance,
    l_curve_over_4pi,
    ny_verdict,
    parameter_values,
    planar_crossing_number,
    trefoil_curve,
    writhe,
    writhe_thin_core_limit,
)


def test_crossing_number_is_three_all_geometries():
    """C1 — crossing number = 3 for every (R, a) in the stable domain."""
    for R in (2.2, 2.5, 2.8, 3.1, 3.5):
        for a in (0.3, 0.65, 0.85):
            assert crossing_number(trefoil_curve(700, R, a)) == 3


def test_crossing_number_robust_to_projection_angle():
    """C1 — every generic projection gives 3 (not just the minimum)."""
    c = trefoil_curve(900, 2.8, 0.3)
    for angle in np.linspace(0.05, np.pi - 0.05, 9):
        assert planar_crossing_number(c, angle) == 3


def test_writhe_converges_to_three_thin_core():
    """C2 — writhe → 3.000 as a → 0."""
    thin = writhe_thin_core_limit()
    assert abs(thin["a=0.05"] - 3.0) < 0.01
    assert abs(thin["a=0.15"] - 3.0) < 0.01
    # monotone approach: thinner core ⇒ closer to 3
    assert thin["a=0.05"] < thin["a=0.85"]


def test_writhe_finite_core_correction_is_small_and_positive():
    """C2 — finite a gives Wr = 3 + O(a²): physical a=0.85 still within ~0.2 of 3."""
    w = abs(writhe(trefoil_curve(800, 3.0, 0.85)))
    assert 3.0 < w < 3.25


def test_braid_word_writhe_is_three():
    """C3 — σ₁³ ⇒ writhe = crossing number = 3."""
    assert braid_word_writhe() == 3


def test_l_curve_over_4pi_is_not_invariant():
    """C4 — l_curve/(4π) floats with geometry, so it is not the derivation."""
    vals = [l_curve_over_4pi(trefoil_curve(600, R, 0.85)) for R in (1.5, 2.5, 2.8)]
    assert max(vals) - min(vals) > 0.5      # floats by ~1.1


def test_interstrand_distance_equals_2a():
    """C5 — inter-strand min distance = 2a exactly (geometric cutoff R)."""
    for a in (0.65, 0.85, 1.05):
        c = trefoil_curve(600, 2.5, a)
        mi = interstrand_min_distance(c, parameter_values(600))
        assert abs(mi - 2.0 * a) < 0.02


def test_verdict_ny_equals_three():
    """The assembled verdict: N_Y = 3, all sub-claims hold."""
    r = ny_verdict()
    assert r["N_Y"] == 3
    assert r["crossing_number_is_3"]
    assert r["writhe_to_3"]
    assert r["l_curve_not_invariant"]
    assert r["interstrand_equals_2a"]

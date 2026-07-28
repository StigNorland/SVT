"""Tests for #187 — SSV-V's remnant arguments under the adopted branch.

These lock in both halves of the finding: Argument 1's mechanism inverts (a
negative result), and its conclusion is nonetheless recoverable by pressure (a
positive one). A failure here means either the finding was wrong or the paper
changed; both require re-opening the damage report.
"""

import sys
from pathlib import Path

import mpmath as mp

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_v")
if p not in sys.path:
    sys.path.insert(0, p)

import ssv_v_remnant_audit_2026 as rem  # noqa: E402


# --- R1: the adopted branch is stable and bounded below -------------------

def test_potential_minimum_is_at_saturation():
    assert rem.potential_minimum(b=1, rhobar=1) == mp.mpf(1)


def test_potential_is_convex():
    for rho in ("0.1", "0.5", "1", "10"):
        assert rem.is_convex(mp.mpf(rho), b=1) is True


def test_potential_is_bounded_below():
    assert rem.is_bounded_below() is True


# --- R2: Argument 1's MECHANISM inverts -----------------------------------

def test_chemical_potential_diverges_negatively_at_zero_density():
    """Argument 1 needs mu -> +infinity; the adopted branch gives -infinity."""
    assert rem.mu_limit_at_zero_density() < 0


def test_argument1_mechanism_does_not_hold():
    """The chemical-potential floor does not exist on the adopted branch."""
    assert rem.argument1_mechanism_holds() is False


def test_mu_falls_without_bound_as_density_drops():
    a = rem.mu_limit_at_zero_density(eps="1e-10")
    b = rem.mu_limit_at_zero_density(eps="1e-30")
    assert b < a < 0


# --- R3: the CONCLUSION survives, by pressure -----------------------------

def test_pressure_is_strictly_increasing_in_density():
    assert rem.pressure_is_increasing() is True


def test_sub_saturated_region_is_compressed():
    """P(rhobar) > P(void): a net inward push, which is what Argument 1 wanted."""
    assert rem.confining_pressure_difference(mp.mpf("0.5")) > 0


def test_argument1_conclusion_survives_by_a_different_mechanism():
    """The distinction that matters: mechanism wrong, conclusion recoverable."""
    assert rem.argument1_mechanism_holds() is False
    assert rem.argument1_conclusion_survives() is True


def test_confinement_scales_with_the_density_deficit():
    """P = b rho, so the inward push is linear in how far below saturation."""
    shallow = rem.confining_pressure_difference(mp.mpf("0.9"))
    deep = rem.confining_pressure_difference(mp.mpf("0.1"))
    assert deep > shallow > 0
    assert abs(deep / shallow - 9) < mp.mpf("1e-20")

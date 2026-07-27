"""Tests for #183 — the SSV-I colour-sector obstruction, machine-checked.

These lock in a *negative* result. A failure here means either the finding was
wrong or the paper changed; both require re-opening the damage report, never a
silent edit of the assertion.
"""

import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

import ssv_i_colour_sector_nogo as cs  # noqa: E402


def test_three_legs_give_two_independent_relative_phases():
    """One of the three phases is the overall gauge phase."""
    assert cs.independent_relative_phases(3) == 2


def test_the_120_degree_construction_is_abelian():
    """Z_3 is abelian, so it cannot be a non-abelian gauge group."""
    assert cs.z3_is_abelian() is True


def test_phase_construction_cannot_reach_su3():
    assert cs.phase_construction_reaches_su3() is False


def test_z3_is_the_centre_of_su3_not_su3():
    """This is exactly why the identification looked right.

    The centre carries triality -- three of them, and only Z_3-neutral
    combinations physical -- which reproduces the countable features while
    supplying none of the dynamics.
    """
    assert cs.z3_is_the_centre_of_su3() is True
    assert cs.su3_dimension() == 8


def test_six_generators_are_missing_and_they_are_the_colour_changing_ones():
    """dim SU(3) = 8; the construction reaches at most the rank-2 Cartan."""
    assert cs.cartan_dimension() == 2
    assert cs.missing_generators() == 6


def test_the_missing_generators_are_off_diagonal():
    """Off-diagonal generators are the ones that map one colour to another."""
    off = [g for g in cs.gell_mann() if not np.allclose(g, np.diag(np.diag(g)))]
    assert len(off) == 6
    for g in off:
        assert not np.allclose(np.diag(np.diag(g)), g)


def test_cartan_generators_commute_with_each_other():
    """So even the reachable part supplies no colour-changing dynamics."""
    diag = [g for g in cs.gell_mann() if np.allclose(g, np.diag(np.diag(g)))]
    assert len(diag) == 2
    a, b = diag
    assert np.allclose(a @ b, b @ a)

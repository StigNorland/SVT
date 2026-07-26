"""Tests for #178 No-go map (IV) -- pi_3 admissibility of fermionic solitons.

Validates the instrument, then checks the result:
  (i)   CONTROL C1/C2: SU(2) hedgehog winding is integer (|B| = 1, 2 for 1, 2
        turns) to grid accuracy, and grid-convergent (C5);
  (ii)  CONTROL C3: B is invariant under smooth profile deformation
        (topological, not dynamical);
  (iii) T1: the U(1) (bare-SSV) winding density is POINTWISE zero -- not a
        cancellation -- so B = 0 for any configuration;
  (iv)  the run-level verdict (bare SSV fails; multi-component condensate is the
        derived minimal repair) holds.
"""

import os
import sys

import numpy as np
import pytest

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_fermion")
sys.path.insert(0, os.path.abspath(SRC))

import soliton_statistics as s  # noqa: E402


@pytest.fixture(scope="module")
def rep():
    return s.run(N=128, L=6.0, w=1.5)


def test_control_C1_C2_hedgehog_winding_integer(rep):
    assert abs(abs(rep["B_hedgehog_1turn"]) - 1.0) < 0.02
    assert abs(abs(rep["B_hedgehog_2turn"]) - 2.0) < 0.05


def test_control_C5_grid_convergent(rep):
    # finer grid is closer to the integer than the coarse one
    assert (abs(abs(rep["B_hedgehog_1turn"]) - 1.0)
            < abs(abs(rep["B_hedgehog_1turn_coarse"]) - 1.0))


def test_control_C3_deformation_stable(rep):
    assert abs(rep["B_hedgehog_1turn"] - rep["B_hedgehog_1turn_deformed"]) < 0.02


def test_T1_u1_density_pointwise_zero(rep):
    # the pi_3 density of a U(1)-valued field vanishes POINTWISE (parallel
    # tangent vectors on a great circle), not by cancellation
    assert rep["u1_max_density"] < 1e-10
    assert abs(rep["u1_winding"]) < 1e-10


def test_u1_pointwise_zero_any_configuration():
    # a second, independent U(1) configuration (different width/amplitude)
    n, h = s.u1_embedding(N=48, L=6.0, w=1.0, amp=5.0)
    assert np.abs(s.winding_density(n, h)).max() < 1e-10


def test_verdict_bare_ssv_fails(rep):
    assert rep["controls_ok"] is True
    assert rep["T1_u1_pointwise_zero"] is True
    assert "bare SSV FAILS" in rep["verdict"]
    assert "multi-component condensate" in rep["verdict"]

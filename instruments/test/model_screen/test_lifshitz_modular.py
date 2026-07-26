"""Tests for #170 -- Lifshitz (z!=1) modular-locality (can reconstruction be presentist?).

Validates the instrument, then checks the result:
  (i)   CONTROL C1: z=1 reproduces sub-calc 1's geometric far tail (~2%);
  (ii)  the z=2 (SSV UV) far tail is robustly larger than z=1 (ratio > 3);
  (iii) the z=2 far tail is N-CONVERGED (physical, not a finite-size/IR artifact);
  (iv)  the run-level cautionary-negative verdict and its honesty flags hold.
"""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_screen")
sys.path.insert(0, os.path.abspath(SRC))

import lifshitz_modular as lf  # noqa: E402


def test_control_C1_z1_geometric():
    # z=1 (relativistic massless) = the CHM/sub-calc-1 geometric boost
    assert lf.far_tail_for_z(40, 1.0, N=800) < 0.05


def test_z2_far_tail_larger_than_z1():
    f1 = lf.far_tail_for_z(40, 1.0, N=800)
    f2 = lf.far_tail_for_z(40, 2.0, N=800)
    assert f2 / f1 > 3.0                       # preferred foliation degrades geometricity


def test_z2_far_tail_N_converged():
    # physical, not a finite-size/IR artifact: stable across chain size
    a = lf.far_tail_for_z(40, 2.0, N=800)
    b = lf.far_tail_for_z(40, 2.0, N=1600)
    assert abs(a - b) / a < 0.02


def test_verdict_cautionary_negative():
    rep = lf.run(ell=40, N=800)
    assert rep["control_C1_z1_geometric"] is True
    assert rep["z2_geometricity_degraded"] is True
    assert rep["far_tail_monotonic_in_z"] is False   # honest: crude probe
    assert "tension" in rep["verdict"]


# --- follow-on: is the geometricity IR-emergent? (Bogoliubov crossover) ---

def test_flow_bogoliobov_N_converged():
    # the flow is physical, not a finite-size artifact (large IR region)
    a = lf.far_tail_bogoliubov(48, 4.0, N=2000)
    b = lf.far_tail_bogoliubov(48, 4.0, N=3000)
    assert abs(a - b) / a < 0.02


def test_flow_UV_nongeometric_IR_recovers():
    flow = lf.run_flow(xi=4.0, ells=(2, 16, 64), N=2000)
    assert flow["R_uv_mean"] > 3.0                    # ell<=xi: sees z=2 (non-geometric)
    assert flow["R_ir_mean"] < 2.0                    # ell>>xi: recovers to ~z=1
    assert flow["R_ir_mean"] < flow["z2_ratio_benchmark"]


def test_flow_emergent_lorentz_verdict():
    flow = lf.run_flow(xi=4.0, ells=(2, 16, 64), N=2000)
    assert flow["emergent_lorentz"] is True
    assert "EMERGENT LORENTZ" in flow["verdict"]

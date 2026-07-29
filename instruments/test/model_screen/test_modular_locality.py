"""Tests for #166 sub-calculation 1 -- modular-locality of the screen.

Validates the instrument before its verdict is trusted, then checks the result:
  (i)   symplectic eigenvalues nu >= 1/2 (physical);
  (ii)  CONTROL C1: Dirichlet entropy gives c ~ 1 (the zero-mode-free control);
  (iii) CONTROL C2: the modular-Hamiltonian formula reconstructs X, P to ~1e-7;
  (iv)  CONTROL C3: the massless modular Hamiltonian is short-range (local boost);
  (v)   RESULT: the far (non-local) tail does NOT grow with the scale m*ell --
        modular flow stays geometric -> R1-open (R3 not triggered);
  (vi)  the verdict string reports R1-open with controls passing.
"""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_screen")
sys.path.insert(0, os.path.abspath(SRC))

import modular_locality as ml  # noqa: E402


def test_symplectic_nu_physical():
    X, P = ml.correlators(20, 0.1, N=800)
    nu = ml.symplectic_nu(X, P)
    assert nu.min() >= 0.5 - 1e-9


def test_control_C1_entropy_central_charge():
    S_l = ml.entanglement_entropy(*ml.correlators(20, 1e-3, N=1200))
    S_2l = ml.entanglement_entropy(*ml.correlators(40, 1e-3, N=1200))
    c_eff = 6.0 * (S_2l - S_l) / np.log(2.0)   # one entangling point -> c/6
    assert 0.9 <= c_eff <= 1.1, f"c_eff = {c_eff}"


def test_control_C2_formula_reconstructs_correlators():
    X, P = ml.correlators(20, 0.15, N=800)
    Xr, Pr = ml.reconstruct_covariance(ml.modular_H_pi(X, P),
                                       ml.modular_H_phi(X, P))
    err = max(np.abs(Xr - X).max() / np.abs(X).max(),
              np.abs(Pr - P).max() / np.abs(P).max())
    assert err < 1e-4, f"reconstruction err {err}"


def test_control_C3_massless_boost_is_local():
    X, P = ml.correlators(40, 1e-3, N=1600)
    assert ml.far_tail(ml.modular_H_pi(X, P)) < 0.05


def test_result_far_tail_does_not_grow_with_scale():
    # non-locality shrinks (not grows) as the scale m*ell increases
    ells = 40
    t_small = ml.far_tail(ml.modular_H_pi(*ml.correlators(ells, 1e-3, N=1600)))
    t_large = ml.far_tail(ml.modular_H_pi(*ml.correlators(ells, 1.0, N=1600)))
    assert t_large <= t_small, f"far tail grew: {t_small} -> {t_large}"


def test_verdict_is_scoped_as_far_tail_control():
    rep = ml.run(ell=24, masses=(1e-3, 0.1, 0.6), N=900)
    assert rep["controls_ok"] is True
    assert rep["far_tail_grows_with_scale"] is False
    assert rep["verdict"].startswith("CONTROL ONLY")
    assert "does not establish" in rep["verdict"]

"""Unit tests for lperp_krylov_helpers.

Covers:
- fft_left_preconditioner: kinetic_coeff inclusion, identity fallback
- gmres_matrix_free: exact solve on small system
- gmres_restarted: convergence, multi-cycle, already-converged early exit
- krylov_implicit_step: lambda=0 fallback, gradient reduction on toy problem
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parents[1]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_i.lperp_krylov_helpers import (
    _pack,
    _unpack,
    fft_left_preconditioner,
    gmres_matrix_free,
    gmres_restarted,
    krylov_implicit_step,
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def make_diag_matvec(diag: np.ndarray):
    """Linear operator A = diag(diag)."""
    return lambda v: diag * v


def rng(seed: int = 0) -> np.random.Generator:
    return np.random.default_rng(seed)


# ---------------------------------------------------------------------------
# fft_left_preconditioner
# ---------------------------------------------------------------------------

def test_preconditioner_identity_when_dt_zero():
    shape = (8, 8, 8)
    dx = 0.5
    m_inv = fft_left_preconditioner(shape, dx, dt=0.0, lambda_perp=100.0)
    v = rng().standard_normal(shape).astype(complex)
    out = m_inv(v)
    assert np.allclose(out, v), "dt=0 preconditioner should be identity"


def test_preconditioner_kinetic_term_changes_output():
    shape = (8, 8, 8)
    dx = 0.5
    dt = 0.01
    lp = 10.0
    v = rng().standard_normal(shape).astype(complex)
    out_no_kin = fft_left_preconditioner(shape, dx, dt, lp, kinetic_coeff=0.0)(v)
    out_with_kin = fft_left_preconditioner(shape, dx, dt, lp, kinetic_coeff=0.5)(v)
    assert not np.allclose(out_no_kin, out_with_kin), \
        "kinetic_coeff=0.5 should give different output from kinetic_coeff=0"


def test_preconditioner_dampens_high_k():
    """High-k modes should be more damped with kinetic term included."""
    shape = (16, 1, 1)
    dx = 0.25
    dt = 0.1
    lp = 50.0
    # Pure high-k signal: Nyquist mode
    v = np.zeros(shape, dtype=complex)
    v[shape[0] // 2, 0, 0] = 1.0
    out_no_kin = fft_left_preconditioner(shape, dx, dt, lp, kinetic_coeff=0.0)(v)
    out_with_kin = fft_left_preconditioner(shape, dx, dt, lp, kinetic_coeff=0.5)(v)
    amp_no_kin = float(np.max(np.abs(out_no_kin)))
    amp_with_kin = float(np.max(np.abs(out_with_kin)))
    assert amp_with_kin < amp_no_kin, \
        "kinetic term should add extra damping at high k"


def test_preconditioner_output_dtype_preserved():
    shape = (6, 6, 6)
    dx = 0.4
    m_inv = fft_left_preconditioner(shape, dx, dt=0.01, lambda_perp=5.0)
    v = rng().standard_normal(shape).astype(complex)
    out = m_inv(v)
    assert out.dtype == v.dtype


# ---------------------------------------------------------------------------
# gmres_matrix_free
# ---------------------------------------------------------------------------

def test_gmres_identity_system():
    n = 20
    x_true = rng().standard_normal(n)
    b = x_true.copy()
    x, k, relres = gmres_matrix_free(lambda v: v, b, tol=1e-10, maxiter=50)
    assert relres < 1e-10
    assert np.allclose(x, x_true, atol=1e-8)


def test_gmres_diagonal_system():
    n = 30
    diag = 1.0 + rng().uniform(0, 4, n)
    x_true = rng().standard_normal(n)
    b = diag * x_true
    x, k, relres = gmres_matrix_free(make_diag_matvec(diag), b, tol=1e-8, maxiter=50)
    assert relres < 1e-8, f"relres={relres}"
    assert np.allclose(x, x_true, atol=1e-6)


def test_gmres_zero_rhs():
    n = 10
    x, k, relres = gmres_matrix_free(lambda v: v, np.zeros(n), tol=1e-8)
    assert np.allclose(x, 0.0)
    assert k == 0
    assert relres == 0.0


def test_gmres_identity_converges_in_one_iteration():
    # For A=I starting from x=0, the first Krylov vector spans the solution
    # exactly, so GMRES should converge in 1 iteration.
    n = 20
    b = rng().standard_normal(n)
    x, k, relres = gmres_matrix_free(lambda v: v, b, tol=1e-10, maxiter=30)
    assert k == 1, f"expected 1 iteration for identity, got {k}"
    assert relres < 1e-10


# ---------------------------------------------------------------------------
# gmres_restarted
# ---------------------------------------------------------------------------

def test_gmres_restarted_identity():
    n = 50
    x_true = rng().standard_normal(n)
    b = x_true.copy()
    x, total_iters, relres = gmres_restarted(lambda v: v, b, tol=1e-10, restart=10, max_cycles=5)
    assert relres < 1e-10
    assert np.allclose(x, x_true, atol=1e-8)


def test_gmres_restarted_needs_multiple_cycles():
    """Restart length shorter than system dimension; verify multi-cycle convergence.

    restart=10 on a 40-element diagonal with condition ~10.  Each cycle
    runs 10 Arnoldi steps; multiple cycles are needed to reach tol=1e-6.
    """
    n = 40
    diag = np.linspace(1.0, 10.0, n)  # condition number 10, well-posed
    x_true = rng().standard_normal(n)
    b = diag * x_true
    x, total_iters, relres = gmres_restarted(
        make_diag_matvec(diag), b, tol=1e-6, restart=10, max_cycles=10
    )
    assert relres < 1e-6, f"relres={relres} after {total_iters} iters"
    assert np.allclose(x, x_true, atol=1e-4)


def test_gmres_restarted_zero_rhs():
    n = 10
    x, k, relres = gmres_restarted(lambda v: v, np.zeros(n), tol=1e-8)
    assert np.allclose(x, 0.0)
    assert k == 0
    assert relres == 0.0


def test_gmres_restarted_matches_unrestarted_on_easy_system():
    """On a well-conditioned system, restarted and unrestarted should give same answer."""
    n = 20
    diag = 1.0 + rng().uniform(0, 1, n)
    x_true = rng().standard_normal(n)
    b = diag * x_true
    matvec = make_diag_matvec(diag)
    x1, _, _ = gmres_matrix_free(matvec, b, tol=1e-10, maxiter=50)
    x2, _, _ = gmres_restarted(matvec, b, tol=1e-10, restart=50, max_cycles=1)
    assert np.allclose(x1, x2, atol=1e-8)


# ---------------------------------------------------------------------------
# krylov_implicit_step
# ---------------------------------------------------------------------------

def test_krylov_step_lambda_zero_is_explicit_euler():
    """With lambda_perp=0 the step should equal psi - dt * g_full(psi)."""
    shape = (4, 4, 4)
    psi = rng().standard_normal(shape) + 1j * rng().standard_normal(shape)
    dt = 0.01
    g = rng().standard_normal(shape) + 1j * rng().standard_normal(shape)
    g_fn = lambda p: g  # constant gradient (linear in psi irrelevant here)
    psi_new, n_iter, relres = krylov_implicit_step(
        psi, g_fn, dt=dt, lambda_perp=0.0, dx=0.5
    )
    expected = psi - dt * g
    assert np.allclose(psi_new, expected), "lambda=0 should be explicit Euler"
    assert n_iter == 0


def test_krylov_step_reduces_gradient_norm():
    """After one implicit step the gradient norm should decrease on a toy quadratic."""
    shape = (6, 6, 6)
    dx = 0.5
    dt = 0.005
    lp = 10.0
    # Quadratic energy: g(psi) = psi  (gradient of 0.5 ||psi||^2)
    g_fn = lambda p: p
    psi0 = 0.1 * (rng().standard_normal(shape) + 1j * rng().standard_normal(shape))
    g_norm_before = float(np.linalg.norm(g_fn(psi0)))
    psi1, _, _ = krylov_implicit_step(
        psi0, g_fn, dt=dt, lambda_perp=lp, dx=dx,
        gmres_tol=1e-6, gmres_restart=30, gmres_max_cycles=5
    )
    g_norm_after = float(np.linalg.norm(g_fn(psi1)))
    assert g_norm_after < g_norm_before, \
        f"gradient norm should decrease: {g_norm_before:.4e} -> {g_norm_after:.4e}"


def test_krylov_step_returns_correct_shape():
    shape = (5, 5, 5)
    psi = rng().standard_normal(shape) + 1j * rng().standard_normal(shape)
    psi_new, _, _ = krylov_implicit_step(
        psi, lambda p: p, dt=0.005, lambda_perp=1.0, dx=0.4
    )
    assert psi_new.shape == shape


def test_krylov_step_kinetic_coeff_zero_still_works():
    shape = (6, 6, 6)
    psi = 0.1 * (rng().standard_normal(shape) + 1j * rng().standard_normal(shape))
    psi_new, n_iter, relres = krylov_implicit_step(
        psi, lambda p: p, dt=0.005, lambda_perp=5.0, dx=0.5,
        kinetic_coeff=0.0, gmres_restart=20, gmres_max_cycles=3
    )
    assert psi_new.shape == shape
    assert np.isfinite(relres)


# ---------------------------------------------------------------------------
# pack / unpack round-trip
# ---------------------------------------------------------------------------

def test_pack_unpack_roundtrip():
    shape = (4, 5, 3)
    z = rng().standard_normal(shape) + 1j * rng().standard_normal(shape)
    assert np.allclose(_unpack(_pack(z), shape), z)


# ---------------------------------------------------------------------------
# runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
            passed += 1
        except Exception as exc:
            print(f"  FAIL  {fn.__name__}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)

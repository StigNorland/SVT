"""Krylov-based fully-implicit step for the L_perp chiral non-local shear term.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1

The FFT-based semi-implicit step (lperp_implicit_helpers) approximates the
L_perp Jacobian by `lambda * (-Laplacian)^2`, which is diagonal in Fourier
and damps all high-k modes uniformly.  That over-smooths the vortex cores
because the actual Jacobian is non-diagonal and `psi`-dependent (cores
should stay sharp where the field has phase singularities, not just
high-k content).

This module replaces the diagonal-in-Fourier approximation with a
matrix-free GMRES solve against the true Jacobian.  The Jacobian action
`J . v` is computed by one-sided finite differencing of `g_full`:

    J . v ~ (g_full(psi + eps v) - g_full(psi)) / eps,

with `eps` chosen for numerical stability.  The FFT diagonal serves as a
LEFT PRECONDITIONER `M ~ I + dt lambda (-Laplacian)^2`, so GMRES converges
in a small number of iterations.

The solve is done in a real (2N-component) packed representation because
the true L_perp Jacobian is R-linear (Wirtinger), not C-linear.

Cost per implicit step: about `K + 1` evaluations of `g_full` where `K` is
the number of GMRES iterations (typically 5-15 with the FFT preconditioner).
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def fft_left_preconditioner(
    shape: tuple[int, ...], dx: float, dt: float, lambda_perp: float
) -> Callable[[np.ndarray], np.ndarray]:
    """Return a function `M_inv(v)` for v complex, applying `(1 + dt lambda k^4)^-1` in Fourier."""
    if lambda_perp == 0.0 or dt == 0.0:
        return lambda v: v
    kx = 2.0 * np.pi * np.fft.fftfreq(shape[0], d=dx)
    ky = 2.0 * np.pi * np.fft.fftfreq(shape[1], d=dx)
    kz = 2.0 * np.pi * np.fft.fftfreq(shape[2], d=dx)
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    k_sq = KX * KX + KY * KY + KZ * KZ
    denom = 1.0 + dt * lambda_perp * k_sq * k_sq

    def m_inv(v: np.ndarray) -> np.ndarray:
        v_hat = np.fft.fftn(v)
        return np.fft.ifftn(v_hat / denom).astype(v.dtype)

    return m_inv


def _pack(z: np.ndarray) -> np.ndarray:
    return np.concatenate([z.real.ravel(), z.imag.ravel()])


def _unpack(r: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    n = int(np.prod(shape))
    return r[:n].reshape(shape) + 1j * r[n:].reshape(shape)


def gmres_matrix_free(
    matvec: Callable[[np.ndarray], np.ndarray],
    b: np.ndarray,
    tol: float = 1.0e-5,
    maxiter: int = 30,
) -> tuple[np.ndarray, int, float]:
    """Simple unrestarted GMRES on a real vector system.

    Returns `(x, k, relres)` where `k` is iteration count used and `relres`
    is the achieved relative residual.
    """
    n = len(b)
    x = np.zeros(n)
    r = b - matvec(x)
    beta = float(np.linalg.norm(r))
    b_norm = float(np.linalg.norm(b))
    if b_norm == 0.0:
        return x, 0, 0.0
    if beta < tol * b_norm:
        return x, 0, beta / b_norm

    V = np.zeros((maxiter + 1, n))
    H = np.zeros((maxiter + 1, maxiter))
    V[0] = r / beta

    y_best = None
    relres = beta / b_norm

    for k in range(maxiter):
        w = matvec(V[k])
        for i in range(k + 1):
            H[i, k] = float(np.dot(V[i], w))
            w = w - H[i, k] * V[i]
        H[k + 1, k] = float(np.linalg.norm(w))
        if H[k + 1, k] > 1.0e-14:
            V[k + 1] = w / H[k + 1, k]
        # Least-squares for y in [0, k]
        e1 = np.zeros(k + 2)
        e1[0] = beta
        y, *_ = np.linalg.lstsq(H[: k + 2, : k + 1], e1, rcond=None)
        residual = float(np.linalg.norm(H[: k + 2, : k + 1] @ y - e1))
        relres = residual / b_norm
        y_best = y
        if residual < tol * b_norm:
            x = x + V[: k + 1].T @ y
            return x, k + 1, relres

    if y_best is not None:
        x = x + V[: len(y_best)].T @ y_best
    return x, maxiter, relres


def krylov_implicit_step(
    psi: np.ndarray,
    g_full_fn: Callable[[np.ndarray], np.ndarray],
    dt: float,
    lambda_perp: float,
    dx: float,
    gmres_tol: float = 1.0e-4,
    gmres_maxiter: int = 30,
) -> tuple[np.ndarray, int, float]:
    """Single fully-implicit step with Krylov solve.

    Solves `(I + dt J) dpsi = -dt g_full(psi)` for `dpsi`, returns
    `(psi + dpsi, n_iter, relres)`.

    `g_full_fn(psi) -> complex array of same shape as psi` is the full
    gradient (LogSE + L_perp) the caller provides.
    """
    g_old = g_full_fn(psi)
    if lambda_perp == 0.0:
        # No L_perp -> trivial explicit step.
        return psi - dt * g_old, 0, 0.0

    shape = psi.shape
    psi_norm = float(np.linalg.norm(psi))
    m_inv = fft_left_preconditioner(shape, dx, dt, lambda_perp)

    def matvec_real(v_real: np.ndarray) -> np.ndarray:
        v = _unpack(v_real, shape)
        v_norm = float(np.linalg.norm(v))
        if v_norm < 1.0e-30:
            return v_real
        eps = 1.0e-7 * max(psi_norm, 1.0) / v_norm
        g_pert = g_full_fn(psi + eps * v)
        jv = (g_pert - g_old) / eps
        a_v = v + dt * jv  # (I + dt J) v
        a_v_pc = m_inv(a_v)  # left-preconditioned
        return _pack(a_v_pc)

    b_complex = -dt * g_old
    b_pc = m_inv(b_complex)
    b_real = _pack(b_pc)

    dpsi_real, n_iter, relres = gmres_matrix_free(
        matvec_real, b_real, tol=gmres_tol, maxiter=gmres_maxiter
    )
    dpsi = _unpack(dpsi_real, shape)
    return psi + dpsi, n_iter, relres

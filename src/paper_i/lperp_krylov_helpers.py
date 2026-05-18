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
LEFT PRECONDITIONER capturing both the LogSE kinetic stiffness and the
L_perp stiffness:

    M = I + dt * (kinetic_coeff * k^2 + lambda_perp * k^4)

in Fourier space.  Including the k^2 kinetic term (previously absent)
substantially improves conditioning at intermediate wavenumbers.

GMRES is run in restarted mode: up to `gmres_max_cycles` cycles of
`gmres_restart` iterations each.  Restarting avoids memory growth and
can escape stagnation that unrestarted GMRES hits at the iteration cap.

The solve is done in a real (2N-component) packed representation because
the true L_perp Jacobian is R-linear (Wirtinger), not C-linear.

Cost per implicit step: about `(K + 1) * cycles` evaluations of `g_full`
where K is iterations per cycle (typically fewer with the improved preconditioner).
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def fft_left_preconditioner(
    shape: tuple[int, ...],
    dx: float,
    dt: float,
    lambda_perp: float,
    kinetic_coeff: float = 0.5,
) -> Callable[[np.ndarray], np.ndarray]:
    """Return M_inv applying (1 + dt*(kinetic_coeff*k^2 + lambda*k^4))^-1 in Fourier.

    kinetic_coeff=0.5 matches the LogSE kinetic term (-1/2 nabla^2) in
    nondimensional units xi=1, rho0=1, c=1.  Setting it to 0 recovers the
    old k^4-only preconditioner.
    """
    if dt == 0.0:
        return lambda v: v
    kx = 2.0 * np.pi * np.fft.fftfreq(shape[0], d=dx)
    ky = 2.0 * np.pi * np.fft.fftfreq(shape[1], d=dx)
    kz = 2.0 * np.pi * np.fft.fftfreq(shape[2], d=dx)
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    k_sq = KX * KX + KY * KY + KZ * KZ
    denom = 1.0 + dt * (kinetic_coeff * k_sq + lambda_perp * k_sq * k_sq)

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
    """Unrestarted GMRES on a real vector system.

    Returns (x, k, relres) where k is iteration count and relres = ||b - Ax|| / ||b||.
    Called directly for one cycle; use gmres_restarted for multi-cycle runs.
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


def gmres_restarted(
    matvec: Callable[[np.ndarray], np.ndarray],
    b: np.ndarray,
    tol: float = 1.0e-5,
    restart: int = 30,
    max_cycles: int = 5,
) -> tuple[np.ndarray, int, float]:
    """Restarted GMRES(restart) with up to max_cycles restart cycles.

    Each cycle runs at most `restart` iterations of unrestarted GMRES on
    the current residual equation, then updates x and checks convergence.
    Memory cost is O(restart * n) per cycle rather than O(total_iters * n).

    Returns (x, total_iters, relres) where relres = ||b - Ax|| / ||b||.
    """
    x = np.zeros(len(b))
    b_norm = float(np.linalg.norm(b))
    if b_norm == 0.0:
        return x, 0, 0.0

    total_iters = 0
    relres = 1.0

    for _ in range(max_cycles):
        r = b - matvec(x)
        relres = float(np.linalg.norm(r)) / b_norm
        if relres <= tol:
            break
        r_norm = float(np.linalg.norm(r))
        # Solve correction equation A*dx = r; pass tol scaled to ||r|| so the
        # outer residual ||b - A*x|| drops by at least tol * b_norm / r_norm.
        inner_tol = tol * b_norm / r_norm if r_norm > 0.0 else tol
        dx, k, _ = gmres_matrix_free(matvec, r, tol=inner_tol, maxiter=restart)
        x = x + dx
        total_iters += k

    # Recompute final relres after last cycle update.
    r = b - matvec(x)
    relres = float(np.linalg.norm(r)) / b_norm
    return x, total_iters, relres


def krylov_implicit_step(
    psi: np.ndarray,
    g_full_fn: Callable[[np.ndarray], np.ndarray],
    dt: float,
    lambda_perp: float,
    dx: float,
    gmres_tol: float = 1.0e-4,
    gmres_restart: int = 30,
    gmres_max_cycles: int = 5,
    kinetic_coeff: float = 0.5,
) -> tuple[np.ndarray, int, float]:
    """Single fully-implicit step with restarted Krylov solve.

    Solves (I + dt J) dpsi = -dt g_full(psi) for dpsi via GMRES(restart)
    with up to gmres_max_cycles restart cycles.  Returns (psi + dpsi, total_iters, relres).

    Preconditioner captures both LogSE kinetic stiffness (kinetic_coeff * k^2)
    and L_perp stiffness (lambda_perp * k^4), improving conditioning at
    intermediate wavenumbers relative to the old k^4-only preconditioner.
    """
    g_old = g_full_fn(psi)
    if lambda_perp == 0.0:
        return psi - dt * g_old, 0, 0.0

    shape = psi.shape
    psi_norm = float(np.linalg.norm(psi))
    m_inv = fft_left_preconditioner(shape, dx, dt, lambda_perp, kinetic_coeff=kinetic_coeff)

    def matvec_real(v_real: np.ndarray) -> np.ndarray:
        v = _unpack(v_real, shape)
        v_norm = float(np.linalg.norm(v))
        if v_norm < 1.0e-30:
            return v_real
        eps = 1.0e-7 * max(psi_norm, 1.0) / v_norm
        g_pert = g_full_fn(psi + eps * v)
        jv = (g_pert - g_old) / eps
        a_v = v + dt * jv
        return _pack(m_inv(a_v))

    b_pc = m_inv(-dt * g_old)
    b_real = _pack(b_pc)

    dpsi_real, total_iters, relres = gmres_restarted(
        matvec_real, b_real, tol=gmres_tol, restart=gmres_restart, max_cycles=gmres_max_cycles
    )
    dpsi = _unpack(dpsi_real, shape)
    return psi + dpsi, total_iters, relres

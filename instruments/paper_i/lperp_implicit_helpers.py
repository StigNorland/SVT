"""Semi-implicit time stepping for the L_perp chiral non-local shear term.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1

The full L_perp Jacobian about a given psi is nonlinear and not diagonal in
Fourier space. But its leading-order stiffness is a 4th-order operator that
scales as `lambda * k^4` in Fourier (one factor of k^2 from each of the two
curls in `curl curl j`, with j bilinear in psi).  We use that scaling as a
preconditioner / approximate Jacobian:

    J_perp_approx = lambda * (-Laplacian)^2

In Fourier space this is just multiplication by `lambda * |k|^4`, so the
implicit Euler step

    (I + dt * J_perp_approx) delta = -dt * g_full(psi_old)

solves to

    delta_hat[k] = -dt * g_full_hat[k] / (1 + dt * lambda * |k|^4),

with one forward and one inverse FFT per step.  The approximation is coarse
(ignores the psi-dependence of the real Jacobian) but it captures the right
scaling of the stiffness with both `lambda` and `dx`.  For static relaxation,
where we only care about the endpoint and not the trajectory, this is enough
to remove the explicit-Euler stability barrier.

Caveat: FFT assumes periodic boundary conditions.  Callers apply their own
boundary anchor after the implicit step; the resulting boundary artifact is
then re-pinned by the anchor.  Interior physics is correct as long as the
periodic-image error decays before reaching the box centre.
"""

from __future__ import annotations

import numpy as np


def fourier_k_squared(shape: tuple[int, ...], dx: float) -> np.ndarray:
    """Return |k|^2 grid for an FFT on a cube of shape `shape` and spacing `dx`."""
    kx = 2.0 * np.pi * np.fft.fftfreq(shape[0], d=dx)
    ky = 2.0 * np.pi * np.fft.fftfreq(shape[1], d=dx)
    kz = 2.0 * np.pi * np.fft.fftfreq(shape[2], d=dx)
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    return KX * KX + KY * KY + KZ * KZ


def semi_implicit_step(
    psi: np.ndarray,
    g_full: np.ndarray,
    dt: float,
    lambda_perp: float,
    k_sq: np.ndarray,
) -> np.ndarray:
    """Single semi-implicit Euler step.

    Returns `psi_new = psi + delta`, where `delta` solves

        (I + dt * lambda_perp * (-Laplacian)^2) delta = -dt * g_full.

    When `lambda_perp == 0` this reduces to plain explicit Euler.
    """
    if lambda_perp == 0.0:
        return psi - dt * g_full
    g_hat = np.fft.fftn(g_full)
    denom = 1.0 + dt * lambda_perp * k_sq * k_sq
    delta_hat = -dt * g_hat / denom
    delta = np.fft.ifftn(delta_hat).astype(np.complex128)
    return psi + delta

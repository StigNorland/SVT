"""Helpers for the chiral non-local shear term L_perp from Paper I.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1

Implements

    E_perp = (lambda / 2) integral |curl j|^2 d^3 x,
    j = Im(psi^* grad psi),

and its Wirtinger derivative

    delta E_perp / delta psi^* = -i lambda (curl omega) . grad psi,
    omega = curl j.

These functions are shared by the per-geometry L_perp static scripts so the
analytical derivation appears in one place.

The finite-difference layout matches the existing LogSE machinery:
periodic-style central differences on a uniform Cartesian grid.  Boundary
treatment is the caller's responsibility (the static scripts apply a
boundary anchor after each relaxation step).
"""

from __future__ import annotations

import numpy as np


def grad_psi(psi: np.ndarray, dx: float) -> np.ndarray:
    """Central-difference gradient of a complex scalar field.

    Returns shape (3, n, n, n) with axis 0 indexing (x, y, z) component.
    """
    out = np.empty((3,) + psi.shape, dtype=psi.dtype)
    for ax in range(3):
        out[ax] = (np.roll(psi, -1, axis=ax) - np.roll(psi, 1, axis=ax)) / (2.0 * dx)
    return out


def current(psi: np.ndarray, dx: float) -> np.ndarray:
    """Probability current j = Im(psi^* grad psi).

    Returns real array of shape (3, n, n, n).
    """
    gp = grad_psi(psi, dx)
    return np.imag(np.conj(psi)[None, ...] * gp)


def curl3(v: np.ndarray, dx: float) -> np.ndarray:
    """Central-difference curl of a 3-vector field on a 3D grid.

    Accepts real or complex v of shape (3, n, n, n) and returns same shape.
    """
    dy_vz = (np.roll(v[2], -1, axis=1) - np.roll(v[2], 1, axis=1)) / (2.0 * dx)
    dz_vy = (np.roll(v[1], -1, axis=2) - np.roll(v[1], 1, axis=2)) / (2.0 * dx)
    dz_vx = (np.roll(v[0], -1, axis=2) - np.roll(v[0], 1, axis=2)) / (2.0 * dx)
    dx_vz = (np.roll(v[2], -1, axis=0) - np.roll(v[2], 1, axis=0)) / (2.0 * dx)
    dx_vy = (np.roll(v[1], -1, axis=0) - np.roll(v[1], 1, axis=0)) / (2.0 * dx)
    dy_vx = (np.roll(v[0], -1, axis=1) - np.roll(v[0], 1, axis=1)) / (2.0 * dx)
    return np.stack((dy_vz - dz_vy, dz_vx - dx_vz, dx_vy - dy_vx), axis=0)


def lperp_energy(psi: np.ndarray, dx: float, lambda_perp: float) -> float:
    """E_perp = (lambda / 2) integral |curl j|^2 d^3 x."""
    if lambda_perp == 0.0:
        return 0.0
    j = current(psi, dx)
    omega = curl3(j, dx)
    return 0.5 * lambda_perp * float(np.sum(omega * omega)) * (dx**3)


def lperp_gradient(psi: np.ndarray, dx: float, lambda_perp: float) -> np.ndarray:
    """delta E_perp / delta psi^* at every cell, returned as complex (n, n, n)."""
    if lambda_perp == 0.0:
        return np.zeros_like(psi)
    j = current(psi, dx)
    omega = curl3(j, dx)
    curl_omega = curl3(omega, dx)
    gp = grad_psi(psi, dx)
    contraction = np.sum(curl_omega * gp, axis=0)
    return -1j * lambda_perp * contraction

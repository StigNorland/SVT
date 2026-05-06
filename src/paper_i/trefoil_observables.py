"""Shared observables for the Paper I static trefoil-breather track.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1
Primary role: centralise early observables for issue #13 so refinement sweeps and
single-run relaxations report the same quantities.
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def energy_density(
    psi: np.ndarray,
    spacing: float,
    log_pressure: float,
    density_floor: float,
) -> np.ndarray:
    grad_sq = sum(np.abs(np.roll(psi, -1, axis=axis) - psi) ** 2 for axis in range(3)) / (spacing**2)
    rho = np.maximum(np.abs(psi) ** 2, density_floor)
    potential = log_pressure * (rho * np.log(rho) - rho + 1.0)
    return 0.5 * grad_sq + potential


def total_energy(
    psi: np.ndarray,
    spacing: float,
    log_pressure: float,
    density_floor: float,
) -> float:
    return float(np.sum(energy_density(psi, spacing, log_pressure, density_floor)) * spacing**3)


def residual_norm(
    psi: np.ndarray,
    gradient_fn: Callable[[np.ndarray], np.ndarray],
) -> float:
    grad = gradient_fn(psi)
    return float(np.sqrt(np.mean(np.abs(grad) ** 2)))


def effective_radius(
    psi: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
) -> float:
    rho = np.abs(psi) ** 2
    weight = np.clip(1.0 - rho, 0.0, None)
    total_weight = float(np.sum(weight))
    if total_weight <= 1.0e-12:
        return 0.0
    radius_sq = x * x + y * y + z * z
    return float(np.sqrt(np.sum(weight * radius_sq) / total_weight))


def depressed_fraction(
    psi: np.ndarray,
    threshold: float,
) -> float:
    rho = np.abs(psi) ** 2
    return float(np.count_nonzero(rho < threshold) / rho.size)


def shell_mean_density(
    psi: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    shell_inner: float,
    shell_outer: float,
) -> float:
    radius = np.sqrt(x * x + y * y + z * z)
    mask = (radius >= shell_inner) & (radius <= shell_outer)
    if not np.any(mask):
        return 1.0
    rho = np.abs(psi) ** 2
    return float(np.mean(rho[mask]))

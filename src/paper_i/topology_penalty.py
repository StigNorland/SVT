"""Topology-preserving density penalty for trefoil/knot relaxation.

Identifies vortex-core regions from the initial state (where density is low)
and adds a penalty for filling these regions with high density.  This biases
the relaxation toward keeping the vortex tube structure intact, which in turn
preserves the phase winding (the soliton-vortex correspondence: a density
depression along a closed curve forces 2pi phase winding around it).

Penalty form:

    E_penalty = mu * sum_i mask_i * max(rho_i - rho_target, 0)^2 * dx^3

where mask_i = 1 if initial rho_i < mask_threshold, else 0, and
rho_target is a small density floor below which no penalty is applied.

Variational gradient wrt psi^*(x) (per-cell density, no dx^3 factor — matches
the logse_gradient and lperp_gradient conventions used elsewhere in this code):

    delta E_penalty / delta psi^*(x) = 2 * mu * mask * max(rho - rho_target, 0) * psi
"""

from __future__ import annotations

import numpy as np


def core_mask(psi_initial: np.ndarray, threshold: float) -> np.ndarray:
    """Boolean mask of cells whose initial density is below threshold.

    These regions are interpreted as the initial vortex-core tube and are
    preserved by the topology penalty.
    """
    rho_init = np.abs(psi_initial) ** 2
    return rho_init < threshold


def topology_penalty_energy(
    psi: np.ndarray,
    mask: np.ndarray,
    rho_target: float,
    mu: float,
    dx: float,
) -> float:
    """Penalty energy for filling initial vortex-core regions."""
    if mu == 0.0:
        return 0.0
    rho = np.abs(psi) ** 2
    excess = np.maximum(rho - rho_target, 0.0)
    return float(mu * np.sum(mask * excess ** 2) * (dx ** 3))


def topology_penalty_gradient(
    psi: np.ndarray,
    mask: np.ndarray,
    rho_target: float,
    mu: float,
) -> np.ndarray:
    """Variational gradient delta E / delta psi^* at each cell."""
    if mu == 0.0:
        return np.zeros_like(psi)
    rho = np.abs(psi) ** 2
    excess = np.maximum(rho - rho_target, 0.0)
    return 2.0 * mu * mask * excess * psi

"""Lattice vortex topology diagnostics for 3D complex fields.

Core function: count_vortex_links(psi) — counts plaquettes with quantised
phase winding |W| > pi.  This is the lattice measure of total vortex line
length; for a trefoil knot it remains approximately constant as long as
the topology is preserved.

Resolution limit: the method requires dx << xi / pi ~ 0.32 xi so that the
phase difference between adjacent grid points stays below pi near the vortex
core.  At the production grid (n=24, hw=6, dx=0.5 xi), converged sharp cores
produce phase jumps > pi that wrap to zero — making the link count 0 even
with intact topology.  Reliable detection requires n >= 48 at hw=6 (dx=0.25 xi).

Theory: on a cubic lattice, a vortex line passing through a face (plaquette)
produces a phase circulation of +/-2pi around that face.  Summing the four
wrapped edge-phase differences around each plaquette gives the winding W.
|W| > pi detects the vortex link; the sign gives the vortex direction.
"""

from __future__ import annotations

import numpy as np


def _wrap(dphi: np.ndarray) -> np.ndarray:
    """Wrap phase differences to (-pi, pi]."""
    return (dphi + np.pi) % (2.0 * np.pi) - np.pi


def count_vortex_links(psi: np.ndarray) -> int:
    """Count plaquettes with |phase winding| > pi in a 3D complex field.

    Each plaquette with winding ~+/-2pi corresponds to one lattice link of
    a quantised vortex line.  The total count equals the total vortex line
    length in lattice units (= physical length / dx).

    Parameters
    ----------
    psi : ndarray, shape (Nx, Ny, Nz), complex
        The field on a 3D lattice.

    Returns
    -------
    int
        Number of vortex link plaquettes across all three face orientations.
    """
    phi = np.angle(psi)

    dphi_dx = _wrap(np.diff(phi, axis=0))  # (Nx-1, Ny, Nz)
    dphi_dy = _wrap(np.diff(phi, axis=1))  # (Nx, Ny-1, Nz)
    dphi_dz = _wrap(np.diff(phi, axis=2))  # (Nx, Ny, Nz-1)

    # xy-plaquette circulation (detects z-direction vorticity):
    # W_z(i,j,k) = dphi_dx[i,j,k] + dphi_dy[i+1,j,k]
    #            - dphi_dx[i,j+1,k] - dphi_dy[i,j,k]
    Wz = (dphi_dx[:, :-1, :] + dphi_dy[1:, :, :]
          - dphi_dx[:, 1:, :] - dphi_dy[:-1, :, :])  # (Nx-1, Ny-1, Nz)

    # xz-plaquette circulation (detects y-direction vorticity):
    # W_y(i,j,k) = dphi_dx[i,j,k] + dphi_dz[i+1,j,k]
    #            - dphi_dx[i,j,k+1] - dphi_dz[i,j,k]
    Wy = (dphi_dx[:, :, :-1] + dphi_dz[1:, :, :]
          - dphi_dx[:, :, 1:] - dphi_dz[:-1, :, :])  # (Nx-1, Ny, Nz-1)

    # yz-plaquette circulation (detects x-direction vorticity):
    # W_x(i,j,k) = dphi_dy[i,j,k] + dphi_dz[i,j+1,k]
    #            - dphi_dy[i,j,k+1] - dphi_dz[i,j,k]
    Wx = (dphi_dy[:, :, :-1] + dphi_dz[:, 1:, :]
          - dphi_dy[:, :, 1:] - dphi_dz[:, :-1, :])  # (Nx, Ny-1, Nz-1)

    return int(
        np.sum(np.abs(Wz) > np.pi)
        + np.sum(np.abs(Wy) > np.pi)
        + np.sum(np.abs(Wx) > np.pi)
    )


def vortex_link_density(psi: np.ndarray, dx: float) -> float:
    """Total vortex line length per unit volume (physical units).

    Normalises count_vortex_links by grid volume so results are comparable
    across different grid spacings at the same box size.

    Returns vortex length / volume in units of xi^{-2}.
    """
    n_links = count_vortex_links(psi)
    n = psi.shape[0]
    volume = (n * dx) ** 3
    return n_links * dx / volume

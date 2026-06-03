"""Numba-accelerated kernels for the trefoil gradient flow (#77 Track 2).

If numba is available, the three per-step hot functions — count_vortex_links,
the LogSE gradient (laplacian + potential), and total_energy — are JIT-compiled
and parallelized across the first grid axis with prange. Each kernel reproduces
its numpy reference to machine precision (see test_numba_match below).

Falls back transparently to numpy if numba is not installed: callers check
NUMBA_AVAILABLE.

All stencils use periodic wraparound, matching the np.roll semantics of the
numpy reference (trefoil_breather_static.laplacian and
trefoil_observables.energy_density). Dirichlet boundary pinning is applied
separately by apply_boundary_anchor after each step.
"""

from __future__ import annotations

import math

import numpy as np

try:
    from numba import njit, prange
    NUMBA_AVAILABLE = True
except ImportError:  # pragma: no cover
    NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):  # type: ignore
        def deco(f):
            return f
        return deco(args[0]) if args and callable(args[0]) else deco

    prange = range  # type: ignore


@njit(cache=True)
def _wrap(d: float) -> float:
    twopi = 2.0 * math.pi
    return (d + math.pi) % twopi - math.pi


@njit(parallel=True, cache=True)
def count_links_numba(psi: np.ndarray) -> int:
    """Fused parallel version of topology_helpers.count_vortex_links.

    Two parallel passes: (1) compute phi = angle(psi) once (n^3 atan2, in
    parallel — this is the single-threaded bottleneck in the numpy reference),
    (2) plaquette winding from phi using cheap wrapped subtractions. Counts
    plaquettes with |phase winding| > pi across all three face orientations.
    """
    nx, ny, nz = psi.shape
    phi = np.empty((nx, ny, nz), dtype=np.float64)
    for i in prange(nx):
        for j in range(ny):
            for k in range(nz):
                c = psi[i, j, k]
                phi[i, j, k] = math.atan2(c.imag, c.real)

    counts = np.zeros(nz, dtype=np.int64)
    for k in prange(nz):
        cnt = 0
        # Wz plaquette (xy face): i in [0,nx-1), j in [0,ny-1), all k
        for i in range(nx - 1):
            for j in range(ny - 1):
                w = (_wrap(phi[i + 1, j, k] - phi[i, j, k])
                     + _wrap(phi[i + 1, j + 1, k] - phi[i + 1, j, k])
                     - _wrap(phi[i + 1, j + 1, k] - phi[i, j + 1, k])
                     - _wrap(phi[i, j + 1, k] - phi[i, j, k]))
                if abs(w) > math.pi:
                    cnt += 1
        if k < nz - 1:
            # Wy plaquette (xz face): i in [0,nx-1), all j, k in [0,nz-1)
            for i in range(nx - 1):
                for j in range(ny):
                    w = (_wrap(phi[i + 1, j, k] - phi[i, j, k])
                         + _wrap(phi[i + 1, j, k + 1] - phi[i + 1, j, k])
                         - _wrap(phi[i + 1, j, k + 1] - phi[i, j, k + 1])
                         - _wrap(phi[i, j, k + 1] - phi[i, j, k]))
                    if abs(w) > math.pi:
                        cnt += 1
            # Wx plaquette (yz face): all i, j in [0,ny-1), k in [0,nz-1)
            for i in range(nx):
                for j in range(ny - 1):
                    w = (_wrap(phi[i, j + 1, k] - phi[i, j, k])
                         + _wrap(phi[i, j + 1, k + 1] - phi[i, j + 1, k])
                         - _wrap(phi[i, j + 1, k + 1] - phi[i, j, k + 1])
                         - _wrap(phi[i, j, k + 1] - phi[i, j, k]))
                    if abs(w) > math.pi:
                        cnt += 1
        counts[k] = cnt
    return int(counts.sum())


@njit(parallel=True, cache=True)
def logse_gradient_numba(
    psi: np.ndarray, dx: float, log_pressure: float, density_floor: float
) -> np.ndarray:
    """Fused parallel LogSE gradient: -0.5*laplacian(psi) + log_pressure*log(rho)*psi.

    Periodic 7-point stencil matching trefoil_breather_static.laplacian
    (which uses np.roll). Fuses laplacian and the potential term into one pass.
    """
    nx, ny, nz = psi.shape
    out = np.empty_like(psi)
    inv = 1.0 / (dx * dx)
    for i in prange(nx):
        ip = (i + 1) % nx
        im = (i - 1) % nx
        for j in range(ny):
            jp = (j + 1) % ny
            jm = (j - 1) % ny
            for k in range(nz):
                kp = (k + 1) % nz
                km = (k - 1) % nz
                c = psi[i, j, k]
                lap = (psi[ip, j, k] + psi[im, j, k]
                       + psi[i, jp, k] + psi[i, jm, k]
                       + psi[i, j, kp] + psi[i, j, km]
                       - 6.0 * c) * inv
                rho = c.real * c.real + c.imag * c.imag
                if rho < density_floor:
                    rho = density_floor
                out[i, j, k] = -0.5 * lap + log_pressure * math.log(rho) * c
    return out


@njit(parallel=True, cache=True)
def energy_total_numba(
    psi: np.ndarray, dx: float, log_pressure: float, density_floor: float
) -> float:
    """Parallel total LogSE energy, matching trefoil_observables.total_energy.

    Forward-difference gradient (periodic) summed over 3 axes, plus the
    log potential, integrated over the cell volume dx^3.
    """
    nx, ny, nz = psi.shape
    inv = 1.0 / (dx * dx)
    partial = np.zeros(nx, dtype=np.float64)
    for i in prange(nx):
        ip = (i + 1) % nx
        local = 0.0
        for j in range(ny):
            jp = (j + 1) % ny
            for k in range(nz):
                kp = (k + 1) % nz
                c = psi[i, j, k]
                dxp = psi[ip, j, k] - c
                dyp = psi[i, jp, k] - c
                dzp = psi[i, j, kp] - c
                grad_sq = (
                    dxp.real * dxp.real + dxp.imag * dxp.imag
                    + dyp.real * dyp.real + dyp.imag * dyp.imag
                    + dzp.real * dzp.real + dzp.imag * dzp.imag
                ) * inv
                rho = c.real * c.real + c.imag * c.imag
                if rho < density_floor:
                    rho = density_floor
                pot = log_pressure * (rho * math.log(rho) - rho + 1.0)
                local += 0.5 * grad_sq + pot
        partial[i] = local
    return float(partial.sum()) * dx * dx * dx


def test_numba_match(n: int = 32, seed: int = 0) -> dict:
    """Verify numba kernels reproduce the numpy references to machine precision."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from topology_helpers import count_vortex_links
    from trefoil_observables import total_energy
    from trefoil_breather_static import laplacian

    rng = np.random.default_rng(seed)
    psi = (rng.standard_normal((n, n, n)) + 1j * rng.standard_normal((n, n, n))).astype(np.complex128)
    dx, lp, df = 0.25, 0.5, 1e-12

    links_np = count_vortex_links(psi)
    links_nb = count_links_numba(psi)

    e_np = total_energy(psi, dx, lp, df)
    e_nb = energy_total_numba(psi, dx, lp, df)

    g_np = -0.5 * laplacian(psi, dx) + lp * np.log(np.maximum(np.abs(psi) ** 2, df)) * psi
    g_nb = logse_gradient_numba(psi, dx, lp, df)
    g_err = float(np.max(np.abs(g_np - g_nb)))

    return {
        "links_np": links_np, "links_nb": links_nb, "links_match": links_np == links_nb,
        "energy_np": e_np, "energy_nb": e_nb, "energy_relerr": abs(e_np - e_nb) / abs(e_np),
        "gradient_max_abs_err": g_err,
    }


if __name__ == "__main__":
    print(f"NUMBA_AVAILABLE = {NUMBA_AVAILABLE}")
    res = test_numba_match()
    for k, v in res.items():
        print(f"  {k}: {v}")

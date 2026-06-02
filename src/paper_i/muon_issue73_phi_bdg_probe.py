"""Issue #73: minimal direct m_phi=+/-1 toroidal BdG grid check.

This is a diagnostic solver, not a closure-grade muon calculation.  It replaces
the hand-picked Kelvin seed family used in issue #72 with cell-local basis
functions on the meridional (r,z) grid and keeps only the m_phi=+/-1 Fourier
sector.  The L_perp contribution is assembled from the same selection-rule
audited current-curl routines used by kelvin_augmented_bdg.py.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
from typing import Callable

import numpy as np

from kelvin_augmented_bdg import (
    AzimuthalMode,
    background_second_current_curl_overlap,
    current_curl_component_overlap,
    dense_eigenvalues,
)
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig, projection_window_weight


ComplexField = Callable[[float, float], complex]


@dataclass(frozen=True)
class GridCell:
    index: int
    i: int
    j: int
    r: float
    z: float
    weight: float


@dataclass(frozen=True)
class ProbeResult:
    label: str
    cfg: ProjectionConfig
    active_cells: int
    matrix_size: int
    hermitian_l_residual: float
    symmetric_m_residual: float
    particle_hole_residual: float
    forbidden_l: float
    forbidden_m: float
    allowed_l: float
    allowed_m: float
    solver: str
    positive: list[float]


def parse_float_list(raw: str) -> list[float]:
    return [float(part) for part in raw.split(",") if part.strip()]


def build_cells(bg, cfg: ProjectionConfig) -> list[GridCell]:
    cells: list[GridCell] = []
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            window = projection_window_weight(bg, r, z, cfg)
            if window <= 0.0:
                continue
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz * window
            cells.append(GridCell(len(cells), i, j, r, z, weight))
    return cells


def make_cell_field(cell: GridCell, cells_by_ij: dict[tuple[int, int], GridCell], cfg: ProjectionConfig) -> ComplexField:
    r_min = cell.r - (cell.i + 0.5) * cfg.dr
    z_min = cell.z - (cell.j + 0.5) * cfg.dz
    norm = 1.0 / math.sqrt(cell.weight)

    def field(r: float, z: float) -> complex:
        i = int(round((r - r_min) / cfg.dr - 0.5))
        j = int(round((z - z_min) / cfg.dz - 0.5))
        here = cells_by_ij.get((i, j))
        if here is None or here.index != cell.index:
            return 0.0j
        return norm + 0.0j

    return field


def build_grid_modes(cells: list[GridCell], cfg: ProjectionConfig) -> list[AzimuthalMode]:
    cells_by_ij = {(cell.i, cell.j): cell for cell in cells}
    modes: list[AzimuthalMode] = []
    for m_phi in (-1, 1):
        for cell in cells:
            modes.append(
                AzimuthalMode(
                    name=f"cell_m{m_phi:+d}_{cell.i}_{cell.j}",
                    field=make_cell_field(cell, cells_by_ij, cfg),
                    m_phi=m_phi,
                )
            )
    return modes


def phase_sq(bg, r: float, z: float) -> complex:
    psi = bg.psi0(r, z)
    amp = abs(psi)
    if amp < 1.0e-14:
        return 1.0 + 0.0j
    return (psi / amp) ** 2


def assemble_local_blocks(bg, cells: list[GridCell], cfg: ProjectionConfig, m_phi: int) -> tuple[np.ndarray, np.ndarray]:
    n = len(cells)
    by_ij = {(cell.i, cell.j): cell.index for cell in cells}
    l_block = np.zeros((n, n), dtype=complex)
    m_block = np.zeros((n, n), dtype=complex)
    for cell in cells:
        row = cell.index
        psi = bg.psi0(cell.r, cell.z)
        amp_sq = max(abs(psi) ** 2, 1.0e-12)
        potential = math.log(amp_sq) + 1.0
        diag = 2.0 / (cfg.dr * cfg.dr) + 0.5 * (m_phi * m_phi) / max(cell.r * cell.r, 1.0e-12) + potential
        l_block[row, row] += diag
        m_block[row, row] += phase_sq(bg, cell.r, cell.z)
        neighbors = (
            (cell.i + 1, cell.j, -0.5 / (cfg.dr * cfg.dr) - 0.25 / (cell.r * cfg.dr)),
            (cell.i - 1, cell.j, -0.5 / (cfg.dr * cfg.dr) + 0.25 / (cell.r * cfg.dr)),
            (cell.i, cell.j + 1, -0.5 / (cfg.dz * cfg.dz)),
            (cell.i, cell.j - 1, -0.5 / (cfg.dz * cfg.dz)),
        )
        for ni, nj, coeff in neighbors:
            col = by_ij.get((ni, nj))
            if col is None:
                continue
            # Convert the finite-difference strong operator to the normalized
            # cell-indicator basis used for the weighted inner product.
            l_block[row, col] += coeff * math.sqrt(cell.weight / cells[col].weight)
    return l_block, m_block


def current_curl_blocks(bg, modes: list[AzimuthalMode], cfg: ProjectionConfig, model: str) -> tuple[np.ndarray, np.ndarray]:
    n = len(modes)
    l_block = np.zeros((n, n), dtype=complex)
    m_block = np.zeros((n, n), dtype=complex)
    for i, bra in enumerate(modes):
        for j, ket in enumerate(modes):
            if bra.m_phi == ket.m_phi:
                uu_ab = current_curl_component_overlap(bg, bra, "u", ket, "u", cfg)
                uu_ba = current_curl_component_overlap(bg, ket, "u", bra, "u", cfg).conjugate()
                l_block[i, j] = 0.5 * (uu_ab + uu_ba)
            if bra.m_phi + ket.m_phi == 0:
                uv_ab = current_curl_component_overlap(bg, bra, "u", ket, "v", cfg)
                uv_ba = current_curl_component_overlap(bg, ket, "u", bra, "v", cfg)
                m_block[i, j] = 0.5 * (uv_ab + uv_ba)
            if model == "full":
                l_bg_ab = background_second_current_curl_overlap(bg, bra, ket, cfg, pair_type="normal")
                l_bg_ba = background_second_current_curl_overlap(bg, ket, bra, cfg, pair_type="normal").conjugate()
                m_bg_ab = background_second_current_curl_overlap(bg, bra, ket, cfg, pair_type="anomalous")
                m_bg_ba = background_second_current_curl_overlap(bg, ket, bra, cfg, pair_type="anomalous")
                l_block[i, j] += 0.5 * (l_bg_ab + l_bg_ba)
                m_block[i, j] += 0.5 * (m_bg_ab + m_bg_ba)
            elif model != "linear":
                raise ValueError(f"unknown current_curl_model: {model}")
    return l_block, m_block


def assemble_bdg(bg, cells: list[GridCell], cfg: ProjectionConfig, lambda_perp: float, current_curl_model: str) -> tuple[np.ndarray, list[AzimuthalMode]]:
    modes = build_grid_modes(cells, cfg)
    n_cell = len(cells)
    l_minus, m_minus = assemble_local_blocks(bg, cells, cfg, m_phi=-1)
    l_plus, m_plus = assemble_local_blocks(bg, cells, cfg, m_phi=1)
    n_mode = 2 * n_cell
    l_block = np.zeros((n_mode, n_mode), dtype=complex)
    m_block = np.zeros((n_mode, n_mode), dtype=complex)
    l_block[:n_cell, :n_cell] = l_minus
    l_block[n_cell:, n_cell:] = l_plus
    # The local LogSE pairing carries the anomalous selection rule m_a+m_b=0.
    m_block[:n_cell, n_cell:] = m_minus
    m_block[n_cell:, :n_cell] = m_plus

    if lambda_perp != 0.0:
        l_perp, m_perp = current_curl_blocks(bg, modes, cfg, current_curl_model)
        l_block += lambda_perp * l_perp
        m_block += lambda_perp * m_perp

    h = np.zeros((2 * n_mode, 2 * n_mode), dtype=complex)
    h[:n_mode, :n_mode] = l_block
    h[:n_mode, n_mode:] = m_block
    h[n_mode:, :n_mode] = -m_block.conjugate()
    h[n_mode:, n_mode:] = -l_block.conjugate()
    return h, modes


def symmetry_receipts(h: np.ndarray, modes: list[AzimuthalMode], bg, cfg: ProjectionConfig) -> dict[str, float]:
    n = len(modes)
    l_block = h[:n, :n]
    m_block = h[:n, n:]
    sigma = np.block(
        [
            [np.zeros((n, n), dtype=complex), np.eye(n, dtype=complex)],
            [np.eye(n, dtype=complex), np.zeros((n, n), dtype=complex)],
        ]
    )
    particle_hole = float(np.max(np.abs(h + sigma @ h.conjugate() @ sigma)))
    m0 = AzimuthalMode("probe_m0", modes[0].field, 0)
    mplus = next(mode for mode in modes if mode.m_phi == 1)
    mminus = next(mode for mode in modes if mode.m_phi == -1)
    l_forbidden, m_forbidden = current_curl_blocks(bg, [m0, mplus], cfg, "linear")
    l_allowed, m_allowed = current_curl_blocks(bg, [mplus, mminus], cfg, "linear")
    return {
        "hermitian_l_residual": float(np.max(np.abs(l_block - l_block.conjugate().T))),
        "symmetric_m_residual": float(np.max(np.abs(m_block - m_block.T))),
        "particle_hole_residual": particle_hole,
        "forbidden_l": float(abs(l_forbidden[0, 1])),
        "forbidden_m": float(abs(m_forbidden[0, 1])),
        "allowed_l": float(abs(l_allowed[0, 0])),
        "allowed_m": float(abs(m_allowed[0, 1])),
    }


def solve_point(
    label: str,
    n: int,
    half_width: float,
    window_kind: str,
    window_radius: float,
    profile_n: int,
    lambda_perp: float,
    current_curl_model: str,
) -> ProbeResult:
    cfg = ProjectionConfig(
        n=n,
        half_width=half_width,
        profile="numerical",
        profile_n=profile_n,
        projection_window=window_kind,
        window_radius=window_radius,
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    cells = build_cells(bg, cfg)
    h, modes = assemble_bdg(bg, cells, cfg, lambda_perp, current_curl_model)
    receipts = symmetry_receipts(h, modes, bg, cfg)
    eigs, solver = dense_eigenvalues(h.tolist())
    positive = sorted(value.real for value in eigs if value.real > 1.0e-6 and abs(value.imag) <= 1.0e-6)
    distinct: list[float] = []
    for value in positive:
        if not distinct or abs(value - distinct[-1]) > 1.0e-4:
            distinct.append(value)
    return ProbeResult(
        label=label,
        cfg=cfg,
        active_cells=len(cells),
        matrix_size=h.shape[0],
        solver=solver,
        positive=distinct,
        **receipts,
    )


def print_result_table(results: list[ProbeResult]) -> None:
    print("\n## Direct phi/Fourier m=+/-1 grid results")
    print("label n hw window r_w cells matrix lowest second third")
    for result in results:
        vals = result.positive[:3] + [float("nan")] * max(0, 3 - len(result.positive))
        print(
            f"{result.label} {result.cfg.n:d} {result.cfg.half_width:.1f} "
            f"{result.cfg.projection_window} {result.cfg.window_radius:.1f} "
            f"{result.active_cells:d} {result.matrix_size:d} "
            f"{vals[0]:.6f} {vals[1]:.6f} {vals[2]:.6f}"
        )


def print_receipts(result: ProbeResult) -> None:
    print("\n## Symmetry and selection-rule receipts")
    print(f"reference                = {result.label}")
    print(f"eigensolver              = {result.solver}")
    print(f"max |L-L^dagger|         = {result.hermitian_l_residual:.3e}")
    print(f"max |M-M^T|              = {result.symmetric_m_residual:.3e}")
    print(f"max particle-hole resid  = {result.particle_hole_residual:.3e}")
    print(f"forbidden L(m0,+1)       = {result.forbidden_l:.3e}")
    print(f"forbidden M(m0,+1)       = {result.forbidden_m:.3e}")
    print(f"allowed L(+1,+1)         = {result.allowed_l:.3e}")
    print(f"allowed M(+1,-1)         = {result.allowed_m:.3e}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #73 direct m_phi=+/-1 toroidal BdG grid probe.")
    parser.add_argument("--n-values", default="11,13,15")
    parser.add_argument("--half-width", type=float, default=8.0)
    parser.add_argument("--window", choices=("hard", "smooth", "none"), default="hard")
    parser.add_argument("--window-radius", type=float, default=4.0)
    parser.add_argument("--profile-n", type=int, default=800)
    parser.add_argument("--lambda-perp", type=float, default=math.pi / 4.0)
    parser.add_argument("--current-curl-model", choices=("linear", "full"), default="linear")
    parser.add_argument("--skip-lperp", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    lambda_perp = 0.0 if args.skip_lperp else args.lambda_perp
    results: list[ProbeResult] = []
    for n in parse_float_list(args.n_values):
        label = f"n{int(n)}"
        results.append(
            solve_point(
                label=label,
                n=int(n),
                half_width=args.half_width,
                window_kind=args.window,
                window_radius=args.window_radius,
                profile_n=args.profile_n,
                lambda_perp=lambda_perp,
                current_curl_model=args.current_curl_model,
            )
        )
    print("Issue #73 direct phi/Fourier BdG probe")
    print(f"half_width              = {args.half_width:.6g}")
    print(f"window                  = {args.window}")
    print(f"window_radius           = {args.window_radius:.6g}")
    print(f"profile_n               = {args.profile_n}")
    print(f"lambda_perp             = {lambda_perp:.9e}")
    print(f"current_curl_model      = {args.current_curl_model}")
    print_result_table(results)
    print_receipts(results[-1])


if __name__ == "__main__":
    main()

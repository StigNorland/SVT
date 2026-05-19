"""Extract N_Y / F from a saved (2,3)-trefoil knot state.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: N_Y, F, mu_0_grid, E_line, E_cavity, E_total
Primary role: closed-knot analogue of trefoil_y_junction_closed_observables.py.
              The (2,3)-trefoil knot is a single continuous closed curve with
              no Y-junctions, so the decomposition is one line tube + one
              cavity ball + bulk residual.
Key limitation: tube radius, cavity radius and calibration half-width are free
                parameters; mu_0 here is the energy per unit arc-length of a
                continuously curved knotted vortex line, so it bakes in
                curvature and is not comparable to the open-Y straight-line mu_0.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, ScriptMetadata
from trefoil_observables import energy_density
from trefoil_breather_static import trefoil_curve


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("N_Y", "F", "mu_0_grid", "E_line", "E_cavity", "E_total"),
    diagnostics=("anchor_shell_energy_fraction", "min_density_position"),
    issue_refs=("#13",),
    limitations=(
        "Tube radius, cavity radius and calibration half-width are free parameters.",
        "mu_0_grid is the energy per unit arc-length along a continuously curved knot, so it bakes in curvature effects.",
        "Closed (2,3)-trefoil-knot geometry only; assumes state was produced by trefoil_breather_static.py.",
    ),
)


@dataclass(frozen=True)
class ExtractionConfig:
    r_tube: float
    r_cavity: float
    cal_arc_half_width: float
    anchor_thickness_xi: float = -1.0  # if >0, overrides cell-based anchor_shell with a fixed physical thickness


@dataclass(frozen=True)
class ExtractionSummary:
    state_path: str
    n: int
    half_width: float
    spacing: float
    log_pressure: float
    major_radius: float
    minor_radius: float
    e_total_raw: float
    e_anchor_shell: float
    e_interior: float
    anchor_cells_used: int
    anchor_thickness_xi_actual: float
    e_line: float
    e_cavity: float
    e_bulk_residual: float
    mu_0_grid: float
    cal_energy: float
    cal_length: float
    l_curve_geometric: float
    l_line_tube: float
    tube_volume: float
    n_y_per_xi: float
    n_y_per_curve_length: float
    f_factor_interior: float
    f_factor_raw: float
    min_density: float
    min_density_position: tuple[float, float, float]


def load_state(path: Path) -> dict:
    data = np.load(path, allow_pickle=False)
    cfg_raw = data["config"].item() if data["config"].ndim == 0 else str(data["config"])
    if isinstance(cfg_raw, bytes):
        cfg_raw = cfg_raw.decode("utf-8")
    cfg = json.loads(cfg_raw)
    psi = data["psi_real"] + 1j * data["psi_imag"]
    return {
        "cfg": cfg,
        "psi": psi.astype(np.complex128),
        "x": np.asarray(data["x"], dtype=float),
        "y": np.asarray(data["y"], dtype=float),
        "z": np.asarray(data["z"], dtype=float),
    }


def cumulative_arc_length_closed(pos: np.ndarray) -> tuple[np.ndarray, float]:
    """Cumulative arc-length at each sample, plus total length (including the
    wraparound segment from the last sample back to the first).
    """
    deltas = np.diff(pos, axis=0)
    seg = np.linalg.norm(deltas, axis=1)
    s = np.concatenate(([0.0], np.cumsum(seg)))
    closing = float(np.linalg.norm(pos[0] - pos[-1]))
    return s, float(s[-1] + closing)


def extract(state: dict, ec: ExtractionConfig) -> ExtractionSummary:
    psi = state["psi"]
    x, y, z = state["x"], state["y"], state["z"]
    cfg_dict = state["cfg"]
    n = int(cfg_dict["n"])
    half_width = float(cfg_dict["half_width"])
    spacing = 2.0 * half_width / n
    log_pressure = float(cfg_dict.get("log_pressure", 0.5))
    density_floor = float(cfg_dict.get("density_floor", 1.0e-12))
    anchor_shell = int(cfg_dict.get("anchor_shell", 2))
    major_radius = float(cfg_dict["major_radius"])
    minor_radius = float(cfg_dict["minor_radius"])
    frame_samples = int(cfg_dict.get("frame_samples", 600))

    cell_volume = spacing**3
    edens = energy_density(psi, spacing, log_pressure, density_floor)
    e_total = float(np.sum(edens) * cell_volume)

    # Anchor shell: by default uses the cell-based anchor_shell from cfg.
    # If ec.anchor_thickness_xi > 0, use a fixed physical thickness instead
    # (grid-invariant: cells within anchor_thickness_xi of any box face are excluded).
    if ec.anchor_thickness_xi > 0.0:
        anchor_cells = max(1, int(round(ec.anchor_thickness_xi / spacing)))
    else:
        anchor_cells = anchor_shell
    anchor_mask = np.zeros_like(edens, dtype=bool)
    if anchor_cells > 0:
        anchor_mask[:anchor_cells, :, :] = True
        anchor_mask[-anchor_cells:, :, :] = True
        anchor_mask[:, :anchor_cells, :] = True
        anchor_mask[:, -anchor_cells:, :] = True
        anchor_mask[:, :, :anchor_cells] = True
        anchor_mask[:, :, -anchor_cells:] = True
    e_anchor_shell = float(np.sum(edens[anchor_mask]) * cell_volume)
    e_interior = e_total - e_anchor_shell

    curve, _tangent, _normal, _binormal = trefoil_curve(
        samples=frame_samples,
        major_radius=major_radius,
        minor_radius=minor_radius,
    )
    s_cum, l_curve_geometric = cumulative_arc_length_closed(curve)

    points = np.stack((x, y, z), axis=-1)
    offsets = points[None, ...] - curve[:, None, None, None, :]
    dist_sq = np.sum(offsets * offsets, axis=-1)
    nearest_idx = np.argmin(dist_sq, axis=0)
    d_curve = np.sqrt(np.take_along_axis(dist_sq, nearest_idx[None, ...], axis=0)[0])
    s_at_cell = s_cum[nearest_idx]

    radius = np.sqrt(x * x + y * y + z * z)

    cavity_mask = (radius < ec.r_cavity) & (~anchor_mask)
    e_cavity = float(np.sum(edens[cavity_mask]) * cell_volume)

    line_mask = (d_curve < ec.r_tube) & (radius >= ec.r_cavity) & (~anchor_mask)
    e_line = float(np.sum(edens[line_mask]) * cell_volume)
    tube_volume = float(np.sum(line_mask) * cell_volume)
    l_line_tube = tube_volume / (math.pi * ec.r_tube * ec.r_tube) if ec.r_tube > 0 else 0.0

    # Self-calibration: take an arc-length slab centred at L/3 (avoids the t=0
    # boundary and the most symmetric subdivision points).
    cal_center = l_curve_geometric / 3.0
    cal_half = ec.cal_arc_half_width
    # s_at_cell can be anywhere in [0, s_cum[-1]]; treat it linearly here
    cal_mask = line_mask & (s_at_cell >= cal_center - cal_half) & (s_at_cell <= cal_center + cal_half)
    cal_energy = float(np.sum(edens[cal_mask]) * cell_volume)
    cal_length = 2.0 * cal_half
    mu_0_grid = cal_energy / cal_length if cal_length > 0 else 0.0

    e_bulk_residual = e_interior - e_line - e_cavity

    if mu_0_grid > 0.0:
        n_y_per_xi = (e_line + e_cavity) / mu_0_grid
        denom = mu_0_grid * l_line_tube if l_line_tube > 0 else 0.0
        n_y_per_curve_length = (e_line + e_cavity) / denom if denom > 0 else float("nan")
        f_factor_interior = e_interior / (n_y_per_xi * mu_0_grid)
        f_factor_raw = e_total / (n_y_per_xi * mu_0_grid)
    else:
        n_y_per_xi = float("nan")
        n_y_per_curve_length = float("nan")
        f_factor_interior = float("nan")
        f_factor_raw = float("nan")

    rho = np.abs(psi) ** 2
    flat_idx = int(np.argmin(rho))
    i, j, k = np.unravel_index(flat_idx, rho.shape)
    min_density = float(rho[i, j, k])
    min_pos = (float(x[i, j, k]), float(y[i, j, k]), float(z[i, j, k]))

    return ExtractionSummary(
        state_path="",
        n=n,
        half_width=half_width,
        spacing=spacing,
        log_pressure=log_pressure,
        major_radius=major_radius,
        minor_radius=minor_radius,
        e_total_raw=e_total,
        e_anchor_shell=e_anchor_shell,
        e_interior=e_interior,
        anchor_cells_used=anchor_cells,
        anchor_thickness_xi_actual=anchor_cells * spacing,
        e_line=e_line,
        e_cavity=e_cavity,
        e_bulk_residual=e_bulk_residual,
        mu_0_grid=mu_0_grid,
        cal_energy=cal_energy,
        cal_length=cal_length,
        l_curve_geometric=l_curve_geometric,
        l_line_tube=l_line_tube,
        tube_volume=tube_volume,
        n_y_per_xi=n_y_per_xi,
        n_y_per_curve_length=n_y_per_curve_length,
        f_factor_interior=f_factor_interior,
        f_factor_raw=f_factor_raw,
        min_density=min_density,
        min_density_position=min_pos,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract N_Y / F from a saved (2,3)-trefoil knot state.")
    parser.add_argument("state", type=Path, help="Path to .npz saved by trefoil_breather_static.py")
    parser.add_argument("--r-tube", type=float, default=1.5, help="Tube radius (in xi) around the knot curve")
    parser.add_argument("--r-cavity", type=float, default=1.5, help="Cavity ball radius (in xi) around origin")
    parser.add_argument("--cal-arc-half-width", type=float, default=0.5, help="Half-length of arc-length calibration slab")
    parser.add_argument("--anchor-thickness-xi", type=float, default=-1.0, help="If >0, exclude a physical boundary thickness (in xi) from e_interior, overriding the cell-based anchor_shell (grid-invariant comparator)")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    state = load_state(args.state)
    ec = ExtractionConfig(
        r_tube=args.r_tube,
        r_cavity=args.r_cavity,
        cal_arc_half_width=args.cal_arc_half_width,
        anchor_thickness_xi=args.anchor_thickness_xi,
    )
    summary = extract(state, ec)
    summary_payload = asdict(summary)
    summary_payload["state_path"] = str(args.state)

    payload = {
        "metadata": {
            "problem_type": SCRIPT_METADATA.problem_type,
            "status": SCRIPT_METADATA.status.value,
            "nondimensionalisation": SCRIPT_METADATA.nondimensionalisation,
            "observables": SCRIPT_METADATA.observables,
            "diagnostics": SCRIPT_METADATA.diagnostics,
            "issue_refs": SCRIPT_METADATA.issue_refs,
            "limitations": SCRIPT_METADATA.limitations,
        },
        "extraction_config": asdict(ec),
        "summary": summary_payload,
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

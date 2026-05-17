"""Extract N_Y and F from a saved closed Y-junction (theta-graph) state.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: N_Y, F, mu_0_grid, per-arc tube energies, top/bottom node ball energies
Primary role: closed-topology analogue of trefoil_y_junction_observables.py;
              handles arc filaments and two Y-nodes for the theta-graph geometry.
Key limitation: tube radius, node radius and equatorial calibration half-width are
                free parameters; mu_0 here is the energy-per-unit-arc-length of a
                curved filament, not the straight-line value of the open-Y extractor.
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
from trefoil_y_junction_closed_static import YJunctionClosedConfig, arc_curve


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=(
        "N_Y",
        "F",
        "mu_0_grid",
        "E_filaments",
        "E_node_top",
        "E_node_bottom",
        "E_total",
    ),
    diagnostics=("anchor_shell_energy_fraction", "tube_arc_length_vs_geometric"),
    issue_refs=("#13",),
    limitations=(
        "Tube radius, node radius, and equatorial calibration half-width are free parameters.",
        "mu_0_grid here is the energy per unit arc-length of a curved filament, so it bakes in arc curvature; not directly comparable to the open-Y straight-line mu_0.",
        "Closed theta-graph geometry only; assumes the state was produced by trefoil_y_junction_closed_static.py.",
    ),
)


@dataclass(frozen=True)
class ExtractionConfig:
    r_tube: float
    r_node: float
    cal_half_width: float  # half-length of the equatorial calibration slab, in xi


@dataclass(frozen=True)
class FilamentReport:
    index: int
    tube_energy: float
    tube_volume: float
    tube_arc_length: float
    geometric_arc_length: float
    cal_energy: float
    cal_length: float
    cal_energy_per_length: float


@dataclass(frozen=True)
class ExtractionSummary:
    state_path: str
    n: int
    half_width: float
    spacing: float
    log_pressure: float
    node_radius: float
    arc_radius: float
    e_total_raw: float
    e_anchor_shell: float
    e_interior: float
    e_filaments: float
    e_node_top: float
    e_node_bottom: float
    e_bulk_residual: float
    mu_0_grid: float
    mu_0_per_filament: tuple[float, ...]
    l_filament_total_tube: float
    l_filament_total_geometric: float
    n_y_per_xi: float
    n_y_per_filament_length: float
    f_factor_interior: float
    f_factor_raw: float
    filaments: tuple[FilamentReport, ...]


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


def cumulative_arc_length(pos: np.ndarray) -> np.ndarray:
    """Cumulative geometric arc length at each sample, starting from zero."""
    deltas = np.diff(pos, axis=0)
    seg = np.linalg.norm(deltas, axis=1)
    s = np.concatenate(([0.0], np.cumsum(seg)))
    return s


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
    node_radius = float(cfg_dict["node_radius"])
    arc_radius = float(cfg_dict["arc_radius"])
    samples_per_arc = int(cfg_dict.get("samples_per_arc", 200))

    cell_volume = spacing**3
    edens = energy_density(psi, spacing, log_pressure, density_floor)
    e_total = float(np.sum(edens) * cell_volume)

    anchor_mask = np.zeros_like(edens, dtype=bool)
    if anchor_shell > 0:
        anchor_mask[:anchor_shell, :, :] = True
        anchor_mask[-anchor_shell:, :, :] = True
        anchor_mask[:, :anchor_shell, :] = True
        anchor_mask[:, -anchor_shell:, :] = True
        anchor_mask[:, :, :anchor_shell] = True
        anchor_mask[:, :, -anchor_shell:] = True
    e_anchor_shell = float(np.sum(edens[anchor_mask]) * cell_volume)

    # Build a stand-in YJunctionClosedConfig so we can reuse the same arc_curve
    # that produced the initial condition.
    cfg = YJunctionClosedConfig(
        n=n,
        half_width=half_width,
        xi=float(cfg_dict.get("xi", 1.0)),
        node_radius=node_radius,
        arc_radius=arc_radius,
        samples_per_arc=samples_per_arc,
        log_pressure=log_pressure,
    )

    points = np.stack((x, y, z), axis=-1)

    # Two node-ball masks
    top_pole = np.array([0.0, 0.0, node_radius])
    bot_pole = np.array([0.0, 0.0, -node_radius])
    r_top = np.linalg.norm(points - top_pole, axis=-1)
    r_bot = np.linalg.norm(points - bot_pole, axis=-1)
    node_top_mask = (r_top < ec.r_node) & (~anchor_mask)
    node_bot_mask = (r_bot < ec.r_node) & (~anchor_mask)
    e_node_top = float(np.sum(edens[node_top_mask]) * cell_volume)
    e_node_bot = float(np.sum(edens[node_bot_mask]) * cell_volume)

    # Per-arc nearest-sample distance and arc-length parameter
    per_arc_d = []
    per_arc_s = []  # arc-length at the nearest sample along each arc
    per_arc_geom_length = []
    for k in range(3):
        pos, _e1, _e2 = arc_curve(cfg, k)
        s_cum = cumulative_arc_length(pos)
        per_arc_geom_length.append(float(s_cum[-1]))

        offsets = points[None, ...] - pos[:, None, None, None, :]
        dist_sq = np.sum(offsets * offsets, axis=-1)
        nearest_idx = np.argmin(dist_sq, axis=0)
        d_k = np.sqrt(np.take_along_axis(dist_sq, nearest_idx[None, ...], axis=0)[0])
        s_at_cell = s_cum[nearest_idx]
        per_arc_d.append(d_k)
        per_arc_s.append(s_at_cell)

    d_stack = np.stack(per_arc_d, axis=0)
    nearest_arc = np.argmin(d_stack, axis=0)
    d_min = np.min(d_stack, axis=0)

    filaments: list[FilamentReport] = []
    e_filaments_total = 0.0
    l_filament_total_tube = 0.0
    l_filament_total_geom = 0.0
    for k in range(3):
        d_k = per_arc_d[k]
        s_k = per_arc_s[k]
        s_total = per_arc_geom_length[k]
        s_eq = 0.5 * s_total
        l_filament_total_geom += s_total

        # Tube mask: nearest arc is k, within r_tube, outside both node balls and anchor.
        owns = (
            (nearest_arc == k)
            & (d_min < ec.r_tube)
            & (r_top >= ec.r_node)
            & (r_bot >= ec.r_node)
            & (~anchor_mask)
        )
        tube_energy = float(np.sum(edens[owns]) * cell_volume)
        tube_volume = float(np.sum(owns) * cell_volume)
        tube_arc_length = (
            tube_volume / (math.pi * ec.r_tube * ec.r_tube) if ec.r_tube > 0 else 0.0
        )
        e_filaments_total += tube_energy
        l_filament_total_tube += tube_arc_length

        cal_mask = owns & (s_k >= s_eq - ec.cal_half_width) & (s_k <= s_eq + ec.cal_half_width)
        cal_energy = float(np.sum(edens[cal_mask]) * cell_volume)
        cal_length = 2.0 * ec.cal_half_width
        per_length = cal_energy / cal_length if cal_length > 0 else 0.0

        filaments.append(
            FilamentReport(
                index=k,
                tube_energy=tube_energy,
                tube_volume=tube_volume,
                tube_arc_length=tube_arc_length,
                geometric_arc_length=s_total,
                cal_energy=cal_energy,
                cal_length=cal_length,
                cal_energy_per_length=per_length,
            )
        )

    per_filament_mu0 = tuple(f.cal_energy_per_length for f in filaments)
    mu_0_grid = float(np.mean(per_filament_mu0))

    e_interior = e_total - e_anchor_shell
    e_bulk_residual = e_interior - e_filaments_total - e_node_top - e_node_bot

    if mu_0_grid > 0.0:
        n_y_per_xi = (e_filaments_total + e_node_top + e_node_bot) / mu_0_grid
        denom = mu_0_grid * l_filament_total_tube if l_filament_total_tube > 0 else 0.0
        n_y_per_filament_length = (
            (e_filaments_total + e_node_top + e_node_bot) / denom if denom > 0 else float("nan")
        )
        f_factor_interior = e_interior / (n_y_per_xi * mu_0_grid)
        f_factor_raw = e_total / (n_y_per_xi * mu_0_grid)
    else:
        n_y_per_xi = float("nan")
        n_y_per_filament_length = float("nan")
        f_factor_interior = float("nan")
        f_factor_raw = float("nan")

    return ExtractionSummary(
        state_path="",
        n=n,
        half_width=half_width,
        spacing=spacing,
        log_pressure=log_pressure,
        node_radius=node_radius,
        arc_radius=arc_radius,
        e_total_raw=e_total,
        e_anchor_shell=e_anchor_shell,
        e_interior=e_interior,
        e_filaments=e_filaments_total,
        e_node_top=e_node_top,
        e_node_bottom=e_node_bot,
        e_bulk_residual=e_bulk_residual,
        mu_0_grid=mu_0_grid,
        mu_0_per_filament=per_filament_mu0,
        l_filament_total_tube=l_filament_total_tube,
        l_filament_total_geometric=l_filament_total_geom,
        n_y_per_xi=n_y_per_xi,
        n_y_per_filament_length=n_y_per_filament_length,
        f_factor_interior=f_factor_interior,
        f_factor_raw=f_factor_raw,
        filaments=tuple(filaments),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract N_Y / F from a saved closed Y-junction state.")
    parser.add_argument("state", type=Path, help="Path to .npz saved by trefoil_y_junction_closed_static.py")
    parser.add_argument("--r-tube", type=float, default=2.0, help="Tube radius (in xi) around each arc filament")
    parser.add_argument("--r-node", type=float, default=2.0, help="Node ball radius (in xi) around each Y-node")
    parser.add_argument(
        "--cal-half-width",
        type=float,
        default=0.5,
        help="Half-length (in xi) of the equatorial calibration slab along each arc",
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    state = load_state(args.state)
    ec = ExtractionConfig(
        r_tube=args.r_tube,
        r_node=args.r_node,
        cal_half_width=args.cal_half_width,
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

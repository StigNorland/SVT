"""Extract N_Y and F from a saved Y-junction relaxed state.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: N_Y, F, filament-tube energies, junction-ball energy, mu_0_grid
Primary role: first concrete extractor for the Paper I closure quantities
              N_Y = (E_filaments + E_node) / mu_0_grid,
              F   = E_total / (N_Y * mu_0_grid),
              from a relaxed Y-junction field on the same grid.
Key limitation: tube radius, node radius, and calibration arc-length window
                are free parameters; this is a measurement script, not a derivation.
                Self-calibration assumes the chosen calibration slab is far enough
                from both the node and the boundary anchor to look like a straight
                isolated vortex.
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


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("N_Y", "F", "mu_0_grid", "E_filaments", "E_node", "E_total"),
    diagnostics=("tube_overlap_fraction", "boundary_anchor_energy_fraction"),
    issue_refs=("#13",),
    limitations=(
        "Tube radius, node radius, and calibration arc-length window are free parameters.",
        "Self-calibration assumes the chosen slab is far enough from both the node and the boundary anchor to look like a straight isolated vortex.",
        "The relaxed Y-junction must be produced by trefoil_y_junction_static.py with the equatorial 120 deg geometry; other layouts are not supported.",
    ),
)


@dataclass(frozen=True)
class ExtractionConfig:
    r_tube: float
    r_node: float
    cal_start: float
    cal_stop: float


@dataclass(frozen=True)
class FilamentReport:
    index: int
    tube_energy: float
    tube_volume: float
    tube_arc_length: float
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
    e_total_raw: float
    e_anchor_shell: float
    e_interior: float
    e_filaments: float
    e_node: float
    e_bulk_residual: float
    mu_0_grid: float
    mu_0_per_filament: tuple[float, ...]
    l_filament_total: float
    n_y_per_xi: float
    n_y_per_filament_length: float
    f_factor_interior: float
    f_factor_raw: float
    n_y_per_xi_times_f_interior: float
    filaments: tuple[FilamentReport, ...]


def y_junction_directions() -> np.ndarray:
    angles = np.array([0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0])
    return np.stack([np.cos(angles), np.sin(angles), np.zeros_like(angles)], axis=1)


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


def compute_arc_and_perp(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, dirs: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    points = np.stack((x, y, z), axis=-1)
    s = np.einsum("ijkl,ml->mijk", points, dirs)
    perp = points[None, ...] - s[..., None] * dirs[:, None, None, None, :]
    d = np.sqrt(np.sum(perp * perp, axis=-1))
    return s, d


def extract(state: dict, ec: ExtractionConfig) -> ExtractionSummary:
    psi = state["psi"]
    x, y, z = state["x"], state["y"], state["z"]
    cfg = state["cfg"]
    n = int(cfg["n"])
    half_width = float(cfg["half_width"])
    spacing = 2.0 * half_width / n
    log_pressure = float(cfg.get("log_pressure", 0.5))
    density_floor = float(cfg.get("density_floor", 1.0e-12))
    anchor_shell = int(cfg.get("anchor_shell", 2))

    cell_volume = spacing**3
    edens = energy_density(psi, spacing, log_pressure, density_floor)
    e_total = float(np.sum(edens) * cell_volume)

    # Energy attributed to the boundary-anchor shells; useful as a sanity check
    # since those cells are pinned and their gradient is artificial.
    anchor_mask = np.zeros_like(edens, dtype=bool)
    if anchor_shell > 0:
        anchor_mask[:anchor_shell, :, :] = True
        anchor_mask[-anchor_shell:, :, :] = True
        anchor_mask[:, :anchor_shell, :] = True
        anchor_mask[:, -anchor_shell:, :] = True
        anchor_mask[:, :, :anchor_shell] = True
        anchor_mask[:, :, -anchor_shell:] = True
    e_anchor_shell = float(np.sum(edens[anchor_mask]) * cell_volume)

    dirs = y_junction_directions()
    s, d = compute_arc_and_perp(x, y, z, dirs)
    radius = np.sqrt(x * x + y * y + z * z)

    # Voronoi-by-filament assignment: each grid point belongs to its nearest filament axis.
    nearest = np.argmin(d, axis=0)
    d_min = np.min(d, axis=0)

    node_mask = (radius < ec.r_node) & (~anchor_mask)
    e_node = float(np.sum(edens[node_mask]) * cell_volume)

    filaments: list[FilamentReport] = []
    e_filaments_total = 0.0
    l_filament_total = 0.0
    for k in range(3):
        s_k = s[k]
        owns = (nearest == k) & (d_min < ec.r_tube) & (s_k > 0) & (radius >= ec.r_node) & (~anchor_mask)
        tube_energy = float(np.sum(edens[owns]) * cell_volume)
        tube_volume = float(np.sum(owns) * cell_volume)
        # Effective arc length of this filament's tube: tube_volume divided by
        # transverse area pi*r_tube^2 gives an effective length estimate.
        tube_arc_length = tube_volume / (math.pi * ec.r_tube * ec.r_tube) if ec.r_tube > 0 else 0.0
        e_filaments_total += tube_energy
        l_filament_total += tube_arc_length

        cal_mask = owns & (s_k >= ec.cal_start) & (s_k <= ec.cal_stop)
        cal_energy = float(np.sum(edens[cal_mask]) * cell_volume)
        cal_length = ec.cal_stop - ec.cal_start
        per_length = cal_energy / cal_length if cal_length > 0 else 0.0

        filaments.append(
            FilamentReport(
                index=k,
                tube_energy=tube_energy,
                tube_volume=tube_volume,
                tube_arc_length=tube_arc_length,
                cal_energy=cal_energy,
                cal_length=cal_length,
                cal_energy_per_length=per_length,
            )
        )

    per_filament_mu0 = tuple(f.cal_energy_per_length for f in filaments)
    mu_0_grid = float(np.mean(per_filament_mu0))

    e_interior = e_total - e_anchor_shell
    e_bulk_residual = e_interior - e_filaments_total - e_node

    if mu_0_grid > 0.0:
        # Per-xi normalisation: count of "xi-length filament + node" units in the
        # localised line/node energy.  For our open three-prong Y with filaments
        # of length ~3 xi each, this is ~9 + junction surplus, not the paper's
        # quoted 3.007.
        n_y_per_xi = (e_filaments_total + e_node) / mu_0_grid
        # Per-filament-length normalisation: divides out the geometry-dependent
        # total filament length, isolating the (1 + junction excess / line cost)
        # invariant that should carry over to the closed compact configuration.
        denom = mu_0_grid * l_filament_total if l_filament_total > 0 else 0.0
        n_y_per_filament_length = (e_filaments_total + e_node) / denom if denom > 0 else float("nan")
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
        e_total_raw=e_total,
        e_anchor_shell=e_anchor_shell,
        e_interior=e_interior,
        e_filaments=e_filaments_total,
        e_node=e_node,
        e_bulk_residual=e_bulk_residual,
        mu_0_grid=mu_0_grid,
        mu_0_per_filament=per_filament_mu0,
        l_filament_total=l_filament_total,
        n_y_per_xi=n_y_per_xi,
        n_y_per_filament_length=n_y_per_filament_length,
        f_factor_interior=f_factor_interior,
        f_factor_raw=f_factor_raw,
        n_y_per_xi_times_f_interior=(
            n_y_per_xi * f_factor_interior if mu_0_grid > 0.0 else float("nan")
        ),
        filaments=tuple(filaments),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract N_Y / F from a saved Y-junction state.")
    parser.add_argument("state", type=Path, help="Path to .npz saved by trefoil_y_junction_static.py")
    parser.add_argument("--r-tube", type=float, default=2.0, help="Tube radius (in xi) around each filament axis")
    parser.add_argument("--r-node", type=float, default=2.0, help="Junction ball radius (in xi) around origin")
    parser.add_argument("--cal-start", type=float, default=2.5, help="Start arc-length of self-calibration slab along each filament")
    parser.add_argument("--cal-stop", type=float, default=4.5, help="Stop arc-length of self-calibration slab along each filament")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    state = load_state(args.state)
    ec = ExtractionConfig(
        r_tube=args.r_tube,
        r_node=args.r_node,
        cal_start=args.cal_start,
        cal_stop=args.cal_stop,
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

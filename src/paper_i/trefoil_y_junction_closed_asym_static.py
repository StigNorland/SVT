"""Asymmetric closed Y-junction prototype: (+1, +1, -1) phase signs.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: total energy, residual norm, depressed-volume fraction, effective radius
Primary role: asymmetric variant of the closed theta-graph Y-junction designed to
              remove the +3 winding monopole at each pole. By flipping the phase
              winding of one of the three arcs, the net winding at each Y-node
              becomes +1 instead of +3, removing the multi-quantum fission
              instability that destroyed the symmetric seed.
Key limitation: the (+1, +1, -1) pattern breaks the 3-fold rotational symmetry
                of the configuration; a reflection symmetry through the plane
                bisecting the two like-signed filaments survives.
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

from shared_numerics import (
    GridSpec,
    Nondimensionalisation,
    OutputStatus,
    RelaxationControls,
    ScriptMetadata,
    grid_step_scale,
)
from trefoil_observables import (
    deficit_volume,
    depressed_fraction,
    effective_radius,
    equivalent_deficit_radius,
    far_field_moment,
    residual_norm,
    shell_mean_deficit,
    shell_mean_density,
    total_energy,
)
from trefoil_y_junction_closed_static import arc_curve


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("total_energy", "residual_norm", "depressed_fraction", "effective_radius"),
    diagnostics=("energy_monotonicity", "residual_norm", "boundary_anchor"),
    issue_refs=("#13",),
    limitations=(
        "Uses an asymmetric (+1, +1, -1) phase-sign pattern on the closed theta-graph skeleton.",
        "Net winding at each Y-node is +1 instead of +3 to avoid the multi-quantum fission instability.",
        "3-fold rotational symmetry is broken; only a single reflection symmetry survives.",
    ),
)


@dataclass(frozen=True)
class YJunctionClosedAsymConfig:
    n: int = 48
    half_width: float = 6.0
    xi: float = 1.0
    node_radius: float = 2.5
    arc_radius: float = 2.5
    samples_per_arc: int = 200
    log_pressure: float = 0.5
    density_floor: float = 1.0e-12
    anchor_shell: int = 2
    boundary_blend_fraction: float = 0.18
    depressed_threshold: float = 0.35
    phase_signs: tuple[int, int, int] = (1, 1, -1)

    @property
    def grid(self) -> GridSpec:
        return GridSpec(n=self.n, half_width=self.half_width)


@dataclass(frozen=True)
class RunSummary:
    steps_completed: int
    final_energy: float
    best_energy: float
    energy_monotonicity_violations: int
    accepted_steps: int
    rejected_steps: int
    final_step_size: float
    residual_norm: float
    depressed_fraction: float
    effective_radius: float
    deficit_volume: float
    equivalent_deficit_radius: float
    far_field_shell_density: float
    far_field_shell_deficit: float
    far_field_moment: float
    min_density: float
    max_density: float
    initial_energy: float
    stop_reason: str


def coordinate_grid(cfg: YJunctionClosedAsymConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dx = cfg.grid.spacing
    axis = (np.arange(cfg.n) + 0.5) * dx - cfg.half_width
    return np.meshgrid(axis, axis, axis, indexing="ij")


# arc_curve is reused from trefoil_y_junction_closed_static — same skeleton.
# Bridge it through a tiny shim that constructs the symmetric config so we can
# share the same arc geometry.
class _GeomShim:
    def __init__(self, cfg: YJunctionClosedAsymConfig) -> None:
        self.arc_radius = cfg.arc_radius
        self.node_radius = cfg.node_radius
        self.samples_per_arc = cfg.samples_per_arc


def initial_state(cfg: YJunctionClosedAsymConfig) -> np.ndarray:
    """Asymmetric three-arc product-vortex ansatz.

    Same skeleton as the symmetric closed Y-junction, but each per-filament phase
    is multiplied by its sign in cfg.phase_signs before summing. The (+1, +1, -1)
    default makes the net winding at each Y-node +1 instead of +3.
    """
    x, y, z = coordinate_grid(cfg)
    points = np.stack((x, y, z), axis=-1)

    amp_total = np.ones_like(x)
    phase_total = np.zeros_like(x)
    shim = _GeomShim(cfg)

    for k in range(3):
        pos, e1, e2 = arc_curve(shim, k)

        offsets = points[None, ...] - pos[:, None, None, None, :]
        dist_sq = np.sum(offsets * offsets, axis=-1)
        nearest = np.argmin(dist_sq, axis=0)

        nearest_pos = pos[nearest]
        nearest_e1 = e1[nearest]
        nearest_e2 = e2[nearest]
        nearest_offset = points - nearest_pos

        perp_e1 = np.sum(nearest_offset * nearest_e1, axis=-1)
        perp_e2 = np.sum(nearest_offset * nearest_e2, axis=-1)
        distance = np.sqrt(np.maximum(perp_e1 * perp_e1 + perp_e2 * perp_e2, 0.0))
        theta_k = np.arctan2(perp_e2, perp_e1)

        amp_k = np.tanh(distance / (math.sqrt(2.0) * cfg.xi))
        amp_total = amp_total * amp_k
        phase_total = phase_total + cfg.phase_signs[k] * theta_k

    psi = amp_total * np.exp(1j * phase_total)
    return psi.astype(np.complex128)


def laplacian(field: np.ndarray, dx: float) -> np.ndarray:
    return (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        + np.roll(field, 1, axis=2)
        + np.roll(field, -1, axis=2)
        - 6.0 * field
    ) / (dx * dx)


def apply_boundary_anchor(
    psi: np.ndarray,
    anchor_target: np.ndarray,
    cfg: YJunctionClosedAsymConfig,
) -> None:
    shell = cfg.anchor_shell
    if shell <= 0 and cfg.boundary_blend_fraction <= 0.0:
        return

    if shell > 0:
        psi[:shell, :, :] = anchor_target[:shell, :, :]
        psi[-shell:, :, :] = anchor_target[-shell:, :, :]
        psi[:, :shell, :] = anchor_target[:, :shell, :]
        psi[:, -shell:, :] = anchor_target[:, -shell:, :]
        psi[:, :, :shell] = anchor_target[:, :, :shell]
        psi[:, :, -shell:] = anchor_target[:, :, -shell:]

    if cfg.boundary_blend_fraction <= 0.0:
        return

    x, y, z = coordinate_grid(cfg)
    radius = np.sqrt(x * x + y * y + z * z)
    r_max = math.sqrt(3.0) * cfg.half_width
    blend_start = max((1.0 - cfg.boundary_blend_fraction) * r_max, 0.0)
    blend_width = max(r_max - blend_start, 1.0e-12)
    mask = radius > blend_start
    if not np.any(mask):
        return
    alpha = np.clip((radius - blend_start) / blend_width, 0.0, 1.0)
    alpha = alpha * alpha * (3.0 - 2.0 * alpha)
    psi[mask] = (1.0 - alpha[mask]) * psi[mask] + alpha[mask] * anchor_target[mask]


def logse_gradient(psi: np.ndarray, cfg: YJunctionClosedAsymConfig) -> np.ndarray:
    rho = np.maximum(np.abs(psi) ** 2, cfg.density_floor)
    return -0.5 * laplacian(psi, cfg.grid.spacing) + cfg.log_pressure * np.log(rho) * psi


def relax(cfg: YJunctionClosedAsymConfig, controls: RelaxationControls) -> tuple[np.ndarray, RunSummary]:
    psi = initial_state(cfg)
    anchor_target = psi.copy()
    apply_boundary_anchor(psi, anchor_target, cfg)
    x, y, z = coordinate_grid(cfg)
    gradient_fn = lambda field: logse_gradient(field, cfg)

    initial_energy = total_energy(psi, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
    last_energy = initial_energy
    best_energy = last_energy
    best_psi = psi.copy()
    violations = 0
    completed = 0
    accepted_steps = 0
    rejected_steps = 0
    reference_spacing = (
        controls.reference_spacing if controls.reference_spacing is not None else (10.0 / 24.0)
    )
    step_scale = grid_step_scale(cfg.grid.spacing, reference_spacing)
    step_size = min(controls.step_size * step_scale, controls.max_step_size * step_scale)
    effective_min_step_size = controls.min_step_size * step_scale
    effective_max_step_size = controls.max_step_size * step_scale
    stale_intervals = 0
    stop_reason = "max_steps"

    for step in range(1, controls.max_steps + 1):
        gradient = logse_gradient(psi, cfg)
        candidate = psi - step_size * gradient
        apply_boundary_anchor(candidate, anchor_target, cfg)

        current_energy = total_energy(candidate, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
        if current_energy > last_energy + controls.energy_tol:
            violations += 1
            rejected_steps += 1
            step_size *= 0.5
            if step_size < effective_min_step_size:
                stop_reason = "step_size_floor"
                completed = step
                break
            continue

        psi = candidate
        accepted_steps += 1
        completed = step

        energy_improvement = last_energy - current_energy
        last_energy = current_energy
        if current_energy < best_energy:
            best_energy = current_energy
            best_psi = psi.copy()

        if energy_improvement <= controls.energy_tol:
            stale_intervals += 1
        else:
            stale_intervals = 0
            step_size = min(step_size * 1.05, effective_max_step_size)

        if accepted_steps % controls.check_interval == 0:
            current_residual = residual_norm(psi, gradient_fn)
            if current_residual <= controls.tolerance:
                stop_reason = "residual_tolerance"
                break
            if stale_intervals >= controls.patience_intervals:
                stop_reason = "energy_plateau"
                break

    psi = best_psi
    rho = np.abs(psi) ** 2
    shell_inner = 0.7 * cfg.half_width
    shell_outer = 0.95 * cfg.half_width
    summary = RunSummary(
        steps_completed=completed,
        final_energy=last_energy,
        best_energy=best_energy,
        energy_monotonicity_violations=violations,
        accepted_steps=accepted_steps,
        rejected_steps=rejected_steps,
        final_step_size=step_size,
        residual_norm=residual_norm(psi, gradient_fn),
        depressed_fraction=depressed_fraction(psi, cfg.depressed_threshold),
        effective_radius=effective_radius(psi, x, y, z),
        deficit_volume=deficit_volume(psi, cfg.grid.spacing),
        equivalent_deficit_radius=equivalent_deficit_radius(psi, cfg.grid.spacing),
        far_field_shell_density=shell_mean_density(psi, x, y, z, shell_inner, shell_outer),
        far_field_shell_deficit=shell_mean_deficit(psi, x, y, z, shell_inner, shell_outer),
        far_field_moment=far_field_moment(psi, x, y, z, shell_inner),
        min_density=float(np.min(rho)),
        max_density=float(np.max(rho)),
        initial_energy=initial_energy,
        stop_reason=stop_reason,
    )
    return psi, summary


def parse_signs(text: str) -> tuple[int, int, int]:
    parts = [int(p.strip()) for p in text.split(",") if p.strip()]
    if len(parts) != 3 or any(p not in (-1, 1) for p in parts):
        raise ValueError("phase-signs must be three comma-separated values in {-1, 1}")
    return tuple(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Static asymmetric closed-topology Y-junction prototype.")
    parser.add_argument("--n", type=int, default=48)
    parser.add_argument("--half-width", type=float, default=6.0)
    parser.add_argument("--node-radius", type=float, default=2.5)
    parser.add_argument("--arc-radius", type=float, default=2.5)
    parser.add_argument("--samples-per-arc", type=int, default=200)
    parser.add_argument("--phase-signs", type=parse_signs, default=(1, 1, -1),
                        help="Comma-separated +/- 1 per filament, e.g. '1,1,-1'")
    parser.add_argument("--log-pressure", type=float, default=0.5)
    parser.add_argument("--step-size", type=float, default=0.01)
    parser.add_argument("--max-steps", type=int, default=200)
    parser.add_argument("--tolerance", type=float, default=2.0e-3)
    parser.add_argument("--min-step-size", type=float, default=1.0e-5)
    parser.add_argument("--max-step-size", type=float, default=5.0e-2)
    parser.add_argument("--check-interval", type=int, default=10)
    parser.add_argument("--patience-intervals", type=int, default=3)
    parser.add_argument("--energy-tol", type=float, default=1.0e-9)
    parser.add_argument("--reference-spacing", type=float)
    parser.add_argument("--boundary-blend-fraction", type=float, default=0.18)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--save-state", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = YJunctionClosedAsymConfig(
        n=args.n,
        half_width=args.half_width,
        node_radius=args.node_radius,
        arc_radius=args.arc_radius,
        samples_per_arc=args.samples_per_arc,
        phase_signs=args.phase_signs,
        log_pressure=args.log_pressure,
        boundary_blend_fraction=args.boundary_blend_fraction,
    )
    controls = RelaxationControls(
        step_size=args.step_size,
        max_steps=args.max_steps,
        tolerance=args.tolerance,
        min_step_size=args.min_step_size,
        max_step_size=args.max_step_size,
        check_interval=args.check_interval,
        patience_intervals=args.patience_intervals,
        energy_tol=args.energy_tol,
        reference_spacing=args.reference_spacing,
    )
    psi, summary = relax(cfg, controls)

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
        "nondimensionalisation": asdict(Nondimensionalisation()),
        "config": asdict(cfg),
        "controls": asdict(controls),
        "summary": asdict(summary),
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    if args.save_state:
        args.save_state.parent.mkdir(parents=True, exist_ok=True)
        x, y, z = coordinate_grid(cfg)
        np.savez_compressed(
            args.save_state,
            psi_real=psi.real,
            psi_imag=psi.imag,
            x=x,
            y=y,
            z=z,
            config=json.dumps(asdict(cfg)),
            controls=json.dumps(asdict(controls)),
            summary=json.dumps(asdict(summary)),
        )
    print(text)


if __name__ == "__main__":
    main()

"""Static open 3-prong Y-junction prototype for the Paper I N_Y / F closure track.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: total energy, residual norm, depressed-volume fraction, effective radius
Primary role: first concrete 3D realisation of three vortex filaments meeting at a
              central node (open three-prong Y, 120 deg apart in the equatorial plane).
              This is the geometry on which N_Y and F are defined in Paper I.
Key limitation: this is an open three-prong Y, not yet the closed topologically-protected
                trefoil knot.  N_Y / F extraction is deferred to a follow-up script.
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


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("total_energy", "residual_norm", "depressed_fraction", "effective_radius"),
    diagnostics=("energy_monotonicity", "residual_norm", "boundary_anchor"),
    issue_refs=("#13",),
    limitations=(
        "Uses an open three-prong Y geometry rather than a closed trefoil knot.",
        "Phase pattern uses the canonical product-vortex ansatz; the 120 deg balance at the node emerges from geometry, with no extra color offset.",
        "N_Y / F extraction is not implemented in this script; it only produces the relaxed Y-junction field.",
    ),
)


@dataclass(frozen=True)
class YJunctionConfig:
    n: int = 48
    half_width: float = 6.0
    xi: float = 1.0
    junction_smoothing: float = 0.0
    log_pressure: float = 0.5
    density_floor: float = 1.0e-12
    anchor_shell: int = 2
    boundary_blend_fraction: float = 0.18
    depressed_threshold: float = 0.35

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


def coordinate_grid(cfg: YJunctionConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dx = cfg.grid.spacing
    axis = (np.arange(cfg.n) + 0.5) * dx - cfg.half_width
    return np.meshgrid(axis, axis, axis, indexing="ij")


def y_junction_frame() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Three filament unit vectors and a transverse (e1, e2) pair per filament.

    Filaments lie in the equatorial plane at 0, 120, 240 degrees.  The out-of-plane
    direction e2 = z-hat is perpendicular to all three, so a single azimuthal-angle
    convention works uniformly across the junction region.
    """
    angles = np.array([0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0])
    dirs = np.stack([np.cos(angles), np.sin(angles), np.zeros_like(angles)], axis=1)
    z_hat = np.array([0.0, 0.0, 1.0])
    e1 = np.cross(dirs, z_hat)
    e1 = e1 / np.linalg.norm(e1, axis=1, keepdims=True)
    e2 = np.tile(z_hat, (3, 1))
    return dirs, e1, e2


def initial_state(cfg: YJunctionConfig) -> np.ndarray:
    """Open three-prong Y-junction product-vortex ansatz.

    For each filament k:
      s_k       = signed arc-length along filament direction d_k
      perp_k    = transverse displacement from the filament axis
      d_eff_k   = sqrt(perp_k^2 + max(0, -s_k)^2)  treats filament as a half-line
      theta_k   = arctan2(perp_k . e2_k, perp_k . e1_k)
      amp_k     = tanh(d_eff_k / (sqrt(2) xi))

    The product-vortex ansatz combines them as

      psi(x) = prod_k amp_k(x) * exp(i * sum_k theta_k(x)).

    This places unit vortex winding around each filament axis, gives |psi| = 0 on any
    filament line (and at the central node by construction), and reaches |psi| -> 1 in
    the bulk far from any filament.  The 120 deg balance at the node is a geometric
    consequence of the three filament directions; no explicit phase offset is added.
    """
    x, y, z = coordinate_grid(cfg)
    points = np.stack((x, y, z), axis=-1)
    dirs, e1, e2 = y_junction_frame()

    s = np.einsum("ijkl,ml->mijk", points, dirs)
    perp = points[None, ...] - s[..., None] * dirs[:, None, None, None, :]
    d = np.sqrt(np.sum(perp * perp, axis=-1))
    d_eff = np.sqrt(d * d + np.maximum(-s, 0.0) ** 2)

    perp_e1 = np.einsum("mijkl,ml->mijk", perp, e1)
    perp_e2 = np.einsum("mijkl,ml->mijk", perp, e2)
    theta = np.arctan2(perp_e2, perp_e1)

    amp_k = np.tanh(d_eff / (math.sqrt(2.0) * cfg.xi))
    amp_total = np.prod(amp_k, axis=0)
    phase_total = np.sum(theta, axis=0)

    if cfg.junction_smoothing > 0.0:
        r2 = x * x + y * y + z * z
        damp = 1.0 - np.exp(-r2 / max(cfg.junction_smoothing**2, 1.0e-12))
        amp_total = amp_total * damp

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
    cfg: YJunctionConfig,
) -> None:
    """Pin / blend the outer shells to anchor_target.

    For an open three-prong Y the filament endpoints reach the box boundary, so
    anchoring to a uniform background would let the filaments retract and the
    topology dissolve.  Instead we anchor to the initial state, which preserves
    the filament endpoints and represents the filaments as continuing into the
    surrounding bulk beyond the simulation box.
    """
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


def logse_gradient(psi: np.ndarray, cfg: YJunctionConfig) -> np.ndarray:
    rho = np.maximum(np.abs(psi) ** 2, cfg.density_floor)
    return -0.5 * laplacian(psi, cfg.grid.spacing) + cfg.log_pressure * np.log(rho) * psi


def relax(cfg: YJunctionConfig, controls: RelaxationControls) -> tuple[np.ndarray, RunSummary]:
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Static open 3-prong Y-junction prototype relaxer.")
    parser.add_argument("--n", type=int, default=48)
    parser.add_argument("--half-width", type=float, default=6.0)
    parser.add_argument("--junction-smoothing", type=float, default=0.0)
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
    cfg = YJunctionConfig(
        n=args.n,
        half_width=args.half_width,
        junction_smoothing=args.junction_smoothing,
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

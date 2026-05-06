"""Static trefoil-breather prototype for the Paper I closure track.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: total energy, residual norm, depressed-volume fraction, effective radius
Primary role: first concrete implementation step for issue #13
Key limitation: this is a single-filament trefoil prototype with a simple LogSE gradient flow,
not yet the full 3D trefoil Y-junction closure solver described in Paper I.
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

from shared_numerics import GridSpec, Nondimensionalisation, OutputStatus, RelaxationControls, ScriptMetadata
from trefoil_observables import (
    depressed_fraction,
    effective_radius,
    far_field_moment,
    residual_norm,
    shell_mean_deficit,
    shell_mean_density,
    total_energy,
)


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("total_energy", "residual_norm", "depressed_fraction", "effective_radius"),
    diagnostics=("energy_monotonicity", "residual_norm", "boundary_anchor"),
    issue_refs=("#13",),
    limitations=(
        "Uses a single trefoil-filament background rather than a full trefoil Y-junction skeleton.",
        "Uses a simple LogSE gradient flow without the full coupled L + L_perp production treatment.",
    ),
)


@dataclass(frozen=True)
class TrefoilConfig:
    n: int = 48
    half_width: float = 6.0
    xi: float = 1.0
    major_radius: float = 2.8
    minor_radius: float = 0.85
    smoothing_radius: float = 0.2
    log_pressure: float = 0.5
    density_floor: float = 1.0e-12
    anchor_shell: int = 2
    depressed_threshold: float = 0.35
    frame_samples: int = 600

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
    far_field_shell_density: float
    far_field_shell_deficit: float
    far_field_moment: float
    min_density: float
    max_density: float
    stop_reason: str


def coordinate_grid(cfg: TrefoilConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dx = cfg.grid.spacing
    axis = (np.arange(cfg.n) + 0.5) * dx - cfg.half_width
    return np.meshgrid(axis, axis, axis, indexing="ij")


def normalize(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    if norm < 1.0e-12:
        return np.array([1.0, 0.0, 0.0], dtype=float)
    return vec / norm


def trefoil_curve(samples: int, major_radius: float, minor_radius: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    t = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    x = (major_radius + minor_radius * np.cos(3.0 * t)) * np.cos(2.0 * t)
    y = (major_radius + minor_radius * np.cos(3.0 * t)) * np.sin(2.0 * t)
    z = minor_radius * np.sin(3.0 * t)
    curve = np.stack((x, y, z), axis=1)

    dt = 2.0 * math.pi / samples
    tangent = np.gradient(curve, dt, axis=0, edge_order=2)
    tangent = tangent / np.linalg.norm(tangent, axis=1, keepdims=True)

    radial_hint = np.stack((np.cos(2.0 * t), np.sin(2.0 * t), np.zeros_like(t)), axis=1)
    normal = radial_hint - np.sum(radial_hint * tangent, axis=1, keepdims=True) * tangent
    normal = np.array([normalize(v) for v in normal])
    binormal = np.cross(tangent, normal)
    binormal = np.array([normalize(v) for v in binormal])
    return curve, tangent, normal, binormal


def initial_state(cfg: TrefoilConfig) -> np.ndarray:
    x, y, z = coordinate_grid(cfg)
    points = np.stack((x, y, z), axis=-1)
    curve, _tangent, normal, binormal = trefoil_curve(
        cfg.frame_samples,
        major_radius=cfg.major_radius,
        minor_radius=cfg.minor_radius,
    )

    offsets = points[None, ...] - curve[:, None, None, None, :]
    dist_sq = np.sum(offsets * offsets, axis=-1)
    nearest = np.argmin(dist_sq, axis=0)

    nearest_curve = curve[nearest]
    nearest_normal = normal[nearest]
    nearest_binormal = binormal[nearest]
    nearest_offset = points - nearest_curve

    radial_n = np.sum(nearest_offset * nearest_normal, axis=-1)
    radial_b = np.sum(nearest_offset * nearest_binormal, axis=-1)
    distance = np.sqrt(np.maximum(radial_n * radial_n + radial_b * radial_b, 0.0))
    theta = np.arctan2(radial_b, radial_n)

    amplitude = np.tanh(distance / (math.sqrt(2.0) * cfg.xi))
    phase = np.exp(1j * theta)

    # Localised central depression acts as a first breather-like seed.
    radius_sq = x * x + y * y + z * z
    seed = 1.0 - 0.25 * np.exp(-radius_sq / max(cfg.smoothing_radius**2, 1.0e-12))
    psi = amplitude * phase * seed
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


def apply_boundary_anchor(psi: np.ndarray, cfg: TrefoilConfig) -> None:
    shell = cfg.anchor_shell
    if shell <= 0:
        return
    psi[:shell, :, :] = 1.0 + 0.0j
    psi[-shell:, :, :] = 1.0 + 0.0j
    psi[:, :shell, :] = 1.0 + 0.0j
    psi[:, -shell:, :] = 1.0 + 0.0j
    psi[:, :, :shell] = 1.0 + 0.0j
    psi[:, :, -shell:] = 1.0 + 0.0j


def logse_gradient(psi: np.ndarray, cfg: TrefoilConfig) -> np.ndarray:
    rho = np.maximum(np.abs(psi) ** 2, cfg.density_floor)
    return -0.5 * laplacian(psi, cfg.grid.spacing) + cfg.log_pressure * np.log(rho) * psi


def relax(
    cfg: TrefoilConfig,
    controls: RelaxationControls,
) -> tuple[np.ndarray, RunSummary]:
    psi = initial_state(cfg)
    apply_boundary_anchor(psi, cfg)
    x, y, z = coordinate_grid(cfg)
    gradient_fn = lambda field: logse_gradient(field, cfg)

    last_energy = total_energy(psi, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
    best_energy = last_energy
    best_psi = psi.copy()
    violations = 0
    completed = 0
    accepted_steps = 0
    rejected_steps = 0
    step_size = controls.step_size
    stale_intervals = 0
    stop_reason = "max_steps"

    for step in range(1, controls.max_steps + 1):
        gradient = logse_gradient(psi, cfg)
        candidate = psi - step_size * gradient
        apply_boundary_anchor(candidate, cfg)

        current_energy = total_energy(candidate, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
        if current_energy > last_energy + controls.energy_tol:
            violations += 1
            rejected_steps += 1
            step_size *= 0.5
            if step_size < controls.min_step_size:
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
            step_size = min(step_size * 1.05, controls.max_step_size)

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
        far_field_shell_density=shell_mean_density(psi, x, y, z, shell_inner, shell_outer),
        far_field_shell_deficit=shell_mean_deficit(psi, x, y, z, shell_inner, shell_outer),
        far_field_moment=far_field_moment(psi, x, y, z, shell_inner),
        min_density=float(np.min(rho)),
        max_density=float(np.max(rho)),
        stop_reason=stop_reason,
    )
    return psi, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Static trefoil-breather prototype relaxer.")
    parser.add_argument("--n", type=int, default=48)
    parser.add_argument("--half-width", type=float, default=6.0)
    parser.add_argument("--major-radius", type=float, default=2.8)
    parser.add_argument("--minor-radius", type=float, default=0.85)
    parser.add_argument("--smoothing-radius", type=float, default=0.2)
    parser.add_argument("--log-pressure", type=float, default=0.5)
    parser.add_argument("--step-size", type=float, default=0.01)
    parser.add_argument("--max-steps", type=int, default=200)
    parser.add_argument("--tolerance", type=float, default=2.0e-3)
    parser.add_argument("--min-step-size", type=float, default=1.0e-5)
    parser.add_argument("--max-step-size", type=float, default=5.0e-2)
    parser.add_argument("--check-interval", type=int, default=10)
    parser.add_argument("--patience-intervals", type=int, default=3)
    parser.add_argument("--energy-tol", type=float, default=1.0e-9)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--save-state", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = TrefoilConfig(
        n=args.n,
        half_width=args.half_width,
        major_radius=args.major_radius,
        minor_radius=args.minor_radius,
        smoothing_radius=args.smoothing_radius,
        log_pressure=args.log_pressure,
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

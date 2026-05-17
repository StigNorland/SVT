"""Asymmetric closed Y-junction with the L_perp chiral non-local shear term.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: total energy (LogSE + L_perp), residual norm, depressed_fraction
Primary role: first implementation of the L + L_perp functional from Paper I, on
              top of the existing asymmetric (+1, +1, -1) closed Y-junction
              relaxation.  Tests whether the chiral non-local shear term changes
              core stability or bulk structure relative to the L-only run.
Key limitation: L_perp involves 5th-order spatial derivatives, so the explicit
                gradient flow is stiff.  The paper's quoted lambda = 2000 is
                likely too large for stable explicit Euler at dx = 0.5; this
                script accepts lambda as a CLI parameter for ramping.

Paper I, eq. chiral:

    L_perp = -(lambda hbar^2)/(2 m_0 rho_0^2) |curl j|^2,
    j = (hbar / 2 m_0 i)(psi^* grad psi - psi grad psi^*) = Im(psi^* grad psi).

In dimensionless units (hbar = m_0 = rho_0 = 1), the static energy
contribution is

    E_perp = (lambda / 2) integral |curl j|^2 d^3 x,

and the Wirtinger derivative is

    delta E_perp / delta psi^* = -i lambda (curl omega) . grad psi,

with omega = curl j.  This combines additively with the LogSE gradient in
the gradient-descent relaxation loop.
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
from trefoil_y_junction_closed_asym_static import (
    YJunctionClosedAsymConfig,
    apply_boundary_anchor,
    coordinate_grid,
    initial_state,
    laplacian,
    logse_gradient,
)


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("total_energy_full", "e_logse", "e_perp", "residual_norm", "depressed_fraction"),
    diagnostics=("energy_monotonicity", "residual_norm", "boundary_anchor", "lperp_step_constraint"),
    issue_refs=("#13",),
    limitations=(
        "Explicit Euler gradient flow is stiff at large lambda (5th-order operator). The paper's quoted lambda = 2000 may need a much finer grid or an implicit scheme.",
        "Only the asymmetric closed Y skeleton is supported; topology choice is inherited from trefoil_y_junction_closed_asym_static.",
    ),
)


@dataclass(frozen=True)
class LperpControls:
    lambda_perp: float


def _grad_psi(psi: np.ndarray, dx: float) -> np.ndarray:
    out = np.empty((3,) + psi.shape, dtype=psi.dtype)
    for ax in range(3):
        out[ax] = (np.roll(psi, -1, axis=ax) - np.roll(psi, 1, axis=ax)) / (2.0 * dx)
    return out


def _current(psi: np.ndarray, dx: float) -> np.ndarray:
    gp = _grad_psi(psi, dx)
    return np.imag(np.conj(psi)[None, ...] * gp)


def _curl(v: np.ndarray, dx: float) -> np.ndarray:
    # v has shape (3, n, n, n).  (curl v)_x = dy v_z - dz v_y, etc.
    dy_vz = (np.roll(v[2], -1, axis=1) - np.roll(v[2], 1, axis=1)) / (2.0 * dx)
    dz_vy = (np.roll(v[1], -1, axis=2) - np.roll(v[1], 1, axis=2)) / (2.0 * dx)
    dz_vx = (np.roll(v[0], -1, axis=2) - np.roll(v[0], 1, axis=2)) / (2.0 * dx)
    dx_vz = (np.roll(v[2], -1, axis=0) - np.roll(v[2], 1, axis=0)) / (2.0 * dx)
    dx_vy = (np.roll(v[1], -1, axis=0) - np.roll(v[1], 1, axis=0)) / (2.0 * dx)
    dy_vx = (np.roll(v[0], -1, axis=1) - np.roll(v[0], 1, axis=1)) / (2.0 * dx)
    return np.stack((dy_vz - dz_vy, dz_vx - dx_vz, dx_vy - dy_vx), axis=0)


def lperp_energy(psi: np.ndarray, dx: float, lambda_perp: float) -> float:
    if lambda_perp == 0.0:
        return 0.0
    j = _current(psi, dx)
    omega = _curl(j, dx)
    return 0.5 * lambda_perp * float(np.sum(omega * omega)) * (dx**3)


def lperp_gradient(psi: np.ndarray, dx: float, lambda_perp: float) -> np.ndarray:
    if lambda_perp == 0.0:
        return np.zeros_like(psi)
    j = _current(psi, dx)
    omega = _curl(j, dx)
    curl_omega = _curl(omega, dx)
    gp = _grad_psi(psi, dx)
    contraction = np.sum(curl_omega * gp, axis=0)  # complex (n,n,n)
    return -1j * lambda_perp * contraction


def full_energy(psi: np.ndarray, cfg: YJunctionClosedAsymConfig, lambda_perp: float) -> tuple[float, float, float]:
    e_log = total_energy(psi, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
    e_perp = lperp_energy(psi, cfg.grid.spacing, lambda_perp)
    return e_log + e_perp, e_log, e_perp


def full_gradient(psi: np.ndarray, cfg: YJunctionClosedAsymConfig, lambda_perp: float) -> np.ndarray:
    g_log = logse_gradient(psi, cfg)
    g_perp = lperp_gradient(psi, cfg.grid.spacing, lambda_perp)
    return g_log + g_perp


@dataclass(frozen=True)
class RunSummary:
    steps_completed: int
    lambda_perp: float
    final_energy_full: float
    final_energy_logse: float
    final_energy_perp: float
    initial_energy_full: float
    initial_energy_logse: float
    initial_energy_perp: float
    best_energy_full: float
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
    min_density: float
    max_density: float
    stop_reason: str


def relax(
    cfg: YJunctionClosedAsymConfig,
    controls: RelaxationControls,
    lperp: LperpControls,
) -> tuple[np.ndarray, RunSummary]:
    psi = initial_state(cfg)
    anchor_target = psi.copy()
    apply_boundary_anchor(psi, anchor_target, cfg)
    x, y, z = coordinate_grid(cfg)

    initial_full, initial_log, initial_perp = full_energy(psi, cfg, lperp.lambda_perp)
    last_energy = initial_full
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

    gradient_fn = lambda field: full_gradient(field, cfg, lperp.lambda_perp)

    for step in range(1, controls.max_steps + 1):
        gradient = full_gradient(psi, cfg, lperp.lambda_perp)
        candidate = psi - step_size * gradient
        apply_boundary_anchor(candidate, anchor_target, cfg)

        current_energy, _e_log, _e_perp = full_energy(candidate, cfg, lperp.lambda_perp)
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
    final_full, final_log, final_perp = full_energy(psi, cfg, lperp.lambda_perp)
    summary = RunSummary(
        steps_completed=completed,
        lambda_perp=lperp.lambda_perp,
        final_energy_full=final_full,
        final_energy_logse=final_log,
        final_energy_perp=final_perp,
        initial_energy_full=initial_full,
        initial_energy_logse=initial_log,
        initial_energy_perp=initial_perp,
        best_energy_full=best_energy,
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
        min_density=float(np.min(rho)),
        max_density=float(np.max(rho)),
        stop_reason=stop_reason,
    )
    return psi, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Static asym closed Y-junction with L_perp chiral shear term.")
    parser.add_argument("--n", type=int, default=24)
    parser.add_argument("--half-width", type=float, default=6.0)
    parser.add_argument("--node-radius", type=float, default=2.5)
    parser.add_argument("--arc-radius", type=float, default=2.5)
    parser.add_argument("--samples-per-arc", type=int, default=200)
    parser.add_argument("--log-pressure", type=float, default=0.5)
    parser.add_argument("--lambda-perp", type=float, default=10.0, help="L_perp coupling (paper quotes 2000)")
    parser.add_argument("--step-size", type=float, default=0.005)
    parser.add_argument("--max-steps", type=int, default=200)
    parser.add_argument("--tolerance", type=float, default=2.0e-3)
    parser.add_argument("--min-step-size", type=float, default=1.0e-8)
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
    lperp = LperpControls(lambda_perp=args.lambda_perp)
    psi, summary = relax(cfg, controls, lperp)

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
        "lperp": asdict(lperp),
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
            lperp=json.dumps(asdict(lperp)),
            summary=json.dumps(asdict(summary)),
        )
    print(text)


if __name__ == "__main__":
    main()

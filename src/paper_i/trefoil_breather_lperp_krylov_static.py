"""(2,3)-trefoil knot with L_perp via Krylov (matrix-free GMRES) implicit step.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: total energy (LogSE + L_perp), residual norm, min_density, gmres_iter
Primary role: replace the FFT semi-implicit step (which over-smooths cores via
              its diagonal-in-Fourier Jacobian approximation) with a true-Jacobian
              matrix-free GMRES solve.  Tests whether the stabilised trefoil's
              cores deepen with the better implicit operator.
Key limitation: Jacobian action computed by finite differencing (eps tuning).
                Cost per step is roughly (gmres_iter + 1) times explicit step.
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
from trefoil_breather_static import (
    TrefoilConfig,
    apply_boundary_anchor,
    coordinate_grid,
    initial_state,
    logse_gradient,
)
from lperp_helpers import lperp_energy, lperp_gradient
from lperp_krylov_helpers import krylov_implicit_step
from topology_helpers import count_vortex_links


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=(
        "total_energy_full",
        "e_logse",
        "e_perp",
        "residual_norm",
        "depressed_fraction",
        "min_density",
    ),
    diagnostics=(
        "energy_monotonicity",
        "residual_norm",
        "boundary_anchor",
        "gmres_iter",
        "gmres_relres",
        "vortex_links",
    ),
    issue_refs=("#13",),
    limitations=(
        "Jacobian action by finite differencing of g_full; eps choice affects accuracy.",
        "FFT preconditioner (k^2 + lambda*k^4) assumes periodic BC; boundary anchor applied afterwards.",
        "Tied to the (2,3)-trefoil-knot initial condition.",
        "mean_gmres_iter reports total iterations across all restart cycles, not per-cycle.",
        "Lattice plaquette vortex link counting (initial/final_vortex_links) is reliable "
        "at the production grid; final_vortex_links=0 in any run indicates topology has "
        "been destroyed by the solver (the min_rho proxy is unreliable, see "
        "winding-number-checkpoint.md). Krylov steps destroy ~20% of vortex links per step; "
        "rejection-based guards cannot prevent this. The winding guard is disabled by default "
        "(winding_drop_tol=-1); enabling it stalls the solver after 2-5 accepted steps. "
        "Topology enforcement requires a penalty term, projected gradient, or constrained method.",
    ),
)


@dataclass(frozen=True)
class LperpControls:
    lambda_perp: float
    gmres_tol: float = 1.0e-4
    gmres_restart: int = 30
    gmres_max_cycles: int = 1  # >1 cycles dissolve vortex topology (see gmres-tuning-final-summary.md)
    kinetic_coeff: float = 0.0        # k^4 only is topology-safe; k^2+k^4 erodes topology
    min_rho_threshold: float = 0.5   # legacy min_rho guard (inactive when min_rho_drift_tol < 0)
    min_rho_drift_tol: float = -1.0  # set >= 0 to enable legacy min_rho guard; replaced by winding guard
    min_rho_warmup: int = 150
    winding_drop_tol: float = -1.0   # disabled: GMRES destroys topology in <5 steps regardless of tol (see winding-number-checkpoint.md)
    winding_warmup: int = 0          # winding guard activates from step 1 (when enabled); initial state has clean 2pi windings


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
    topology_violations: int
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
    mean_gmres_iter: float
    max_gmres_iter: int
    initial_vortex_links: int
    final_vortex_links: int
    stop_reason: str


def full_energy(psi: np.ndarray, cfg: TrefoilConfig, lambda_perp: float) -> tuple[float, float, float]:
    e_log = total_energy(psi, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
    e_perp = lperp_energy(psi, cfg.grid.spacing, lambda_perp)
    return e_log + e_perp, e_log, e_perp


def full_gradient(psi: np.ndarray, cfg: TrefoilConfig, lambda_perp: float) -> np.ndarray:
    g_log = logse_gradient(psi, cfg)
    g_perp = lperp_gradient(psi, cfg.grid.spacing, lambda_perp)
    return g_log + g_perp


def relax(
    cfg: TrefoilConfig,
    controls: RelaxationControls,
    lperp: LperpControls,
) -> tuple[np.ndarray, RunSummary]:
    psi = initial_state(cfg)
    apply_boundary_anchor(psi, cfg)
    x, y, z = coordinate_grid(cfg)

    dx = cfg.grid.spacing

    initial_full, initial_log, initial_perp = full_energy(psi, cfg, lperp.lambda_perp)
    last_energy = initial_full
    best_energy = last_energy
    best_psi = psi.copy()
    violations = 0
    topology_violations = 0
    completed = 0
    accepted_steps = 0
    rejected_steps = 0
    best_min_rho = float("inf")  # deepest core seen across all accepted steps
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
    g_full_for_krylov = lambda field: full_gradient(field, cfg, lperp.lambda_perp)

    gmres_iters: list[int] = []
    initial_links = count_vortex_links(psi)

    for step in range(1, controls.max_steps + 1):
        candidate, n_iter, _relres = krylov_implicit_step(
            psi,
            g_full_for_krylov,
            dt=step_size,
            lambda_perp=lperp.lambda_perp,
            dx=dx,
            gmres_tol=lperp.gmres_tol,
            gmres_restart=lperp.gmres_restart,
            gmres_max_cycles=lperp.gmres_max_cycles,
            kinetic_coeff=lperp.kinetic_coeff,
        )
        apply_boundary_anchor(candidate, cfg)

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

        # Legacy min_rho guard (disabled by default; see gmres-tuning-final-summary.md).
        candidate_min_rho = float(np.min(np.abs(candidate) ** 2))
        if (
            accepted_steps >= lperp.min_rho_warmup
            and lperp.min_rho_threshold > 0.0
            and best_min_rho < lperp.min_rho_threshold
            and lperp.min_rho_drift_tol >= 0.0
            and candidate_min_rho > best_min_rho * (1.0 + lperp.min_rho_drift_tol)
        ):
            topology_violations += 1
            rejected_steps += 1
            continue

        # Winding-number guard: reject steps that reduce total vortex line length
        # by more than winding_drop_tol relative to the INITIAL trefoil topology.
        # The initial condition has clean 2pi phase windings (links=initial_links).
        # The relaxation tends to destroy these windings; the guard enforces a floor
        # on links to keep the field in the topological sector.
        candidate_links = (
            count_vortex_links(candidate) if lperp.winding_drop_tol >= 0.0 else 0
        )
        if (
            lperp.winding_drop_tol >= 0.0
            and accepted_steps >= lperp.winding_warmup
            and candidate_links < initial_links * (1.0 - lperp.winding_drop_tol)
        ):
            topology_violations += 1
            rejected_steps += 1
            continue

        gmres_iters.append(n_iter)
        psi = candidate
        accepted_steps += 1
        completed = step
        best_min_rho = min(best_min_rho, candidate_min_rho)

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
        topology_violations=topology_violations,
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
        mean_gmres_iter=float(np.mean(gmres_iters)) if gmres_iters else 0.0,
        max_gmres_iter=int(max(gmres_iters)) if gmres_iters else 0,
        initial_vortex_links=initial_links,
        final_vortex_links=count_vortex_links(psi),
        stop_reason=stop_reason,
    )
    return psi, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="(2,3)-trefoil + L_perp via Krylov-implicit GMRES stepping.")
    parser.add_argument("--n", type=int, default=24)
    parser.add_argument("--half-width", type=float, default=6.0)
    parser.add_argument("--major-radius", type=float, default=2.8)
    parser.add_argument("--minor-radius", type=float, default=0.85)
    parser.add_argument("--smoothing-radius", type=float, default=0.2)
    parser.add_argument("--log-pressure", type=float, default=0.5)
    parser.add_argument("--lambda-perp", type=float, default=2000.0)
    parser.add_argument("--gmres-tol", type=float, default=1.0e-4)
    parser.add_argument("--gmres-restart", type=int, default=30)
    parser.add_argument("--gmres-max-cycles", type=int, default=1)
    parser.add_argument("--kinetic-coeff", type=float, default=0.0)
    parser.add_argument("--min-rho-threshold", type=float, default=0.5)
    parser.add_argument("--min-rho-drift-tol", type=float, default=-1.0)
    parser.add_argument("--min-rho-warmup", type=int, default=150)
    parser.add_argument("--winding-drop-tol", type=float, default=-1.0)
    parser.add_argument("--winding-warmup", type=int, default=0)
    parser.add_argument("--step-size", type=float, default=0.005)
    parser.add_argument("--max-steps", type=int, default=200)
    parser.add_argument("--tolerance", type=float, default=2.0e-3)
    parser.add_argument("--min-step-size", type=float, default=1.0e-9)
    parser.add_argument("--max-step-size", type=float, default=5.0e-2)
    parser.add_argument("--check-interval", type=int, default=20)
    parser.add_argument("--patience-intervals", type=int, default=3)
    parser.add_argument("--energy-tol", type=float, default=1.0e-9)
    parser.add_argument("--reference-spacing", type=float)
    parser.add_argument("--boundary-blend-fraction", type=float, default=0.18)
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
    lperp = LperpControls(
        lambda_perp=args.lambda_perp,
        gmres_tol=args.gmres_tol,
        gmres_restart=args.gmres_restart,
        gmres_max_cycles=args.gmres_max_cycles,
        kinetic_coeff=args.kinetic_coeff,
        min_rho_threshold=args.min_rho_threshold,
        min_rho_drift_tol=args.min_rho_drift_tol,
        min_rho_warmup=args.min_rho_warmup,
        winding_drop_tol=args.winding_drop_tol,
        winding_warmup=args.winding_warmup,
    )
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

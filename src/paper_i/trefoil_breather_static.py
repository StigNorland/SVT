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

from shared_numerics import GridSpec, Nondimensionalisation, OutputStatus, RelaxationControls, ScriptMetadata, grid_step_scale
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
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("total_energy", "residual_norm", "depressed_fraction", "effective_radius"),
    diagnostics=("energy_monotonicity", "residual_norm", "boundary_anchor", "topology_winding_retention"),
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
    boundary_blend_fraction: float = 0.18
    depressed_threshold: float = 0.35
    frame_samples: int = 600

    @property
    def grid(self) -> GridSpec:
        return GridSpec(n=self.n, half_width=self.half_width)


@dataclass(frozen=True)
class RunSummary:
    continued_from_steps: int
    steps_completed: int
    total_steps_effective: int
    initial_l2_norm: float
    final_l2_norm: float
    l2_norm_relative_drift: float
    final_energy: float
    best_energy: float
    energy_monotonicity_violations: int
    accepted_steps: int
    rejected_steps: int
    max_backtracks_used: int
    final_step_size: float
    residual_norm: float
    projected_residual_norm: float
    depressed_fraction: float
    effective_radius: float
    deficit_volume: float
    equivalent_deficit_radius: float
    far_field_shell_density: float
    far_field_shell_deficit: float
    far_field_moment: float
    topology_loop_radius: float
    topology_mean_winding: float
    topology_winding_std: float
    topology_min_winding: float
    topology_max_winding: float
    topology_unit_fraction: float
    topology_alignment_score: float
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


def interpolate_complex_field(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    points: np.ndarray,
) -> np.ndarray:
    """Trilinearly interpolate the complex field at arbitrary Cartesian points."""
    dx = cfg.grid.spacing
    axis_min = -cfg.half_width + 0.5 * dx
    points = np.asarray(points, dtype=float)

    ux = np.clip((points[:, 0] - axis_min) / dx, 0.0, cfg.n - 1.0)
    uy = np.clip((points[:, 1] - axis_min) / dx, 0.0, cfg.n - 1.0)
    uz = np.clip((points[:, 2] - axis_min) / dx, 0.0, cfg.n - 1.0)

    ix0 = np.clip(np.floor(ux).astype(int), 0, cfg.n - 2)
    iy0 = np.clip(np.floor(uy).astype(int), 0, cfg.n - 2)
    iz0 = np.clip(np.floor(uz).astype(int), 0, cfg.n - 2)
    ix1 = ix0 + 1
    iy1 = iy0 + 1
    iz1 = iz0 + 1

    tx = ux - ix0
    ty = uy - iy0
    tz = uz - iz0

    c000 = psi[ix0, iy0, iz0]
    c100 = psi[ix1, iy0, iz0]
    c010 = psi[ix0, iy1, iz0]
    c110 = psi[ix1, iy1, iz0]
    c001 = psi[ix0, iy0, iz1]
    c101 = psi[ix1, iy0, iz1]
    c011 = psi[ix0, iy1, iz1]
    c111 = psi[ix1, iy1, iz1]

    c00 = (1.0 - tx) * c000 + tx * c100
    c10 = (1.0 - tx) * c010 + tx * c110
    c01 = (1.0 - tx) * c001 + tx * c101
    c11 = (1.0 - tx) * c011 + tx * c111
    c0 = (1.0 - ty) * c00 + ty * c10
    c1 = (1.0 - ty) * c01 + ty * c11
    return (1.0 - tz) * c0 + tz * c1


def branch_winding_diagnostics(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    sample_count: int = 12,
    loop_points: int = 64,
) -> dict[str, float]:
    """Measure whether the relaxed field still carries unit winding around the trefoil filament.

    This is a local topology-facing diagnostic rather than a full knot invariant:
    the seeded proton proxy should keep unit circulation around the branch centerline
    if the relaxation preserves the intended filament identity.
    """
    curve, _tangent, normal, binormal = trefoil_curve(
        cfg.frame_samples,
        major_radius=cfg.major_radius,
        minor_radius=cfg.minor_radius,
    )
    sample_indices = np.linspace(0, cfg.frame_samples - 1, sample_count, endpoint=False, dtype=int)
    loop_radius = max(2.0 * cfg.grid.spacing, 0.75 * cfg.xi)
    phis = np.linspace(0.0, 2.0 * math.pi, loop_points, endpoint=False)

    windings: list[float] = []
    for idx in sample_indices:
        center = curve[idx]
        loop = (
            center[None, :]
            + loop_radius * np.cos(phis)[:, None] * normal[idx][None, :]
            + loop_radius * np.sin(phis)[:, None] * binormal[idx][None, :]
        )
        samples = interpolate_complex_field(psi, cfg, loop)
        closed_angles = np.unwrap(np.angle(np.concatenate((samples, samples[:1]))))
        windings.append(float((closed_angles[-1] - closed_angles[0]) / (2.0 * math.pi)))

    winding_array = np.asarray(windings, dtype=float)
    unit_fraction = float(np.mean(np.abs(winding_array - 1.0) <= 0.25))
    alignment_score = float(np.mean(np.clip(1.0 - np.abs(winding_array - 1.0), 0.0, 1.0)))
    return {
        "loop_radius": float(loop_radius),
        "mean_winding": float(np.mean(winding_array)),
        "winding_std": float(np.std(winding_array)),
        "min_winding": float(np.min(winding_array)),
        "max_winding": float(np.max(winding_array)),
        "unit_fraction": unit_fraction,
        "alignment_score": alignment_score,
    }


def loop_circulation_geometry(
    cfg: TrefoilConfig,
    sample_count: int = 12,
    loop_points: int = 64,
) -> tuple[np.ndarray, float]:
    """Construct sampling loops around the seeded trefoil centerline."""
    curve, _tangent, normal, binormal = trefoil_curve(
        cfg.frame_samples,
        major_radius=cfg.major_radius,
        minor_radius=cfg.minor_radius,
    )
    sample_indices = np.linspace(0, cfg.frame_samples - 1, sample_count, endpoint=False, dtype=int)
    loop_radius = max(2.0 * cfg.grid.spacing, 0.75 * cfg.xi)
    phis = np.linspace(0.0, 2.0 * math.pi, loop_points, endpoint=False)

    loops = []
    for idx in sample_indices:
        center = curve[idx]
        loop = (
            center[None, :]
            + loop_radius * np.cos(phis)[:, None] * normal[idx][None, :]
            + loop_radius * np.sin(phis)[:, None] * binormal[idx][None, :]
        )
        loops.append(loop)

    return np.stack(loops, axis=0), float(loop_radius)


def topology_guard_satisfied(topology: dict[str, float], controls: RelaxationControls) -> bool:
    if not controls.topology_hard_guard:
        return True
    mean_floor = controls.topology_mean_winding_min
    if mean_floor is not None and topology["mean_winding"] < mean_floor:
        return False
    unit_floor = controls.topology_unit_fraction_min
    if unit_floor is not None and topology["unit_fraction"] < unit_floor:
        return False
    alignment_floor = controls.topology_alignment_score_min
    if alignment_floor is not None and topology["alignment_score"] < alignment_floor:
        return False
    return True


def topology_penalty(topology: dict[str, float], controls: RelaxationControls) -> float:
    if controls.topology_pressure_weight <= 0.0:
        return 0.0
    penalty = 0.0
    mean_floor = controls.topology_mean_winding_min
    if mean_floor is not None:
        mean_shortfall = max(mean_floor - topology["mean_winding"], 0.0)
        penalty += mean_shortfall * mean_shortfall
    unit_floor = controls.topology_unit_fraction_min
    if unit_floor is not None:
        unit_shortfall = max(unit_floor - topology["unit_fraction"], 0.0)
        penalty += unit_shortfall * unit_shortfall
    alignment_floor = controls.topology_alignment_score_min
    if alignment_floor is not None:
        alignment_shortfall = max(alignment_floor - topology["alignment_score"], 0.0)
        penalty += alignment_shortfall * alignment_shortfall
    return controls.topology_pressure_weight * penalty


def load_saved_state(path: Path) -> tuple[TrefoilConfig, RelaxationControls, np.ndarray, dict[str, object]]:
    data = np.load(path, allow_pickle=False)
    cfg = TrefoilConfig(**json.loads(str(data["config"])))
    controls = RelaxationControls(**json.loads(str(data["controls"])))
    psi = data["psi_real"] + 1j * data["psi_imag"]
    summary = json.loads(str(data["summary"]))

    if psi.shape != (cfg.n, cfg.n, cfg.n):
        raise ValueError(f"Saved state shape {psi.shape} does not match config grid ({cfg.n}, {cfg.n}, {cfg.n}).")

    x = data["x"]
    y = data["y"]
    z = data["z"]
    expected_x, expected_y, expected_z = coordinate_grid(cfg)
    if not (
        np.allclose(x, expected_x)
        and np.allclose(y, expected_y)
        and np.allclose(z, expected_z)
    ):
        raise ValueError("Saved state coordinate grid does not match the config-derived Cartesian grid.")

    return cfg, controls, psi.astype(np.complex128), summary


def save_state(
    path: Path,
    psi: np.ndarray,
    cfg: TrefoilConfig,
    controls: RelaxationControls,
    summary: RunSummary,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    x, y, z = coordinate_grid(cfg)
    np.savez_compressed(
        path,
        psi_real=psi.real,
        psi_imag=psi.imag,
        x=x,
        y=y,
        z=z,
        config=json.dumps(asdict(cfg)),
        controls=json.dumps(asdict(controls)),
        summary=json.dumps(asdict(summary)),
    )


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


def pinned_mask(cfg: TrefoilConfig) -> np.ndarray:
    mask = np.zeros((cfg.n, cfg.n, cfg.n), dtype=bool)
    shell = cfg.anchor_shell
    if shell <= 0:
        return mask
    mask[:shell, :, :] = True
    mask[-shell:, :, :] = True
    mask[:, :shell, :] = True
    mask[:, -shell:, :] = True
    mask[:, :, :shell] = True
    mask[:, :, -shell:] = True
    return mask


def l2_norm(field: np.ndarray, spacing: float) -> float:
    return float(np.sum(np.abs(field) ** 2) * spacing**3)


def free_mask(cfg: TrefoilConfig) -> np.ndarray:
    return ~pinned_mask(cfg)


def projected_gradient(
    psi: np.ndarray,
    gradient: np.ndarray,
    cfg: TrefoilConfig,
) -> np.ndarray:
    """Project the gradient onto the tangent space of the constrained L2 manifold.

    For the constrained flow, admissible variations satisfy
    Re <psi, delta psi> = 0 on the freely updated interior cells. We therefore
    subtract the component of the gradient parallel to psi on that free subspace.
    """
    mask = free_mask(cfg)
    projected = np.array(gradient, dtype=np.complex128, copy=True)
    projected[~mask] = 0.0
    if not np.any(mask):
        return projected

    cell_volume = cfg.grid.spacing**3
    psi_free = psi[mask]
    grad_free = gradient[mask]
    denom = float(np.sum(np.abs(psi_free) ** 2) * cell_volume)
    if denom <= 1.0e-16:
        return projected

    numer = float(np.real(np.vdot(psi_free, grad_free)) * cell_volume)
    multiplier = numer / denom
    projected[mask] = grad_free - multiplier * psi_free
    return projected


def enforce_l2_norm(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    target_norm: float,
) -> None:
    mask = ~pinned_mask(cfg)
    if not np.any(mask):
        return
    cell_volume = cfg.grid.spacing**3
    fixed_norm = float(np.sum(np.abs(psi[~mask]) ** 2) * cell_volume)
    free_norm = float(np.sum(np.abs(psi[mask]) ** 2) * cell_volume)
    if free_norm <= 1.0e-16:
        return
    numerator = max(target_norm - fixed_norm, 0.0)
    scale = math.sqrt(numerator / free_norm) if numerator > 0.0 else 0.0
    psi[mask] *= scale


def apply_boundary_anchor(psi: np.ndarray, cfg: TrefoilConfig) -> None:
    shell = cfg.anchor_shell
    if shell <= 0 and cfg.boundary_blend_fraction <= 0.0:
        return

    # Keep the very outermost cells pinned to the background to avoid wraparound artefacts.
    if shell > 0:
        psi[:shell, :, :] = 1.0 + 0.0j
        psi[-shell:, :, :] = 1.0 + 0.0j
        psi[:, :shell, :] = 1.0 + 0.0j
        psi[:, -shell:, :] = 1.0 + 0.0j
        psi[:, :, :shell] = 1.0 + 0.0j
        psi[:, :, -shell:] = 1.0 + 0.0j

    # Apply a soft radial blend in the outer region so the recovery profile is not
    # dominated by a hard box-wall clamp.
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
    psi[mask] = (1.0 - alpha[mask]) * psi[mask] + alpha[mask] * (1.0 + 0.0j)


def logse_gradient(psi: np.ndarray, cfg: TrefoilConfig) -> np.ndarray:
    rho = np.maximum(np.abs(psi) ** 2, cfg.density_floor)
    return -0.5 * laplacian(psi, cfg.grid.spacing) + cfg.log_pressure * np.log(rho) * psi


def topology_flow_term(
    psi: np.ndarray,
    reference_psi: np.ndarray,
    anchor_mask: np.ndarray,
    controls: RelaxationControls,
) -> np.ndarray:
    """Local branch-anchor term that keeps the flow near the seeded trefoil core.

    This is not a full topological invariant. It is a first continuous flow bias that
    penalizes losing the seeded trefoil branch structure in the near-core tube where the
    initial branch identity is encoded most strongly.
    """
    if controls.topology_flow_weight <= 0.0:
        return np.zeros_like(psi)
    term = np.zeros_like(psi)
    term[anchor_mask] = controls.topology_flow_weight * (psi[anchor_mask] - reference_psi[anchor_mask])
    return term


def topology_phase_flow_term(
    psi: np.ndarray,
    reference_psi: np.ndarray,
    phase_anchor_mask: np.ndarray,
    controls: RelaxationControls,
) -> np.ndarray:
    """Phase-aware branch anchor that nudges circulation toward the seeded trefoil pattern.

    The target keeps the current amplitude but replaces the local phase by the seeded
    trefoil phase. This pushes on circulation structure more directly than a full-field
    anchor while avoiding the singular core itself.
    """
    if controls.topology_phase_flow_weight <= 0.0:
        return np.zeros_like(psi)
    term = np.zeros_like(psi)
    reference_phase = np.exp(1j * np.angle(reference_psi[phase_anchor_mask]))
    target = np.abs(psi[phase_anchor_mask]) * reference_phase
    term[phase_anchor_mask] = controls.topology_phase_flow_weight * (psi[phase_anchor_mask] - target)
    return term


def scatter_complex_samples_to_grid(
    cfg: TrefoilConfig,
    points: np.ndarray,
    values: np.ndarray,
) -> np.ndarray:
    """Deposit complex sample values back to the Cartesian grid via trilinear weights."""
    dx = cfg.grid.spacing
    axis_min = -cfg.half_width + 0.5 * dx
    ux = np.clip((points[:, 0] - axis_min) / dx, 0.0, cfg.n - 1.0)
    uy = np.clip((points[:, 1] - axis_min) / dx, 0.0, cfg.n - 1.0)
    uz = np.clip((points[:, 2] - axis_min) / dx, 0.0, cfg.n - 1.0)

    ix0 = np.clip(np.floor(ux).astype(int), 0, cfg.n - 2)
    iy0 = np.clip(np.floor(uy).astype(int), 0, cfg.n - 2)
    iz0 = np.clip(np.floor(uz).astype(int), 0, cfg.n - 2)
    ix1 = ix0 + 1
    iy1 = iy0 + 1
    iz1 = iz0 + 1

    tx = ux - ix0
    ty = uy - iy0
    tz = uz - iz0

    result = np.zeros((cfg.n, cfg.n, cfg.n), dtype=np.complex128)
    weights = np.zeros((cfg.n, cfg.n, cfg.n), dtype=float)
    corners = (
        (ix0, iy0, iz0, (1.0 - tx) * (1.0 - ty) * (1.0 - tz)),
        (ix1, iy0, iz0, tx * (1.0 - ty) * (1.0 - tz)),
        (ix0, iy1, iz0, (1.0 - tx) * ty * (1.0 - tz)),
        (ix1, iy1, iz0, tx * ty * (1.0 - tz)),
        (ix0, iy0, iz1, (1.0 - tx) * (1.0 - ty) * tz),
        (ix1, iy0, iz1, tx * (1.0 - ty) * tz),
        (ix0, iy1, iz1, (1.0 - tx) * ty * tz),
        (ix1, iy1, iz1, tx * ty * tz),
    )
    for ix, iy, iz, w in corners:
        np.add.at(result, (ix, iy, iz), w * values)
        np.add.at(weights, (ix, iy, iz), w)

    mask = weights > 1.0e-12
    result[mask] /= weights[mask]
    return result


def topology_loop_flow_term(
    psi: np.ndarray,
    reference_psi: np.ndarray,
    cfg: TrefoilConfig,
    controls: RelaxationControls,
    loop_points: np.ndarray,
) -> np.ndarray:
    """Loop-circulation correction acting directly on sampled winding loops.

    This compares the current complex field to the seeded loop phase on the same
    sampled circulation loops used by the winding diagnostic, then deposits the
    mismatch back to the grid so the flow acts where circulation is measured.
    """
    if controls.topology_loop_flow_weight <= 0.0:
        return np.zeros_like(psi)

    flat_points = loop_points.reshape(-1, 3)
    current_samples = interpolate_complex_field(psi, cfg, flat_points)
    reference_samples = interpolate_complex_field(reference_psi, cfg, flat_points)
    target = np.abs(current_samples) * np.exp(1j * np.angle(reference_samples))
    mismatch = current_samples - target
    return controls.topology_loop_flow_weight * scatter_complex_samples_to_grid(cfg, flat_points, mismatch)


def topology_winding_flow_term(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    controls: RelaxationControls,
    loop_points: np.ndarray,
) -> np.ndarray:
    """Loop-circulation correction built from phase-increment mismatch.

    Rather than matching the seeded field value, this compares the discrete phase
    increments around each sampled loop to the target unit-circulation pattern and
    deposits a corrective phase torque back to the grid.
    """
    if controls.topology_winding_flow_weight <= 0.0:
        return np.zeros_like(psi)

    sample_count, loop_point_count, _ = loop_points.shape
    flat_points = loop_points.reshape(-1, 3)
    current_samples = interpolate_complex_field(psi, cfg, flat_points).reshape(sample_count, loop_point_count)

    current_phase = np.unwrap(np.angle(current_samples), axis=1)
    closed_phase = np.concatenate((current_phase, current_phase[:, :1] + 2.0 * math.pi), axis=1)
    increments = np.diff(closed_phase, axis=1)
    target_increment = (2.0 * math.pi) / loop_point_count
    mismatch = increments - target_increment

    # Convert edge mismatch into a node-local phase torque by taking the discrete
    # divergence of the increment error around the loop.
    node_torque = np.roll(mismatch, 1, axis=1) - mismatch
    point_torque = node_torque.reshape(-1)
    point_values = 1j * point_torque * current_samples.reshape(-1)
    return controls.topology_winding_flow_weight * scatter_complex_samples_to_grid(cfg, flat_points, point_values)


def relax(
    cfg: TrefoilConfig,
    controls: RelaxationControls,
    initial_psi: np.ndarray | None = None,
    continued_from_steps: int = 0,
) -> tuple[np.ndarray, RunSummary]:
    psi = initial_state(cfg) if initial_psi is None else np.array(initial_psi, dtype=np.complex128, copy=True)
    reference_psi = initial_state(cfg)
    reference_amp = np.abs(reference_psi)
    anchor_mask = reference_amp <= controls.topology_anchor_amplitude_cutoff
    phase_anchor_mask = (
        (reference_amp >= controls.topology_anchor_amplitude_min)
        & (reference_amp <= controls.topology_anchor_amplitude_cutoff)
    )
    loop_points, _loop_radius = loop_circulation_geometry(cfg)
    apply_boundary_anchor(psi, cfg)
    target_l2_norm = l2_norm(psi, cfg.grid.spacing)
    x, y, z = coordinate_grid(cfg)
    gradient_fn = lambda field: (
        logse_gradient(field, cfg)
        + topology_flow_term(field, reference_psi, anchor_mask, controls)
        + topology_phase_flow_term(field, reference_psi, phase_anchor_mask, controls)
        + topology_loop_flow_term(field, reference_psi, cfg, controls, loop_points)
        + topology_winding_flow_term(field, cfg, controls, loop_points)
    )
    projected_residual_fn = lambda field: projected_gradient(field, gradient_fn(field), cfg)

    last_energy = total_energy(psi, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
    best_energy = last_energy
    best_psi = psi.copy()
    best_topology = branch_winding_diagnostics(psi, cfg)
    last_effective_objective = last_energy + topology_penalty(best_topology, controls)
    violations = 0
    completed = 0
    accepted_steps = 0
    rejected_steps = 0
    topology_rejections = 0
    max_backtracks_used = 0
    reference_spacing = controls.reference_spacing if controls.reference_spacing is not None else (10.0 / 24.0)
    step_scale = grid_step_scale(cfg.grid.spacing, reference_spacing)
    step_size = min(controls.step_size * step_scale, controls.max_step_size * step_scale)
    effective_min_step_size = controls.min_step_size * step_scale
    effective_max_step_size = controls.max_step_size * step_scale
    stale_intervals = 0
    stop_reason = "max_steps"

    for step in range(1, controls.max_steps + 1):
        gradient = gradient_fn(psi)
        current_energy = None
        candidate = None
        trial_step_size = step_size
        accepted = False
        used_backtracks = 0

        for backtrack in range(controls.max_backtracks + 1):
            trial = psi - trial_step_size * gradient
            apply_boundary_anchor(trial, cfg)
            if controls.conserve_l2_norm:
                enforce_l2_norm(trial, cfg, target_l2_norm)
                apply_boundary_anchor(trial, cfg)

            trial_energy = total_energy(trial, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
            trial_topology = branch_winding_diagnostics(trial, cfg)
            allowed_increase = controls.energy_tol + controls.relative_energy_tol * max(abs(last_energy), abs(trial_energy), 1.0)
            effective_allowed_increase = controls.energy_tol + controls.relative_energy_tol * max(
                abs(last_effective_objective),
                abs(trial_energy + topology_penalty(trial_topology, controls)),
                1.0,
            )
            if trial_energy <= last_energy + allowed_increase:
                if not topology_guard_satisfied(trial_topology, controls):
                    topology_rejections += 1
                    rejected_steps += 1
                    trial_step_size *= controls.line_search_shrink
                    if trial_step_size < effective_min_step_size:
                        break
                    continue
                trial_effective_objective = trial_energy + topology_penalty(trial_topology, controls)
                if trial_effective_objective <= last_effective_objective + effective_allowed_increase:
                    candidate = trial
                    current_energy = trial_energy
                    accepted = True
                    used_backtracks = backtrack
                    accepted_topology = trial_topology
                    accepted_effective_objective = trial_effective_objective
                    break

            violations += 1
            rejected_steps += 1
            trial_step_size *= controls.line_search_shrink
            if trial_step_size < effective_min_step_size:
                break

        if not accepted:
            step_size = trial_step_size
            stop_reason = "step_size_floor"
            completed = step
            break

        max_backtracks_used = max(max_backtracks_used, used_backtracks)
        step_size = trial_step_size

        psi = candidate
        accepted_steps += 1
        completed = step

        energy_improvement = last_energy - current_energy
        last_energy = current_energy
        last_effective_objective = accepted_effective_objective
        if current_energy < best_energy:
            best_energy = current_energy
            best_psi = psi.copy()
            best_topology = accepted_topology

        if energy_improvement <= controls.energy_tol:
            stale_intervals += 1
        else:
            stale_intervals = 0
            step_size = min(step_size * 1.05, effective_max_step_size)

        if accepted_steps % controls.check_interval == 0:
            current_residual = (
                residual_norm(psi, projected_residual_fn)
                if controls.conserve_l2_norm
                else residual_norm(psi, gradient_fn)
            )
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
    topology = best_topology
    summary = RunSummary(
        continued_from_steps=continued_from_steps,
        steps_completed=completed,
        total_steps_effective=continued_from_steps + completed,
        initial_l2_norm=target_l2_norm,
        final_l2_norm=l2_norm(psi, cfg.grid.spacing),
        l2_norm_relative_drift=abs(l2_norm(psi, cfg.grid.spacing) - target_l2_norm) / max(abs(target_l2_norm), 1.0e-12),
        final_energy=last_energy,
        best_energy=best_energy,
        energy_monotonicity_violations=violations,
        accepted_steps=accepted_steps,
        rejected_steps=rejected_steps,
        max_backtracks_used=max_backtracks_used,
        final_step_size=step_size,
        residual_norm=residual_norm(psi, gradient_fn),
        projected_residual_norm=residual_norm(psi, projected_residual_fn),
        depressed_fraction=depressed_fraction(psi, cfg.depressed_threshold),
        effective_radius=effective_radius(psi, x, y, z),
        deficit_volume=deficit_volume(psi, cfg.grid.spacing),
        equivalent_deficit_radius=equivalent_deficit_radius(psi, cfg.grid.spacing),
        far_field_shell_density=shell_mean_density(psi, x, y, z, shell_inner, shell_outer),
        far_field_shell_deficit=shell_mean_deficit(psi, x, y, z, shell_inner, shell_outer),
        far_field_moment=far_field_moment(psi, x, y, z, shell_inner),
        topology_loop_radius=topology["loop_radius"],
        topology_mean_winding=topology["mean_winding"],
        topology_winding_std=topology["winding_std"],
        topology_min_winding=topology["min_winding"],
        topology_max_winding=topology["max_winding"],
        topology_unit_fraction=topology["unit_fraction"],
        topology_alignment_score=topology["alignment_score"],
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
    parser.add_argument("--no-conserve-l2-norm", action="store_true")
    parser.add_argument("--min-step-size", type=float, default=1.0e-5)
    parser.add_argument("--max-step-size", type=float, default=5.0e-2)
    parser.add_argument("--check-interval", type=int, default=10)
    parser.add_argument("--patience-intervals", type=int, default=3)
    parser.add_argument("--energy-tol", type=float, default=1.0e-9)
    parser.add_argument("--relative-energy-tol", type=float, default=1.0e-10)
    parser.add_argument("--line-search-shrink", type=float, default=0.5)
    parser.add_argument("--max-backtracks", type=int, default=12)
    parser.add_argument("--reference-spacing", type=float)
    parser.add_argument("--boundary-blend-fraction", type=float, default=0.18)
    parser.add_argument("--topology-mean-winding-min", type=float)
    parser.add_argument("--topology-unit-fraction-min", type=float)
    parser.add_argument("--topology-alignment-score-min", type=float)
    parser.add_argument("--topology-pressure-weight", type=float, default=0.0)
    parser.add_argument("--topology-flow-weight", type=float, default=0.0)
    parser.add_argument("--topology-phase-flow-weight", type=float, default=0.0)
    parser.add_argument("--topology-loop-flow-weight", type=float, default=0.0)
    parser.add_argument("--topology-anchor-amplitude-min", type=float, default=0.15)
    parser.add_argument("--topology-anchor-amplitude-cutoff", type=float, default=0.95)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--load-state", type=Path)
    parser.add_argument("--save-state", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    continuation_source = None
    initial_psi = None
    continued_from_steps = 0

    if args.load_state:
        cfg, saved_controls, initial_psi, saved_summary = load_saved_state(args.load_state)
        continuation_source = str(args.load_state)
        continued_from_steps = int(saved_summary.get("total_steps_effective", saved_summary.get("steps_completed", 0)))
        controls = RelaxationControls(
            step_size=args.step_size,
            max_steps=args.max_steps,
            tolerance=args.tolerance,
            conserve_l2_norm=not args.no_conserve_l2_norm,
            min_step_size=args.min_step_size,
            max_step_size=args.max_step_size,
            check_interval=args.check_interval,
            patience_intervals=args.patience_intervals,
            energy_tol=args.energy_tol,
            relative_energy_tol=args.relative_energy_tol,
            line_search_shrink=args.line_search_shrink,
            max_backtracks=args.max_backtracks,
            reference_spacing=args.reference_spacing if args.reference_spacing is not None else saved_controls.reference_spacing,
            topology_hard_guard=False,
            topology_mean_winding_min=args.topology_mean_winding_min,
            topology_unit_fraction_min=args.topology_unit_fraction_min,
            topology_alignment_score_min=args.topology_alignment_score_min,
            topology_pressure_weight=args.topology_pressure_weight,
            topology_flow_weight=args.topology_flow_weight,
            topology_phase_flow_weight=args.topology_phase_flow_weight,
            topology_loop_flow_weight=args.topology_loop_flow_weight,
            topology_anchor_amplitude_min=args.topology_anchor_amplitude_min,
            topology_anchor_amplitude_cutoff=args.topology_anchor_amplitude_cutoff,
        )
    else:
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
            conserve_l2_norm=not args.no_conserve_l2_norm,
            min_step_size=args.min_step_size,
            max_step_size=args.max_step_size,
            check_interval=args.check_interval,
            patience_intervals=args.patience_intervals,
            energy_tol=args.energy_tol,
            relative_energy_tol=args.relative_energy_tol,
            line_search_shrink=args.line_search_shrink,
            max_backtracks=args.max_backtracks,
            reference_spacing=args.reference_spacing,
            topology_hard_guard=False,
            topology_mean_winding_min=args.topology_mean_winding_min,
            topology_unit_fraction_min=args.topology_unit_fraction_min,
            topology_alignment_score_min=args.topology_alignment_score_min,
            topology_pressure_weight=args.topology_pressure_weight,
            topology_flow_weight=args.topology_flow_weight,
            topology_phase_flow_weight=args.topology_phase_flow_weight,
            topology_loop_flow_weight=args.topology_loop_flow_weight,
            topology_anchor_amplitude_min=args.topology_anchor_amplitude_min,
            topology_anchor_amplitude_cutoff=args.topology_anchor_amplitude_cutoff,
        )
    psi, summary = relax(cfg, controls, initial_psi=initial_psi, continued_from_steps=continued_from_steps)

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
        "continuation": {
            "source": continuation_source,
            "continued_from_steps": continued_from_steps,
        },
        "summary": asdict(summary),
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    if args.save_state:
        save_state(args.save_state, psi, cfg, controls, summary)
    print(text)


if __name__ == "__main__":
    main()

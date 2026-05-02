from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from direct_bdg_projection import project_operator
from kelvin_augmented_bdg import AzimuthalMode, build_bdg, build_modes, kelvin_self_induction_shift
from muon_mode_prototype import SSVScales
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


@dataclass(frozen=True)
class ScanPoint:
    omega: float
    total_response: float
    core_response: float
    kelvin_response: float
    response_ratio: float


def boundary_shell_drive(
    bg,
    cfg: ProjectionConfig,
    basis_mode: AzimuthalMode,
    drive_mode: AzimuthalMode,
    shell_width: float,
) -> complex:
    """Project an analytic boundary-shell Kelvin drive into a basis mode.

    The full 3D drive is a Kelvin helicity wave on the outer meridional shell.
    Since the basis already carries the azimuthal label analytically, this
    routine projects only the matching 2D meridional envelope.
    """
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    total = 0.0j
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            s = bg.s(r, z)
            if s < cfg.half_width - shell_width:
                continue
            drive = drive_mode.field(r, z)
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz
            total += weight * basis_mode.field(r, z).conjugate() * drive
    return total


def drive_vector(bg, modes: list[AzimuthalMode], cfg: ProjectionConfig, shell_width: float, drive_mode_name: str) -> np.ndarray:
    n = len(modes)
    vec = np.zeros(2 * n, dtype=complex)
    drive_mode = next((mode for mode in modes if mode.name == drive_mode_name), None)
    if drive_mode is None:
        raise ValueError(f"Drive mode {drive_mode_name!r} not found. Available: {', '.join(m.name for m in modes)}")

    drive_m = drive_mode.m_phi
    for i, mode in enumerate(modes):
        if mode.m_phi != drive_m:
            continue
        # Boundary drive enters the particle channel. A conjugate hole drive
        # can be added later for a real time-domain boundary condition.
        vec[i] = boundary_shell_drive(bg, cfg, mode, drive_mode, shell_width)
    norm = np.linalg.norm(vec)
    if norm > 0.0:
        vec /= norm
    return vec


def sector_response(x: np.ndarray, mode_count: int, core_count: int = 2) -> tuple[float, float, float]:
    core_indices = list(range(core_count)) + list(range(mode_count, mode_count + core_count))
    kelvin_indices = [idx for idx in range(2 * mode_count) if idx not in core_indices]
    core = float(np.linalg.norm(x[core_indices]))
    kelvin = float(np.linalg.norm(x[kelvin_indices]))
    total = float(np.linalg.norm(x))
    return total, core, kelvin


def solve_response(h: np.ndarray, drive: np.ndarray, omega: float, damping: float) -> np.ndarray:
    size = h.shape[0]
    a = h - (omega + 1j * damping) * np.eye(size, dtype=complex)
    return np.linalg.solve(a, drive)


def scan(
    h: np.ndarray,
    drive: np.ndarray,
    mode_count: int,
    omega_min: float,
    omega_max: float,
    omega_steps: int,
    damping: float,
) -> list[ScanPoint]:
    points = []
    for idx in range(omega_steps):
        omega = omega_min + (omega_max - omega_min) * idx / max(omega_steps - 1, 1)
        x = solve_response(h, drive, omega, damping)
        total, core, kelvin = sector_response(x, mode_count)
        points.append(
            ScanPoint(
                omega=omega,
                total_response=total,
                core_response=core,
                kelvin_response=kelvin,
                response_ratio=core / max(kelvin, 1.0e-30),
            )
        )
    return points


def half_max_width(points: list[ScanPoint]) -> tuple[float, float] | None:
    if not points:
        return None
    peak = max(points, key=lambda point: point.total_response)
    half = 0.5 * peak.total_response
    above = [point.omega for point in points if point.total_response >= half]
    if not above:
        return None
    return min(above), max(above)


def nearest_half_rung(omega: float) -> tuple[float, float, float]:
    mu0 = (2.0 / 3.0) * SSVScales().muon_ratio_draft
    rung = max(0.5, round(2.0 * omega / mu0) / 2.0)
    value = rung * mu0
    return rung, value, abs(omega - value) / max(value, 1.0e-30)


def local_peaks(points: list[ScanPoint], min_prominence: float) -> list[ScanPoint]:
    if len(points) < 3:
        return points[:]
    peaks = []
    for i in range(1, len(points) - 1):
        prev_p = points[i - 1]
        point = points[i]
        next_p = points[i + 1]
        if point.total_response < prev_p.total_response or point.total_response < next_p.total_response:
            continue
        shoulder = max(prev_p.total_response, next_p.total_response)
        if point.total_response - shoulder >= min_prominence:
            peaks.append(point)
    return sorted(peaks, key=lambda point: point.total_response, reverse=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Driven-boundary Kelvin response scan for Arnold-tongue-like resonance peaks.")
    parser.add_argument("--n", type=int, default=31)
    parser.add_argument("--half-width", type=float, default=5.0)
    parser.add_argument("--profile-n", type=int, default=1200)
    parser.add_argument("--lambda-perp", type=float, default=math.pi / 4.0)
    parser.add_argument("--kelvin-phi-n", type=int, default=1024)
    parser.add_argument("--kelvin-core-radius", type=float, default=1.0)
    parser.add_argument("--drive-mode", default="K_helicity_plus_plus")
    parser.add_argument("--shell-width", type=float, default=1.0)
    parser.add_argument("--omega-min", type=float, default=0.10)
    parser.add_argument("--omega-max", type=float, default=0.40)
    parser.add_argument("--omega-steps", type=int, default=61)
    parser.add_argument("--damping", type=float, default=0.01)
    parser.add_argument("--top", type=int, default=8)
    parser.add_argument("--peak-prominence", type=float, default=0.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        profile="numerical",
        profile_n=args.profile_n,
        chi_parity="sin",
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=False, kelvin_seed="helicity")
    h = np.array(
        build_bdg(
            bg,
            modes,
            cfg,
            "profile-logse",
            chiral_mix=0.0,
            bridge_model="shape",
            lambda_perp=args.lambda_perp,
            kelvin_dispersion="self-induction",
            kelvin_phi_n=args.kelvin_phi_n,
            kelvin_core_radius=args.kelvin_core_radius,
        ),
        dtype=complex,
    )
    drive = drive_vector(bg, modes, cfg, args.shell_width, args.drive_mode)
    points = scan(h, drive, len(modes), args.omega_min, args.omega_max, args.omega_steps, args.damping)
    peak = max(points, key=lambda point: point.total_response)
    width = half_max_width(points)
    kelvin_scale = kelvin_self_induction_shift(bg, args.kelvin_phi_n, args.kelvin_core_radius)

    print("Driven-boundary Kelvin response scan")
    print(f"grid n                   = {cfg.n}")
    print(f"half_width               = {cfg.half_width}")
    print(f"profile_n                = {cfg.profile_n}")
    print(f"lambda_perp              = {args.lambda_perp:.12e}")
    print(f"kelvin_self_induction    = {kelvin_scale:.12e}")
    print(f"drive_mode               = {args.drive_mode}")
    print(f"shell_width              = {args.shell_width:.12e}")
    print(f"damping                  = {args.damping:.12e}")
    print(f"omega_range              = {args.omega_min:.12e} {args.omega_max:.12e}")
    print(f"omega_steps              = {args.omega_steps}")
    print(f"peak_omega               = {peak.omega:.12e}")
    print(f"peak_total_response      = {peak.total_response:.12e}")
    print(f"peak_core_response       = {peak.core_response:.12e}")
    print(f"peak_kelvin_response     = {peak.kelvin_response:.12e}")
    print(f"peak_core_kelvin_ratio   = {peak.response_ratio:.12e}")
    if width is not None:
        print(f"half_max_width           = {width[0]:.12e} {width[1]:.12e}")
        print(f"half_max_span            = {width[1] - width[0]:.12e}")
    print("top omega total_response core_response kelvin_response core_kelvin_ratio")
    for point in sorted(points, key=lambda item: item.total_response, reverse=True)[: args.top]:
        rung, rung_value, rel = nearest_half_rung(point.omega)
        print(
            f"{point.omega:.12e} {point.total_response:.12e} {point.core_response:.12e} "
            f"{point.kelvin_response:.12e} {point.response_ratio:.12e} "
            f"rung={rung:.1f} rung_value={rung_value:.12e} rung_rel_error={rel:.12e}"
        )
    peaks = local_peaks(points, args.peak_prominence)
    print("local_peaks omega total_response core_response kelvin_response core_kelvin_ratio rung rung_value rung_rel_error")
    for point in peaks[: args.top]:
        rung, rung_value, rel = nearest_half_rung(point.omega)
        print(
            f"{point.omega:.12e} {point.total_response:.12e} {point.core_response:.12e} "
            f"{point.kelvin_response:.12e} {point.response_ratio:.12e} "
            f"{rung:.1f} {rung_value:.12e} {rel:.12e}"
        )


if __name__ == "__main__":
    main()

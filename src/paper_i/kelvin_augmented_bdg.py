from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Callable

from direct_bdg_projection import (
    background_phase,
    m_operator,
    normalized_modes,
    project_operator,
    qr_eigenvalues,
)
from restricted_bdg_matrix import build_background, i_mode
from restricted_bdg_three_mode import gram_schmidt
from toroidal_background import ToroidalBackground
from toroidal_projection_integrals import ProjectionConfig


ComplexField = Callable[[float, float], complex]
ComplexMatrix = list[list[complex]]


def dense_eigenvalues(h: ComplexMatrix) -> tuple[list[complex], str]:
    try:
        import numpy as np
    except ModuleNotFoundError:
        return qr_eigenvalues(h), "internal-qr"
    eigs = np.linalg.eigvals(np.array(h, dtype=complex))
    return [complex(value) for value in eigs], "numpy"


@dataclass(frozen=True)
class AzimuthalMode:
    name: str
    field: ComplexField
    m_phi: int


def central_laplacian_cyl_m(field: ComplexField, m_phi: int, r: float, z: float, h: float) -> complex:
    d2_r = (field(r + h, z) - 2.0 * field(r, z) + field(r - h, z)) / (h * h)
    d_r = (field(r + h, z) - field(r - h, z)) / (2.0 * h)
    d2_z = (field(r, z + h) - 2.0 * field(r, z) + field(r, z - h)) / (h * h)
    azimuthal = -(m_phi * m_phi) * field(r, z) / max(r * r, 1.0e-12)
    return d2_r + d_r / max(r, 1.0e-12) + d2_z + azimuthal


def l_operator_m(
    bg: ToroidalBackground,
    mode: AzimuthalMode,
    r: float,
    z: float,
    cfg: ProjectionConfig,
    operator_model: str,
    effective_m_phi: int | None = None,
) -> complex:
    psi = bg.psi0(r, z)
    amp_sq = max(abs(psi) ** 2, 1.0e-12)
    m_phi = mode.m_phi if effective_m_phi is None else effective_m_phi
    lap = central_laplacian_cyl_m(mode.field, m_phi, r, z, cfg.dr)
    if operator_model == "provisional":
        return -0.5 * lap + 2.0 * (1.0 - amp_sq) * mode.field(r, z)
    return -0.5 * lap + (math.log(amp_sq) + 1.0) * mode.field(r, z)


def m_operator_m(
    bg: ToroidalBackground,
    mode: AzimuthalMode,
    r: float,
    z: float,
    cfg: ProjectionConfig,
    operator_model: str,
) -> complex:
    # Same local pairing as the direct two/four-mode diagnostic. The azimuthal
    # orthogonality is handled at projection time.
    return m_operator(bg, mode.field, r, z, cfg, operator_model)


def project_pair(
    bg: ToroidalBackground,
    bra: AzimuthalMode,
    op_field: ComplexField,
    ket_m: int,
    cfg: ProjectionConfig,
) -> complex:
    if bra.m_phi != ket_m:
        return 0.0j
    return project_operator(bg, bra.field, op_field, cfg)


def normalize_by_phi_modes(bg: ToroidalBackground, modes: list[AzimuthalMode], cfg: ProjectionConfig) -> list[AzimuthalMode]:
    normalized = []
    for mode in modes:
        norm = project_operator(bg, mode.field, mode.field, cfg).real
        scale = 1.0 / math.sqrt(abs(norm))

        def make_scaled(fn: ComplexField, factor: float) -> ComplexField:
            def scaled(r: float, z: float) -> complex:
                return factor * fn(r, z)

            return scaled

        normalized.append(AzimuthalMode(mode.name, make_scaled(mode.field, scale), mode.m_phi))
    return normalized


def build_modes(
    bg: ToroidalBackground,
    cfg: ProjectionConfig,
    include_core_four: bool,
    kelvin_seed: str,
) -> list[AzimuthalMode]:
    chi = bg.phi_chi_sin
    core_seeds = [bg.phi_R, chi]
    if include_core_four:
        core_seeds.extend([bg.phi_momentum, i_mode(chi)])
    core = gram_schmidt(bg, core_seeds, cfg)
    modes = [AzimuthalMode("R", core[0], 0), AzimuthalMode("chi", core[1], 0)]
    if include_core_four:
        modes.extend([AzimuthalMode("P_R", core[2], 0), AzimuthalMode("P_chi", core[3], 0)])
    if kelvin_seed == "breathing":
        modes.extend(
            [
                AzimuthalMode("K_plus", bg.phi_R, 1),
                AzimuthalMode("K_minus", bg.phi_R, -1),
            ]
        )
    elif kelvin_seed == "displacement":
        modes.extend(
            [
                AzimuthalMode("K_rad_plus", bg.phi_kelvin_radial, 1),
                AzimuthalMode("K_rad_minus", bg.phi_kelvin_radial, -1),
                AzimuthalMode("K_z_plus", bg.phi_kelvin_vertical, 1),
                AzimuthalMode("K_z_minus", bg.phi_kelvin_vertical, -1),
            ]
        )
    elif kelvin_seed == "helicity":
        def k_helicity(helicity: int) -> ComplexField:
            def field(r: float, z: float) -> complex:
                return (bg.phi_kelvin_radial(r, z) + 1j * helicity * bg.phi_kelvin_vertical(r, z)) / math.sqrt(2.0)

            return field

        modes.extend(
            [
                AzimuthalMode("K_helicity_plus_plus", k_helicity(1), 1),
                AzimuthalMode("K_helicity_minus_plus", k_helicity(1), -1),
                AzimuthalMode("K_helicity_plus_minus", k_helicity(-1), 1),
                AzimuthalMode("K_helicity_minus_minus", k_helicity(-1), -1),
            ]
        )
    return normalize_by_phi_modes(bg, modes, cfg)


def is_kelvin_mode(mode: AzimuthalMode) -> bool:
    return mode.name.startswith("K_")


def kelvin_self_induction_shift(bg: ToroidalBackground, phi_n: int, core_radius: float) -> float:
    from kelvin_self_induction import kelvin_self_induction

    result = kelvin_self_induction(
        radius=bg.r_e,
        core_radius=core_radius,
        m_phi=1,
        helicity=1,
        phi_n=phi_n,
        amplitude=1.0e-3 * bg.xi,
    )
    return result.omega_bdg_scale


def build_bdg(
    bg: ToroidalBackground,
    modes: list[AzimuthalMode],
    cfg: ProjectionConfig,
    operator_model: str,
    chiral_mix: float,
    bridge_model: str,
    lambda_perp: float,
    kelvin_dispersion: str = "local",
    kelvin_phi_n: int = 512,
    kelvin_core_radius: float = 1.0,
) -> ComplexMatrix:
    n = len(modes)
    size = 2 * n
    h = [[0.0j for _ in range(size)] for _ in range(size)]
    kelvin_shift = kelvin_self_induction_shift(bg, kelvin_phi_n, kelvin_core_radius) if kelvin_dispersion == "self-induction" else 0.0
    for i, bra in enumerate(modes):
        for j, ket in enumerate(modes):
            def l_ket(r: float, z: float, mode=ket) -> complex:
                effective_m = 0 if kelvin_dispersion == "self-induction" and is_kelvin_mode(mode) else None
                return l_operator_m(bg, mode, r, z, cfg, operator_model, effective_m_phi=effective_m)

            def m_ket(r: float, z: float, mode=ket) -> complex:
                return m_operator_m(bg, mode, r, z, cfg, operator_model)

            l_ij = project_pair(bg, bra, l_ket, ket.m_phi, cfg)
            m_ij = project_pair(bg, bra, m_ket, ket.m_phi, cfg)
            if kelvin_dispersion == "self-induction" and is_kelvin_mode(bra) and is_kelvin_mode(ket):
                # Kelvin waves are filament modes of the ring centerline. In the
                # self-induction model their Kelvin-Kelvin block is supplied by
                # the explicit azimuthal Biot-Savart integral, not by the local
                # straight-core BdG operator used for meridional core modes.
                l_ij = kelvin_shift if i == j else 0.0j
                m_ij = 0.0j
            if chiral_mix != 0.0 and abs(bra.m_phi - ket.m_phi) == 1:
                # Minimal chiral bridge: localized core overlap that carries one unit
                # of azimuthal angular momentum, connecting m=0 breathing/chiral modes
                # to m=±1 Kelvin centerline modes. This is a phenomenological projection
                # of the chiral-shear operator's angular-momentum-changing part.
                if bridge_model == "current-curl":
                    from chiral_bridge_projection import chiral_overlap

                    l_ij += chiral_mix * chiral_overlap(bg, bra, ket, cfg)
                else:
                    l_ij += chiral_mix * chiral_bridge_overlap(bg, bra, ket, cfg)
            if lambda_perp != 0.0:
                l_corr, m_corr = hermitian_current_curl_bdg_blocks(bg, bra, ket, cfg)
                l_ij += lambda_perp * l_corr
                m_ij += lambda_perp * m_corr
            h[i][j] = l_ij
            h[i][j + n] = m_ij
            h[i + n][j] = -m_ij.conjugate()
            h[i + n][j + n] = -l_ij.conjugate()
    return h


def hermitian_current_curl_bdg_blocks(
    bg: ToroidalBackground,
    bra: AzimuthalMode,
    ket: AzimuthalMode,
    cfg: ProjectionConfig,
) -> tuple[complex, complex]:
    # Treat delta psi and delta psi* as independent Nambu coordinates. The
    # curl-curl energy then gives a Hermitian normal block L from u/u and a
    # complex-symmetric anomalous block M from u/v.
    uu_ab = current_curl_component_overlap(bg, bra, "u", ket, "u", cfg)
    uu_ba = current_curl_component_overlap(bg, ket, "u", bra, "u", cfg).conjugate()
    uv_ab = current_curl_component_overlap(bg, bra, "u", ket, "v", cfg)
    uv_ba = current_curl_component_overlap(bg, ket, "u", bra, "v", cfg)
    return 0.5 * (uu_ab + uu_ba), 0.5 * (uv_ab + uv_ba)


def current_variation_component_m(
    bg: ToroidalBackground,
    mode: AzimuthalMode,
    component: str,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> tuple[complex, complex, complex]:
    from chiral_bridge_projection import central_gradient

    psi = bg.psi0(r, z)
    phi = mode.field(r, z)
    grad_psi = central_gradient(bg.psi0, r, z, cfg.dr)
    grad_phi = central_gradient(mode.field, r, z, cfg.dr)
    dphi_dvarphi = 1j * mode.m_phi * phi
    prefactor = 1.0 / (2.0j)

    if component == "u":
        j_r = prefactor * (psi.conjugate() * grad_phi[0] - phi * grad_psi[0].conjugate())
        j_z = prefactor * (psi.conjugate() * grad_phi[1] - phi * grad_psi[1].conjugate())
        j_phi = prefactor * psi.conjugate() * dphi_dvarphi / max(r, 1.0e-12)
        return j_r, j_phi, j_z
    if component == "v":
        j_r = prefactor * (phi * grad_psi[0] - psi * grad_phi[0])
        j_z = prefactor * (phi * grad_psi[1] - psi * grad_phi[1])
        j_phi = -prefactor * psi * dphi_dvarphi / max(r, 1.0e-12)
        return j_r, j_phi, j_z
    raise ValueError(f"unknown Nambu current component: {component}")


def curl_current_component_m(
    bg: ToroidalBackground,
    mode: AzimuthalMode,
    component: str,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> tuple[complex, complex, complex]:
    h = cfg.dr

    def jr(rr: float, zz: float) -> complex:
        return current_variation_component_m(bg, mode, component, rr, zz, cfg)[0]

    def jphi(rr: float, zz: float) -> complex:
        return current_variation_component_m(bg, mode, component, rr, zz, cfg)[1]

    def jz(rr: float, zz: float) -> complex:
        return current_variation_component_m(bg, mode, component, rr, zz, cfg)[2]

    j_r, _, _ = current_variation_component_m(bg, mode, component, r, z, cfg)
    d_jphi_dz = (jphi(r, z + h) - jphi(r, z - h)) / (2.0 * h)
    d_jz_dvarphi = 1j * mode.m_phi * jz(r, z)
    curl_r = (d_jz_dvarphi - r * d_jphi_dz) / max(r, 1.0e-12)

    d_jr_dz = (jr(r, z + h) - jr(r, z - h)) / (2.0 * h)
    d_jz_dr = (jz(r + h, z) - jz(r - h, z)) / (2.0 * h)
    curl_phi = d_jr_dz - d_jz_dr

    d_rjphi_dr = ((r + h) * jphi(r + h, z) - (r - h) * jphi(r - h, z)) / (2.0 * h)
    d_jr_dvarphi = 1j * mode.m_phi * j_r
    curl_z = (d_rjphi_dr - d_jr_dvarphi) / max(r, 1.0e-12)
    return curl_r, curl_phi, curl_z


def current_curl_component_overlap(
    bg: ToroidalBackground,
    a: AzimuthalMode,
    component_a: str,
    b: AzimuthalMode,
    component_b: str,
    cfg: ProjectionConfig,
) -> complex:
    total = 0.0j
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            ca = curl_current_component_m(bg, a, component_a, r, z, cfg)
            cb = curl_current_component_m(bg, b, component_b, r, z, cfg)
            dot = ca[0].conjugate() * cb[0] + ca[1].conjugate() * cb[1] + ca[2].conjugate() * cb[2]
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz
            total += weight * dot
    return total


def chiral_bridge_overlap(
    bg: ToroidalBackground,
    bra: AzimuthalMode,
    ket: AzimuthalMode,
    cfg: ProjectionConfig,
) -> complex:
    total = 0.0j
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            psi = bg.psi0(r, z)
            core_weight = (1.0 - abs(psi) ** 2) ** 2
            theta = bg.theta(r, z)
            handed = 1.0
            if "K_rad" in ket.name or "K_rad" in bra.name:
                handed = math.cos(theta)
            elif "K_z" in ket.name or "K_z" in bra.name:
                handed = math.sin(theta)
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz
            total += weight * core_weight * handed * bra.field(r, z).conjugate() * ket.field(r, z)
    return total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Direct BdG projection with m_phi=±1 Kelvin seeds.")
    parser.add_argument("--n", type=int, default=31)
    parser.add_argument("--half-width", type=float, default=4.0)
    parser.add_argument("--profile", choices=("toy", "numerical"), default="numerical")
    parser.add_argument("--profile-n", type=int, default=1200)
    parser.add_argument("--profile-x-max", type=float, default=20.0)
    parser.add_argument("--operator-model", choices=("profile-logse", "provisional"), default="profile-logse")
    parser.add_argument("--core-basis", choices=("two", "four"), default="four")
    parser.add_argument(
        "--kelvin-seed",
        choices=("breathing", "displacement", "helicity"),
        default="displacement",
        help="Kelvin seed shape: breathing=Phi_R e^imphi, displacement=-grad Psi0 e^imphi, helicity=K_rad +/- i K_z.",
    )
    parser.add_argument(
        "--chiral-mix",
        type=float,
        default=0.0,
        help="Phenomenological chiral bridge strength between m=0 core modes and m=±1 Kelvin modes.",
    )
    parser.add_argument(
        "--bridge-model",
        choices=("shape", "current-curl"),
        default="shape",
        help="Bridge matrix element model.",
    )
    parser.add_argument(
        "--lambda-perp",
        type=float,
        default=0.0,
        help="Hermitian projected current-curl chiral block strength.",
    )
    parser.add_argument(
        "--kelvin-dispersion",
        choices=("local", "self-induction"),
        default="local",
        help="Kelvin azimuthal physics: local uses analytic m_phi/r term, self-induction uses an explicit vortex-ring azimuthal integral.",
    )
    parser.add_argument("--kelvin-phi-n", type=int, default=512, help="Azimuthal quadrature points for self-induction Kelvin dispersion.")
    parser.add_argument("--kelvin-core-radius", type=float, default=1.0, help="Regularization core radius for self-induction Kelvin dispersion.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        profile=args.profile,
        profile_n=args.profile_n,
        profile_x_max=args.profile_x_max,
        chi_parity="sin",
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(
        bg,
        cfg,
        include_core_four=args.core_basis == "four",
        kelvin_seed=args.kelvin_seed,
    )
    h = build_bdg(
        bg,
        modes,
        cfg,
        args.operator_model,
        chiral_mix=args.chiral_mix,
        bridge_model=args.bridge_model,
        lambda_perp=args.lambda_perp,
        kelvin_dispersion=args.kelvin_dispersion,
        kelvin_phi_n=args.kelvin_phi_n,
        kelvin_core_radius=args.kelvin_core_radius,
    )
    eigs, eigensolver = dense_eigenvalues(h)
    positive = sorted(value.real for value in eigs if value.real > 1.0e-5 and abs(value.imag) < 1.0e-5)
    positive_above_kelvin = [value for value in positive if value > 5.0e-2]
    print("Kelvin-augmented direct BdG projection")
    print(f"eigensolver              = {eigensolver}")
    print(f"grid n                   = {cfg.n}")
    print(f"half_width               = {cfg.half_width}")
    print(f"profile                  = {cfg.profile}")
    print(f"profile_n                = {cfg.profile_n}")
    print(f"operator_model           = {args.operator_model}")
    print(f"core_basis               = {args.core_basis}")
    print(f"kelvin_seed              = {args.kelvin_seed}")
    print(f"chiral_mix               = {args.chiral_mix:.9e}")
    print(f"bridge_model             = {args.bridge_model}")
    print(f"lambda_perp              = {args.lambda_perp:.9e}")
    print(f"kelvin_dispersion        = {args.kelvin_dispersion}")
    if args.kelvin_dispersion == "self-induction":
        print(f"kelvin_phi_n             = {args.kelvin_phi_n}")
        print(f"kelvin_core_radius       = {args.kelvin_core_radius:.9e}")
        print(f"kelvin_self_induction    = {kelvin_self_induction_shift(bg, args.kelvin_phi_n, args.kelvin_core_radius):.9e}")
    print("Modes")
    for i, mode in enumerate(modes):
        print(f"  {i}: {mode.name}, m_phi={mode.m_phi}")
    print("Positive eigenvalues")
    for value in positive:
        print(f"  {value:.9e}")
    if positive:
        print(f"lowest_positive          = {positive[0]:.9e}")
    else:
        print("  none passing real-positive filter")
    if positive_above_kelvin:
        print(f"lowest_above_kelvin      = {positive_above_kelvin[0]:.9e}")
    print("All eigenvalues")
    for value in sorted(eigs, key=lambda z: (z.real, z.imag)):
        print(f"  {value.real:.9e} {value.imag:+.9e}i")


if __name__ == "__main__":
    main()

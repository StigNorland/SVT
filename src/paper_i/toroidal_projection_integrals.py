from __future__ import annotations

from dataclasses import dataclass
import argparse
import math
from multiprocessing import Pool
from typing import Callable

from toroidal_background import CurvedToroidalBackground, ToroidalBackground
from vortex_profile import VortexProfile


ComplexField = Callable[[float, float], complex]


@dataclass(frozen=True)
class ProjectionConfig:
    half_width: float = 8.0
    n: int = 101
    hbar: float = 1.0
    m0: float = 1.0
    rho0: float = 1.0
    b: float = 0.5
    lambda_chiral: float | None = None
    density_floor: float = 1.0e-8
    chi_parity: str = "cos"
    orthogonalize_chi: bool = True
    profile: str = "toy"
    profile_n: int = 2000
    profile_x_max: float = 20.0
    workers: int = 1
    curvature_coeffs: tuple[float, ...] = ()
    phase_coeffs: tuple[float, ...] = ()
    inner_outer_stiffness: float = 0.0

    @property
    def dr(self) -> float:
        return 2.0 * self.half_width / self.n

    @property
    def dz(self) -> float:
        return self.dr


@dataclass(frozen=True)
class ProjectionResult:
    k0_rr: float
    k0_rchi: float
    k0_chichi: float
    kp_rr: float
    kp_rchi: float
    kp_chichi: float
    kio_rr: float
    norm_rr: float
    norm_rchi: float
    norm_chichi: float

    @property
    def k_rr(self) -> float:
        return self.k0_rr + self.kp_rr + self.kio_rr

    @property
    def k_rchi(self) -> float:
        return self.k0_rchi + self.kp_rchi

    @property
    def k_chichi(self) -> float:
        return self.k0_chichi + self.kp_chichi

    @property
    def k_rr_normalized(self) -> float:
        return self.k_rr / self.norm_rr

    @property
    def k_rchi_normalized(self) -> float:
        return self.k_rchi / math.sqrt(self.norm_rr * self.norm_chichi)

    @property
    def k_chichi_normalized(self) -> float:
        return self.k_chichi / self.norm_chichi


def central_gradient(field: ComplexField, r: float, z: float, step: float) -> tuple[complex, complex]:
    d_r = (field(r + step, z) - field(r - step, z)) / (2.0 * step)
    d_z = (field(r, z + step) - field(r, z - step)) / (2.0 * step)
    return d_r, d_z


def density_variation(bg: ToroidalBackground, mode: ComplexField, r: float, z: float) -> float:
    psi = bg.psi0(r, z)
    phi = mode(r, z)
    return 2.0 * (psi.conjugate() * phi).real


def logse_stiffness_integrand(
    bg: ToroidalBackground,
    mode_a: ComplexField,
    mode_b: ComplexField,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> float:
    grad_a = central_gradient(mode_a, r, z, cfg.dr)
    grad_b = central_gradient(mode_b, r, z, cfg.dr)
    grad_dot = (grad_a[0].conjugate() * grad_b[0] + grad_a[1].conjugate() * grad_b[1]).real

    psi_abs_sq = abs(bg.psi0(r, z)) ** 2
    rho = max(cfg.rho0 * psi_abs_sq, cfg.density_floor)
    v_second = -cfg.b / rho
    delta_rho_a = cfg.rho0 * density_variation(bg, mode_a, r, z)
    delta_rho_b = cfg.rho0 * density_variation(bg, mode_b, r, z)

    gradient_piece = (cfg.hbar**2 / (2.0 * cfg.m0)) * grad_dot
    density_piece = 0.5 * v_second * delta_rho_a * delta_rho_b
    return gradient_piece + density_piece


def current_variation(
    bg: ToroidalBackground,
    mode: ComplexField,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> tuple[float, float]:
    psi = bg.psi0(r, z)
    phi = mode(r, z)
    grad_psi = central_gradient(bg.psi0, r, z, cfg.dr)
    grad_phi = central_gradient(mode, r, z, cfg.dr)

    prefactor = cfg.hbar / (2.0 * cfg.m0 * 1j)
    j_r = prefactor * (
        phi.conjugate() * grad_psi[0]
        + psi.conjugate() * grad_phi[0]
        - phi * grad_psi[0].conjugate()
        - psi * grad_phi[0].conjugate()
    )
    j_z = prefactor * (
        phi.conjugate() * grad_psi[1]
        + psi.conjugate() * grad_phi[1]
        - phi * grad_psi[1].conjugate()
        - psi * grad_phi[1].conjugate()
    )
    return j_r.real, j_z.real


def curl_current_variation(
    bg: ToroidalBackground,
    mode: ComplexField,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> float:
    step = cfg.dr

    def j_r_at(rr: float, zz: float) -> float:
        return current_variation(bg, mode, rr, zz, cfg)[0]

    def j_z_at(rr: float, zz: float) -> float:
        return current_variation(bg, mode, rr, zz, cfg)[1]

    d_jr_dz = (j_r_at(r, z + step) - j_r_at(r, z - step)) / (2.0 * step)
    d_jz_dr = (j_z_at(r + step, z) - j_z_at(r - step, z)) / (2.0 * step)
    return d_jr_dz - d_jz_dr


def chiral_stiffness_integrand(
    bg: ToroidalBackground,
    mode_a: ComplexField,
    mode_b: ComplexField,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> float:
    lambda_chiral = cfg.lambda_chiral
    if lambda_chiral is None:
        lambda_chiral = bg.alpha**2 * cfg.rho0 / cfg.m0

    curl_a = curl_current_variation(bg, mode_a, r, z, cfg)
    curl_b = curl_current_variation(bg, mode_b, r, z, cfg)
    prefactor = lambda_chiral * cfg.hbar**2 / (cfg.m0 * cfg.rho0)
    return prefactor * curl_a * curl_b


def norm_integrand(mode_a: ComplexField, mode_b: ComplexField, r: float, z: float) -> float:
    return (mode_a(r, z).conjugate() * mode_b(r, z)).real


def inner_outer_strain_integrand(bg: ToroidalBackground, r: float, z: float, cfg: ProjectionConfig) -> float:
    if cfg.inner_outer_stiffness == 0.0:
        return 0.0
    psi = bg.psi0(r, z)
    s_val = bg.s(r, z)
    theta = bg.theta(r, z)
    h_phi = bg.r_e + s_val * math.cos(theta)
    if h_phi <= 0.0:
        return 0.0

    # Localize the resistance to the defect/core. A bulk |psi|^2 weight would diverge
    # because the vacuum extends to infinity; (1-|psi|^2)^2 keeps the modulus attached
    # to the density-depleted toroidal core.
    core_weight = (1.0 - abs(psi) ** 2) ** 2

    # Leading inner/outer mismatch shape. The inner and outer sides sit at opposite signs
    # of cos(theta), so cos^2(theta) is the lowest even strain-energy density. The small
    # global curvature scale is represented by the fitted coefficient rather than adding
    # an extra alpha^2 suppression here.
    return cfg.inner_outer_stiffness * core_weight * (math.cos(theta) ** 2)


def integrate_pair(
    bg: ToroidalBackground,
    mode_a: ComplexField,
    mode_b: ComplexField,
    cfg: ProjectionConfig,
) -> tuple[float, float, float, float]:
    k0 = 0.0
    kp = 0.0
    kio = 0.0
    norm = 0.0
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz
            k0 += weight * logse_stiffness_integrand(bg, mode_a, mode_b, r, z, cfg)
            kp += weight * chiral_stiffness_integrand(bg, mode_a, mode_b, r, z, cfg)
            if mode_a == bg.phi_R and mode_b == bg.phi_R:
                kio += weight * inner_outer_strain_integrand(bg, r, z, cfg)
            norm += weight * norm_integrand(mode_a, mode_b, r, z)
    return k0, kp, kio, norm


def mode_value(
    bg: ToroidalBackground,
    mode_name: str,
    projection: float,
    r: float,
    z: float,
) -> complex:
    if mode_name == "R":
        return bg.phi_R(r, z)
    if mode_name == "chi_cos":
        return bg.phi_chi(r, z)
    if mode_name == "chi_sin":
        return bg.phi_chi_sin(r, z)
    if mode_name == "chi_cos_orth":
        return bg.phi_chi(r, z) - projection * bg.phi_R(r, z)
    if mode_name == "chi_sin_orth":
        return bg.phi_chi_sin(r, z) - projection * bg.phi_R(r, z)
    raise ValueError(f"Unknown mode name: {mode_name}")


def central_gradient_mode(
    bg: ToroidalBackground,
    mode_name: str,
    projection: float,
    r: float,
    z: float,
    step: float,
) -> tuple[complex, complex]:
    d_r = (
        mode_value(bg, mode_name, projection, r + step, z)
        - mode_value(bg, mode_name, projection, r - step, z)
    ) / (2.0 * step)
    d_z = (
        mode_value(bg, mode_name, projection, r, z + step)
        - mode_value(bg, mode_name, projection, r, z - step)
    ) / (2.0 * step)
    return d_r, d_z


def density_variation_mode(
    bg: ToroidalBackground,
    mode_name: str,
    projection: float,
    r: float,
    z: float,
) -> float:
    psi = bg.psi0(r, z)
    phi = mode_value(bg, mode_name, projection, r, z)
    return 2.0 * (psi.conjugate() * phi).real


def logse_stiffness_integrand_mode(
    bg: ToroidalBackground,
    mode_a: str,
    mode_b: str,
    projection_a: float,
    projection_b: float,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> float:
    grad_a = central_gradient_mode(bg, mode_a, projection_a, r, z, cfg.dr)
    grad_b = central_gradient_mode(bg, mode_b, projection_b, r, z, cfg.dr)
    grad_dot = (grad_a[0].conjugate() * grad_b[0] + grad_a[1].conjugate() * grad_b[1]).real
    psi_abs_sq = abs(bg.psi0(r, z)) ** 2
    rho = max(cfg.rho0 * psi_abs_sq, cfg.density_floor)
    v_second = -cfg.b / rho
    delta_rho_a = cfg.rho0 * density_variation_mode(bg, mode_a, projection_a, r, z)
    delta_rho_b = cfg.rho0 * density_variation_mode(bg, mode_b, projection_b, r, z)
    return (cfg.hbar**2 / (2.0 * cfg.m0)) * grad_dot + 0.5 * v_second * delta_rho_a * delta_rho_b


def current_variation_mode(
    bg: ToroidalBackground,
    mode_name: str,
    projection: float,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> tuple[float, float]:
    psi = bg.psi0(r, z)
    phi = mode_value(bg, mode_name, projection, r, z)
    grad_psi = central_gradient(bg.psi0, r, z, cfg.dr)
    grad_phi = central_gradient_mode(bg, mode_name, projection, r, z, cfg.dr)
    prefactor = cfg.hbar / (2.0 * cfg.m0 * 1j)
    j_r = prefactor * (
        phi.conjugate() * grad_psi[0]
        + psi.conjugate() * grad_phi[0]
        - phi * grad_psi[0].conjugate()
        - psi * grad_phi[0].conjugate()
    )
    j_z = prefactor * (
        phi.conjugate() * grad_psi[1]
        + psi.conjugate() * grad_phi[1]
        - phi * grad_psi[1].conjugate()
        - psi * grad_phi[1].conjugate()
    )
    return j_r.real, j_z.real


def curl_current_variation_mode(
    bg: ToroidalBackground,
    mode_name: str,
    projection: float,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> float:
    step = cfg.dr
    d_jr_dz = (
        current_variation_mode(bg, mode_name, projection, r, z + step, cfg)[0]
        - current_variation_mode(bg, mode_name, projection, r, z - step, cfg)[0]
    ) / (2.0 * step)
    d_jz_dr = (
        current_variation_mode(bg, mode_name, projection, r + step, z, cfg)[1]
        - current_variation_mode(bg, mode_name, projection, r - step, z, cfg)[1]
    ) / (2.0 * step)
    return d_jr_dz - d_jz_dr


def chiral_stiffness_integrand_mode(
    bg: ToroidalBackground,
    mode_a: str,
    mode_b: str,
    projection_a: float,
    projection_b: float,
    r: float,
    z: float,
    cfg: ProjectionConfig,
) -> float:
    lambda_chiral = cfg.lambda_chiral
    if lambda_chiral is None:
        lambda_chiral = bg.alpha**2 * cfg.rho0 / cfg.m0
    curl_a = curl_current_variation_mode(bg, mode_a, projection_a, r, z, cfg)
    curl_b = curl_current_variation_mode(bg, mode_b, projection_b, r, z, cfg)
    return lambda_chiral * cfg.hbar**2 / (cfg.m0 * cfg.rho0) * curl_a * curl_b


def norm_integrand_mode(
    bg: ToroidalBackground,
    mode_a: str,
    mode_b: str,
    projection_a: float,
    projection_b: float,
    r: float,
    z: float,
) -> float:
    return (
        mode_value(bg, mode_a, projection_a, r, z).conjugate()
        * mode_value(bg, mode_b, projection_b, r, z)
    ).real


def integrate_pair_row(args: tuple[ToroidalBackground, ProjectionConfig, str, str, float, float, int]) -> tuple[float, float, float, float]:
    bg, cfg, mode_a, mode_b, projection_a, projection_b, i = args
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    r = r_min + (i + 0.5) * cfg.dr
    if r <= 0.0:
        return 0.0, 0.0, 0.0
    k0 = 0.0
    kp = 0.0
    kio = 0.0
    norm = 0.0
    for j in range(cfg.n):
        z = z_min + (j + 0.5) * cfg.dz
        weight = 2.0 * math.pi * r * cfg.dr * cfg.dz
        k0 += weight * logse_stiffness_integrand_mode(
            bg, mode_a, mode_b, projection_a, projection_b, r, z, cfg
        )
        kp += weight * chiral_stiffness_integrand_mode(
            bg, mode_a, mode_b, projection_a, projection_b, r, z, cfg
        )
        if mode_a == "R" and mode_b == "R":
            kio += weight * inner_outer_strain_integrand(bg, r, z, cfg)
        norm += weight * norm_integrand_mode(bg, mode_a, mode_b, projection_a, projection_b, r, z)
    return k0, kp, kio, norm


def integrate_pair_parallel(
    bg: ToroidalBackground,
    mode_a: str,
    mode_b: str,
    projection_a: float,
    projection_b: float,
    cfg: ProjectionConfig,
) -> tuple[float, float, float, float]:
    tasks = [(bg, cfg, mode_a, mode_b, projection_a, projection_b, i) for i in range(cfg.n)]
    with Pool(processes=cfg.workers) as pool:
        rows = pool.map(integrate_pair_row, tasks)
    return (
        sum(row[0] for row in rows),
        sum(row[1] for row in rows),
        sum(row[2] for row in rows),
        sum(row[3] for row in rows),
    )


def compute_projection_integrals(cfg: ProjectionConfig) -> ProjectionResult:
    if cfg.profile == "numerical":
        profile = VortexProfile.solve(x_max=cfg.profile_x_max, n=cfg.profile_n)
        bg_cls = CurvedToroidalBackground if (cfg.curvature_coeffs or cfg.phase_coeffs) else ToroidalBackground
        bg = bg_cls(
            f0=profile.value,
            f0_prime=profile.derivative,
            curvature_coeffs=cfg.curvature_coeffs,
            phase_coeffs=cfg.phase_coeffs,
        ) if (cfg.curvature_coeffs or cfg.phase_coeffs) else bg_cls(f0=profile.value, f0_prime=profile.derivative)
    else:
        bg = (
            CurvedToroidalBackground(
                curvature_coeffs=cfg.curvature_coeffs,
                phase_coeffs=cfg.phase_coeffs,
            )
            if (cfg.curvature_coeffs or cfg.phase_coeffs)
            else ToroidalBackground()
        )
    mode_r = bg.phi_R
    mode_chi = bg.phi_chi if cfg.chi_parity == "cos" else bg.phi_chi_sin
    mode_chi_name = "chi_cos" if cfg.chi_parity == "cos" else "chi_sin"
    projection = 0.0
    if cfg.orthogonalize_chi:
        _, _, _, norm_rr_pre = integrate_pair(bg, mode_r, mode_r, cfg)
        _, _, _, norm_rchi_pre = integrate_pair(bg, mode_r, mode_chi, cfg)
        projection = norm_rchi_pre / norm_rr_pre
        raw_mode_chi = mode_chi

        def orthogonal_chi(r: float, z: float) -> complex:
            return raw_mode_chi(r, z) - projection * mode_r(r, z)

        mode_chi = orthogonal_chi
        mode_chi_name = f"{mode_chi_name}_orth"

    if cfg.workers > 1:
        k0_rr, kp_rr, kio_rr, norm_rr = integrate_pair_parallel(bg, "R", "R", 0.0, 0.0, cfg)
        k0_rchi, kp_rchi, _, norm_rchi = integrate_pair_parallel(
            bg, "R", mode_chi_name, 0.0, projection, cfg
        )
        k0_chichi, kp_chichi, _, norm_chichi = integrate_pair_parallel(
            bg, mode_chi_name, mode_chi_name, projection, projection, cfg
        )
    else:
        k0_rr, kp_rr, kio_rr, norm_rr = integrate_pair(bg, mode_r, mode_r, cfg)
        k0_rchi, kp_rchi, _, norm_rchi = integrate_pair(bg, mode_r, mode_chi, cfg)
        k0_chichi, kp_chichi, _, norm_chichi = integrate_pair(bg, mode_chi, mode_chi, cfg)
    return ProjectionResult(
        k0_rr=k0_rr,
        k0_rchi=k0_rchi,
        k0_chichi=k0_chichi,
        kp_rr=kp_rr,
        kp_rchi=kp_rchi,
        kp_chichi=kp_chichi,
        kio_rr=kio_rr,
        norm_rr=norm_rr,
        norm_rchi=norm_rchi,
        norm_chichi=norm_chichi,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute first toroidal projection-integral estimates for the SSV muon ansatz."
    )
    parser.add_argument("--n", type=int, default=61, help="Grid points per dimension.")
    parser.add_argument("--half-width", type=float, default=6.0, help="Domain half-width in xi units.")
    parser.add_argument(
        "--lambda-chiral",
        type=float,
        default=None,
        help="Override lambda. Default uses alpha^2 in natural rho0=m0=1 units.",
    )
    parser.add_argument(
        "--chi-parity",
        choices=("cos", "sin"),
        default="cos",
        help="Angular parity of the seed chiral mode.",
    )
    parser.add_argument(
        "--no-orthogonalize-chi",
        action="store_true",
        help="Disable Gram-Schmidt removal of the Phi_R component from Phi_chi.",
    )
    parser.add_argument(
        "--profile",
        choices=("toy", "numerical"),
        default="toy",
        help="Core profile source. 'numerical' solves Appendix C profile before projection.",
    )
    parser.add_argument(
        "--profile-n",
        type=int,
        default=2000,
        help="Grid size for the numerical planar profile solve.",
    )
    parser.add_argument(
        "--profile-x-max",
        type=float,
        default=20.0,
        help="Outer radius for the numerical planar profile solve.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes for projection rows. Use 1 for sequential.",
    )
    parser.add_argument(
        "--curvature-coeffs",
        default="",
        help="Comma-separated f1 curvature coefficients for the curved torus ansatz.",
    )
    parser.add_argument(
        "--phase-coeffs",
        default="",
        help="Comma-separated g1 phase/flow coefficients for the curved torus ansatz.",
    )
    parser.add_argument(
        "--inner-outer-stiffness",
        type=float,
        default=0.0,
        help="Dimensionless localized inner/outer breathing-strain stiffness coefficient.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    curvature_coeffs = (
        tuple(float(part) for part in args.curvature_coeffs.split(",") if part.strip())
        if args.curvature_coeffs.strip()
        else ()
    )
    phase_coeffs = (
        tuple(float(part) for part in args.phase_coeffs.split(",") if part.strip())
        if args.phase_coeffs.strip()
        else ()
    )
    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        lambda_chiral=args.lambda_chiral,
        chi_parity=args.chi_parity,
        orthogonalize_chi=not args.no_orthogonalize_chi,
        profile=args.profile,
        profile_n=args.profile_n,
        profile_x_max=args.profile_x_max,
        workers=args.workers,
        curvature_coeffs=curvature_coeffs,
        phase_coeffs=phase_coeffs,
        inner_outer_stiffness=args.inner_outer_stiffness,
    )
    result = compute_projection_integrals(cfg)
    print("Toroidal projection integral prototype")
    print(f"grid n                   = {cfg.n}")
    print(f"half_width               = {cfg.half_width}")
    print(f"chi_parity               = {cfg.chi_parity}")
    print(f"orthogonalize_chi        = {cfg.orthogonalize_chi}")
    print(f"profile                  = {cfg.profile}")
    print(f"workers                  = {cfg.workers}")
    print(f"curvature_coeffs         = {cfg.curvature_coeffs}")
    print(f"phase_coeffs             = {cfg.phase_coeffs}")
    print(f"inner_outer_stiffness    = {cfg.inner_outer_stiffness:.9e}")
    print(f"dr = dz                  = {cfg.dr:.6f}")
    print(f"K0_RR                    = {result.k0_rr:.9e}")
    print(f"K0_Rchi                  = {result.k0_rchi:.9e}")
    print(f"K0_chichi                = {result.k0_chichi:.9e}")
    print(f"Kperp_RR                 = {result.kp_rr:.9e}")
    print(f"Kperp_Rchi               = {result.kp_rchi:.9e}")
    print(f"Kperp_chichi             = {result.kp_chichi:.9e}")
    print(f"Kio_RR                   = {result.kio_rr:.9e}")
    print(f"K_RR                     = {result.k_rr:.9e}")
    print(f"K_Rchi                   = {result.k_rchi:.9e}")
    print(f"K_chichi                 = {result.k_chichi:.9e}")
    print(f"N_RR                     = {result.norm_rr:.9e}")
    print(f"N_Rchi                   = {result.norm_rchi:.9e}")
    print(f"N_chichi                 = {result.norm_chichi:.9e}")
    print(f"Khat_RR                  = {result.k_rr_normalized:.9e}")
    print(f"Khat_Rchi                = {result.k_rchi_normalized:.9e}")
    print(f"Khat_chichi              = {result.k_chichi_normalized:.9e}")


if __name__ == "__main__":
    main()

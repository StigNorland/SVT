from __future__ import annotations

from dataclasses import dataclass
import argparse
import math
from typing import Callable

from muon_mode_prototype import SSVScales
from toroidal_background import CurvedToroidalBackground, ToroidalBackground
from toroidal_projection_integrals import ProjectionConfig, integrate_pair
from vortex_profile import VortexProfile


ComplexField = Callable[[float, float], complex]


@dataclass(frozen=True)
class Symmetric2:
    rr: float
    rc: float
    cc: float

    def as_rows(self) -> tuple[tuple[float, float], tuple[float, float]]:
        return ((self.rr, self.rc), (self.rc, self.cc))


@dataclass(frozen=True)
class RestrictedBdGResult:
    k_xx: Symmetric2
    k_yy: Symmetric2
    a_block: Symmetric2
    b_block: Symmetric2
    omega_minus_sq: float
    omega_plus_sq: float
    omega_minus: float
    omega_plus: float


def matmul2(a: Symmetric2 | tuple[tuple[float, float], tuple[float, float]], b: Symmetric2 | tuple[tuple[float, float], tuple[float, float]]) -> tuple[tuple[float, float], tuple[float, float]]:
    ar = a.as_rows() if isinstance(a, Symmetric2) else a
    br = b.as_rows() if isinstance(b, Symmetric2) else b
    return (
        (
            ar[0][0] * br[0][0] + ar[0][1] * br[1][0],
            ar[0][0] * br[0][1] + ar[0][1] * br[1][1],
        ),
        (
            ar[1][0] * br[0][0] + ar[1][1] * br[1][0],
            ar[1][0] * br[0][1] + ar[1][1] * br[1][1],
        ),
    )


def eigvals2(m: tuple[tuple[float, float], tuple[float, float]]) -> tuple[float, float]:
    trace = m[0][0] + m[1][1]
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    disc = trace * trace - 4.0 * det
    if disc < 0.0 and disc > -1.0e-10:
        disc = 0.0
    if disc < 0.0:
        raise ValueError(f"Complex 2x2 eigenvalues in restricted BdG diagnostic: {disc}")
    root = math.sqrt(disc)
    return (0.5 * (trace - root), 0.5 * (trace + root))


def subtract2(a: Symmetric2, b: Symmetric2) -> Symmetric2:
    return Symmetric2(rr=a.rr - b.rr, rc=a.rc - b.rc, cc=a.cc - b.cc)


def add2(a: Symmetric2, b: Symmetric2) -> Symmetric2:
    return Symmetric2(rr=a.rr + b.rr, rc=a.rc + b.rc, cc=a.cc + b.cc)


def scale2(a: Symmetric2, s: float) -> Symmetric2:
    return Symmetric2(rr=s * a.rr, rc=s * a.rc, cc=s * a.cc)


def normalize_k(k: Symmetric2, norm_rr: float, norm_cc: float) -> Symmetric2:
    return Symmetric2(
        rr=k.rr / norm_rr,
        rc=k.rc / math.sqrt(norm_rr * norm_cc),
        cc=k.cc / norm_cc,
    )


def solve_bdg_from_blocks(a_block: Symmetric2, b_block: Symmetric2) -> tuple[float, float, float, float]:
    """Solve the 2-mode bosonic BdG diagnostic.

    For real symmetric A and B, the positive BdG frequencies satisfy

        omega^2 eigs((A-B)(A+B)).

    This is the restricted first-order analogue of the previous oscillator diagnostic.
    """
    a_minus_b = subtract2(a_block, b_block)
    a_plus_b = add2(a_block, b_block)
    omega_sq = eigvals2(matmul2(a_minus_b, a_plus_b))
    return (
        omega_sq[0],
        omega_sq[1],
        math.sqrt(omega_sq[0]) if omega_sq[0] >= 0.0 else float("nan"),
        math.sqrt(omega_sq[1]) if omega_sq[1] >= 0.0 else float("nan"),
    )


def build_background(
    profile: str,
    profile_n: int,
    profile_x_max: float,
    curvature_coeffs: tuple[float, ...],
    phase_coeffs: tuple[float, ...],
) -> ToroidalBackground:
    if profile == "numerical":
        vortex = VortexProfile.solve(n=profile_n, x_max=profile_x_max)
        if curvature_coeffs or phase_coeffs:
            return CurvedToroidalBackground(
                f0=vortex.value,
                f0_prime=vortex.derivative,
                curvature_coeffs=curvature_coeffs,
                phase_coeffs=phase_coeffs,
            )
        return ToroidalBackground(f0=vortex.value, f0_prime=vortex.derivative)
    if curvature_coeffs or phase_coeffs:
        return CurvedToroidalBackground(
            curvature_coeffs=curvature_coeffs,
            phase_coeffs=phase_coeffs,
        )
    return ToroidalBackground()


def build_modes(bg: ToroidalBackground, cfg: ProjectionConfig) -> tuple[ComplexField, ComplexField]:
    mode_r = bg.phi_R
    raw_chi = bg.phi_chi if cfg.chi_parity == "cos" else bg.phi_chi_sin
    if not cfg.orthogonalize_chi:
        return mode_r, raw_chi
    _, _, _, norm_rr = integrate_pair(bg, mode_r, mode_r, cfg)
    _, _, _, norm_rchi = integrate_pair(bg, mode_r, raw_chi, cfg)
    projection = norm_rchi / norm_rr

    def mode_chi(r: float, z: float) -> complex:
        return raw_chi(r, z) - projection * mode_r(r, z)

    return mode_r, mode_chi


def i_mode(mode: ComplexField) -> ComplexField:
    def wrapped(r: float, z: float) -> complex:
        return 1j * mode(r, z)

    return wrapped


def stiffness_matrix(
    bg: ToroidalBackground,
    mode_r: ComplexField,
    mode_chi: ComplexField,
    cfg: ProjectionConfig,
    inner_outer_reference: ComplexField | None = None,
) -> tuple[Symmetric2, float, float]:
    k_rr, kp_rr, kio_rr, norm_rr = integrate_pair(bg, mode_r, mode_r, cfg)
    k_rc, kp_rc, _, _ = integrate_pair(bg, mode_r, mode_chi, cfg)
    k_cc, kp_cc, _, norm_cc = integrate_pair(bg, mode_chi, mode_chi, cfg)
    if inner_outer_reference is not None:
        _, _, kio_rr, _ = integrate_pair(bg, inner_outer_reference, inner_outer_reference, cfg)
    return (
        Symmetric2(
            rr=k_rr + kp_rr + kio_rr,
            rc=k_rc + kp_rc,
            cc=k_cc + kp_cc,
        ),
        norm_rr,
        norm_cc,
    )


def compute_restricted_bdg(cfg: ProjectionConfig) -> RestrictedBdGResult:
    bg = build_background(
        cfg.profile,
        cfg.profile_n,
        cfg.profile_x_max,
        cfg.curvature_coeffs,
        cfg.phase_coeffs,
    )
    mode_r, mode_chi = build_modes(bg, cfg)
    k_xx_raw, norm_rr, norm_cc = stiffness_matrix(
        bg, mode_r, mode_chi, cfg, inner_outer_reference=mode_r
    )
    k_yy_raw, _, _ = stiffness_matrix(
        bg, i_mode(mode_r), i_mode(mode_chi), cfg, inner_outer_reference=mode_r
    )

    k_xx = normalize_k(k_xx_raw, norm_rr, norm_cc)
    k_yy = normalize_k(k_yy_raw, norm_rr, norm_cc)

    # In this restricted diagnostic, A is the average curvature of amplitude and phase
    # quadratures; B is their half-difference. This is the minimal A/B split available
    # from the current projected Hessian machinery.
    a_block = scale2(add2(k_xx, k_yy), 0.5)
    b_block = scale2(subtract2(k_xx, k_yy), 0.5)
    omega_minus_sq, omega_plus_sq, omega_minus, omega_plus = solve_bdg_from_blocks(a_block, b_block)
    return RestrictedBdGResult(
        k_xx=k_xx,
        k_yy=k_yy,
        a_block=a_block,
        b_block=b_block,
        omega_minus_sq=omega_minus_sq,
        omega_plus_sq=omega_plus_sq,
        omega_minus=omega_minus,
        omega_plus=omega_plus,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Restricted 2-mode BdG matrix diagnostic.")
    parser.add_argument("--n", type=int, default=61)
    parser.add_argument("--half-width", type=float, default=6.0)
    parser.add_argument("--chi-parity", choices=("cos", "sin"), default="sin")
    parser.add_argument("--profile", choices=("toy", "numerical"), default="numerical")
    parser.add_argument("--profile-n", type=int, default=2400)
    parser.add_argument("--profile-x-max", type=float, default=20.0)
    parser.add_argument("--no-orthogonalize-chi", action="store_true")
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
        chi_parity=args.chi_parity,
        orthogonalize_chi=not args.no_orthogonalize_chi,
        profile=args.profile,
        profile_n=args.profile_n,
        profile_x_max=args.profile_x_max,
        workers=1,
        curvature_coeffs=curvature_coeffs,
        phase_coeffs=phase_coeffs,
        inner_outer_stiffness=args.inner_outer_stiffness,
    )
    result = compute_restricted_bdg(cfg)
    scales = SSVScales()
    print("Restricted two-mode BdG diagnostic")
    print(f"grid n                   = {cfg.n}")
    print(f"half_width               = {cfg.half_width}")
    print(f"chi_parity               = {cfg.chi_parity}")
    print(f"profile                  = {cfg.profile}")
    print(f"profile_n                = {cfg.profile_n}")
    print(f"curvature_coeffs         = {cfg.curvature_coeffs}")
    print(f"phase_coeffs             = {cfg.phase_coeffs}")
    print(f"inner_outer_stiffness    = {cfg.inner_outer_stiffness:.9e}")
    print("")
    print("Normalized real-amplitude Hessian K_xx")
    print(f"Kxx_RR                   = {result.k_xx.rr:.9e}")
    print(f"Kxx_Rchi                 = {result.k_xx.rc:.9e}")
    print(f"Kxx_chichi               = {result.k_xx.cc:.9e}")
    print("")
    print("Normalized phase-quadrature Hessian K_yy")
    print(f"Kyy_RR                   = {result.k_yy.rr:.9e}")
    print(f"Kyy_Rchi                 = {result.k_yy.rc:.9e}")
    print(f"Kyy_chichi               = {result.k_yy.cc:.9e}")
    print("")
    print("Restricted BdG blocks")
    print(f"A_RR                     = {result.a_block.rr:.9e}")
    print(f"A_Rchi                   = {result.a_block.rc:.9e}")
    print(f"A_chichi                 = {result.a_block.cc:.9e}")
    print(f"B_RR                     = {result.b_block.rr:.9e}")
    print(f"B_Rchi                   = {result.b_block.rc:.9e}")
    print(f"B_chichi                 = {result.b_block.cc:.9e}")
    print("")
    print("BdG eigenvalue diagnostic")
    print(f"omega_minus_sq           = {result.omega_minus_sq:.9e}")
    print(f"omega_plus_sq            = {result.omega_plus_sq:.9e}")
    print(f"omega_minus              = {result.omega_minus:.9e}")
    print(f"omega_plus               = {result.omega_plus:.9e}")
    print("")
    print("Muon target comparison")
    print(f"target omega_mu/omega_c  = {scales.muon_ratio_draft:.9e}")
    if math.isfinite(result.omega_minus):
        print(f"omega_minus / target     = {result.omega_minus / scales.muon_ratio_draft:.9e}")
    else:
        print("omega_minus / target     = non-real lower branch")
    print(f"omega_plus / target      = {result.omega_plus / scales.muon_ratio_draft:.9e}")
    print("")
    print("Caveat")
    print("This is a restricted BdG diagnostic from projected quadrature Hessians.")
    print("The next refinement is direct projection of the differential BdG operator L/M.")


if __name__ == "__main__":
    main()

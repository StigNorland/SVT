from __future__ import annotations

from dataclasses import dataclass
import argparse
import math

from muon_mode_prototype import SSVScales
from toroidal_projection_integrals import ProjectionConfig, ProjectionResult, compute_projection_integrals


@dataclass(frozen=True)
class Matrix2:
    aa: float
    ab: float
    bb: float

    def determinant(self) -> float:
        return self.aa * self.bb - self.ab * self.ab


@dataclass(frozen=True)
class GeneralizedEigenResult:
    lambda_minus: float
    lambda_plus: float
    omega_minus: float
    omega_plus: float


def solve_generalized_2x2(k: Matrix2, n: Matrix2) -> GeneralizedEigenResult:
    """Solve det(K - lambda N)=0 for symmetric 2x2 K and N.

    Here lambda = omega^2 in the provisional oscillator interpretation.
    """
    a = n.determinant()
    b = -(
        k.aa * n.bb
        + k.bb * n.aa
        - 2.0 * k.ab * n.ab
    )
    c = k.determinant()
    if abs(a) < 1.0e-300:
        raise ValueError("Norm matrix is singular; cannot solve generalized eigenproblem.")

    discriminant = b * b - 4.0 * a * c
    if discriminant < 0.0 and discriminant > -1.0e-10:
        discriminant = 0.0
    if discriminant < 0.0:
        raise ValueError(f"Complex generalized eigenvalues: discriminant={discriminant}")

    root = math.sqrt(discriminant)
    lam1 = (-b - root) / (2.0 * a)
    lam2 = (-b + root) / (2.0 * a)
    lambda_minus = min(lam1, lam2)
    lambda_plus = max(lam1, lam2)
    omega_minus = math.sqrt(lambda_minus) if lambda_minus >= 0.0 else float("nan")
    omega_plus = math.sqrt(lambda_plus) if lambda_plus >= 0.0 else float("nan")
    return GeneralizedEigenResult(
        lambda_minus=lambda_minus,
        lambda_plus=lambda_plus,
        omega_minus=omega_minus,
        omega_plus=omega_plus,
    )


def matrices_from_projection(result: ProjectionResult) -> tuple[Matrix2, Matrix2]:
    k = Matrix2(
        aa=result.k_rr,
        ab=result.k_rchi,
        bb=result.k_chichi,
    )
    n = Matrix2(
        aa=result.norm_rr,
        ab=result.norm_rchi,
        bb=result.norm_chichi,
    )
    return k, n


def normalized_matrices_from_projection(result: ProjectionResult) -> tuple[Matrix2, Matrix2]:
    k = Matrix2(
        aa=result.k_rr_normalized,
        ab=result.k_rchi_normalized,
        bb=result.k_chichi_normalized,
    )
    n = Matrix2(aa=1.0, ab=0.0, bb=1.0)
    return k, n


def format_summary(
    cfg: ProjectionConfig,
    projection: ProjectionResult,
    raw_eigs: GeneralizedEigenResult,
    normalized_eigs: GeneralizedEigenResult,
) -> str:
    scales = SSVScales()
    lines = [
        "Projected two-mode eigenvalue diagnostic",
        f"grid n                   = {cfg.n}",
        f"half_width               = {cfg.half_width}",
        f"chi_parity               = {cfg.chi_parity}",
        f"orthogonalize_chi        = {cfg.orthogonalize_chi}",
        f"profile                  = {cfg.profile}",
        f"profile_n                = {cfg.profile_n}",
        f"workers                  = {cfg.workers}",
        "",
        "Raw projected matrices",
        f"K = [[{projection.k_rr:.9e}, {projection.k_rchi:.9e}],",
        f"     [{projection.k_rchi:.9e}, {projection.k_chichi:.9e}]]",
        f"N = [[{projection.norm_rr:.9e}, {projection.norm_rchi:.9e}],",
        f"     [{projection.norm_rchi:.9e}, {projection.norm_chichi:.9e}]]",
        "",
        "Normalized stiffness matrix",
        f"Khat_RR                  = {projection.k_rr_normalized:.9e}",
        f"Khat_Rchi                = {projection.k_rchi_normalized:.9e}",
        f"Khat_chichi              = {projection.k_chichi_normalized:.9e}",
        "",
        "Generalized eigenvalues from raw K X = omega^2 N X",
        f"lambda_minus             = {raw_eigs.lambda_minus:.9e}",
        f"lambda_plus              = {raw_eigs.lambda_plus:.9e}",
        f"omega_minus              = {raw_eigs.omega_minus:.9e}",
        f"omega_plus               = {raw_eigs.omega_plus:.9e}",
        "",
        "Eigenvalues from normalized Khat",
        f"lambda_minus_hat         = {normalized_eigs.lambda_minus:.9e}",
        f"lambda_plus_hat          = {normalized_eigs.lambda_plus:.9e}",
        f"omega_minus_hat          = {normalized_eigs.omega_minus:.9e}",
        f"omega_plus_hat           = {normalized_eigs.omega_plus:.9e}",
        "",
        "Muon target comparison",
        f"target omega_mu/omega_c  = {scales.muon_ratio_draft:.9e}",
        f"omega_minus_hat / target = {normalized_eigs.omega_minus / scales.muon_ratio_draft:.9e}",
        f"omega_plus_hat / target  = {normalized_eigs.omega_plus / scales.muon_ratio_draft:.9e}",
        "",
        "Interpretation caveat",
        "This uses a real L2 norm as the provisional mass matrix. The full BdG problem needs",
        "the symplectic norm and u/v fluctuation basis before these can be physical frequencies.",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and solve the projected two-mode eigenvalue diagnostic."
    )
    parser.add_argument("--n", type=int, default=101)
    parser.add_argument("--half-width", type=float, default=6.0)
    parser.add_argument("--chi-parity", choices=("cos", "sin"), default="sin")
    parser.add_argument("--profile", choices=("toy", "numerical"), default="numerical")
    parser.add_argument("--profile-n", type=int, default=4000)
    parser.add_argument("--profile-x-max", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--no-orthogonalize-chi", action="store_true")
    parser.add_argument(
        "--inner-outer-stiffness",
        type=float,
        default=0.0,
        help="Dimensionless localized inner/outer breathing-strain stiffness coefficient.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        chi_parity=args.chi_parity,
        orthogonalize_chi=not args.no_orthogonalize_chi,
        profile=args.profile,
        profile_n=args.profile_n,
        profile_x_max=args.profile_x_max,
        workers=args.workers,
        inner_outer_stiffness=args.inner_outer_stiffness,
    )
    projection = compute_projection_integrals(cfg)
    raw_k, raw_n = matrices_from_projection(projection)
    raw_eigs = solve_generalized_2x2(raw_k, raw_n)
    normalized_k, normalized_n = normalized_matrices_from_projection(projection)
    normalized_eigs = solve_generalized_2x2(normalized_k, normalized_n)
    print(format_summary(cfg, projection, raw_eigs, normalized_eigs))


if __name__ == "__main__":
    main()

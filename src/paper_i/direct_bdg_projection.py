from __future__ import annotations

import argparse
import cmath
import math
from dataclasses import dataclass
from typing import Callable

from restricted_bdg_three_mode import complex_inner, gram_schmidt
from toroidal_background import ToroidalBackground
from toroidal_projection_integrals import ProjectionConfig, integrate_pair
from vortex_profile import VortexProfile


ComplexField = Callable[[float, float], complex]
ComplexMatrix = list[list[complex]]


@dataclass(frozen=True)
class DirectBdGResult:
    h: ComplexMatrix
    eigs: list[complex]


def parse_coeffs(raw: str) -> tuple[float, ...]:
    return tuple(float(part) for part in raw.split(",") if part.strip()) if raw.strip() else ()


def central_laplacian_cyl(field: ComplexField, r: float, z: float, h: float) -> complex:
    d2_r = (field(r + h, z) - 2.0 * field(r, z) + field(r - h, z)) / (h * h)
    d_r = (field(r + h, z) - field(r - h, z)) / (2.0 * h)
    d2_z = (field(r, z + h) - 2.0 * field(r, z) + field(r, z - h)) / (h * h)
    return d2_r + d_r / max(r, 1.0e-12) + d2_z


def background_phase(bg: ToroidalBackground, r: float, z: float) -> complex:
    psi = bg.psi0(r, z)
    amp = abs(psi)
    if amp < 1.0e-14:
        return 1.0 + 0.0j
    return psi / amp


def l_operator(
    bg: ToroidalBackground,
    field: ComplexField,
    r: float,
    z: float,
    cfg: ProjectionConfig,
    operator_model: str,
) -> complex:
    psi = bg.psi0(r, z)
    amp_sq = max(abs(psi) ** 2, 1.0e-12)
    lap = central_laplacian_cyl(field, r, z, cfg.dr)

    if operator_model == "provisional":
        v_amp = 2.0 * (1.0 - amp_sq)
        return -0.5 * lap + v_amp * field(r, z)

    # Profile-matched LogSE model. The numerical f0 profile solves
    #   f'' + r^-1 f' - r^-2 f - 2 f log(f^2) = 0,
    # equivalent to the stationary equation
    #   -1/2 ∇²ψ + log(|ψ|²)ψ = 0.
    # For iψ_t = -1/2∇²ψ + g(n)ψ with g(n)=log(n), the BdG diagonal
    # coefficient is g(n)+n g'(n)=log(n)+1.
    return -0.5 * lap + (math.log(amp_sq) + 1.0) * field(r, z)


def m_operator(
    bg: ToroidalBackground,
    field: ComplexField,
    r: float,
    z: float,
    cfg: ProjectionConfig,
    operator_model: str,
) -> complex:
    psi = bg.psi0(r, z)
    amp_sq = max(abs(psi) ** 2, 1.0e-12)
    phase_sq = background_phase(bg, r, z) ** 2

    if operator_model == "provisional":
        v_pair = -2.0 * (1.0 - amp_sq)
        return v_pair * phase_sq * field(r, z)

    # For g(n)=log(n), g'(n)=1/n, hence ψ0² g'(n)=e^{2iΘ}.
    return phase_sq * field(r, z)


def project_operator(
    bg: ToroidalBackground,
    bra: ComplexField,
    op_field: ComplexField,
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
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz
            total += weight * bra(r, z).conjugate() * op_field(r, z)
    return total


def norm(bg: ToroidalBackground, mode: ComplexField, cfg: ProjectionConfig) -> float:
    return complex_inner(bg, mode, mode, cfg).real


def normalized_modes(bg: ToroidalBackground, modes: list[ComplexField], cfg: ProjectionConfig) -> list[ComplexField]:
    out = []
    for mode in modes:
        n = norm(bg, mode, cfg)
        scale = 1.0 / math.sqrt(abs(n))

        def make_scaled(fn: ComplexField, factor: float) -> ComplexField:
            def scaled(r: float, z: float) -> complex:
                return factor * fn(r, z)

            return scaled

        out.append(make_scaled(mode, scale))
    return out


def build_background(cfg: ProjectionConfig) -> ToroidalBackground:
    if cfg.profile == "numerical":
        profile = VortexProfile.solve(n=cfg.profile_n, x_max=cfg.profile_x_max)
        return ToroidalBackground(f0=profile.value, f0_prime=profile.derivative)
    return ToroidalBackground()


def build_basis(bg: ToroidalBackground, cfg: ProjectionConfig, basis: str) -> list[ComplexField]:
    chi = bg.phi_chi_sin
    if basis == "two":
        seeds = [bg.phi_R, chi]
    else:
        seeds = [bg.phi_R, chi, bg.phi_momentum, i_mode(chi)]
    modes = gram_schmidt(bg, seeds, cfg)
    return normalized_modes(bg, modes, cfg)


def i_mode(mode: ComplexField) -> ComplexField:
    def wrapped(r: float, z: float) -> complex:
        return 1j * mode(r, z)

    return wrapped


def build_direct_bdg_matrix(
    bg: ToroidalBackground,
    modes: list[ComplexField],
    cfg: ProjectionConfig,
    operator_model: str,
    include_projected_chiral: bool,
) -> ComplexMatrix:
    n = len(modes)
    size = 2 * n
    h = [[0.0j for _ in range(size)] for _ in range(size)]

    for i, bra in enumerate(modes):
        for j, ket in enumerate(modes):
            def l_ket(r: float, z: float, fn=ket) -> complex:
                return l_operator(bg, fn, r, z, cfg, operator_model)

            def m_ket(r: float, z: float, fn=ket) -> complex:
                return m_operator(bg, fn, r, z, cfg, operator_model)

            l_ij = project_operator(bg, bra, l_ket, cfg)
            m_ij = project_operator(bg, bra, m_ket, cfg)
            if include_projected_chiral:
                _, kp_ij, _, _ = integrate_pair(bg, bra, ket, cfg)
                l_ij += kp_ij
            h[i][j] = l_ij
            h[i][j + n] = m_ij
            h[i + n][j] = -m_ij.conjugate()
            h[i + n][j + n] = -l_ij.conjugate()
    return h


def qr_decompose(a: ComplexMatrix) -> tuple[ComplexMatrix, ComplexMatrix]:
    n = len(a)
    q_cols: list[list[complex]] = []
    r = [[0.0j for _ in range(n)] for _ in range(n)]
    cols = [[a[i][j] for i in range(n)] for j in range(n)]
    for j, col in enumerate(cols):
        v = col[:]
        for i, qi in enumerate(q_cols):
            rij = sum(qi[k].conjugate() * v[k] for k in range(n))
            r[i][j] = rij
            v = [v[k] - rij * qi[k] for k in range(n)]
        norm_v = math.sqrt(sum(abs(value) ** 2 for value in v))
        if norm_v < 1.0e-14:
            q_cols.append([0.0j for _ in range(n)])
        else:
            q_cols.append([value / norm_v for value in v])
            r[j][j] = norm_v
    q = [[q_cols[j][i] for j in range(n)] for i in range(n)]
    return q, r


def complex_matmul(a: ComplexMatrix, b: ComplexMatrix) -> ComplexMatrix:
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def qr_eigenvalues(a: ComplexMatrix, iterations: int = 4000) -> list[complex]:
    m = [[complex(value) for value in row] for row in a]
    n = len(m)
    for _ in range(iterations):
        shift = m[n - 1][n - 1]
        shifted = [[m[i][j] - (shift if i == j else 0.0) for j in range(n)] for i in range(n)]
        q, r = qr_decompose(shifted)
        m = complex_matmul(r, q)
        for i in range(n):
            m[i][i] += shift
    return [m[i][i] for i in range(n)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Direct restricted BdG L/M projection diagnostic.")
    parser.add_argument("--n", type=int, default=31)
    parser.add_argument("--half-width", type=float, default=4.0)
    parser.add_argument("--profile", choices=("toy", "numerical"), default="numerical")
    parser.add_argument("--profile-n", type=int, default=1200)
    parser.add_argument("--profile-x-max", type=float, default=20.0)
    parser.add_argument(
        "--operator-model",
        choices=("profile-logse", "provisional"),
        default="profile-logse",
        help="Local BdG L/M coefficient model.",
    )
    parser.add_argument(
        "--include-projected-chiral",
        action="store_true",
        help="Add projected chiral-shear Hessian contribution to the L block.",
    )
    parser.add_argument(
        "--basis",
        choices=("two", "four"),
        default="two",
        help="Restricted u/v basis: two=(R,chi), four=(R,chi,P_R,P_chi).",
    )
    return parser.parse_args()


def print_matrix(name: str, m: ComplexMatrix) -> None:
    print(name)
    for row in m:
        print("  " + " ".join(f"{v.real: .6e}{v.imag:+.2e}i" for v in row))


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
    bg = build_background(cfg)
    modes = build_basis(bg, cfg, args.basis)
    h = build_direct_bdg_matrix(
        bg,
        modes,
        cfg,
        args.operator_model,
        include_projected_chiral=args.include_projected_chiral,
    )
    eigs = qr_eigenvalues(h)
    print("Direct restricted BdG L/M projection")
    print(f"grid n                   = {cfg.n}")
    print(f"half_width               = {cfg.half_width}")
    print(f"profile                  = {cfg.profile}")
    print(f"profile_n                = {cfg.profile_n}")
    print(f"operator_model           = {args.operator_model}")
    print(f"include_projected_chiral = {args.include_projected_chiral}")
    print(f"basis                    = {args.basis}")
    print_matrix("H_BdG", h)
    print("Eigenvalues")
    for value in sorted(eigs, key=lambda z: z.real):
        print(f"  {value.real:.9e} {value.imag:+.9e}i")


if __name__ == "__main__":
    main()

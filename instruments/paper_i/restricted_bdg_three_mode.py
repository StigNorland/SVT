from __future__ import annotations

import argparse
import cmath
import math
from dataclasses import dataclass
from typing import Callable

# Note (2026-05-30 cleanup): import of SSVScales removed; it was used only for
# the fitted muon target `muon_ratio_draft = 0.207` (now quarantined in
# instruments/_fitted_quarantine/). See papers/SSV-I/path-b-eigenvalue-result.md.
from restricted_bdg_matrix import build_background, i_mode
from toroidal_projection_integrals import ProjectionConfig, integrate_pair, projection_window_weight


ComplexField = Callable[[float, float], complex]
Matrix = list[list[float]]


@dataclass(frozen=True)
class ThreeModeResult:
    k_xx: Matrix
    k_yy: Matrix
    symplectic: Matrix
    a_block: Matrix
    b_block: Matrix
    omega_sq: list[float]
    omega: list[float]


def zero_matrix(n: int) -> Matrix:
    return [[0.0 for _ in range(n)] for _ in range(n)]


def add_matrix(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]


def sub_matrix(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a))] for i in range(len(a))]


def scale_matrix(a: Matrix, s: float) -> Matrix:
    return [[s * a[i][j] for j in range(len(a))] for i in range(len(a))]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [
        [sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def trace(a: Matrix) -> float:
    return sum(a[i][i] for i in range(len(a)))


def det3(m: Matrix) -> float:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def cubic_roots_real_for_3x3(m: Matrix) -> list[float]:
    tr = trace(m)
    m2 = matmul(m, m)
    c2 = 0.5 * (tr * tr - trace(m2))
    c3 = det3(m)

    # Characteristic polynomial: lambda^3 - tr lambda^2 + c2 lambda - c3 = 0.
    a = -tr
    b = c2
    c = -c3
    p = b - a * a / 3.0
    q = 2.0 * a * a * a / 27.0 - a * b / 3.0 + c
    disc = (q / 2.0) ** 2 + (p / 3.0) ** 3

    roots: list[complex] = []
    if disc >= 0.0:
        sqrt_disc = math.sqrt(disc)
        u = complex(-q / 2.0 + sqrt_disc) ** (1.0 / 3.0)
        v = complex(-q / 2.0 - sqrt_disc) ** (1.0 / 3.0)
        omega = complex(-0.5, math.sqrt(3.0) / 2.0)
        for factor in (1.0 + 0j, omega, omega * omega):
            roots.append(factor * u + factor.conjugate() * v - a / 3.0)
    else:
        radius = 2.0 * math.sqrt(-p / 3.0)
        angle = math.acos((3.0 * q / (2.0 * p)) * math.sqrt(-3.0 / p)) / 3.0
        for k in range(3):
            roots.append(radius * math.cos(angle - 2.0 * math.pi * k / 3.0) - a / 3.0)

    real_roots = []
    for root in roots:
        if isinstance(root, complex):
            if abs(root.imag) < 1.0e-7:
                real_roots.append(root.real)
            else:
                # Keep real part but mark complex behavior by preserving ordering impact.
                real_roots.append(root.real)
        else:
            real_roots.append(root)
    return sorted(real_roots)


def linear_combination(terms: list[tuple[float, ComplexField]]) -> ComplexField:
    def mode(r: float, z: float) -> complex:
        return sum(coeff * fn(r, z) for coeff, fn in terms)

    return mode


def norm(bg, a: ComplexField, b: ComplexField, cfg: ProjectionConfig) -> float:
    _, _, _, n_ab = integrate_pair(bg, a, b, cfg)
    return n_ab


def complex_inner(bg, a: ComplexField, b: ComplexField, cfg: ProjectionConfig) -> complex:
    total = 0.0j
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz * projection_window_weight(bg, r, z, cfg)
            total += weight * a(r, z).conjugate() * b(r, z)
    return total


def symplectic_matrix(bg, modes: list[ComplexField], cfg: ProjectionConfig, norms: list[float]) -> Matrix:
    n = len(modes)
    s = zero_matrix(n)
    for i in range(n):
        for j in range(n):
            overlap = complex_inner(bg, modes[i], modes[j], cfg)
            s[i][j] = 2.0 * overlap.imag / math.sqrt(norms[i] * norms[j])
    return s


def gram_schmidt(bg, modes: list[ComplexField], cfg: ProjectionConfig) -> list[ComplexField]:
    orthogonal: list[ComplexField] = []
    for mode in modes:
        terms: list[tuple[float, ComplexField]] = [(1.0, mode)]
        for prev in orthogonal:
            denom = norm(bg, prev, prev, cfg)
            if abs(denom) < 1.0e-14:
                continue
            projection = norm(bg, prev, linear_combination(terms), cfg) / denom
            terms.append((-projection, prev))
        orthogonal.append(linear_combination(terms))
    return orthogonal


def stiffness_matrix(bg, modes: list[ComplexField], cfg: ProjectionConfig, kio_rr: float = 0.0) -> tuple[Matrix, list[float]]:
    n_modes = len(modes)
    k = zero_matrix(n_modes)
    norms = [0.0 for _ in range(n_modes)]
    cfg_no_io = ProjectionConfig(
        n=cfg.n,
        half_width=cfg.half_width,
        chi_parity=cfg.chi_parity,
        orthogonalize_chi=cfg.orthogonalize_chi,
        profile=cfg.profile,
        profile_n=cfg.profile_n,
        profile_x_max=cfg.profile_x_max,
        workers=1,
        curvature_coeffs=cfg.curvature_coeffs,
        phase_coeffs=cfg.phase_coeffs,
        inner_outer_stiffness=0.0,
        projection_window=cfg.projection_window,
        window_radius=cfg.window_radius,
        window_taper=cfg.window_taper,
    )
    for i in range(n_modes):
        for j in range(i, n_modes):
            k0, kp, _, n_ij = integrate_pair(bg, modes[i], modes[j], cfg_no_io)
            value = k0 + kp
            k[i][j] = value
            k[j][i] = value
            if i == j:
                norms[i] = n_ij
    k[0][0] += kio_rr
    return k, norms


def normalize_matrix(k: Matrix, norms: list[float]) -> Matrix:
    n = len(k)
    return [
        [k[i][j] / math.sqrt(norms[i] * norms[j]) for j in range(n)]
        for i in range(n)
    ]


def compute_three_mode_bdg(cfg: ProjectionConfig) -> ThreeModeResult:
    bg = build_background(
        cfg.profile,
        cfg.profile_n,
        cfg.profile_x_max,
        cfg.curvature_coeffs,
        cfg.phase_coeffs,
    )
    seed_modes = [bg.phi_R, bg.phi_chi_sin if cfg.chi_parity == "sin" else bg.phi_chi, bg.phi_momentum]
    modes = gram_schmidt(bg, seed_modes, cfg)
    _, _, kio_rr, _ = integrate_pair(bg, bg.phi_R, bg.phi_R, cfg)

    k_xx_raw, norms = stiffness_matrix(bg, modes, cfg, kio_rr=kio_rr)
    k_yy_raw, _ = stiffness_matrix(bg, [i_mode(mode) for mode in modes], cfg, kio_rr=kio_rr)
    k_xx = normalize_matrix(k_xx_raw, norms)
    k_yy = normalize_matrix(k_yy_raw, norms)
    symplectic = symplectic_matrix(bg, modes, cfg, norms)
    a_block = scale_matrix(add_matrix(k_xx, k_yy), 0.5)
    b_block = scale_matrix(sub_matrix(k_xx, k_yy), 0.5)
    omega_sq = cubic_roots_real_for_3x3(matmul(sub_matrix(a_block, b_block), add_matrix(a_block, b_block)))
    omega = [math.sqrt(value) if value >= 0.0 else float("nan") for value in omega_sq]
    return ThreeModeResult(
        k_xx=k_xx,
        k_yy=k_yy,
        symplectic=symplectic,
        a_block=a_block,
        b_block=b_block,
        omega_sq=omega_sq,
        omega=omega,
    )


def parse_coeffs(raw: str) -> tuple[float, ...]:
    return tuple(float(part) for part in raw.split(",") if part.strip()) if raw.strip() else ()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Restricted 3-mode BdG diagnostic with conjugate momentum seed.")
    parser.add_argument("--n", type=int, default=31)
    parser.add_argument("--half-width", type=float, default=4.0)
    parser.add_argument("--chi-parity", choices=("cos", "sin"), default="sin")
    parser.add_argument("--profile", choices=("toy", "numerical"), default="numerical")
    parser.add_argument("--profile-n", type=int, default=1200)
    parser.add_argument("--profile-x-max", type=float, default=20.0)
    parser.add_argument("--curvature-coeffs", default="")
    parser.add_argument("--phase-coeffs", default="")
    parser.add_argument("--inner-outer-stiffness", type=float, default=0.0)
    return parser.parse_args()


def print_matrix(name: str, m: Matrix) -> None:
    print(name)
    for row in m:
        print("  " + " ".join(f"{value: .9e}" for value in row))


def main() -> None:
    args = parse_args()
    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        chi_parity=args.chi_parity,
        profile=args.profile,
        profile_n=args.profile_n,
        profile_x_max=args.profile_x_max,
        curvature_coeffs=parse_coeffs(args.curvature_coeffs),
        phase_coeffs=parse_coeffs(args.phase_coeffs),
        inner_outer_stiffness=args.inner_outer_stiffness,
    )
    result = compute_three_mode_bdg(cfg)
    print("Restricted three-mode BdG diagnostic: R, chi, P")
    print(f"grid n                   = {cfg.n}")
    print(f"half_width               = {cfg.half_width}")
    print(f"profile                  = {cfg.profile}")
    print(f"profile_n                = {cfg.profile_n}")
    print(f"inner_outer_stiffness    = {cfg.inner_outer_stiffness:.9e}")
    print_matrix("K_xx", result.k_xx)
    print_matrix("K_yy", result.k_yy)
    print_matrix("S = 2 Im <mode_i|mode_j>", result.symplectic)
    print_matrix("A", result.a_block)
    print_matrix("B", result.b_block)
    print("BdG omega^2")
    for i, value in enumerate(result.omega_sq):
        print(f"omega_sq[{i}]            = {value:.9e}")
    print("BdG omega")
    for i, value in enumerate(result.omega):
        print(f"omega[{i}]               = {value:.9e}")


if __name__ == "__main__":
    main()

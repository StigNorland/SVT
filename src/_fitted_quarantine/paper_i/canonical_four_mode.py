from __future__ import annotations

import argparse
import cmath
import math

from muon_mode_prototype import SSVScales
from restricted_bdg_matrix import build_background, i_mode
from restricted_bdg_three_mode import (
    Matrix,
    complex_inner,
    gram_schmidt,
    normalize_matrix,
    stiffness_matrix,
    symplectic_matrix,
)
from toroidal_projection_integrals import ProjectionConfig


def parse_coeffs(raw: str) -> tuple[float, ...]:
    return tuple(float(part) for part in raw.split(",") if part.strip()) if raw.strip() else ()


def mat_vec(a: Matrix, x: list[complex]) -> list[complex]:
    return [sum(a[i][j] * x[j] for j in range(len(x))) for i in range(len(x))]


def invert_matrix(a: Matrix) -> Matrix:
    n = len(a)
    mat = [[float(a[i][j]) for j in range(n)] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(mat[r][col]))
        if abs(mat[pivot][col]) < 1.0e-12:
            raise ValueError("Matrix is singular or nearly singular.")
        mat[col], mat[pivot] = mat[pivot], mat[col]
        pivot_value = mat[col][col]
        for j in range(2 * n):
            mat[col][j] /= pivot_value
        for r in range(n):
            if r == col:
                continue
            factor = mat[r][col]
            for j in range(2 * n):
                mat[r][j] -= factor * mat[col][j]
    return [row[n:] for row in mat]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def qr_decompose(a: list[list[complex]]) -> tuple[list[list[complex]], list[list[complex]]]:
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
        norm = math.sqrt(sum(abs(value) ** 2 for value in v))
        if norm < 1.0e-14:
            q_cols.append([0.0j for _ in range(n)])
        else:
            q_cols.append([value / norm for value in v])
            r[j][j] = norm
    q = [[q_cols[j][i] for j in range(n)] for i in range(n)]
    return q, r


def complex_matmul(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def qr_eigenvalues(a: Matrix, iterations: int = 4000) -> list[complex]:
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


def print_matrix(name: str, m: Matrix) -> None:
    print(name)
    for row in m:
        print("  " + " ".join(f"{value: .9e}" for value in row))


def build_four_mode_matrices(cfg: ProjectionConfig) -> tuple[Matrix, Matrix, list[float]]:
    bg = build_background(
        cfg.profile,
        cfg.profile_n,
        cfg.profile_x_max,
        cfg.curvature_coeffs,
        cfg.phase_coeffs,
    )
    chi_seed = bg.phi_chi_sin if cfg.chi_parity == "sin" else bg.phi_chi
    seeds = [bg.phi_R, chi_seed, bg.phi_momentum, i_mode(chi_seed)]
    modes = gram_schmidt(bg, seeds, cfg)
    k_raw, norms = stiffness_matrix(bg, modes, cfg, kio_rr=0.0)
    k = normalize_matrix(k_raw, norms)
    s = symplectic_matrix(bg, modes, cfg, norms)
    return k, s, norms


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Canonical four-mode diagnostic: R, chi, P_R, P_chi.")
    parser.add_argument("--n", type=int, default=31)
    parser.add_argument("--half-width", type=float, default=4.0)
    parser.add_argument("--profile", choices=("toy", "numerical"), default="numerical")
    parser.add_argument("--profile-n", type=int, default=1200)
    parser.add_argument("--profile-x-max", type=float, default=20.0)
    parser.add_argument("--curvature-coeffs", default="")
    parser.add_argument("--phase-coeffs", default="")
    parser.add_argument("--inner-outer-stiffness", type=float, default=0.0)
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
        curvature_coeffs=parse_coeffs(args.curvature_coeffs),
        phase_coeffs=parse_coeffs(args.phase_coeffs),
        inner_outer_stiffness=args.inner_outer_stiffness,
    )
    k, s, _ = build_four_mode_matrices(cfg)
    scales = SSVScales()

    print("Canonical four-mode diagnostic: R, chi, P_R, P_chi")
    print(f"grid n                   = {cfg.n}")
    print(f"half_width               = {cfg.half_width}")
    print(f"profile                  = {cfg.profile}")
    print(f"profile_n                = {cfg.profile_n}")
    print_matrix("K", k)
    print_matrix("S", s)
    try:
        s_inv = invert_matrix(s)
    except ValueError as exc:
        print(f"Cannot invert S: {exc}")
        return
    generator = matmul(s_inv, k)
    eigenvalues = qr_eigenvalues(generator)
    freqs = sorted(abs(value.imag) for value in eigenvalues if abs(value.imag) > 1.0e-6)
    print_matrix("Generator S^-1 K", generator)
    print("Eigenvalues of S^-1 K")
    for value in eigenvalues:
        print(f"  {value.real:.9e} {value.imag:+.9e}i")
    print("Frequencies |Im eigenvalue|")
    for value in freqs:
        print(f"  {value:.9e}")
    print(f"target omega_mu/omega_c  = {scales.muon_ratio_draft:.9e}")
    if freqs:
        closest = min(freqs, key=lambda value: abs(value - scales.muon_ratio_draft))
        print(f"closest/target           = {closest / scales.muon_ratio_draft:.9e}")


if __name__ == "__main__":
    main()

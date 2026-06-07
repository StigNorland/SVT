"""Reduced curved-torus relaxation check for the Paper I static branch.

Status: validation
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1
Primary observables: reduced-basis relaxation coefficients and energy response
Primary role: small-basis validation asset for issue #12, not closure-grade evidence for #13
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import cmath
import math

from toroidal_background import ALPHA, ToroidalBackground
from vortex_profile import VortexProfile


@dataclass(frozen=True)
class RelaxationConfig:
    n: int = 81
    half_width: float = 6.0
    profile_n: int = 3000
    profile_x_max: float = 20.0
    alpha: float = ALPHA
    xi: float = 1.0
    lambda_chiral: float | None = None
    finite_diff_step: float = 0.25

    @property
    def dr(self) -> float:
        return 2.0 * self.half_width / self.n

    @property
    def dz(self) -> float:
        return self.dr


def basis_values(x: float) -> list[float]:
    """Smooth curvature-correction basis functions.

    The x^2 factor makes alpha*f1*cos(theta)*exp(i theta) regular at the vortex core.
    """
    scales = (1.0, 2.0, 4.0)
    return [(x * x) * math.exp(-x / scale) for scale in scales]


def solve_linear_system(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    mat = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(mat[r][col]))
        if abs(mat[pivot][col]) < 1.0e-14:
            raise ValueError("Singular Hessian in curved torus relaxation.")
        mat[col], mat[pivot] = mat[pivot], mat[col]
        pivot_val = mat[col][col]
        for j in range(col, n + 1):
            mat[col][j] /= pivot_val
        for r in range(n):
            if r == col:
                continue
            factor = mat[r][col]
            for j in range(col, n + 1):
                mat[r][j] -= factor * mat[col][j]
    return [mat[i][n] for i in range(n)]


class CurvedTorusAnsatz:
    def __init__(
        self,
        bg: ToroidalBackground,
        amp_coeffs: list[float],
        phase_coeffs: list[float],
        alpha: float = ALPHA,
    ):
        self.bg = bg
        self.amp_coeffs = amp_coeffs
        self.phase_coeffs = phase_coeffs
        self.alpha = alpha

    def f1(self, x: float) -> float:
        return sum(c * b for c, b in zip(self.amp_coeffs, basis_values(x)))

    def g1(self, x: float) -> float:
        return sum(c * b for c, b in zip(self.phase_coeffs, basis_values(x)))

    def psi(self, r: float, z: float) -> complex:
        s = self.bg.s(r, z)
        theta = self.bg.theta(r, z)
        x = s / self.bg.xi
        amp = self.bg.f0(x) + self.alpha * self.f1(x) * math.cos(theta)
        phase = theta + self.alpha * self.g1(x) * math.sin(theta)
        return amp * cmath.exp(1j * phase)


def central_gradient(field, r: float, z: float, step: float) -> tuple[complex, complex]:
    d_r = (field(r + step, z) - field(r - step, z)) / (2.0 * step)
    d_z = (field(r, z + step) - field(r, z - step)) / (2.0 * step)
    return d_r, d_z


def potential_u(abs_psi_sq: float) -> float:
    if abs_psi_sq <= 1.0e-300:
        return 1.0
    return abs_psi_sq * math.log(abs_psi_sq) - abs_psi_sq + 1.0


def current(field, r: float, z: float, step: float) -> tuple[float, float]:
    psi = field(r, z)
    grad = central_gradient(field, r, z, step)
    j_r = ((psi.conjugate() * grad[0] - psi * grad[0].conjugate()) / (2j)).real
    j_z = ((psi.conjugate() * grad[1] - psi * grad[1].conjugate()) / (2j)).real
    return j_r, j_z


def curl_current(field, r: float, z: float, step: float) -> float:
    d_jr_dz = (current(field, r, z + step, step)[0] - current(field, r, z - step, step)[0]) / (
        2.0 * step
    )
    d_jz_dr = (current(field, r + step, z, step)[1] - current(field, r - step, z, step)[1]) / (
        2.0 * step
    )
    return d_jr_dz - d_jz_dr


def split_coeffs(coeffs: list[float]) -> tuple[list[float], list[float]]:
    dim = len(basis_values(1.0))
    return coeffs[:dim], coeffs[dim:]


def torus_energy(bg: ToroidalBackground, coeffs: list[float], cfg: RelaxationConfig) -> float:
    amp_coeffs, phase_coeffs = split_coeffs(coeffs)
    ansatz = CurvedTorusAnsatz(bg, amp_coeffs, phase_coeffs, alpha=cfg.alpha)
    field = ansatz.psi
    lam = cfg.lambda_chiral
    if lam is None:
        lam = cfg.alpha * cfg.alpha

    energy = 0.0
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            psi = field(r, z)
            grad = central_gradient(field, r, z, cfg.dr)
            grad_energy = 0.5 * (abs(grad[0]) ** 2 + abs(grad[1]) ** 2)
            pot_energy = potential_u(abs(psi) ** 2)
            curl = curl_current(field, r, z, cfg.dr)
            chiral_energy = 0.5 * lam * curl * curl
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz
            energy += weight * (grad_energy + pot_energy + chiral_energy)
    return energy


def quadratic_relaxation(bg: ToroidalBackground, cfg: RelaxationConfig) -> tuple[list[float], dict[str, float]]:
    dim = 2 * len(basis_values(1.0))
    h = cfg.finite_diff_step
    zero = [0.0] * dim
    e0 = torus_energy(bg, zero, cfg)

    gradients = []
    for i in range(dim):
        plus = zero[:]
        minus = zero[:]
        plus[i] = h
        minus[i] = -h
        e_plus = torus_energy(bg, plus, cfg)
        e_minus = torus_energy(bg, minus, cfg)
        gradients.append((e_plus - e_minus) / (2.0 * h))

    hessian = [[0.0 for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        plus = zero[:]
        minus = zero[:]
        plus[i] = h
        minus[i] = -h
        e_plus = torus_energy(bg, plus, cfg)
        e_minus = torus_energy(bg, minus, cfg)
        hessian[i][i] = (e_plus - 2.0 * e0 + e_minus) / (h * h)

    for i in range(dim):
        for j in range(i + 1, dim):
            pp = zero[:]
            pm = zero[:]
            mp = zero[:]
            mm = zero[:]
            pp[i] = h
            pp[j] = h
            pm[i] = h
            pm[j] = -h
            mp[i] = -h
            mp[j] = h
            mm[i] = -h
            mm[j] = -h
            e_pp = torus_energy(bg, pp, cfg)
            e_pm = torus_energy(bg, pm, cfg)
            e_mp = torus_energy(bg, mp, cfg)
            e_mm = torus_energy(bg, mm, cfg)
            value = (e_pp - e_pm - e_mp + e_mm) / (4.0 * h * h)
            hessian[i][j] = value
            hessian[j][i] = value

    coeffs = solve_linear_system(hessian, [-g for g in gradients])

    # Guard against overstepping the local quadratic model.
    best_coeffs = zero
    best_energy = e0
    for scale in (1.0, 0.5, 0.25, 0.125):
        trial = [scale * c for c in coeffs]
        e_trial = torus_energy(bg, trial, cfg)
        if e_trial < best_energy:
            best_energy = e_trial
            best_coeffs = trial

    stats = {
        "energy_unrelaxed": e0,
        "energy_relaxed": best_energy,
        "energy_delta": best_energy - e0,
        "gradient_norm": math.sqrt(sum(g * g for g in gradients)),
    }
    return best_coeffs, stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Relax the curved torus ansatz in a small f1 basis.")
    parser.add_argument("--n", type=int, default=41)
    parser.add_argument("--half-width", type=float, default=5.0)
    parser.add_argument("--profile-n", type=int, default=1800)
    parser.add_argument("--profile-x-max", type=float, default=20.0)
    parser.add_argument("--finite-diff-step", type=float, default=0.25)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = RelaxationConfig(
        n=args.n,
        half_width=args.half_width,
        profile_n=args.profile_n,
        profile_x_max=args.profile_x_max,
        finite_diff_step=args.finite_diff_step,
    )
    vortex = VortexProfile.solve(n=cfg.profile_n, x_max=cfg.profile_x_max)
    bg = ToroidalBackground(f0=vortex.value, f0_prime=vortex.derivative)
    coeffs, stats = quadratic_relaxation(bg, cfg)
    print("Curved torus relaxation")
    print(f"grid n             = {cfg.n}")
    print(f"half_width         = {cfg.half_width}")
    print(f"profile_n          = {cfg.profile_n}")
    print(f"finite_diff_step   = {cfg.finite_diff_step}")
    print(f"basis_count        = {len(coeffs)}")
    amp_coeffs, phase_coeffs = split_coeffs(coeffs)
    for i, coeff in enumerate(amp_coeffs):
        print(f"amp_c[{i}]          = {coeff:.12e}")
    for i, coeff in enumerate(phase_coeffs):
        print(f"phase_c[{i}]        = {coeff:.12e}")
    print(
        "amp_coeffs_cli     = "
        + ",".join(f"{coeff:.12g}" for coeff in amp_coeffs)
    )
    print(
        "phase_coeffs_cli   = "
        + ",".join(f"{coeff:.12g}" for coeff in phase_coeffs)
    )
    print(f"E_unrelaxed        = {stats['energy_unrelaxed']:.12e}")
    print(f"E_relaxed          = {stats['energy_relaxed']:.12e}")
    print(f"Delta_E            = {stats['energy_delta']:.12e}")
    print(f"relative_delta     = {stats['energy_delta'] / stats['energy_unrelaxed']:.12e}")
    print(f"gradient_norm      = {stats['gradient_norm']:.12e}")


if __name__ == "__main__":
    main()

"""First-pass cubic-vertex self-energy estimate for the muon mode.

Implements the calculation outlined in
papers/SSV-I/muon-cubic-vertex-self-energy-memo.md.

The LogSE expansion around the relaxed electron-torus equilibrium produces
a cubic vertex with coupling

    g_3(x) = -b * rho_0 / (6 * (1 + x_0(x))^2)
           = -b * rho_0^3 / (6 * |psi_0(x)|^4)        for rho_0 = 1.

In the breather core |psi_0|^2 -> O(0.1) rho_0, so g_3 is enhanced by
~ 1/(min_rho)^2 ~ 100x relative to the asymptotic LogSE coupling. This
script computes the cubic matrix element

    V_{abc} = -b/6 * 2*pi * int dr dz r * |psi_0(r,z)|^2
                            * phi_a(r,z) * phi_b(r,z) * phi_c(r,z)
              * 2*pi * delta_{m_a + m_b + m_c, 0}

(in the single-amplitude / "u + v* ~ phi" first-pass approximation;
the full Bogoliubov treatment is a follow-up) and then estimates the
one-loop self-energy

    Sigma_a(omega_a) ~ sum_{b,c} |V_{abc}|^2 / (omega_a - omega_b - omega_c)

for representative external modes.

The headline output is the *ratio* of cubic-vertex-weighted action
between Kelvin-helicity (muon-like, delocalized on torus) and
breathing/core (electron-like, peaked at core) modes. If the ratio
disagrees by O(0.01 to 0.1), the cubic vertex is the credible carrier
of the residual ~1% gap.

Status: prototype / first-pass dimensional estimate.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

from kelvin_augmented_bdg import (
    AzimuthalMode,
    build_modes,
    is_kelvin_mode,
)
from toroidal_background import ToroidalBackground
from toroidal_projection_integrals import ProjectionConfig, projection_window_weight


@dataclass(frozen=True)
class ModeIntegrals:
    name: str
    m_phi: int
    norm: float
    core_weight: float
    cubic_diag: float        # V_aaa (zero if m_phi != 0)
    cubic_kelvin_breather: float  # V_{a, a*, breathing} for paired Kelvin


def background_density_squared(bg: ToroidalBackground, r: float, z: float) -> float:
    """Local |psi_0(r,z)|^2 with a small floor."""
    return max(abs(bg.psi0(r, z)) ** 2, 1.0e-12)


def cubic_coupling(amp_sq: float, b_coeff: float = 1.0) -> float:
    """g_3(x) = -b * rho_0^3 / (6 * |psi_0|^4) in code units (rho_0 = 1)."""
    return -b_coeff / (6.0 * amp_sq * amp_sq)


def meridional_integral(
    bg: ToroidalBackground,
    cfg: ProjectionConfig,
    integrand,
    use_window: bool = True,
) -> float:
    """Midpoint cylindrical meridional integral with optional smooth window."""
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    total = 0.0
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            jac = 2.0 * math.pi * r * cfg.dr * cfg.dz
            if use_window:
                jac *= projection_window_weight(bg, r, z, cfg)
            total += jac * integrand(r, z)
    return total


def mode_norm(bg: ToroidalBackground, mode: AzimuthalMode, cfg: ProjectionConfig) -> float:
    """L2 norm of mode amplitude on the meridional grid (real-valued sq abs)."""
    def integrand(r, z):
        val = mode.field(r, z)
        return abs(val) ** 2
    return meridional_integral(bg, cfg, integrand)


def mode_core_weight(bg: ToroidalBackground, mode: AzimuthalMode, cfg: ProjectionConfig) -> float:
    """Integral of |mode|^2 weighted by 1/|psi_0|^2 -- proxy for how much the
    mode lives where the cubic coupling is enhanced (the breather core)."""
    def integrand(r, z):
        amp_sq = background_density_squared(bg, r, z)
        return abs(mode.field(r, z)) ** 2 / amp_sq
    return meridional_integral(bg, cfg, integrand)


def cubic_matrix_element_meridional(
    bg: ToroidalBackground,
    cfg: ProjectionConfig,
    mode_a: AzimuthalMode,
    mode_b: AzimuthalMode,
    mode_c: AzimuthalMode,
    b_coupling: float = 1.0,
) -> complex:
    """Cubic-vertex matrix element with first-pass simplification:

    Use density-perturbation amplitude delta_rho_n ~ |psi_0|^2 * phi_n
    (u + v* ~ phi for an input mode). Then

      V_abc = int g_3 * delta_rho_a * delta_rho_b * delta_rho_c d^3x
            = int -b/(6 |psi_0|^4) * |psi_0|^6 * phi_a phi_b phi_c d^3x
            = -b/6 int |psi_0|^2 * phi_a * phi_b * phi_c d^3x.

    Azimuthal selection: m_a + m_b + m_c = 0 (otherwise the d phi integral
    gives zero). Within that, the meridional integral is computed below
    with the cylindrical Jacobian; the d phi integral contributes 2*pi
    when the selection rule is satisfied (folded into the meridional
    Jacobian already by `meridional_integral`).
    """
    if mode_a.m_phi + mode_b.m_phi + mode_c.m_phi != 0:
        return 0.0
    pref = -b_coupling / 6.0

    def integrand(r, z):
        amp_sq = background_density_squared(bg, r, z)
        prod = mode_a.field(r, z) * mode_b.field(r, z) * mode_c.field(r, z)
        return amp_sq * prod
    return pref * meridional_integral(bg, cfg, integrand)


def conjugate_mode(mode: AzimuthalMode) -> AzimuthalMode:
    """Create the m_phi -> -m_phi partner with complex-conjugated field."""
    def conj_field(r, z, mode=mode):
        return mode.field(r, z).conjugate()
    return AzimuthalMode(name=mode.name + "*", field=conj_field, m_phi=-mode.m_phi)


def compute_mode_integrals(
    bg: ToroidalBackground,
    cfg: ProjectionConfig,
    modes: list[AzimuthalMode],
    b_coupling: float,
) -> list[ModeIntegrals]:
    # Identify a representative m_phi=0 "breathing" mode for the paired
    # Kelvin contribution: prefer phi_R-based breather seed (mode "K_plus"
    # in combined basis); fall back to "R" or "chi".
    breather_candidates = [m for m in modes if m.m_phi == 0]
    if not breather_candidates:
        raise RuntimeError("no m_phi=0 mode found for breathing intermediate")
    breather = breather_candidates[0]
    if any(m.name == "R" for m in breather_candidates):
        breather = next(m for m in breather_candidates if m.name == "R")

    results = []
    for mode in modes:
        norm = mode_norm(bg, mode, cfg)
        core = mode_core_weight(bg, mode, cfg)
        if mode.m_phi == 0:
            diag = cubic_matrix_element_meridional(bg, cfg, mode, mode, mode, b_coupling)
            cubic_diag = abs(diag) ** 2
        else:
            cubic_diag = 0.0
        # Paired contribution V_{a, a*, breather} when m_a + (-m_a) + 0 = 0
        a_star = conjugate_mode(mode)
        paired = cubic_matrix_element_meridional(bg, cfg, mode, a_star, breather, b_coupling)
        cubic_kelvin_breather = abs(paired) ** 2
        results.append(
            ModeIntegrals(
                name=mode.name,
                m_phi=mode.m_phi,
                norm=norm,
                core_weight=core,
                cubic_diag=cubic_diag,
                cubic_kelvin_breather=cubic_kelvin_breather,
            )
        )
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="First-pass cubic-vertex self-energy estimate for the muon mode."
    )
    parser.add_argument("--n", type=int, default=49, help="Meridional grid size.")
    parser.add_argument("--half-width", type=float, default=5.0, help="Box half-width.")
    parser.add_argument("--profile-n", type=int, default=1800, help="Vortex profile resolution.")
    parser.add_argument("--alpha", type=float, default=1.0 / 137.035999084, help="Thin-ring parameter.")
    parser.add_argument("--core-basis", choices=("two", "four"), default="four")
    parser.add_argument("--kelvin-seed", choices=("helicity", "displacement", "breathing", "combined"), default="combined")
    parser.add_argument("--window-radius", type=float, default=4.0, help="Smooth-window radius.")
    parser.add_argument("--window-taper", type=float, default=1.0, help="Smooth-window taper.")
    parser.add_argument("--b-coupling", type=float, default=1.0, help="LogSE coupling b (rho_0 = 1).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("SSV-I -- cubic-vertex self-energy first pass")
    print(f"grid n={args.n}, half_width={args.half_width}, "
          f"profile_n={args.profile_n}, alpha={args.alpha:.6e}")
    print(f"core_basis={args.core_basis}, kelvin_seed={args.kelvin_seed}, "
          f"window R={args.window_radius}, T={args.window_taper}")
    print()

    from vortex_profile import VortexProfile
    vortex = VortexProfile.solve(n=args.profile_n, x_max=20.0)
    bg = ToroidalBackground(alpha=args.alpha, f0=vortex.value, f0_prime=vortex.derivative)

    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        profile="numerical",
        profile_n=args.profile_n,
        profile_x_max=20.0,
        chi_parity="sin",
        projection_window="smooth",
        window_radius=args.window_radius,
        window_taper=args.window_taper,
    )

    include_four = args.core_basis == "four"
    modes = build_modes(bg, cfg, include_core_four=include_four, kelvin_seed=args.kelvin_seed)
    print(f"basis size = {len(modes)} modes")
    print()

    # Report the cubic-coupling profile inside the breather core
    # for orientation.
    psi0_at_core = background_density_squared(bg, bg.r_e, 0.0)
    g3_core = cubic_coupling(psi0_at_core, args.b_coupling)
    g3_far = cubic_coupling(1.0, args.b_coupling)
    enhancement = abs(g3_core / g3_far) if g3_far != 0 else float("nan")
    print(f"|psi_0|^2 at core (r=R_e, z=0)     = {psi0_at_core:.6e}")
    print(f"g_3 at core                        = {g3_core:+.6e}")
    print(f"g_3 far (|psi|^2 = 1)              = {g3_far:+.6e}")
    print(f"core enhancement |g3_core/g3_far|  = {enhancement:.2f}")
    print()

    results = compute_mode_integrals(bg, cfg, modes, args.b_coupling)

    # Sort by mode azimuthal sector, then name
    results.sort(key=lambda r: (r.m_phi, r.name))

    print(f"{'mode':>26} {'m':>3} {'norm':>10} {'core_wt':>10} "
          f"{'|V_aaa|^2':>13} {'|V_aab|^2':>13}")
    print("-" * 80)
    for r in results:
        print(
            f"{r.name:>26} {r.m_phi:>+3d} {r.norm:>10.4e} {r.core_weight:>10.4e} "
            f"{r.cubic_diag:>13.4e} {r.cubic_kelvin_breather:>13.4e}"
        )
    print()
    print("Notes:")
    print("  - 'core_wt' = integral |phi|^2 / |psi_0|^2 (where g_3 is enhanced).")
    print("  - 'V_aaa' = diagonal cubic matrix element (m=0 modes only).")
    print("  - 'V_aab' = |V_{a, a*, breather}|^2 -- paired cubic, where")
    print("    'breather' is the lowest m=0 mode in the basis.")
    print()

    # Headline ratios: the structural difference between core-peaked (R, chi,
    # breathing) and Kelvin-delocalized modes is what carries the muon-electron
    # Lamb-shift difference.
    core_peaked = [r for r in results if r.m_phi == 0]
    kelvin_modes = [r for r in results if abs(r.m_phi) == 1]
    if core_peaked and kelvin_modes:
        avg_core_diag = sum(r.cubic_diag for r in core_peaked) / len(core_peaked)
        avg_kelvin_paired = sum(r.cubic_kelvin_breather for r in kelvin_modes) / len(kelvin_modes)
        # First-pass dimensionless Lamb-shift indicator:
        # |V_Kelvin|^2 vs |V_breather|^2 -- ratio drives Sigma_mu vs Sigma_e
        ratio = (
            avg_kelvin_paired / avg_core_diag if avg_core_diag > 0 else float("inf")
        )
        print(f"avg |V_aaa|^2 over m=0 core modes        = {avg_core_diag:.4e}")
        print(f"avg |V_aab|^2 over Kelvin modes (paired) = {avg_kelvin_paired:.4e}")
        print(f"ratio |V_aab|^2 / |V_aaa|^2              = {ratio:.4e}")
        # Self-energy estimate:
        # Sigma ~ |V|^2 / omega, with omega ~ O(1) in code units
        # Relative shift Delta = Sigma_mu/omega_mu - Sigma_e/omega_e
        # For first-pass: |Delta| ~ ratio - 1 (very rough)
        first_pass_delta = abs(ratio - 1.0)
        print()
        print(f"first-pass relative shift indicator |Delta| ~ {first_pass_delta:.3e}")
        print("(this is a dimensional indicator only; the actual one-loop")
        print(" diagram requires the full Bogoliubov v-component and the")
        print(" energy denominator -- see memo §6.)")


if __name__ == "__main__":
    main()

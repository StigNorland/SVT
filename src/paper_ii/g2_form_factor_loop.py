"""Toroidal-form-factor loop integral for the SSV ring-size correction to (g-2)/2.

Paper II §3 closure/falsification calculation for issue #33.  The Schwinger one-loop
vertex correction is modified by inserting the toroidal-vortex form factor
F(|k|R*) = J_0(|k|R*) at each internal photon-electron vertex, so the loop
integrand acquires a factor F^2(|k|R*) on the photon line.  R* = ξ/α is the
SSV equilibrium ring radius (Paper I), with ξ = ƛ_e the electron Compton
wavelength, so R̃ ≡ R* m_e = 1/α ≈ 137.

Reduction
---------
Feynman-parametrise the three propagators of the vertex-correction diagram
(two electron, one photon) with parameters (x, y, z=1-x-y).  After combining
denominators and shifting the loop momentum l → l + S(x,y,z), the form factor
F(|k_photon|R*) depends on the spatial part of the *unshifted* photon
momentum.  In the electron rest frame the shift S = (x+y)p has p_spatial = 0,
so |k_photon,spatial| = |l_spatial,shifted| — the form-factor argument is
unaffected by the Feynman shift.

The F_2(0) projection of the numerator is a constant in l (P&S eq. 6.33),
proportional to 2m^2 z(1-z), with z = 1-x-y.  All x,y dependence reduces to
the triangle area (1-z), and the 4-D Euclidean l-integral with the form
factor inserted becomes:

  I_F(Δ, R*) = (3/(32π^2)) ∫₀^∞ dk · k² · J_0²(kR*) / (k² + Δ)^(5/2)

where Δ = (1-z)²m². The ratio η(Δ,R*) ≡ I_F/I_0 (with I_0 = 1/(32π² Δ) the
F=1 limit) is

  η(Δ, R*) = 3Δ · ∫₀^∞ dk · k² · J_0²(kR*) / (k² + Δ)^(5/2).

Reordering integrations and rescaling κ = k/m_e, R̃ = R* m_e:

  a_e[F, R*] = (3α/π) · ∫₀^∞ dκ · κ² · J_0²(κ R̃) · G(κ)

with

  G(κ) = ∫₀^1 du · u^3 / (κ² + u²)^(5/2)
       = -1/√(κ²+1) + κ² / [3(κ²+1)^(3/2)] + 2/(3κ).

At F=1 (κR̃ → 0 limit, point-like coupling) one has J_0² = 1 and
∫₀^∞ κ² G(κ) dκ = 1/6 (verified below), recovering Schwinger's α/(2π).

The integrand κ² J_0²(κ R̃) G(κ) is regular at κ=0 (G ~ 2/(3κ) ⇒ κ²G ~ 2κ/3)
and decays as 1/κ⁵ at infinity (numerator κ² × ⟨J_0²⟩ ~ 1/(πR̃) × κ, kernel
G ~ 1/(4κ⁴) ⇒ integrand ~ 1/(4π R̃ κ³) ⇒ ∫_{large} ~ 1/κ² convergent).
For R̃ = 1/α the Bessel argument oscillates ~137× across κ ∈ [0,1], so the
integral must be evaluated with care.  We use scipy.integrate.quad with the
Bessel oscillation points supplied as breakpoints.
"""

from __future__ import annotations

import math
import warnings

import numpy as np
from scipy import integrate
from scipy import special

ALPHA = 1.0 / 137.035999084  # CODATA 2018 fine-structure constant
SCHWINGER = ALPHA / (2.0 * math.pi)
EXP_AE = 1.15965218059e-3   # CODATA 2018 measured a_e (electron, dimensionless)


def G_kernel(kappa: float) -> float:
    """Feynman-parameter kernel G(κ) = ∫₀¹ u³/(κ²+u²)^(5/2) du."""
    if kappa <= 0.0:
        return float("inf")
    a = math.sqrt(kappa * kappa + 1.0)
    return -1.0 / a + (kappa * kappa) / (3.0 * a**3) + 2.0 / (3.0 * kappa)


def integrand_schwinger(kappa: float) -> float:
    """κ² · G(κ).  Closed-form integral over κ ∈ [0,∞) is 1/6."""
    return kappa * kappa * G_kernel(kappa)


def integrand_modified(kappa: float, r_tilde: float) -> float:
    """κ² · J_0²(κ R̃) · G(κ).  Default = Paper II §3 form factor."""
    j0 = special.j0(kappa * r_tilde)
    return kappa * kappa * j0 * j0 * G_kernel(kappa)


# ── Form-factor families for the "borrow algebra, keep scales" exploration ──
#
# Each F2(x) returns F(x)² where x = κ·R̃, with R̃ ≡ R_v · m_e the
# dimensionless effective vertex scale.  All are normalised F²(0) = 1
# (point-coupling limit) and F²(x) → some power of 1/x at large x.

def F2_bessel(x: float) -> float:
    """J_0(x)²  — Paper II §3's classical-current-loop form factor."""
    j0 = special.j0(x)
    return j0 * j0

def F2_gaussian(x: float) -> float:
    """exp(-x²)  — Gaussian smearing of an extended source."""
    return math.exp(-x * x)

def F2_yukawa(x: float) -> float:
    """1 / (1 + x²)²  — dipole / Yukawa form factor."""
    return 1.0 / (1.0 + x * x) ** 2

def F2_lorentzian(x: float) -> float:
    """1 / (1 + x²)  — single-pole / Lorentzian form factor."""
    return 1.0 / (1.0 + x * x)

def F2_constant(_x: float) -> float:
    """F² = 1 — point-like / purely topological vertex."""
    return 1.0


FORM_FACTOR_FAMILIES = {
    "J_0² (current loop)": F2_bessel,
    "Gaussian":            F2_gaussian,
    "Dipole (Yukawa)":     F2_yukawa,
    "Lorentzian":          F2_lorentzian,
    "Constant (F=1)":      F2_constant,
}


def integrand_family(kappa: float, r_tilde: float, f2) -> float:
    return kappa * kappa * f2(kappa * r_tilde) * G_kernel(kappa)


def evaluate_family(r_tilde: float, f2) -> tuple[float, float]:
    """Compute a_e[F] for a given form-factor family at scale R̃."""
    # Single quad call; for non-oscillatory F² this converges fast.
    if f2 is F2_bessel and r_tilde > 1e-3:
        # Use Bessel-zero breakpoints for J_0² at large R̃.
        return evaluate_modified(r_tilde)
    val, err = integrate.quad(
        integrand_family, 0.0, np.inf, args=(r_tilde, f2),
        limit=400, epsabs=1e-16, epsrel=1e-10,
    )
    return val, err


def max_allowed_rv(f2, target_frac: float = 1e-5,
                   r_lo: float = 1e-7, r_hi: float = 10.0) -> float:
    """Bisect to find the largest R̃ such that |δa_e/a_e_Schw| ≤ target_frac.

    target_frac = 1e-5 ≈ tolerance set by next-order QED contribution
    (α/π)² ≈ 5.4e-6, below which a 1-loop SSV form-factor correction
    would not spoil agreement with QED + CODATA at the 5-loop level.
    """
    def excess(r_tilde: float) -> float:
        val, _ = evaluate_family(r_tilde, f2)
        a_full = (3.0 * ALPHA / math.pi) * val
        return abs(a_full / SCHWINGER - 1.0) - target_frac

    # If even r_lo exceeds target, return 0
    if excess(r_lo) > 0:
        return 0.0
    if excess(r_hi) < 0:
        return r_hi
    # bisection
    for _ in range(60):
        mid = math.sqrt(r_lo * r_hi)  # log-bisection
        if excess(mid) < 0:
            r_lo = mid
        else:
            r_hi = mid
    return math.sqrt(r_lo * r_hi)


def bessel_zeros(r_tilde: float, k_max: float, n_max: int = 5000) -> list[float]:
    """Zeros of J_0(κ R̃) on (0, k_max], used as integration breakpoints."""
    zeros_j0 = special.jn_zeros(0, n_max)  # zeros of J_0
    pts = [z / r_tilde for z in zeros_j0 if z / r_tilde < k_max]
    return pts


def evaluate_schwinger_normalization() -> float:
    """Verify ∫₀^∞ κ² G(κ) dκ = 1/6, so (3α/π)·(1/6) = α/(2π) = Schwinger."""
    val, err = integrate.quad(
        integrand_schwinger, 0.0, np.inf, limit=200,
        epsabs=1e-14, epsrel=1e-12,
    )
    return val, err


def evaluate_modified(r_tilde: float) -> tuple[float, float]:
    """Compute ∫₀^∞ κ² J_0²(κR̃) G(κ) dκ with Bessel-zero breakpoints."""
    # Split: (0, κ_split) with breakpoints at J_0 zeros, then (κ_split, ∞) tail.
    kappa_split = 50.0  # cover the bulk; tail beyond decays fast.
    zeros = bessel_zeros(r_tilde, kappa_split, n_max=20000)

    if not zeros:
        val_a, err_a = integrate.quad(
            integrand_modified, 0.0, kappa_split, args=(r_tilde,),
            limit=400, epsabs=1e-16, epsrel=1e-10,
        )
    else:
        val_a, err_a = integrate.quad(
            integrand_modified, 0.0, kappa_split, args=(r_tilde,),
            points=zeros,
            limit=max(400, len(zeros) + 50),
            epsabs=1e-16, epsrel=1e-10,
        )
    val_b, err_b = integrate.quad(
        integrand_modified, kappa_split, np.inf, args=(r_tilde,),
        limit=400, epsabs=1e-16, epsrel=1e-10,
    )
    return val_a + val_b, math.hypot(err_a, err_b)


def main() -> None:
    # The exploratory family scan intentionally pushes below the integration
    # noise floor for the CODATA column.  The regression tests assert the
    # stable invariants; keep the report output readable.
    warnings.filterwarnings("ignore", category=integrate.IntegrationWarning)

    print("=" * 70)
    print("Paper II §3 — toroidal form-factor loop integral (issue #33)")
    print("=" * 70)

    # ── 1.  Verify Schwinger normalisation ────────────────────────────────
    int_schw, err_schw = evaluate_schwinger_normalization()
    a_e_schw = (3.0 * ALPHA / math.pi) * int_schw
    print()
    print("── 1. Normalisation check (F ≡ 1) ────────────────────────────────")
    print(f"  ∫₀^∞ κ² G(κ) dκ               = {int_schw:.12f}  (target 1/6 = {1/6:.12f})")
    print(f"  reported abs error            = {err_schw:.2e}")
    print(f"  a_e (F=1) = (3α/π)·integral   = {a_e_schw:.6e}")
    print(f"  Schwinger α/(2π)              = {SCHWINGER:.6e}")
    print(f"  relative error                = {(a_e_schw / SCHWINGER - 1):+.3e}")

    # ── 2.  Form-factor result, R̃ = 1/α ──────────────────────────────────
    r_tilde = 1.0 / ALPHA
    int_mod, err_mod = evaluate_modified(r_tilde)
    a_e_mod = (3.0 * ALPHA / math.pi) * int_mod
    delta_a = a_e_mod - SCHWINGER

    print()
    print("── 2. Form-factor result (R̃ = R*·m_e = 1/α) ──────────────────────")
    print(f"  R̃                             = {r_tilde:.6f}")
    print(f"  ∫₀^∞ κ² J_0²(κR̃) G(κ) dκ      = {int_mod:.6e}")
    print(f"  quad abs-error estimate       = {err_mod:.2e}")
    print(f"  a_e[F]                        = {a_e_mod:.6e}")
    print(f"  δa_e = a_e[F] − α/(2π)        = {delta_a:+.6e}")
    print(f"  δa_e / [α/(2π)]               = {delta_a / SCHWINGER:+.6e}")

    # ── 3.  Compare to paper's parametric estimate ────────────────────────
    paper_param = -ALPHA**3 / (4.0 * math.pi)
    print()
    print("── 3. Compared to parametric estimate ────────────────────────────")
    print(f"  Paper II eq. (612)  −α³/(4π)   = {paper_param:+.6e}")
    print(f"  Numerical δa_e                 = {delta_a:+.6e}")
    print(f"  Ratio (numerical / parametric) = {delta_a / paper_param:+.3e}")

    # ── 4.  Compare to experiment ─────────────────────────────────────────
    print()
    print("── 4. Compared to CODATA measurement of a_e ──────────────────────")
    print(f"  a_e (experiment, CODATA 2018)  = {EXP_AE:.6e}")
    print(f"  a_e[F] (this calc)             = {a_e_mod:.6e}")
    print(f"  a_e[F] / a_e(exp)              = {a_e_mod / EXP_AE:.6e}")
    print(f"  Fractional deviation           = {(a_e_mod / EXP_AE - 1):+.3e}")

    # ── 5.  R̃ scan to expose the suppression structure ───────────────────
    print()
    print("── 5. R̃ scan: how the form factor suppresses Schwinger ──────────")
    print(f"  {'R̃':>10s}  {'a_e[F]':>14s}  {'a_e[F]/a_e_Schw':>16s}  {'δa_e':>14s}")
    for r in (0.0, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0, 1.0 / ALPHA):
        if r == 0.0:
            val = 1.0 / 6.0
        else:
            val, _ = evaluate_modified(r)
        a_full = (3.0 * ALPHA / math.pi) * val
        ratio = a_full / SCHWINGER
        d = a_full - SCHWINGER
        print(f"  {r:>10.4g}  {a_full:>14.6e}  {ratio:>16.6e}  {d:>+14.6e}")

    # ── 6.  Form-factor family scan (exploration for the algebra-import) ──
    # Tolerances: 1e-3 is "leaves Schwinger to 0.1 %", well below the
    # 0.15 % gap between Schwinger and CODATA that higher-order QED fills.
    # 5e-6 ≈ α/π × Schwinger, the 2-loop scale: any 1-loop SSV correction
    # smaller than this would not spoil 2-loop matching.
    # 1e-10 ≈ current CODATA uncertainty on a_e relative to Schwinger.
    print()
    print("── 6. Maximum R_v for each form-factor family ────────────────────")
    print("    (R_v = effective vertex scale in units of ƛ_e = 1/m_e)")
    print()
    print(f"  {'Family':<22s}  {'≤0.1% Schw':>12s}  {'≤2-loop':>12s}  {'≤CODATA':>12s}")
    print(f"  {'':<22s}  {'(1e-3)':>12s}  {'(5e-6)':>12s}  {'(1e-10)':>12s}")
    for name, f2 in FORM_FACTOR_FAMILIES.items():
        r_loose = max_allowed_rv(f2, target_frac=1e-3)
        r_two_loop = max_allowed_rv(f2, target_frac=5e-6)
        r_codata = max_allowed_rv(f2, target_frac=1e-10)
        if f2 is F2_constant:
            print(f"  {name:<22s}  {'∞':>12s}  {'∞':>12s}  {'∞':>12s}")
        else:
            print(f"  {name:<22s}  {r_loose:>12.4e}  {r_two_loop:>12.4e}  {r_codata:>12.4e}")

    print()
    print("  Comparison to candidate SSV-intrinsic scales:")
    print(f"    R*  = ƛ_e/α      → R̃ = {1.0/ALPHA:.4e}   (ring radius, Paper I)")
    print(f"    ξ   = ƛ_e        → R̃ = 1                (vortex core / tube)")
    print(f"    ƛ_e/α² (chiral?) → R̃ = {ALPHA:.4e}     (would need motivation)")


if __name__ == "__main__":
    main()

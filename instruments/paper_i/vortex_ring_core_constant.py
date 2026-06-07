"""
Compute the ring-energy core constant C for the LogSE vortex.

The Lamb thin-ring formula (SSV units: xi=1, rho0=1, c=1):

    E_ring = pi * R * [ln(8R/xi) - C]

For a hollow core at r=xi: C = 2.0 (standard default).
For the actual LogSE vortex profile, C is smaller because the density
profile is smooth (not a step function), adding extra kinetic energy
inside the core region.

Derivation
----------
The per-unit-length kinetic energy of a straight vortex:

    eps(R) / L  =  pi * integral_0^R  f^2(r)/r  dr

For large R this behaves as  pi [ln R + A], where:

    A  =  lim_{R->inf}  [ integral_0^R f^2/r dr  -  ln R ]
       =  integral_0^1 f^2(r)/r dr  -  integral_1^inf (1-f^2(r))/r dr

Both pieces converge (the first since f~r near 0, the second since
f^2->1 exponentially fast).

The ring energy is  E_ring = pi R [ln(8R) - C]  where:

    C = 2 - A

Sanity check (hollow core, f=1 for r>1, f=0 otherwise):
    A_hollow = 0  =>  C_hollow = 2  ✓

For GPE:  A_GPE ≈ 1.385  =>  C_GPE ≈ 0.615  (Roberts & Grant 1971).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from paper_i.vortex_profile import VortexProfile


# ---------------------------------------------------------------------------
# Core-constant computation
# ---------------------------------------------------------------------------

def compute_core_constant(
    n_profile: int = 4000,
    x_max: float = 14.0,   # stay well inside stability limit (~16)
    n_quad: int = 200_000,
) -> dict:
    """Compute C for the LogSE vortex ring.

    Returns a dict with C, A, and the two sub-integrals.

    The LogSE profile becomes numerically unstable for r > ~16 xi
    (oscillatory shooting solution near x_max).  We use x_max=14 and
    estimate the tail analytically.  The LogSE linearises near f=1 as
    epsilon ~ exp(-2r), so the tail  integral_{x_max}^inf (1-f^2)/r dr
    is approximately  (1-f^2(x_max)) * exp(-2*(r-x_max)) integrated,
    giving (1-f^2(x_max)) / (2 * x_max).
    """
    prof = VortexProfile.solve(x_min=1e-4, x_max=x_max, n=n_profile)

    # Fine quadrature grid (dense near origin, coarser farther out)
    r = np.concatenate([
        np.linspace(1e-4, 1.0, 50_000),
        np.linspace(1.0, x_max, 150_000)[1:],
    ])
    f = np.array([prof.value(ri) for ri in r])
    f2 = f ** 2

    # Part 1: integral_0^1  f^2/r  dr
    mask1 = r <= 1.0
    r1, f2_1 = r[mask1], f2[mask1]
    A_part1 = float(np.trapezoid(f2_1 / r1, r1))

    # Part 2: integral_1^x_max  (1-f^2)/r  dr  +  analytic tail
    mask2 = r >= 1.0
    r2, f2_2 = r[mask2], f2[mask2]
    A_part2_numerical = float(np.trapezoid((1.0 - f2_2) / r2, r2))

    # Analytic tail beyond x_max:  epsilon ~ A*exp(-2r), so
    # integral_{x_max}^inf (1-f^2)/r dr ~ (1-f^2(x_max)) * [exp(-2(r-x_max))/(2r)] integrated
    # Leading term: (1-f^2(x_max)) / (2 * x_max)
    f_at_xmax = prof.value(x_max * 0.9999)  # last valid point
    tail_est = float((1.0 - f_at_xmax**2) / (2.0 * x_max))
    A_part2 = A_part2_numerical + tail_est

    A = A_part1 - A_part2
    C = 2.0 - A

    # Cross-check: A_direct = integral_0^R f^2/r dr - ln(R) → A as R → inf
    crosscheck = {}
    for R_check in [3.0, 5.0, 8.0, x_max]:
        mask = r <= R_check
        r_c, f2_c = r[mask], f2[mask]
        integral = float(np.trapezoid(f2_c / r_c, r_c))
        crosscheck[R_check] = integral - math.log(R_check)

    return {
        "C": C,
        "A": A,
        "A_part1_int0_to_1": A_part1,
        "A_part2_numerical": A_part2_numerical,
        "A_part2_tail_est": tail_est,
        "A_part2_total": A_part2,
        "crosscheck_A_at_R": crosscheck,
        "slope_at_origin": prof.slope,
        "f_sq_half_radius": _half_density_radius(prof),
        "n_profile": n_profile,
        "x_max": x_max,
        "n_quad": len(r),
    }


def _half_density_radius(prof: VortexProfile) -> float:
    """Radius where f^2 = 0.5."""
    r_vals = np.linspace(0.01, 5.0, 10000)
    f2 = np.array([prof.value(r) ** 2 for r in r_vals])
    idx = int(np.searchsorted(f2, 0.5))
    if idx == 0 or idx >= len(r_vals):
        return float("nan")
    r0, r1 = r_vals[idx - 1], r_vals[idx]
    f0, f1 = f2[idx - 1], f2[idx]
    return float(r0 + (0.5 - f0) / (f1 - f0) * (r1 - r0))


# ---------------------------------------------------------------------------
# Re-run H7 (best-fit geometric series) with corrected C
# ---------------------------------------------------------------------------

PARTICLES = {
    "e":   1.0,
    "μ":   206.7682830,
    "τ":   3477.23,
    "π⁰":  264.1421,
    "π±":  273.1320,
    "p":   1836.15267,
    "n":   1838.68366,
}
ALPHA_INV = 137.035999084


def ring_energy(r: float, C: float) -> float:
    return math.pi * r * (math.log(8.0 * r) - C)


def h7_result(C: float) -> dict:
    """Find best-fit (R_e, q) for geometric series R_n = R_e * q^n."""
    from scipy.optimize import minimize

    mmu, mtau = PARTICLES["μ"], PARTICLES["τ"]
    r_floor = math.exp(C) / 8.0 * 1.001

    def err(params):
        log_re, log_q = params
        r_e = math.exp(log_re)
        q   = math.exp(log_q)
        r_mu  = r_e * q
        r_tau = r_e * q * q
        if r_e < r_floor or r_mu < r_floor or r_tau < r_floor:
            return 1e9
        e_e   = ring_energy(r_e,   C)
        e_mu  = ring_energy(r_mu,  C)
        e_tau = ring_energy(r_tau, C)
        if e_e <= 0 or e_mu <= 0 or e_tau <= 0:
            return 1e9
        err_mu  = (e_mu  / e_e - mmu)  / mmu
        err_tau = (e_tau / e_e - mtau) / mtau
        return err_mu**2 + err_tau**2

    res = minimize(err, x0=[0.0, math.log(8.0)], method="Nelder-Mead",
                   options={"xatol": 1e-12, "fatol": 1e-16, "maxiter": 50000})

    r_e = math.exp(res.x[0])
    q   = math.exp(res.x[1])

    e_e   = ring_energy(r_e,       C)
    e_mu  = ring_energy(r_e * q,   C)
    e_tau = ring_energy(r_e * q**2, C)

    return {
        "C": C,
        "r_e": r_e,
        "q": q,
        "ln_q": math.log(q),
        "q_over_8": q / 8.0,
        "r_e_over_1": r_e / 1.0,
        "r_e_over_alpha_inv": r_e / ALPHA_INV,
        "pred_mu":  e_mu  / e_e,
        "pred_tau": e_tau / e_e,
        "err_mu_pct":  (e_mu  / e_e - mmu)  / mmu  * 100,
        "err_tau_pct": (e_tau / e_e - mtau) / mtau * 100,
    }


# ---------------------------------------------------------------------------
# H1 test (R = 8^n) at the corrected C
# ---------------------------------------------------------------------------

def h1_result(C: float) -> dict:
    """Test R = {1, 8, 64} xi at the given C."""
    mmu, mtau = PARTICLES["μ"], PARTICLES["τ"]
    e1  = ring_energy(1.0,  C)
    e8  = ring_energy(8.0,  C)
    e64 = ring_energy(64.0, C)
    if e1 <= 0:
        return {"C": C, "valid": False}
    return {
        "C": C,
        "valid": True,
        "E(1)":  e1,
        "E(8)":  e8,
        "E(64)": e64,
        "pred_mu":  e8  / e1,
        "pred_tau": e64 / e1,
        "err_mu_pct":  (e8  / e1 - mmu)  / mmu  * 100,
        "err_tau_pct": (e64 / e1 - mtau) / mtau * 100,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Computing LogSE vortex ring core constant...")
    result = compute_core_constant()

    print(f"\n  LogSE vortex profile: slope at origin = {result['slope_at_origin']:.5f}")
    print(f"  Half-density radius R_sc = {result['f_sq_half_radius']:.4f} xi")
    print(f"\n  A_part1 = integral_0^1 f^2/r dr        = {result['A_part1_int0_to_1']:.6f}")
    print(f"  A_part2 = integral_1^xmax (1-f^2)/r dr = {result['A_part2_numerical']:.6f}")
    print(f"  A_part2 tail (analytic)                = {result['A_part2_tail_est']:.6f}")
    print(f"  A = A_part1 - A_part2_total             = {result['A']:.6f}")
    print(f"\n  C_LogSE = 2 - A = {result['C']:.6f}")
    print(f"  (compare: C_hollow = 2.000, C_GPE ≈ 0.615)")

    print("\n  Cross-check: integral_0^R f^2/r dr - ln(R)  →  A  as R -> inf")
    for R, val in sorted(result["crosscheck_A_at_R"].items()):
        print(f"    R={R:5.1f}:  {val:.6f}  (should converge to {result['A']:.6f})")

    C = result["C"]

    print(f"\n--- H1 (R = {{1, 8, 64}} xi) at C_LogSE = {C:.4f} ---")
    h1 = h1_result(C)
    if h1["valid"]:
        print(f"  m_mu/m_e  predicted={h1['pred_mu']:.4f}  actual=206.7683  err={h1['err_mu_pct']:+.2f}%")
        print(f"  m_tau/m_e predicted={h1['pred_tau']:.4f}  actual=3477.23   err={h1['err_tau_pct']:+.2f}%")
    else:
        print(f"  H1 invalid at this C (E(1) <= 0 means R=1 xi is below the formula's valid range)")

    print(f"\n--- H7 (best-fit R_e × q^n) at C_LogSE = {C:.4f} ---")
    h7 = h7_result(C)
    print(f"  Best-fit: R_e = {h7['r_e']:.5f} xi,  q = {h7['q']:.5f}")
    print(f"  q vs 8:   q/8 = {h7['q_over_8']:.5f}   (deviation {(h7['q_over_8']-1)*100:+.2f}%)")
    print(f"  ln(q) = {h7['ln_q']:.5f}  (ln(8) = {math.log(8):.5f})")
    print(f"  R_e vs alpha^-1: {h7['r_e_over_alpha_inv']:.5f}")
    print(f"  m_mu/m_e  err={h7['err_mu_pct']:+.4f}%")
    print(f"  m_tau/m_e err={h7['err_tau_pct']:+.4f}%")

    # Compare across C values
    print("\n--- Summary: q and R_e vs C ---")
    print(f"  {'C':>8s}  {'R_e/xi':>10s}  {'q':>10s}  {'q/8':>8s}  {'H1 mu err%':>12s}")
    print("  " + "-" * 58)
    for C_test in [2.0, 1.5, 1.0, 0.615, C, 0.3, 0.0]:
        h7t = h7_result(C_test)
        h1t = h1_result(C_test)
        h1_mu_err = h1t["err_mu_pct"] if h1t.get("valid") else float("nan")
        print(f"  {C_test:8.3f}  {h7t['r_e']:10.4f}  {h7t['q']:10.4f}  "
              f"{h7t['q_over_8']:8.4f}  {h1_mu_err:12.2f}")

    # Print marker for the LogSE result
    print(f"\n  => C_LogSE = {C:.4f},  best-fit q = {h7['q']:.4f},  q/8 = {h7['q_over_8']:.4f}")


if __name__ == "__main__":
    main()

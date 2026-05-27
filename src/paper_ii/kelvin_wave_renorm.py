"""Step 3: Kelvin wave renormalization — one-loop correction to lambda_perp.

Question: can δλ_perp from quantum/thermal Kelvin waves close the 232x gap?

Two mechanisms to check:
  (A) Classical LIA (Local Induction Approximation):
      lambda_bend(R) = (rho * kappa^2 * R / 4pi) * ln(R/xi)
      -> logarithmic, not linear

  (B) One-loop Kelvin wave RG correction:
      delta_lambda_perp / lambda_perp = integral of propagator over modes k = 1/R .. 1/xi

For the LIA dispersion: omega_K(k) = (kappa * k^2 / 4pi) * ln(1/(k*xi))

The one-loop (Wilsonian) correction integrates out modes from k_min = 1/R to k_max = 1/xi.
The relevant integral is the self-energy of the bending stiffness vertex:

  I_KW(R) = integral_{1/R}^{1/xi} dk * G_K(k)

where G_K(k) = omega_K(k) / k^2 ~ ln(1/k*xi) is the spectral weight.

We also check power-law running: lambda_perp(R) = lambda_perp(xi) * (R/xi)^p
for p = 0 (constant), 1/2, 1 (linear), 3/2.
"""

from __future__ import annotations

import math
import numpy as np

ALPHA = 1.0 / 137.035999084
PHI   = (1.0 + math.sqrt(5.0)) / 2.0
R_CAP = PHI / ALPHA          # ~ 221.5 xi
XI    = 1.0                  # healing length (natural unit)
KAPPA = 2.0 * math.pi        # circulation quantum (in units where hbar/m = 1)


def lia_bending_stiffness(R: float, xi: float = 1.0) -> float:
    """Classical LIA bending stiffness: lambda_bend = (kappa^2 / 4pi) * R * ln(R/xi)."""
    return (KAPPA**2 / (4 * math.pi)) * R * math.log(R / xi)


def kelvin_wave_integral(R: float, xi: float = 1.0, n_k: int = 10000) -> dict:
    """One-loop Kelvin wave integral from k_min = 1/R to k_max = 1/xi.

    Returns the integral and its scaling behavior.
    """
    k_min = 1.0 / R
    k_max = 1.0 / xi

    # Logarithmic spacing in k
    k = np.geomspace(k_min, k_max, n_k)

    # LIA spectral weight: G_K(k) = omega_K(k) / k^2 ~ (kappa/4pi) * ln(1/k*xi)
    log_factor = np.log(1.0 / (k * xi))
    log_factor = np.maximum(log_factor, 0.0)  # ensure non-negative

    G_k = (KAPPA / (4 * math.pi)) * log_factor

    # One-loop correction (Wilsonian, integrating over dk):
    I_dk = float(np.trapezoid(G_k, k))                   # ~ constant (UV dominated)

    # One-loop correction (log-RG, integrating over d ln k):
    I_dlnk = float(np.trapezoid(G_k, np.log(k)))         # ~ log(R/xi)

    # For comparison: LIA in k-space:
    # lambda_bend = integral_{k_min}^{k_max} dk * [k * omega_K(k) / k^4] * (ring phase space)
    # = kappa/(4pi) * integral dk / k * ln(1/k*xi)
    # = kappa/(4pi) * integral d(ln k) * ln(1/k*xi)

    # Manual integral of ln(1/k*xi) over dk (UV-dominated):
    integrand_uv = log_factor  # G_k proportional to this
    I_uv = float(np.trapezoid(integrand_uv, k))

    # Manual integral of ln(1/k*xi)^2 over d(ln k) (IR):
    integrand_ir = log_factor**2
    I_ir = float(np.trapezoid(integrand_ir, np.log(k)))

    return {
        "I_dk": I_dk,
        "I_dlnk": I_dlnk,
        "I_uv_scaling": I_uv,
        "I_ir_scaling": I_ir,
        "k_min": k_min, "k_max": k_max,
        "R": R,
    }


def main():
    print("=" * 72)
    print("Step 3: Kelvin wave renormalization — one-loop integral scaling")
    print("=" * 72)
    print()

    lam_perp   = 1.0 / ALPHA**2
    lam_target = PHI**3 / ALPHA**3
    lam_local  = lam_perp * 2.503   # (J+K)/4 from Step 1

    print(f"  phi = {PHI:.8f}, alpha = {ALPHA:.8f}")
    print(f"  R_cap = phi/alpha = {R_CAP:.2f} xi")
    print(f"  lambda_perp = alpha^-2 = {lam_perp:.4e}")
    print(f"  lambda_target = phi^3/alpha^3 = {lam_target:.4e}")
    print(f"  lambda_local (core only) = {lam_local:.4e}")
    print(f"  Gap: {lam_target/lam_local:.1f}x")
    print()

    # ── (A) Classical LIA ────────────────────────────────────────────────────
    print("── (A) Classical LIA bending stiffness ─────────────────────────────")
    r_vals = [1.0, 5.0, 10.0, 50.0, 100.0, R_CAP]
    print(f"  {'R/xi':>8}  {'LIA lambda_bend':>16}  {'LIA/target':>12}  {'ln(R/xi)':>10}")
    for R in r_vals:
        lia = lia_bending_stiffness(R)
        label = "R_cap" if abs(R - R_CAP) < 0.5 else ""
        print(f"  {R:8.2f}  {lia:16.4e}  {lia/lam_target:12.6f}  {math.log(R):10.4f}  {label}")
    print()

    lia_at_cap = lia_bending_stiffness(R_CAP)
    print(f"  LIA at R_cap = {lia_at_cap:.4e}")
    print(f"  Combined (local + LIA) at R_cap: {lam_local + lia_at_cap:.4e}")
    print(f"  Combined / target: {(lam_local + lia_at_cap)/lam_target:.4f}")
    print(f"  LIA scaling: R * ln(R/xi) — logarithmic, not linear")
    print()

    # ── (B) One-loop Kelvin wave integral (spectral weight) ──────────────────
    print("── (B) One-loop Kelvin wave integral I_KW(R) ───────────────────────")
    r_probe = [5.0, 10.0, 20.0, 50.0, 100.0, R_CAP]
    print(f"  {'R/xi':>8}  {'I_dk':>14}  {'I_dlnk':>14}  {'ln(R/xi)':>10}")
    prev_dk, prev_dlnk, prev_lnR = None, None, None
    results_kw = []
    for R in r_probe:
        res = kelvin_wave_integral(R)
        lnR = math.log(R)
        results_kw.append((R, res["I_dk"], res["I_dlnk"], lnR))
        print(f"  {R:8.2f}  {res['I_dk']:14.6f}  {res['I_dlnk']:14.6f}  {lnR:10.4f}")
    print()

    # Fit: I_dlnk vs ln(R/xi) — should be linear if log scaling
    lnR_vals = np.array([math.log(row[0]) for row in results_kw])
    I_dlnk_vals = np.array([row[2] for row in results_kw])
    A = np.column_stack([lnR_vals, np.ones_like(lnR_vals)])
    c, _, _, _ = np.linalg.lstsq(A, I_dlnk_vals, rcond=None)
    print(f"  Fit I_dlnk = {c[0]:.4f} * ln(R/xi) + {c[1]:.4f}")
    print(f"  -> One-loop integral scales as: ln(R/xi)  (logarithmic, not linear)")
    print()

    # ── Power-law running comparison ─────────────────────────────────────────
    print("── Power-law running: lambda_perp(R) = lambda_perp(xi) * (R/xi)^p ─")
    print(f"  {'p':>6}  {'lambda_perp(R_cap)':>22}  {'lambda_bend':>16}  {'gap':>8}")
    for p in [0.0, 0.5, 1.0, 1.5, 2.0]:
        lam_eff = lam_perp * (R_CAP / XI)**p
        lam_bend_p = lam_eff * 2.503   # (J+K)/4 ~ 2.503 from core integrals
        gap_p = lam_target / lam_bend_p
        print(f"  {p:6.1f}  {lam_eff:22.4e}  {lam_bend_p:16.4e}  {gap_p:8.4f}")
    print()

    # ── Logarithmic running δλ/λ = c * ln(R/xi) ─────────────────────────────
    print("── Logarithmic running: lambda_perp(R) = lambda_perp(xi) * [1 + c*ln(R/xi)] ─")
    ln_ratio = math.log(R_CAP / XI)
    print(f"  ln(R_cap/xi) = {ln_ratio:.4f}")
    # What c is needed to close the gap?
    c_needed = (lam_target / lam_local - 1) / ln_ratio
    print(f"  c needed to close gap: c = (232 - 1) / ln(222) = {c_needed:.4f}")
    print(f"  LIA gives c ~ kappa^2/(4pi * lambda_perp) = {KAPPA**2 / (4*math.pi*lam_perp):.6f}")
    print(f"  -> LIA coefficient is {KAPPA**2/(4*math.pi*lam_perp)/c_needed:.4e} of what's needed")
    print()

    # ── Summary ──────────────────────────────────────────────────────────────
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Gap to close:         {lam_target/lam_local:.1f}x")
    print(f"  LIA enhancement:      {lia_at_cap/lam_local:.4f}x  (ln scaling, R*ln(R/xi))")
    print(f"  Combined / target:    {(lam_local + lia_at_cap)/lam_target:.6f}")
    print(f"  ln(R_cap/xi):         {math.log(R_CAP):.4f}")
    print(f"  Linear (p=1) at R_cap: {(R_CAP)**1:.1f}x enhancement — sufficient")
    print(f"  Log enhancement:       {math.log(R_CAP):.1f}x — insufficient by {R_CAP/math.log(R_CAP):.0f}x")
    print()
    print("  Conclusion: Kelvin wave one-loop correction is O(ln(R/xi)) = O(5.4),")
    print(f"  not O(R/xi) = O({R_CAP:.0f}). The 232x gap is NOT closed by KW renormalization.")
    print(f"  A linear running lambda_perp(R) ~ R requires anomalous dimension [lambda_perp] = 1.")
    print()

    # ── LIA at cap vs target, explicit ───────────────────────────────────────
    print("── Detailed LIA vs SSV target at R_cap ────────────────────────────")
    print(f"  kappa = 2pi = {KAPPA:.4f}")
    print(f"  R_cap = phi/alpha = {R_CAP:.4f} xi")
    print(f"  LIA: lambda_bend_LIA = (kappa^2 / 4pi) * R * ln(R/xi)")
    print(f"                       = {KAPPA**2/(4*math.pi):.4f} * {R_CAP:.2f} * {math.log(R_CAP):.4f}")
    print(f"                       = {lia_at_cap:.4e}")
    print(f"  SSV core:              {lam_local:.4e}")
    print(f"  Combined:              {lam_local + lia_at_cap:.4e}")
    print(f"  Target phi^3/alpha^3:  {lam_target:.4e}")
    print(f"  Remaining gap:         {lam_target / (lam_local + lia_at_cap):.2f}x")


if __name__ == "__main__":
    main()

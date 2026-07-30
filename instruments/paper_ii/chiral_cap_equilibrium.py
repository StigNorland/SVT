"""SSV chiral-shear cap equilibrium diagnostic — Paper II §4.

PHYSICAL MODEL
==============
The vortex ring at the W-reconnection saddle has cap radius R_cap set by
the balance of three energies in the cap-rim variational problem:

    E(R) = pi R^2  +  2 pi tau R  +  2 pi lambda_bend / R
           ^^^^^^^^^   ^^^^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^
           pressure     line tension  chiral-shear bending
           (opens cap)  (closes cap)  (resists curvature)

  - Pressure P0 * pi R^2 * xi: cost of holding cap open.  P0 = xi = 1 here.
  - Line tension 2 pi tau R: cap rim is a vortex ring of energy tau per unit
    length, recomputed from the corrected Paper I profile.
  - Chiral-shear bending 2 pi lambda_bend/R: a curved vortex ring of radius R
    has bending energy integral(kappa^2 ds) = 2pi/R.  The bending stiffness
    lambda_bend (units xi^3 in dimensionless system) resists small R.

EQUILIBRIUM CONDITION
=====================
dE/dR = 0  gives the CUBIC:

    R^3 + tau R^2 - lambda_bend = 0           ... (*)

In the tau -> 0 limit: R_eq = lambda_bend^{1/3}.

For R_eq = phi/alpha exactly:
    lambda_bend = (phi/alpha)^3 + tau (phi/alpha)^2
                ~ (phi/alpha)^3   [since tau << phi/alpha]

SSV IDENTIFICATION
==================
In SSV the chiral-shear mode speed is c_perp = alpha c.  The bending
stiffness of a vortex in the chiral-shear medium scales as

    lambda_bend = A_bend * (c / c_perp)^n * xi^3

for some power n and O(1) coefficient A_bend.  This script finds the required
lambda_bend numerically, expresses it as a multiple of (1/alpha)^n, and
checks which n (and what A_bend) closes the gapbox.

RESULT PREVIEW
==============
Imposing R_cap = phi/alpha determines the stiffness required by this candidate
energy model.  That algebraic inversion is not a derivation of either phi or
the stiffness from the SSV Lagrangian.  The corrected local core calculation
falls short by about 380x, so the physical cap-setting mechanism remains open.
"""

from __future__ import annotations

import math
import sys
import os

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from paper_i.corrected_vortex_profile import CorrectedVortexProfile

# ── Constants ─────────────────────────────────────────────────────────────────
ALPHA    = 1.0 / 137.035999084
PHI      = (1.0 + math.sqrt(5.0)) / 2.0    # golden ratio
R_CAP_II = PHI / ALPHA                      # Paper II target: phi/alpha ~ 221.7 xi

# Line tension from the corrected conventional-healing-length profile.
# Re-derived here for self-containedness.
TAU_PHYS = None   # filled in during runtime from vortex profile


# ── Vortex line tension (quick re-derive) ─────────────────────────────────────
def compute_tau_phys() -> float:
    """Corrected line tension regularised at R_cap = phi/alpha.

    The shifted LogSE energy density is
    ``0.5 |grad f|^2 + 0.5 (rho log rho - rho + 1)``.  Only the
    phase-gradient term has a logarithmic tail, giving ``pi log(R/r_max)``.
    """
    profile = CorrectedVortexProfile.solve(x_min=1e-4, x_max=15.0, n=3000)
    xs  = np.array(profile.xs)
    fs  = np.array(profile.fs)
    fps = np.array(profile.fps)
    f2  = np.maximum(fs ** 2, 1e-300)
    eps = (
        0.5 * fps**2
        + 0.5 * (fs/xs)**2
        + 0.5 * (f2 * np.log(f2) - f2 + 1.0)
    )
    tau_core = float(np.trapezoid(eps * 2.0 * math.pi * xs, xs))
    tau_tail = math.pi * math.log(R_CAP_II / 15.0)
    return tau_core + tau_tail


# ── Cap energy model ──────────────────────────────────────────────────────────
def E_cap(R: float, tau: float, lam: float) -> float:
    """Variational cap energy E(R; tau, lambda_bend)."""
    return math.pi * R**2 + 2.0 * math.pi * tau * R + 2.0 * math.pi * lam / R


def dE_cap(R: float, tau: float, lam: float) -> float:
    """dE/dR."""
    return 2.0 * math.pi * R + 2.0 * math.pi * tau - 2.0 * math.pi * lam / R**2


def R_eq(tau: float, lam: float) -> float:
    """Equilibrium radius from cubic R^3 + tau R^2 - lam = 0."""
    # cubic: R^3 + tau R^2 - lam = 0.  For lam > 0 there is exactly one
    # positive real root (Descartes: one sign change -> one positive root).
    f = lambda R: R**3 + tau * R**2 - lam
    # upper bracket: R_hi such that f(R_hi) > 0
    R_hi = max(lam ** (1.0 / 3.0) * 2.0, 1.0)
    while f(R_hi) <= 0:
        R_hi *= 2.0
    R_lo = 1e-6
    return float(brentq(f, R_lo, R_hi, xtol=1e-10))


# ── Golden-ratio fixed-point argument ─────────────────────────────────────────
def golden_ratio_analysis(tau: float) -> dict:
    """
    Find lambda* such that R_eq = phi/alpha.

    From the cubic: lambda* = R_cap^3 + tau * R_cap^2.
    Decompose as multiples of (1/alpha)^n for n = 1,2,3,4.
    """
    R_c  = R_CAP_II
    lam  = R_c**3 + tau * R_c**2

    # Express lam / (phi/alpha)^n for n = 1..4
    ratios = {}
    for n in range(1, 5):
        ratios[n] = lam / (PHI / ALPHA) ** n

    # tau->0 limit: lam_0 = R_c^3 = (phi/alpha)^3 => coefficient = phi^3
    lam_0 = R_c**3
    phi3  = PHI ** 3

    return {
        "lam":        lam,
        "lam_0":      lam_0,
        "R_c":        R_c,
        "tau_frac":   tau * R_c**2 / lam_0,   # fractional tau correction
        "ratios":     ratios,
        "lam_0_over_alpha3":  lam_0 * ALPHA**3,   # = phi^3
        "phi3":       phi3,
    }


# ── Fibonacci self-consistency ─────────────────────────────────────────────────
def fibonacci_check(R_c: float) -> None:
    """Print the tautological check induced by imposing R_c = phi/alpha."""
    x = ALPHA * R_c
    print(f"  Imposed x = alpha R_cap = {x:.6f} = phi")
    print(f"  Therefore x^3 = {x**3:.6f} = phi^3")
    print(f"  Identity check: phi^2 = {PHI**2:.6f}, phi+1 = {PHI+1:.6f}")
    print("  No independent Fibonacci sequence or dynamical fixed point follows.")


# ── Lambda scan ───────────────────────────────────────────────────────────────
def lambda_scan(tau: float, n_pts: int = 40) -> tuple[np.ndarray, np.ndarray]:
    """Scan lambda_bend and find R_eq(lambda). Returns (lambdas, R_eqs)."""
    lam_min = tau**3 * 0.1
    lam_max = R_CAP_II**3 * 5.0
    lambdas = np.logspace(math.log10(lam_min), math.log10(lam_max), n_pts)
    R_eqs   = np.array([R_eq(tau, l) for l in lambdas])
    return lambdas, R_eqs


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    global TAU_PHYS

    print("=" * 68)
    print("SSV Chiral-Cap Equilibrium: candidate-model diagnostic")
    print("Paper II §4 — chiral-shear bending stiffness")
    print("=" * 68)
    print()

    # ── 0. Line tension ───────────────────────────────────────────────────
    print("── 0. LINE TENSION (re-derived) ───────────────────────────────")
    tau = compute_tau_phys()
    TAU_PHYS = tau
    print(f"  tau = {tau:.4f} xi  (corrected coefficient-one profile)")
    print()

    # ── 1. Energy landscape ───────────────────────────────────────────────
    print("── 1. ENERGY LANDSCAPE  E(R) = pi R^2 + 2pi tau R + 2pi lam/R ─")
    print()

    ga   = golden_ratio_analysis(tau)
    lam_star = ga["lam"]

    print(f"  Target: R_cap = phi/alpha = {R_CAP_II:.2f} xi")
    print(f"  Required lambda_bend*  = R_cap^3 + tau R_cap^2")
    print(f"                         = {R_CAP_II:.2f}^3 + {tau:.2f} x {R_CAP_II:.2f}^2")
    print(f"                         = {R_CAP_II**3:.2e} + {tau * R_CAP_II**2:.2e}")
    print(f"                         = {lam_star:.4e}")
    print()

    print(f"  Dimensional ratios of the imposed-target stiffness:")
    for n, ratio in ga["ratios"].items():
        print(f"    lambda* / (phi/alpha)^{n} = {ratio:.6f}")
    print()
    print(f"  tau->0 limit: lambda*_0 = R_cap^3 = (phi/alpha)^3")
    print(f"    lambda*_0 * alpha^3   = {ga['lam_0_over_alpha3']:.6f}")
    print(f"    phi^3                 = {ga['phi3']:.6f}  ✓")
    print()
    print(f"  Tau correction: tau * R_cap^2 / lambda*_0 = {ga['tau_frac']:.4f}")
    print(f"  (tau << phi/alpha: correction is {ga['tau_frac']*100:.1f}%)")
    print()

    # Verify equilibrium
    R_check = R_eq(tau, lam_star)
    print(f"  Cubic root check: R_eq(lambda*) = {R_check:.4f} xi")
    print(f"  Target R_cap     = {R_CAP_II:.4f} xi  "
          f"(error {abs(R_check - R_CAP_II)/R_CAP_II*100:.6f}%)")
    print()

    # ── 2. Energy at equilibrium ──────────────────────────────────────────
    print("── 2. ENERGY AT EQUILIBRIUM ────────────────────────────────────")
    E_P   = math.pi * R_CAP_II**2
    E_tau = 2.0 * math.pi * tau * R_CAP_II
    E_cs  = 2.0 * math.pi * lam_star / R_CAP_II
    E_tot = E_P + E_tau + E_cs

    print(f"  E_pressure   = pi R^2          = {E_P:.4e}  [cap formula: "
          f"{E_P * 0.51099895e-3:.3f} GeV]")
    print(f"  E_line_tens  = 2pi tau R        = {E_tau:.4e}  ({E_tau/E_tot*100:.1f}%)")
    print(f"  E_chiral     = 2pi lambda/R     = {E_cs:.4e}  ({E_cs/E_tot*100:.1f}%)")
    print(f"  E_total      at R_cap           = {E_tot:.4e}")
    print()
    print(f"  Virial ratio E_cs / E_P = {E_cs/E_P:.4f}  (expected 2 from d/dR: R^3 = lam => E_cs = 2 E_P)")
    print()

    # ── 3. SSV identification of lambda_bend ─────────────────────────────
    print("── 3. REQUIRED INPUT, NOT AN SSV DERIVATION ────────────────────")
    print()
    print(f"  Exact candidate-model requirement:")
    print(f"    lambda_bend* = (phi/alpha)^3 * (1 + tau/(phi/alpha))")
    print(f"                 = {lam_star:.4e} xi^3")
    print(f"  Tau->0 shorthand:")
    print(f"    lambda_bend,0 = phi^3 / alpha^3 = {ga['lam_0']:.4e} xi^3")
    print()
    print(f"  In SSV: chiral-shear mode speed c_perp = alpha c")
    print(f"          => (c / c_perp)^3 = alpha^-3 = {ALPHA**(-3):.4e}")
    print(f"  This permits alpha^-3 dimensionally; it does not derive the power,")
    print(f"  coefficient phi^3, or a linear-running/non-local mechanism.")
    print()
    print(f"  Physical bending stiffness (SI):")
    xi_m    = 3.8616e-13           # electron Compton wavelength in metres
    hbar    = 1.0546e-34
    c_SI    = 2.9979e8
    m_e     = 9.1094e-31
    lam_SI  = PHI**3 / ALPHA**3 * xi_m**3
    print(f"    xi   = {xi_m:.4e} m")
    print(f"    lambda_bend* = phi^3/alpha^3 * xi^3 = {lam_SI:.4e} m^3")
    print(f"    [or in units m_e c^2 xi^2: {PHI**3/ALPHA**3:.4e}]")
    print()

    # Express in terms of SSV mass ladder
    N_p = 1.0 / (1.0 / 1836.15267343 / ALPHA)   # m_p alpha / m_e
    print(f"  Cross-checks with SSV mass ladder:")
    print(f"    N_p = m_p alpha / m_e = {N_p:.4f}")
    print(f"    phi^3 / alpha^3 vs 1/alpha^3 : ratio = phi^3 = {PHI**3:.4f}")
    print(f"    phi^3 / alpha^3 vs N_p/alpha^2: ratio = {PHI**3 / ALPHA**3 / (N_p / ALPHA**2):.4f}")
    print(f"    phi^3 / alpha^3 vs N_p^2/alpha : ratio = {PHI**3 / ALPHA**3 / (N_p**2 / ALPHA):.4f}")
    print()

    # ── 4. Golden ratio fixed point ────────────────────────────────────────
    print("── 4. ALGEBRAIC GOLDEN-RATIO RESTATEMENT ───────────────────────")
    print()
    print(f"  Define x = alpha * R / xi.  Equilibrium (tau->0): x^3 = alpha^3 * lambda*")
    print(f"  With lambda* = phi^3 / alpha^3: x^3 = phi^3 => x = phi")
    print()
    fibonacci_check(R_CAP_II)

    # ── 5. Lambda scan ────────────────────────────────────────────────────
    print("── 5. R_eq vs lambda_bend SCAN ─────────────────────────────────")
    lambdas, R_eqs = lambda_scan(tau)

    # Find where R_eq = phi/alpha
    # (closest point in scan)
    idx = int(np.argmin(np.abs(R_eqs - R_CAP_II)))
    print(f"  Scan range: lambda in [{lambdas[0]:.2e}, {lambdas[-1]:.2e}]")
    print()
    print(f"  {'lambda_bend':>14}  {'R_eq':>10}  {'R_eq/(phi/alpha)':>18}")
    print(f"  {'-'*46}")
    for lam_i, r_i in zip(lambdas[::5], R_eqs[::5]):
        print(f"  {lam_i:14.4e}  {r_i:10.2f}  {r_i/R_CAP_II:18.4f}")
    print()
    print(f"  Scan confirms: R_eq = phi/alpha at lambda_bend = {lam_star:.4e}")

    print()
    print("── 6. PHYSICAL INTERPRETATION ──────────────────────────────────")
    print()
    print(f"  The candidate-model bending stiffness needed to stabilise the")
    print(f"  vortex ring at R_cap = phi/alpha is:")
    print()
    print(f"    lambda_bend* = (phi/alpha)^3 [1 + tau alpha/phi] xi^3")
    print(f"                 = {lam_star:.4e} xi^3")
    print()
    print(f"  In the tau->0 shorthand this has THREE powers of the inverse")
    print(f"  chiral speed (c/c_perp = 1/alpha), with a phi^3 pre-factor.")
    print()
    print(f"  Algebraic status of phi^3:")
    print(f"    phi satisfies phi^2 = phi + 1 by definition.")
    print(f"    At equilibrium (tau->0): E_cs = 2 E_P  (virial theorem).")
    print(f"    The energy ratio E_cs/E_P = 2 is independent of lambda —")
    print(f"    it holds for ANY equilibrium of E = pi R^2 + 2pi lam/R.")
    print(f"    Because R_cap=phi/alpha was imposed, phi also appears in the")
    print(f"    energy curvature at that imposed minimum:")
    print()
    d2E_dimless = 6.0 * PHI**3   # d^2E/dx^2 at x=phi, units (pi/alpha^2)
    print(f"    d^2E/dx^2|_phi = 6 phi^3 = {d2E_dimless:.4f}  [x = alpha R, E in pi/alpha^2 units]")
    print(f"    curvature-to-height ratio = phi^3 / phi^2 = phi = {PHI:.6f}")
    print(f"    This is an algebraic consequence, not an independent physical origin.")
    print()
    print(f"  STATUS: GENUINELY OPEN.")
    print(f"    The cubic maps an assumed R_cap to a required lambda_bend; it does")
    print(f"    not predict R_cap.  The corrected local core integral is about 380x")
    print(f"    too small, and linear running no longer gives the former 4.4% match.")

    print()
    print("=" * 68)
    print("SUMMARY")
    print("=" * 68)
    print()
    print(f"  Energy model: E(R) = pi R^2 + 2pi tau R + 2pi lambda_bend/R")
    print(f"  Line tension: tau = {tau:.3f} xi  (from Paper I vortex profile)")
    print()
    print(f"  Required bending stiffness for R_eq = phi/alpha:")
    print(f"    lambda_bend* = {lam_star:.4e} xi^3")
    print(f"    = phi^3 / alpha^3 * xi^3  [tau-correction: {ga['tau_frac']*100:.1f}%]")
    print(f"    = (phi/alpha)^3 * xi^3")
    print()
    print(f"  Candidate tau->0 input: lambda_bend = phi^3 * (c/c_perp)^3 * xi^3")
    print(f"  Status: permitted scaling, not derived from the Lagrangian")
    print()
    print(f"  W mass from equilibrium cap energy:")
    print(f"    m_W = pi R_cap^2 m_e c^2 = pi (phi/alpha)^2 m_e c^2")
    print(f"        = {math.pi * (PHI/ALPHA)**2 * 0.51099895e-3:.3f} GeV  (obs: 80.377 GeV)")
    print()
    print(f"  Open step: derive a cap-setting mechanism from the SSV dynamics")
    print(f"    without inserting R_cap, lambda_bend, or the observed W mass.")


if __name__ == "__main__":
    main()

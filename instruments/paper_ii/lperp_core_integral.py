"""SSV chiral-shear bending stiffness: L_perp core integral — Paper II §4.

Computes the core integrals that determine the bending modulus of a vortex ring
from the SSV chiral-shear Lagrangian term:

    L_perp = (lambda_perp / 2) int |curl j|^2 d^3r

Three integrals are computed from the Paper I planar vortex profile f(r):

  I_curl = int (2ff'/r)^2 2pi r dr            (straight-vortex L_perp density)
  J_bend = int r^2 [d/dr(2ff'/r)]^2 2pi r dr  (core curvature-correction)
  K_bend = int (2ff'/r)^2 r^2 2pi r dr        (metric-Jacobian correction)

Physical interpretation of the bending formula
----------------------------------------------
When a vortex ring of radius R is bent with curvature kappa = 1/R, the
curvature-induced correction to the L_perp energy per unit ring length is
(leading order in kappa):

    delta(E_perp/length) = (lambda_perp/4) * kappa^2 * J_bend

Multiplied by the circumference 2pi R:
    E_bend = pi lambda_perp J_bend / (2R)

Comparing with the model 2pi lambda_bend/R:
    lambda_bend_LOCAL = lambda_perp * J_bend / 4  (local curvature correction)

Similarly, the metric-Jacobian correction to the L_perp energy of a torus with
tube radius ~ xi contributes (angular average of cos^2 = 1/2):
    lambda_bend_METRIC = lambda_perp * K_bend / 4

Total from BOTH contributions:
    lambda_bend_TOTAL = lambda_perp * (J_bend + K_bend) / 4

The SSV natural coupling from c_perp = alpha c at scale xi:
    lambda_perp_natural = alpha^-2   (k^4 dispersion, omega = c_perp k at k=1/xi)

IMPORTANT NOTE ON DOMAIN:
The planar vortex profile has an algebraic tail 1-f ~ 1/(4r^2) which does NOT
cause problems for I_curl and K_bend (they converge). However, the forward
shooting integration becomes contaminated by growing modes beyond r~15 xi.
All integrals must be evaluated only up to r_max=15 xi. The tail contributions
beyond this are analytically negligible (see below).

KEY RESULT: The local curvature correction gives lambda_bend a factor ~300
below the required phi^3/alpha^3. This implies the 2pi lambda_bend/R energy
term does NOT arise from local vortex core bending but from a more global
physical mechanism — likely the chiral-mode confinement energy in the cap
(analogous to a bag model) or a non-local chiral-shear interaction.

Reference: chiral_cap_equilibrium.py (requires lambda_bend = phi^3/alpha^3).
"""

from __future__ import annotations

import math
import sys

import numpy as np

sys.path.insert(0, "instruments/paper_i")
from vortex_profile import VortexProfile  # noqa: E402 (path insert above)


ALPHA = 1.0 / 137.035999084
PHI = (1.0 + math.sqrt(5.0)) / 2.0
R_MAX_RELIABLE = 15.0   # growing-mode contamination beyond this


def compute_core_integrals(
    r: np.ndarray,
    f: np.ndarray,
    fp: np.ndarray,
    r_max: float,
) -> tuple[float, float, float]:
    """Compute I_curl, J_bend, K_bend up to r_max.

    Uses np.gradient for d/dr(curl_j) to avoid catastrophic cancellation
    at small r (where f'^2/r - ff'/r^2 ~ slope^2/r - slope^2/r ~ 0).
    """
    mask = r <= r_max
    r_m = r[mask]
    f_m = f[mask]
    fp_m = fp[mask]
    r_s = np.maximum(r_m, 1.0e-12)

    curl_j = 2.0 * f_m * fp_m / r_s                          # (2ff'/r)
    d_curl = np.gradient(curl_j, r_m)                        # d/dr(2ff'/r)

    i_curl = float(np.trapezoid(curl_j**2 * 2.0 * math.pi * r_m, r_m))
    j_bend = float(np.trapezoid(r_m**2 * d_curl**2 * 2.0 * math.pi * r_m, r_m))
    k_bend = float(np.trapezoid(curl_j**2 * r_m**2 * 2.0 * math.pi * r_m, r_m))
    return i_curl, j_bend, k_bend


def analytic_tail(r0: float) -> tuple[float, float, float]:
    """Estimate the tail contributions from r0 to inf using f ~ 1 - 1/(4r^2).

    curl_j = 2ff'/r ~ 1/r^4  (from f'~1/(2r^3), f~1)
    d/dr(curl_j) ~ -4/r^5

    I_curl_tail = int (1/r^4)^2 * 2pi*r dr = 2pi int 1/r^7 dr = 2pi/(6 r0^6)
    J_bend_tail = int r^2 * (4/r^5)^2 * 2pi*r dr = 32pi int 1/r^7 dr = 32pi/(6 r0^6)
    K_bend_tail = int (1/r^4)^2 * r^2 * 2pi*r dr = 2pi int 1/r^5 dr = 2pi/(4 r0^4)
    """
    i_curl_tail = 2.0 * math.pi / (6.0 * r0**6)
    j_bend_tail = 32.0 * math.pi / (6.0 * r0**6)
    k_bend_tail = 2.0 * math.pi / (4.0 * r0**4)
    return i_curl_tail, j_bend_tail, k_bend_tail


def main() -> None:
    n_pts = 4000
    x_max_solve = 15.0   # reliable limit for forward shooting
    print("=" * 68)
    print("SSV L_perp core integral — Paper II §4 bending stiffness check")
    print("=" * 68)
    print(f"  Profile: b=1 convention, n={n_pts}, x_max={x_max_solve} xi")
    print(f"  Reliable integration up to r_max = {R_MAX_RELIABLE} xi")
    print(f"  (Growing mode contamination beyond this radius)")
    print()

    vp = VortexProfile.solve(n=n_pts, x_max=x_max_solve)
    r = np.array(vp.xs)
    f = np.array(vp.fs)
    fp = np.array(vp.fps)

    print(f"  Vortex slope a (f ~ a*r)    = {vp.slope:.6f}")
    print(f"  f(r_max) = {float(f[-1]):.8f}  (target 1)")
    print()

    # ── Core integrals ────────────────────────────────────────────────────────
    i_curl, j_bend, k_bend = compute_core_integrals(r, f, fp, R_MAX_RELIABLE)
    i_tail, j_tail, k_tail = analytic_tail(R_MAX_RELIABLE)

    print("── 1. CORE INTEGRALS (b=1 convention, r < 15 xi) ───────────────")
    print(f"  I_curl = int (2ff'/r)^2 * 2pi r dr        = {i_curl:.6f}")
    print(f"  J_bend = int r^2 [d/dr(2ff'/r)]^2 * 2pi r dr = {j_bend:.6f}")
    print(f"  K_bend = int (2ff'/r)^2 r^2 * 2pi r dr    = {k_bend:.6f}")
    print()
    print(f"  Analytic tail r > {R_MAX_RELIABLE:.0f} xi (f ~ 1 - 1/(4r^2)):")
    print(f"    I_curl_tail = 2pi/(6*r0^6) = {i_tail:.3e}  (negligible)")
    print(f"    J_bend_tail = 32pi/(6*r0^6) = {j_tail:.3e}  (negligible)")
    print(f"    K_bend_tail = 2pi/(4*r0^4) = {k_tail:.3e}  (small for K)")
    print(f"  Fractional J_bend tail: {j_tail/j_bend:.2e}")
    print()

    # ── Bending stiffness formulae ────────────────────────────────────────────
    lam_perp_natural = 1.0 / ALPHA**2       # alpha^{-2}
    lam_bend_target = PHI**3 / ALPHA**3     # phi^3/alpha^3

    lam_bend_J = lam_perp_natural * j_bend / 4.0
    lam_bend_K = lam_perp_natural * k_bend / 4.0
    lam_bend_local = lam_perp_natural * (j_bend + k_bend) / 4.0

    print("── 2. BENDING STIFFNESS FROM L_perp CORE CORRECTIONS ──────────")
    print(f"  SSV natural coupling lambda_perp = alpha^{{-2}} = {lam_perp_natural:.4e}")
    print()
    print("  Formula: lambda_bend = lambda_perp * (J_bend + K_bend) / 4")
    print(f"    Curvature correction (J_bend/4):     {lam_bend_J:.4e}")
    print(f"    Metric correction   (K_bend/4):     {lam_bend_K:.4e}")
    print(f"    Total (local):                       {lam_bend_local:.4e}")
    print(f"    Required (phi^3/alpha^3):            {lam_bend_target:.4e}")
    print(f"    Gap factor (required/local):         {lam_bend_target/lam_bend_local:.1f}  <-- factor missing!")
    print()

    # ── Golden ratio coincidences ─────────────────────────────────────────────
    phi3_over_alpha = PHI**3 / ALPHA
    print("── 3. GOLDEN-RATIO STRUCTURE IN CORE INTEGRALS ────────────────")
    print(f"  phi^3/alpha = {phi3_over_alpha:.4f}")
    print(f"  J_bend / (phi^3/alpha) = {j_bend/phi3_over_alpha:.6f}")
    print(f"  K_bend / (phi^3/alpha) = {k_bend/phi3_over_alpha:.6f}")
    print(f"  I_curl (straight density, per unit length) = {i_curl:.4f}")
    print()
    print("  Ratio J_bend / I_curl = "
          f"{j_bend/i_curl:.4f}  (bending vs straight-line stiffness)")
    print()

    # ── Physical interpretation ───────────────────────────────────────────────
    print("── 4. PHYSICAL INTERPRETATION ──────────────────────────────────")
    print()
    print(f"  The local curvature correction to L_perp gives:")
    print(f"    lambda_bend_local = {lam_bend_local:.3e}  (factor {lam_bend_target/lam_bend_local:.0f} too small)")
    print()
    print(f"  Required for cap equilibrium at R_cap = phi/alpha = {PHI/ALPHA:.1f} xi:")
    print(f"    lambda_bend* = phi^3/alpha^3 = {lam_bend_target:.3e}")
    print()
    print(f"  CONCLUSION: The 2pi*lambda_bend/R energy term does NOT arise")
    print(f"  from local vortex core bending (curvature correction to L_perp).")
    print(f"  The physical mechanism requires a global / non-local effect:")
    print()
    print(f"  Candidate mechanisms:")
    print(f"    (a) Chiral-mode confinement energy in the cap (bag-model):")
    print(f"        Lowest chiral mode in disk of radius R has energy ~ c_perp/R = alpha/R.")
    print(f"        For phi^3/alpha^3 modes filling the cap: N_modes ~ (phi/alpha)^2 ~ R^2.")
    print(f"        E_conf ~ N_modes * alpha/R ~ phi^2 R -- scales as R, not 1/R.")
    print()
    print(f"    (b) Chiral-shear vacuum energy of the reconnection region:")
    print(f"        The cap boundary (vortex ring) is a source for the chiral")
    print(f"        mode. The chiral mode's Green function at distance R ~ 1/(alpha R)")
    print(f"        gives E_boundary ~ 2pi R * lambda_perp * (1/alpha R)^2")
    print(f"                         = 2pi lambda_perp / (alpha^2 R)")
    print(f"        => lambda_bend ~ lambda_perp / alpha^2 = alpha^{{-4}} (too large).")
    print()
    print(f"    (c) Non-perturbative topological origin:")
    print(f"        The cap is a topological object (Seifert surface of the trefoil).")
    print(f"        The chiral shear energy of the Seifert surface may be quantized")
    print(f"        at lambda_bend = phi^3/alpha^3 from the knot invariant structure.")
    print(f"        This is the most likely Paper II §4 mechanism.")
    print()

    # ── Required lambda_perp ─────────────────────────────────────────────────
    lam_perp_needed = 4.0 * lam_bend_target / (j_bend + k_bend)
    print("── 5. REQUIRED lambda_perp FOR LOCAL FORMULA TO WORK ───────────")
    print(f"  If formula lambda_bend = lambda_perp*(J+K)/4 is used:")
    print(f"    lambda_perp_needed = 4*phi^3/alpha^3 / (J+K)")
    print(f"                       = {lam_perp_needed:.4e}")
    print(f"    vs natural alpha^{{-2}}  = {lam_perp_natural:.4e}")
    print(f"    enhancement factor     = {lam_perp_needed/lam_perp_natural:.1f}")
    print()
    print(f"  For the formula to work with alpha^{{-2}}, the core integral")
    print(f"  J+K would need to equal 4*phi^3/alpha = {4*PHI**3/ALPHA:.1f}")
    print(f"  vs computed J+K = {j_bend+k_bend:.2f}  (factor {4*PHI**3/ALPHA/(j_bend+k_bend):.0f} short)")
    print()

    # ── Summary ────────────────────────────────────────────────────────────────
    print("=" * 68)
    print("SUMMARY")
    print("=" * 68)
    print()
    print(f"  Core integrals (b=1, reliable r < 15 xi):")
    print(f"    I_curl = {i_curl:.4f}  (L_perp density per unit ring length)")
    print(f"    J_bend = {j_bend:.4f}  (curvature correction to L_perp)")
    print(f"    K_bend = {k_bend:.4f}  (metric Jacobian correction)")
    print()
    print(f"  Bending stiffness from local L_perp correction:")
    print(f"    lambda_bend(local) = {lam_bend_local:.3e}  (lambda_perp=alpha^-2, J+K/4)")
    print(f"    lambda_bend(reqd)  = {lam_bend_target:.3e}  (phi^3/alpha^3)")
    print(f"    Gap factor         = {lam_bend_target/lam_bend_local:.0f}x")
    print()
    print(f"  OPEN GAPBOX (Paper II §4):")
    print(f"    The 2pi lambda_bend/R bending energy at R_cap = phi/alpha")
    print(f"    cannot be reproduced by local L_perp curvature corrections alone.")
    print(f"    The physical origin must be non-local (topological cap energy,")
    print(f"    chiral-shear vacuum contribution, or knot-invariant quantization).")


if __name__ == "__main__":
    main()

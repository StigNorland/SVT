"""SSV vortex cap mass: W/Z masses from reconnection end-cap — Paper II §4.

Connects the Paper I vortex-core profile to Paper II's cap-energy formula for
the W-boson mass and the Weinberg angle.

PHYSICAL PICTURE (Paper II §4):
  W boson = saddle of two approaching charged vortex rings.
  The reconnection passes through a momentary open-ended vortex tube.
  Dominant energy: end-cap cost  E_cap = P0 * pi * R_cap^2 * xi.
  Golden-ratio conjecture:       R_cap = phi * xi / alpha.
  => m_W = pi * (phi/alpha)^2 * m_e * c^2 = 78.9 GeV.

THREE SECTIONS:

1. VORTEX LINE TENSION (numerical) — imports the Paper I 2D LogSE solver.
   The line tension tau diverges logarithmically (IR divergence from the
   1/r^2 phase-gradient tail), but is finite and well-defined when
   regularised at R_cap.

2. CAP ENERGY vs FORCE BALANCE — shows that the pure LogSE line tension
   gives R_cap^LogSE ≈ tau_{b=1/2} ≈ 14 xi from a naive surface-tension
   estimate, a factor ~15 below the golden-ratio value phi/alpha ≈ 222 xi.
   The discrepancy quantifies how much additional stiffness the chiral-shear
   term (lambda_perp ~ 2000) must supply.

3. W/Z MASSES AND WEINBERG ANGLE — Paper II golden-ratio analytic formula
   for m_W; tree-level SM mass ratio for m_Z; sin^2(theta_W) = 0.231 as
   experimental input (predicting it from chiral-shear mixing is an open
   gapbox for Paper II §4).

Conventions:
  - Paper I (vortex_profile.py) uses b=1 convention:
      ODE: f'' + (1/r) f' - f/r^2 = 2 f ln(f^2)
  - Physical (cap-formula) uses b=1/2 convention:
      ODE: f'' + (1/r) f' - f/r^2 = f ln(f^2)
  - Relation: f_phys(r) = f_b1(r/sqrt(2))  =>  tau_phys = tau_b1 / 2
              xi_b1 = xi_phys / sqrt(2)
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from paper_i.vortex_profile import VortexProfile

# ── Physical constants (CODATA 2018) ─────────────────────────────────────────
ME_C2_GEV  = 0.51099895e-3            # m_e c^2 in GeV
ALPHA      = 1.0 / 137.035999084      # fine-structure constant
PHI_GR     = (1.0 + math.sqrt(5.0)) / 2.0   # golden ratio ≈ 1.618034
SQRT2      = math.sqrt(2.0)

M_W_OBS    = 80.377    # GeV  (PDG 2023)
M_Z_OBS    = 91.188    # GeV
SIN2_THW   = 0.23122   # PDG 2023 (MS-bar scheme)

# ── Solver parameters ─────────────────────────────────────────────────────────
R_MAX_B1   = 15.0   # paper_i integration limit (forward shooting stable here)
N_PROFILE  = 3000   # radial grid points


# ── Line tension ──────────────────────────────────────────────────────────────
def line_tension(profile: VortexProfile, r_max: float) -> dict[str, float]:
    """Vortex line tension in paper_i (b=1) units, regularised at R_cap.

    tau = integral of energy density 2 pi r dr from 0 to r_max,
    plus analytic tail correction.

    Energy density (b=1 convention):
        eps = 0.5 (f')^2 + 0.5 (f/r)^2 - f^2 ln(f^2)
              ^^^^^^^^^^   ^^^^^^^^^^^^   ^^^^^^^^^^^
              radial kin.  winding phase  LogSE potential

    Algebraic tail (verified numerically): 1-f ~ 1/(4r^2) for large r.
    This arises from the -f/r^2 winding term, which sources an algebraic
    correction to the background.  Consequence: BOTH kin_p and pot decay
    as ~ 1/(2r^2), each giving a pi ln(R) contribution to the integral.
    Total tail: 2 pi ln(R_cap/r_max)  [NOT pi — both terms contribute].
    """
    xs  = np.array(profile.xs)
    fs  = np.array(profile.fs)
    fps = np.array(profile.fps)

    mask = xs <= r_max
    xs, fs, fps = xs[mask], fs[mask], fps[mask]

    f2    = np.maximum(fs ** 2, 1.0e-300)
    kin_r = 0.5 * fps ** 2
    kin_p = 0.5 * (fs / xs) ** 2
    pot   = -f2 * np.log(f2)
    eps   = kin_r + kin_p + pot

    tau_core = float(np.trapezoid(eps * 2.0 * np.pi * xs, xs))

    # Analytic tail: kin_p ~ 1/(2r^2) AND pot ~ 1/(2r^2) for large r.
    # Each contributes pi ln(R_cap/r_max); total is 2 pi ln(R_cap/r_max).
    R_cap_b1  = PHI_GR / ALPHA / SQRT2   # R_cap in paper_i xi units
    tau_tail  = 2.0 * math.pi * math.log(R_cap_b1 / r_max) if R_cap_b1 > r_max else 0.0

    tau_b1    = tau_core + tau_tail
    tau_phys  = tau_b1 / 2.0   # physical (b=1/2) units

    return {
        "tau_core_b1":  tau_core,
        "tau_tail_b1":  tau_tail,
        "tau_b1":       tau_b1,
        "tau_phys":     tau_phys,
        "R_cap_b1":     R_cap_b1,
    }


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    R_cap_phys = PHI_GR / ALPHA   # Paper II golden-ratio cap radius [xi_physical]

    print("=" * 68)
    print("SSV Vortex Cap Mass: W/Z masses — Paper II §4")
    print("=" * 68)
    print()

    # ── 1. Vortex core profile ─────────────────────────────────────────────
    print("── 1. VORTEX CORE PROFILE (Paper I, b=1 convention) ──────────")
    profile = VortexProfile.solve(x_min=1.0e-4, x_max=R_MAX_B1, n=N_PROFILE)
    slope   = profile.slope

    print(f"  2D cylindrical LogSE, n=1 winding:  r in [1e-4, {R_MAX_B1}], n = {N_PROFILE}")
    print(f"  Core slope a (f ~ a*r):  a = {slope:.6f}")
    print()
    print(f"  Profile values:")
    for r in (0.5, 1.0, 2.0, 5.0, 10.0, 15.0):
        print(f"    f({r:5.1f} xi_b1) = {profile.value(r):.8f}")
    print()

    # Core radii (bisection)
    def bisect_f(target: float, lo: float, hi: float, n: int = 60) -> float:
        for _ in range(n):
            mid = 0.5 * (lo + hi)
            (lo if profile.value(mid) < target else hi).__class__  # type check
            if profile.value(mid) < target:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    r50_b1 = bisect_f(0.5, 0.01, 3.0)
    r90_b1 = bisect_f(0.9, 0.5,  8.0)
    r50_ph = r50_b1 * SQRT2   # physical xi units
    r90_ph = r90_b1 * SQRT2
    print(f"  Core radii (xi_b1):  r(f=0.5) = {r50_b1:.4f},  r(f=0.9) = {r90_b1:.4f}")
    print(f"  Core radii (xi_phys): r(f=0.5) = {r50_ph:.4f},  r(f=0.9) = {r90_ph:.4f}")
    print(f"  Physical interpretation: vortex core ≈ 1 xi (by definition of xi)")
    print()

    # Algebraic tail check: 1-f ~ 1/(4r^2) for large r.
    # The -f/r^2 winding term sources an algebraic (not exponential) approach to 1.
    for r_chk in (5.0, 8.0, 10.0, 12.0):
        fv   = profile.value(r_chk)
        dev  = 1.0 - fv
        alg  = 1.0 / (4.0 * r_chk ** 2)
        print(f"    r={r_chk:5.1f}  1-f={dev:.7f}  1/(4r^2)={alg:.7f}  "
              f"ratio={dev/alg:.4f}")
    print()

    # ── 2. Line tension ───────────────────────────────────────────────────
    print("── 2. VORTEX LINE TENSION ─────────────────────────────────────")
    lt = line_tension(profile, R_MAX_B1)
    tau_b1   = lt["tau_b1"]
    tau_phys = lt["tau_phys"]
    R_cap_b1 = lt["R_cap_b1"]

    print(f"  Integration up to r_max = {R_MAX_B1} xi_b1:")
    print(f"    tau_core (numerical)   = {lt['tau_core_b1']:.4f}  [b=1 dimless]")
    print(f"    tau_tail (analytic,    = {lt['tau_tail_b1']:.4f}")
    print(f"      2 pi ln({R_cap_b1:.1f}/{R_MAX_B1}):")
    print(f"      both kin_p and pot ~ 1/(2r^2) => 2 pi ln(R_cap/r_max))")
    print(f"    tau_total  (b=1)       = {tau_b1:.4f}")
    print(f"    tau_total  (b=1/2)     = {tau_phys:.4f}  [physical, tau_b1/2 = tau_b1/2]")
    print()

    # Naive surface-tension estimate for R_cap:
    # Assume the tube terminates at a cap held open by line tension.
    # The tube length decreases at rate tau (force pulling caps together).
    # The cap energy P0 * pi * R_cap^2 (b=1/2 units, P0=1) resists closure.
    # Saddle condition: d/dR_cap [pi R_cap^2] = 2 pi R_cap = force from line tension.
    # But the LINE TENSION acts along the tube axis, not radially. The radial
    # force on the cap rim is instead from the tube-wall curvature.
    # Simplified estimate: R_cap ~ tau_phys (line tension balances cap surface tension).
    R_cap_LogSE = tau_phys   # rough lower bound from LogSE alone
    factor      = R_cap_phys / R_cap_LogSE

    print(f"  Naive LogSE cap estimate:  R_cap ~ tau_phys = {R_cap_LogSE:.1f} xi")
    print(f"  Paper II golden ratio:     R_cap = phi/alpha = {R_cap_phys:.1f} xi")
    print(f"  Enhancement factor needed: {factor:.1f}")
    print()
    print(f"  Interpretation:")
    print(f"    Pure LogSE cannot stabilise a cap at R_cap = {R_cap_phys:.0f} xi.")
    print(f"    The chiral-shear coupling lambda_perp ~ alpha^(-2) ~ {ALPHA**(-2):.0f}")
    print(f"    adds k^4 stiffness that pushes the equilibrium cap radius to phi/alpha.")
    print(f"    This is the open chiral-shear calculation in Paper II §4.")
    print()

    # ── 3. W/Z masses and Weinberg angle ─────────────────────────────────
    print("── 3. W/Z MASSES AND WEINBERG ANGLE (Paper II analytic) ───────")
    print()

    # W mass: E_cap = pi R_cap^2 m_e c^2  (P0 = xi = 1, b=1/2 convention)
    m_W_SSV = math.pi * (R_cap_phys ** 2) * ME_C2_GEV
    gap_W   = (1.0 - m_W_SSV / M_W_OBS) * 100.0
    print(f"  m_W = pi * (phi/alpha)^2 * m_e c^2")
    print(f"      = pi * {R_cap_phys:.2f}^2 * {ME_C2_GEV*1e3:.4f} MeV")
    print(f"      = {m_W_SSV:.3f} GeV  (observed: {M_W_OBS:.3f} GeV,  gap = {gap_W:.2f}%)")
    print()

    # Z mass from tree-level SM: cos(theta_W) = m_W / m_Z
    cos_tW   = math.sqrt(1.0 - SIN2_THW)   # from PDG sin^2(theta_W)
    m_Z_SSV  = m_W_SSV / cos_tW
    gap_Z    = (1.0 - m_Z_SSV / M_Z_OBS) * 100.0
    print(f"  Tree-level: cos(theta_W) = sqrt(1 - sin^2(theta_W)) = {cos_tW:.5f}")
    print(f"  m_Z = m_W / cos(theta_W) = {m_Z_SSV:.3f} GeV  "
          f"(observed: {M_Z_OBS:.3f} GeV,  gap = {gap_Z:.2f}%)")
    print()

    # What R_cap_Z would give the observed m_Z (for a Z cap formula analogue)?
    R_cap_Z_implied = math.sqrt(M_Z_OBS / (math.pi * ME_C2_GEV))
    ratio_caps      = R_cap_Z_implied / R_cap_phys
    print(f"  Implied R_cap_Z from obs m_Z:  {R_cap_Z_implied:.2f} xi")
    print(f"  R_cap_Z / R_cap_W = {ratio_caps:.4f}")
    print(f"  1/cos(theta_W)    = {1/cos_tW:.4f}  (tree-level prediction for ratio)")
    print(f"  sqrt(phi)         = {math.sqrt(PHI_GR):.4f}  (golden-ratio sub-conjecture)")
    print()

    # Effective sin^2(theta_W) from mass ratio only
    cos_tW_mass  = M_W_OBS / M_Z_OBS
    sin2_tW_mass = 1.0 - cos_tW_mass ** 2
    print(f"  sin^2(theta_W) consistency check:")
    print(f"    From PDG (direct):             {SIN2_THW:.5f}")
    print(f"    From observed m_W/m_Z:         {sin2_tW_mass:.5f}")
    print(f"    Discrepancy (radiative corr.): {abs(SIN2_THW - sin2_tW_mass):.5f}")
    print()
    print(f"  Paper II prediction:")
    print(f"    m_W is determined by R_cap = phi/alpha.  ✓ (gap {gap_W:.2f}%)")
    print(f"    sin^2(theta_W) = 0.231 should follow from chiral-shear mixing at the")
    print(f"    Z saddle.  Open gapbox — requires full lambda_perp calculation.")
    print()

    # ── 4. Summary ────────────────────────────────────────────────────────
    print("=" * 68)
    print("SUMMARY")
    print("=" * 68)
    print()
    print(f"  Vortex profile (Paper I, b=1 conv.):")
    print(f"    Core slope a       = {slope:.6f}")
    print(f"    Line tension tau   = {tau_b1:.2f} [b=1]  =  {tau_phys:.2f} [b=1/2, phys]")
    print()
    print(f"  Cap radius:")
    print(f"    R_cap (LogSE only) = {R_cap_LogSE:.1f} xi   (line tension estimate)")
    print(f"    R_cap (Paper II)   = {R_cap_phys:.1f} xi   (phi/alpha, golden ratio)")
    print(f"    Enhancement needed = {factor:.1f}x  [chiral-shear lambda_perp ~ {ALPHA**(-2):.0f}]")
    print()
    print(f"  Electroweak masses (Paper II cap formula + tree-level SM):")
    print(f"    m_W = {m_W_SSV:.3f} GeV  (obs {M_W_OBS:.3f} GeV,  {gap_W:.2f}% gap)")
    print(f"    m_Z = {m_Z_SSV:.3f} GeV  (obs {M_Z_OBS:.3f} GeV,  {gap_Z:.2f}% gap)")
    print()
    print(f"  Open gapboxes for Paper II §4:")
    print(f"    (i)  Derive R_cap = phi/alpha from chiral-shear equilibrium")
    print(f"    (ii) Derive sin^2(theta_W) = 0.231 from amplitude/phase cap mixing")


if __name__ == "__main__":
    main()

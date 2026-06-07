"""1D spherically symmetric proton breather profile — Paper II.

Solves the radial dimensionless LogSE exterior to a hard-sphere proton core
at r_core = a_p = m_e/m_p (in units of xi). Produces two results:

1. STATIC PROFILE  — the equilibrium density healing layer outside the proton
   core, characterised by the deficit volume DV, RMS radius, and asymptotic
   amplitude A*.

2. BJERKNES ANALYSIS  — evaluates the gravitational coupling using the Paper II
   formula (§Newton's Constant).  The key physical argument here is FREQUENCY
   SEPARATION: the proton pulsates at omega_p = m_p c^2/hbar, while the healing
   layer's natural Bogoliubov mode frequency is omega_0 = sqrt(2) c / xi.
   Since omega_p >> omega_0, the healing layer is frozen on the proton's fast
   time scale and does NOT contribute to the Bjerknes radiation.  Only the core
   volume V_0 enters the dynamic Bjerknes formula.

   The calculation shows that the Paper II analytical estimate gives
   alpha_G ~ 1.6e-33, a factor ~3e5 above CODATA (5.9e-39).  This residual
   factor is the open problem for the 3D trefoil calculation (src/paper_i/).

Paper II reference: §Gravity, eqs. (G_from_medium), (Qp), (G_ladder).

Dimensionless LogSE (xi = 1, rho0 = 1, c = 1, hbar = 1, m0 = m_e = 1):
    f'' + (2/r) f' = ln(f^2) f

Boundary conditions:
    f(r_core) = 0    [Dirichlet at hard-sphere proton core]
    f(r) -> 1        [returns to background]

Asymptotic form: f ~ 1 - A* exp(-sqrt(2) r) / r   (decaying mode, B=0)

Numerical method: BACKWARD SHOOTING (stable; avoids growing-mode contamination).
"""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


# ── Physical constants (CODATA 2018) ─────────────────────────────────────────
ME_OVER_MP = 1.0 / 1836.15267343
ALPHA = 1.0 / 137.035999084
ALPHA_G_CODATA = 5.9062e-39         # G m_p^2 / (hbar c)
N_P = 1.0 / (ME_OVER_MP / ALPHA)   # m_p * alpha / m_e ≈ 13.40

R_CORE = ME_OVER_MP                 # a_p / xi  (dimensionless)
SQRT2 = math.sqrt(2.0)


# ── Radial LogSE ODE ──────────────────────────────────────────────────────────
def _rhs(r: float, y: np.ndarray) -> np.ndarray:
    """f'' + (2/r) f' = ln(f^2) f"""
    f, fp = float(y[0]), float(y[1])
    r_s = max(r, 1.0e-15)
    f_s = max(abs(f), 1.0e-150)     # floor prevents log(0)
    fpp = math.copysign(f_s, f) * math.log(f_s * f_s) - 2.0 * fp / r_s
    return np.array([fp, fpp])


# ── Backward shooting ─────────────────────────────────────────────────────────
def _asymptotic_ic(r_max: float, A: float) -> tuple[float, float]:
    """f and f' from decaying asymptotic f ~ 1 - A exp(-sqrt2 r) / r."""
    e = math.exp(-SQRT2 * r_max)
    f = 1.0 - A * e / r_max
    fp = A * e * (SQRT2 * r_max + 1.0) / r_max**2
    return f, fp


def integrate_inward(
    A: float, r_core: float, r_max: float, n_pts: int = 6000,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate from r_max -> r_core with asymptotic IC; return (r, f) ascending."""
    f0, fp0 = _asymptotic_ic(r_max, A)
    sol = solve_ivp(
        _rhs,
        (r_max, r_core),
        np.array([f0, fp0]),
        t_eval=np.linspace(r_max, r_core, n_pts),
        method="RK45",
        rtol=1.0e-11,
        atol=1.0e-13,
    )
    return sol.t[::-1], sol.y[0, ::-1]


def find_amplitude(r_core: float, r_max: float) -> float:
    """Bisect over A > 0 to find A* with f(r_core) = 0."""
    def residual(A: float) -> float:
        _, f = integrate_inward(A, r_core, r_max)
        return float(f[0])

    A_lo, A_hi = r_core * 1.0e-3, r_core * 1.0e6
    r_lo, r_hi = residual(A_lo), residual(A_hi)

    if r_lo * r_hi > 0:
        log_lo, log_hi = math.log10(A_lo), math.log10(A_hi)
        for i in range(1, 41):
            A_try = 10.0 ** (log_lo + i * (log_hi - log_lo) / 40)
            r_try = residual(A_try)
            if r_try * r_lo < 0:
                A_hi, r_hi = A_try, r_try
                break
            r_lo, A_lo = r_try, A_try

    A_star = brentq(residual, A_lo, A_hi, xtol=A_lo * 1.0e-8, rtol=1.0e-8)
    return float(A_star)


# ── Observables ───────────────────────────────────────────────────────────────
def deficit_volume(r: np.ndarray, f: np.ndarray, r_core: float) -> float:
    """DV = V_core + healing-layer integral of (1 - f^2) 4pi r^2 dr."""
    v_core = (4.0 / 3.0) * math.pi * r_core**3
    v_heal = float(np.trapezoid((1.0 - f**2) * 4.0 * math.pi * r**2, r))
    return v_core + v_heal


def rms_radius(r: np.ndarray, f: np.ndarray, r_core: float) -> float:
    num = float(np.trapezoid((1.0 - f**2) * r**2 * 4.0 * math.pi * r**2, r))
    denom = deficit_volume(r, f, r_core)
    return math.sqrt(num / denom) if denom > 1.0e-30 else float("nan")


# ── Bjerknes / G calculation ──────────────────────────────────────────────────
def bjerknes_alpha_g(delta_V: float, r_core: float) -> dict[str, float]:
    """Compute alpha_G from Paper II Bjerknes formula.

    Paper II (§Newton's Constant):
        G = rho0 omega_p^2 Q_eff^2 / (8 pi m_p^2)
        Q_eff = delta_V * (a_p/xi)^3     [sub-grain suppression]

    In dimensionless units (xi = rho0 = c = hbar = m_e = 1):
        m_p = 1/r_core,  omega_p = m_p,  (a_p/xi)^3 = r_core^3

    G_dimless relates to alpha_G via Paper II ladder:
        G = alpha_G hbar c alpha^2 / (N_p^2 m_e^2)
        => alpha_G = G_dimless * N_p^2 / alpha^2
    """
    m_p = 1.0 / r_core
    eta = r_core**3             # (a_p/xi)^3
    Q_eff = delta_V * eta
    G_d = m_p**2 * Q_eff**2 / (8.0 * math.pi * m_p**2)   # omega_p^2/m_p^2 = 1
    alpha_G = G_d * N_P**2 / ALPHA**2
    return {"eta": eta, "Q_eff": Q_eff, "G_dimless": G_d, "alpha_G": alpha_G,
            "ratio": alpha_G / ALPHA_G_CODATA}


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    r_core = R_CORE
    r_max = 12.0
    n_pts = 6000

    print("=" * 68)
    print("Proton Breather 1D — Paper II, gravity sector")
    print("=" * 68)
    print(f"  r_core = a_p/xi = {r_core:.4e}    r_max = {r_max}    n = {n_pts}")
    print(f"  N_p = {N_P:.4f}    1/alpha = {1/ALPHA:.4f}")
    print()

    # ── 1. Static profile ─────────────────────────────────────────────────
    print("── 1. STATIC EXTERIOR PROFILE ──────────────────────────────────")
    A_star = find_amplitude(r_core, r_max)
    r_arr, f_arr = integrate_inward(A_star, r_core, r_max, n_pts)

    DV = deficit_volume(r_arr, f_arr, r_core)
    V0 = (4.0 / 3.0) * math.pi * r_core**3
    V_heal = DV - V0
    R_rms = rms_radius(r_arr, f_arr, r_core)

    print(f"  A* (decaying amplitude)       = {A_star:.4e}")
    print(f"  f(r_core)                     = {float(f_arr[0]):.2e}  (target 0)")
    print(f"  f(r_max)                      = {float(f_arr[-1]):.8f}  (target 1)")
    print()
    print(f"  V_core = (4/3)pi a_p^3        = {V0:.4e}")
    print(f"  V_heal (healing layer int.)   = {V_heal:.4e}")
    print(f"  DV = V_core + V_heal          = {DV:.4e}")
    print(f"  DV / V_core  (form factor)    = {DV/V0:.2e}   <<< healing layer dominates")
    print(f"  R_rms (deficit centroid)      = {R_rms:.4f} xi")
    print()

    # Asymptotic decay check
    ia, ib = int(0.70 * n_pts), int(0.90 * n_pts)
    ra, rb = float(r_arr[ia]), float(r_arr[ib])
    da, db = 1.0 - float(f_arr[ia]), 1.0 - float(f_arr[ib])
    if da > 1.0e-14 and db > 1.0e-14:
        lam = (math.log(abs(da * ra)) - math.log(abs(db * rb))) / (rb - ra)
        print(f"  Asymptotic check (r={ra:.1f}–{rb:.1f}): "
              f"lambda = {lam:.5f}  (expected sqrt2 = {SQRT2:.5f},  "
              f"error {abs(lam-SQRT2)/SQRT2*100:.2f}%)")
    print()

    # ── 2. Frequency separation ───────────────────────────────────────────
    print("── 2. FREQUENCY SEPARATION ──────────────────────────────────────")
    omega_0 = SQRT2            # Bogoliubov monopole mode: sqrt(2) c/xi in dimless units
    omega_p = 1.0 / r_core    # proton Compton frequency = m_p in dimless units
    print(f"  Healing-layer natural freq   omega_0 = sqrt(2) = {omega_0:.4f}")
    print(f"  Proton Compton freq          omega_p = 1/r_core = {omega_p:.1f}")
    print(f"  Ratio  omega_p / omega_0              = {omega_p/omega_0:.1f}")
    print()
    print(f"  Since omega_p >> omega_0, the healing layer is FROZEN on the")
    print(f"  proton's pulsation time scale.  The forced response of the")
    print(f"  healing layer at omega_p is suppressed by (omega_0/omega_p)^2")
    print(f"  = {(omega_0/omega_p)**2:.2e}, which is negligible.")
    print()
    print(f"  => The static deficit volume DV = {DV:.2e} is NOT the Bjerknes input.")
    print(f"     Only the core volume V0 = {V0:.2e} enters the dynamic formula.")
    print()

    # ── 3. Bjerknes / G calculation ───────────────────────────────────────
    print("── 3. BJERKNES ANALYSIS ─────────────────────────────────────────")
    print()

    # Case A: naive (static DV as delta_V) — wrong, but instructive
    resA = bjerknes_alpha_g(DV, r_core)
    print(f"  Case A: delta_V = DV (static deficit, WRONG — healing frozen)")
    print(f"    alpha_G = {resA['alpha_G']:.3e}  "
          f"(ratio to CODATA: {resA['ratio']:.2e}  log10={math.log10(resA['ratio']):.1f})")
    print()

    # Case B: Paper II formula — delta_V = V0 (core oscillation amplitude)
    resB = bjerknes_alpha_g(V0, r_core)
    print(f"  Case B: delta_V = V0 (Paper II: core oscillation, CORRECT)")
    print(f"    Q_eff = V0 * (a_p/xi)^3 = {resB['Q_eff']:.3e}")
    print(f"    alpha_G = {resB['alpha_G']:.3e}")
    print(f"    alpha_G (CODATA) = {ALPHA_G_CODATA:.3e}")
    print(f"    ratio Paper II / CODATA = {resB['ratio']:.2e}  "
          f"(log10 = {math.log10(resB['ratio']):.1f})")
    print()
    print(f"  The Paper II analytical estimate overestimates alpha_G by")
    print(f"  {resB['ratio']:.2e} (factor ~{resB['ratio']:.0e}).")
    print(f"  This is the geometric form-factor gap that the 3D trefoil")
    print(f"  profile (src/paper_i/) must supply.")
    print()

    # ── 4. Summary table ──────────────────────────────────────────────────
    print("=" * 68)
    print("SUMMARY")
    print("=" * 68)
    print()
    print(f"  Static profile:")
    print(f"    A*         = {A_star:.4e}")
    print(f"    V_core     = {V0:.4e} xi^3    (proton bare volume)")
    print(f"    V_heal     = {V_heal:.4e} xi^3    (healing-layer excess)")
    print(f"    R_rms      = {R_rms:.4f} xi    (deficit RMS radius)")
    print()
    print(f"  Frequency separation:")
    print(f"    omega_p / omega_0 = {omega_p/omega_0:.1f}  >>  1  (healing layer frozen)")
    print()
    print(f"  Bjerknes formula (Paper II, Case B: delta_V = V0):")
    print(f"    alpha_G (1D spherical)  = {resB['alpha_G']:.4e}")
    print(f"    alpha_G (CODATA)        = {ALPHA_G_CODATA:.4e}")
    print(f"    ratio                   = {resB['ratio']:.2e}")
    print(f"    log10(ratio)            = {math.log10(resB['ratio']):.2f}")
    print()
    print(f"  Residual discrepancy:  ~{resB['ratio']:.0e} overestimate.")
    print(f"  Physical origin: the 1D spherical model uses a simple hard-sphere")
    print(f"  V0 = (4/3)pi a_p^3.  The 3D trefoil topology concentrates the")
    print(f"  knotted core into a smaller effective acoustic cross-section,")
    print(f"  providing the missing geometric suppression.")
    print(f"  Open calculation: 3D proton breather profile -> src/paper_i/.")


if __name__ == "__main__":
    main()

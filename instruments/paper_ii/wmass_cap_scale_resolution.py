"""Resolution of the W-mass cap bending-stiffness shortfall — Paper II §weak (#105).

Background
----------
Paper II derives the W mass from the energy of the two depleted end-caps of the
reconnection jet, `m_W = 2 P0 V_cap` with `V_cap = pi R_cap^2 xi`. Writing the
cap as a vortex ring held in equilibrium,

    E(R) = pi R^2 + 2 pi tau R + 2 pi lambda_bend / R      (P0 = xi = 1),

minimisation gives the cubic `R^3 + tau R^2 = lambda_bend`, and placing the
equilibrium at the observed cap radius `R_cap = phi/alpha` requires a bending
stiffness `lambda_bend = phi^3/alpha^3 ~ 1.09e7 xi^3`.  The chiral-shear
Lagrangian's *local* curvature correction (lperp_core_integral) supplies only
`lambda_bend_local = lambda_perp (J+K)/4 ~ 4.7e4 xi^3` — a factor ~232 short.

This script settles where the 232 comes from and resolves it, testing the
pre-registered routes of issue #105.

Findings (all reproduced below)
--------------------------------
E  AUDIT. `m_W = pi phi^2 (m_e/alpha^2)` with `m_e/alpha^2 = 9.60 GeV` and two
   caps.  Back-solving the observed `m_W = 80.36 GeV` gives `R_cap = 1.633 xi/alpha`,
   NOT the `1.70` stated in the text (a stale number); `phi = 1.618` matches the
   true cap radius to 0.9%.

A  LOCAL CURVATURE IS FALSIFIED — structurally.  `lambda_bend_local = O(1) * alpha^-2`
   because `lambda_perp = alpha^-2` and `(J+K)/4` is an O(1) core integral.  The
   equilibrium cubic with this stiffness puts the cap at `R_eq ~ alpha^(-2/3) ~ 31 xi`,
   giving `m_W ~ 1.6 GeV` (51x too small).  No local curvature correction can ever
   reach the ring scale `xi/alpha`: the shortfall is exactly one power of
   `1/alpha = R*/xi` (the ring/core ratio), 232 = (phi^3/((J+K)/4)) * (1/alpha).

B  RESOLUTION — the cap scale is the inherited electron ring scale, not a bending
   equilibrium.  The reconnecting defects ARE electron-scale rings of radius
   `R* = xi/alpha` (derived in Paper I from the Lamb energy).  The cap cannot be
   smaller than the throats it joins, so `R_cap = O(1) * R*`, hence
   `m_W ~ P0 R_cap^2 xi ~ m_e (R*/xi)^2 = m_e/alpha^2`.  The `1/alpha^2` scale is
   framework-derived; the 232x "shortfall" was an artefact of setting R_cap by a
   local bending equilibrium, which is not the mechanism.  The residual prefactor
   `pi phi^2 ~ 8.2` (two caps * pi * the cap aspect phi^2) is O(1); only `phi`
   remains coincidence-grade.

A' SHARPEST OPEN FORM (kept for the record, not a closure).  If one retains the
   bending-equilibrium picture, the required stiffness is exactly `lambda_perp`
   *evaluated at the cap scale* with a linear running `lambda_perp(k) ~ 1/k`:
   `lambda_bend = (J+K)/4 * alpha^-2 * (R_cap/xi) = (J+K)/4 * phi/alpha^3`, which
   lands within ~5% of `phi^3/alpha^3`.  Whether the chiral-shear dispersion
   actually runs linearly is an undelivered derivation; route B closes #105
   without needing it.

Verdict: #105 resolved by route B (scale derived, 232 dissolved); m_W scale is
derived, the O(1) `phi` prefactor remains a coincidence (rule 1 / rule 5).
"""

from __future__ import annotations

import math

import numpy as np

# --- constants ------------------------------------------------------------
ALPHA = 1.0 / 137.035999084
PHI = (1.0 + math.sqrt(5.0)) / 2.0
M_E_MEV = 0.510998950        # electron mass, MeV
M_W_OBS_GEV = 80.3692        # PDG 2024 W mass, GeV

# core integrals from lperp_core_integral.py (b=1 LogSE profile, r<15 xi)
J_BEND = 7.8093
K_BEND = 2.2014
JK_OVER_4 = (J_BEND + K_BEND) / 4.0     # ~2.50, the O(1) local coefficient

TAU_XI = 17.0                # computed vortex line tension (xi), vortex_cap_mass.py

# --- basic scales ---------------------------------------------------------
def m_e_over_alpha2_gev() -> float:
    """The cap energy scale m_e/alpha^2 (= 2 P0 V_cap at R_cap = xi/alpha)."""
    return (M_E_MEV / ALPHA**2) / 1000.0


def m_W_from_Rcap(Rcap_over_xi: float) -> float:
    """W mass (GeV) from two caps: m_W = 2 P0 pi R_cap^2 xi, P0 = m_e/(2 xi^3)."""
    return math.pi * M_E_MEV * Rcap_over_xi**2 / 1000.0


# --- E: audit of the m_W <-> R_cap <-> lambda_bend chain ------------------
def true_Rcap_over_xi_alpha() -> float:
    """Cap radius (in units xi/alpha) that reproduces the observed m_W."""
    Rcap_xi = math.sqrt(M_W_OBS_GEV * 1000.0 / (math.pi * M_E_MEV))
    return Rcap_xi * ALPHA


# --- stiffness values -----------------------------------------------------
def lambda_bend_local() -> float:
    """Local chiral-shear curvature correction: lambda_perp (J+K)/4, lambda_perp = alpha^-2."""
    return JK_OVER_4 * ALPHA**-2


def lambda_bend_required() -> float:
    """Stiffness that places the equilibrium cubic at R = phi/alpha (tau -> 0 limit)."""
    return PHI**3 / ALPHA**3


def gap_factor() -> float:
    return lambda_bend_required() / lambda_bend_local()


# --- A: equilibrium cubic R^3 + tau R^2 = lambda_bend ---------------------
def R_equilibrium_xi(lambda_bend: float, tau_xi: float = TAU_XI) -> float:
    """Positive real root of R^3 + tau R^2 - lambda_bend = 0 (units xi)."""
    roots = np.roots([1.0, tau_xi, 0.0, -lambda_bend])
    pos = [r.real for r in roots if abs(r.imag) < 1e-6 and r.real > 0]
    return max(pos)


# --- A': anomalous-running form -------------------------------------------
def lambda_bend_running(Rcap_over_xi: float | None = None) -> float:
    """lambda_perp evaluated at the cap scale with linear running lambda_perp(k) ~ 1/k:
    lambda_bend = (J+K)/4 * alpha^-2 * (R_cap/xi).  R_cap defaults to phi/alpha."""
    if Rcap_over_xi is None:
        Rcap_over_xi = PHI / ALPHA
    return JK_OVER_4 * ALPHA**-2 * Rcap_over_xi


def _report() -> None:
    me_a2 = m_e_over_alpha2_gev()
    R_phi = PHI / ALPHA
    lam_loc, lam_req = lambda_bend_local(), lambda_bend_required()
    R_loc = R_equilibrium_xi(lam_loc)
    R_req = R_equilibrium_xi(lam_req)
    lam_run = lambda_bend_running()

    print("=" * 70)
    print("W-mass cap bending-stiffness shortfall — resolution (#105)")
    print("=" * 70)
    print(f"\n[E] AUDIT of the m_W <-> R_cap chain")
    print(f"    m_e/alpha^2                 = {me_a2:.3f} GeV")
    print(f"    m_W = pi phi^2 (m_e/alpha^2)= {math.pi*PHI**2*me_a2:.2f} GeV   (obs {M_W_OBS_GEV:.2f})")
    print(f"    true R_cap from observed m_W= {true_Rcap_over_xi_alpha():.4f} xi/alpha")
    print(f"    (text states 1.70; phi = {PHI:.4f}, off {abs(true_Rcap_over_xi_alpha()-PHI)/PHI*100:.2f}% -> 1.70 is stale)")

    print(f"\n[A] LOCAL curvature is structurally insufficient")
    print(f"    lambda_bend_local = (J+K)/4 * alpha^-2 = {lam_loc:.3e} xi^3   ((J+K)/4={JK_OVER_4:.3f})")
    print(f"    lambda_bend_reqd  = phi^3/alpha^3      = {lam_req:.3e} xi^3")
    print(f"    gap               = {gap_factor():.1f}x  = (phi^3/((J+K)/4)) * (1/alpha) = {PHI**3/JK_OVER_4:.3f} * {1/ALPHA:.1f}")
    print(f"    equilibrium cubic, LOCAL : R_eq = {R_loc:.1f} xi = {R_loc*ALPHA:.3f} (xi/alpha) ~ alpha^(-2/3)={ALPHA**(-2/3):.1f} xi")
    print(f"                               -> m_W = {m_W_from_Rcap(R_loc):.2f} GeV  (51x too small)")
    print(f"    equilibrium cubic, REQD  : R_eq = {R_req:.1f} xi = {R_req*ALPHA:.3f} (xi/alpha) ~ phi")

    print(f"\n[B] RESOLUTION: cap scale = inherited electron ring scale R* = xi/alpha")
    print(f"    R* (Paper I, derived)       = {1/ALPHA:.1f} xi")
    print(f"    m_W ~ m_e (R*/xi)^2 = m_e/alpha^2 = {me_a2:.2f} GeV  (the 1/alpha^2 is DERIVED)")
    print(f"    residual prefactor pi phi^2 = {math.pi*PHI**2:.2f}  (O(1); only phi is coincidence-grade)")
    print(f"    => 232x shortfall DISSOLVED: it was an artefact of a local bending equilibrium.")

    print(f"\n[A'] sharpest open form (not a closure): linear running lambda_perp(k) ~ 1/k")
    print(f"    lambda_bend = (J+K)/4 * alpha^-2 * (R_cap/xi) = {lam_run:.3e} xi^3")
    print(f"    vs required phi^3/alpha^3 = {lam_req:.3e}  -> within {abs(lam_run-lam_req)/lam_req*100:.1f}%")
    print(f"    (depends on an undelivered chiral-shear dispersion-running derivation)")
    print("\nVERDICT: #105 resolved by route B. m_W scale derived; phi remains O(1) coincidence.")


if __name__ == "__main__":
    _report()

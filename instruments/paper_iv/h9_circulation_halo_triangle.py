"""#119 H9 -- the circulation-halo G triangle vs the BTFR.

Pre-registered in issue #119 (owner's H9 comment + operational execution
plan).  Pure constants-level computation, no simulation: solves the closed
triangle (G, rho0, Gamma = N h/m0) implied by the H7a/H8 intrinsic
circulation halo against the observed baryonic Tully-Fisher relation, with
the Fall relation J ~ M^{5/3} supplying the natural-chain Gamma(M).

Physics (fixed by the pre-registration):
  - halo energy density   e(r) = rho0 * Gamma^2 / (8 pi^2 r^2)
    (the H7a/H8 measured form, e*r^2 = l^2 rho/2 in code units where the
    circulation quantum is 2 pi);
  - Poisson source (reading b)   lap(Phi) = 4 pi G e / c^2
    =>  v_flat^2 = G rho0 Gamma^2 / (2 pi c^2)   [exact factor, tested];
  - quantisation   Gamma = N h / m0.

Decision rules (operational, posted to #119 before computing):
  (a) magnitude -- solving the triangle at the reference point with the
      primary saturation dials must give alpha_G = G m_p^2/(hbar c) within
      10^+-2 of 5.9e-39; any other magnitude falsifies the circulation-halo
      G route on the natural chain;
  (b) slope -- the chain implies M_b ~ v^x with x = 1/beta where
      beta = dln j/dln M; PASS iff x = 4.0 +- 0.5.

Run:  python instruments/paper_iv/h9_circulation_halo_triangle.py
Writes the receipt to papers/SSV-IV/results/h9_triangle_receipt.json.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ----------------------------------------------------------------------
# CODATA / astronomical constants (SI)
# ----------------------------------------------------------------------
C = 2.997_924_58e8          # m/s
G_NEWTON = 6.674_30e-11     # m^3 kg^-1 s^-2
HBAR = 1.054_571_817e-34    # J s
H_PLANCK = 6.626_070_15e-34  # J s
M_E = 9.109_383_7015e-31    # kg
M_P = 1.672_621_923_69e-27  # kg
M_SUN = 1.988_47e30         # kg
KPC = 3.085_677_581e19      # m

ALPHA_G_TARGET = G_NEWTON * M_P**2 / (HBAR * C)   # ~5.9e-39 (the input, per H9)

# ----------------------------------------------------------------------
# SSV saturation dials (pre-registered; primary first)
# ----------------------------------------------------------------------
A_P = HBAR / (M_P * C)                  # grain scale, Paper I:  ~2.10e-16 m
RHO_GRAIN = M_P / A_P**3                # Compton-packed grains  ~1.80e20 kg/m^3
L_PLANCK = 1.616_255e-35                # m
M_PLANCK = 2.176_434e-8                 # kg
RHO_PLANCK = M_PLANCK / L_PLANCK**3     # Sakharov corner        ~5.2e96 kg/m^3
RHO_NUCLEAR = 2.3e17                    # nuclear saturation (reference)

RHO0_DIALS = {
    "grain (m_p/a_p^3, primary)": RHO_GRAIN,
    "Planck (Sakharov corner)": RHO_PLANCK,
    "nuclear saturation (reference)": RHO_NUCLEAR,
}

M0_DIALS = {"m_p (grain, primary)": M_P, "m_e (variant)": M_E}

# ----------------------------------------------------------------------
# Observational anchors (literature inputs, flagged in the plan)
# ----------------------------------------------------------------------
BTFR_A = 47.0               # M_sun km^-4 s^4   (McGaugh 2012, M_b = A v^4)
BTFR_SLOPE_OBS = (3.98, 0.06)   # free-fit slope (McGaugh 2012)
M_REF = 6.0e10 * M_SUN      # reference baryonic mass (MW-like)

# Fall relation: j_b(M) = J11 * (M / 1e11 M_sun)^beta   [kpc km/s]
FALL_J11_KPC_KMS = 2.0e3    # normalisation at 1e11 M_sun (+-50% tolerated)
FALL_BETA_PREREG = 2.0 / 3.0    # the pre-registered J ~ M^{5/3} form
FALL_BETA_EMP = 0.55            # empirical variant (Fall/Romanowsky, Posti+18)


def v_btfr(m_b: float) -> float:
    """Flat rotation velocity (m/s) from the BTFR at baryonic mass m_b (kg)."""
    v_kms = (m_b / M_SUN / BTFR_A) ** 0.25
    return v_kms * 1.0e3


def j_fall(m_b: float, beta: float) -> float:
    """Baryon specific angular momentum (m^2/s) from the Fall relation."""
    j_kpc_kms = FALL_J11_KPC_KMS * (m_b / (1.0e11 * M_SUN)) ** beta
    return j_kpc_kms * KPC * 1.0e3


def gamma_natural(m_b: float, beta: float) -> float:
    """Natural-chain entrained circulation: Gamma = 2 pi j_b(M)."""
    return 2.0 * math.pi * j_fall(m_b, beta)


def v_flat_sq_from_triangle(g: float, rho0: float, gamma: float) -> float:
    """The triangle relation v_flat^2 = G rho0 Gamma^2 / (2 pi c^2)."""
    return g * rho0 * gamma**2 / (2.0 * math.pi * C**2)


def g_solved(rho0: float, gamma: float, v_flat: float) -> float:
    """Solve the triangle for G given rho0, Gamma and the observed v_flat."""
    return 2.0 * math.pi * C**2 * v_flat**2 / (rho0 * gamma**2)


def alpha_g(g: float) -> float:
    return g * M_P**2 / (HBAR * C)


def run() -> dict:
    v_ref = v_btfr(M_REF)

    # ---- rule (a): magnitude, all dial combinations -------------------
    magnitude = {}
    for rho_name, rho0 in RHO0_DIALS.items():
        gam = gamma_natural(M_REF, FALL_BETA_PREREG)
        g_req = g_solved(rho0, gam, v_ref)
        a_g = alpha_g(g_req)
        magnitude[rho_name] = {
            "Gamma_m2_per_s": gam,
            "G_solved": g_req,
            "alpha_G_solved": a_g,
            "alpha_G_target": ALPHA_G_TARGET,
            "orders_off": math.log10(a_g / ALPHA_G_TARGET),
            "pass_within_1e2": abs(math.log10(a_g / ALPHA_G_TARGET)) <= 2.0,
        }

    # ---- rule (b): slope ----------------------------------------------
    slope = {}
    for label, beta in (("prereg J~M^{5/3}", FALL_BETA_PREREG),
                        ("empirical j~M^{0.55}", FALL_BETA_EMP)):
        x = 1.0 / beta          # M_b ~ v^x implied by v^2 ~ Gamma^2 ~ M^{2 beta}
        slope[label] = {
            "beta": beta,
            "implied_btfr_slope": x,
            "observed_slope": BTFR_SLOPE_OBS,
            "pass_4p0_pm_0p5": abs(x - 4.0) <= 0.5,
        }
    # inverse requirement: BTFR slope 4 <=> Gamma ~ M^{1/4} <=> J ~ M^{5/4}
    slope["inverse_requirement"] = {
        "Gamma_exponent_required": 0.25,
        "J_exponent_required": 1.25,
        "J_exponent_fall": 5.0 / 3.0,
        "exponent_gap": 5.0 / 3.0 - 1.25,
    }

    # ---- inversions (reported, not pass/fail) -------------------------
    gam_fall = gamma_natural(M_REF, FALL_BETA_PREREG)
    rho0_required = (2.0 * math.pi * C**2 * v_ref**2
                     / (G_NEWTON * gam_fall**2))
    gamma_required = math.sqrt(
        2.0 * math.pi * C**2 * v_ref**2 / (G_NEWTON * RHO_GRAIN))
    inversions = {
        "rho0_required_for_real_G_on_fall_chain_kg_m3": rho0_required,
        "Gamma_required_with_grain_rho0_real_G_m2_s": gamma_required,
        "Gamma_fall_chain_m2_s": gam_fall,
        "Gamma_ratio_fall_over_required": gam_fall / gamma_required,
        "N_required_m_p": gamma_required * M_P / H_PLANCK,
        "N_required_m_e": gamma_required * M_E / H_PLANCK,
        "N_fall_m_p": gam_fall * M_P / H_PLANCK,
        "medium_flow_at_10kpc_required_m_s":
            gamma_required / (2.0 * math.pi * 10.0 * KPC),
        "halo_mass_density_at_10kpc_required_kg_m3":
            RHO_GRAIN * gamma_required**2
            / (8.0 * math.pi**2 * C**2 * (10.0 * KPC) ** 2),
    }

    primary = magnitude["grain (m_p/a_p^3, primary)"]
    verdict = {
        "rule_a_magnitude": "PASS" if primary["pass_within_1e2"] else "FAIL",
        "rule_b_slope": "PASS"
        if slope["prereg J~M^{5/3}"]["pass_4p0_pm_0p5"] else "FAIL",
    }
    verdict["route"] = (
        "circulation-halo G route on the natural chain SURVIVES"
        if verdict["rule_a_magnitude"] == "PASS"
        and verdict["rule_b_slope"] == "PASS"
        else "circulation-halo G route on the natural chain FALSIFIED"
    )

    return {
        "issue": 119,
        "hypothesis": "H9 circulation-halo G triangle vs BTFR",
        "reference_point": {
            "M_b_Msun": M_REF / M_SUN,
            "v_btfr_km_s": v_ref / 1.0e3,
        },
        "saturation_dials": {
            "a_p_m": A_P,
            "rho_grain_kg_m3": RHO_GRAIN,
            "rho_planck_kg_m3": RHO_PLANCK,
            "rho_nuclear_kg_m3": RHO_NUCLEAR,
        },
        "rule_a_magnitude": magnitude,
        "rule_b_slope": slope,
        "inversions": inversions,
        "verdict": verdict,
    }


def main() -> None:
    out = run()
    here = Path(__file__).resolve().parents[2]
    dest = here / "papers" / "SSV-IV" / "results" / "h9_triangle_receipt.json"
    dest.write_text(json.dumps(out, indent=2))

    v = out["verdict"]
    prim = out["rule_a_magnitude"]["grain (m_p/a_p^3, primary)"]
    print(f"reference: M_b = {out['reference_point']['M_b_Msun']:.2e} Msun, "
          f"v_BTFR = {out['reference_point']['v_btfr_km_s']:.1f} km/s")
    print(f"rule (a) magnitude [{v['rule_a_magnitude']}]: "
          f"alpha_G solved = {prim['alpha_G_solved']:.2e} "
          f"vs target {prim['alpha_G_target']:.2e} "
          f"({prim['orders_off']:+.1f} orders)")
    sl = out["rule_b_slope"]["prereg J~M^{5/3}"]
    print(f"rule (b) slope [{v['rule_b_slope']}]: implied BTFR slope = "
          f"{sl['implied_btfr_slope']:.2f} vs observed "
          f"{sl['observed_slope'][0]} +- {sl['observed_slope'][1]}")
    inv = out["inversions"]
    print(f"inversions: rho0 required = "
          f"{inv['rho0_required_for_real_G_on_fall_chain_kg_m3']:.2e} kg/m^3; "
          f"Gamma_fall/Gamma_required = "
          f"{inv['Gamma_ratio_fall_over_required']:.2e}")
    print(f"verdict: {v['route']}")
    print(f"receipt: {dest}")


if __name__ == "__main__":
    main()

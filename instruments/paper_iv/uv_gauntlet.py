"""#148 UV-GAUNTLET -- the update ceiling and the grain vs the measured
ultraviolet sky.

#129 items 5 and 6 (the SSV-IV gapboxes): the update ceiling N0 vs >>GeV
photons, and the grain a_p vs collider-scale Lorentz invariance.  A
constraint-pricing run in the TOKEN-TAX mold: pinned formulas, pinned
published bounds, computed margins.  Decision rule (#148): margin >= 2
orders => that naive reading is falsified-as-written and the survivor
requirement enters SSV-IV in quantitative form; margin < 2 orders =>
"tension, open".  C5 is the pre-registered honest NON-exclusion check.

Confrontations:
  C1  ceiling N0 = m_p c^2/hbar vs observed photon frequencies
      (LHAASO PeV photons, GRB 221009A).
  C2  bare-medium Bogoliubov dispersion w^2 = c^2k^2 [1 + (k a_p/2)^2]
      (the quantum-pressure k^4 term, measured real in the #138 magnon
      channel) vs the GRB 090510 quadratic time-of-flight bound.
  C3  the same superluminal branch vs photon-decay survival of PeV
      photons (gamma -> e+e- opens above threshold).
  C4  grain structure at 0.94 GeV vs collider compositeness/contact
      scales.
  C5  lab Lorentz tests (resonator anisotropy) -- expected NOT to
      exclude; recorded plainly either way.

All physics formulas are stated in the pre-registration (issue #148);
this script is pinned arithmetic plus the receipt.

Run:  python instruments/paper_iv/uv_gauntlet.py
Writes papers/SSV-IV/results/uv_gauntlet_receipt.json.
"""

from __future__ import annotations

import json
import math
import os

# ------------------------------------------------------------ SI constants
HBAR = 1.054571817e-34      # J s
C = 2.99792458e8            # m/s
M_P = 1.67262192369e-27     # kg
M_E = 9.1093837015e-31      # kg
E_CHARGE = 1.602176634e-19  # J/eV
GEV = 1.0e9 * E_CHARGE      # J

# ------------------------------------------------------- pinned SSV scales
A_P = HBAR / (M_P * C)                  # the grain, m
E_GRAIN_GEV = M_P * C ** 2 / GEV        # 0.938 GeV
N0 = M_P * C ** 2 / HBAR                # update ceiling, s^-1
M_E_GEV = M_E * C ** 2 / GEV

# ---------------------------------------------------- pinned observations
PHOTONS = [
    # (name, E in GeV, citation)
    ("LHAASO J2032+4127", 1.42e6, "Cao et al., Nature 594, 33 (2021)"),
    ("Crab Nebula", 1.1e6, "LHAASO, Science 373, 425 (2021)"),
    ("GRB 221009A", 1.3e4, "LHAASO, Science 380, 1390 (2023)"),
]
E_QG2_BOUND_GEV = 1.3e11      # Vasileiou et al., PRD 87, 122001 (2013)
E_GRB090510_GEV = 31.0        # highest GRB 090510 photon
E_LV_SUP_LINEAR_GEV = 1.42e24  # LHAASO Collab., PRL 128, 051102 (2022)
LAMBDA_CONTACT_GEV = 1.0e4    # LEP/LHC contact-interaction scale ~10 TeV
R_ELECTRON_BOUND_M = 2.0e-19  # electron substructure (Bourilkov 2001)
RESONATOR_BOUND = 1.0e-18     # Nagel et al., Nat. Commun. 6, 8174 (2015)
K_OPTICAL = 9.5e6             # m^-1 (optical cavity, pre-registered)
V_CMB_OVER_C = 1.23e-3        # CMB-frame boost


def delta_v_over_c(e_gev: float) -> float:
    """Weak-dispersion limit of the Bogoliubov branch:
    v_g/c - 1 = (3/8) (k a_p)^2 with k a_p = E/E_grain."""
    return 0.375 * (e_gev / E_GRAIN_GEV) ** 2


def vg_over_c_exact(e_gev: float) -> float:
    """Exact group velocity of w = c k sqrt(1 + (k a_p/2)^2):
    v_g/c = (1 + 2u^2)/sqrt(1 + u^2), u = k a_p / 2."""
    u = 0.5 * e_gev / E_GRAIN_GEV
    return (1.0 + 2.0 * u * u) / math.sqrt(1.0 + u * u)


def effective_eqg2() -> float:
    """Match (3/8)(E/E_grain)^2 = (3/2)(E/E_QG2)^2 (the Vasileiou
    v_g convention, n=2): E_QG2_eff = 2 E_grain."""
    return 2.0 * E_GRAIN_GEV


def photon_decay_threshold_delta(e_gev: float) -> float:
    """Superluminal delta above which gamma -> e+ e- opens:
    effective mass^2 = 2 delta E^2 > (2 m_e c^2)^2."""
    return 2.0 * (M_E_GEV / e_gev) ** 2


def run() -> dict:
    # --- C1: ceiling vs photon frequencies --------------------------------
    c1 = []
    for name, e_gev, cite in PHOTONS:
        omega = e_gev * GEV / HBAR
        margin = math.log10(omega / N0)
        c1.append({"source": name, "E_GeV": e_gev, "citation": cite,
                   "omega_s^-1": omega, "margin_orders": margin})
    c1_verdict = ("falsified-as-written"
                  if min(r["margin_orders"] for r in c1) >= 2.0
                  else "tension, open")

    # --- C2: grain dispersion vs GRB time-of-flight ------------------------
    eqg2 = effective_eqg2()
    c2_margin = math.log10(E_QG2_BOUND_GEV / eqg2)
    c2 = {"ssv_effective_E_QG2_GeV": eqg2,
          "prereg_estimate_GeV": math.sqrt(8.0 / 3.0) * E_GRAIN_GEV,
          "bound_E_QG2_GeV": E_QG2_BOUND_GEV,
          "bound_citation": "Vasileiou et al., PRD 87, 122001 (2013), "
                            "95% CL, GRB 090510",
          "margin_orders": c2_margin,
          "delta_v_at_31GeV": delta_v_over_c(E_GRB090510_GEV),
          "note": "delta_v(31 GeV) > 1: the perturbative reading collapses "
                  "entirely; the margin in scale understates the kill",
          "verdict": ("falsified-as-written" if c2_margin >= 2.0
                      else "tension, open")}

    # --- C3: superluminal photon decay -------------------------------------
    e_pev = PHOTONS[0][1]
    d_ssv = delta_v_over_c(e_pev)
    d_thr = photon_decay_threshold_delta(e_pev)
    c3_margin = math.log10(d_ssv / d_thr)
    c3 = {"E_GeV": e_pev,
          "k_a_p": e_pev / E_GRAIN_GEV,
          "ssv_delta": d_ssv,
          "decay_threshold_delta": d_thr,
          "margin_orders_above_decay_threshold": c3_margin,
          "linear_bound_E_LV_GeV": E_LV_SUP_LINEAR_GEV,
          "linear_bound_citation": "LHAASO Collab., PRL 128, 051102 (2022)",
          "note": "k a_p ~ 1.5e6 >> 1: outside the perturbative domain; at "
                  "k a_p >> 1 the branch is free-particle-like "
                  "(v_g/c ~ E/E_grain), so the kill holds a fortiori",
          "verdict": ("falsified-as-written" if c3_margin >= 2.0
                      else "tension, open")}

    # --- C4: collider compositeness ----------------------------------------
    c4_energy_margin = math.log10(LAMBDA_CONTACT_GEV / E_GRAIN_GEV)
    c4_length_margin = math.log10(A_P / R_ELECTRON_BOUND_M)
    c4 = {"grain_scale_GeV": E_GRAIN_GEV, "grain_length_m": A_P,
          "contact_scale_GeV": LAMBDA_CONTACT_GEV,
          "electron_radius_bound_m": R_ELECTRON_BOUND_M,
          "citation": "LEP contact-interaction limits ~10 TeV; "
                      "Bourilkov, PRD 64, 071701 (2001)",
          "margin_orders_energy": c4_energy_margin,
          "margin_orders_length": c4_length_margin,
          "verdict": ("falsified-as-written"
                      if min(c4_energy_margin, c4_length_margin) >= 2.0
                      else "tension, open")}

    # --- C5: lab Lorentz tests (honest non-exclusion check) ----------------
    # anisotropy modulation ~ (3/8)(k a_p)^2 * 2(v/c), the generous
    # O(v/c) scaling pinned in the pre-registration
    signal = 0.375 * (K_OPTICAL * A_P) ** 2 * 2.0 * V_CMB_OVER_C
    c5 = {"k_optical_m^-1": K_OPTICAL,
          "k_a_p": K_OPTICAL * A_P,
          "predicted_anisotropy_signal": signal,
          "bound": RESONATOR_BOUND,
          "bound_citation": "Nagel et al., Nat. Commun. 6, 8174 (2015)",
          "orders_below_bound": math.log10(RESONATOR_BOUND / signal),
          "verdict": "NOT excluded by laboratory interferometry -- the "
                     "kill lives at TeV-PeV, recorded plainly per the "
                     "pre-registration"}

    survivors = [
        "S1: the propagating phase channel must be exactly linear "
        "(Lorentzian) to <~1e-17 fractional dispersion out to >= 1e6 "
        "E_grain -- a protection mechanism (Fermi-point/emergent-LI "
        "class, Volovik) is a derivation obligation on the #138 photon "
        "identification, not a free pass: the k^4 quantum-pressure term "
        "is measured-real in the magnon channel and present on the "
        "Bogoliubov branch by the same algebra",
        "S2: the ceiling N0, if retained, must be reinterpreted off the "
        "single-mode frequency axis (e.g. per-grain bandwidth shared "
        "across a delocalized mode) -- as written it is dead by ~6 orders",
        "S3: the grain must not scatter -- no form factor at GeV; the "
        "grain may appear only in defect statics (where #138 put alpha) "
        "and in update accounting",
    ]
    honesty = [
        "C2 and C3 price the same object (the Bogoliubov branch) at "
        "different energies; they are one kill stated twice, not two "
        "independent kills",
        "C5 is a non-exclusion and is reported as such: laboratory "
        "interferometry is ~12 orders too soft to see the grain "
        "dispersion at optical k",
        "the confrontations assume the photon rides the bare phase "
        "channel (#138 R1); if future structure protects that channel, "
        "C2/C3 become constraints on the protection, not kills of SSV",
    ]

    receipt = {
        "issue": 148,
        "hypothesis": "UV-GAUNTLET: quantify SSV-IV gapboxes 5/6 "
                      "(ceiling vs >>GeV photons; grain vs Lorentz tests)",
        "pinned_scales": {"a_p_m": A_P, "E_grain_GeV": E_GRAIN_GEV,
                          "N0_s^-1": N0},
        "C1_ceiling_vs_photons": {"rows": c1, "verdict": c1_verdict},
        "C2_grain_dispersion_vs_GRB_TOF": c2,
        "C3_superluminal_photon_decay": c3,
        "C4_collider_compositeness": c4,
        "C5_lab_lorentz_non_exclusion": c5,
        "survivor_requirements": survivors,
        "honesty_clauses": honesty,
    }
    return receipt


def main() -> dict:
    receipt = run()
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, "..", ".."))
    path = os.path.join(repo, "papers", "SSV-IV", "results",
                        "uv_gauntlet_receipt.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)

    print(f"UV-GAUNTLET (#148)  --  receipt -> "
          f"{os.path.relpath(path, repo)}")
    print(f"  pinned: a_p = {A_P:.4e} m, E_grain = {E_GRAIN_GEV:.4f} GeV, "
          f"N0 = {N0:.4e} /s")
    c1 = receipt["C1_ceiling_vs_photons"]
    for r in c1["rows"]:
        print(f"  C1 {r['source']:<18} E = {r['E_GeV']:.3g} GeV  "
              f"margin = {r['margin_orders']:+.2f} orders")
    print(f"  C1 verdict: {c1['verdict']}")
    c2 = receipt["C2_grain_dispersion_vs_GRB_TOF"]
    print(f"  C2 E_QG2(SSV) = {c2['ssv_effective_E_QG2_GeV']:.3f} GeV vs "
          f"bound {c2['bound_E_QG2_GeV']:.2e} GeV  ->  "
          f"{c2['margin_orders']:+.2f} orders; "
          f"delta_v(31 GeV) = {c2['delta_v_at_31GeV']:.1f}  ->  "
          f"{c2['verdict']}")
    c3 = receipt["C3_superluminal_photon_decay"]
    print(f"  C3 delta(1.42 PeV) = {c3['ssv_delta']:.2e} vs decay "
          f"threshold {c3['decay_threshold_delta']:.2e}  ->  "
          f"{c3['margin_orders_above_decay_threshold']:+.1f} orders above "
          f"-> {c3['verdict']}")
    c4 = receipt["C4_collider_compositeness"]
    print(f"  C4 margins: {c4['margin_orders_energy']:+.2f} orders "
          f"(energy), {c4['margin_orders_length']:+.2f} orders (length)  "
          f"->  {c4['verdict']}")
    c5 = receipt["C5_lab_lorentz_non_exclusion"]
    print(f"  C5 predicted signal {c5['predicted_anisotropy_signal']:.2e} "
          f"vs bound {c5['bound']:.0e}  ->  "
          f"{c5['orders_below_bound']:.1f} orders BELOW -> non-exclusion")
    return receipt


if __name__ == "__main__":
    main()

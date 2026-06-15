"""#155 H-EOS S1 -- surface gravity, Unruh/Hawking T, and the trans-Planckian
robustness margin of a flowing LogSE dumb-hole; Clausius closure -> G_eff.

Pre-registered on issue #155 (S1(a)/S1(b)/S1(c) in the body; the instrument
design, the four quantities, the robustness margin, and the decision rules
posted as a comment BEFORE computing, rule 6). Supplies the ANALYTIC half of
the Jacobson route whose area-law INPUT was delivered by S2
(`horizon_entanglement_entropy.py`, R1). Owner's scope: analytic + the
scale-separation margin (NOT a full dispersive mode-propagation solver).

The acoustic metric is KINEMATIC: it is fixed algebraically by the flow
(rho, v, c_s) with no back-reaction (Visser 1997, gr-qc/9712010, sec.14 --
"form yes, G no"). So the surface gravity and Unruh temperature are computable
from the flow alone; the dynamics (what sources the flow, and G) is not. This
is the structural reason the gravity sector reads "form yes, G no".

S1(a) -- flowing dumb-hole (3D radial sink / draining bathtub):
  c_s = sqrt(B0) is DENSITY-INDEPENDENT in the LogSE (mu(rho)=B0 ln rho =>
  rho mu'(rho)=B0), a clean feature: the acoustic metric's lapse comes from the
  flow alone. Mass-conserving radial sink v(r) = c_s r_H^2 / r^2 crosses c_s at
  the acoustic horizon r_H (a radial SINK, not a pure vortex, is required for a
  true horizon -- Visser sec.5/8).
    surface gravity (Visser eq 70):  g_H = 1/2 |d/dr (c_s^2 - v^2)|_{r_H}
                                          = 2 c_s^2 / r_H   (analytic)
    Hawking/Unruh T   (eq 118):      kT_H = hbar g_H/(2 pi c_s)
                                          => T_H = c_s/(pi r_H)   (analytic)
  Both verified numerically from the profile.

  THE NEGATIVE-CAPABLE TEST -- trans-Planckian / superluminal-dispersion
  robustness (the W4/#148 obligation). The LogSE phonon dispersion
  omega^2 = c_s^2 k^2 + k^4/4 is SUPERLUMINAL: the group velocity
    v_g(k) = (c_s^2 + k^2/2)/sqrt(c_s^2 + k^2/4)
  exceeds c_s for ALL k>0 (excess ~ (3/8) k^2/c_s as k->0), so high-k modes can
  outrun sound and leak across the acoustic horizon (Corley-Jacobson 1996;
  Unruh-Schuetzhold 2005). Thermality is robust iff the surface-gravity
  frequency sits well below the dispersion frequency:
    margin  M = g_H xi/(2 pi c_s^2) = xi/(pi r_H)   must be << 1.
  Robust for astrophysical r_H >> xi; O(1) for grain-scale local Rindler
  horizons (the Jacobson construction) -- the conditional caveat that ties the
  gravity sector to the #148 local-Lorentz protection.

S1(b) -- area-law dS = eta dA: RESOLVED by S2 (R1). Read eta from its receipt.

S1(c) -- Clausius closure delta Q = T_H dS on the local horizon yields
  (Jacobson 1995; VII-b sec.5.1)  nabla^2 Phi = 4 pi G_eff e/c^2  with
    G_eff = 1/(4 hbar c eta).
  eta is O(1) per xi^2 (S2: c2 ~ O(1) in xi-units), so G_eff ~ xi^2 c^3/hbar
  (grain scale) and overshoots G_N by (a_p/l_P)^2 = 1/alpha_G ~ 1.69e38.
  GUARD (rule 1): (a_p/l_P)^2 = 1/alpha_G is the #122 IDENTITY, not a
  derivation; G's magnitude stays conceded (D-b, #154). S1(c) shows only that
  the FORM closes and the magnitude is exactly the conceded overshoot.

Run:  python instruments/paper_v/dumb_hole_surface_gravity.py
Writes papers/SSV-V/results/heos_s1_receipt.json and
papers/SSV-V/figures/heos_s1_dumbhole.png.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-V" / "results"
FIGURES = ROOT / "papers" / "SSV-V" / "figures"

B0 = 1.0                          # log coupling: c_s^2 = B0
C_S = math.sqrt(B0)               # sound speed (density-independent)
XI = 1.0 / math.sqrt(2.0 * B0)    # healing length ~ 0.707


# ----------------------------------------------------------------------
# flow + acoustic metric
# ----------------------------------------------------------------------

def v_sink(r, r_H):
    """Mass-conserving 3D radial-sink inflow speed, v = c_s (r_H/r)^2, so
    v(r_H) = c_s exactly (the acoustic horizon)."""
    return C_S * (r_H / r) ** 2


def surface_gravity_numeric(r_H, n=20001, span=6.0):
    """g_H = 1/2 |d/dr (c_s^2 - v^2)| at the horizon, from a finite-difference
    derivative of the profile (verifies the analytic 2 c_s^2/r_H)."""
    r = np.linspace(r_H * (1 - 1e-3), r_H * (1 + 1e-3), 5)
    f = C_S**2 - v_sink(r, r_H) ** 2          # vanishes at r_H
    dfdr = np.gradient(f, r)
    # value at the central node (r = r_H)
    g = 0.5 * abs(dfdr[len(dfdr) // 2])
    return g


def group_velocity(k):
    """LogSE phonon group velocity v_g = d omega/dk, omega^2 = c_s^2 k^2+k^4/4."""
    omega = np.sqrt(C_S**2 * k**2 + 0.25 * k**4)
    with np.errstate(divide="ignore", invalid="ignore"):
        vg = (C_S**2 * k + 0.5 * k**3) / omega
    return vg


# ----------------------------------------------------------------------
# S1(a) battery
# ----------------------------------------------------------------------

def s1a(rH_list):
    """Surface gravity, Hawking T, and the robustness margin across horizon
    sizes; the superluminal-excess (leak) diagnostic."""
    rows = []
    for r_H in rH_list:
        g_an = 2.0 * C_S**2 / r_H
        g_num = surface_gravity_numeric(r_H)
        T_an = C_S / (math.pi * r_H)
        T_num = g_num / (2.0 * math.pi * C_S)
        margin = XI / (math.pi * r_H)              # g_H xi/(2 pi c_s^2)
        rows.append({
            "r_H": r_H,
            "g_H_analytic": g_an,
            "g_H_numeric": g_num,
            "g_H_rel_err": abs(g_num - g_an) / g_an,
            "T_H_analytic": T_an,
            "T_H_numeric": T_num,
            "T_H_rel_err": abs(T_num - T_an) / T_an,
            "robustness_margin_M": margin,
            "thermality_robust": bool(margin < 0.1),
        })
    # superluminal-excess profile: v_g(k) - c_s > 0 for all k>0
    ks = np.linspace(1e-3, 4.0 / XI, 200)
    vg = group_velocity(ks)
    excess = vg - C_S
    superluminal_everywhere = bool(np.all(excess > -1e-12))
    # small-k excess coefficient should match (3/8)/c_s
    small = ks < 0.05
    coeff = float(np.polyfit(ks[small] ** 2, excess[small], 1)[0])
    return {
        "rows": rows,
        "superluminal_for_all_k": superluminal_everywhere,
        "small_k_excess_coeff_measured": coeff,
        "small_k_excess_coeff_analytic": 0.375 / C_S,
        "leak_note": "v_g > c_s for all k>0 (excess ~ (3/8)k^2/c_s); the "
                     "horizon is sharp for hydrodynamic modes (k xi << 1), "
                     "fuzzy at the grain scale k ~ 1/xi.",
    }


# ----------------------------------------------------------------------
# S1(c) Clausius closure -> G_eff
# ----------------------------------------------------------------------

def read_s2_eta():
    """Area coefficient eta from the S2 receipt (c2 of S = c2 R^2 + c1 R + c0,
    the entanglement entropy per unit area). O(1) in xi-units => eta ~ 1/xi^2."""
    rec = RESULTS / "heos_s2_receipt.json"
    if not rec.is_file():
        return None
    d = json.loads(rec.read_text())
    return float(d["A_baseline"]["diag"]["c2_area"])


def s1c():
    """Clausius closure: form G_eff = 1/(4 hbar c eta); magnitude overshoot
    (a_p/l_P)^2 = 1/alpha_G (the conceded #122 identity, NOT a derivation)."""
    eta = read_s2_eta()
    m_P, m_p = 2.176434e-8, 1.67262192e-27          # kg
    overshoot = (m_P / m_p) ** 2                     # = 1/alpha_G
    out = {
        "eta_from_S2_c2_area": eta,
        "eta_is_O1_per_xi2": bool(eta is not None and 0.1 < eta < 100.0),
        "G_eff_form": "G_eff = 1/(4 hbar c eta)  [Jacobson, VII-b sec.5.1]",
        "G_eff_code_units": (1.0 / (4.0 * eta) if eta else None),
        "overshoot_a_p_over_l_P_squared": overshoot,
        "guard": "(a_p/l_P)^2 = 1/alpha_G is the #122 IDENTITY (l_P and "
                 "alpha_G both contain G), not a derivation; G's magnitude "
                 "stays conceded (D-b, #154). The Clausius chain delivers the "
                 "FORM; the magnitude is exactly the conceded overshoot.",
    }
    return out


# ----------------------------------------------------------------------
# battery + verdict
# ----------------------------------------------------------------------

def battery():
    # horizon sizes spanning hydrodynamic (r_H >> xi) down toward grain scale
    rH_list = [2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
    A = s1a(rH_list)
    C = s1c()

    g_ok = all(row["g_H_rel_err"] < 1e-3 for row in A["rows"])
    T_ok = all(row["T_H_rel_err"] < 1e-3 for row in A["rows"])
    # margin -> 0 as r_H grows (thermality robust for scale-separated horizons)
    margins = [row["robustness_margin_M"] for row in A["rows"]]
    margin_monotone = all(margins[i + 1] < margins[i]
                          for i in range(len(margins) - 1))
    robust_large = A["rows"][-1]["thermality_robust"]
    # the grain-scale caveat: extrapolate where M crosses 1 (r_H ~ xi/pi)
    rH_breakdown = XI / math.pi               # M = 1 at r_H = xi/pi
    R1a = bool(g_ok and T_ok and margin_monotone and robust_large
               and A["superluminal_for_all_k"])
    out = {
        "config": {"B0": B0, "c_s": C_S, "xi": XI},
        "S1a": A,
        "S1c": C,
        "verdicts": {
            "g_H_matches_visser_eq70": bool(g_ok),
            "T_H_matches_visser_eq118": bool(T_ok),
            "dispersion_superluminal_all_k": bool(A["superluminal_for_all_k"]),
            "margin_M_to_zero_for_large_rH": bool(margin_monotone
                                                  and robust_large),
            "rH_breakdown_grainscale": rH_breakdown,
            "S1c_eta_O1_form_closes": bool(C["eta_is_O1_per_xi2"]),
            "S1c_overshoot": C["overshoot_a_p_over_l_P_squared"],
            "VERDICT": "R1(a)" if R1a else "R2(a)",
            "VERDICT_meaning": (
                "R1(a): regular acoustic horizon; g_H, T_H match Visser; "
                "thermality robust for scale-separated horizons (M=xi/(pi r_H) "
                "-> 0), O(1) at the grain scale (W4/#148 caveat). Clausius "
                "closes in FORM; G magnitude conceded (overshoot "
                f"~{C['overshoot_a_p_over_l_P_squared']:.2e})."
                if R1a else
                "R2(a): horizon or thermality not robust -- Jacobson route "
                "undermined for this medium."),
            "form_yes_G_no": bool(R1a),
        },
    }
    return out


def figure(out, dest):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None
    rows = out["S1a"]["rows"]
    rH = [r["r_H"] for r in rows]
    M = [r["robustness_margin_M"] for r in rows]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8))
    ax = axes[0]
    ax.loglog(rH, M, "o-", label=r"margin $M=\xi/(\pi r_H)$")
    ax.axhline(1.0, color="r", ls="--", lw=1, label="trans-Planckian breakdown")
    ax.axhline(0.1, color="orange", ls=":", lw=1, label="robust threshold")
    ax.set_xlabel(r"horizon radius $r_H/\xi$")
    ax.set_ylabel("robustness margin $M$")
    ax.set_title("thermality robust iff $M\\ll1$: $M\\to0$ for $r_H\\gg\\xi$,\n"
                 "$O(1)$ at grain-scale (Rindler) horizons (W4/#148)",
                 fontsize=8)
    ax.legend(fontsize=7)
    ax = axes[1]
    ks = np.linspace(1e-3, 3.0 / XI, 200)
    ax.plot(ks * XI, group_velocity(ks) / C_S, "-", label=r"$v_g/c_s$")
    ax.axhline(1.0, color="k", ls=":", lw=1, label=r"$c_s$ (sound)")
    ax.set_xlabel(r"$k\,\xi$")
    ax.set_ylabel(r"$v_g/c_s$")
    ax.set_title("LogSE dispersion is superluminal for all $k>0$\n"
                 "(the leak channel; excess $\\sim(3/8)k^2/c_s$)", fontsize=8)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(dest, dpi=160)
    plt.close(fig)
    return dest


def main():
    print("H-EOS S1 dumb-hole surface gravity / Unruh T / robustness margin",
          flush=True)
    out = battery()
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    dest = RESULTS / "heos_s1_receipt.json"
    dest.write_text(json.dumps(out, indent=1))
    fig = figure(out, FIGURES / "heos_s1_dumbhole.png")
    print("\n--- verdicts ---")
    for k, v in out["verdicts"].items():
        print(f"  {k}: {v}")
    print(f"receipt -> {dest}")
    if fig:
        print(f"figure  -> {fig}")


if __name__ == "__main__":
    main()

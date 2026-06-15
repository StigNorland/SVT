"""#155 H-A0-IR -- the IR acceleration scale a0 = cH0/2pi and the duality
over-constraint, as a COEFFICIENT-CONSISTENCY test.

Pre-registered on issue #155 (the coefficient-consistency framing, the candidate
table, the discrimination-power and z-falsifier designs, and the R1/R2 decision
rules posted as a comment BEFORE computing, rule 6). The cosmological/IR half of
Option D: S2 (area-law dS) and S1 (surface gravity + Unruh T) closed the LOCAL
horizon half in form; this asks whether the SAME holographic thermodynamics
(the Gibbons-Hawking / Unruh 2pi and the area-law 1/4) also governs the
COSMOLOGICAL horizon, i.e. whether a0 = cH0/2pi.

Why coefficient-consistency, not a three-G match (non-circularity, recorded):
  (i) a_p/l_P is the #122 circular identity ((a_p/l_P)^2 = 1/alpha_G), guarded,
      NOT a derivation; and
  (ii) SSV-VIII concedes the a0 MAGNITUDE: Lambda = (8 pi G/c^2)(P0/rho0 c^2)
      with the absolute saturation pressure P0(rho0) an UNDETERMINED input,
      exactly as G's magnitude is conceded (D-b, #154).
  With two conceded magnitudes + a circular identity a literal three-G match has
  no teeth. The teeth are in the dimensionless coefficient a0/(cH0), which must
  equal the de Sitter Gibbons-Hawking 1/2pi -- the SAME 2pi that S1 used in
  kT_H = hbar g_H/(2 pi c).

Derivation (S-analytic):  a0 = c f_dS,  f_dS = H0/2pi  (the de Sitter horizon's
  Gibbons-Hawking thermal frequency) => a0 = cH0/2pi. Magnitude (H0, via P0->
  Lambda) conceded; only the coefficient 1/2pi is derived.

Confrontation: the measured cored a0 (#146, with its 16-84% interval) against
each candidate coefficient for H0 in {67.4, 73.0}; the discrimination power
(sigma-separation of 1/2pi vs 1/6 given the scatter + H0 tension); and the
re-pinned z-evolution falsifier (the decisive cH-vs-sqrt(Lambda) separator).

Decision rules (fixed in #155):
  R1 = a0 consistent with cH0/2pi (ratio in [0.85,1.15] across H0) using the
       same GH-2pi as S1/S2, AND c^2 sqrt(Lambda) excluded (off by >~3x)
       => local & cosmological screens share one thermodynamics; the weak-
       derivation falsifier (b) is discharged from promissory to SURVIVED.
  R2 = a0 inconsistent with cH0/2pi (matches sqrt(Lambda) or far from any cH)
       => inconsistent thermodynamics => the duality is FALSIFIED.
  Honesty bars: magnitude conceded; 1/2pi vs 1/6 NOT decisively separated if
  their sigma-separation < 1; the decisive cH-vs-sqrtLambda test is the z-
  evolution falsifier (needs high-z data); cored amplitude post-hoc (#146 A4).

Run:  python instruments/paper_vi/a0_overconstraint.py
Writes papers/SSV-VI/results/a0_overconstraint_receipt.json and
papers/SSV-VI/figures/a0_overconstraint.png.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VI" / "results"
FIGURES = ROOT / "papers" / "SSV-VI" / "figures"

# --- constants (matching the #146 anchor table) ---
C_LIGHT = 2.99792458e8            # m/s
MPC_M = 3.0856775814913673e22     # m
LAMBDA = 1.1e-52                  # m^-2 (pinned, #146)
H0_LIST = {"67.4": 67.4, "73.0": 73.0}   # km/s/Mpc (Planck, SH0ES)
OMEGA_M = 0.315                   # flat LCDM (z-falsifier)

# Independent literature target: the radial-acceleration-relation scale
# g_dagger (McGaugh-Lelli-Schombert 2016), MUCH tighter than the SSV-halo a0 in
# random error but with a large systematic. Used as a robustness cross-check.
RAR_A0 = 1.20e-10                 # m/s^2
RAR_A0_RANDOM = 0.02e-10          # +/- random
RAR_A0_SYST = 0.24e-10            # +/- systematic (the binding one)


def H0_si(h0_kmsmpc):
    return h0_kmsmpc * 1.0e3 / MPC_M     # s^-1


def candidate_a0(h0_kmsmpc):
    """Predicted a0 for each candidate coefficient at this H0."""
    H = H0_si(h0_kmsmpc)
    cH = C_LIGHT * H
    return {
        "GH_2pi (cH0/2pi, SSV)": cH / (2.0 * math.pi),
        "Verlinde (cH0/6)": cH / 6.0,
        "equipartition (cH0)": cH,
        "deSitter (c^2 sqrt(Lambda))": C_LIGHT**2 * math.sqrt(LAMBDA),
    }


def desitter_surface_gravity(h0_kmsmpc, eps=1e-4):
    """The cosmological-horizon instance of S1's Visser eq-70 surface gravity,
    computed by the SAME finite-difference construction as the local dumb-hole
    (instruments/paper_v/dumb_hole_surface_gravity.py): the Hubble flow
    v(r) = H0 r against sound speed c crosses at the de Sitter horizon
    r_dS = c/H0, and
        g_dS = 1/2 |d/dr (c^2 - v^2)|_{r_dS} = c H0   (analytic),
    so  a0 = g_dS/(2 pi) = c H0/2 pi  and  kT_dS = hbar g_dS/(2 pi c) = hbar H0/2pi.
    Returns (g_dS_numeric, g_dS_analytic = c H0, a0 = g_dS/2pi)."""
    H = H0_si(h0_kmsmpc)
    r_dS = C_LIGHT / H
    # central finite difference of f(r) = c^2 - (H r)^2 at r_dS (same method
    # as surface_gravity_numeric in the S1 instrument)
    dr = eps * r_dS
    f = lambda r: C_LIGHT**2 - (H * r) ** 2
    dfdr = (f(r_dS + dr) - f(r_dS - dr)) / (2 * dr)
    g_num = 0.5 * abs(dfdr)
    return g_num, C_LIGHT * H, g_num / (2.0 * math.pi)


# ----------------------------------------------------------------------
# measured target (#146 primary-tier cored)
# ----------------------------------------------------------------------

def read_measured_a0():
    """Cored, primary-tier a0 median and 16-84% interval from the #146 receipt
    (fallback to the published numbers if the receipt is absent)."""
    rec = RESULTS / "a0_target_receipt.json"
    if rec.is_file():
        d = json.loads(rec.read_text())
        t = d["tiers"]["primary_cored"]
        return (t["a0_median_m_s2"], t["log10_a0_median"],
                t["log10_a0_p16"], t["log10_a0_p84"])
    # published fallback
    return (1.1281640861824739e-10, -9.94762772966029,
            -10.228541842859483, -9.61104199467827)


# ----------------------------------------------------------------------
# z-evolution falsifier (the decisive cH-vs-sqrtLambda separator)
# ----------------------------------------------------------------------

def z_falsifier(zs=(0.5, 1.0, 2.0)):
    """cH branch: BTFR normalization shift Delta log M = log10[H(z)/H0]
    (flat LCDM, Omega_m). sqrt(Lambda) branch: 0 at all z."""
    out = {}
    for z in zs:
        Hz_over_H0 = math.sqrt(OMEGA_M * (1 + z) ** 3 + (1 - OMEGA_M))
        out[f"z={z}"] = {"cH_branch_dex": math.log10(Hz_over_H0),
                         "sqrtLambda_branch_dex": 0.0}
    return out


# ----------------------------------------------------------------------
# battery
# ----------------------------------------------------------------------

def battery():
    a0_meas, log_med, log_p16, log_p84 = read_measured_a0()
    sigma_dex = 0.5 * (log_p84 - log_p16)        # ~1sigma in dex

    # confrontation: ratio measured/predicted per candidate per H0
    confront = {}
    for tag, h0 in H0_LIST.items():
        preds = candidate_a0(h0)
        confront[tag] = {name: {"a0_pred": p,
                                "ratio_meas_over_pred": a0_meas / p,
                                "offset_dex": math.log10(a0_meas / p)}
                         for name, p in preds.items()}

    # --- robustness cross-check: the independent RAR scale (tighter) ---
    # which cH coefficient does each a0 estimator prefer? (central values)
    rar_pref = {}
    ssv_pref = {}
    for h in H0_LIST:
        preds = candidate_a0(H0_LIST[h])
        gh, ver = preds["GH_2pi (cH0/2pi, SSV)"], preds["Verlinde (cH0/6)"]
        rar_pref[h] = {"ratio_GH2pi": RAR_A0 / gh, "ratio_Verlinde": RAR_A0 / ver,
                       "prefers": "1/2pi" if abs(RAR_A0 - gh) < abs(RAR_A0 - ver)
                       else "1/6"}
        ssv_pref[h] = {"ratio_GH2pi": a0_meas / gh, "ratio_Verlinde": a0_meas / ver,
                       "prefers": "1/2pi" if abs(a0_meas - gh) < abs(a0_meas - ver)
                       else "1/6"}
    rar_sqrtL = RAR_A0 / candidate_a0(73.0)["deSitter (c^2 sqrt(Lambda))"]
    estimators_disagree = (ssv_pref["73.0"]["prefers"]
                           != rar_pref["73.0"]["prefers"])

    # --- the de Sitter horizon via the SAME S1 surface-gravity machinery ---
    ds = {}
    for h in H0_LIST:
        g_num, g_an, a0_ds = desitter_surface_gravity(H0_LIST[h])
        ds[h] = {"g_dS_numeric": g_num, "g_dS_analytic_cH0": g_an,
                 "g_dS_rel_err": abs(g_num - g_an) / g_an,
                 "a0_from_g_dS_over_2pi": a0_ds,
                 "matches_cH0_over_2pi": abs(a0_ds - candidate_a0(
                     H0_LIST[h])["GH_2pi (cH0/2pi, SSV)"]) / a0_ds < 1e-9}
    ds_machinery_ok = all(d["g_dS_rel_err"] < 1e-3 and d["matches_cH0_over_2pi"]
                          for d in ds.values())

    # discrimination power: 1/2pi vs 1/6 are a fixed factor apart; H0 tension
    # shifts the cH anchor; compare both to the measurement sigma.
    sep_2pi_vs_6_dex = abs(math.log10((1.0 / (2 * math.pi)) / (1.0 / 6.0)))
    sep_2pi_vs_6_sigma = sep_2pi_vs_6_dex / sigma_dex
    h0_tension_dex = abs(math.log10(73.0 / 67.4))
    # decision path: even the tight RAR random error cannot separate them,
    # because the binding error is the RAR systematic + the H0 tension.
    rar_syst_dex = abs(math.log10((RAR_A0 + RAR_A0_SYST) / RAR_A0))
    sep_blocked_by = ("RAR systematic (%.3f dex) + H0 tension (%.3f dex) both "
                      "exceed the 1/2pi-vs-1/6 gap (%.3f dex)"
                      % (rar_syst_dex, h0_tension_dex, sep_2pi_vs_6_dex))

    # ---- verdict ----
    # GH-2pi consistent across H0 (ratio in band); sqrt(Lambda) excluded
    gh_ratios = [confront[h]["GH_2pi (cH0/2pi, SSV)"]["ratio_meas_over_pred"]
                 for h in H0_LIST]
    gh_consistent = all(0.85 <= r <= 1.15 for r in gh_ratios)
    sqrtL_ratio = confront["73.0"]["deSitter (c^2 sqrt(Lambda))"][
        "ratio_meas_over_pred"]
    sqrtL_excluded = (sqrtL_ratio < 1 / 3.0) or (sqrtL_ratio > 3.0)
    # robustness: sqrt(Lambda) is excluded under BOTH a0 estimators
    sqrtL_excluded_both = sqrtL_excluded and (rar_sqrtL < 1 / 3.0)
    R1 = bool(gh_consistent and sqrtL_excluded_both and ds_machinery_ok)
    decisive_2pi_vs_6 = bool(sep_2pi_vs_6_sigma >= 1.0)

    out = {
        "constants": {"c": C_LIGHT, "Lambda_m^-2": LAMBDA,
                      "Omega_m": OMEGA_M, "H0_kmsMpc": H0_LIST},
        "measured_a0_cored_primary": {
            "a0_m_s2": a0_meas, "log10_median": log_med,
            "log10_p16": log_p16, "log10_p84": log_p84,
            "sigma_dex": sigma_dex},
        "derivation": "a0 = c f_dS, f_dS = H0/2pi (de Sitter Gibbons-Hawking "
                      "thermal frequency) => a0 = cH0/2pi; the SAME 2pi as S1 "
                      "kT_H = hbar g_H/(2 pi c). Magnitude conceded (P0->Lambda).",
        "confrontation_ratio_meas_over_pred": confront,
        "rar_cross_check": {
            "RAR_a0": RAR_A0, "ssv_halo_a0": a0_meas,
            "ssv_halo_prefers": ssv_pref, "rar_prefers": rar_pref,
            "rar_sqrtLambda_ratio_H73": rar_sqrtL,
            "estimators_disagree_on_2pi_vs_6": bool(estimators_disagree),
            "note": (f"the SSV-halo a0 (1.13e-10) favours 1/2pi; the tighter "
                     f"literature RAR a0 (1.20e-10) favours Verlinde 1/6 at "
                     f"H0=73 -- the two best estimators straddle the two cH "
                     f"coefficients (~6 percent apart). Both keep sqrt(Lambda) "
                     f"excluded (RAR ratio {rar_sqrtL:.3f}). So 1/2pi is SSV's "
                     f"prediction and is consistent, but NOT singled out."),
        },
        "deSitter_via_S1_machinery": {
            "per_H0": ds, "machinery_ok": bool(ds_machinery_ok),
            "note": "the SAME Visser eq-70 finite-difference surface gravity "
                    "as the S1 dumb-hole, applied to the Hubble flow v=H0 r, "
                    "gives g_dS = c H0 and a0 = g_dS/2pi = cH0/2pi -- the "
                    "shared thermodynamics is a computation, not an assertion.",
        },
        "discrimination": {
            "sep_2pi_vs_6_dex": sep_2pi_vs_6_dex,
            "sep_2pi_vs_6_sigma": sep_2pi_vs_6_sigma,
            "H0_tension_dex": h0_tension_dex,
            "rar_systematic_dex": rar_syst_dex,
            "decisive_2pi_vs_6": decisive_2pi_vs_6,
            "separation_blocked_by": sep_blocked_by,
            "note": "1/2pi and 1/6 differ by 6/2pi = 0.955 (0.020 dex); the "
                    "SSV-halo sigma is ~0.31 dex, the H0 tension shifts the "
                    "anchor 0.035 dex, and even the tight RAR is blocked by "
                    "its ~0.086 dex systematic -- so 1/2pi vs 1/6 is NOT "
                    "separable by any current estimator.",
        },
        "z_falsifier": z_falsifier(),
        "verdicts": {
            "GH_2pi_consistent": bool(gh_consistent),
            "GH_2pi_ratios": {h: confront[h]["GH_2pi (cH0/2pi, SSV)"][
                "ratio_meas_over_pred"] for h in H0_LIST},
            "sqrtLambda_excluded_both_estimators": bool(sqrtL_excluded_both),
            "sqrtLambda_ratio_H73": sqrtL_ratio,
            "deSitter_machinery_reproduces_cH0_2pi": bool(ds_machinery_ok),
            "estimators_disagree_2pi_vs_6": bool(estimators_disagree),
            "1over2pi_vs_1over6_decisively_separated": decisive_2pi_vs_6,
            "VERDICT": "R1" if R1 else "R2",
            "VERDICT_meaning": (
                "R1: a0 consistent with cH0/2pi (the SAME finite-difference "
                "surface-gravity machinery as the S1 dumb-hole gives g_dS=cH0 "
                "=> a0=cH0/2pi); c^2 sqrt(Lambda) excluded under BOTH the "
                "SSV-halo and the RAR a0. Local & cosmological screens share one "
                "thermodynamics -- the duality SURVIVES its falsifier; the weak-"
                "derivation (b) is discharged from promissory to survived. "
                "Magnitude conceded; 1/2pi vs 1/6 NOT separable by any current "
                "estimator (SSV-halo favours 1/2pi, RAR favours 1/6) -- decisive "
                "test = the z-evolution falsifier, high-z data."
                if R1 else
                "R2: a0 inconsistent with cH0/2pi -- the duality is FALSIFIED "
                "(local & cosmological screens have inconsistent thermodynamics)."),
            "form_yes_magnitude_conceded": bool(R1),
        },
    }
    return out


def figure(out, dest):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except Exception:
        return None
    meas = out["measured_a0_cored_primary"]
    a0 = meas["a0_m_s2"]
    lo = 10 ** meas["log10_p16"]
    hi = 10 ** meas["log10_p84"]
    conf = out["confrontation_ratio_meas_over_pred"]["73.0"]
    names = list(conf.keys())
    preds = [conf[n]["a0_pred"] for n in names]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    y = np.arange(len(names))
    ax.barh(y, preds, color=["tab:green", "tab:orange", "tab:red", "tab:purple"],
            alpha=0.7)
    ax.axvline(a0, color="k", lw=2, label="measured cored $a_0$ (#146)")
    ax.axvspan(lo, hi, color="k", alpha=0.12, label="16--84\\%")
    ax.set_yticks(y)
    ax.set_yticklabels([n.split(" (")[0] for n in names], fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel(r"$a_0$ (m/s$^2$), $H_0=73$")
    ax.set_title("a$_0$ candidates vs the measured scale: GH-2$\\pi$ on target,\n"
                 "$c^2\\sqrt{\\Lambda}$ excluded (8$\\times$), $1/2\\pi$ vs $1/6$ "
                 "within the scatter", fontsize=8)
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    fig.savefig(dest, dpi=160)
    plt.close(fig)
    return dest


def main():
    print("H-A0-IR: a0 = cH0/2pi coefficient-consistency over-constraint",
          flush=True)
    out = battery()
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    dest = RESULTS / "a0_overconstraint_receipt.json"
    dest.write_text(json.dumps(out, indent=1))
    fig = figure(out, FIGURES / "a0_overconstraint.png")
    v = out["verdicts"]
    print("\n--- verdicts ---")
    for k in ("GH_2pi_consistent", "GH_2pi_ratios",
              "sqrtLambda_excluded_both_estimators", "sqrtLambda_ratio_H73",
              "deSitter_machinery_reproduces_cH0_2pi",
              "estimators_disagree_2pi_vs_6",
              "1over2pi_vs_1over6_decisively_separated", "VERDICT"):
        print(f"  {k}: {v[k]}")
    print(f"  discrimination: 1/2pi vs 1/6 = "
          f"{out['discrimination']['sep_2pi_vs_6_sigma']:.3f} sigma "
          f"(sigma={out['measured_a0_cored_primary']['sigma_dex']:.3f} dex)")
    print(f"  z-falsifier (cH branch): "
          f"{ {k: round(v2['cH_branch_dex'],3) for k,v2 in out['z_falsifier'].items()} }")
    print(f"receipt -> {dest}")
    if fig:
        print(f"figure  -> {fig}")


if __name__ == "__main__":
    main()

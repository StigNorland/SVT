"""#146 H-A0 S0 -- the measured acceleration scale.

Measurement side ONLY of the #129 item-1 reframe: convert the frozen
#133/#136 per-galaxy halo amplitudes (papers/SSV-VI/results/
sparc_per_galaxy_results.csv) into the acceleration-scale form

    a0_h = v_h^4 / (G * M_bar)

(the deep-limit identity: for v^2 = v_bar^2 + v_h^2 with the halo
dominating at large r, the constant-v_h form coincides with the MOND
simple/RAR-nu deep limit with the same a0), test single-scale constancy
(rule A1), pin the target window for any future H-A0 derivation (rule
A2), price the anchors without declaring any of them hit (rule A3), and
emit the redshift-falsifier table fixed in the pre-registration.

No new fitting against rotation curves happens here; the only inputs
are the published per-galaxy fit results.  Decision rules live in issue
#146 and are evaluated verbatim.

Run:  python instruments/paper_vi/a0_from_vh.py [--quick]
Writes papers/SSV-VI/results/a0_target_receipt.json.
"""

from __future__ import annotations

import csv
import json
import math
import os

import numpy as np

# ---------------------------------------------------------------- constants
G_SI = 6.674e-11                  # m^3 kg^-1 s^-2
M_SUN = 1.989e30                  # kg
C_SI = 2.998e8                    # m/s
MPC = 3.0857e22                   # m
LAMBDA_SI = 1.10e-52              # m^-2  (pinned in #146)
H0_VALUES = (67.4, 73.0)          # km/s/Mpc (Planck / SH0ES, pinned)
OMEGA_M = 0.315                   # flat LCDM, pinned
A0_RAR = 1.2e-10                  # m/s^2 (literature RAR scale, pinned)
Z_GRID = (0.5, 1.0, 2.0)

# cored-fit bounds from instruments/paper_vi/sparc_halo_fit.py
# (0 <= vh <= 500 km/s, 0.01 <= rc <= 50 kpc): bound-hitters are
# degenerate fits and are excluded with their count reported (#146).
CORED_RC_BOUND = 49.0
CORED_VH_BOUND = 495.0

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CSV_PATH = os.path.join(REPO, "papers", "SSV-VI", "results",
                        "sparc_per_galaxy_results.csv")
RECEIPT = os.path.join(REPO, "papers", "SSV-VI", "results",
                       "a0_target_receipt.json")


def a0_from(vh_kms: float, mbar_msun: float) -> float:
    """a0_h = v_h^4 / (G M_bar) in m/s^2 (the deep-limit identity)."""
    v = vh_kms * 1.0e3
    return v ** 4 / (G_SI * mbar_msun * M_SUN)


def load_rows(path: str = CSV_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def tier_mask(rows: list[dict], tier: str) -> list[bool]:
    if tier == "primary":
        return [int(r["in_primary"]) == 1 for r in rows]
    if tier == "q2":
        return [int(r["Q"]) <= 2 for r in rows]
    if tier == "all":
        return [True for _ in rows]
    raise ValueError(tier)


def amplitude(rows: list[dict], which: str):
    """Return (vh list, n_excluded, exclusion reason counts).

    'nocore': vh_kms, excluding vh <= 0 (a0 undefined in log space).
    'cored' : cored_vh, additionally excluding bound-hitting fits
              (rc >= 49 kpc or vh >= 495 km/s) -- degenerate.
    """
    vals, reasons = [], {"vh_zero": 0, "rc_bound": 0, "vh_bound": 0}
    for r in rows:
        if which == "nocore":
            vh = float(r["vh_kms"])
            if vh <= 0.0:
                reasons["vh_zero"] += 1
                vals.append(None)
                continue
        elif which == "cored":
            vh = float(r["cored_vh"])
            rc = float(r["cored_rc_kpc"])
            if vh <= 0.0:
                reasons["vh_zero"] += 1
                vals.append(None)
                continue
            if rc >= CORED_RC_BOUND:
                reasons["rc_bound"] += 1
                vals.append(None)
                continue
            if vh >= CORED_VH_BOUND:
                reasons["vh_bound"] += 1
                vals.append(None)
                continue
        else:
            raise ValueError(which)
        vals.append(vh)
    n_exc = sum(v is None for v in vals)
    return vals, n_exc, reasons


def slope_with_bootstrap(logm: np.ndarray, loga: np.ndarray,
                         n_boot: int = 2000, seed: int = 146):
    """OLS slope of log10 a0 vs log10 M_bar + bootstrap 95% CI."""
    sl, ic = np.polyfit(logm, loga, 1)
    rng = np.random.default_rng(seed)
    n = len(logm)
    boots = np.empty(n_boot)
    for i in range(n_boot):
        j = rng.integers(0, n, n)
        boots[i] = np.polyfit(logm[j], loga[j], 1)[0]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return float(sl), float(ic), float(lo), float(hi)


def analyse(rows: list[dict], n_boot: int = 2000) -> dict:
    out = {}
    for tier in ("primary", "q2", "all"):
        tmask = tier_mask(rows, tier)
        for amp in ("nocore", "cored"):
            vals, n_exc, reasons = amplitude(rows, amp)
            logm, loga = [], []
            for r, m, v in zip(rows, tmask, vals):
                if not m or v is None:
                    continue
                logm.append(math.log10(float(r["Mbar_Msun"])))
                loga.append(math.log10(a0_from(v, float(r["Mbar_Msun"]))))
            logm = np.asarray(logm)
            loga = np.asarray(loga)
            med, p16, p84 = np.percentile(loga, [50, 16, 84])
            sl, ic, lo, hi = slope_with_bootstrap(logm, loga, n_boot)
            n_tier = int(sum(tmask))
            out[f"{tier}_{amp}"] = {
                "n_tier": n_tier,
                "n_used": int(len(loga)),
                "n_excluded": n_tier - int(len(loga)),
                "exclusion_reasons_global": reasons,
                "log10_a0_median": float(med),
                "log10_a0_p16": float(p16),
                "log10_a0_p84": float(p84),
                "a0_median_m_s2": float(10.0 ** med),
                "slope_log_a0_vs_log_M": sl,
                "slope_ci95": [lo, hi],
                # v_h^4 = G M a0  =>  4 dlogv/dlogM = 1 + s
                # =>  BTFR slope dlogM/dlogv = 4/(1+s)
                "equiv_btfr_slope": float(4.0 / (1.0 + sl)),
            }
    return out


def anchors() -> dict:
    table = {}
    for h0 in H0_VALUES:
        h0_si = h0 * 1.0e3 / MPC
        table[f"cH0_over_2pi_H0_{h0}"] = C_SI * h0_si / (2.0 * math.pi)
    table["c2_sqrt_Lambda"] = C_SI ** 2 * math.sqrt(LAMBDA_SI)
    table["RAR_literature"] = A0_RAR
    return table


def z_falsifier_table() -> dict:
    """cH-anchor BTFR-normalization shift Delta log10 M(z) =
    log10[H(z)/H0] (flat LCDM); sqrt(Lambda) anchor: identically 0."""
    out = {}
    for z in Z_GRID:
        hz = math.sqrt(OMEGA_M * (1.0 + z) ** 3 + (1.0 - OMEGA_M))
        out[f"z_{z}"] = {"H_over_H0": hz,
                         "cH_anchor_dlog10_M": math.log10(hz),
                         "sqrtLambda_anchor_dlog10_M": 0.0}
    return out


def evaluate_rules(stats: dict) -> dict:
    """Decision rules A1-A4 of #146, verbatim."""
    a1 = {}
    for amp in ("nocore", "cored"):
        s = stats[f"primary_{amp}"]
        a1[amp] = {"slope": s["slope_log_a0_vs_log_M"],
                   "ci95": s["slope_ci95"],
                   "pass_abs_slope_le_0p10":
                       abs(s["slope_log_a0_vs_log_M"]) <= 0.10}

    cored = stats["primary_cored"]
    nocore = stats["primary_nocore"]
    spread = abs(cored["log10_a0_median"] - nocore["log10_a0_median"])
    a4_wide = spread > 0.3
    if a4_wide:                       # A4: window must cover both amplitudes
        lo = min(cored["log10_a0_p16"], nocore["log10_a0_p16"])
        hi = max(cored["log10_a0_p84"], nocore["log10_a0_p84"])
    else:
        lo, hi = cored["log10_a0_p16"], cored["log10_a0_p84"]
    a2 = {"target_log10_a0_window": [float(lo), float(hi)],
          "target_a0_window_m_s2": [float(10.0 ** lo), float(10.0 ** hi)],
          "headline_log10_a0": cored["log10_a0_median"],
          "status": "from post-hoc-flagged cored amplitude; flag propagates "
                    "until the #133 r_c promotion condition is met"}
    anch = anchors()
    a3 = {name: {"value_m_s2": val,
                 "ratio_cored_median_over_anchor":
                     cored["a0_median_m_s2"] / val,
                 "ratio_nocore_median_over_anchor":
                     nocore["a0_median_m_s2"] / val}
          for name, val in anch.items()}
    return {"A1_constancy": a1,
            "A2_target": a2,
            "A3_anchor_table_no_anchor_declared_hit": a3,
            "A4_two_amplitude_spread_dex": float(spread),
            "A4_wide_window_applied": bool(a4_wide)}


def main(quick: bool = False) -> dict:
    rows = load_rows()
    n_boot = 200 if quick else 2000
    stats = analyse(rows, n_boot=n_boot)
    rules = evaluate_rules(stats)
    receipt = {
        "issue": 146,
        "hypothesis": "H-A0 S0: single galaxy-independent a0_h = "
                      "v_h^4/(G M_bar) (measurement side only)",
        "inputs": "papers/SSV-VI/results/sparc_per_galaxy_results.csv "
                  "(frozen #133/#136 fits; no new fitting)",
        "pinned_constants": {
            "G_SI": G_SI, "M_sun_kg": M_SUN, "c_m_s": C_SI,
            "Lambda_m^-2": LAMBDA_SI, "H0_km_s_Mpc": list(H0_VALUES),
            "Omega_m": OMEGA_M, "a0_RAR_m_s2": A0_RAR},
        "tiers": stats,
        "rules": rules,
        "z_falsifier_table": z_falsifier_table(),
    }
    os.makedirs(os.path.dirname(RECEIPT), exist_ok=True)
    with open(RECEIPT, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)

    print(f"H-A0 S0 (#146)  --  receipt -> {os.path.relpath(RECEIPT, REPO)}")
    for key in ("primary_nocore", "primary_cored"):
        s = stats[key]
        print(f"  {key}: n={s['n_used']}/{s['n_tier']}  "
              f"log10 a0 = {s['log10_a0_median']:+.3f} "
              f"[{s['log10_a0_p16']:+.3f}, {s['log10_a0_p84']:+.3f}]  "
              f"a0 = {s['a0_median_m_s2']:.3e} m/s^2  "
              f"slope = {s['slope_log_a0_vs_log_M']:+.3f} "
              f"CI {s['slope_ci95']}")
    a1 = rules["A1_constancy"]
    print(f"  A1 constancy: nocore "
          f"{'PASS' if a1['nocore']['pass_abs_slope_le_0p10'] else 'FAIL'}, "
          f"cored {'PASS' if a1['cored']['pass_abs_slope_le_0p10'] else 'FAIL'}")
    a2 = rules["A2_target"]
    print(f"  A2 target window: log10 a0 in "
          f"[{a2['target_log10_a0_window'][0]:+.3f}, "
          f"{a2['target_log10_a0_window'][1]:+.3f}]  "
          f"(A4 wide window: {rules['A4_wide_window_applied']}, "
          f"spread {rules['A4_two_amplitude_spread_dex']:.3f} dex)")
    for name, row in rules["A3_anchor_table_no_anchor_declared_hit"].items():
        print(f"  A3 {name}: {row['value_m_s2']:.3e} m/s^2  "
              f"cored/anchor = {row['ratio_cored_median_over_anchor']:.3f}  "
              f"nocore/anchor = {row['ratio_nocore_median_over_anchor']:.3f}")
    return receipt


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="reduced bootstrap (CI only; medians unchanged)")
    args = ap.parse_args()
    main(quick=args.quick)

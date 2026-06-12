"""#147 DSPH-LEDGER -- the dwarf-spheroidal discriminator, run as a ledger.

#129 item 3 (inherited from H7a's corollary): dispersion-supported dwarfs
barely rotate yet are DM-dominated -- the standing falsifier for
circulation-sourced halo phenomenology.  Three pre-registered questions
(issue #147, rules fixed before computing):

  B1  mass law vs rotation law: do the eight classical Milky Way dSphs
      follow the #133 v_h(M_bar) relation (model A), or the
      rotation-proportional entrainment law v_h ~ Gamma_bar = 2 pi R v_rot
      (model B, normalized at the H9 MW reference)?
  B2  circulation budget (honesty check): do the dwarfs' rotation UPPER
      LIMITS still carry more circulation than the H9-inverted requirement
      Gamma_req(M)?  (Expected: yes -- the budget does NOT bind.)
  B3  universal core: does the #133 post-hoc cored form with a universal
      r_c = 2.5 kpc (most dwarf-favorable quartile) under-predict the
      dwarfs' dispersions by > 2x?

Pinned data: McConnachie 2012 (AJ 144, 4) compilation values; Wolf et al.
2010 mass estimator v_c(r_1/2) = sqrt(3) sigma_los at r_1/2 = (4/3) R_e.
Decision rules are evaluated verbatim; robustness sweeps (M*/L x/÷2,
v_rot in {1, 3, 10} km/s, +/-30% anisotropy systematic on v_c) are part of
the pre-registration: verdicts must be sweep-stable or are reported fragile.

Run:  python instruments/paper_vi/dsph_ledger.py [--quick]
Writes papers/SSV-VI/results/dsph_ledger_receipt.json and (unless --quick)
papers/SSV-VI/figures/fig_dsph_ledger.png.
"""

from __future__ import annotations

import csv
import json
import math
import os

import numpy as np

# ---------------------------------------------------------------- constants
G_PC = 4.30091e-3        # G in pc (km/s)^2 / M_sun
PC_M = 3.0857e16         # m
KM = 1.0e3               # m

# #133 mass law (model A):  log10 v_h = SLOPE log10 M_bar + INTERCEPT
SLOPE_A = 0.256
INTERCEPT_A = -0.665

# H9 MW reference (h9_triangle_receipt.json) and inversion
M_MW = 6.0e10            # M_sun
R_MW_KPC = 15.0          # kpc
V_MW = 220.0             # km/s
GAMMA_REQ_MW = 1.297e9   # m^2/s, Gamma_req at M_MW;  Gamma_req ~ M^{1/4}

R_C_UNIVERSAL_KPC = 2.5  # #133 post-hoc r_c lower quartile (dwarf-favorable)

# ------------------------------------------------- pinned data (issue #147)
# name, L_V (1e6 L_sun), sigma_los (km/s), R_e projected (pc)
DSPH = [
    ("Fornax",     20.0, 11.7, 710.0),
    ("Leo I",       5.5,  9.2, 251.0),
    ("Sculptor",    2.3,  9.2, 283.0),
    ("Leo II",      0.74, 6.6, 176.0),
    ("Sextans",     0.44, 7.9, 695.0),
    ("Carina",      0.38, 6.6, 250.0),
    ("Ursa Minor",  0.29, 9.5, 181.0),
    ("Draco",       0.29, 9.1, 221.0),
]

ML_BASE, ML_SWEEP = 1.6, (0.8, 1.6, 3.2)     # M*/L_V
VROT_BASE, VROT_SWEEP = 3.0, (1.0, 3.0, 10.0)  # km/s upper limit
ANISO_SWEEP = (0.7, 1.0, 1.3)                # systematic factor on v_c

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RECEIPT = os.path.join(REPO, "papers", "SSV-VI", "results",
                       "dsph_ledger_receipt.json")
FIGURE = os.path.join(REPO, "papers", "SSV-VI", "figures",
                      "fig_dsph_ledger.png")
SPARC_CSV = os.path.join(REPO, "papers", "SSV-VI", "results",
                         "sparc_per_galaxy_results.csv")


def model_a_vh(mbar_msun: float) -> float:
    """#133 mass law, km/s."""
    return 10.0 ** (SLOPE_A * math.log10(mbar_msun) + INTERCEPT_A)


def model_b_vh(re_kpc: float, vrot_kms: float) -> float:
    """Rotation-proportional entrainment, normalized at the H9 MW
    reference: v_h = v_h_A(M_MW) * (R v_rot) / (R_MW v_MW)."""
    return model_a_vh(M_MW) * (re_kpc * vrot_kms) / (R_MW_KPC * V_MW)


def gamma_req(mbar_msun: float) -> float:
    """H9-inverted circulation requirement, m^2/s (Gamma ~ M^{1/4})."""
    return GAMMA_REQ_MW * (mbar_msun / M_MW) ** 0.25


def dwarf_row(name, lv6, sigma, re_pc, *, ml=ML_BASE, vrot=VROT_BASE,
              aniso=1.0):
    """All derived quantities for one dwarf at given sweep settings."""
    mstar = ml * lv6 * 1.0e6                  # M_sun (gas-free)
    r_half = (4.0 / 3.0) * re_pc              # 3D half-light radius, pc
    v_c = math.sqrt(3.0) * sigma * aniso      # Wolf, km/s
    v_bar_sq = G_PC * (mstar / 2.0) / r_half  # (km/s)^2
    v_h_obs = math.sqrt(max(v_c ** 2 - v_bar_sq, 0.0))
    v_h_a = model_a_vh(mstar)
    v_h_b = model_b_vh(re_pc / 1.0e3, vrot)
    # B3: universal-core prediction at r_1/2
    r_kpc = r_half / 1.0e3
    core_fac = r_kpc ** 2 / (r_kpc ** 2 + R_C_UNIVERSAL_KPC ** 2)
    sigma_pred = math.sqrt((v_bar_sq + v_h_a ** 2 * core_fac) / 3.0)
    # B2: circulation budget vs requirement (SI)
    gamma_bar = 2.0 * math.pi * (re_pc * PC_M) * (vrot * KM)
    return {
        "name": name, "M_star_Msun": mstar, "r_half_pc": r_half,
        "sigma_obs_kms": sigma, "v_c_kms": v_c,
        "v_bar_kms": math.sqrt(v_bar_sq), "v_h_obs_kms": v_h_obs,
        "v_h_modelA_kms": v_h_a, "v_h_modelB_upper_kms": v_h_b,
        "delta_A_dex": math.log10(v_h_obs / v_h_a) if v_h_obs > 0 else None,
        "delta_B_dex": math.log10(v_h_obs / v_h_b) if v_h_obs > 0 else None,
        "sigma_pred_universal_core_kms": sigma_pred,
        "below_half_sigma": sigma_pred < sigma / 2.0,
        "gamma_bar_limit_m2_s": gamma_bar,
        "gamma_req_m2_s": gamma_req(mstar),
        "budget_ratio": gamma_bar / gamma_req(mstar),
    }


def ledger(*, ml=ML_BASE, vrot=VROT_BASE, aniso=1.0):
    return [dwarf_row(*d, ml=ml, vrot=vrot, aniso=aniso) for d in DSPH]


def verdicts(rows):
    """B1/B2/B3 rules of #147, verbatim."""
    da = sorted(r["delta_A_dex"] for r in rows)
    db = sorted(r["delta_B_dex"] for r in rows)
    med_a = 0.5 * (da[3] + da[4])
    med_b = 0.5 * (db[3] + db[4])
    if med_b >= 1.5 and abs(med_a) <= 0.5:
        b1 = "rotation-proportional entrainment FALSIFIED"
    elif med_a < -0.5:
        b1 = "mass law fails out-of-sample (dwarfs below relation)"
    elif med_a > 0.5:
        b1 = "mass law under-predicts dwarfs (recorded; tidal confound)"
    else:
        b1 = "inconclusive on pre-registered thresholds"
    n_below = sum(r["below_half_sigma"] for r in rows)
    return {
        "median_delta_A_dex": med_a,
        "median_delta_B_dex": med_b,
        "B1": b1,
        "B2_budget_binds": bool(any(r["budget_ratio"] < 1.0 for r in rows)),
        "B2_min_budget_ratio": min(r["budget_ratio"] for r in rows),
        "B3_n_below_half_sigma": int(n_below),
        "B3": ("universal kpc-scale core FALSIFIED at dSph scales"
               if n_below >= 6 else "universal core survives at dwarfs"),
    }


def sweep():
    """Pre-registered robustness sweep; verdict stability check."""
    out = []
    for ml in ML_SWEEP:
        for vrot in VROT_SWEEP:
            for an in ANISO_SWEEP:
                v = verdicts(ledger(ml=ml, vrot=vrot, aniso=an))
                out.append({"ml": ml, "vrot_kms": vrot, "aniso": an,
                            "B1": v["B1"],
                            "median_delta_A_dex": v["median_delta_A_dex"],
                            "median_delta_B_dex": v["median_delta_B_dex"],
                            "B3_n_below": v["B3_n_below_half_sigma"]})
    return out


def make_figure(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    # SPARC primary tier as background
    with open(SPARC_CSV, newline="", encoding="utf-8-sig") as fh:
        sparc = [r for r in csv.DictReader(fh)
                 if int(r["in_primary"]) == 1 and float(r["vh_kms"]) > 0]
    ax.plot([float(r["Mbar_Msun"]) for r in sparc],
            [float(r["vh_kms"]) for r in sparc],
            "o", ms=3.5, mfc="0.75", mec="0.55", zorder=1,
            label="SPARC primary tier (#133 fits)")
    mm = np.logspace(4.5, 11.7, 100)
    ax.plot(mm, [model_a_vh(m) for m in mm], "b-", lw=1.6, zorder=2,
            label=r"model A: $\log v_h = 0.256\,\log M_{\rm bar} - 0.665$")
    ax.fill_between(mm, [model_a_vh(m) * 10 ** -0.14 for m in mm],
                    [model_a_vh(m) * 10 ** 0.14 for m in mm],
                    color="b", alpha=0.12, zorder=2, label="0.14 dex scatter")
    # dwarfs: observed (M*/L sweep as error bar) + model B upper limits
    for r in rows:
        lo = dwarf_row(*[d for d in DSPH if d[0] == r["name"]][0],
                       ml=ML_SWEEP[0])["v_h_obs_kms"]
        hi = dwarf_row(*[d for d in DSPH if d[0] == r["name"]][0],
                       ml=ML_SWEEP[-1])["v_h_obs_kms"]
        m_lo = r["M_star_Msun"] * ML_SWEEP[0] / ML_BASE
        m_hi = r["M_star_Msun"] * ML_SWEEP[-1] / ML_BASE
        ax.plot([m_lo, m_hi], [lo, hi], "-", color="crimson", lw=1.0,
                zorder=3)
        ax.plot(r["M_star_Msun"], r["v_h_obs_kms"], "D", color="crimson",
                ms=6, zorder=4)
        ax.annotate(r["name"], (r["M_star_Msun"], r["v_h_obs_kms"]),
                    textcoords="offset points", xytext=(5, 4), fontsize=7)
        ax.plot(r["M_star_Msun"], r["v_h_modelB_upper_kms"], "v",
                color="darkorange", ms=7, zorder=4)
    ax.plot([], [], "D", color="crimson", ms=6,
            label="classical dSphs, observed (Wolf)")
    ax.plot([], [], "v", color="darkorange", ms=7,
            label=r"model B upper limit ($v_h \propto R\,v_{\rm rot}$, "
                  r"$v_{\rm rot} \leq 3$ km/s)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$M_{\rm bar}$ [$M_\odot$]")
    ax.set_ylabel(r"$v_h$ [km/s]")
    ax.set_title("#147 DSPH-LEDGER: the halo amplitude reads mass, "
                 "not rotation")
    ax.legend(loc="upper left", fontsize=7.5)
    ax.set_ylim(1e-2, 4e2)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIGURE), exist_ok=True)
    fig.savefig(FIGURE, dpi=160)
    plt.close(fig)


def main(quick: bool = False) -> dict:
    rows = ledger()
    v = verdicts(rows)
    sw = sweep()
    b1_stable = all(s["B1"] == v["B1"] for s in sw)
    b3_stable = all(s["B3_n_below"] >= 6 for s in sw) if \
        v["B3_n_below_half_sigma"] >= 6 else \
        all(s["B3_n_below"] < 6 for s in sw)
    receipt = {
        "issue": 147,
        "hypothesis": "DSPH-LEDGER: mass law vs rotation law, budget, "
                      "universal core (rules B1-B3 of #147)",
        "pinned": {
            "data": "McConnachie 2012 compilation (8 classical MW dSphs)",
            "mass_law": [SLOPE_A, INTERCEPT_A],
            "h9_reference": {"M_MW": M_MW, "R_MW_kpc": R_MW_KPC,
                             "v_MW_kms": V_MW,
                             "Gamma_req_MW_m2_s": GAMMA_REQ_MW},
            "r_c_universal_kpc": R_C_UNIVERSAL_KPC,
            "ml_base": ML_BASE, "vrot_base_kms": VROT_BASE},
        "baseline_ledger": rows,
        "verdicts": v,
        "sweep": sw,
        "B1_sweep_stable": bool(b1_stable),
        "B3_sweep_stable": bool(b3_stable),
    }
    os.makedirs(os.path.dirname(RECEIPT), exist_ok=True)
    with open(RECEIPT, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)

    print(f"DSPH-LEDGER (#147)  --  receipt -> "
          f"{os.path.relpath(RECEIPT, REPO)}")
    print(f"  {'dwarf':<11} {'M*':>9} {'v_h obs':>8} {'model A':>8} "
          f"{'dA':>6} {'model B<=':>9} {'dB':>6} {'sig_pred':>8} "
          f"{'sig_obs':>7}")
    for r in rows:
        print(f"  {r['name']:<11} {r['M_star_Msun']:>9.2e} "
              f"{r['v_h_obs_kms']:>8.2f} {r['v_h_modelA_kms']:>8.2f} "
              f"{r['delta_A_dex']:>+6.2f} {r['v_h_modelB_upper_kms']:>9.4f} "
              f"{r['delta_B_dex']:>+6.2f} "
              f"{r['sigma_pred_universal_core_kms']:>8.2f} "
              f"{r['sigma_obs_kms']:>7.1f}")
    print(f"  B1: median dA = {v['median_delta_A_dex']:+.3f}, "
          f"median dB = {v['median_delta_B_dex']:+.3f}  ->  {v['B1']} "
          f"(sweep-stable: {b1_stable})")
    print(f"  B2: budget binds: {v['B2_budget_binds']} "
          f"(min ratio {v['B2_min_budget_ratio']:.2e}) -- the naive "
          f"'no rotation => no budget' killer does NOT bind"
          if not v["B2_budget_binds"] else
          f"  B2: budget BINDS (min ratio {v['B2_min_budget_ratio']:.2e})")
    print(f"  B3: {v['B3_n_below_half_sigma']}/8 below half sigma  ->  "
          f"{v['B3']} (sweep-stable: {b3_stable})")
    if not quick:
        make_figure(rows)
        print(f"  figure -> {os.path.relpath(FIGURE, REPO)}")
    return receipt


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="skip the figure")
    args = ap.parse_args()
    main(quick=args.quick)

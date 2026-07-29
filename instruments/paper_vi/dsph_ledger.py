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
v_rot in {1, 3, 10} km/s, +/-30% anisotropy systematic on v_c, and since #203
the MW normalisation radius in {4, 10, 15} kpc) are part of the
pre-registration: verdicts must be sweep-stable or are reported fragile.

B1 IS REPORTED FRAGILE.  The R_MW axis added in #203 makes 6 of the 81 sweep
points return "inconclusive" rather than "falsified".  All six sit at
v_rot = 10 km/s -- 3.3x above the <= 3 km/s observational upper limit the
sweep exists to stress -- and at the smallest, most model-B-favourable MW
radius.  Within v_rot <= 3 km/s the verdict holds at all 54 points with a
0.17 dex margin.  Both statements are in the receipt; the unqualified
B1_sweep_stable flag stays false.

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

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
H9_RECEIPT = os.path.join(REPO, "papers", "SSV-IV", "results",
                          "h9_triangle_receipt.json")


def _h9_reference():
    """The MW reference point, read from H9's receipt rather than retyped.

    Until #203 these were four hand-copied literals under a comment claiming
    all four came from ``h9_triangle_receipt.json``.  Only two did: `M_MW` and
    `GAMMA_REQ_MW`.  `V_MW` was 220 where H9 records a BTFR velocity of 189.02
    at this mass, and `R_MW_KPC` was 15 -- a radius H9 does not contain at all.
    Reading them makes that class of defect structurally impossible instead of
    merely fixed, and is rule 14's "a load-bearing number must not exist twice"
    applied across papers.
    """
    with open(H9_RECEIPT, encoding="utf-8") as fh:
        h9 = json.load(fh)
    return (h9["reference_point"]["M_b_Msun"],
            h9["reference_point"]["v_btfr_km_s"],
            h9["inversions"]["Gamma_required_with_grain_rho0_real_G_m2_s"])


M_MW, V_MW, GAMMA_REQ_MW = _h9_reference()   # M_sun, km/s, m^2/s

# The MW circulation radius is NOT in the H9 receipt -- 10 kpc is merely where
# H9 evaluates its required medium flow.  It is a convention either way, so it
# is declared as one and carried as a pre-registered sweep axis (#203) rather
# than asserted.  4 kpc is a half-light-like normalisation, comparable with the
# dwarfs' own r_1/2; 15 kpc is the outer disc.  Smaller R_MW favours model B.
R_MW_KPC = 10.0
R_MW_SWEEP = (4.0, 10.0, 15.0)

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

RECEIPT = os.path.join(REPO, "papers", "SSV-VI", "results",
                       "dsph_ledger_receipt.json")
FIGURE = os.path.join(REPO, "papers", "SSV-VI", "figures",
                      "fig_dsph_ledger.png")
SPARC_CSV = os.path.join(REPO, "papers", "SSV-VI", "results",
                         "sparc_per_galaxy_results.csv")

# Significant figures the receipt is written to.
#
# The receipt is a tracked artifact and the test suite rewrites it, so any
# instability shows up as git churn on every run.  Two consecutive runs on one
# machine are byte-identical -- the arithmetic is deterministic -- but results
# drift by up to ~4e-15 relative *across environments* (BLAS/CPU reduction
# order), which was enough to move 25 of the 259 floats and dirty the working
# tree on five separate occasions during the #198 work.
#
# Measured, not estimated (rounding is monotonic, so testing both ends of the
# drift interval against every value is exact):
#
#     s.f.   drift the receipt tolerates
#      6     1.9e-08   (4733785x observed)
#      8     7.7e-12   (   1931x observed)
#      9     4.9e-12   (   1222x observed)
#     10     3.7e-13   (     91x observed)
#     12     1.0e-14   (      3x observed)
#
# #203 is the worked example of why this number needs re-measuring rather than
# inheriting.  At 10 s.f. the margin was ~900x when the receipt held 259
# floats; adding the R_MW sweep axis tripled it to 618, and one sweep value
# landed 3.7e-13 from a rounding boundary -- margin down to 91x, and the guard
# fired.  The margin is a property of the *values*, not of the s.f. choice, so
# a receipt that grows erodes it.  (Note 8 s.f. beats 9 here for the same
# reason: it is where these particular numbers fall, not a trend.)
#
# 8 s.f. holds ~1900x while still leaving five orders of magnitude more
# precision than the ~3 s.f. of physics these numbers carry (km/s, dex).
# Guarded by test_receipt_is_stable_under_environment_drift.
RECEIPT_SIGFIGS = 8


def _stable(value):
    """Round floats to RECEIPT_SIGFIGS so the receipt is environment-stable.

    Recurses through the receipt structure.  ``bool`` is deliberately handled
    before ``float``/``int`` -- in Python ``isinstance(True, int)`` is True, and
    a verdict flag rewritten as ``1`` would be a silent content change.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, float):
        return float(f"{value:.{RECEIPT_SIGFIGS}g}")
    if isinstance(value, dict):
        return {k: _stable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_stable(v) for v in value]
    return value


def model_a_vh(mbar_msun: float) -> float:
    """#133 mass law, km/s."""
    return 10.0 ** (SLOPE_A * math.log10(mbar_msun) + INTERCEPT_A)


def model_b_vh(r_half_kpc: float, vrot_kms: float,
               r_mw_kpc: float = R_MW_KPC) -> float:
    """Rotation-proportional entrainment, normalized at the H9 MW
    reference: v_h = v_h_A(M_MW) * (R v_rot) / (R_MW v_MW).

    The radius is r_1/2, the same one the rest of the ledger uses; before #203
    this line alone used the projected R_e, so the dwarf's circulation was
    evaluated at a different radius from its dynamics (a factor 4/3).

    Linear in Gamma is derived, not chosen: model A gives v_h ~ M^0.256 and H9
    gives Gamma_req ~ M^0.25, hence v_h ~ Gamma^1.02.  See #203 section C --
    Gamma^{1/4} would put model B on top of model A and dissolve the test.
    """
    return model_a_vh(M_MW) * (r_half_kpc * vrot_kms) / (r_mw_kpc * V_MW)


def gamma_req(mbar_msun: float) -> float:
    """H9-inverted circulation requirement, m^2/s (Gamma ~ M^{1/4})."""
    return GAMMA_REQ_MW * (mbar_msun / M_MW) ** 0.25


def dwarf_row(name, lv6, sigma, re_pc, *, ml=ML_BASE, vrot=VROT_BASE,
              aniso=1.0, r_mw_kpc=R_MW_KPC):
    """All derived quantities for one dwarf at given sweep settings."""
    mstar = ml * lv6 * 1.0e6                  # M_sun (gas-free)
    r_half = (4.0 / 3.0) * re_pc              # 3D half-light radius, pc
    v_c = math.sqrt(3.0) * sigma * aniso      # Wolf, km/s
    v_bar_sq = G_PC * (mstar / 2.0) / r_half  # (km/s)^2
    v_h_obs = math.sqrt(max(v_c ** 2 - v_bar_sq, 0.0))
    v_h_a = model_a_vh(mstar)
    v_h_b = model_b_vh(r_half / 1.0e3, vrot, r_mw_kpc)
    # B3: universal-core prediction at r_1/2
    r_kpc = r_half / 1.0e3
    core_fac = r_kpc ** 2 / (r_kpc ** 2 + R_C_UNIVERSAL_KPC ** 2)
    sigma_pred = math.sqrt((v_bar_sq + v_h_a ** 2 * core_fac) / 3.0)
    # B2: circulation budget vs requirement (SI)
    # r_1/2, not R_e, for the same reason as model B above (#203).
    gamma_bar = 2.0 * math.pi * (r_half * PC_M) * (vrot * KM)
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


def ledger(*, ml=ML_BASE, vrot=VROT_BASE, aniso=1.0, r_mw_kpc=R_MW_KPC):
    return [dwarf_row(*d, ml=ml, vrot=vrot, aniso=aniso, r_mw_kpc=r_mw_kpc)
            for d in DSPH]


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
                for rmw in R_MW_SWEEP:
                    v = verdicts(ledger(ml=ml, vrot=vrot, aniso=an,
                                        r_mw_kpc=rmw))
                    out.append({"ml": ml, "vrot_kms": vrot, "aniso": an,
                                "r_mw_kpc": rmw,
                                "B1": v["B1"],
                                "median_delta_A_dex":
                                    v["median_delta_A_dex"],
                                "median_delta_B_dex":
                                    v["median_delta_B_dex"],
                                "B3_n_below": v["B3_n_below_half_sigma"]})
    return out


def b1_fragility_report(baseline_b1, sw):
    """Where B1 stops holding, and whether that region is observable.

    Added by #203 together with the R_MW sweep axis, which is what made B1
    fragile.  A bare ``B1_sweep_stable: false`` would record the fragility
    while hiding the one thing a reader needs -- that every disagreeing point
    sits at v_rot = 10 km/s, which is 3.3x ABOVE the <= 3 km/s observational
    upper limit the sweep exists to stress.  Reported, not softened: the
    unqualified flag stays false (rule 1).
    """
    bad = [s for s in sw if s["B1"] != baseline_b1]
    inside = [s for s in sw if s["vrot_kms"] <= VROT_BASE]
    bad_inside = [s for s in inside if s["B1"] != baseline_b1]
    return {
        "n_sweep_points": len(sw),
        "n_disagreeing": len(bad),
        "disagreeing_at": sorted({
            (s["vrot_kms"], s["r_mw_kpc"]) for s in bad}),
        "all_disagreement_above_vrot_limit":
            bool(bad) and all(s["vrot_kms"] > VROT_BASE for s in bad),
        "vrot_observational_limit_kms": VROT_BASE,
        "within_vrot_limit": {
            "n_points": len(inside),
            "n_disagreeing": len(bad_inside),
            "stable": not bad_inside,
            "min_median_delta_B_dex":
                min(s["median_delta_B_dex"] for s in inside),
            "margin_dex":
                min(s["median_delta_B_dex"] for s in inside) - 1.5},
    }


def summary() -> dict:
    """The paper's load-bearing numbers, computed without writing anything.

    ``gen_values.py`` (rule 14) calls these.  It must not go through ``main``:
    that writes the tracked receipt, so rendering the paper would mutate a
    result artifact.  Deliberately recomputes rather than reading the receipt,
    so ``gen_values --check`` can compare the two.
    """
    rows = ledger()
    v = verdicts(rows)
    f = b1_fragility_report(v["B1"], sweep())
    return {
        "median_delta_A_dex": v["median_delta_A_dex"],
        "median_delta_B_dex": v["median_delta_B_dex"],
        "shortfall_factor": 10.0 ** v["median_delta_B_dex"],
        "delta_A_min_dex": min(r["delta_A_dex"] for r in rows),
        "delta_A_max_dex": max(r["delta_A_dex"] for r in rows),
        "n_sweep_points": float(f["n_sweep_points"]),
        "n_sweep_disagreeing": float(f["n_disagreeing"]),
        "within_limit_margin_dex": f["within_vrot_limit"]["margin_dex"],
        "min_budget_ratio": v["B2_min_budget_ratio"],
        # The observational form of "why are the triangles at 10^-1?" (#203):
        # the rotation each dwarf would need for a law linear in Gamma to reach
        # its observed v_h.  Every value exceeds the Milky Way's own 220 km/s.
        "vrot_needed_min_kms": min(_vrot_needed(r) for r in rows),
        "vrot_needed_max_kms": max(_vrot_needed(r) for r in rows),
    }


def _vrot_needed(row) -> float:
    """v_rot at which model B would reproduce this dwarf's observed v_h."""
    return (row["v_h_obs_kms"] * (R_MW_KPC * V_MW)
            / (model_a_vh(M_MW) * row["r_half_pc"] / 1.0e3))


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
    b1_fragility = b1_fragility_report(v["B1"], sw)
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
            "h9_reference": {
                "read_from": "papers/SSV-IV/results/h9_triangle_receipt.json",
                "M_MW": M_MW, "v_MW_kms": V_MW,
                "Gamma_req_MW_m2_s": GAMMA_REQ_MW},
            "conventions": {
                "R_MW_kpc": R_MW_KPC,
                "R_MW_kpc_note": "not in the H9 receipt; convention, swept",
                "R_MW_sweep_kpc": list(R_MW_SWEEP),
                "model_b_radius": "r_1/2 (= 4/3 R_e), as elsewhere in the "
                                  "ledger",
                "model_b_exponent": "v_h ~ Gamma^1 (derived: model A "
                                    "M^0.256 with H9 Gamma_req M^0.25)"},
            "r_c_universal_kpc": R_C_UNIVERSAL_KPC,
            "ml_base": ML_BASE, "vrot_base_kms": VROT_BASE},
        "baseline_ledger": rows,
        "verdicts": v,
        "sweep": sw,
        "B1_sweep_stable": bool(b1_stable),
        "B1_fragility": b1_fragility,
        "B3_sweep_stable": bool(b3_stable),
    }
    os.makedirs(os.path.dirname(RECEIPT), exist_ok=True)
    with open(RECEIPT, "w", encoding="utf-8") as fh:
        json.dump(_stable(receipt), fh, indent=2)

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
    f = b1_fragility
    if not b1_stable:
        print(f"      FRAGILE: {f['n_disagreeing']}/{f['n_sweep_points']} "
              f"sweep points disagree, all at "
              f"{sorted({p[0] for p in f['disagreeing_at']})} km/s "
              f"(limit {f['vrot_observational_limit_kms']}) and R_MW "
              f"{sorted({p[1] for p in f['disagreeing_at']})} kpc")
        w = f["within_vrot_limit"]
        print(f"      within v_rot <= {f['vrot_observational_limit_kms']} "
              f"km/s: {w['n_disagreeing']}/{w['n_points']} disagree, "
              f"min median dB {w['min_median_delta_B_dex']:.3f} "
              f"(margin {w['margin_dex']:+.3f} dex)")
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

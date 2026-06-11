"""#133 -- SPARC multi-galaxy test of the SSV circulation halo.

Pre-registered in issue #133 (posted before computing). The SSV halo
(#119 H7a/H8: isothermal 1/r^2 circulation-energy density => Phi = v_h^2
ln r) adds a CONSTANT v_h^2 in quadrature to the baryonic curve, so on
SPARC the SSV model is

    v_model^2(r) = Vgas*|Vgas| + 0.5*Vdisk*|Vdisk| + 0.7*Vbul^2 + v_h^2

with the SPARC-standard mass-to-light ratios fixed: ONE free parameter
per galaxy (v_h >= 0), no core radius (the pure pre-registered form).

Comparison models on identical fixed baryons:
  - NFW halo, 2 params (V200, c);
  - MOND/RAR, 0 params (a0 = 1.2e-10 m/s^2, nu(y) = 1/(1 - e^-sqrt(y)));
  - Flynn & Cannaliato (arXiv:2601.00522) endpoint-anchored solid-body
    omega model (illustrative row, no decision rule).

Decision rules (a)-(c): see issue #133 / the result note.

Data: SPARC (Lelli, McGaugh & Schombert 2016, AJ 152, 157), files
papers/SSV-VI/data/SPARC/{SPARC,MassModels}_Lelli2016c.mrt -- the
official MRT files (author's direct download, 2026-06-11; verified
content-identical to the vendored copy the battery first ran on).

Run:  python instruments/paper_vi/sparc_halo_fit.py
Writes papers/SSV-VI/results/sparc_halo_fit_receipt.json and figures.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SPARC_DIR = ROOT / "papers" / "SSV-VI" / "data" / "SPARC"
RESULTS = ROOT / "papers" / "SSV-VI" / "results"
FIGURES = ROOT / "papers" / "SSV-VI" / "figures"

UPS_DISK = 0.5            # SPARC-standard M/L at [3.6], disc
UPS_BUL = 0.7             # SPARC-standard M/L at [3.6], bulge
KMS2_PER_KPC = 3.2408e-14  # 1 (km/s)^2/kpc in m/s^2
A0_SI = 1.2e-10            # MOND acceleration scale, m/s^2
A0 = A0_SI / KMS2_PER_KPC  # in (km/s)^2 / kpc  (~3702.8)
H0_KMS_KPC = 0.073         # 73 km/s/Mpc

# pre-registered sample cuts (issue #133)
MIN_POINTS = 10
MIN_INC = 30.0


# ----------------------------------------------------------------------
# SPARC MRT parsing (fixed-width per the byte-by-byte headers)
# ----------------------------------------------------------------------

def _data_lines(path: Path):
    """Yield data rows of an MRT file (everything after the last ---- rule)."""
    lines = path.read_text().splitlines()
    last_rule = max(i for i, l in enumerate(lines) if l.startswith("-----"))
    for line in lines[last_rule + 1:]:
        if line.strip():
            yield line


def parse_mass_models(path: Path) -> dict:
    """MassModels_Lelli2016c.mrt -> {galaxy: dict of arrays}.

    Token-based: SPARC identifiers and numeric fields contain no internal
    whitespace, and the vendored file's column spacing is shifted relative
    to its byte-by-byte header, so fixed-width slicing is unsafe.
    Columns: ID D R Vobs e_Vobs Vgas Vdisk Vbul SBdisk SBbul."""
    out: dict = {}
    for ln in _data_lines(path):
        f = ln.split()
        if len(f) != 10:
            raise ValueError(f"unexpected mass-model row: {ln!r}")
        out.setdefault(f[0], []).append([float(x) for x in f[2:8]])
    for gal, rows in out.items():
        a = np.array(rows)
        out[gal] = {"R": a[:, 0], "Vobs": a[:, 1], "eV": a[:, 2],
                    "Vgas": a[:, 3], "Vdisk": a[:, 4], "Vbul": a[:, 5]}
    return out


def parse_galaxy_table(path: Path) -> dict:
    """SPARC_Lelli2016c.mrt (Table 1) -> {galaxy: properties}.

    Token-based for the same reason as parse_mass_models. Columns:
    Galaxy T D e_D f_D Inc e_Inc L[3.6] e_L[3.6] Reff SBeff Rdisk SBdisk
    MHI RHI Vflat e_Vflat Q [Ref] -- the trailing reference field may be
    absent."""
    out = {}
    for ln in _data_lines(path):
        f = ln.split()
        if len(f) not in (18, 19):
            raise ValueError(f"unexpected galaxy-table row: {ln!r}")
        out[f[0]] = {
            "T": int(f[1]),
            "D": float(f[2]),
            "Inc": float(f[5]),
            "L36": float(f[7]),       # 1e9 Lsun
            "Rdisk": float(f[11]),
            "MHI": float(f[13]),      # 1e9 Msun
            "Vflat": float(f[15]),
            "Q": int(f[17]),
        }
    return out


# ----------------------------------------------------------------------
# models
# ----------------------------------------------------------------------

def v_bar_sq(g: dict, ups_d: float = UPS_DISK, ups_b: float = UPS_BUL):
    """Baryonic contribution in (km/s)^2; Vgas signed per SPARC convention."""
    return (g["Vgas"] * np.abs(g["Vgas"])
            + ups_d * g["Vdisk"] * np.abs(g["Vdisk"])
            + ups_b * g["Vbul"] ** 2)


def chi2(v_model, g):
    return float(np.sum(((g["Vobs"] - v_model) / g["eV"]) ** 2))


def fit_ssv(g: dict):
    """1-param SSV fit: v^2 = vbar^2 + vh^2. Returns (vh, lo, hi, chi2)."""
    vb2 = v_bar_sq(g)
    grid = np.linspace(0.0, 500.0, 2001)
    c2 = np.array([chi2(np.sqrt(np.clip(vb2 + vh * vh, 0.0, None)), g)
                   for vh in grid])
    i = int(np.argmin(c2))
    vh, cmin = grid[i], c2[i]
    inside = grid[c2 <= cmin + 1.0]          # Delta-chi2 = 1 interval
    return vh, float(inside.min()), float(inside.max()), cmin


def fit_ssv_cored(g: dict):
    """POST-HOC exploration (flagged in #133; NOT a pre-registered model):
    cored halo v_h^2 * r^2/(r^2 + r_c^2) -- the H7a/H8 1/r^2 energy
    density was measured OUTSIDE the defect core, so the pure form
    extrapolates beyond the measurement; this 2-param variant rolls the
    halo off below r_c. Identical to a pseudo-isothermal sphere."""
    from scipy.optimize import minimize
    vb2 = v_bar_sq(g)

    def f(p):
        vh, rc = p
        if not (0.0 <= vh <= 500.0 and 0.01 <= rc <= 50.0):
            return 1e12
        halo = vh * vh * g["R"] ** 2 / (g["R"] ** 2 + rc * rc)
        return chi2(np.sqrt(np.clip(vb2 + halo, 0.0, None)), g)

    best = None
    for vh0 in (30, 80, 150, 250):
        for rc0 in (0.5, 2.0, 8.0):
            r = minimize(f, [vh0, rc0], method="Nelder-Mead",
                         options={"xatol": 1e-3, "fatol": 1e-6,
                                  "maxiter": 2000})
            if best is None or r.fun < best.fun:
                best = r
    return float(best.x[0]), float(best.x[1]), float(best.fun)


def v_nfw_sq(r, v200, c):
    """NFW circular velocity^2 (km/s)^2 at r [kpc]."""
    r200 = v200 / (10.0 * H0_KMS_KPC)
    x = np.clip(r / r200, 1e-9, None)
    mu = np.log(1.0 + c * x) - c * x / (1.0 + c * x)
    mu_c = math.log(1.0 + c) - c / (1.0 + c)
    return v200 ** 2 * mu / (x * mu_c)


def fit_nfw(g: dict):
    """2-param NFW fit on fixed baryons. Coarse grid + Nelder-Mead refine."""
    from scipy.optimize import minimize
    vb2 = v_bar_sq(g)

    def f(p):
        v200, c = p
        if not (10.0 <= v200 <= 600.0 and 1.0 <= c <= 100.0):
            return 1e12
        return chi2(np.sqrt(np.clip(vb2 + v_nfw_sq(g["R"], v200, c),
                                    0.0, None)), g)

    best = None
    for v200 in (30, 60, 100, 150, 220, 320):
        for c in (3, 6, 10, 18, 30):
            r = minimize(f, [v200, c], method="Nelder-Mead",
                         options={"xatol": 1e-3, "fatol": 1e-6,
                                  "maxiter": 2000})
            if best is None or r.fun < best.fun:
                best = r
    return float(best.x[0]), float(best.x[1]), float(best.fun)


def v_mond(g: dict):
    """MOND/RAR prediction (0 params): g_obs = g_bar * nu(g_bar/a0)."""
    vb2 = v_bar_sq(g)
    gbar = np.clip(vb2, 1e-6, None) / g["R"]            # (km/s)^2/kpc
    y = gbar / A0
    nu = 1.0 / (1.0 - np.exp(-np.sqrt(y)))
    return np.sqrt(gbar * nu * g["R"])


def v_flynn(g: dict):
    """Flynn & Cannaliato endpoint-anchored model: Keplerian decline from
    the innermost point plus solid-body R*omega anchored at the outermost
    point (their eqs. 2, 5, 6). Illustrative only."""
    r1, v1 = g["R"][0], g["Vobs"][0]
    r2, v2 = g["R"][-1], g["Vobs"][-1]
    vk = v1 * np.sqrt(r1 / g["R"])
    omega = (v2 - v1 * math.sqrt(r1 / r2)) / r2
    return vk + omega * g["R"]


# ----------------------------------------------------------------------
# the pre-registered battery
# ----------------------------------------------------------------------

def select_sample(curves, table, q_max=1):
    sample = []
    for gal, g in curves.items():
        t = table.get(gal)
        if t is None:
            continue
        if (t["Q"] <= q_max and t["Inc"] >= MIN_INC
                and len(g["R"]) >= MIN_POINTS):
            sample.append(gal)
    return sorted(sample)


def run_galaxy(g: dict):
    n = len(g["R"])
    vh, vh_lo, vh_hi, c2_ssv = fit_ssv(g)
    v200, cnfw, c2_nfw = fit_nfw(g)
    vh_c, rc_c, c2_cored = fit_ssv_cored(g)
    c2_mond = chi2(v_mond(g), g)
    c2_fly = chi2(v_flynn(g), g)
    return {
        "N": n,
        "vh": vh, "vh_lo": vh_lo, "vh_hi": vh_hi,
        "chi2_ssv": c2_ssv, "chi2red_ssv": c2_ssv / max(n - 1, 1),
        "nfw_v200": v200, "nfw_c": cnfw,
        "chi2_nfw": c2_nfw, "chi2red_nfw": c2_nfw / max(n - 2, 1),
        "posthoc_cored_vh": vh_c, "posthoc_cored_rc": rc_c,
        "chi2red_cored": c2_cored / max(n - 2, 1),
        "bic_cored": c2_cored + 2 * math.log(n),
        "chi2_mond": c2_mond, "chi2red_mond": c2_mond / n,
        "chi2_flynn": c2_fly, "chi2red_flynn": c2_fly / n,
        "bic_ssv": c2_ssv + 1 * math.log(n),
        "bic_nfw": c2_nfw + 2 * math.log(n),
    }


def rule_a(res: dict):
    med_ssv = float(np.median([r["chi2red_ssv"] for r in res.values()]))
    med_nfw = float(np.median([r["chi2red_nfw"] for r in res.values()]))
    bic_wins = sum(1 for r in res.values() if r["bic_ssv"] <= r["bic_nfw"])
    return {
        "median_chi2red_ssv": med_ssv,
        "median_chi2red_nfw": med_nfw,
        "ratio": med_ssv / med_nfw if med_nfw > 0 else float("inf"),
        "threshold": 1.5,
        "bic_win_fraction": bic_wins / len(res),
        "verdict": "PASS" if med_ssv <= 1.5 * med_nfw else "FAIL",
    }


def rule_b(curves, res):
    """Median fractional residual of the SSV fits per quintile of r/Rmax."""
    fr, qb = [], []
    for gal, r in res.items():
        g = curves[gal]
        vmod = np.sqrt(np.clip(v_bar_sq(g) + r["vh"] ** 2, 0.0, None))
        fr.extend(((g["Vobs"] - vmod) / g["Vobs"]).tolist())
        qb.extend((g["R"] / g["R"].max()).tolist())
    fr, qb = np.array(fr), np.array(qb)
    med = []
    for k in range(5):
        m = (qb >= k * 0.2) & (qb < (k + 1) * 0.2 + (1e-9 if k == 4 else 0))
        med.append(float(np.median(fr[m])) if m.any() else float("nan"))
    ok = all(abs(x) < 0.05 for x in med if not math.isnan(x))
    return {"median_frac_residual_quintiles": med, "threshold": 0.05,
            "verdict": "PASS" if ok else "FAIL"}


def rule_c(table, res, rng_seed=42):
    """log vh = a log Mbar + b over vh-constrained galaxies; a = 0.25 +- 0.05."""
    xs, ys, gals = [], [], []
    for gal, r in res.items():
        if r["vh_lo"] <= 0.0:
            continue                       # vh consistent with zero
        t = table[gal]
        mbar = 1e9 * (UPS_DISK * t["L36"] + 1.33 * t["MHI"])
        if mbar <= 0:
            continue
        xs.append(math.log10(mbar))
        ys.append(math.log10(r["vh"]))
        gals.append(gal)
    xs, ys = np.array(xs), np.array(ys)
    a, b = np.polyfit(xs, ys, 1)
    rng = np.random.default_rng(rng_seed)
    boots = []
    for _ in range(2000):
        i = rng.integers(0, len(xs), len(xs))
        boots.append(np.polyfit(xs[i], ys[i], 1)[0])
    a_err = float(np.std(boots))
    scatter = float(np.std(ys - (a * xs + b)))
    return {"n_galaxies": len(xs), "slope": float(a), "slope_err": a_err,
            "intercept": float(b), "scatter_dex": scatter,
            "prediction": 0.25, "tolerance": 0.05,
            "verdict": "PASS" if abs(a - 0.25) <= 0.05 else "FAIL",
            "galaxies": gals}


def run(q_max=1):
    curves = parse_mass_models(SPARC_DIR / "MassModels_Lelli2016c.mrt")
    table = parse_galaxy_table(SPARC_DIR / "SPARC_Lelli2016c.mrt")
    sample = select_sample(curves, table, q_max=q_max)
    res = {gal: run_galaxy(curves[gal]) for gal in sample}
    out = {
        "issue": 133,
        "sample": {"q_max": q_max, "min_inc": MIN_INC,
                   "min_points": MIN_POINTS, "n_galaxies": len(sample),
                   "n_total_sparc": len(curves)},
        "fixed": {"ups_disk": UPS_DISK, "ups_bul": UPS_BUL,
                  "a0_m_s2": A0_SI},
        "rule_a_competitiveness": rule_a(res),
        "rule_b_residual_quintiles": rule_b(curves, res),
        "rule_c_vh_mbar_scaling": rule_c(table, res),
        "comparison_rows": {
            "median_chi2red_mond":
                float(np.median([r["chi2red_mond"] for r in res.values()])),
            "median_chi2red_flynn":
                float(np.median([r["chi2red_flynn"] for r in res.values()])),
        },
        "posthoc_cored_halo": {
            "flagged": "POST HOC -- not pre-registered; see issue #133",
            "median_chi2red":
                float(np.median([r["chi2red_cored"] for r in res.values()])),
            "bic_win_fraction_vs_nfw":
                sum(1 for r in res.values()
                    if r["bic_cored"] <= r["bic_nfw"]) / len(res),
            "median_rc_kpc":
                float(np.median([r["posthoc_cored_rc"]
                                 for r in res.values()])),
        },
        "per_galaxy": res,
    }
    return out, curves, table, sample


# ----------------------------------------------------------------------
# figures
# ----------------------------------------------------------------------

def make_figures(out, curves, table, sample):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    FIGURES.mkdir(parents=True, exist_ok=True)

    # --- montage: 12 galaxies spanning the luminosity range -------------
    lums = sorted(sample, key=lambda g: table[g]["L36"])
    picks = [lums[int(i * (len(lums) - 1) / 11)] for i in range(12)]
    fig, axes = plt.subplots(3, 4, figsize=(15, 10))
    for ax, gal in zip(axes.flat, picks):
        g = curves[gal]
        r = out["per_galaxy"][gal]
        vb2 = v_bar_sq(g)
        rr = np.linspace(g["R"].min(), g["R"].max(), 200)
        vb2_i = np.interp(rr, g["R"], vb2)
        ax.errorbar(g["R"], g["Vobs"], yerr=g["eV"], fmt="k.", ms=4,
                    lw=0.8, label="SPARC")
        ax.plot(rr, np.sqrt(np.clip(vb2_i, 0, None)), "g--", lw=1,
                label="baryons")
        ax.plot(rr, np.sqrt(np.clip(vb2_i + r["vh"] ** 2, 0, None)), "b-",
                lw=1.6, label=f"SSV $v_h$={r['vh']:.0f}")
        ax.plot(rr, np.sqrt(np.clip(
            vb2_i + v_nfw_sq(rr, r["nfw_v200"], r["nfw_c"]), 0, None)),
            "r:", lw=1.4, label="NFW")
        ax.set_title(f"{gal}  $\\chi^2_r$ SSV {r['chi2red_ssv']:.1f} / "
                     f"NFW {r['chi2red_nfw']:.1f}", fontsize=9)
        ax.set_xlabel("r [kpc]", fontsize=8)
        ax.set_ylabel("v [km/s]", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.legend(fontsize=6)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_sparc_montage.png", dpi=130)
    plt.close(fig)

    # --- vh vs Mbar ------------------------------------------------------
    rc = out["rule_c_vh_mbar_scaling"]
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    xs, ys = [], []
    for gal in rc["galaxies"]:
        t = table[gal]
        xs.append(1e9 * (UPS_DISK * t["L36"] + 1.33 * t["MHI"]))
        ys.append(out["per_galaxy"][gal]["vh"])
    xs, ys = np.array(xs), np.array(ys)
    ax.loglog(xs, ys, "ko", ms=4, alpha=0.7)
    xx = np.logspace(np.log10(xs.min()), np.log10(xs.max()), 50)
    ax.loglog(xx, 10 ** rc["intercept"] * xx ** rc["slope"], "b-",
              label=f"fit: slope {rc['slope']:.3f} ± {rc['slope_err']:.3f}")
    ax.loglog(xx, ys.mean() * (xx / np.median(xs)) ** 0.25, "r--",
              label="BTFR-equivalent slope 0.25")
    ax.set_xlabel(r"$M_{\rm bar}$ [$M_\odot$]")
    ax.set_ylabel(r"$v_h$ [km/s]")
    ax.set_title(f"SSV halo amplitude vs baryonic mass "
                 f"({rc['n_galaxies']} galaxies, {rc['verdict']})")
    ax.legend()
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_sparc_vh_mbar.png", dpi=130)
    plt.close(fig)

    # --- residual quintiles ----------------------------------------------
    rb = out["rule_b_residual_quintiles"]
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.bar(range(5), rb["median_frac_residual_quintiles"],
           tick_label=["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1"])
    ax.axhline(0.05, color="r", ls="--", lw=1)
    ax.axhline(-0.05, color="r", ls="--", lw=1)
    ax.set_xlabel(r"$r/R_{\rm max}$ quintile")
    ax.set_ylabel("median fractional residual")
    ax.set_title(f"SSV stacked residuals ({rb['verdict']})")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_sparc_residual_quintiles.png", dpi=130)
    plt.close(fig)


def main():
    out, curves, table, sample = run(q_max=1)
    out_q2, *_ = run(q_max=2)
    out["robustness_q_le_2"] = {
        "n_galaxies": out_q2["sample"]["n_galaxies"],
        "rule_a": out_q2["rule_a_competitiveness"],
        "rule_b": out_q2["rule_b_residual_quintiles"]["verdict"],
        "rule_c_slope": out_q2["rule_c_vh_mbar_scaling"]["slope"],
        "rule_c_verdict": out_q2["rule_c_vh_mbar_scaling"]["verdict"],
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    dest = RESULTS / "sparc_halo_fit_receipt.json"
    dest.write_text(json.dumps(out, indent=1))
    make_figures(out, curves, table, sample)

    ra = out["rule_a_competitiveness"]
    rb = out["rule_b_residual_quintiles"]
    rc = out["rule_c_vh_mbar_scaling"]
    print(f"sample: {out['sample']['n_galaxies']} galaxies "
          f"(Q=1, i>={MIN_INC}, N>={MIN_POINTS}) of "
          f"{out['sample']['n_total_sparc']}")
    print(f"rule (a) [{ra['verdict']}]: median chi2red SSV(1p) = "
          f"{ra['median_chi2red_ssv']:.2f} vs NFW(2p) = "
          f"{ra['median_chi2red_nfw']:.2f} (ratio {ra['ratio']:.2f}, "
          f"threshold 1.5); SSV BIC-wins {ra['bic_win_fraction']:.0%}")
    print(f"rule (b) [{rb['verdict']}]: quintile medians "
          + ", ".join(f"{x:+.3f}" for x in
                      rb["median_frac_residual_quintiles"]))
    print(f"rule (c) [{rc['verdict']}]: vh ~ Mbar^a, a = {rc['slope']:.3f}"
          f" ± {rc['slope_err']:.3f} (pred 0.25 ± 0.05), "
          f"{rc['n_galaxies']} galaxies, scatter {rc['scatter_dex']:.2f} dex")
    cm = out["comparison_rows"]
    print(f"comparison: median chi2red MOND/RAR(0p) = "
          f"{cm['median_chi2red_mond']:.2f}; Flynn omega = "
          f"{cm['median_chi2red_flynn']:.2f}")
    ph = out["posthoc_cored_halo"]
    print(f"post hoc (FLAGGED) cored halo (2p): median chi2red = "
          f"{ph['median_chi2red']:.2f}; BIC-wins vs NFW "
          f"{ph['bic_win_fraction_vs_nfw']:.0%}; median r_c = "
          f"{ph['median_rc_kpc']:.1f} kpc")
    rq = out["robustness_q_le_2"]
    print(f"robustness Q<=2 ({rq['n_galaxies']} gals): rule a "
          f"{rq['rule_a']['verdict']} (ratio {rq['rule_a']['ratio']:.2f}), "
          f"rule b {rq['rule_b']}, rule c slope {rq['rule_c_slope']:.3f} "
          f"({rq['rule_c_verdict']})")
    print(f"receipt -> {dest}")


if __name__ == "__main__":
    main()

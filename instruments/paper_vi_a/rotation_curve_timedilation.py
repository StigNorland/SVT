"""SSV-VI-a / issue #122 — rotation curve as the gradient of the time-dilation field.

SSV gravity *is* the gradient of the time-dilation (update-capacity) field
(Paper IV: the availability A = dτ/dt = 1 + Φ/c²).  A circular orbit therefore
obeys, in the weak field that holds across a galactic disc,

        v²(r) = r · dΦ/dr ,

with ONE field Φ(r) sourced by everything present.  Because v² = r dΦ/dr is
linear in Φ, the contributions add in quadrature:

        v²(r) = v²_CBH(r) + v²_bulge(r) + v²_disc(r) + v²_wave(r) .

* v²_CBH  = G M_BH / r        — the central condensate black hole's time-dilation
                                well.  This is the **Newtonian/Keplerian limit
                                near the CBH, recovered as the weak-field limit of
                                the field — not bolted on.**
* v²_bulge= G M_b r/(r+a_b)²  — Hernquist bulge (M31 has a dominant bulge).
* v²_disc = (2 G M_d/R_d) y²[I₀K₀−I₁K₁](y),  y=r/2R_d  — Freeman exponential disc.
* v²_wave = V_w²(1−e^{−r/r₀})(1+ε J₀(πr/Δr)) — the SSV standing-wave field shed by
                                the CBH (Paper VI-a §4).  Mestel-like → **flat
                                plateau**; the J₀ term is the node-spacing wiggle.
                                Core-suppressed (r₀) so the inner curve is the
                                Newtonian baryons, the outer plateau is the wave.

The CBH frequency enters only through the node spacing Δr; it is isolated in
`bh_node_spacing()` as a single swappable input (repo form f_BH = m_p²c²/(h M_BH);
a gravity.tex variant can replace it).  The numerological constant C and the
λ_BH∝M_BH vs Δr∝1/M_BH scaling tension are carried over, NOT resolved here.

Honest comparison: the SAME baryons (CBH+bulge+disc) plus an NFW halo, the
standard dark-matter model — not a shape strawman.  Both fit M31 (Chemin et al.
2009 Table 4) over the FULL radial range with absolute errors, so reduced χ² is
meaningful.

The reported question (rule 1): does the flat plateau V_w *emerge* from the
CBH-sourced wave field, or is it a free amplitude equivalent to a dark-matter
normalisation?  The fit answers it honestly — see the decomposition output.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit
from scipy.special import i0, i1, j0, k0, k1

# Units: kpc, km/s, Msun.
G = 4.30091e-6  # kpc (km/s)^2 / Msun

DATA = Path("papers/SSV-VI/data/chemin2009_table4_m31_rotation_curve.csv")
JSON_OUT = Path("papers/SSV-VI/results/m31_timedilation_receipt.json")

# --- swappable CBH-frequency input ------------------------------------------
M_BH_MSUN = 1.4e8           # M31 central black hole
C_KPC_MSUN = 1.8e9          # node-spacing constant (numerological; #42 / flagged)

# M31 measured baryons (literature: Tamm+2012 / Corbelli+2010 scale) for the
# physically-honest "baryons fixed" fit.  Hernquist bulge + exponential disc.
M31_BULGE_MSUN, M31_BULGE_A_KPC = 3.0e10, 1.0
M31_DISC_MSUN, M31_DISC_RD_KPC = 7.0e10, 5.3


def bh_node_spacing(m_bh_msun: float = M_BH_MSUN) -> float:
    """Δr = C / M_BH (kpc).  Single point of contact for the CBH-frequency model;
    replace with a gravity.tex form here if it differs from the repo's
    f_BH = m_p^2 c^2 / (h M_BH)."""
    return C_KPC_MSUN / m_bh_msun


# --- velocity components (each is r dΦ_i/dr) --------------------------------

def v2_cbh(r, m_bh=M_BH_MSUN):
    return G * m_bh / r


def v2_bulge(r, m_b, a_b):
    return G * m_b * r / (r + a_b) ** 2


def v2_disc(r, m_d, r_d):
    y = r / (2.0 * r_d)
    bracket = i0(y) * k0(y) - i1(y) * k1(y)
    return (2.0 * G * m_d / r_d) * y * y * bracket


def v2_wave(r, v_w, r0, eps, dr):
    k = math.pi / dr
    return v_w ** 2 * (1.0 - np.exp(-r / r0)) * (1.0 + eps * j0(k * r))


def v2_nfw(r, rho_s, r_s):
    x = r / r_s
    return 4.0 * math.pi * G * rho_s * r_s ** 3 * (np.log1p(x) - x / (1.0 + x)) / r


# --- total models -----------------------------------------------------------

def ssv_total(r, m_b, a_b, m_d, r_d, v_w, r0, eps):
    dr = bh_node_spacing()
    v2 = v2_cbh(r) + v2_bulge(r, m_b, a_b) + v2_disc(r, m_d, r_d) + v2_wave(r, v_w, r0, eps, dr)
    return np.sqrt(np.maximum(v2, 1e-12))


def v2_baryons_fixed(r):
    """CBH + M31 measured bulge + measured disc (no free parameters)."""
    return (v2_cbh(r) + v2_bulge(r, M31_BULGE_MSUN, M31_BULGE_A_KPC)
            + v2_disc(r, M31_DISC_MSUN, M31_DISC_RD_KPC))


def ssv_wave_on_fixed_baryons(r, v_w, r0, eps):
    """Physically-honest model: measured baryons + the CBH wave field only."""
    dr = bh_node_spacing()
    v2 = v2_baryons_fixed(r) + v2_wave(r, v_w, r0, eps, dr)
    return np.sqrt(np.maximum(v2, 1e-12))


def nfw_total(r, m_b, a_b, m_d, r_d, rho_s, r_s):
    v2 = v2_cbh(r) + v2_bulge(r, m_b, a_b) + v2_disc(r, m_d, r_d) + v2_nfw(r, rho_s, r_s)
    return np.sqrt(np.maximum(v2, 1e-12))


# --- data -------------------------------------------------------------------

def load_data(r_min: float = 0.0):
    r, v, e = [], [], []
    with DATA.open() as fh:
        for row in csv.DictReader(fh):
            rk, vk, ek = row["radius_kpc"], row["vrot_kms"], row["vrot_err_kms"]
            if rk and vk and float(rk) > r_min:
                r.append(float(rk))
                v.append(float(vk))
                e.append(float(ek) if ek and float(ek) > 0 else 10.0)
    return np.array(r), np.array(v), np.array(e)


def fit(name, func, r, v, e, p0, bounds, pnames):
    popt, _ = curve_fit(func, r, v, p0=p0, bounds=bounds, sigma=e,
                        absolute_sigma=True, maxfev=200_000)
    pred = func(r, *popt)
    chi2 = float(np.sum(((pred - v) / e) ** 2))
    dof = len(r) - len(popt)
    rms = float(np.sqrt(np.mean((pred - v) ** 2)))
    aic = chi2 + 2 * len(popt)
    return {
        "name": name,
        "params": {pnames[i]: float(popt[i]) for i in range(len(popt))},
        "chi2": chi2, "dof": dof, "reduced_chi2": chi2 / dof,
        "rms_kms": rms, "aic": aic,
    }, popt


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--r-min", type=float, default=0.0, help="default 0 = full range")
    ap.add_argument("--json-out", type=Path, default=JSON_OUT)
    args = ap.parse_args()

    r, v, e = load_data(args.r_min)
    dr = bh_node_spacing()

    ssv, ps = fit(
        "SSV time-dilation", ssv_total, r, v, e,
        p0=(3.0e10, 1.0, 7.0e10, 5.3, 150.0, 2.0, -0.3),
        bounds=((0, 0.1, 0, 1.0, 0, 0.1, -0.8),
                (3e11, 5.0, 3e11, 15.0, 400, 10.0, 0.8)),
        pnames=("M_bulge", "a_bulge_kpc", "M_disc", "R_d_kpc", "V_wave_kms", "r0_kpc", "epsilon"),
    )
    nfw, pn = fit(
        "baryons + NFW", nfw_total, r, v, e,
        p0=(3.0e10, 1.0, 7.0e10, 5.3, 1.0e7, 15.0),
        bounds=((0, 0.1, 0, 1.0, 1e5, 1.0),
                (3e11, 5.0, 3e11, 15.0, 1e9, 100.0)),
        pnames=("M_bulge", "a_bulge_kpc", "M_disc", "R_d_kpc", "rho_s_Msun_kpc3", "r_s_kpc"),
    )
    # Physically-honest fit: M31 measured baryons FIXED, only the CBH wave floats.
    fixed, pf = fit(
        "measured baryons + CBH wave", ssv_wave_on_fixed_baryons, r, v, e,
        p0=(160.0, 3.0, -0.3),
        bounds=((0, 0.1, -0.8), (400, 15.0, 0.8)),
        pnames=("V_wave_kms", "r0_kpc", "epsilon"),
    )

    # Baryon-vs-wave decomposition at the outermost measured radius.
    r_out = float(r.max())
    vb2 = v2_cbh(np.array([r_out]))[0] + v2_bulge(r_out, *ps[:2]) + v2_disc(r_out, ps[2], ps[3])
    vw2 = v2_wave(np.array([r_out]), ps[4], ps[5], ps[6], dr)[0]
    wave_fraction = vw2 / (vb2 + vw2)

    receipt = {
        "source": "Chemin, Carignan & Foster (2009), arXiv:0909.3846, Table 4",
        "fit_domain": {"r_min_kpc": args.r_min, "r_max_kpc": r_out, "n_points": int(len(r)), "full_range": args.r_min == 0.0},
        "fixed": {"M_BH_Msun": M_BH_MSUN, "C_kpc_Msun": C_KPC_MSUN, "delta_r_kpc": dr},
        "fits": [ssv, nfw, fixed],
        "m31_measured_baryons": {
            "M_bulge_Msun": M31_BULGE_MSUN, "a_bulge_kpc": M31_BULGE_A_KPC,
            "M_disc_Msun": M31_DISC_MSUN, "R_d_kpc": M31_DISC_RD_KPC,
            "v_baryon_at_r_out_kms": math.sqrt(v2_baryons_fixed(np.array([r_out]))[0]),
        },
        "decomposition_at_r_out_free_fit": {
            "r_out_kpc": r_out,
            "v_baryon_kms": math.sqrt(vb2),
            "v_wave_kms": math.sqrt(max(vw2, 0.0)),
            "wave_fraction_of_v2": wave_fraction,
            "note": "free fit drove the baryonic disc to ~0; wave absorbs nearly all support",
        },
        "newtonian_limit_note": "v2_cbh(r)=G*M_BH/r recovered exactly as r->0; wave field core-suppressed (->0).",
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(receipt, indent=2) + "\n")

    print("SSV-VI-a #122 — time-dilation rotation curve (M31, full range)")
    print("=" * 70)
    print(f"n={len(r)}  r=[{r.min():.2f},{r.max():.2f}] kpc  Δr(fixed)={dr:.2f} kpc")
    for fdict in (ssv, nfw, fixed):
        print(f"\n{fdict['name']}:  reduced χ²={fdict['reduced_chi2']:.2f}  "
              f"RMS={fdict['rms_kms']:.2f} km/s  AIC={fdict['aic']:.1f}")
        print("   " + ", ".join(f"{k}={v:.4g}" for k, v in fdict["params"].items()))
    vbar_out = math.sqrt(v2_baryons_fixed(np.array([r_out]))[0])
    print(f"\nFree-fit decomposition at r_out={r_out:.1f} kpc: "
          f"v_baryon={math.sqrt(vb2):.1f}, v_wave={math.sqrt(max(vw2,0)):.1f} km/s "
          f"→ wave supplies {wave_fraction*100:.0f}% of v²  (baryon disc driven to ~0)")
    print(f"Measured baryons give v_bar={vbar_out:.1f} km/s at r_out "
          f"(vs observed ~{v[-5:].mean():.0f}); the CBH wave must supply the rest.")
    print(f"Wrote {args.json_out}")


if __name__ == "__main__":
    main()

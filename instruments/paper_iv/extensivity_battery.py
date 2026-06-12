"""#149 H-EXT -- does the medium's static response read total energy, or
circulation?  (composite-body extensivity battery)

#129 item 2.  S1 (analytic, in the pre-registration): stationary
Madelung/Bernoulli for the LogSE gives b drho/rho0 = -v^2/2 + localized
quantum-pressure terms, so the far field reads the LOCAL velocity field
only -- a circulation multipole ladder:

    net winding W            : v ~ W/r      =>  drho ~ -W^2/(2b r^2)
    net-zero, dipole p != 0  : v ~ p/r^2    =>  drho ~ -p^2/(2b r^4)
    net-zero, dipole-zero    : v ~ q/r^3    =>  drho ~ -q^2/(2b r^6)

Total energy never appears as a far-field source.  S2 (this script)
tests the alternative the live architecture needs -- an energy-sourced
monopole drho ~ E_tot/r^2 for matter-like (net-zero) composites:

  E0   empty box: numerical floor.
  E1   positive control: single ell=1 in the D=30 checkerboard screen
       (H8b replication; drho r^2 -> -1/(2b) within 15% or the run is
       invalid).
  E2   THE composite: compact checkerboard quadrupole (net winding 0,
       dipole 0, spacing 8), stationary by symmetry.  Far-tail slope +
       amplitude vs the 5%-of-E1 monopole bound.
  E2b  moving composite: v-av dipole pair (d=8), profile about the pair
       centroid (expected slope ~4 -- the middle rung of the ladder).
  E3   N-scaling: two well-separated E2 clusters vs one (an
       energy-sourced monopole would double the far amplitude).
  E4   energy ledger (report-only): per-core aperture energies, cluster
       vs control.

Machinery: the validated H7a/H8 pattern from bath_driven_interaction
(imaginary-time relaxation preconditioner, split-step LogSE, absorber,
final-snapshot + time-averaged profiles; validity window t <= 40).
Decision rules live in issue #149 and are evaluated verbatim.

Run:  python instruments/paper_iv/extensivity_battery.py [--quick]
Writes papers/SSV-IV/results/extensivity_receipt.json and (full mode)
papers/SSV-IV/figures/fig_extensivity_ladder.png.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time as _time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bath_driven_interaction import (  # noqa: E402
    make_grid, absorber, xp, _to, _host, backend_name)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RECEIPT = os.path.join(REPO, "papers", "SSV-IV", "results",
                       "extensivity_receipt.json")
FIGURE = os.path.join(REPO, "papers", "SSV-IV", "figures",
                      "fig_extensivity_ladder.png")

B = 1.0


# --------------------------------------------------------------------------
def relax_evolve(charges, *, N=320, L=140.0, b=B, dt=0.02, relax_tau=8.0,
                 t_total=40.0, t_avg=15.0, floor=1e-6):
    """Imprint vortices, imaginary-time relax (H7a-redo preconditioner),
    evolve undriven, return 2D time-averaged density, AC variance, final
    density and energy density, and the grid -- the run_vortex pattern,
    kept 2D so profiles can be taken about arbitrary centers."""
    dx, X, Y, K2 = make_grid(N, L)
    Gamma = absorber(X, Y, L, width=20.0, gmax=1.2)
    xi = 1.0 / math.sqrt(2.0 * b)

    psi0 = np.ones((N, N), dtype=complex)
    for (xs, ys, ell) in charges:
        rr = np.sqrt((X - xs) ** 2 + (Y - ys) ** 2)
        th = np.arctan2(Y - ys, X - xs)
        psi0 *= (np.tanh(rr / xi) ** abs(ell)) * np.exp(1j * ell * th)

    KX = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    KXg, KYg = np.meshgrid(KX, KX, indexing="ij")

    psi = _to(psi0)
    decay = _to(np.exp(-Gamma * dt))
    expK_half = _to(np.exp(-1j * K2 / 2.0 * (dt / 2.0)))
    iKX = _to(1j * KXg)
    iKY = _to(1j * KYg)

    if relax_tau > 0.0:
        dtau = 0.02
        relK_half = _to(np.exp(-K2 / 2.0 * (dtau / 2.0)))
        for _ in range(int(round(relax_tau / dtau))):
            psi = xp.fft.ifft2(relK_half * xp.fft.fft2(psi))
            rho = xp.abs(psi) ** 2
            psi = psi * xp.exp(-(b * xp.log(xp.maximum(rho, floor))) * dtau)
            psi = xp.fft.ifft2(relK_half * xp.fft.fft2(psi))

    # the relaxed state IS the static configuration -- the static-response
    # profiles are measured here, before real-time evolution adds sound
    # (the real-time run below is the stability cross-check)
    rho_rel = _host(xp.abs(psi) ** 2)

    nsteps = int(round(t_total / dt))
    n_avg_start = int(round((t_total - t_avg) / dt))
    rho_acc = xp.zeros((N, N))
    rho2_acc = xp.zeros((N, N))
    acc = 0
    for n in range(nsteps):
        psi = xp.fft.ifft2(expK_half * xp.fft.fft2(psi))
        rho = xp.abs(psi) ** 2
        psi = psi * xp.exp(-1j * (b * xp.log(xp.maximum(rho, floor))) * dt)
        psi = 1.0 + (psi - 1.0) * decay
        psi = xp.fft.ifft2(expK_half * xp.fft.fft2(psi))
        if n >= n_avg_start:
            rho = xp.abs(psi) ** 2
            rho_acc += rho
            rho2_acc += rho * rho
            acc += 1
    mean_rho = _host(rho_acc) / acc
    var_rho = _host(rho2_acc) / acc - mean_rho ** 2

    rho_f = xp.abs(psi) ** 2
    ft = xp.fft.fft2(psi)
    gx = xp.fft.ifft2(iKX * ft)
    gy = xp.fft.ifft2(iKY * ft)
    rs = xp.maximum(rho_f, floor)
    e_f = _host(0.5 * (xp.abs(gx) ** 2 + xp.abs(gy) ** 2)
                + b * (rs * xp.log(rs) - rs + 1.0))
    return {"mean_rho": mean_rho, "var_rho": var_rho, "rho_rel": rho_rel,
            "rho_f": _host(rho_f), "e_f": e_f, "X": X, "Y": Y, "dx": dx}


def find_cores(rho, X, Y, n_cores, r_search=30.0, min_sep=3.0):
    """The n_cores deepest density minima within r_search of the box
    center, mutually separated by at least min_sep."""
    R = np.sqrt(X * X + Y * Y)
    work = np.where(R < r_search, rho, np.inf)
    cores = []
    for _ in range(n_cores):
        idx = np.unravel_index(np.argmin(work), work.shape)
        xc, yc = float(X[idx]), float(Y[idx])
        cores.append((xc, yc))
        mask = (X - xc) ** 2 + (Y - yc) ** 2 < min_sep ** 2
        work = np.where(mask, np.inf, work)
    return cores


def radial_profile(field, X, Y, center, r_edges):
    """Azimuthally averaged radial profile about an arbitrary center."""
    R = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)
    rc = 0.5 * (r_edges[:-1] + r_edges[1:])
    prof = np.empty(len(rc))
    for i in range(len(rc)):
        m = (R >= r_edges[i]) & (R < r_edges[i + 1])
        prof[i] = field[m].mean() if m.any() else np.nan
    return rc, prof


def fit_logslope(rc, absvals, valid):
    """Slope s of |drho| ~ r^{-s} over the valid bins (>= 4 required)."""
    rc = np.asarray(rc)[valid]
    av = np.asarray(absvals)[valid]
    if len(rc) < 4:
        return None, int(len(rc))
    s = -np.polyfit(np.log(rc), np.log(av), 1)[0]
    return float(s), int(len(rc))


def aperture_energy(e_f, X, Y, center, r_ap):
    R2 = (X - center[0]) ** 2 + (Y - center[1]) ** 2
    dx = X[1, 0] - X[0, 0]
    return float(e_f[R2 < r_ap ** 2].sum() * dx * dx)


# --------------------------------------------------------------------------
def run_battery(quick=False):
    if quick:
        # live region |x| < L/2 - 20 = 22: screens and windows must sit
        # well inside it (H7a lesson: the absorber destroys winding)
        box = dict(N=192, L=84.0, relax_tau=4.0, t_total=20.0, t_avg=8.0)
        d_screen, d_quad, sep3 = 12.0, 6.0, 0.0   # no E3 in quick mode
        e1_win = (2.0, 3.5)        # xi << r << D/4
        e2_slope_win, e2_amp_win = (9.0, 20.0), (16.0, 21.0)
        e2b_slope_win = (9.0, 18.0)
    else:
        box = dict(N=320, L=140.0, relax_tau=8.0, t_total=40.0, t_avg=15.0)
        d_screen, d_quad, sep3 = 30.0, 8.0, 25.0
        # DEVIATION (recorded): the pre-registered window (5, 12) reaches
        # into the screen-cancellation zone (partners at D cancel the
        # test vortex's velocity beyond r ~ D/4); the asymptotic
        # single-vortex window is xi << r << D/4.
        e1_win = (3.0, 7.0)
        e2_slope_win, e2_amp_win = (12.0, 40.0), (36.0, 44.0)
        e2b_slope_win = (12.0, 36.0)

    out = {}
    t0 = _time.time()

    # ---- E0: floor --------------------------------------------------------
    r_edges = np.arange(1.0, box["L"] / 2.0 - 20.0, 1.0)
    e0 = relax_evolve([], **box)
    rc, prof0 = radial_profile(np.abs(e0["rho_rel"] - 1.0),
                               e0["X"], e0["Y"], (0.0, 0.0), r_edges)
    prof0_ev = radial_profile(np.abs(e0["mean_rho"] - 1.0),
                              e0["X"], e0["Y"], (0.0, 0.0), r_edges)[1]
    out["E0"] = {"floor_relaxed_max": float(np.nanmax(prof0)),
                 "floor_evolved_max": float(np.nanmax(prof0_ev)),
                 "elapsed_s": round(_time.time() - t0, 1)}
    floor_prof = np.maximum(prof0, 1e-10)

    # ---- E1: positive control (H8b replication) ---------------------------
    # Rule source: the RELAXED state (static configuration, no drift, no
    # sound); the evolved final snapshot is the stability cross-check.
    t0 = _time.time()
    D = d_screen
    e1 = relax_evolve([(0.0, 0.0, 1), (D, 0.0, -1), (D, D, 1), (0.0, D, -1)],
                      **box)
    rc1, dr1 = radial_profile(e1["rho_rel"] - 1.0, e1["X"], e1["Y"],
                              (0.0, 0.0), r_edges)
    w = (rc1 >= e1_win[0]) & (rc1 <= e1_win[1])
    plateau = float(np.nanmean(dr1[w] * rc1[w] ** 2))
    core = find_cores(e1["rho_f"], e1["X"], e1["Y"], 1,
                      r_search=D / 2.0)[0]
    dr1_ev = radial_profile(e1["rho_f"] - 1.0, e1["X"], e1["Y"],
                            core, r_edges)[1]
    wev = (rc1 >= e1_win[0]) & (rc1 <= e1_win[1])
    plateau_ev = float(np.nanmean(dr1_ev[wev] * rc1[wev] ** 2))
    out["E1"] = {"drho_r2_plateau_relaxed": plateau,
                 "drho_r2_plateau_evolved_snapshot": plateau_ev,
                 "evolved_core_xy": [round(core[0], 2), round(core[1], 2)],
                 "expected": -1.0 / (2.0 * B),
                 "rel_dev": abs(plateau / (-1.0 / (2.0 * B)) - 1.0),
                 "rel_dev_evolved":
                     abs(plateau_ev / (-1.0 / (2.0 * B)) - 1.0),
                 "window": list(e1_win),
                 "elapsed_s": round(_time.time() - t0, 1)}

    # ---- E2: the stationary net-zero quadrupole composite -----------------
    t0 = _time.time()
    h = d_quad / 2.0
    quad = [(-h, -h, 1), (h, -h, -1), (h, h, 1), (-h, h, -1)]
    e2 = relax_evolve(quad, **box)
    rc2, dr2 = radial_profile(e2["rho_rel"] - 1.0, e2["X"], e2["Y"],
                              (0.0, 0.0), r_edges)
    dr2_ev = radial_profile(e2["mean_rho"] - 1.0, e2["X"], e2["Y"],
                            (0.0, 0.0), r_edges)[1]
    a2 = np.abs(dr2)
    win = (rc2 >= e2_slope_win[0]) & (rc2 <= e2_slope_win[1])
    valid = win & (a2 > 3.0 * floor_prof)
    s2, nbins2 = fit_logslope(rc2, a2, valid)
    wamp = (rc2 >= e2_amp_win[0]) & (rc2 <= e2_amp_win[1])
    amp2 = float(np.nanmean(dr2[wamp] * rc2[wamp] ** 2))
    # last bin where the relaxed-state signal still exceeds 3x floor:
    # the deepest radius at which a monopole coefficient is bounded
    above = np.where(valid)[0]
    if len(above):
        i_last = int(above[-1])
        bound_r = float(rc2[i_last])
        bound_coeff = float(a2[i_last] * rc2[i_last] ** 2)
    else:
        bound_r, bound_coeff = None, None
    out["E2"] = {"slope": s2, "n_valid_bins": nbins2,
                 "drho_r2_far": amp2,
                 "ratio_to_E1_plateau": abs(amp2 / plateau),
                 "drho_r2_far_evolved": float(np.nanmean(
                     dr2_ev[wamp] * rc2[wamp] ** 2)),
                 "monopole_bound_r": bound_r,
                 "monopole_bound_coeff": bound_coeff,
                 "monopole_bound_ratio_to_E1":
                     (abs(bound_coeff / plateau)
                      if bound_coeff is not None else None),
                 "slope_window": list(e2_slope_win),
                 "amp_window": list(e2_amp_win),
                 "elapsed_s": round(_time.time() - t0, 1)}

    # ---- E2b: the moving dipole composite ----------------------------------
    t0 = _time.time()
    pair = [(-h, 0.0, 1), (h, 0.0, -1)]
    e2b = relax_evolve(pair, **box)
    cores = find_cores(e2b["rho_f"], e2b["X"], e2b["Y"], 2, r_search=25.0)
    cen = (0.5 * (cores[0][0] + cores[1][0]),
           0.5 * (cores[0][1] + cores[1][1]))
    d_eff = math.dist(cores[0], cores[1])
    rcb, drb = radial_profile(e2b["rho_f"] - 1.0, e2b["X"], e2b["Y"],
                              cen, r_edges)
    soundb = radial_profile(np.sqrt(np.maximum(e2b["var_rho"], 0.0)),
                            e2b["X"], e2b["Y"], cen, r_edges)[1]
    ab = np.abs(drb)
    winb = (rcb >= e2b_slope_win[0]) & (rcb <= e2b_slope_win[1])
    # the moving pair is measured on a snapshot: gate bins on the local
    # sound RMS, not the (machine-clean) empty-box floor
    validb = winb & (ab > 1.5 * np.nan_to_num(soundb)) \
        & (ab > 3.0 * floor_prof)
    s2b, nbins2b = fit_logslope(rcb, ab, validb)
    # the relaxed (static) dipole profile gives the clean middle rung:
    # the pair sits at its imprint position, no translation, no sound
    rcr, drr = radial_profile(e2b["rho_rel"] - 1.0, e2b["X"], e2b["Y"],
                              (0.0, 0.0), r_edges)
    ar = np.abs(drr)
    # asymptotic dipole regime r >~ 2.5 d
    winr = (rcr >= 2.5 * d_quad) & (rcr <= e2b_slope_win[1])
    validr = winr & (ar > 3.0 * floor_prof)
    s2br, nbins2br = fit_logslope(rcr, ar, validr)
    out["E2b"] = {"cores": [[round(c[0], 2), round(c[1], 2)]
                            for c in cores],
                  "d_eff": round(d_eff, 2),
                  "centroid": [round(cen[0], 2), round(cen[1], 2)],
                  "slope_evolved_snapshot": s2b,
                  "n_valid_bins_evolved": nbins2b,
                  "slope_relaxed": s2br,
                  "n_valid_bins_relaxed": nbins2br,
                  "slope_window": list(e2b_slope_win),
                  "elapsed_s": round(_time.time() - t0, 1)}

    # ---- E3: N-scaling (full mode only) ------------------------------------
    if sep3 > 0:
        t0 = _time.time()
        two = ([(x - sep3, y, l) for (x, y, l) in quad]
               + [(x + sep3, y, l) for (x, y, l) in quad])
        e3 = relax_evolve(two, **box)
        rc3, dr3 = radial_profile(e3["rho_rel"] - 1.0, e3["X"], e3["Y"],
                                  (0.0, 0.0), r_edges)
        wamp3 = (rc3 >= e2_amp_win[0]) & (rc3 <= e2_amp_win[1])
        amp3 = float(np.nanmean(dr3[wamp3] * rc3[wamp3] ** 2))
        # the N-scaling comparison at the deepest bounded radius too
        amp3_b = (float(np.abs(dr3[i_last]) * rc3[i_last] ** 2)
                  if bound_r is not None else None)
        out["E3"] = {"drho_r2_far_2clusters": amp3,
                     "drho_r2_far_1cluster": amp2,
                     "ratio": (amp3 / amp2) if abs(amp2) > 1e-12 else None,
                     "coeff_2clusters_at_bound_r": amp3_b,
                     "ratio_at_bound_r": ((amp3_b / bound_coeff)
                                          if bound_coeff else None),
                     "elapsed_s": round(_time.time() - t0, 1)}

        # ---- E4: energy ledger (report-only) --------------------------------
        r_ap = 3.5
        e_single = aperture_energy(e1["e_f"], e1["X"], e1["Y"], core, r_ap)
        e_quad = sum(aperture_energy(
            e2["e_f"], e2["X"], e2["Y"],
            c, r_ap) for c in find_cores(e2["rho_f"], e2["X"], e2["Y"], 4,
                                         r_search=12.0))
        out["E4"] = {"aperture": r_ap,
                     "E_single_core": e_single,
                     "E_cluster_4cores": e_quad,
                     "ratio_over_4x": e_quad / (4.0 * e_single)}

    # profiles for the figure / receipt (E1/E2 = relaxed static state,
    # E2b = evolved snapshot of the moving pair)
    out["profiles"] = {
        "r": [round(float(x), 2) for x in rc2],
        "E1_absdrho": [None if np.isnan(v) else float(v)
                       for v in np.abs(dr1)],
        "E2_absdrho": [None if np.isnan(v) else float(v) for v in a2],
        "E2_absdrho_evolved": [None if np.isnan(v) else float(v)
                               for v in np.abs(dr2_ev)],
        "E2b_absdrho": [None if np.isnan(v) else float(v) for v in ab],
        "E2b_absdrho_relaxed": [None if np.isnan(v) else float(v)
                                for v in ar],
        "E0_floor": [None if np.isnan(v) else float(v) for v in prof0],
    }
    out["deviations_from_preregistration"] = [
        "E1 plateau window moved from (5, 12) to (3, 7): the registered "
        "window reaches into the screen-cancellation zone (partners at "
        "D = 30 cancel the test vortex's velocity beyond r ~ D/4) and, "
        "past r ~ 17, the bins pass through the partner cores. "
        "Geometry, fixed before any rule re-evaluation.",
        "Rule source moved from evolved-state profiles to the RELAXED "
        "(static) state: the first full run showed a ~1e-3 standing-"
        "sound/boundary-ring floor in the evolved fields that swamps "
        "any far signal (drho*r^2 grows toward the box edge). The "
        "static question is pre-registered as 'the medium's static "
        "response'; the evolved profiles are retained in the receipt "
        "as the stability cross-check. First-run numbers recorded in "
        "the result note.",
        "Amplitude clause: reported at the pre-registered r = 40 AND "
        "as the monopole bound at the deepest above-floor radius; if "
        "the 5% certification is floor-limited at r = 40, the achieved "
        "bound is recorded instead of silently passing.",
    ]
    return out


def evaluate_rules(out):
    """Decision rules R1-R3 of #149, verbatim."""
    e1 = out["E1"]
    r3_valid = e1["rel_dev"] <= 0.15
    e2 = out["E2"]
    amp_ok = e2["ratio_to_E1_plateau"] <= 0.05
    s = e2["slope"]
    if s is None:
        slope_clause = "no bins above 3x floor beyond 2D -- amplitude " \
                       "clause alone decides (consistent with no monopole)"
        slope_ok = True
    else:
        slope_ok = s >= 3.5
        slope_clause = f"measured slope {s:.2f} (>= 3.5 required)"
    r2 = bool(r3_valid and amp_ok and slope_ok)
    r1 = False
    if e2["slope"] is not None and "E3" in out and \
            out["E3"]["ratio"] is not None:
        r1 = (abs(e2["slope"] - 2.0) <= 0.3
              and abs(out["E3"]["ratio"] - 2.0) <= 0.6)
    achieved = e2.get("monopole_bound_ratio_to_E1")
    return {"R3_instrument_valid": bool(r3_valid),
            "R2_clean_negative": r2,
            "R2_amplitude_at_r40_ratio": e2["ratio_to_E1_plateau"],
            "R2_achieved_monopole_bound":
                (f"{achieved:.3f} of the E1 coefficient at "
                 f"r = {e2.get('monopole_bound_r')}"
                 if achieved is not None else "n/a"),
            "R2_slope_clause": slope_clause,
            "R1_monopole_found": bool(r1)}


def make_figure(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    p = out["profiles"]
    r = np.array(p["r"], dtype=float)

    def arr(key):
        return np.array([np.nan if v is None else v for v in p[key]])

    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    ax.loglog(r, arr("E1_absdrho"), "o-", ms=3, color="tab:blue",
              label=r"E1 single $\ell=1$ (winding: $r^{-2}$)")
    ax.loglog(r, arr("E2b_absdrho_relaxed"), "s-", ms=3, color="tab:green",
              label=r"E2b net-zero dipole pair ($r^{-4}$)")
    ax.loglog(r, arr("E2_absdrho"), "d-", ms=3, color="tab:red",
              label=r"E2 net-zero quadrupole ($r^{-6}$)")
    ax.loglog(r, arr("E0_floor"), ":", color="0.5", label="E0 floor")
    for s, rref, yref, c in ((2, 8.0, 8e-3, "tab:blue"),
                             (4, 8.0, 3e-3, "tab:green"),
                             (6, 8.0, 1e-3, "tab:red")):
        rr = np.array([rref, rref * 3.0])
        ax.loglog(rr, yref * (rr / rref) ** (-s), "--", lw=1, color=c,
                  alpha=0.6)
    ax.set_xlabel(r"$r$ (from composite centroid)")
    ax.set_ylabel(r"$|\langle\delta\rho\rangle|$")
    ax.set_title("#149 H-EXT: the circulation multipole ladder",
                 fontsize=11)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIGURE), exist_ok=True)
    fig.savefig(FIGURE, dpi=160)
    plt.close(fig)


def main(quick=False):
    print(f"H-EXT (#149) -- extensivity battery, backend {backend_name()}"
          f"{' [quick]' if quick else ''}")
    out = run_battery(quick=quick)
    rules = evaluate_rules(out)
    receipt = {"issue": 149,
               "hypothesis": "H-EXT: energy-sourced monopole vs "
                             "circulation multipole ladder (rules of #149)",
               "mode": "quick" if quick else "full",
               "b": B,
               "results": {k: v for k, v in out.items() if k != "profiles"},
               "profiles": out["profiles"],
               "rules": rules}
    os.makedirs(os.path.dirname(RECEIPT), exist_ok=True)
    if not quick:
        with open(RECEIPT, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2)
        make_figure(out)
        print(f"  receipt -> {os.path.relpath(RECEIPT, REPO)}")
        print(f"  figure  -> {os.path.relpath(FIGURE, REPO)}")

    e1, e2 = out["E1"], out["E2"]
    print(f"  E1 plateau (relaxed) drho*r^2 = "
          f"{e1['drho_r2_plateau_relaxed']:+.4f} "
          f"(expected {e1['expected']:+.2f}; dev {e1['rel_dev']:.1%}; "
          f"evolved snapshot {e1['drho_r2_plateau_evolved_snapshot']:+.4f})")
    print(f"  E2 far amplitude (relaxed, r in {e2['amp_window']}) "
          f"drho*r^2 = {e2['drho_r2_far']:+.6f} "
          f"({e2['ratio_to_E1_plateau']:.2%} of E1 plateau; bound 5%)")
    print(f"  E2 monopole bound: {e2['monopole_bound_ratio_to_E1']} "
          f"of E1 at r = {e2['monopole_bound_r']}")
    print(f"  E2 slope: {e2['slope']} over {e2['n_valid_bins']} valid bins")
    print(f"  E2b slope: relaxed {out['E2b']['slope_relaxed']} / "
          f"evolved snapshot {out['E2b']['slope_evolved_snapshot']} "
          f"(d_eff {out['E2b']['d_eff']})")
    if "E3" in out:
        print(f"  E3 two-cluster/one-cluster far ratio: "
              f"{out['E3']['ratio']}")
    if "E4" in out:
        print(f"  E4 cluster energy / 4x single: "
              f"{out['E4']['ratio_over_4x']:.3f}")
    print(f"  R3 instrument valid: {rules['R3_instrument_valid']}; "
          f"R2 clean negative: {rules['R2_clean_negative']} "
          f"({rules['R2_slope_clause']}); "
          f"R1 monopole found: {rules['R1_monopole_found']}")
    return receipt


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="small deterministic grid (no receipt/figure)")
    args = ap.parse_args()
    main(quick=args.quick)

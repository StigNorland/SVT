"""#129 H-SPATIAL -- does the medium delay light in a gravity well?

Pre-registered on issue #129 (H-SPATIAL comment + lensing/force-guard
addendum, posted before computing). Measures gamma_eff = (index/
propagation delay)/(clock-rate delay) for a phase wave crossing a static
density depression in the logarithmic medium.

S1 analytic result (derivation in the result note): linearizing the
Madelung equations around a static background rho_b(x) gives

    phi_tt = b [ lap(phi) + grad(ln rho_b) . grad(phi) ],

so in the eikonal limit the phase-wave ray speed is sqrt(b) EVERYWHERE,
independent of rho_b -- the logarithmic nonlinearity is the unique case
whose sound speed (c_s^2 = b) carries no density dependence, and even the
dispersive k^4/4 Bogoliubov correction is rho-independent. Matter clocks,
by contrast, dilate by Phi = b ln(rho_b/rho_0) (the H8b identification).
S1 therefore PREDICTS gamma_eff = 0 (decision rule R2): the literal LogSE
medium supplies the time half of gravity and none of the spatial half.

S2 (this script) tests that prediction with a demonstrated-sensitive
instrument:
  - main runs: sound packet transits a Thomas-Fermi depression
    rho_b = exp(-V/b) from an external Gaussian V; arrival time compared
    to a V = 0 control; clock-delay denominator Dt_clock = int V dl.
  - POSITIVE CONTROL: a region of spatially varying b(x) (which DOES
    change c_s; uniform rho = 1 stays an exact equilibrium since
    b(x)*ln(1) = 0) with an exactly predictable delay -- proves the
    instrument would have seen an index if one existed.
  - R3: wavelength sweep (decade), R4: depth sweep, plus an off-axis run
    for the deflection null.

Force-vs-time guard: both halves of gamma_eff are delays; the probe is a
collective sound wave of the medium itself (NOT a Schroedinger packet in
an external potential, which is the matter/time side already covered by
wave_deflection.py); no force is modelled anywhere.

Run:  python instruments/paper_iv/h_spatial_index.py [--quick] [--cpu]
GPU via SSV_GPU=1 (cupy, complex64). Writes
papers/SSV-IV/results/h_spatial_receipt.json and a figure.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time as _time
from pathlib import Path

import numpy as np

_GPU = os.environ.get("SSV_GPU", "") not in ("", "0", "false", "False")
if _GPU:
    import cupy as xp
else:
    xp = np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-IV" / "results"
FIGURES = ROOT / "papers" / "SSV-IV" / "figures"

B0 = 1.0                      # LogSE coupling: c_s = sqrt(B0) = 1


# ----------------------------------------------------------------------
# medium
# ----------------------------------------------------------------------

class Medium2D:
    """Split-step LogSE on a periodic grid; b may be spatially varying."""

    def __init__(self, nx, ny, dx, b=None, V=None):
        self.nx, self.ny, self.dx = nx, ny, dx
        kx = 2 * np.pi * np.fft.fftfreq(nx, dx)
        ky = 2 * np.pi * np.fft.fftfreq(ny, dx)
        KX, KY = np.meshgrid(kx, ky, indexing="ij")
        self.k2 = xp.asarray((KX**2 + KY**2).astype(np.float32))
        # 2/3-rule dealiasing: the log nonlinearity is infinite-order in
        # the perturbation and aliases into high k; without this filter
        # the split-step develops a spurious high-k instability (fp32
        # blows up by t~20, fp64 follows later). Probe carriers sit far
        # below the cutoff, so the filter does not touch the physics.
        kx_max, ky_max = np.abs(kx).max(), np.abs(ky).max()
        mask = ((np.abs(KX) <= (2 / 3) * kx_max)
                & (np.abs(KY) <= (2 / 3) * ky_max))
        self.dealias = xp.asarray(mask.astype(np.float32))
        self.b = xp.asarray(np.float32(B0) if b is None
                            else b.astype(np.float32))
        self.V = xp.asarray(np.zeros((nx, ny), np.float32) if V is None
                            else V.astype(np.float32))

    def step(self, psi, dt):
        """Strang split: half nonlinear, full kinetic (dealiased)."""
        rho = xp.abs(psi) ** 2
        ph = (self.b * xp.log(xp.maximum(rho, 1e-12)) + self.V) * (dt / 2)
        psi = psi * xp.exp(-1j * ph)
        psi = xp.fft.ifft2(xp.fft.fft2(psi)
                           * (xp.exp(-1j * self.k2 * (dt / 2))
                              * self.dealias))
        rho = xp.abs(psi) ** 2
        ph = (self.b * xp.log(xp.maximum(rho, 1e-12)) + self.V) * (dt / 2)
        return psi * xp.exp(-1j * ph)


def grids(nx, ny, dx):
    x = (np.arange(nx) - nx / 2) * dx
    y = (np.arange(ny) - ny / 2) * dx
    return np.meshgrid(x, y, indexing="ij")


def make_packet(X, rho_b, k, x0, w, eps=1e-3):
    """Right-moving sound packet on background rho_b:
    u = eps g(x) cos(k(x-x0)),  phi = (sqrt(b)/k) eps g(x) sin(k(x-x0))."""
    g = np.exp(-((X - x0) / w) ** 2)
    u = eps * g * np.cos(k * (X - x0))
    phi = (math.sqrt(B0) / k) * eps * g * np.sin(k * (X - x0))
    psi = np.sqrt(rho_b * (1.0 + u)) * np.exp(1j * phi)
    return psi.astype(np.complex64)


# ----------------------------------------------------------------------
# one transit
# ----------------------------------------------------------------------

def run_transit(nx, ny, dx, k, x0, w, x_det, t_end, dt,
                V=None, b=None, y_offset=0.0, record_every=1,
                eps=1e-3, tag="", with_packet=True):
    """Propagate (packet or no-packet baseline); record the on-axis
    density strip signal at the detector column and the transverse
    centroid there. Returns (t, signal, centroid_y).

    The baseline run (with_packet=False) carries the background's own
    startup transients (Thomas-Fermi vs exact equilibrium mismatch);
    subtracting it from the packet run isolates the probe wave exactly
    at linear order."""
    X, Y = grids(nx, ny, dx)
    rho_b = np.ones((nx, ny), np.float32)
    if V is not None:
        rho_b = np.exp(-V / B0).astype(np.float32)     # Thomas-Fermi
    med = Medium2D(nx, ny, dx, b=b, V=V)
    if with_packet:
        g_y = np.exp(-((Y - y_offset) / (0.30 * ny * dx)) ** 2)
        g = np.exp(-((X - x0) / w) ** 2) * g_y
        u = eps * g * np.cos(k * (X - x0))
        phi = (math.sqrt(B0) / k) * eps * g * np.sin(k * (X - x0))
        psi0 = np.sqrt(rho_b * (1.0 + u)) * np.exp(1j * phi)
    else:
        psi0 = np.sqrt(rho_b).astype(np.complex64)
    psi = xp.asarray(psi0.astype(np.complex64))
    rho_b_d = xp.asarray(rho_b)
    i_det = int(round(x_det / dx + nx / 2))

    n_steps = int(round(t_end / dt))
    ts, cols = [], []
    t0 = _time.time()
    for n in range(n_steps):
        psi = med.step(psi, dt)
        if n % record_every == 0:
            dr = xp.abs(psi[i_det, :]) ** 2 - rho_b_d[i_det, :]
            ts.append((n + 1) * dt)
            cols.append(np.asarray(dr.get() if _GPU else dr,
                                   dtype=np.float32))
    if tag:
        print(f"    [{tag}] {n_steps} steps in {_time.time()-t0:.0f}s",
              flush=True)
    return np.array(ts), np.array(cols)


def col_signal(t, cols, ny, dx, k, y_offset=0.0):
    """Strip-summed scalar signal from a detector-column time series."""
    yv = (np.arange(ny) - ny / 2) * dx
    lam = 2 * math.pi / k
    strip = (np.abs(yv - y_offset) <= lam).astype(np.float32)
    return cols @ strip


def col_centroid_at_peak(t, cols, ny, dx, k, y_offset=0.0):
    """Transverse power-weighted centroid of the packet at arrival,
    computed from a (baseline-subtracted) column time series: power is
    summed over the arrival window, the centroid restricted to a
    +-3 lambda window around the launch offset (noise across the full
    column otherwise drags the centroid toward the box centre)."""
    yv = (np.arange(ny) - ny / 2) * dx
    lam = 2 * math.pi / k
    omega = math.sqrt(B0) * k
    s = col_signal(t, cols, ny, dx, k, y_offset)
    z = _analytic(s, t, omega)
    _, sl = _peak_window_centroid(t, np.abs(z) ** 2)
    p = np.sum(cols[sl, :] ** 2, axis=0)
    ywin = np.abs(yv - y_offset) <= 3 * lam
    return float(np.sum(p[ywin] * yv[ywin]) / np.sum(p[ywin]))


def transit_cols(**kw):
    """Baseline-subtracted detector-column time series: packet run minus
    no-packet run on the same background (removes startup transients
    exactly at linear order)."""
    t, cols = run_transit(with_packet=True, **kw)
    tag = kw.pop("tag", "")
    _, cols0 = run_transit(with_packet=False,
                           tag=(tag + " baseline") if tag else "", **kw)
    return t, cols - cols0


def _analytic(sig, t=None, omega=None):
    """Analytic signal via FFT (positive-frequency doubling). If a
    carrier omega is given, bandpass to [0.5, 1.5]*omega first -- slow
    drifts otherwise dominate the envelope at long carrier periods."""
    n = len(sig)
    S = np.fft.fft(sig - np.mean(sig))
    h = np.zeros(n)
    h[0] = 1.0
    if n % 2 == 0:
        h[n // 2] = 1.0
        h[1:n // 2] = 2.0
    else:
        h[1:(n + 1) // 2] = 2.0
    if omega is not None and t is not None:
        f = np.fft.fftfreq(n, t[1] - t[0]) * 2 * np.pi
        band = (np.abs(f) >= 0.5 * omega) & (np.abs(f) <= 1.5 * omega)
        h = h * band
    return np.fft.ifft(S * h)


def _peak_window_centroid(t, w2, frac=0.1):
    """Envelope-power centroid restricted to the contiguous window around
    the global peak where power exceeds frac*max -- immune to record
    truncation and to low-level energy elsewhere in the record."""
    i_pk = int(np.argmax(w2))
    thr = frac * w2[i_pk]
    lo = i_pk
    while lo > 0 and w2[lo - 1] > thr:
        lo -= 1
    hi = i_pk
    while hi < len(w2) - 1 and w2[hi + 1] > thr:
        hi += 1
    sl = slice(lo, hi + 1)
    return float(np.sum(t[sl] * w2[sl]) / np.sum(w2[sl])), sl


def arrival_shift(t, s_ref, s_test, omega):
    """Arrival-time shift of s_test vs s_ref (positive = later):
    peak-windowed envelope centroid (coarse), refined by carrier phase in
    the overlap of the two windows (cycle-skip corrected). The
    VLBI/Shapiro method, hardened against record truncation."""
    z_r = _analytic(s_ref, t, omega)
    z_t = _analytic(s_test, t, omega)
    w_r, w_t = np.abs(z_r) ** 2, np.abs(z_t) ** 2
    t_r, sl_r = _peak_window_centroid(t, w_r)
    t_s, sl_t = _peak_window_centroid(t, w_t)
    coarse = t_s - t_r
    lo = max(sl_r.start, sl_t.start)
    hi = min(sl_r.stop, sl_t.stop)
    if hi <= lo:                      # disjoint windows: coarse only
        return float(coarse)
    sl = slice(lo, hi)
    dphi = np.angle(np.sum(z_t[sl] * np.conj(z_r[sl])))
    fine = -dphi / omega          # later arrival => phase lag => -dphi>0
    n_cyc = round((coarse - fine) * omega / (2 * math.pi))
    return float(fine + n_cyc * 2 * math.pi / omega)


# ----------------------------------------------------------------------
# the battery
# ----------------------------------------------------------------------

def predicted_clock_delay(v0, sigma):
    """Dt_clock = int V dl along the central chord (b = c = 1 units)."""
    return v0 * sigma * math.sqrt(math.pi)


def predicted_index_delay_bwell(eta, sigma, dx, L, k):
    """Exact predicted delay for the positive control
    b(x) = 1 - eta exp(-r^2/sigma^2) along y = 0, including the
    (rho-independent) Bogoliubov dispersion: v_p(x) = sqrt(b(x) + k^2/4)."""
    x = np.arange(-L / 2, L / 2, dx)
    bx = B0 * (1.0 - eta * np.exp(-(x / sigma) ** 2))
    vp = np.sqrt(bx + k * k / 4.0)
    vp0 = math.sqrt(B0 + k * k / 4.0)
    return float(np.trapezoid(1.0 / vp - 1.0 / vp0, x))


def battery(quick=False):
    if quick:
        nx, ny, dx = 1024, 256, 0.5
        sigma, x0 = 50.0, -160.0
        x_det, t_end, dt, rec = 160.0, 400.0, 0.1, 4
        lams = [8.0, 16.0]
        depths = [0.1]
        lam_pc = 8.0
    else:
        nx, ny, dx = 4096, 768, 0.5
        sigma, x0 = 120.0, -550.0
        x_det, t_end, dt, rec = 550.0, 1600.0, 0.1, 4
        lams = [10.0, 20.0, 50.0]   # R3 window: xi << lambda << sigma
        depths = [0.05, 0.1]
        lam_pc = 20.0
    L = nx * dx

    def w_of(lam):
        """Per-wavelength envelope width: >= 3 carrier wavelengths so the
        packet has a well-defined carrier (fewer and the phase-delay
        measurement breaks, as the lam=50/w=100 run demonstrated)."""
        return max(24.0 if quick else 60.0, 3.0 * lam)

    base = dict(nx=nx, ny=ny, dx=dx, x0=x0, x_det=x_det,
                t_end=t_end, dt=dt, record_every=rec)
    X, Y = grids(nx, ny, dx)
    r2 = X**2 + Y**2

    out = {"config": {"nx": nx, "ny": ny, "dx": dx, "sigma": sigma,
                      "lambdas": lams, "depths": depths, "b0": B0,
                      "lam_positive_control": lam_pc,
                      "quick": quick, "gpu": _GPU},
           "runs": {}}

    # ---- controls (V = 0, uniform medium = exact equilibrium: no
    # baseline needed) per wavelength; also calibrate the speed ---------
    controls = {}
    for lam in lams:
        k = 2 * math.pi / lam
        t, cols = run_transit(k=k, w=w_of(lam),
                              tag=f"control lam={lam}", **base)
        s = col_signal(t, cols, ny, dx, k)
        controls[lam] = (t, s, cols)
        z = _analytic(s, t, math.sqrt(B0) * k)
        t_arr, _ = _peak_window_centroid(t, np.abs(z) ** 2)
        v_meas = (x_det - x0) / t_arr
        vg_pred = ((k + k**3 / 2)
                   / math.sqrt(B0 * k * k + k**4 / 4))
        out["runs"][f"control_lam{lam}"] = {
            "v_measured": float(v_meas),
            "v_group_predicted": float(vg_pred)}

    # ---- POSITIVE CONTROL: varying-b well (real index; uniform rho = 1
    # remains an exact equilibrium, so no baseline needed). GENTLE well:
    # the predicted delay must stay well under half a carrier period so
    # the phase measurement is unambiguous and lensing distortion weak ---
    eta = 0.04
    b_well = (B0 * (1.0 - eta * np.exp(-r2 / sigma**2))).astype(np.float32)
    k = 2 * math.pi / lam_pc
    om = math.sqrt(B0) * k
    t, cols = run_transit(k=k, w=w_of(lam_pc), b=b_well,
                          tag="positive-control", **base)
    s = col_signal(t, cols, ny, dx, k)
    dt_pc = arrival_shift(controls[lam_pc][0], controls[lam_pc][1], s, om)
    dt_pc_pred = predicted_index_delay_bwell(eta, sigma, dx, L, k)
    out["positive_control"] = {
        "eta": eta, "lambda": lam_pc,
        "delay_measured": dt_pc, "delay_predicted": dt_pc_pred,
        "ratio": dt_pc / dt_pc_pred if dt_pc_pred else float("nan")}

    # ---- main runs: TF depression (baseline-subtracted), R3 sweep ------
    v_main = depths[-1]
    gam = {}
    for lam in lams:
        k = 2 * math.pi / lam
        om = math.sqrt(B0) * k
        V = (v_main * np.exp(-r2 / sigma**2)).astype(np.float32)
        t, cols = transit_cols(k=k, w=w_of(lam), V=V,
                               tag=f"depression lam={lam}", **base)
        s = col_signal(t, cols, ny, dx, k)
        d_idx = arrival_shift(controls[lam][0], controls[lam][1], s, om)
        d_clk = predicted_clock_delay(v_main, sigma)
        gam[lam] = d_idx / d_clk
        out["runs"][f"depression_lam{lam}_V{v_main}"] = {
            "index_delay": d_idx, "clock_delay": d_clk,
            "gamma_eff": gam[lam]}

    # ---- R4: depth sweep at the positive-control wavelength ------------
    k = 2 * math.pi / lam_pc
    om = math.sqrt(B0) * k
    for v0 in depths[:-1]:
        V = (v0 * np.exp(-r2 / sigma**2)).astype(np.float32)
        t, cols = transit_cols(k=k, w=w_of(lam_pc), V=V,
                               tag=f"depth V0={v0}", **base)
        s = col_signal(t, cols, ny, dx, k)
        d_idx = arrival_shift(controls[lam_pc][0], controls[lam_pc][1],
                              s, om)
        d_clk = predicted_clock_delay(v0, sigma)
        out["runs"][f"depression_lam{lam_pc}_V{v0}"] = {
            "index_delay": d_idx, "clock_delay": d_clk,
            "gamma_eff": d_idx / d_clk}

    # ---- deflection null: off-axis run ---------------------------------
    if not quick:
        k = 2 * math.pi / lam_pc
        V = (v_main * np.exp(-r2 / sigma**2)).astype(np.float32)
        yoff = sigma / math.sqrt(2)
        t, cols = transit_cols(k=k, w=w_of(lam_pc), V=V, y_offset=yoff,
                               tag="off-axis", **base)
        t0c, cols0 = run_transit(k=k, w=w_of(lam_pc), y_offset=yoff,
                                 tag="off-axis control", **base)
        cen = col_centroid_at_peak(t, cols, ny, dx, k, y_offset=yoff)
        cen0 = col_centroid_at_peak(t0c, cols0, ny, dx, k, y_offset=yoff)
        out["deflection"] = {
            "y_offset": yoff,
            "centroid_shift": float(cen - cen0),
            "note": "baseline-subtracted transverse centroid shift at "
                    "the packet's arrival, vs uniform-medium control"}

    # ---- verdicts -------------------------------------------------------
    g_vals = list(gam.values())
    g_med = float(np.median(g_vals))
    pc = out["positive_control"]
    pc_ok = bool(abs(pc["ratio"] - 1.0) < 0.2)
    achrom_spread = float(np.max(g_vals) - np.min(g_vals))
    out["verdicts"] = {
        "instrument_validated": pc_ok,
        "gamma_eff_median": g_med,
        "gamma_eff_by_lambda": {str(k_): float(v) for k_, v in gam.items()},
        "R1_pass_gamma_1": bool(abs(g_med - 1.0) <= 0.1),
        "R2_gamma_0": bool(abs(g_med) <= 0.1),
        "R3_achromatic_spread": achrom_spread,
        "S1_prediction": "gamma_eff = 0 (log nonlinearity: c_s "
                         "density-independent; clocks dilate by b ln rho)",
    }
    return out


def main():
    quick = "--quick" in sys.argv
    print(f"H-SPATIAL S2, backend {'cupy/GPU' if _GPU else 'numpy/CPU'}, "
          f"quick={quick}", flush=True)
    out = battery(quick=quick)
    RESULTS.mkdir(parents=True, exist_ok=True)
    dest = RESULTS / ("h_spatial_receipt_quick.json" if quick
                      else "h_spatial_receipt.json")
    dest.write_text(json.dumps(out, indent=1))
    v = out["verdicts"]
    pc = out["positive_control"]
    print(f"positive control: measured {pc['delay_measured']:.2f} vs "
          f"predicted {pc['delay_predicted']:.2f} "
          f"(ratio {pc['ratio']:.3f}) -> instrument "
          f"{'VALIDATED' if v['instrument_validated'] else 'NOT VALIDATED'}")
    for lam, g in v["gamma_eff_by_lambda"].items():
        print(f"  lambda={lam}: gamma_eff = {g:+.4f}")
    print(f"median gamma_eff = {v['gamma_eff_median']:+.4f}  "
          f"(R1 needs 1.0+-0.1; R2 is |g|<=0.1)")
    print(f"R3 spread across wavelengths: {v['R3_achromatic_spread']:.4f}")
    if "deflection" in out:
        print(f"deflection centroid shift: "
              f"{out['deflection']['centroid_shift']:+.3f}")
    print(f"receipt -> {dest}")


if __name__ == "__main__":
    main()

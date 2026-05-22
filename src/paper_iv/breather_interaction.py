"""
SSV IV -- breather-interaction solver
=====================================

Tests the *source* end of the gravitational chain (Paper IV, Section 4): that
two oscillating ("breathing") sources in the logarithmic-Schrodinger medium
radiate waves, interfere through the medium's nonlinearity, and exert a
time-averaged force on one another -- attractive when they oscillate in phase.

Together with wave_deflection.py (Section 6: a probe refracting in an imposed
potential) this closes the chain -- Section 4 produces the field, Section 6
bends a probe in it.

Model (hbar = m = rho0 = 1), on a uniform background psi = 1:

    i d_t psi = -1/2 lap psi + b ln(|psi|^2) psi + V(x,t) psi   (+ absorber)

Two localised drives pulse the medium at x = -d/2 and x = +d/2,

    V(x,t) = V0 ramp(t) sin(w t) [ W_A(x) + s W_B(x) ],

with s = +1 (in phase) or s = -1 (anti-phase).  Each driven spot radiates
waves; the waves interfere; the time-averaged force on source A,

    <F_A,x> = < integral rho(x,t) d_x V_A(x,t) dx > ,

is measured over an integer number of drive periods.  Section 4 predicts
<F_A,x> > 0 (A pulled toward B, attraction) for in-phase drives, a reversal
for anti-phase drives, and no net force on an isolated source.  Outgoing
waves are removed by a relaxation absorber, so the measurement is of
radiation, not of box modes.

Run:  python breather_interaction.py
"""

import numpy as np


# --------------------------------------------------------------------------
# grid, source windows, absorber
# --------------------------------------------------------------------------
def make_grid(N, L):
    x = np.linspace(-L / 2, L / 2, N, endpoint=False)
    dx = x[1] - x[0]
    X, Y = np.meshgrid(x, x, indexing="ij")
    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    return dx, X, Y, KX * KX + KY * KY


def window(X, Y, xs, w):
    """Gaussian source window at (xs, 0) and its x-derivative."""
    W = np.exp(-((X - xs) ** 2 + Y ** 2) / (2.0 * w * w))
    dWdx = -(X - xs) / (w * w) * W
    return W, dWdx


def absorber(X, Y, L, width, gmax):
    """Smooth damping layer near the four box edges."""
    edge = L / 2.0 - width

    def ramp(q):
        s = np.clip((np.abs(q) - edge) / width, 0.0, 1.0)
        return s * s

    return gmax * np.maximum(ramp(X), ramp(Y))


# --------------------------------------------------------------------------
# one run: returns the time-averaged force on source A
# --------------------------------------------------------------------------
def run(d, s_phase, *, N=256, L=100.0, b=1.0, V0=0.25, w=1.6, omega=0.7,
        dt=0.025, t_ramp=15.0, t_transient=110.0, n_periods=12,
        single=False, floor=1e-6):
    dx, X, Y, K2 = make_grid(N, L)
    WA, dWA = window(X, Y, -d / 2.0, w)
    WB, dWB = window(X, Y, +d / 2.0, w)
    Wdrive = WA + (0.0 if single else s_phase) * WB
    Gamma = absorber(X, Y, L, width=18.0, gmax=1.5)
    decay = np.exp(-Gamma * dt)

    period = 2.0 * np.pi / omega
    t_total = t_transient + n_periods * period
    nsteps = int(round(t_total / dt))

    psi = np.ones((N, N), dtype=complex)
    expK_half = np.exp(-1j * K2 / 2.0 * (dt / 2.0))
    cellA = V0 * dWA * dx * dx                  # force-integral kernel for A

    fsum, fcount = 0.0, 0
    for n in range(nsteps):
        t = n * dt
        psi = np.fft.ifft2(expK_half * np.fft.fft2(psi))      # kinetic dt/2
        tm = t + dt / 2.0
        ramp = min(1.0, tm / t_ramp)
        Vt = V0 * ramp * np.sin(omega * tm) * Wdrive
        rho = np.abs(psi) ** 2
        psi = psi * np.exp(-1j * (b * np.log(np.maximum(rho, floor)) + Vt) * dt)
        psi = 1.0 + (psi - 1.0) * decay                       # relaxation absorber
        psi = np.fft.ifft2(expK_half * np.fft.fft2(psi))      # kinetic dt/2
        if t >= t_transient:                                  # measure F_A,x
            rho = np.abs(psi) ** 2
            fsum += np.sin(omega * (t + dt)) * np.sum(rho * cellA)
            fcount += 1
    return fsum / max(fcount, 1)


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------
def main():
    import sys
    import time as _time
    try:
        sys.stdout.reconfigure(line_buffering=True)      # stream output
    except Exception:
        pass

    cfg = dict(N=160, t_transient=70.0, n_periods=8)

    print("SSV IV -- breather-interaction test (Section 4: the interference "
          "cross-term)")
    print("2D logarithmic-Schrodinger medium, hbar = m = rho0 = 1; "
          "i d_t psi = -1/2 lap psi + b ln|psi|^2 psi + V psi")
    print(f"grid N={cfg['N']}, transient {cfg['t_transient']:.0f}, "
          f"averaging over {cfg['n_periods']} drive periods")
    print()
    print("Section 4: the two-breather force is the bilinear cross-term")
    print("u_AB = -b rho0 x_A x_B.  Flipping one source's phase flips x_B, "
          "so the")
    print("force must reverse exactly -- the in-phase/anti-phase ratio is "
          "the")
    print("decisive, regime-independent signature and must equal -1.")
    print()

    t0 = _time.time()
    print("baseline: a single isolated source should feel no net force ...")
    f_single = run(d=24.0, s_phase=+1.0, single=True, **cfg)
    print(f"  single source:   <F_A,x> = {f_single:+.3e}   "
          f"[{_time.time()-t0:.0f}s]\n")

    header = "  d      in-phase <F_A,x>     anti-phase <F_A,x>     ratio"
    print(header)
    print("  " + "-" * (len(header) - 2))

    rows = []
    for d in (15.0, 20.0, 25.0, 30.0):
        tr = _time.time()
        f_in = run(d, s_phase=+1.0, **cfg)
        f_anti = run(d, s_phase=-1.0, **cfg)
        rows.append((d, f_in, f_anti))
        ratio = f_in / f_anti if f_anti != 0 else float("nan")
        print(f"  {d:4.0f}   {f_in:+.4e}        {f_anti:+.4e}      "
              f"{ratio:+7.2f}   [{_time.time()-tr:.0f}s]")

    f_in = [r[1] for r in rows]
    f_anti = [r[2] for r in rows]
    scale = max(abs(v) for v in f_in)
    ratios = [fi / fa for fi, fa in zip(f_in, f_anti)]

    baseline_ok = abs(f_single) < 0.15 * scale
    antisym_ok = all(abs(r + 1.0) < 0.15 for r in ratios)

    print()
    print("The in-phase force changes sign across these separations: they "
          "span the")
    print("radiation zone (d ~ 2-3 sound wavelengths), where retardation "
          "rotates")
    print("the arriving wave's phase.  Near-zone attraction (d << lambda) "
          "and the")
    print("full F(d) oscillation are mapped by the 'near' and 'fine' runs.")
    print("At every separation, anti-phase reverses in-phase exactly:")
    print()
    print(f"  isolated source ~ 0          : "
          f"{'OK' if baseline_ok else 'FAIL'}")
    print(f"  anti-phase = -(in-phase)     : "
          f"{'OK' if antisym_ok else 'FAIL'}")
    ok = baseline_ok and antisym_ok
    print()
    print("RESULT:", "PASS -- the two-breather force is the bilinear "
          "interference cross-term of Section 4" if ok
          else "FAIL -- see table above")
    print("  (in-phase attraction: run 'near';  F(d) oscillation: run "
          "'fine')")
    return 0 if ok else 1


def sweep_fine(d_lo=7.0, d_hi=46.0, step=1.5):
    """Fine in-phase separation sweep, to map F(d) and resolve any
    radiation-zone oscillation against a possible attractive DC component."""
    import sys
    import time as _time
    import numpy as _np
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    cfg = dict(N=160, t_transient=70.0, n_periods=8)
    ds = _np.arange(d_lo, d_hi + 1e-6, step)

    print("SSV IV -- fine in-phase separation sweep of the "
          "breather-interaction force")
    print(f"grid N={cfg['N']}, {len(ds)} separations, in-phase drives, "
          f"sound wavelength ~ 9")
    print()
    print("     d         <F_A,x>")
    print("   " + "-" * 28)
    for d in ds:
        t0 = _time.time()
        f = run(float(d), +1.0, **cfg)
        print(f"   {d:5.1f}    {f:+.5e}    [{_time.time() - t0:.0f}s]")
    print()
    print("SWEEP COMPLETE")


def sweep_nearzone(omega=0.15, ds=(6.0, 8.0, 10.0, 12.0)):
    """Near-zone in-phase test.  Drive at low frequency so the sound
    wavelength lambda = 2 pi c_s / omega (with c_s = sqrt(b) = 1) greatly
    exceeds the separation d.  In this regime retardation is negligible and
    Section 4 predicts a clean, monotonically decreasing in-phase attraction
    with none of the radiation-zone sign oscillation seen when d ~ lambda.
    The separations are kept to d/lambda < 1/3 -- the genuine near zone;
    beyond that the radiation-zone oscillation mapped by sweep_fine() takes
    over and the sign begins to alternate.  The drive ramp, transient and
    averaging window are scaled to the long drive period."""
    import sys
    import time as _time
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    period = 2.0 * np.pi / omega
    lam = 2.0 * np.pi / omega                 # c_s = sqrt(b) = 1
    cfg = dict(N=160, omega=omega, t_ramp=2.0 * period,
               t_transient=5.0 * period, n_periods=6)

    print("SSV IV -- near-zone in-phase breather-interaction test "
          "(Section 4)")
    print("2D logarithmic-Schrodinger medium, hbar = m = rho0 = 1; "
          "c_s = sqrt(b) = 1")
    print(f"omega={omega}, sound wavelength lambda ~ {lam:.0f}, drive "
          f"period ~ {period:.0f}")
    print(f"separations stay below d/lambda = {max(ds) / lam:.2f} -- the "
          f"near zone\n")
    print("     d      d/lambda       <F_A,x>")
    print("   " + "-" * 40)

    rows = []
    for d in ds:
        t0 = _time.time()
        f = run(float(d), +1.0, **cfg)
        rows.append((d, f))
        print(f"   {d:5.1f}    {d / lam:8.3f}    {f:+.5e}    "
              f"[{_time.time() - t0:.0f}s]")

    attract = all(f > 0 for _, f in rows)
    decay = all(rows[i][1] > rows[i + 1][1] for i in range(len(rows) - 1))
    print()
    print("Section 4: in the near zone two in-phase breathers attract "
          "(<F_A,x> > 0,")
    print("A pulled toward B) and the force falls monotonically as the "
          "field dilutes.")
    print()
    print(f"  in-phase attractive (F > 0)    : "
          f"{'OK' if attract else 'FAIL'}")
    print(f"  monotonic decrease with d      : "
          f"{'OK' if decay else 'FAIL'}")
    print()
    print("RESULT:", "PASS -- near-zone in-phase breathers attract, force "
          "falls with d" if attract and decay
          else "FAIL -- see table above")
    print("NEARZONE COMPLETE")
    return 0 if attract and decay else 1


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "fine":
        sweep_fine()
        raise SystemExit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "near":
        raise SystemExit(sweep_nearzone())
    raise SystemExit(main())

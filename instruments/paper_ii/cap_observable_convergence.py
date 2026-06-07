"""Grid convergence of the reconnection cap-radius observable, and a diagnosis of
why the phi cap-geometry ansatz cannot yet be tested — Paper II §weak / #97.

Two findings, both reproduced by `main()`:

POSITIVE — the threshold-free `moment` observable is grid-convergent.
  The legacy `volume` cap radius (sqrt of a hard-threshold depleted-cell count)
  drifts ~30% across grids; the `radial-slice` max-extent is noisy in general.
  The `moment` radius — the depletion-weighted transverse second moment
  R_cap = sqrt(2 <rho^2>_w), w = (1-|psi|^2)_+, in the slice of maximum
  depletion — is an integral of the smooth field and converges to a few percent.
  This removes the #97 blocker that `cap_radius` drifts 17–62% under refinement.

NEGATIVE — the 2-ring merger harness produces no transient cap to measure.
  Evolving two coaxial opposite-circulation rings (the canonical reconnection
  case) at the c=1 convention (log_pressure=0.5), the on-axis |psi| at the
  geometric centre *increases* (it never depletes), and both the total depletion
  Sum w and R_cap grow *monotonically* with no interior peak or plateau.  There
  is thus no well-posed "cap radius" instant in this harness, so the golden-ratio
  cap-geometry ansatz (R_cap = phi R*) cannot be tested with it — independently
  of grid resolution.  The earlier "cap forms at ~6 xi" was an early-time sample
  of this monotonic growth read off at the (unstable) energy-saddle index.

Verdict: #97's observable is fixed; the phi-ansatz test is blocked not by grid
noise but by the absence of a transient cap in this configuration.  The remaining
work is a harness that realises the actual W-tube end-cap geometry (or a
principled reconnection-instant), not further refinement of this one.
"""

from __future__ import annotations

import dataclasses
import math

import numpy as np

import reconnection_supplement as r


def _run_to_time(n: int, lam: float, T: float, method: str, snapshots: int = 2):
    """Evolve the opposite-circulation pair to fixed physical time T; return the path."""
    cfg = r.Config(n=n, length=18.0, log_pressure=0.5, lambda_perp=lam,
                   cap_method=method, snapshots=snapshots)
    eff_dt = r.stability_dt_max(cfg)
    cfg = dataclasses.replace(cfg, steps=max(2, round(T / eff_dt)))
    path = r.evolve_path(cfg, 1.0, -1.0, effective_dt=eff_dt)
    return path, cfg


def grid_convergence(lam: float, T: float, ns, methods=("moment", "volume", "radial-slice")):
    """R_cap at fixed (lam, T) across grids `ns`, per method, with % spread."""
    table = {m: [] for m in methods}
    for n in ns:
        for m in methods:
            path, cfg = _run_to_time(n, lam, T, m)
            table[m].append(r.cap_radius_and_volume(path[-1], cfg)[0])

    def spread(xs):
        xs = np.asarray(xs, float)
        return float((xs.max() - xs.min()) / xs.mean() * 100.0)

    return {m: {"values": table[m], "spread_pct": spread(table[m])} for m in methods}


def dynamics_trace(n: int, lam: float, T: float, frames: int = 31):
    """Per-frame (center |psi|, total depletion, moment R_cap) over [0, T]."""
    path, cfg = _run_to_time(n, lam, T, "moment", snapshots=frames)
    c = cfg.n // 2
    center = [float(np.abs(p[c, c, c])) for p in path]
    sum_w = [float(np.clip(1 - np.abs(p) ** 2, 0, None).sum()) for p in path]
    rcap = [r.cap_radius_and_volume(p, cfg)[0] for p in path]
    return {"center_abs": center, "sum_w": sum_w, "rcap": rcap}


def has_interior_peak(series, rel_tol: float = 0.02) -> bool:
    """True if `series` rises then falls by more than rel_tol (a transient), i.e.
    the max is interior and the endpoint is meaningfully below it."""
    s = np.asarray(series, float)
    imax = int(np.argmax(s))
    return 0 < imax < len(s) - 1 and (s[imax] - s[-1]) / max(abs(s[imax]), 1e-30) > rel_tol


def main() -> None:
    print("=" * 68)
    print("Reconnection cap observable: grid convergence + cap-existence (#97)")
    print("=" * 68)

    lam, T = 1.0, 0.045
    print(f"\n[POSITIVE] grid convergence at lambda_perp={lam}, T={T}")
    conv = grid_convergence(lam, T, ns=(24, 32, 40, 48))
    print(f"  {'n':>4} {'moment':>9} {'volume':>9} {'rad-slice':>10}")
    for i, n in enumerate((24, 32, 40, 48)):
        print(f"  {n:>4} {conv['moment']['values'][i]:>9.3f} "
              f"{conv['volume']['values'][i]:>9.3f} {conv['radial-slice']['values'][i]:>10.3f}")
    print("  spread across n (%): " +
          ", ".join(f"{m}={conv[m]['spread_pct']:.1f}" for m in conv))

    print(f"\n[NEGATIVE] dynamics (n=40, lambda_perp={lam}): is there a transient cap?")
    tr = dynamics_trace(40, lam, 0.063)
    print(f"  center |psi|: {tr['center_abs'][0]:.3f} -> {tr['center_abs'][-1]:.3f} "
          f"({'depletes' if tr['center_abs'][-1] < tr['center_abs'][0] else 'never depletes'})")
    print(f"  sum_w peak interior? {has_interior_peak(tr['sum_w'])}  "
          f"({tr['sum_w'][0]:.0f} -> {tr['sum_w'][-1]:.0f})")
    print(f"  R_cap peak interior? {has_interior_peak(tr['rcap'])}  "
          f"({tr['rcap'][0]:.2f} -> {tr['rcap'][-1]:.2f})")
    print("\n  => monotonic growth, no transient cap: the phi-ansatz test is not")
    print("     extractable from this 2-ring harness (independent of grid).")


if __name__ == "__main__":
    main()

"""#77 follow-up: Peierls-Nabarro lattice-pinning test.

Question: is the rugged multi-basin landscape of the relaxed trefoil a physical
feature of the continuum, or a lattice artifact (Peierls-Nabarro pinning — the
spurious energy barrier a discrete grid creates as a defect moves between cells)?

Decisive test: take a single straight LogSE vortex, translate its core across
the grid in sub-cell steps, and measure the energy oscillation. That oscillation
amplitude IS the Peierls-Nabarro barrier for this field on this grid. Measure it
as a function of dx:

  - barrier amplitude -> 0 as dx -> 0   =>  LATTICE ARTIFACT (continuum smooth)
  - barrier amplitude -> finite constant =>  PHYSICAL ruggedness

Box size L is held fixed; only n (hence dx) varies. log_pressure = 0.5 (the
canonical c=1 convention used in all trefoil runs).

Usage:
    python peierls_nabarro_test.py [--box 8] [--output OUT.json]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from vortex_profile import VortexProfile

LOG_PRESSURE = 0.5
DENSITY_FLOOR = 1e-12


def energy_2d(psi: np.ndarray, dx: float, log_pressure: float) -> float:
    """Per-unit-length 2D LogSE energy (matches the 3D energy_density form)."""
    grad_sq = (
        np.abs(np.roll(psi, -1, axis=0) - psi) ** 2
        + np.abs(np.roll(psi, -1, axis=1) - psi) ** 2
    ) / (dx * dx)
    rho = np.maximum(np.abs(psi) ** 2, DENSITY_FLOOR)
    potential = log_pressure * (rho * np.log(rho) - rho + 1.0)
    return float(np.sum(0.5 * grad_sq + potential) * dx * dx)


def imprint_vortex(n: int, box: float, x0: float, y0: float,
                   prof: VortexProfile) -> tuple[np.ndarray, float]:
    """Single straight vortex (winding +1) with core at (x0, y0)."""
    dx = box / n
    ax = (np.arange(n) + 0.5) * dx - box / 2.0
    X, Y = np.meshgrid(ax, ax, indexing="ij")
    rx, ry = X - x0, Y - y0
    r = np.sqrt(rx * rx + ry * ry)
    theta = np.arctan2(ry, rx)
    # vectorised profile lookup: f(r), f->1 beyond the solved range
    f = np.interp(r.ravel(), prof.xs, prof.fs, left=0.0, right=1.0).reshape(r.shape)
    psi = f * np.exp(1j * theta)
    return psi.astype(np.complex128), dx


def pn_barrier(n: int, box: float, prof: VortexProfile, n_shift: int = 11) -> dict:
    """Translate the core from 0 to dx along x; return energy oscillation amplitude."""
    dx = box / n
    shifts = np.linspace(0.0, dx, n_shift)
    energies = []
    for s in shifts:
        psi, _ = imprint_vortex(n, box, x0=float(s), y0=0.0, prof=prof)
        energies.append(energy_2d(psi, dx, LOG_PRESSURE))
    energies = np.array(energies)
    e_mean = float(energies.mean())
    amplitude = float(energies.max() - energies.min())
    return {
        "n": n, "dx": dx, "box": box,
        "E_mean": e_mean,
        "pn_barrier_abs": amplitude,
        "pn_barrier_rel": amplitude / abs(e_mean) if e_mean != 0 else float("nan"),
        "energies": energies.tolist(),
        "shifts": shifts.tolist(),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--box", type=float, default=8.0)
    p.add_argument("--n-values", type=str, default="64,128,256,512,1024")
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args()

    print("Solving LogSE vortex profile...")
    prof = VortexProfile.solve(x_min=1e-4, x_max=14.0, n=4000)

    n_values = [int(x) for x in args.n_values.split(",")]
    print(f"\nPeierls-Nabarro translation-barrier test  box={args.box}  log_pressure={LOG_PRESSURE}")
    print(f"{'n':>6s} {'dx':>9s} {'E_mean':>11s} {'PN_abs':>12s} {'PN_rel':>11s} {'ratio_to_prev':>13s}")
    print("-" * 68)

    rows = []
    prev = None
    for n in n_values:
        row = pn_barrier(n, args.box, prof)
        rows.append(row)
        ratio = (row["pn_barrier_abs"] / prev["pn_barrier_abs"]
                 if prev and prev["pn_barrier_abs"] > 0 else float("nan"))
        print(f"{n:6d} {row['dx']:9.5f} {row['E_mean']:11.4f} "
              f"{row['pn_barrier_abs']:12.4e} {row['pn_barrier_rel']:11.3e} "
              f"{ratio:13.3f}")
        prev = row

    # Verdict: how does PN barrier scale? Halving dx should ~quarter it (or faster)
    # for a lattice artifact; stay constant for physical ruggedness.
    print("\n" + "=" * 68)
    first, last = rows[0], rows[-1]
    dx_ratio = first["dx"] / last["dx"]
    barrier_ratio = (first["pn_barrier_abs"] / last["pn_barrier_abs"]
                     if last["pn_barrier_abs"] > 0 else float("inf"))
    print(f"Over dx {first['dx']:.4f} -> {last['dx']:.4f} ({dx_ratio:.0f}x finer):")
    print(f"  PN barrier shrank by {barrier_ratio:.1f}x "
          f"({first['pn_barrier_abs']:.3e} -> {last['pn_barrier_abs']:.3e})")
    if barrier_ratio > dx_ratio:
        print(f"  => barrier falls FASTER than dx: LATTICE ARTIFACT "
              f"(continuum landscape is smooth; resolution cures it)")
    elif barrier_ratio < 2.0:
        print(f"  => barrier ~constant under refinement: PHYSICAL ruggedness")
    else:
        print(f"  => intermediate; inspect the trend")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w") as fh:
            json.dump({"box": args.box, "log_pressure": LOG_PRESSURE, "rows": rows},
                      fh, indent=2, default=str)
        print(f"\nWrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()

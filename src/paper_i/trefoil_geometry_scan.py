"""#77 Track 2 follow-up: trefoil geometry (R, a) energy scan.

N_Y x F was computed at a fixed knot geometry (major_radius R=2.8 xi,
minor_radius a=0.85 xi). The physical proton sits at the (R, a) that minimises
the relaxed total LogSE energy. This script scans initial (R, a), relaxes each
with the numba gradient-flow solver, and records:
  - final total energy E (the quantity to minimise)
  - converged N_Y_arc, F, N_Y x F at that geometry

The gradient-flow solver preserves the topological basin (the ring does not
collapse — verified: core mean cylindrical radius tracks the nominal R), so
each initial (R, a) relaxes within its own basin and the final energies are a
meaningful function of (R, a).

Usage:
    python trefoil_geometry_scan.py [--n 96] [--output OUT.json]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from trefoil_breather_static import TrefoilConfig, coordinate_grid
from trefoil_breather_observables import extract, ExtractionConfig
from trefoil_gradient_flow_static import (
    chunked_initial_state,
    run_gradient_flow,
)

# Scan grid (xi units)
R_VALUES = (2.2, 2.5, 2.8, 3.1, 3.4)
A_VALUES = (0.65, 0.85, 1.05)

R_CUTOFF = 1.18  # straight-vortex calibration cutoff for N_Y / F


def relax_geometry(
    major_radius: float,
    minor_radius: float,
    n: int,
    half_width: float,
    max_steps: int,
    alpha: float,
) -> dict:
    cfg = TrefoilConfig(
        n=n,
        half_width=half_width,
        major_radius=major_radius,
        minor_radius=minor_radius,
        log_pressure=0.5,
        frame_samples=100 if n >= 96 else 600,
    )
    psi0 = chunked_initial_state(cfg)
    t0 = time.perf_counter()
    psi, records = run_gradient_flow(
        psi0, cfg,
        lambda_perp=0.0,
        alpha_init=alpha,
        topo_drop_tol=1,
        max_steps=max_steps,
        energy_rtol=1e-7,
        check_interval=10_000,   # silence periodic prints
        save_path=None,
        use_numba=True,
        verbose=False,
    )
    elapsed = time.perf_counter() - t0
    e_final = records[-1].energy if records else float("nan")
    links = records[-1].n_links if records else 0

    # Extract N_Y / F on the converged field
    x, y, z = coordinate_grid(cfg)
    state = {
        "cfg": {
            "n": cfg.n, "half_width": cfg.half_width,
            "major_radius": cfg.major_radius, "minor_radius": cfg.minor_radius,
            "log_pressure": cfg.log_pressure, "frame_samples": cfg.frame_samples,
            "density_floor": cfg.density_floor,
        },
        "psi": psi, "x": x, "y": y, "z": z,
    }
    ec = ExtractionConfig(
        r_tube=1.5, r_cavity=1.5, cal_arc_half_width=0.5,
        anchor_thickness_xi=1.0, straight_vortex_r_max=R_CUTOFF,
    )
    obs = extract(state, ec)

    return {
        "major_radius": major_radius,
        "minor_radius": minor_radius,
        "n": n,
        "e_final": e_final,
        "links": links,
        "n_steps": len(records),
        "n_y_arc": obs.n_y_per_curve_length,
        "f_factor": obs.f_factor_straight_int,
        "n_y_times_f": obs.n_y_times_f_straight,
        "l_curve": obs.l_curve_geometric,
        "elapsed_s": elapsed,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n", type=int, default=96)
    p.add_argument("--half-width", type=float, default=6.0)
    p.add_argument("--max-steps", type=int, default=2000)
    p.add_argument("--alpha", type=float, default=1e-3)
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args()

    print(f"Trefoil geometry scan  n={args.n}  R={R_VALUES}  a={A_VALUES}")
    print(f"{'R':>5s} {'a':>5s} {'E_final':>11s} {'links':>6s} "
          f"{'N_Y_arc':>8s} {'F':>7s} {'N_Y*F':>7s} {'steps':>6s} {'t(s)':>6s}")
    print("-" * 70)

    rows = []
    for R in R_VALUES:
        for a in A_VALUES:
            row = relax_geometry(R, a, args.n, args.half_width, args.max_steps, args.alpha)
            rows.append(row)
            print(f"{R:5.2f} {a:5.2f} {row['e_final']:11.3f} {row['links']:6d} "
                  f"{row['n_y_arc']:8.4f} {row['f_factor']:7.4f} "
                  f"{row['n_y_times_f']:7.3f} {row['n_steps']:6d} {row['elapsed_s']:6.1f}")

    # Minimum-energy geometry
    valid = [r for r in rows if np.isfinite(r["e_final"])]
    best = min(valid, key=lambda r: r["e_final"])
    print("\n" + "=" * 70)
    print(f"Minimum-energy geometry: R={best['major_radius']:.2f} a={best['minor_radius']:.2f}")
    print(f"  E_final = {best['e_final']:.3f}")
    print(f"  N_Y_arc = {best['n_y_arc']:.4f}  F = {best['f_factor']:.4f}  "
          f"N_Y*F = {best['n_y_times_f']:.3f}")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w") as fh:
            json.dump({"rows": rows, "best": best,
                       "R_values": list(R_VALUES), "a_values": list(A_VALUES),
                       "n": args.n}, fh, indent=2, default=str)
        print(f"\nWrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()

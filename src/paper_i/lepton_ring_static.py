"""#78 Task C: singly-wound vortex-ring static minimiser (generations test).

Seeds a singly-wound toroidal vortex ring at a given major radius R, relaxes it
with the #77 numba gradient-flow + topology-guard pipeline (pure LogSE,
lambda_perp = 0), and reports the relaxed total LogSE energy E(R) and the
relaxed ring radius (to detect collapse).

Used to test whether lepton generations are distinct static minima at
R_n ~ 8^n xi: ratio E(8xi)/E(1xi) vs m_mu/m_e = 206.77 (see
route-c-generation-minima-prereg.md).

Usage:
    python lepton_ring_static.py --radii 1.0,8.0 --tube 0.85 --dx 0.125 \
        --max-steps 8000 --output OUT.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from trefoil_breather_static import TrefoilConfig, coordinate_grid, apply_boundary_anchor
from trefoil_gradient_flow_static import (
    _nearest_curve_chunked, normalize_bulk, run_gradient_flow,
)
from gradient_flow_numba import count_links_numba, energy_total_numba


def ring_curve(samples: int, major_radius: float):
    """Planar circle of radius R in the z=0 plane, with Frenet-like frame.

    normal points radially inward/outward (in-plane), binormal is +z, so the
    imprinted phase winds 2*pi around the tube cross-section -> a singly-wound
    vortex ring of circulation 1.
    """
    t = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    x = major_radius * np.cos(t)
    y = major_radius * np.sin(t)
    z = np.zeros_like(t)
    curve = np.stack((x, y, z), axis=1)
    tangent = np.stack((-np.sin(t), np.cos(t), np.zeros_like(t)), axis=1)
    normal = np.stack((np.cos(t), np.sin(t), np.zeros_like(t)), axis=1)   # radial, in-plane
    binormal = np.stack((np.zeros_like(t), np.zeros_like(t), np.ones_like(t)), axis=1)  # +z
    return curve, tangent, normal, binormal


def ring_initial_state(cfg: TrefoilConfig) -> np.ndarray:
    """Singly-wound ring imprint, memory-efficient (chunked nearest-point)."""
    x, y, z = coordinate_grid(cfg)
    points = np.stack((x, y, z), axis=-1)
    curve, _t, normal, binormal = ring_curve(cfg.frame_samples, cfg.major_radius)
    nearest = _nearest_curve_chunked(points, curve)
    nearest_curve = curve[nearest]
    nearest_normal = normal[nearest]
    nearest_binormal = binormal[nearest]
    off = points - nearest_curve
    radial_n = np.sum(off * nearest_normal, axis=-1)
    radial_b = np.sum(off * nearest_binormal, axis=-1)
    distance = np.sqrt(np.maximum(radial_n**2 + radial_b**2, 0.0))
    theta = np.arctan2(radial_b, radial_n)
    amplitude = np.tanh(distance / (math.sqrt(2.0) * cfg.xi))
    phase = np.exp(1j * theta)
    return (amplitude * phase).astype(np.complex128)


def relaxed_ring_radius(psi: np.ndarray, cfg: TrefoilConfig) -> float:
    """Mean cylindrical radius of the depleted core (rho < 0.25)."""
    x, y, z = coordinate_grid(cfg)
    rho = np.abs(psi) ** 2
    core = rho < 0.25
    if core.sum() == 0:
        return 0.0
    r_cyl = np.sqrt(x[core] ** 2 + y[core] ** 2)
    return float(r_cyl.mean())


def run_one(R: float, tube: float, dx: float, max_steps: int, alpha: float) -> dict:
    # box: half-width = R + margin; margin >= 4 xi, rounded so n is even
    half_width = max(6.0, R + 4.0)
    n = int(round(2 * half_width / dx))
    n += n % 2
    half_width = n * dx / 2.0
    frame = max(600, int(8 * n))

    cfg = TrefoilConfig(
        n=n, half_width=half_width, major_radius=R, minor_radius=tube,
        log_pressure=0.5, frame_samples=frame,
    )
    psi0 = ring_initial_state(cfg)
    apply_boundary_anchor(psi0, cfg)
    psi0 = normalize_bulk(psi0, cfg)
    links0 = int(count_links_numba(psi0))
    R0 = relaxed_ring_radius(psi0, cfg)

    t0 = time.perf_counter()
    psi, recs = run_gradient_flow(
        psi0, cfg, lambda_perp=0.0, alpha_init=alpha, topo_drop_tol=1,
        max_steps=max_steps, energy_rtol=1e-7, check_interval=99999,
        use_numba=True, verbose=False,
    )
    elapsed = time.perf_counter() - t0
    E = float(energy_total_numba(psi, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor))
    Rr = relaxed_ring_radius(psi, cfg)
    links = int(count_links_numba(psi))
    return {
        "R_seed": R, "tube": tube, "dx": cfg.grid.spacing, "n": n,
        "half_width": half_width, "frame_samples": frame,
        "E_relaxed": E, "R_relaxed": Rr, "R_initial_core": R0,
        "links_initial": links0, "links_final": links,
        "steps": len(recs), "elapsed_s": elapsed,
        "collapsed": bool(Rr < 4.0 and R >= 6.0),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--radii", type=str, default="1.0,8.0")
    p.add_argument("--tube", type=float, default=0.85)
    p.add_argument("--dx", type=float, default=0.125)
    p.add_argument("--max-steps", type=int, default=8000)
    p.add_argument("--alpha", type=float, default=1e-3)
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args()

    radii = [float(s) for s in args.radii.split(",")]
    print(f"Lepton ring static minimiser  radii={radii}  tube={args.tube}  dx={args.dx}")
    print(f"{'R_seed':>7s} {'n':>4s} {'E_relaxed':>11s} {'R_relaxed':>10s} "
          f"{'links_i':>8s} {'links_f':>8s} {'steps':>6s} {'t(s)':>6s}")
    print("-" * 70)
    rows = []
    for R in radii:
        r = run_one(R, args.tube, args.dx, args.max_steps, args.alpha)
        rows.append(r)
        print(f"{r['R_seed']:7.2f} {r['n']:4d} {r['E_relaxed']:11.4f} "
              f"{r['R_relaxed']:10.3f} {r['links_initial']:8d} {r['links_final']:8d} "
              f"{r['steps']:6d} {r['elapsed_s']:6.1f}")

    # ratio E(8)/E(1) if both present
    by_R = {round(r["R_seed"]): r for r in rows}
    print("\n" + "=" * 60)
    if 8 in by_R and 1 in by_R:
        e8, e1 = by_R[8]["E_relaxed"], by_R[1]["E_relaxed"]
        ratio = e8 / e1 if e1 != 0 else float("nan")
        collapsed8 = by_R[8]["collapsed"]
        print(f"E(8xi)/E(1xi) = {ratio:.2f}")
        print(f"  m_mu/m_e   = 206.77   (PASS band [165,248], suggestive [103,414])")
        print(f"  (3/2)mu0/me= 207.5")
        print(f"  R_relaxed(8xi) = {by_R[8]['R_relaxed']:.2f}  collapsed={collapsed8}")
        if collapsed8:
            verdict = "NULL (8xi ring collapsed - no distinct minimum)"
        elif 165 <= ratio <= 248:
            verdict = "PASS"
        elif 103 <= ratio <= 414:
            verdict = "SUGGESTIVE"
        else:
            verdict = "FAIL"
        print(f"  VERDICT: {verdict}")
    else:
        ratio, verdict = None, "incomplete"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w") as fh:
            json.dump({"rows": rows, "ratio_8_over_1": ratio, "verdict": verdict}, fh, indent=2)
        print(f"\nWrote {args.output}")


if __name__ == "__main__":
    main()

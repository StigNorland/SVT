"""Proton closure gate (iii) probe: relaxer convergence from non-(2,3)-parameterised seeds.

Companion to papers/SSV-I/proton-gate-iii-prereg.md.

Generalises trefoil_curve to take (p, q) winding numbers and a custom
(R_M, r_m) so we can seed the relaxer from:
  REF       (2, 3) at R=2.8, r=0.85  -- reference trefoil
  REPARAM   (3, 2) at R=2.8, r=0.85  -- same topology, alternate parameterisation
  PERTURB   (2, 3) at R=3.0, r=0.70  -- same topology, perturbed geometry
  FIVEKNOT  (2, 5) at R=2.8, r=0.85  -- (2,5) cinquefoil knot
  SEVENKNOT (2, 7) at R=2.8, r=0.85  -- (2,7) torus knot

Each runs the krylov_static relaxer programmatically with the same numeric
parameters as the reference saved state (lambda_perp=2000, penalty_mu=400,
n=24, hw=6) and a fixed max_steps=800 budget. Final state is written to
papers/SSV-I/data/gate-iii-<label>.npz and observables are extracted at
R=1.18 xi for direct comparison to the reference table in the prereg.

Run: python proton_gate_iii_probe.py  (from src/paper_i).
"""
from __future__ import annotations

import json
import math
import sys
import time
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parents[2] / "papers" / "SSV-I" / "data"

# Import the relaxer's pieces. We re-use TrefoilConfig and the relaxer's
# internals, but provide our own seed via a monkey-patched initial_state.
import trefoil_breather_static as tbs
from trefoil_breather_static import TrefoilConfig, coordinate_grid
from trefoil_breather_observables import extract, ExtractionConfig, load_state


def torus_knot_curve(samples: int, major_radius: float, minor_radius: float,
                     p: int, q: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """General (p, q) torus knot.  p windings around the major axis,
    q windings around the minor circle.  Returns (curve, tangent, normal,
    binormal) in the same shape as trefoil_breather_static.trefoil_curve.
    """
    t = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    x = (major_radius + minor_radius * np.cos(q * t)) * np.cos(p * t)
    y = (major_radius + minor_radius * np.cos(q * t)) * np.sin(p * t)
    z = minor_radius * np.sin(q * t)
    curve = np.stack((x, y, z), axis=1)

    dt = 2.0 * math.pi / samples
    tangent = np.gradient(curve, dt, axis=0, edge_order=2)
    tangent = tangent / np.linalg.norm(tangent, axis=1, keepdims=True)

    radial_hint = np.stack((np.cos(p * t), np.sin(p * t), np.zeros_like(t)), axis=1)
    normal = radial_hint - np.sum(radial_hint * tangent, axis=1, keepdims=True) * tangent
    normal_norms = np.linalg.norm(normal, axis=1, keepdims=True)
    normal_norms = np.where(normal_norms < 1e-12, 1.0, normal_norms)
    normal = normal / normal_norms
    binormal = np.cross(tangent, normal)
    bn_norms = np.linalg.norm(binormal, axis=1, keepdims=True)
    bn_norms = np.where(bn_norms < 1e-12, 1.0, bn_norms)
    binormal = binormal / bn_norms
    return curve, tangent, normal, binormal


def make_initial_state(cfg: TrefoilConfig, p: int, q: int) -> np.ndarray:
    """Recreate initial_state(cfg) but with a (p, q) torus knot seed."""
    x, y, z = coordinate_grid(cfg)
    points = np.stack((x, y, z), axis=-1)
    curve, _tangent, normal, binormal = torus_knot_curve(
        cfg.frame_samples, major_radius=cfg.major_radius,
        minor_radius=cfg.minor_radius, p=p, q=q,
    )
    offsets = points[None, ...] - curve[:, None, None, None, :]
    dist_sq = np.sum(offsets * offsets, axis=-1)
    nearest = np.argmin(dist_sq, axis=0)
    nearest_curve = curve[nearest]
    nearest_normal = normal[nearest]
    nearest_binormal = binormal[nearest]
    nearest_offset = points - nearest_curve
    radial_n = np.sum(nearest_offset * nearest_normal, axis=-1)
    radial_b = np.sum(nearest_offset * nearest_binormal, axis=-1)
    distance = np.sqrt(np.maximum(radial_n * radial_n + radial_b * radial_b, 0.0))
    theta = np.arctan2(radial_b, radial_n)
    amplitude = np.tanh(distance / (math.sqrt(2.0) * cfg.xi))
    phase = np.exp(1j * theta)
    radius_sq = x * x + y * y + z * z
    seed = 1.0 - 0.25 * np.exp(-radius_sq / max(cfg.smoothing_radius**2, 1.0e-12))
    psi = amplitude * phase * seed
    return psi.astype(np.complex128)


def relax(label: str, p: int, q: int, major_radius: float, minor_radius: float,
          n: int = 24, half_width: float = 6.0,
          lambda_perp: float = 2000.0, penalty_mu: float = 400.0,
          max_steps: int = 800) -> dict:
    """Run the krylov_static relaxer programmatically with the (p,q) seed."""
    # Build a TrefoilConfig matching the saved-state convention
    cfg = TrefoilConfig(
        n=n, half_width=half_width, xi=1.0, major_radius=major_radius,
        minor_radius=minor_radius, smoothing_radius=0.2, log_pressure=0.5,
    )
    # Monkey-patch initial_state to produce our custom (p, q) seed.
    original_initial_state = tbs.initial_state
    tbs.initial_state = lambda c: make_initial_state(c, p=p, q=q)
    try:
        # Drive the relaxer through its main() entry, with CLI-emulated argv.
        import trefoil_breather_lperp_krylov_static as relaxer
        out_path = DATA_DIR / f"gate-iii-{label}.npz"
        argv_backup = sys.argv
        sys.argv = [
            "trefoil_breather_lperp_krylov_static.py",
            "--n", str(n),
            "--half-width", str(half_width),
            "--major-radius", str(major_radius),
            "--minor-radius", str(minor_radius),
            "--lambda-perp", str(lambda_perp),
            "--penalty-mu", str(penalty_mu),
            "--max-steps", str(max_steps),
            "--check-interval", "50",
            "--output", str(out_path),
        ]
        t0 = time.time()
        try:
            relaxer.main()
        finally:
            sys.argv = argv_backup
        dt = time.time() - t0
    finally:
        tbs.initial_state = original_initial_state

    # Load the saved state and extract observables at R=1.18.
    state = load_state(out_path)
    ec = ExtractionConfig(r_tube=1.5, r_cavity=1.5, cal_arc_half_width=0.5,
                          anchor_thickness_xi=1.0, straight_vortex_r_max=1.18)
    s = extract(state, ec)
    return {
        "label": label,
        "(p,q)": (p, q),
        "R_M": major_radius,
        "r_m": minor_radius,
        "wall_time_s": dt,
        "out_path": str(out_path),
        "final_energy_full": float(s.e_total_raw),
        "e_interior": float(s.e_interior),
        "mu_0_str_1p18": float(s.mu_0_straight),
        "F_str_1p18": float(s.f_factor_straight_int),
        "n_y_str_1p18": float(s.n_y_straight),
        "n_y_x_F_1p18": float(s.n_y_times_f_straight),
        "min_density": float(s.min_density),
    }


SEEDS = [
    ("REF",       2, 3, 2.8, 0.85),
    ("REPARAM",   3, 2, 2.8, 0.85),
    ("PERTURB",   2, 3, 3.0, 0.70),
    ("FIVEKNOT",  2, 5, 2.8, 0.85),
    ("SEVENKNOT", 2, 7, 2.8, 0.85),
]


def main() -> None:
    print("=== Proton gate (iii) probe ===")
    print(f"5 seeds at n=24, hw=6, lambda_perp=2000, penalty_mu=400, max_steps=800")
    print()
    results = []
    for label, p, q, R, r in SEEDS:
        print(f"--- {label}: (p,q)=({p},{q}), R_M={R}, r_m={r} ---")
        try:
            res = relax(label, p, q, R, r)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
        print(f"  wall time: {res['wall_time_s']:.0f} s")
        print(f"  final_energy_full = {res['final_energy_full']:.3f}")
        print(f"  F(R=1.18)         = {res['F_str_1p18']:.4f}")
        print(f"  n_y_str(R=1.18)   = {res['n_y_str_1p18']:.4f}")
        print(f"  mu_0_str(R=1.18)  = {res['mu_0_str_1p18']:.4f}")
        print(f"  min_density       = {res['min_density']:.4g}")
        results.append(res)
        print()

    # Cross-seed summary table
    print("\n=== Cross-seed table ===")
    cols = ["label", "(p,q)", "final_energy_full", "F_str_1p18",
            "n_y_str_1p18", "n_y_x_F_1p18", "min_density"]
    print("  ".join(f"{c:>20s}" for c in cols))
    for r in results:
        row = [str(r["label"]), str(r["(p,q)"]),
               f"{r['final_energy_full']:.3f}", f"{r['F_str_1p18']:.4f}",
               f"{r['n_y_str_1p18']:.4f}", f"{r['n_y_x_F_1p18']:.4f}",
               f"{r['min_density']:.4g}"]
        print("  ".join(f"{v:>20s}" for v in row))

    # iii-a verdict on REF, REPARAM, PERTURB
    print("\n=== Gate (iii-a) decision: REF vs REPARAM vs PERTURB ===")
    a_results = [r for r in results if r["label"] in ("REF", "REPARAM", "PERTURB")]
    if len(a_results) == 3:
        energies = [r["final_energy_full"] for r in a_results]
        Fs = [r["F_str_1p18"] for r in a_results]
        e_spread = 100 * (max(energies) - min(energies)) / np.mean(energies)
        f_spread = 100 * (max(Fs) - min(Fs)) / np.mean(Fs)
        print(f"  energy spread: {e_spread:.1f}%   F spread: {f_spread:.1f}%")
        if e_spread < 5 and f_spread < 5:
            print("  PASS-A: all three within 5% on both energy and F")
        elif e_spread > 10 or f_spread > 10:
            print("  FAIL-A: at least one spread > 10%")
        else:
            print("  AMBIGUOUS-A: 5-10% spread")
    else:
        print(f"  insufficient runs ({len(a_results)}/3) -- cannot decide")


if __name__ == "__main__":
    main()

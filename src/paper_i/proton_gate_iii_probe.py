"""Proton closure gate (iii-a) probe: same-topology basin of attraction.

Companion to papers/SSV-I/proton-gate-iii-prereg.md (scope reduced to iii-a
per the 2026-05-30 decision: REF, REPARAM, PERTURB only).

Tests whether the relaxer converges to the same final state when seeded from
different parameterisations / perturbations of the SAME trefoil topology:
  REF      (2,3) at R=2.8, r=0.85   -- reference trefoil
  REPARAM  (3,2) at R=2.8, r=0.85   -- same knot, alternate parameterisation
  PERTURB  (2,3) at R=3.0, r=0.70   -- same knot, perturbed geometry

v2 fixes (v1 was invalid -- see papers/SSV-I/proton-gate-iii-bug-note.md):
  - BUG 1: the relaxer does `from trefoil_breather_static import initial_state`,
    so it binds its OWN module-level name. Patching tbs.initial_state never
    reached it -> all seeds silently used the default (2,3) trefoil. Fix:
    patch relaxer.initial_state (the load-bearing name) AND tbs.initial_state.
  - BUG 2: readback used the shared load_state which choked; this probe uses a
    local allow_pickle=False reader with the confirmed key mapping
    (psi = psi_real + i psi_imag; config is a JSON string member).
  - Output mangling guard: all results are written to a JSON artifact
    (gate-iii-results.json) rather than relied on via stdout.
  - Seed-difference guard: records each seed's initial deficit signature and
    the relaxer's initial_vortex_links so a silent "all seeds identical"
    failure cannot recur undetected.

Run: python proton_gate_iii_probe.py  (from src/paper_i).
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parents[2] / "papers" / "SSV-I" / "data"
RESULTS_JSON = DATA_DIR / "gate-iii-results.json"

import trefoil_breather_static as tbs
from trefoil_breather_static import TrefoilConfig, coordinate_grid
from trefoil_breather_observables import extract, ExtractionConfig
import trefoil_breather_lperp_krylov_static as relaxer


def load_state_local(path: Path) -> dict:
    """allow_pickle=False reader matching the krylov npz format, returning the
    dict shape that trefoil_breather_observables.extract() expects."""
    d = np.load(path, allow_pickle=False)
    cfg_raw = d["config"].item() if d["config"].ndim == 0 else str(d["config"])
    if isinstance(cfg_raw, bytes):
        cfg_raw = cfg_raw.decode("utf-8")
    cfg = json.loads(cfg_raw)
    psi = (d["psi_real"] + 1j * d["psi_imag"]).astype(np.complex128)
    return {
        "cfg": cfg,
        "psi": psi,
        "x": np.asarray(d["x"], dtype=float),
        "y": np.asarray(d["y"], dtype=float),
        "z": np.asarray(d["z"], dtype=float),
    }


def torus_knot_curve(samples, major_radius, minor_radius, p, q):
    """General (p, q) torus knot. p windings around the major axis, q around
    the minor circle. Same return shape as trefoil_breather_static.trefoil_curve."""
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
    nn = np.linalg.norm(normal, axis=1, keepdims=True)
    normal = normal / np.where(nn < 1e-12, 1.0, nn)
    binormal = np.cross(tangent, normal)
    bn = np.linalg.norm(binormal, axis=1, keepdims=True)
    binormal = binormal / np.where(bn < 1e-12, 1.0, bn)
    return curve, tangent, normal, binormal


def make_initial_state(cfg, p, q):
    """Recreate trefoil_breather_static.initial_state(cfg) with a (p,q) seed."""
    x, y, z = coordinate_grid(cfg)
    points = np.stack((x, y, z), axis=-1)
    curve, _t, normal, binormal = torus_knot_curve(
        cfg.frame_samples, cfg.major_radius, cfg.minor_radius, p, q)
    offsets = points[None, ...] - curve[:, None, None, None, :]
    nearest = np.argmin(np.sum(offsets * offsets, axis=-1), axis=0)
    nearest_offset = points - curve[nearest]
    radial_n = np.sum(nearest_offset * normal[nearest], axis=-1)
    radial_b = np.sum(nearest_offset * binormal[nearest], axis=-1)
    distance = np.sqrt(np.maximum(radial_n**2 + radial_b**2, 0.0))
    theta = np.arctan2(radial_b, radial_n)
    amplitude = np.tanh(distance / (math.sqrt(2.0) * cfg.xi))
    phase = np.exp(1j * theta)
    radius_sq = x * x + y * y + z * z
    seed = 1.0 - 0.25 * np.exp(-radius_sq / max(cfg.smoothing_radius**2, 1e-12))
    return (amplitude * phase * seed).astype(np.complex128)


def seed_signature(cfg, p, q):
    """Cheap fingerprint of the seed so we can PROVE seeds differ."""
    psi = make_initial_state(cfg, p, q)
    rho = np.abs(psi) ** 2
    return {
        "deficit_sum": float(np.sum(np.maximum(0.0, 1.0 - rho))),
        "min_rho": float(rho.min()),
    }


def relax(label, p, q, major_radius, minor_radius,
          n=24, half_width=6.0, lambda_perp=2000.0, penalty_mu=400.0, max_steps=800):
    cfg = TrefoilConfig(n=n, half_width=half_width, xi=1.0,
                        major_radius=major_radius, minor_radius=minor_radius,
                        smoothing_radius=0.2, log_pressure=0.5)
    sig = seed_signature(cfg, p, q)

    seed_fn = lambda c: make_initial_state(c, p, q)
    orig_relaxer = relaxer.initial_state
    orig_tbs = tbs.initial_state
    relaxer.initial_state = seed_fn      # load-bearing patch
    tbs.initial_state = seed_fn
    # IMPORTANT: --save-state writes the npz field; --output writes the JSON
    # summary. v1/v2 mistakenly passed the npz path to --output (which writes
    # JSON text), so the "npz" started with '{' and could not be loaded. Use
    # --save-state for the field, --output for a separate summary JSON.
    state_path = DATA_DIR / f"gate-iii-{label}.npz"
    summary_path = DATA_DIR / f"gate-iii-{label}-summary.json"
    out_path = state_path
    try:
        argv_backup = sys.argv
        sys.argv = [
            "trefoil_breather_lperp_krylov_static.py",
            "--n", str(n), "--half-width", str(half_width),
            "--major-radius", str(major_radius), "--minor-radius", str(minor_radius),
            "--lambda-perp", str(lambda_perp), "--penalty-mu", str(penalty_mu),
            "--max-steps", str(max_steps), "--check-interval", "50",
            "--save-state", str(state_path),
            "--output", str(summary_path),
        ]
        t0 = time.time()
        try:
            relaxer.main()
        finally:
            sys.argv = argv_backup
        dt = time.time() - t0
    finally:
        relaxer.initial_state = orig_relaxer
        tbs.initial_state = orig_tbs

    state = load_state_local(out_path)
    ec = ExtractionConfig(r_tube=1.5, r_cavity=1.5, cal_arc_half_width=0.5,
                          anchor_thickness_xi=1.0, straight_vortex_r_max=1.18)
    s = extract(state, ec)
    return {
        "label": label, "p": p, "q": q, "R_M": major_radius, "r_m": minor_radius,
        "wall_time_s": round(dt, 1),
        "seed_deficit_sum": round(sig["deficit_sum"], 4),
        "seed_min_rho": sig["min_rho"],
        "final_energy_full": round(float(s.e_total_raw), 4),
        "e_interior": round(float(s.e_interior), 4),
        "mu_0_str_1p18": round(float(s.mu_0_straight), 6),
        "F_str_1p18": round(float(s.f_factor_straight_int), 4),
        "n_y_str_1p18": round(float(s.n_y_straight), 4),
        "min_density": float(s.min_density),
    }


SEEDS = [
    ("REF", 2, 3, 2.8, 0.85),
    ("REPARAM", 3, 2, 2.8, 0.85),
    ("PERTURB", 2, 3, 3.0, 0.70),
]


def main():
    results = []
    for label, p, q, R, r in SEEDS:
        print(f"relaxing {label} (p,q)=({p},{q}) R={R} r={r} ...", flush=True)
        results.append(relax(label, p, q, R, r))

    # seed-difference guard
    sigs = [(r["label"], r["seed_deficit_sum"]) for r in results]
    distinct_seeds = len({s for _, s in sigs}) == len(sigs)

    energies = [r["final_energy_full"] for r in results]
    Fs = [r["F_str_1p18"] for r in results]
    e_spread = 100 * (max(energies) - min(energies)) / (sum(energies) / len(energies))
    f_spread = 100 * (max(Fs) - min(Fs)) / (sum(Fs) / len(Fs))

    if e_spread < 5 and f_spread < 5:
        verdict = "PASS-A"
    elif e_spread > 10 or f_spread > 10:
        verdict = "FAIL-A"
    else:
        verdict = "AMBIGUOUS-A"

    payload = {
        "scope": "iii-a (REF, REPARAM, PERTURB)",
        "params": {"n": 24, "hw": 6.0, "lambda_perp": 2000.0,
                   "penalty_mu": 400.0, "max_steps": 800},
        "seed_signatures": sigs,
        "distinct_seeds": distinct_seeds,
        "results": results,
        "energy_spread_pct": round(e_spread, 2),
        "F_spread_pct": round(f_spread, 2),
        "verdict": verdict,
    }
    RESULTS_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {RESULTS_JSON}")
    print(f"distinct_seeds={distinct_seeds}  e_spread={e_spread:.2f}%  "
          f"f_spread={f_spread:.2f}%  verdict={verdict}")


if __name__ == "__main__":
    main()

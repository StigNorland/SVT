"""Muon Stage 3 (revised) probe: radial-window sweep test of the thin-ring
hypothesis for the hw-drift.

Companion to papers/SSV-I/muon-stage3-diagnostic-prereg.md.

Sweeps the smooth-window radius r_w at fixed hw=8 on the
selection-rule-fixed L+L_perp BdG operator. If the lowest Kelvin Nambu
eigenfrequency plateaus near 0.207 over a range of small r_w (the
thin-ring region) and monotonically drifts to ~0.11 only as r_w opens
toward the outer region, the Stage 2 hw-drift is the expected
finite-alpha breakdown of the thin-ring approximation, and the operator
is correctly implemented.

Both smooth and hard windows are swept to ensure the result is not a
property of the window shape.

Run: python muon_stage3_radial_window_probe.py  (from instruments/paper_i).
~10 spectrum solves per window type, ~minutes each.
"""
from __future__ import annotations

import math
import time

import numpy as np

from kelvin_augmented_bdg import build_bdg, build_modes
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


# Fixed parameters across all runs.
N = 41
HW = 8.0
PROFILE_N = 1600
LAMBDA_PERP = math.pi / 4.0
KELVIN_PHI_N = 1024
KELVIN_CORE_RADIUS = 1.0
WINDOW_TAPER = 0.5
STABLE_TOL = 1.0e-5

R_W_POINTS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]


def lowest_kelvin_mode(window_kind: str, r_w: float) -> tuple[float, str, dict]:
    """Solve the fixed-operator BdG spectrum with the given window cutoff,
    return the lowest Kelvin Nambu eigenfrequency, its dominant-sector tag,
    and a small dict of sector weights for the dominant mode.
    """
    cfg = ProjectionConfig(
        n=N, half_width=HW, profile="numerical", profile_n=PROFILE_N,
        chi_parity="sin",
        projection_window=window_kind,
        window_radius=r_w,
        window_taper=(WINDOW_TAPER if window_kind == "smooth" else 0.0),
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=False, kelvin_seed="helicity")
    Nm = len(modes)
    by_m = {0: [], 1: [], -1: []}
    for i, m in enumerate(modes):
        by_m.setdefault(m.m_phi, []).append(i)
    h = build_bdg(
        bg, modes, cfg, "profile-logse", chiral_mix=0.0, bridge_model="shape",
        lambda_perp=LAMBDA_PERP, kelvin_dispersion="self-induction",
        kelvin_phi_n=KELVIN_PHI_N, kelvin_core_radius=KELVIN_CORE_RADIUS,
    )
    H = np.array(h, dtype=complex)
    eigvals, eigvecs = np.linalg.eig(H)
    stable_idx = sorted(
        (k for k, lam in enumerate(eigvals)
         if lam.real > 1e-5 and abs(lam.imag) <= STABLE_TOL),
        key=lambda k: eigvals[k].real,
    )
    deduped = []
    for k in stable_idx:
        if not deduped or abs(eigvals[k].real - eigvals[deduped[-1]].real) > 1e-4:
            deduped.append(k)
    # Find lowest Kelvin-dominated mode (m=0 amplitude < m=+/-1 amplitude)
    for k in deduped:
        lam = eigvals[k].real
        v = eigvecs[:, k]
        v = v / np.linalg.norm(v)
        u = v[:Nm]
        u_m0 = float(np.sqrt(sum(abs(u[i])**2 for i in by_m[0])))
        u_mp = float(np.sqrt(sum(abs(u[i])**2 for i in by_m[+1])))
        u_mm = float(np.sqrt(sum(abs(u[i])**2 for i in by_m[-1])))
        wts = {"m=0": u_m0**2, "m=+1": u_mp**2, "m=-1": u_mm**2}
        dom = max(wts, key=wts.get)
        if dom != "m=0":
            return lam, dom, {"m=0": u_m0, "m=+1": u_mp, "m=-1": u_mm}
    return float("nan"), "no-Kelvin", {}


def main() -> None:
    t0 = time.time()
    print("=== Stage 3 radial-window probe ===")
    print(f"fixed: n={N}, hw={HW}, lambda_perp=pi/4, helicity 2-core basis")
    print(f"sweep: window_radius r_w in {R_W_POINTS}")
    print()

    for kind in ("smooth", "hard"):
        print(f"## {kind.upper()} window")
        print(f"  {'r_w':>5s}  {'omega':>10s}  {'sector':>6s}  | u(m=0) u(m=+1) u(m=-1)")
        results = []
        for r_w in R_W_POINTS:
            t = time.time()
            lam, dom, wts = lowest_kelvin_mode(kind, r_w)
            dt = time.time() - t
            results.append((r_w, lam, dom, wts))
            u_m0 = wts.get("m=0", 0.0)
            u_mp = wts.get("m=+1", 0.0)
            u_mm = wts.get("m=-1", 0.0)
            print(f"  {r_w:5.2f}  {lam:10.4f}  {dom:>6s}  |  {u_m0:.3f}   {u_mp:.3f}   {u_mm:.3f}   ({dt:.0f}s)")
        # quick on-the-fly verdict hints
        omegas = [r[1] for r in results if not math.isnan(r[1])]
        if omegas:
            near_207 = [(r[0], r[1]) for r in results
                        if not math.isnan(r[1]) and abs(r[1] - 0.207) / 0.207 <= 0.05]
            if near_207:
                radii = [p[0] for p in near_207]
                print(f"\n  POINTS WITHIN 5% OF 0.207: r_w in {radii}")
            else:
                print("\n  (no points within 5% of 0.207)")
        print()

    print(f"=== total time: {time.time()-t0:.1f}s ===")


if __name__ == "__main__":
    main()

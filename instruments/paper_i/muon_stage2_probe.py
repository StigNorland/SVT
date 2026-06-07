"""Muon Stage 2 probe: basis convergence of the fixed operator.

Companion to papers/SSV-I/muon-stage2-prereg.md.

Runs three pre-registered sweeps on the selection-rule-correct operator
(Stage 1):
  - n-sweep:     n in {31, 41, 51, 61}      at hw=5, helicity basis
  - hw-sweep:    hw in {4, 5, 6, 7, 8}      at n=41, helicity basis
  - basis-sweep: 4 basis choices            at n=41, hw=5

At each point: full spectrum, eigenvector sector decomposition of the two
lowest Kelvin Nambu modes (per Stage 1 finding), and tracking of how they
move.

Run: python muon_stage2_probe.py  (from instruments/paper_i). Slow -- a few minutes
per spectrum solve, ~15 minutes total at the n-sweep top end.
"""
from __future__ import annotations

import math
import time

import numpy as np

from kelvin_augmented_bdg import build_bdg, build_modes
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


def run_one(n: int, half_width: float, core_four: bool, kelvin_seed: str,
            profile_n: int = 1600, lambda_perp: float = math.pi / 4.0,
            kelvin_phi_n: int = 1024, kelvin_core_radius: float = 1.0,
            stable_tol: float = 1e-5) -> dict:
    """Build the BdG matrix at the given parameters, diagonalise, and return:
        - distinct stable positive eigenvalues
        - sector-decomposed identification of the two lowest Kelvin Nambu modes
    """
    cfg = ProjectionConfig(
        n=n, half_width=half_width, profile="numerical",
        profile_n=profile_n, chi_parity="sin",
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=core_four, kelvin_seed=kelvin_seed)
    Nm = len(modes)
    by_m = {0: [], 1: [], -1: []}
    for i, m in enumerate(modes):
        by_m.setdefault(m.m_phi, []).append(i)

    h = build_bdg(
        bg, modes, cfg, "profile-logse", chiral_mix=0.0, bridge_model="shape",
        lambda_perp=lambda_perp, kelvin_dispersion="self-induction",
        kelvin_phi_n=kelvin_phi_n, kelvin_core_radius=kelvin_core_radius,
    )
    H = np.array(h, dtype=complex)
    eigvals, eigvecs = np.linalg.eig(H)
    stable_idx = [
        k for k, lam in enumerate(eigvals)
        if lam.real > 1e-5 and abs(lam.imag) <= stable_tol
    ]
    stable_idx.sort(key=lambda k: eigvals[k].real)
    deduped_idx = []
    for k in stable_idx:
        if not deduped_idx or abs(eigvals[k].real - eigvals[deduped_idx[-1]].real) > 1e-4:
            deduped_idx.append(k)

    # For each distinct stable mode, sector-decompose
    def sec_wt_u(v, idxs):
        u = v[:Nm]
        return float(np.sqrt(sum(abs(u[i])**2 for i in idxs)))

    rows = []
    for k in deduped_idx:
        lam = eigvals[k].real
        v = eigvecs[:, k]
        v = v / np.linalg.norm(v)
        u_m0 = sec_wt_u(v, by_m.get(0, []))
        u_mp = sec_wt_u(v, by_m.get(+1, []))
        u_mm = sec_wt_u(v, by_m.get(-1, []))
        # Dominant sector by u-weight
        wts = {"m=0": u_m0**2, "m=+1": u_mp**2, "m=-1": u_mm**2}
        dom = max(wts, key=wts.get)
        rows.append((lam, dom, u_m0, u_mp, u_mm))

    return {"n_modes": Nm, "rows": rows}


def print_table(title, sweep_axis, points, get_label, results):
    print(f"\n## {title}")
    print(f"  {sweep_axis:>6s}  | {'lo Kelvin':>10s} {'sector':>6s} | {'up Kelvin':>10s} {'sector':>6s} | other low modes")
    for pt, res in zip(points, results):
        # Find first two Kelvin (non-m=0-dominant) modes
        kelvin_rows = [(lam, dom, u_m0, u_mp, u_mm)
                       for (lam, dom, u_m0, u_mp, u_mm) in res["rows"]
                       if dom != "m=0"]
        if len(kelvin_rows) >= 2:
            lo_lam, lo_dom = kelvin_rows[0][0], kelvin_rows[0][1]
            up_lam, up_dom = kelvin_rows[1][0], kelvin_rows[1][1]
        elif len(kelvin_rows) == 1:
            lo_lam, lo_dom = kelvin_rows[0][0], kelvin_rows[0][1]
            up_lam, up_dom = float("nan"), "absent"
        else:
            lo_lam, lo_dom = float("nan"), "absent"
            up_lam, up_dom = float("nan"), "absent"
        m0_rows = [(lam, dom) for (lam, dom, *_) in res["rows"] if dom == "m=0"]
        m0_str = ", ".join(f"{lam:.3f}" for lam, _ in m0_rows[:3])
        print(f"  {get_label(pt):>6s}  | {lo_lam:10.4f} {lo_dom:>6s} | {up_lam:10.4f} {up_dom:>6s} | m=0: [{m0_str}]")


def main() -> None:
    t0 = time.time()

    print("=== Stage 2: convergence sweeps on the fixed operator ===")
    print(f"reference: lambda_perp = pi/4, kelvin_dispersion=self-induction")

    # n-sweep
    n_points = [31, 41, 51, 61]
    n_results = []
    for n in n_points:
        print(f"\n[n-sweep] n={n} hw=5 ...", flush=True)
        t = time.time()
        res = run_one(n=n, half_width=5.0, core_four=False, kelvin_seed="helicity")
        print(f"  done in {time.time()-t:.1f}s  ({res['n_modes']} basis modes, {len(res['rows'])} distinct stable)")
        n_results.append(res)
    print_table("n-sweep (hw=5, helicity, 2-core)", "n", n_points, lambda n: str(n), n_results)

    # hw-sweep
    hw_points = [4.0, 5.0, 6.0, 7.0, 8.0]
    hw_results = []
    for hw in hw_points:
        print(f"\n[hw-sweep] n=41 hw={hw} ...", flush=True)
        t = time.time()
        res = run_one(n=41, half_width=hw, core_four=False, kelvin_seed="helicity")
        print(f"  done in {time.time()-t:.1f}s")
        hw_results.append(res)
    print_table("hw-sweep (n=41, helicity, 2-core)", "hw", hw_points, lambda hw: f"{hw:.0f}", hw_results)

    # basis-sweep
    bases = [
        (False, "helicity", "hel-2c"),
        (True, "helicity", "hel-4c"),
        (False, "combined", "comb-2c"),
        (True, "core_enriched", "ce-4c"),
    ]
    b_results = []
    for core_four, seed, label in bases:
        print(f"\n[basis-sweep] {label} ...", flush=True)
        t = time.time()
        res = run_one(n=41, half_width=5.0, core_four=core_four, kelvin_seed=seed)
        print(f"  done in {time.time()-t:.1f}s ({res['n_modes']} basis modes)")
        b_results.append(res)
    print_table("basis-sweep (n=41, hw=5)", "basis", bases, lambda b: b[2], b_results)

    print(f"\n=== total time: {time.time()-t0:.1f}s ===")


if __name__ == "__main__":
    main()

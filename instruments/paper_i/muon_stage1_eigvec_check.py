"""Stage 1 sanity check: eigenvector sector decomposition of the two low modes.

For each eigenvalue of the fixed BdG matrix at the Stage 1 reference point,
project the Nambu eigenvector (u_0, ..., u_5, v_0, ..., v_5) onto the three
m_phi sub-sectors of the 6-mode helicity basis:

  m_phi = 0:  modes 0 (R), 1 (chi)
  m_phi = +1: modes 2 (K_helicity_plus_plus), 4 (K_helicity_plus_minus)
  m_phi = -1: modes 3 (K_helicity_minus_plus), 5 (K_helicity_minus_minus)

Report each eigenvalue's (u, v) sector weights so we can see whether the
0.214 and 0.153 modes are pure-sector or mixed.

Run: python muon_stage1_eigvec_check.py
"""
from __future__ import annotations

import math

import numpy as np

from kelvin_augmented_bdg import build_bdg, build_modes
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


def main() -> None:
    cfg = ProjectionConfig(
        n=41, half_width=5.0, profile="numerical", profile_n=1600, chi_parity="sin",
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=False, kelvin_seed="helicity")
    N = len(modes)
    print(f"basis ({N} modes):")
    for i, m in enumerate(modes):
        print(f"  [{i}] {m.name}  m_phi={m.m_phi:+d}")
    print()

    # Sector index sets (modes with given m_phi)
    by_m = {0: [], 1: [], -1: []}
    for i, m in enumerate(modes):
        by_m[m.m_phi].append(i)
    print(f"sectors: m=0 -> {by_m[0]}, m=+1 -> {by_m[+1]}, m=-1 -> {by_m[-1]}")
    print()

    h = build_bdg(
        bg, modes, cfg, "profile-logse", chiral_mix=0.0, bridge_model="shape",
        lambda_perp=math.pi / 4.0, kelvin_dispersion="self-induction",
        kelvin_phi_n=1024, kelvin_core_radius=1.0,
    )
    H = np.array(h, dtype=complex)
    eigvals, eigvecs = np.linalg.eig(H)
    # eigvecs[:, k] is the k-th eigenvector

    # Filter to positive-real, near-real eigenvalues (matches the stable
    # criterion used in muon_stage1_probe.py)
    stable_idx = [
        k for k, lam in enumerate(eigvals)
        if lam.real > 1e-5 and abs(lam.imag) <= 1e-5
    ]
    # Sort by ascending Re(lambda)
    stable_idx.sort(key=lambda k: eigvals[k].real)
    # Dedup near-degenerate (separated by < 1e-4)
    deduped = []
    for k in stable_idx:
        if not deduped or abs(eigvals[k].real - eigvals[deduped[-1]].real) > 1e-4:
            deduped.append(k)

    print(f"--- {len(deduped)} distinct stable positive eigenvalues ---")
    print(f"{'omega':>10s}  {'u(m=0)':>10s} {'u(m=+1)':>10s} {'u(m=-1)':>10s}  | {'v(m=0)':>10s} {'v(m=+1)':>10s} {'v(m=-1)':>10s}  | dom sector")
    for k in deduped:
        lam = eigvals[k].real
        v = eigvecs[:, k]
        # Eigenvector layout: u-block = v[0:N], v-block = v[N:2N]
        u_block = v[:N]
        v_block = v[N:]
        # Normalise to unit total amplitude for fractions
        total = np.linalg.norm(v)
        u_block /= total
        v_block /= total
        def sec_wt(arr, idxs):
            return float(np.sqrt(sum(abs(arr[i])**2 for i in idxs)))
        u_m0  = sec_wt(u_block, by_m[0])
        u_mp  = sec_wt(u_block, by_m[+1])
        u_mm  = sec_wt(u_block, by_m[-1])
        v_m0  = sec_wt(v_block, by_m[0])
        v_mp  = sec_wt(v_block, by_m[+1])
        v_mm  = sec_wt(v_block, by_m[-1])
        # Identify dominant sector
        wts = {"m=0": u_m0**2 + v_m0**2,
               "m=+1": u_mp**2 + v_mp**2,
               "m=-1": u_mm**2 + v_mm**2}
        dom = max(wts, key=wts.get)
        dom_frac = wts[dom] / sum(wts.values())
        print(f"  {lam:.4f}  {u_m0:10.4f} {u_mp:10.4f} {u_mm:10.4f}  | {v_m0:10.4f} {v_mp:10.4f} {v_mm:10.4f}  | {dom} ({dom_frac:.0%})")


if __name__ == "__main__":
    main()

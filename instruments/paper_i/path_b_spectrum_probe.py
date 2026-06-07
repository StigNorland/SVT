"""Path B basis-robustness probe (papers/SSV-I/path-b-eigenvalue-result.md).

Tests whether the committed L+L_perp toroidal-breather BdG spectrum produces the
muon rung (3/2, omega/omega_c ~ 0.207) AND the pion rung (2, ~0.276) as genuine
stable eigenmodes, across several basis sizes. No tuning: lambda_perp = pi/4 is
the claimed parameter-free coupling; every other knob is the committed default.

Result: the muon mode is basis-robust (0.2148 in every basis); the pion window
is empty in every basis. See the result note for the full discussion.

Run: python path_b_spectrum_probe.py   (from src/paper_i)
"""
from __future__ import annotations

import math

from kelvin_augmented_bdg import build_bdg, build_modes, dense_eigenvalues
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig

# Ladder ruler = 0.138 (NOT fed to the operator; only used to classify output).
# Inlined deliberately so this Path B reproduction does not depend on the
# quarantined muon_mode_prototype.SSVScales (the 0.207 muon-target back-solver).
# 0.138 = (2/3) * 0.207, the muon-derived half-integer rung spacing.
MUON_RATIO_DRAFT = 0.207
MU0 = (2.0 / 3.0) * MUON_RATIO_DRAFT
MUON_WIN = (0.197, 0.217)  # +-5% of 0.207
PION_WIN = (0.262, 0.290)  # +-5% of 0.276


def stable_spectrum(core_four: bool, seed: str, n: int = 41, half_width: float = 5.0,
                    profile_n: int = 1600, kelvin_phi_n: int = 512) -> list[float]:
    cfg = ProjectionConfig(n=n, half_width=half_width, profile="numerical",
                           profile_n=profile_n, chi_parity="sin")
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=core_four, kelvin_seed=seed)
    h = build_bdg(bg, modes, cfg, "profile-logse", chiral_mix=0.0, bridge_model="shape",
                  lambda_perp=math.pi / 4.0, kelvin_dispersion="self-induction",
                  kelvin_phi_n=kelvin_phi_n, kelvin_core_radius=1.0)
    eigs, _ = dense_eigenvalues(h)
    st = sorted(v.real for v in eigs if v.real > 1.0e-5 and abs(v.imag) <= 1.0e-5)
    out: list[float] = []
    for w in st:
        if not out or abs(w - out[-1]) > 1.0e-4:  # collapse near-degenerate pairs
            out.append(w)
    return out


def in_window(spectrum: list[float], window: tuple[float, float]) -> list[float]:
    lo, hi = window
    return [round(w, 4) for w in spectrum if lo <= w <= hi]


def main() -> None:
    print(f"mu0 ruler = {MU0:.4f}  muon target 0.207 (rung 3/2)  pion target 0.276 (rung 2)")
    for core_four, seed in [(False, "helicity"), (True, "helicity"),
                            (False, "combined"), (True, "core_enriched")]:
        spec = stable_spectrum(core_four, seed)
        muon = in_window(spec, MUON_WIN)
        pion = in_window(spec, PION_WIN)
        rungs = [round(w / MU0, 2) for w in spec]
        print(f"core_four={core_four!s:5} seed={seed:13} n_modes_spec={len(spec)} "
              f"MUON={muon} PION={pion} rungs={rungs}")


if __name__ == "__main__":
    main()

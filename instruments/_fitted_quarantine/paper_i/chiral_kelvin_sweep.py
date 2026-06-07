from __future__ import annotations

import argparse
import math

from kelvin_augmented_bdg import build_bdg, build_modes
from muon_mode_prototype import SSVScales
from restricted_bdg_matrix import build_background
from direct_bdg_projection import qr_eigenvalues
from toroidal_projection_integrals import ProjectionConfig


def extract_hybrid(eigs: list[complex], lower: float, upper: float) -> float | None:
    candidates = []
    for value in eigs:
        magnitude = abs(value)
        if lower <= magnitude <= upper:
            candidates.append(magnitude)
    if not candidates:
        return None
    target = SSVScales().muon_ratio_draft
    return min(candidates, key=lambda x: abs(x - target))


def run_point(cfg: ProjectionConfig, chiral_mix: float, lower: float, upper: float) -> tuple[float, float | None]:
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=False, kelvin_seed="displacement")
    h = build_bdg(bg, modes, cfg, "profile-logse", chiral_mix=chiral_mix)
    eigs = qr_eigenvalues(h)
    return chiral_mix, extract_hybrid(eigs, lower, upper)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sweep chiral Kelvin bridge strength.")
    parser.add_argument("--n", type=int, default=31)
    parser.add_argument("--half-width", type=float, default=4.0)
    parser.add_argument("--profile-n", type=int, default=1200)
    parser.add_argument("--start", type=float, default=3.0)
    parser.add_argument("--stop", type=float, default=8.0)
    parser.add_argument("--steps", type=int, default=11)
    parser.add_argument("--hybrid-lower", type=float, default=0.10)
    parser.add_argument("--hybrid-upper", type=float, default=0.35)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        profile="numerical",
        profile_n=args.profile_n,
        chi_parity="sin",
    )
    target = SSVScales().muon_ratio_draft
    best: tuple[float, float] | None = None
    print("Chiral-Kelvin bridge sweep")
    print(f"target omega_mu/omega_c = {target:.9e}")
    print(f"grid n                  = {cfg.n}")
    print(f"half_width              = {cfg.half_width}")
    print(f"profile_n               = {cfg.profile_n}")
    print("mix hybrid abs_error rel_error")
    for i in range(args.steps):
        mix = args.start + (args.stop - args.start) * i / max(args.steps - 1, 1)
        _, hybrid = run_point(cfg, mix, args.hybrid_lower, args.hybrid_upper)
        if hybrid is None:
            print(f"{mix:.9e} none none none")
            continue
        error = abs(hybrid - target)
        rel = error / target
        print(f"{mix:.9e} {hybrid:.9e} {error:.9e} {rel:.9e}")
        if best is None or error < abs(best[1] - target):
            best = (mix, hybrid)
    if best is not None:
        print("Best")
        print(f"mix                      = {best[0]:.9e}")
        print(f"hybrid                   = {best[1]:.9e}")
        print(f"hybrid/target            = {best[1] / target:.9e}")


if __name__ == "__main__":
    main()

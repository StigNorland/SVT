from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

from kelvin_augmented_bdg import build_bdg, build_modes, dense_eigenvalues, kelvin_self_induction_shift
from muon_mode_prototype import SSVScales
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


@dataclass(frozen=True)
class LadderHit:
    omega: float
    rung: float
    rung_value: float
    abs_error: float
    rel_error: float


def nearest_half_integer_rung(omega: float, mu0_ratio: float) -> LadderHit:
    rung = round(2.0 * omega / mu0_ratio) / 2.0
    if rung < 0.5:
        rung = 0.5
    rung_value = rung * mu0_ratio
    abs_error = abs(omega - rung_value)
    rel_error = abs_error / max(abs(rung_value), 1.0e-30)
    return LadderHit(omega, rung, rung_value, abs_error, rel_error)


def classify_eigs(eigs: list[complex], stable_tol: float) -> tuple[list[float], list[complex]]:
    stable = sorted(value.real for value in eigs if value.real > 1.0e-5 and abs(value.imag) <= stable_tol)
    unstable = [value for value in eigs if value.real > 1.0e-5 and abs(value.imag) > stable_tol]
    return stable, unstable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify BdG spectrum against the half-integer alpha-harmonic ladder.")
    parser.add_argument("--n", type=int, default=41)
    parser.add_argument("--half-width", type=float, default=5.0)
    parser.add_argument("--profile-n", type=int, default=1600)
    parser.add_argument("--lambda-perp", type=float, default=math.pi / 4.0)
    parser.add_argument("--kelvin-phi-n", type=int, default=1024)
    parser.add_argument("--kelvin-core-radius", type=float, default=1.0)
    parser.add_argument("--stable-tol", type=float, default=1.0e-5)
    parser.add_argument("--max-rung-error", type=float, default=0.05)
    parser.add_argument("--show-all", action="store_true")
    parser.add_argument("--all-eigs", action="store_true", help="Print every eigenvalue, including negative and complex values.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scales = SSVScales()
    mu0_ratio = (2.0 / 3.0) * scales.muon_ratio_draft
    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        profile="numerical",
        profile_n=args.profile_n,
        chi_parity="sin",
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=False, kelvin_seed="helicity")
    h = build_bdg(
        bg,
        modes,
        cfg,
        "profile-logse",
        chiral_mix=0.0,
        bridge_model="shape",
        lambda_perp=args.lambda_perp,
        kelvin_dispersion="self-induction",
        kelvin_phi_n=args.kelvin_phi_n,
        kelvin_core_radius=args.kelvin_core_radius,
    )
    eigs, eigensolver = dense_eigenvalues(h)
    stable, unstable = classify_eigs(eigs, args.stable_tol)
    kelvin_scale = kelvin_self_induction_shift(bg, args.kelvin_phi_n, args.kelvin_core_radius)

    print("Alpha-harmonic ladder spectrum test")
    print(f"eigensolver              = {eigensolver}")
    print(f"grid n                   = {cfg.n}")
    print(f"half_width               = {cfg.half_width}")
    print(f"profile_n                = {cfg.profile_n}")
    print(f"lambda_perp              = {args.lambda_perp:.12e}")
    print(f"kelvin_self_induction    = {kelvin_scale:.12e}")
    print(f"mu0_ratio                = {mu0_ratio:.12e}")
    print(f"stable_positive_count    = {len(stable)}")
    print(f"unstable_positive_count  = {len(unstable)}")
    print("stable omega nearest_rung rung_value abs_error rel_error status")
    for omega in stable:
        hit = nearest_half_integer_rung(omega, mu0_ratio)
        status = "hit" if hit.rel_error <= args.max_rung_error else "miss"
        if args.show_all or status == "hit":
            print(
                f"{hit.omega:.12e} {hit.rung:.1f} {hit.rung_value:.12e} "
                f"{hit.abs_error:.12e} {hit.rel_error:.12e} {status}"
            )
    if unstable:
        print("unstable positive eigenvalues")
        for value in sorted(unstable, key=lambda z: (z.real, abs(z.imag))):
            print(f"{value.real:.12e} {value.imag:+.12e}i")
    if args.all_eigs:
        print("all eigenvalues with nearest ladder rung by |Re omega|")
        for value in sorted(eigs, key=lambda z: (z.real, z.imag)):
            hit = nearest_half_integer_rung(abs(value.real), mu0_ratio)
            stability = "stable" if abs(value.imag) <= args.stable_tol else "complex"
            print(
                f"{value.real:.12e} {value.imag:+.12e}i "
                f"absRe={abs(value.real):.12e} rung={hit.rung:.1f} "
                f"rung_value={hit.rung_value:.12e} rel_error={hit.rel_error:.12e} {stability}"
            )


if __name__ == "__main__":
    main()

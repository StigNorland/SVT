from __future__ import annotations

import argparse
from dataclasses import dataclass

from kelvin_augmented_bdg import build_bdg, build_modes, dense_eigenvalues, kelvin_self_induction_shift
from muon_mode_prototype import SSVScales
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


@dataclass(frozen=True)
class TrackingPoint:
    n: int
    half_width: float
    profile_n: int


@dataclass(frozen=True)
class Branch:
    value: float
    core_weight: float
    kelvin_weight: float
    krein_norm: float
    core_krein: float
    kelvin_krein: float


def positive_real(eigs: list[complex]) -> list[float]:
    return sorted(value.real for value in eigs if value.real > 1.0e-5 and abs(value.imag) < 1.0e-5)


def window(values: list[float], lower: float, upper: float) -> list[float]:
    return [value for value in values if lower <= value <= upper]


def branch_weights(vector: object, mode_count: int, core_count: int = 2) -> tuple[float, float, float, float, float]:
    try:
        import numpy as np
    except ModuleNotFoundError:
        return 0.0, 0.0, 0.0, 0.0, 0.0
    vec = np.asarray(vector)
    particles = vec[:mode_count]
    holes = vec[mode_count:]
    core_indices = list(range(core_count)) + list(range(mode_count, mode_count + core_count))
    kelvin_indices = [idx for idx in range(2 * mode_count) if idx not in core_indices]

    eta_weights = np.concatenate((np.ones(mode_count), -np.ones(mode_count)))
    signed = eta_weights * np.abs(vec) ** 2
    core_krein = float(np.sum(signed[core_indices]))
    kelvin_krein = float(np.sum(signed[kelvin_indices]))
    krein_norm = float(np.sum(np.abs(particles) ** 2) - np.sum(np.abs(holes) ** 2))
    sector_total = abs(core_krein) + abs(kelvin_krein)
    if sector_total <= 1.0e-30:
        return 0.0, 0.0, krein_norm, core_krein, kelvin_krein
    core_weight = abs(core_krein) / sector_total
    kelvin_weight = abs(kelvin_krein) / sector_total
    return core_weight, kelvin_weight, krein_norm, core_krein, kelvin_krein


def eig_branches(h: list[list[complex]], mode_count: int) -> list[Branch]:
    try:
        import numpy as np
    except ModuleNotFoundError:
        eigs, _ = dense_eigenvalues(h)
        return [Branch(value.real, 0.0, 0.0, 0.0, 0.0, 0.0) for value in eigs if value.real > 1.0e-5 and abs(value.imag) < 1.0e-5]
    values, vectors = np.linalg.eig(np.array(h, dtype=complex))
    branches = []
    for i, value in enumerate(values):
        if value.real <= 1.0e-5 or abs(value.imag) >= 1.0e-5:
            continue
        core_weight, kelvin_weight, krein_norm, core_krein, kelvin_krein = branch_weights(vectors[:, i], mode_count)
        branches.append(Branch(float(value.real), core_weight, kelvin_weight, krein_norm, core_krein, kelvin_krein))
    return sorted(branches, key=lambda branch: branch.value)


def run_point(
    point: TrackingPoint,
    lambda_perp: float,
    kelvin_phi_n: int,
    kelvin_core_radius: float,
    hybrid_lower: float,
    hybrid_upper: float,
) -> tuple[list[Branch], list[Branch], Branch | None, float]:
    cfg = ProjectionConfig(
        n=point.n,
        half_width=point.half_width,
        profile="numerical",
        profile_n=point.profile_n,
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
        lambda_perp=lambda_perp,
        kelvin_dispersion="self-induction",
        kelvin_phi_n=kelvin_phi_n,
        kelvin_core_radius=kelvin_core_radius,
    )
    positives = eig_branches(h, len(modes))
    kelvin_scale = kelvin_self_induction_shift(bg, kelvin_phi_n, kelvin_core_radius)
    hybrids = [branch for branch in positives if hybrid_lower <= branch.value <= hybrid_upper]
    target = SSVScales().muon_ratio_draft
    selected = min(hybrids, key=lambda branch: abs(branch.value - target)) if hybrids else None
    return positives, hybrids, selected, kelvin_scale


def parse_points(raw: str) -> list[TrackingPoint]:
    points = []
    for chunk in raw.split(";"):
        if not chunk.strip():
            continue
        n_raw, half_width_raw, profile_n_raw = chunk.split(",")
        points.append(TrackingPoint(int(n_raw), float(half_width_raw), int(profile_n_raw)))
    return points


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track Kelvin self-induction and muon-window hybrid branches across grids.")
    parser.add_argument(
        "--points",
        default="13,4,400;21,4,800;31,4,1200",
        help="Semicolon list of n,half_width,profile_n points.",
    )
    parser.add_argument("--lambda-perp", type=float, default=0.7853981633974483)
    parser.add_argument("--kelvin-phi-n", type=int, default=512)
    parser.add_argument("--kelvin-core-radius", type=float, default=1.0)
    parser.add_argument("--hybrid-lower", type=float, default=0.10)
    parser.add_argument("--hybrid-upper", type=float, default=0.40)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = SSVScales().muon_ratio_draft
    print("Kelvin self-induction branch tracking")
    print(f"target omega_mu/omega_c = {target:.9e}")
    print(f"lambda_perp             = {args.lambda_perp:.9e}")
    print(f"kelvin_phi_n            = {args.kelvin_phi_n}")
    print(f"kelvin_core_radius      = {args.kelvin_core_radius:.9e}")
    print("n half_width profile_n kelvin_scale kelvin_pair hybrids selected abs_error rel_error")
    for point in parse_points(args.points):
        positives, hybrids, selected, kelvin_scale = run_point(
            point,
            lambda_perp=args.lambda_perp,
            kelvin_phi_n=args.kelvin_phi_n,
            kelvin_core_radius=args.kelvin_core_radius,
            hybrid_lower=args.hybrid_lower,
            hybrid_upper=args.hybrid_upper,
        )
        kelvin_pair = [branch for branch in positives if branch.value < 0.05]
        hybrid_text = ",".join(
            (
                f"{branch.value:.9e}"
                f"[Krein={branch.krein_norm:+.2e},c={branch.core_weight:.2f},k={branch.kelvin_weight:.2f},"
                f"cS={branch.core_krein:+.2e},kS={branch.kelvin_krein:+.2e}]"
            )
            for branch in hybrids
        ) if hybrids else "none"
        kelvin_text = ",".join(f"{branch.value:.9e}" for branch in kelvin_pair) if kelvin_pair else "none"
        if selected is None:
            print(
                f"{point.n} {point.half_width:.3f} {point.profile_n} {kelvin_scale:.9e} "
                f"{kelvin_text} {hybrid_text} none none none"
            )
            continue
        error = abs(selected.value - target)
        print(
            f"{point.n} {point.half_width:.3f} {point.profile_n} {kelvin_scale:.9e} "
            f"{kelvin_text} {hybrid_text} {selected.value:.9e} {error:.9e} {error / target:.9e}"
        )


if __name__ == "__main__":
    main()

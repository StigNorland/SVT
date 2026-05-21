from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from kelvin_augmented_bdg import build_bdg, build_modes, kelvin_self_induction_shift
from kelvin_branch_tracking import TrackingPoint, branch_weights, parse_points
from muon_mode_prototype import SSVScales
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


@dataclass(frozen=True)
class BranchSnapshot:
    branch_id: str
    omega: float
    core_weight: float
    kelvin_weight: float
    krein_norm: float
    krein_sign: int
    core_krein: float
    kelvin_krein: float
    match_score: float | None
    euclidean_overlap: float | None
    krein_overlap: float | None
    frequency_step: float | None


@dataclass(frozen=True)
class PointSnapshot:
    n: int
    half_width: float
    profile_n: int
    kelvin_scale: float
    branches: list[BranchSnapshot]


@dataclass
class BranchVector:
    omega: float
    vector: np.ndarray
    core_weight: float
    kelvin_weight: float
    krein_norm: float
    core_krein: float
    kelvin_krein: float

    @property
    def krein_sign(self) -> int:
        if self.krein_norm > 0.0:
            return 1
        if self.krein_norm < 0.0:
            return -1
        return 0


def lambda_from_delta(delta_relax: float) -> float:
    return (math.pi / 4.0) * (1.0 + delta_relax)


def eta_metric(mode_count: int) -> np.ndarray:
    return np.concatenate((np.ones(mode_count), -np.ones(mode_count)))


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm <= 1.0e-30:
        return vector
    return vector / norm


def eig_hybrid_vectors(
    point: TrackingPoint,
    lambda_perp: float,
    kelvin_phi_n: int,
    kelvin_core_radius: float,
    core_basis: str,
    kelvin_seed: str,
    current_curl_model: str,
    projection_window: str,
    window_radius: float,
    window_taper: float,
    hybrid_lower: float,
    hybrid_upper: float,
) -> tuple[list[BranchVector], float]:
    cfg = ProjectionConfig(
        n=point.n,
        half_width=point.half_width,
        profile="numerical",
        profile_n=point.profile_n,
        chi_parity="sin",
        projection_window=projection_window,
        window_radius=window_radius,
        window_taper=window_taper,
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    include_core_four = core_basis == "four"
    core_count = 4 if include_core_four else 2
    modes = build_modes(bg, cfg, include_core_four=include_core_four, kelvin_seed=kelvin_seed)
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
        current_curl_model=current_curl_model,
    )
    values, vectors = np.linalg.eig(np.array(h, dtype=complex))
    branches: list[BranchVector] = []
    for idx, value in enumerate(values):
        if value.real <= hybrid_lower or value.real >= hybrid_upper or abs(value.imag) >= 1.0e-5:
            continue
        vector = normalize_vector(vectors[:, idx])
        core_weight, kelvin_weight, krein_norm, core_krein, kelvin_krein = branch_weights(
            vector,
            len(modes),
            core_count=core_count,
        )
        branches.append(
            BranchVector(
                omega=float(value.real),
                vector=vector,
                core_weight=core_weight,
                kelvin_weight=kelvin_weight,
                krein_norm=krein_norm,
                core_krein=core_krein,
                kelvin_krein=kelvin_krein,
            )
        )
    branches.sort(key=lambda branch: branch.omega)
    kelvin_scale = kelvin_self_induction_shift(bg, kelvin_phi_n, kelvin_core_radius)
    return branches, kelvin_scale


def overlap_metrics(previous: BranchVector, candidate: BranchVector) -> tuple[float, float, float]:
    mode_count = previous.vector.size // 2
    eta = eta_metric(mode_count)
    euclidean = float(abs(np.vdot(previous.vector, candidate.vector)))
    raw_krein = np.vdot(previous.vector, eta * candidate.vector)
    denom = math.sqrt(max(abs(previous.krein_norm * candidate.krein_norm), 1.0e-30))
    krein = float(min(abs(raw_krein) / denom, 1.0))
    same_sign = 1.0 if previous.krein_sign == candidate.krein_sign else 0.0
    # The score is intentionally dominated by eigenvector overlap. Krein sign is
    # used as a guard rail, not as a replacement for actual vector continuity.
    score = 0.65 * euclidean + 0.25 * krein + 0.10 * same_sign
    return score, euclidean, krein


def continue_labels(
    points: list[TrackingPoint],
    lambda_perp: float,
    kelvin_phi_n: int,
    kelvin_core_radius: float,
    core_basis: str,
    kelvin_seed: str,
    current_curl_model: str,
    projection_window: str,
    window_radius: float,
    window_taper: float,
    hybrid_lower: float,
    hybrid_upper: float,
) -> list[PointSnapshot]:
    snapshots: list[PointSnapshot] = []
    labelled_previous: dict[str, BranchVector] = {}

    for point_index, point in enumerate(points):
        branches, kelvin_scale = eig_hybrid_vectors(
            point,
            lambda_perp=lambda_perp,
            kelvin_phi_n=kelvin_phi_n,
            kelvin_core_radius=kelvin_core_radius,
            core_basis=core_basis,
            kelvin_seed=kelvin_seed,
            current_curl_model=current_curl_model,
            projection_window=projection_window,
            window_radius=window_radius,
            window_taper=window_taper,
            hybrid_lower=hybrid_lower,
            hybrid_upper=hybrid_upper,
        )
        if point_index == 0:
            current: dict[str, BranchVector] = {
                f"B{idx}_by_initial_order": branch for idx, branch in enumerate(branches)
            }
            rows = [
                BranchSnapshot(
                    branch_id=label,
                    omega=branch.omega,
                    core_weight=branch.core_weight,
                    kelvin_weight=branch.kelvin_weight,
                    krein_norm=branch.krein_norm,
                    krein_sign=branch.krein_sign,
                    core_krein=branch.core_krein,
                    kelvin_krein=branch.kelvin_krein,
                    match_score=None,
                    euclidean_overlap=None,
                    krein_overlap=None,
                    frequency_step=None,
                )
                for label, branch in current.items()
            ]
            labelled_previous = current
            snapshots.append(PointSnapshot(point.n, point.half_width, point.profile_n, kelvin_scale, rows))
            continue

        unused = list(range(len(branches)))
        current = {}
        rows = []
        for label, previous in labelled_previous.items():
            if not unused:
                break
            scored = []
            for idx in unused:
                score, euclidean, krein = overlap_metrics(previous, branches[idx])
                scored.append((score, euclidean, krein, idx))
            score, euclidean, krein, best_idx = max(scored, key=lambda item: item[0])
            unused.remove(best_idx)
            branch = branches[best_idx]
            current[label] = branch
            rows.append(
                BranchSnapshot(
                    branch_id=label,
                    omega=branch.omega,
                    core_weight=branch.core_weight,
                    kelvin_weight=branch.kelvin_weight,
                    krein_norm=branch.krein_norm,
                    krein_sign=branch.krein_sign,
                    core_krein=branch.core_krein,
                    kelvin_krein=branch.kelvin_krein,
                    match_score=score,
                    euclidean_overlap=euclidean,
                    krein_overlap=krein,
                    frequency_step=branch.omega - previous.omega,
                )
            )
        for idx in unused:
            label = f"new_B{idx}_at_n{point.n}"
            branch = branches[idx]
            current[label] = branch
            rows.append(
                BranchSnapshot(
                    branch_id=label,
                    omega=branch.omega,
                    core_weight=branch.core_weight,
                    kelvin_weight=branch.kelvin_weight,
                    krein_norm=branch.krein_norm,
                    krein_sign=branch.krein_sign,
                    core_krein=branch.core_krein,
                    kelvin_krein=branch.kelvin_krein,
                    match_score=None,
                    euclidean_overlap=None,
                    krein_overlap=None,
                    frequency_step=None,
                )
            )
        labelled_previous = current
        rows.sort(key=lambda row: row.branch_id)
        snapshots.append(PointSnapshot(point.n, point.half_width, point.profile_n, kelvin_scale, rows))

    return snapshots


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Track reduced muon hybrid branch identity by eigenvector overlap and Krein signature."
    )
    parser.add_argument("--points", default="13,4,400;17,4,600;21,4,800;25,4,1000;31,4,1200")
    parser.add_argument("--delta-relax", type=float, default=0.038)
    parser.add_argument("--lambda-perp", type=float, help="override lambda_perp directly")
    parser.add_argument("--core-basis", choices=("two", "four"), default="two")
    parser.add_argument("--kelvin-seed", choices=("helicity", "displacement", "breathing", "combined"), default="helicity")
    parser.add_argument("--current-curl-model", choices=("linear", "full"), default="linear")
    parser.add_argument("--projection-window", choices=("hard", "smooth"), default="hard")
    parser.add_argument("--window-radius", type=float, default=0.0)
    parser.add_argument("--window-taper", type=float, default=0.0)
    parser.add_argument("--kelvin-phi-n", type=int, default=256)
    parser.add_argument("--kelvin-core-radius", type=float, default=1.0)
    parser.add_argument("--hybrid-lower", type=float, default=0.10)
    parser.add_argument("--hybrid-upper", type=float, default=0.40)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    lambda_perp = args.lambda_perp if args.lambda_perp is not None else lambda_from_delta(args.delta_relax)
    snapshots = continue_labels(
        parse_points(args.points),
        lambda_perp=lambda_perp,
        kelvin_phi_n=args.kelvin_phi_n,
        kelvin_core_radius=args.kelvin_core_radius,
        core_basis=args.core_basis,
        kelvin_seed=args.kelvin_seed,
        current_curl_model=args.current_curl_model,
        projection_window=args.projection_window,
        window_radius=args.window_radius,
        window_taper=args.window_taper,
        hybrid_lower=args.hybrid_lower,
        hybrid_upper=args.hybrid_upper,
    )
    target = SSVScales().muon_ratio_draft
    print("Muon branch identity tracking by eigenvector/Krein overlap")
    print(f"target omega_mu/omega_c = {target:.9e}")
    print(f"lambda_perp             = {lambda_perp:.9e}")
    print(f"delta_relax             = {args.delta_relax:.9e}")
    print(f"core_basis              = {args.core_basis}")
    print(f"kelvin_seed             = {args.kelvin_seed}")
    print(f"current_curl_model      = {args.current_curl_model}")
    print(f"projection_window       = {args.projection_window}")
    print(f"window_radius           = {args.window_radius:.9e}")
    print(f"window_taper            = {args.window_taper:.9e}")
    print(f"kelvin_phi_n            = {args.kelvin_phi_n}")
    print(f"kelvin_core_radius      = {args.kelvin_core_radius:.9e}")
    print(
        "n half_width profile_n branch_id omega abs_error rel_error core_weight kelvin_weight "
        "krein_norm krein_sign match_score euclidean_overlap krein_overlap frequency_step"
    )
    for snapshot in snapshots:
        for branch in snapshot.branches:
            abs_error = abs(branch.omega - target)
            rel_error = abs_error / target
            def fmt(value: float | None) -> str:
                return "none" if value is None else f"{value:.9e}"

            print(
                f"{snapshot.n} {snapshot.half_width:.3f} {snapshot.profile_n} {branch.branch_id} "
                f"{branch.omega:.9e} {abs_error:.9e} {rel_error:.9e} "
                f"{branch.core_weight:.9e} {branch.kelvin_weight:.9e} "
                f"{branch.krein_norm:.9e} {branch.krein_sign:+d} "
                f"{fmt(branch.match_score)} {fmt(branch.euclidean_overlap)} "
                f"{fmt(branch.krein_overlap)} {fmt(branch.frequency_step)}"
            )
    if args.output:
        payload = {
            "target_omega_mu_over_omega_c": target,
            "lambda_perp": lambda_perp,
            "delta_relax": args.delta_relax,
            "core_basis": args.core_basis,
            "kelvin_seed": args.kelvin_seed,
            "current_curl_model": args.current_curl_model,
            "projection_window": args.projection_window,
            "window_radius": args.window_radius,
            "window_taper": args.window_taper,
            "kelvin_phi_n": args.kelvin_phi_n,
            "kelvin_core_radius": args.kelvin_core_radius,
            "points": [asdict(snapshot) for snapshot in snapshots],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Results written to {args.output}")


if __name__ == "__main__":
    main()

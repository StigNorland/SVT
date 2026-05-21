from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from kelvin_branch_tracking import TrackingPoint, parse_points, run_point
from muon_mode_prototype import SSVScales


@dataclass(frozen=True)
class HybridBranchRow:
    omega: float
    core_weight: float
    kelvin_weight: float
    krein_norm: float
    core_krein: float
    kelvin_krein: float


@dataclass(frozen=True)
class LambdaBandRow:
    n: int
    half_width: float
    profile_n: int
    kelvin_core_radius: float
    delta_relax: float
    lambda_perp: float
    selected_omega: float | None
    abs_error: float | None
    rel_error: float | None
    core_weight: float | None
    kelvin_weight: float | None
    kelvin_scale: float
    hybrid_count: int
    hybrid_branches: list[HybridBranchRow]


def lambda_from_delta(delta_relax: float) -> float:
    return (math.pi / 4.0) * (1.0 + delta_relax)


def serialise_hybrids(hybrids: object) -> list[HybridBranchRow]:
    return [
        HybridBranchRow(
            omega=branch.value,
            core_weight=branch.core_weight,
            kelvin_weight=branch.kelvin_weight,
            krein_norm=branch.krein_norm,
            core_krein=branch.core_krein,
            kelvin_krein=branch.kelvin_krein,
        )
        for branch in hybrids
    ]


def run_band(
    points: list[TrackingPoint],
    deltas: list[float],
    kelvin_phi_n: int,
    kelvin_core_radii: list[float],
    hybrid_lower: float,
    hybrid_upper: float,
) -> list[LambdaBandRow]:
    target = SSVScales().muon_ratio_draft
    rows: list[LambdaBandRow] = []
    for point in points:
        for kelvin_core_radius in kelvin_core_radii:
            for delta in deltas:
                lambda_perp = lambda_from_delta(delta)
                _, hybrids, selected, kelvin_scale = run_point(
                    point,
                    lambda_perp=lambda_perp,
                    kelvin_phi_n=kelvin_phi_n,
                    kelvin_core_radius=kelvin_core_radius,
                    hybrid_lower=hybrid_lower,
                    hybrid_upper=hybrid_upper,
                )
                if selected is None:
                    rows.append(
                        LambdaBandRow(
                            n=point.n,
                            half_width=point.half_width,
                            profile_n=point.profile_n,
                            kelvin_core_radius=kelvin_core_radius,
                            delta_relax=delta,
                            lambda_perp=lambda_perp,
                            selected_omega=None,
                            abs_error=None,
                            rel_error=None,
                            core_weight=None,
                            kelvin_weight=None,
                            kelvin_scale=kelvin_scale,
                            hybrid_count=len(hybrids),
                            hybrid_branches=serialise_hybrids(hybrids),
                        )
                    )
                    continue
                abs_error = abs(selected.value - target)
                rows.append(
                    LambdaBandRow(
                        n=point.n,
                        half_width=point.half_width,
                        profile_n=point.profile_n,
                        kelvin_core_radius=kelvin_core_radius,
                        delta_relax=delta,
                        lambda_perp=lambda_perp,
                        selected_omega=selected.value,
                        abs_error=abs_error,
                        rel_error=abs_error / target,
                        core_weight=selected.core_weight,
                        kelvin_weight=selected.kelvin_weight,
                        kelvin_scale=kelvin_scale,
                        hybrid_count=len(hybrids),
                        hybrid_branches=serialise_hybrids(hybrids),
                    )
                )
    return rows


def parse_deltas(raw: str) -> list[float]:
    return [float(chunk.strip()) for chunk in raw.split(",") if chunk.strip()]


def parse_floats(raw: str) -> list[float]:
    return [float(chunk.strip()) for chunk in raw.split(",") if chunk.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Propagate a relaxed thin-ring lambda_perp band through the Kelvin-augmented reduced BdG branch tracker."
    )
    parser.add_argument("--points", default="31,5,1200", help="Semicolon list of n,half_width,profile_n points.")
    parser.add_argument("--deltas", default="0.0,0.033,0.038,0.043", help="Comma-separated delta_relax values.")
    parser.add_argument("--kelvin-phi-n", type=int, default=512)
    parser.add_argument("--kelvin-core-radius", type=float, default=1.0, help="single Kelvin core radius")
    parser.add_argument(
        "--kelvin-core-radii",
        help="comma-separated Kelvin core radii; overrides --kelvin-core-radius",
    )
    parser.add_argument("--hybrid-lower", type=float, default=0.10)
    parser.add_argument("--hybrid-upper", type=float, default=0.40)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = SSVScales().muon_ratio_draft
    rows = run_band(
        points=parse_points(args.points),
        deltas=parse_deltas(args.deltas),
        kelvin_phi_n=args.kelvin_phi_n,
        kelvin_core_radii=parse_floats(args.kelvin_core_radii) if args.kelvin_core_radii else [args.kelvin_core_radius],
        hybrid_lower=args.hybrid_lower,
        hybrid_upper=args.hybrid_upper,
    )

    print("Muon lambda-band propagation through reduced BdG branch tracker")
    print(f"target omega_mu/omega_c = {target:.9e}")
    print(f"kelvin_phi_n            = {args.kelvin_phi_n}")
    if args.kelvin_core_radii:
        print(f"kelvin_core_radii       = {args.kelvin_core_radii}")
    else:
        print(f"kelvin_core_radius      = {args.kelvin_core_radius:.9e}")
    print(
        "n half_width profile_n kelvin_core_radius delta_relax lambda_perp selected "
        "abs_error rel_error core_weight kelvin_weight hybrids hybrid_omegas"
    )
    for row in rows:
        selected = "none" if row.selected_omega is None else f"{row.selected_omega:.9e}"
        abs_error = "none" if row.abs_error is None else f"{row.abs_error:.9e}"
        rel_error = "none" if row.rel_error is None else f"{row.rel_error:.9e}"
        core = "none" if row.core_weight is None else f"{row.core_weight:.9e}"
        kelvin = "none" if row.kelvin_weight is None else f"{row.kelvin_weight:.9e}"
        hybrid_omegas = ",".join(f"{branch.omega:.9e}" for branch in row.hybrid_branches) or "none"
        print(
            f"{row.n} {row.half_width:.3f} {row.profile_n} {row.kelvin_core_radius:.9e} "
            f"{row.delta_relax:.9e} {row.lambda_perp:.9e} {selected} "
            f"{abs_error} {rel_error} {core} {kelvin} {row.hybrid_count} {hybrid_omegas}"
        )

    if args.output:
        payload = {
            "target_omega_mu_over_omega_c": target,
            "kelvin_phi_n": args.kelvin_phi_n,
            "kelvin_core_radii": parse_floats(args.kelvin_core_radii) if args.kelvin_core_radii else [args.kelvin_core_radius],
            "rows": [asdict(row) for row in rows],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Results written to {args.output}")


if __name__ == "__main__":
    main()

"""Check whether cumulative Q_p(<r) flattens before the boundary blend region starts.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: cumulative static-potential coefficient versus radius, blend-start remainder,
and near-edge slope diagnostics
Primary role: determine whether the source is effectively settled in the interior or still building
as it enters the boundary recovery layer.
Key limitation: this is a diagnostic check on saved prototype states and depends on the current blend-layer definition.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether cumulative Q_p(<r) flattens before the boundary blend region begins."
    )
    parser.add_argument("states", nargs="+", type=Path, help="Saved .npz states from trefoil_breather_static.py")
    parser.add_argument("--bins", type=int, default=40, help="Number of radial shells used for the cumulative curve.")
    parser.add_argument("--probe-radius", type=float, default=12.0, help="Probe radius on the +x axis.")
    parser.add_argument(
        "--tail-window",
        type=int,
        default=3,
        help="Number of bins immediately before the blend start used for the pre-boundary slope check.",
    )
    parser.add_argument(
        "--remainder-tol",
        type=float,
        default=0.02,
        help="Maximum allowed fraction of Q_p still added after blend_start for a clean interior plateau.",
    )
    parser.add_argument(
        "--slope-tol",
        type=float,
        default=0.01,
        help="Maximum allowed relative span of cumulative Q_p over the pre-blend tail window.",
    )
    parser.add_argument("--xi", type=float, default=1.0)
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def green_static(radius: np.ndarray, xi: float, c: float) -> np.ndarray:
    radius = np.asarray(radius, dtype=float)
    out = np.empty_like(radius)
    nonzero = radius > 1.0e-12
    out[nonzero] = (1.0 - np.exp(-2.0 * radius[nonzero] / xi)) / (4.0 * math.pi * c * c * radius[nonzero])
    out[~nonzero] = 1.0 / (2.0 * math.pi * c * c * xi)
    return out


def metric_span(values: list[float]) -> dict[str, float]:
    if not values:
        return {"min": 0.0, "max": 0.0, "span": 0.0, "relative_span": 0.0}
    v_min = min(values)
    v_max = max(values)
    span = v_max - v_min
    scale = max(abs(v_min), abs(v_max), 1.0e-12)
    return {"min": v_min, "max": v_max, "span": span, "relative_span": span / scale}


def load_state(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict[str, object], dict[str, object], float]:
    data = np.load(path, allow_pickle=False)
    psi = data["psi_real"] + 1j * data["psi_imag"]
    x = data["x"]
    y = data["y"]
    z = data["z"]
    config = json.loads(str(data["config"]))
    summary = json.loads(str(data["summary"]))
    spacing = float(x[1, 0, 0] - x[0, 0, 0]) if x.shape[0] > 1 else 0.0
    return psi, x, y, z, config, summary, spacing


def cumulative_q_profile(
    deficit: np.ndarray,
    radius: np.ndarray,
    kernel: np.ndarray,
    cell_volume: float,
    bins: int,
    probe_radius: float,
    c: float,
) -> list[dict[str, float]]:
    edges = np.linspace(0.0, float(np.max(radius)), bins + 1)
    cumulative_potential = 0.0
    rows: list[dict[str, float]] = []
    for i in range(bins):
        inner = float(edges[i])
        outer = float(edges[i + 1])
        mask = (radius >= inner) & (radius < outer if i < bins - 1 else radius <= outer)
        shell_potential = float(np.sum(deficit[mask] * kernel[mask]) * cell_volume)
        cumulative_potential += shell_potential
        cumulative_q = float(4.0 * math.pi * c * c * probe_radius * cumulative_potential)
        rows.append(
            {
                "r_inner": inner,
                "r_outer": outer,
                "r_mid": 0.5 * (inner + outer),
                "shell_potential_at_probe": shell_potential,
                "cumulative_q_p_effective": cumulative_q,
            }
        )
    return rows


def analyze_state(
    path: Path,
    bins: int,
    probe_radius: float,
    tail_window: int,
    remainder_tol: float,
    slope_tol: float,
    xi: float,
    c: float,
) -> dict[str, object]:
    psi, x, y, z, config, summary, spacing = load_state(path)
    cell_volume = spacing**3
    radius = np.sqrt(x * x + y * y + z * z)
    deficit = np.clip(1.0 - np.abs(psi) ** 2, 0.0, None)
    distance_to_probe = np.sqrt((x - probe_radius) ** 2 + y * y + z * z)
    kernel = green_static(distance_to_probe, xi=xi, c=c)

    profile = cumulative_q_profile(deficit, radius, kernel, cell_volume, bins, probe_radius, c)
    total_q = float(profile[-1]["cumulative_q_p_effective"]) if profile else 0.0

    r_max = math.sqrt(3.0) * float(config["half_width"])
    blend_fraction = float(config.get("boundary_blend_fraction", 0.0))
    blend_start = max((1.0 - blend_fraction) * r_max, 0.0)

    last_preblend_index = -1
    for i, row in enumerate(profile):
        if float(row["r_outer"]) <= blend_start:
            last_preblend_index = i

    if last_preblend_index >= 0:
        preblend_q = float(profile[last_preblend_index]["cumulative_q_p_effective"])
        remainder_fraction = abs(total_q - preblend_q) / max(abs(total_q), 1.0e-12)
        tail_start = max(0, last_preblend_index - max(tail_window, 1) + 1)
        tail_values = [float(row["cumulative_q_p_effective"]) for row in profile[tail_start : last_preblend_index + 1]]
        tail_span = metric_span(tail_values)
    else:
        preblend_q = 0.0
        remainder_fraction = 1.0
        tail_values = []
        tail_span = metric_span(tail_values)

    plateau_before_blend = remainder_fraction <= remainder_tol and tail_span["relative_span"] <= slope_tol

    return {
        "state": str(path),
        "n": int(config["n"]),
        "half_width": float(config["half_width"]),
        "steps_completed": int(summary.get("total_steps_effective", summary.get("steps_completed", 0))),
        "projected_residual_norm": float(summary.get("projected_residual_norm", summary.get("residual_norm", 0.0))),
        "shell_mean_density": float(1.0 - summary.get("far_field_shell_deficit", 0.0)),
        "probe_radius": float(probe_radius),
        "blend_start_radius": float(blend_start),
        "blend_start_fraction_of_rmax": float(1.0 - blend_fraction),
        "total_q_p_effective": total_q,
        "preblend_q_p_effective": preblend_q,
        "post_blend_remainder_fraction": float(remainder_fraction),
        "preblend_tail_span": tail_span,
        "plateau_before_blend": bool(plateau_before_blend),
        "criteria": {
            "remainder_tol": float(remainder_tol),
            "slope_tol": float(slope_tol),
            "tail_window_bins": int(tail_window),
        },
        "profile": profile,
    }


def cross_state_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "post_blend_remainder_fraction": metric_span([float(row["post_blend_remainder_fraction"]) for row in rows]),
        "preblend_q_p_effective": metric_span([float(row["preblend_q_p_effective"]) for row in rows]),
        "total_q_p_effective": metric_span([float(row["total_q_p_effective"]) for row in rows]),
        "states_plateaued_before_blend": int(sum(1 for row in rows if bool(row["plateau_before_blend"]))),
    }


def main() -> None:
    args = parse_args()
    rows = [
        analyze_state(
            path,
            bins=args.bins,
            probe_radius=args.probe_radius,
            tail_window=args.tail_window,
            remainder_tol=args.remainder_tol,
            slope_tol=args.slope_tol,
            xi=args.xi,
            c=args.c,
        )
        for path in args.states
    ]
    rows.sort(key=lambda row: (float(row["half_width"]), int(row["n"])))

    payload = {
        "bins": int(args.bins),
        "probe_radius": float(args.probe_radius),
        "tail_window": int(args.tail_window),
        "remainder_tol": float(args.remainder_tol),
        "slope_tol": float(args.slope_tol),
        "xi": float(args.xi),
        "c": float(args.c),
        "rows": rows,
        "cross_state_summary": cross_state_summary(rows),
        "interpretation": {
            "purpose": "Check whether cumulative Q_p(<r) settles before the boundary blend region starts, rather than only flattening inside the recovery layer.",
            "warning": "A negative result means the source is still boundary-adjacent under the current solver setup; it does not by itself prove the halo is unphysical.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

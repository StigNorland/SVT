"""Scan how Q_p^eff splits between inner support and outer halo as the support cutoff moves.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: inner/outer static-potential coefficients as functions of cutoff radius
Primary role: make the halo contribution explicit and controllable on plateaued saved states
before committing to a proton-support window.
Key limitation: this is a diagnostic scan on saved prototype states, not a derived source functional.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan inner/outer Q_p support versus cutoff radius on saved trefoil states.")
    parser.add_argument("states", nargs="+", type=Path, help="Saved .npz states from trefoil_breather_static.py")
    parser.add_argument(
        "--cutoffs",
        default="2,3,4,5,6,7,8,9,10",
        help="Comma-separated cutoff radii in xi units.",
    )
    parser.add_argument("--probe-radius", type=float, default=12.0, help="Probe radius on the +x axis.")
    parser.add_argument("--window-width", type=float, default=0.5, help="Smooth cutoff width for tanh windows.")
    parser.add_argument("--xi", type=float, default=1.0)
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def parse_float_list(text: str) -> list[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def green_static(radius: np.ndarray, xi: float, c: float) -> np.ndarray:
    radius = np.asarray(radius, dtype=float)
    out = np.empty_like(radius)
    nonzero = radius > 1.0e-12
    out[nonzero] = (1.0 - np.exp(-2.0 * radius[nonzero] / xi)) / (4.0 * math.pi * c * c * radius[nonzero])
    out[~nonzero] = 1.0 / (2.0 * math.pi * c * c * xi)
    return out


def smooth_cutoff(radius: np.ndarray, cutoff: float, width: float) -> np.ndarray:
    return 0.5 * (1.0 - np.tanh((radius - cutoff) / max(width, 1.0e-12)))


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


def q_from_weighted_deficit(weighted_deficit: np.ndarray, kernel: np.ndarray, cell_volume: float, probe_radius: float, c: float) -> tuple[float, float]:
    potential = float(np.sum(weighted_deficit * kernel) * cell_volume)
    q_value = float(4.0 * math.pi * c * c * probe_radius * potential)
    return potential, q_value


def analyze_state(path: Path, cutoffs: list[float], probe_radius: float, width: float, xi: float, c: float) -> dict[str, object]:
    psi, x, y, z, config, summary, spacing = load_state(path)
    cell_volume = spacing**3
    radius = np.sqrt(x * x + y * y + z * z)
    deficit = np.clip(1.0 - np.abs(psi) ** 2, 0.0, None)
    distance_to_probe = np.sqrt((x - probe_radius) ** 2 + y * y + z * z)
    kernel = green_static(distance_to_probe, xi=xi, c=c)

    total_potential, total_q = q_from_weighted_deficit(deficit, kernel, cell_volume, probe_radius, c)
    total_deficit = float(np.sum(deficit) * cell_volume)

    rows = []
    for cutoff in cutoffs:
        hard_inner_weight = (radius <= cutoff).astype(float)
        hard_outer_weight = 1.0 - hard_inner_weight
        smooth_inner_weight = smooth_cutoff(radius, cutoff, width)
        smooth_outer_weight = 1.0 - smooth_inner_weight

        hard_inner_pot, hard_inner_q = q_from_weighted_deficit(deficit * hard_inner_weight, kernel, cell_volume, probe_radius, c)
        hard_outer_pot, hard_outer_q = q_from_weighted_deficit(deficit * hard_outer_weight, kernel, cell_volume, probe_radius, c)
        smooth_inner_pot, smooth_inner_q = q_from_weighted_deficit(deficit * smooth_inner_weight, kernel, cell_volume, probe_radius, c)
        smooth_outer_pot, smooth_outer_q = q_from_weighted_deficit(deficit * smooth_outer_weight, kernel, cell_volume, probe_radius, c)

        hard_inner_deficit = float(np.sum(deficit * hard_inner_weight) * cell_volume)
        hard_outer_deficit = float(np.sum(deficit * hard_outer_weight) * cell_volume)
        smooth_inner_deficit = float(np.sum(deficit * smooth_inner_weight) * cell_volume)
        smooth_outer_deficit = float(np.sum(deficit * smooth_outer_weight) * cell_volume)

        rows.append(
            {
                "cutoff": float(cutoff),
                "hard_inner": {
                    "deficit_volume": hard_inner_deficit,
                    "potential_at_probe": hard_inner_pot,
                    "q_p_effective": hard_inner_q,
                    "q_fraction": hard_inner_q / max(total_q, 1.0e-12),
                },
                "hard_outer": {
                    "deficit_volume": hard_outer_deficit,
                    "potential_at_probe": hard_outer_pot,
                    "q_p_effective": hard_outer_q,
                    "q_fraction": hard_outer_q / max(total_q, 1.0e-12),
                },
                "smooth_inner": {
                    "deficit_volume": smooth_inner_deficit,
                    "potential_at_probe": smooth_inner_pot,
                    "q_p_effective": smooth_inner_q,
                    "q_fraction": smooth_inner_q / max(total_q, 1.0e-12),
                },
                "smooth_outer": {
                    "deficit_volume": smooth_outer_deficit,
                    "potential_at_probe": smooth_outer_pot,
                    "q_p_effective": smooth_outer_q,
                    "q_fraction": smooth_outer_q / max(total_q, 1.0e-12),
                },
            }
        )

    return {
        "state": str(path),
        "n": int(config["n"]),
        "half_width": float(config["half_width"]),
        "steps_completed": int(summary.get("total_steps_effective", summary.get("steps_completed", 0))),
        "projected_residual_norm": float(summary.get("projected_residual_norm", summary.get("residual_norm", 0.0))),
        "shell_mean_density": float(1.0 - summary.get("far_field_shell_deficit", 0.0)),
        "probe_radius": float(probe_radius),
        "total_deficit_volume": total_deficit,
        "total_q_p_effective": total_q,
        "cutoff_scan": rows,
    }


def cross_state_summary(rows: list[dict[str, object]], cutoffs: list[float]) -> dict[str, object]:
    cutoffs_summary = []
    for cutoff in cutoffs:
        matched = []
        for row in rows:
            for entry in row["cutoff_scan"]:
                if abs(float(entry["cutoff"]) - cutoff) < 1.0e-9:
                    matched.append(
                        {
                            "half_width": float(row["half_width"]),
                            "hard_inner_q": float(entry["hard_inner"]["q_p_effective"]),
                            "hard_outer_q": float(entry["hard_outer"]["q_p_effective"]),
                            "hard_outer_fraction": float(entry["hard_outer"]["q_fraction"]),
                            "smooth_inner_q": float(entry["smooth_inner"]["q_p_effective"]),
                            "smooth_outer_q": float(entry["smooth_outer"]["q_p_effective"]),
                            "smooth_outer_fraction": float(entry["smooth_outer"]["q_fraction"]),
                        }
                    )
        cutoffs_summary.append(
            {
                "cutoff": float(cutoff),
                "hard_inner_q": metric_span([item["hard_inner_q"] for item in matched]),
                "hard_outer_q": metric_span([item["hard_outer_q"] for item in matched]),
                "hard_outer_fraction": metric_span([item["hard_outer_fraction"] for item in matched]),
                "smooth_inner_q": metric_span([item["smooth_inner_q"] for item in matched]),
                "smooth_outer_q": metric_span([item["smooth_outer_q"] for item in matched]),
                "smooth_outer_fraction": metric_span([item["smooth_outer_fraction"] for item in matched]),
            }
        )
    return {"by_cutoff": cutoffs_summary}


def main() -> None:
    args = parse_args()
    cutoffs = parse_float_list(args.cutoffs)
    rows = [analyze_state(path, cutoffs, args.probe_radius, args.window_width, args.xi, args.c) for path in args.states]
    rows.sort(key=lambda row: (float(row["half_width"]), int(row["n"])))

    payload = {
        "cutoffs": cutoffs,
        "probe_radius": float(args.probe_radius),
        "window_width": float(args.window_width),
        "xi": float(args.xi),
        "c": float(args.c),
        "rows": rows,
        "cross_state_summary": cross_state_summary(rows, cutoffs),
        "interpretation": {
            "purpose": "Make the halo contribution explicit by scanning how much Q_p^eff lives inside and outside moving support cutoffs.",
            "warning": "This is a diagnostic scan on saved prototype states; it does not by itself prove which support window is physically correct.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

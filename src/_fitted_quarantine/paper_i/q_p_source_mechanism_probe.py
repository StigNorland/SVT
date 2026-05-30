"""Probe where the static proton source is accumulating in plateaued trefoil states.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: cumulative radial deficit integrals, region-split source totals,
window-sensitive static-potential coefficients
Primary role: diagnose whether changes in Q_p^eff come from the core, mid region, or halo
before adding more reduced source ansatzes.
Key limitation: this is a mechanism probe on saved prototype states, not a closure-grade source functional.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe cumulative source build-up, region splits, and window sensitivity on saved trefoil states."
    )
    parser.add_argument("states", nargs="+", type=Path, help="Saved .npz states from trefoil_breather_static.py")
    parser.add_argument("--bins", type=int, default=32, help="Number of radial bins for cumulative profiles.")
    parser.add_argument(
        "--probe-radius",
        type=float,
        default=12.0,
        help="Probe radius on the +x axis used for the static-potential accumulation diagnostic.",
    )
    parser.add_argument(
        "--region-edges",
        default="2,5",
        help="Comma-separated radial edges for core/mid/halo split. Example: 2,5 gives core < 2, mid 2-5, halo > 5.",
    )
    parser.add_argument(
        "--window-width",
        type=float,
        default=0.5,
        help="Transition width for smooth window probes.",
    )
    parser.add_argument("--xi", type=float, default=1.0, help="Carrier healing length xi.")
    parser.add_argument("--c", type=float, default=1.0, help="Carrier speed c.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    return parser.parse_args()


def parse_float_list(text: str) -> list[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def metric_span(values: list[float]) -> dict[str, float]:
    if not values:
        return {"min": 0.0, "max": 0.0, "span": 0.0, "relative_span": 0.0}
    v_min = min(values)
    v_max = max(values)
    span = v_max - v_min
    scale = max(abs(v_min), abs(v_max), 1.0e-12)
    return {"min": v_min, "max": v_max, "span": span, "relative_span": span / scale}


def green_static(radius: np.ndarray, xi: float, c: float) -> np.ndarray:
    radius = np.asarray(radius, dtype=float)
    out = np.empty_like(radius)
    nonzero = radius > 1.0e-12
    out[nonzero] = (1.0 - np.exp(-2.0 * radius[nonzero] / xi)) / (4.0 * math.pi * c * c * radius[nonzero])
    out[~nonzero] = 1.0 / (2.0 * math.pi * c * c * xi)
    return out


def smooth_cutoff(radius: np.ndarray, cutoff: float, width: float) -> np.ndarray:
    return 0.5 * (1.0 - np.tanh((radius - cutoff) / max(width, 1.0e-12)))


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


def region_breakdown(
    deficit: np.ndarray,
    squared_deficit: np.ndarray,
    potential_density: np.ndarray,
    radius: np.ndarray,
    cell_volume: float,
    edges: list[float],
) -> list[dict[str, float]]:
    bounds = [0.0] + edges + [float(np.max(radius)) + 1.0e-9]
    labels = ["core", "mid", "halo"]
    rows: list[dict[str, float]] = []
    for i in range(len(bounds) - 1):
        inner = float(bounds[i])
        outer = float(bounds[i + 1])
        mask = (radius >= inner) & (radius < outer if i < len(bounds) - 2 else radius <= outer)
        vol = float(np.sum(deficit[mask]) * cell_volume)
        sq = float(np.sum(squared_deficit[mask]) * cell_volume)
        pot = float(np.sum(potential_density[mask]) * cell_volume)
        rows.append(
            {
                "label": labels[i] if i < len(labels) else f"region_{i}",
                "r_inner": inner,
                "r_outer": outer,
                "deficit_volume": vol,
                "squared_deficit_integral": sq,
                "potential_at_probe": pot,
            }
        )
    total_deficit = sum(row["deficit_volume"] for row in rows)
    total_potential = sum(row["potential_at_probe"] for row in rows)
    for row in rows:
        row["deficit_fraction"] = row["deficit_volume"] / max(total_deficit, 1.0e-12)
        row["potential_fraction"] = row["potential_at_probe"] / max(total_potential, 1.0e-12)
    return rows


def cumulative_profile(
    deficit: np.ndarray,
    squared_deficit: np.ndarray,
    potential_density: np.ndarray,
    radius: np.ndarray,
    cell_volume: float,
    bins: int,
) -> list[dict[str, float]]:
    edges = np.linspace(0.0, float(np.max(radius)), bins + 1)
    shell_deficit: list[float] = []
    shell_squared: list[float] = []
    shell_potential: list[float] = []
    rows: list[dict[str, float]] = []

    cumulative_deficit = 0.0
    cumulative_squared = 0.0
    cumulative_potential = 0.0

    for i in range(bins):
        inner = float(edges[i])
        outer = float(edges[i + 1])
        mask = (radius >= inner) & (radius < outer if i < bins - 1 else radius <= outer)
        deficit_value = float(np.sum(deficit[mask]) * cell_volume)
        squared_value = float(np.sum(squared_deficit[mask]) * cell_volume)
        potential_value = float(np.sum(potential_density[mask]) * cell_volume)
        shell_deficit.append(deficit_value)
        shell_squared.append(squared_value)
        shell_potential.append(potential_value)
        cumulative_deficit += deficit_value
        cumulative_squared += squared_value
        cumulative_potential += potential_value
        rows.append(
            {
                "r_inner": inner,
                "r_outer": outer,
                "r_mid": 0.5 * (inner + outer),
                "shell_deficit_volume": deficit_value,
                "shell_squared_deficit_integral": squared_value,
                "shell_potential_at_probe": potential_value,
                "cumulative_deficit_volume": cumulative_deficit,
                "cumulative_squared_deficit_integral": cumulative_squared,
                "cumulative_potential_at_probe": cumulative_potential,
            }
        )
    return rows


def window_sensitivity(
    deficit: np.ndarray,
    distance_to_probe: np.ndarray,
    radius: np.ndarray,
    cell_volume: float,
    edges: list[float],
    width: float,
    xi: float,
    c: float,
    probe_radius: float,
) -> list[dict[str, float]]:
    kernel = green_static(distance_to_probe, xi=xi, c=c)
    core_edge = edges[0]
    mid_edge = edges[1] if len(edges) > 1 else edges[0]

    windows = {
        "full_domain": np.ones_like(radius),
        "hard_core": (radius <= core_edge).astype(float),
        "hard_mid": (radius <= mid_edge).astype(float),
        "halo_only": (radius >= mid_edge).astype(float),
        "smooth_core": smooth_cutoff(radius, core_edge, width),
        "smooth_mid": smooth_cutoff(radius, mid_edge, width),
    }

    rows: list[dict[str, float]] = []
    for name, weight in windows.items():
        weighted_deficit = deficit * weight
        deficit_volume = float(np.sum(weighted_deficit) * cell_volume)
        potential = float(np.sum(weighted_deficit * kernel) * cell_volume)
        q_p_effective = float(4.0 * math.pi * c * c * probe_radius * potential)
        rows.append(
            {
                "window": name,
                "weighted_deficit_volume": deficit_volume,
                "potential_at_probe": potential,
                "q_p_effective": q_p_effective,
            }
        )
    return rows


def analyze_state(
    path: Path,
    bins: int,
    probe_radius: float,
    region_edges: list[float],
    window_width: float,
    xi: float,
    c: float,
) -> dict[str, object]:
    psi, x, y, z, config, summary, spacing = load_state(path)
    cell_volume = spacing**3
    rho = np.abs(psi) ** 2
    deficit = np.clip(1.0 - rho, 0.0, None)
    squared_deficit = deficit * deficit
    radius = np.sqrt(x * x + y * y + z * z)
    distance_to_probe = np.sqrt((x - probe_radius) ** 2 + y * y + z * z)
    potential_density = deficit * green_static(distance_to_probe, xi=xi, c=c)

    cumulative = cumulative_profile(deficit, squared_deficit, potential_density, radius, cell_volume, bins)
    regions = region_breakdown(deficit, squared_deficit, potential_density, radius, cell_volume, region_edges)
    windows = window_sensitivity(
        deficit,
        distance_to_probe,
        radius,
        cell_volume,
        region_edges,
        window_width,
        xi,
        c,
        probe_radius,
    )

    total_deficit = float(np.sum(deficit) * cell_volume)
    total_squared = float(np.sum(squared_deficit) * cell_volume)
    total_potential = float(np.sum(potential_density) * cell_volume)
    q_p_effective = float(4.0 * math.pi * c * c * probe_radius * total_potential)

    return {
        "state": str(path),
        "n": int(config["n"]),
        "half_width": float(config["half_width"]),
        "steps_completed": int(summary.get("total_steps_effective", summary.get("steps_completed", 0))),
        "raw_residual_norm": float(summary.get("residual_norm", 0.0)),
        "projected_residual_norm": float(summary.get("projected_residual_norm", summary.get("residual_norm", 0.0))),
        "shell_mean_density": float(1.0 - summary.get("far_field_shell_deficit", 0.0)),
        "probe_radius": probe_radius,
        "totals": {
            "deficit_volume": total_deficit,
            "squared_deficit_integral": total_squared,
            "potential_at_probe": total_potential,
            "q_p_effective": q_p_effective,
        },
        "region_breakdown": regions,
        "window_sensitivity": windows,
        "cumulative_profile": cumulative,
    }


def cross_state_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    sorted_rows = sorted(rows, key=lambda row: (float(row["half_width"]), int(row["n"])))
    totals_q = [float(row["totals"]["q_p_effective"]) for row in sorted_rows]
    totals_v = [float(row["totals"]["deficit_volume"]) for row in sorted_rows]
    shell_density = [float(row["shell_mean_density"]) for row in sorted_rows]

    transitions = []
    for previous, current in zip(sorted_rows, sorted_rows[1:]):
        prev_q = float(previous["totals"]["q_p_effective"])
        curr_q = float(current["totals"]["q_p_effective"])
        prev_v = float(previous["totals"]["deficit_volume"])
        curr_v = float(current["totals"]["deficit_volume"])
        transitions.append(
            {
                "from_half_width": float(previous["half_width"]),
                "to_half_width": float(current["half_width"]),
                "q_p_effective_relative_change": abs(curr_q - prev_q) / max(abs(curr_q), abs(prev_q), 1.0e-12),
                "deficit_volume_relative_change": abs(curr_v - prev_v) / max(abs(curr_v), abs(prev_v), 1.0e-12),
                "shell_density_relative_change": abs(float(current["shell_mean_density"]) - float(previous["shell_mean_density"]))
                / max(abs(float(current["shell_mean_density"])), abs(float(previous["shell_mean_density"])), 1.0e-12),
            }
        )

    return {
        "q_p_effective": metric_span(totals_q),
        "deficit_volume": metric_span(totals_v),
        "shell_mean_density": metric_span(shell_density),
        "transitions": transitions,
    }


def main() -> None:
    args = parse_args()
    region_edges = parse_float_list(args.region_edges)
    if len(region_edges) < 1:
        raise SystemExit("At least one region edge is required.")
    if len(region_edges) == 1:
        region_edges = [region_edges[0], region_edges[0] * 2.0]

    rows = [
        analyze_state(
            path,
            bins=args.bins,
            probe_radius=args.probe_radius,
            region_edges=region_edges,
            window_width=args.window_width,
            xi=args.xi,
            c=args.c,
        )
        for path in args.states
    ]
    rows.sort(key=lambda row: (float(row["half_width"]), int(row["n"])))

    payload = {
        "probe_radius": float(args.probe_radius),
        "region_edges": region_edges,
        "window_width": float(args.window_width),
        "xi": float(args.xi),
        "c": float(args.c),
        "rows": rows,
        "cross_state_summary": cross_state_summary(rows),
        "interpretation": {
            "purpose": "Localize where the static source grows: cumulative radial build-up, core/mid/halo split, and sensitivity to reasonable source windows.",
            "warning": "This is a mechanism probe on saved prototype states. Large changes across half_width can still reflect missing large-box closure in the underlying trefoil state.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

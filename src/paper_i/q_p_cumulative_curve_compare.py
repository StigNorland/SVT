"""Compare cumulative Q_p(<r) curves across plateaued saved trefoil states on shared physical radii.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: cumulative static-potential coefficient on shared radii, normalized cumulative fractions
Primary role: test whether different half_width branches share any common interior source-build-up regime.
Key limitation: this compares saved prototype states and does not by itself resolve which support functional is physical.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare cumulative Q_p(<r) curves across shared physical radii.")
    parser.add_argument("states", nargs="+", type=Path, help="Saved .npz states from trefoil_breather_static.py")
    parser.add_argument(
        "--sample-radii",
        default="1,2,3,4,5,6,7,8",
        help="Comma-separated shared radii in xi units for curve comparison.",
    )
    parser.add_argument("--bins", type=int, default=80, help="Internal radial resolution for cumulative interpolation.")
    parser.add_argument("--probe-radius", type=float, default=12.0)
    parser.add_argument("--xi", type=float, default=1.0)
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
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


def cumulative_profile(
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
                "r_outer": outer,
                "cumulative_q_p_effective": cumulative_q,
            }
        )
    return rows


def interpolate_cumulative(profile: list[dict[str, float]], radius: float) -> float:
    if not profile:
        return 0.0
    radii = np.array([float(row["r_outer"]) for row in profile], dtype=float)
    values = np.array([float(row["cumulative_q_p_effective"]) for row in profile], dtype=float)
    if radius <= radii[0]:
        return float(values[0])
    if radius >= radii[-1]:
        return float(values[-1])
    return float(np.interp(radius, radii, values))


def analyze_state(path: Path, sample_radii: list[float], bins: int, probe_radius: float, xi: float, c: float) -> dict[str, object]:
    psi, x, y, z, config, summary, spacing = load_state(path)
    cell_volume = spacing**3
    radius = np.sqrt(x * x + y * y + z * z)
    deficit = np.clip(1.0 - np.abs(psi) ** 2, 0.0, None)
    distance_to_probe = np.sqrt((x - probe_radius) ** 2 + y * y + z * z)
    kernel = green_static(distance_to_probe, xi=xi, c=c)

    profile = cumulative_profile(deficit, radius, kernel, cell_volume, bins, probe_radius, c)
    total_q = float(profile[-1]["cumulative_q_p_effective"]) if profile else 0.0
    r_max = math.sqrt(3.0) * float(config["half_width"])
    blend_start = max((1.0 - float(config.get("boundary_blend_fraction", 0.0))) * r_max, 0.0)

    samples = []
    for sample_radius in sample_radii:
        q_value = interpolate_cumulative(profile, sample_radius)
        samples.append(
            {
                "radius": float(sample_radius),
                "q_p_effective": q_value,
                "normalized_fraction": q_value / max(total_q, 1.0e-12),
                "inside_blend_start": bool(sample_radius <= blend_start),
            }
        )

    return {
        "state": str(path),
        "n": int(config["n"]),
        "half_width": float(config["half_width"]),
        "steps_completed": int(summary.get("total_steps_effective", summary.get("steps_completed", 0))),
        "projected_residual_norm": float(summary.get("projected_residual_norm", summary.get("residual_norm", 0.0))),
        "shell_mean_density": float(1.0 - summary.get("far_field_shell_deficit", 0.0)),
        "blend_start_radius": blend_start,
        "total_q_p_effective": total_q,
        "samples": samples,
    }


def cross_state_summary(rows: list[dict[str, object]], sample_radii: list[float]) -> dict[str, object]:
    sample_summary = []
    for sample_radius in sample_radii:
        q_values = []
        normalized = []
        inside_flags = []
        for row in rows:
            for sample in row["samples"]:
                if abs(float(sample["radius"]) - sample_radius) < 1.0e-9:
                    q_values.append(float(sample["q_p_effective"]))
                    normalized.append(float(sample["normalized_fraction"]))
                    inside_flags.append(bool(sample["inside_blend_start"]))
        sample_summary.append(
            {
                "radius": float(sample_radius),
                "q_p_effective": metric_span(q_values),
                "normalized_fraction": metric_span(normalized),
                "inside_blend_start_for_all_states": bool(all(inside_flags)),
            }
        )
    return {"by_radius": sample_summary}


def main() -> None:
    args = parse_args()
    sample_radii = parse_float_list(args.sample_radii)
    rows = [analyze_state(path, sample_radii, args.bins, args.probe_radius, args.xi, args.c) for path in args.states]
    rows.sort(key=lambda row: (float(row["half_width"]), int(row["n"])))

    payload = {
        "sample_radii": sample_radii,
        "bins": int(args.bins),
        "probe_radius": float(args.probe_radius),
        "xi": float(args.xi),
        "c": float(args.c),
        "rows": rows,
        "cross_state_summary": cross_state_summary(rows, sample_radii),
        "interpretation": {
            "purpose": "Compare cumulative Q_p(<r) across shared interior radii to see whether different half_width branches share any common source-build-up regime.",
            "warning": "Large spread at shared radii means the interior source already disagrees before any boundary recovery layer begins.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

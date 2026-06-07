"""Compute direct static-source diagnostics from saved trefoil states.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: deficit-volume integral, squared-deficit integral, direct static potential, asymptotic 1/r coefficient
Primary role: extract the actual static-source signal implied by the saved proton states using the full linearised LogSE Green's function
Key limitation: this uses the linearised scalar-sector Green's function only and does not include any chiral-shear corrections.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute direct static-source diagnostics from saved trefoil states.")
    parser.add_argument("states", nargs="+", type=Path, help="Saved .npz states from trefoil_breather_static.py")
    parser.add_argument(
        "--probe-radii",
        default="8,10,12,16,20",
        help="Comma-separated probe radii in xi units for evaluating the static potential on the +x axis.",
    )
    parser.add_argument(
        "--xi",
        type=float,
        default=1.0,
        help="Carrier healing length xi in the current nondimensionalisation.",
    )
    parser.add_argument(
        "--c",
        type=float,
        default=1.0,
        help="Long-wavelength carrier speed c in the current nondimensionalisation.",
    )
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


def relative_drift(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-12)


def green_static(radius: np.ndarray, xi: float, c: float) -> np.ndarray:
    """Static Green's function of the linearised scalar LogSE density sector.

    G(r) = (1 - exp(-2 r / xi)) / (4 pi c^2 r)

    with the finite r -> 0 limit handled explicitly.
    """
    radius = np.asarray(radius, dtype=float)
    out = np.empty_like(radius)
    nonzero = radius > 1.0e-12
    out[nonzero] = (1.0 - np.exp(-2.0 * radius[nonzero] / xi)) / (4.0 * math.pi * c * c * radius[nonzero])
    out[~nonzero] = 1.0 / (2.0 * math.pi * c * c * xi)
    return out


def load_state(path: Path, probe_radii: list[float], xi: float, c: float) -> dict[str, object]:
    data = np.load(path, allow_pickle=False)
    psi = data["psi_real"] + 1j * data["psi_imag"]
    x = data["x"]
    y = data["y"]
    z = data["z"]
    config = json.loads(str(data["config"]))
    summary = json.loads(str(data["summary"]))

    spacing = float(x[1, 0, 0] - x[0, 0, 0]) if x.shape[0] > 1 else 0.0
    cell_volume = spacing**3
    rho = np.abs(psi) ** 2
    deficit = np.clip(1.0 - rho, 0.0, None)

    deficit_volume = float(np.sum(deficit) * cell_volume)
    squared_deficit_integral = float(np.sum(deficit * deficit) * cell_volume)

    potentials: list[dict[str, float]] = []
    asymptotic_samples: list[float] = []
    for radius in probe_radii:
        distance = np.sqrt((x - radius) ** 2 + y * y + z * z)
        potential = float(np.sum(deficit * green_static(distance, xi=xi, c=c)) * cell_volume)
        q_p_sample = float(4.0 * math.pi * c * c * radius * potential)
        potentials.append(
            {
                "radius": float(radius),
                "potential": potential,
                "q_p_asymptotic_sample": q_p_sample,
            }
        )
        asymptotic_samples.append(q_p_sample)

    tail_count = min(3, len(asymptotic_samples))
    tail_values = asymptotic_samples[-tail_count:]
    q_p_asymptotic_fit = float(sum(tail_values) / max(len(tail_values), 1))

    return {
        "state": str(path),
        "n": int(config["n"]),
        "half_width": float(config["half_width"]),
        "steps_completed": int(summary["steps_completed"]),
        "residual_norm": float(summary["residual_norm"]),
        "shell_mean_density": float(1.0 - summary["far_field_shell_deficit"]),
        "shell_mean_deficit": float(summary["far_field_shell_deficit"]),
        "deficit_volume": deficit_volume,
        "squared_deficit_integral": squared_deficit_integral,
        "potentials": potentials,
        "q_p_asymptotic_fit": q_p_asymptotic_fit,
        "q_p_asymptotic_tail_span": metric_span(tail_values),
    }


def main() -> None:
    args = parse_args()
    probe_radii = parse_float_list(args.probe_radii)
    rows = [load_state(path, probe_radii, xi=args.xi, c=args.c) for path in args.states]
    rows.sort(key=lambda row: (row["n"], row["half_width"], row["steps_completed"]))

    by_n: dict[int, list[dict[str, object]]] = {}
    by_half_width: dict[float, list[dict[str, object]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), []).append(row)
        by_half_width.setdefault(float(row["half_width"]), []).append(row)

    by_n_summary = {
        str(n): {
            "half_width_values": [float(row["half_width"]) for row in entries],
            "deficit_volume": metric_span([float(row["deficit_volume"]) for row in entries]),
            "squared_deficit_integral": metric_span([float(row["squared_deficit_integral"]) for row in entries]),
            "q_p_asymptotic_fit": metric_span([float(row["q_p_asymptotic_fit"]) for row in entries]),
            "shell_mean_density": metric_span([float(row["shell_mean_density"]) for row in entries]),
        }
        for n, entries in sorted(by_n.items())
    }

    cross_resolution = {}
    for half_width, entries in sorted(by_half_width.items()):
        if len(entries) < 2:
            continue
        entries = sorted(entries, key=lambda row: row["n"])
        coarse = entries[0]
        fine = entries[-1]
        cross_resolution[str(half_width)] = {
            "coarse_n": int(coarse["n"]),
            "fine_n": int(fine["n"]),
            "deficit_volume": {
                "coarse": float(coarse["deficit_volume"]),
                "fine": float(fine["deficit_volume"]),
                "relative_drift": relative_drift(float(coarse["deficit_volume"]), float(fine["deficit_volume"])),
            },
            "squared_deficit_integral": {
                "coarse": float(coarse["squared_deficit_integral"]),
                "fine": float(fine["squared_deficit_integral"]),
                "relative_drift": relative_drift(
                    float(coarse["squared_deficit_integral"]), float(fine["squared_deficit_integral"])
                ),
            },
            "q_p_asymptotic_fit": {
                "coarse": float(coarse["q_p_asymptotic_fit"]),
                "fine": float(fine["q_p_asymptotic_fit"]),
                "relative_drift": relative_drift(float(coarse["q_p_asymptotic_fit"]), float(fine["q_p_asymptotic_fit"])),
            },
            "shell_mean_density": {
                "coarse": float(coarse["shell_mean_density"]),
                "fine": float(fine["shell_mean_density"]),
                "relative_drift": relative_drift(float(coarse["shell_mean_density"]), float(fine["shell_mean_density"])),
            },
        }

    payload = {
        "probe_radii": probe_radii,
        "xi": float(args.xi),
        "c": float(args.c),
        "green_function": "G(r) = (1 - exp(-2 r / xi)) / (4 pi c^2 r)",
        "rows": rows,
        "by_n": by_n_summary,
        "cross_resolution": cross_resolution,
        "interpretation": {
            "purpose": "Compute direct static-source diagnostics: bare deficit volume, squared-deficit integral, and the actual potential sourced through the linearised LogSE static Green's function.",
            "warning": "The asymptotic coefficient is only as trustworthy as the convergence of the underlying static state.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

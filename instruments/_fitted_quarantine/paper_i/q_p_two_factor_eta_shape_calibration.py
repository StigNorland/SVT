"""Calibrate additive saturating Q_p strength by normalized cross-branch shape agreement.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: matched-half-width shape agreement between coarse and fine branches
Primary role: choose a provisional eta by asking which value best aligns the normalized half-width dependence across resolutions
Key limitation: this is still a reduced consistency criterion rather than a physical derivation of eta.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calibrate additive saturating Q_p strength by normalized branch shape agreement.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Geometry-aware sweep JSON files")
    parser.add_argument("--eta-values", default="0.02,0.05,0.1,0.15,0.2,0.3,0.5,0.75,1.0,1.5,2.0,3.0,4.0,5.0,7.5,10.0")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def parse_float_list(text: str) -> list[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def load_rows(paths: list[Path]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for run in payload.get("runs", []):
            summary = run["summary"]
            effective_radius = float(summary["effective_radius"])
            equivalent_deficit_radius = float(summary["equivalent_deficit_radius"])
            saturating = equivalent_deficit_radius / max(effective_radius + equivalent_deficit_radius, 1.0e-12)
            rows.append(
                {
                    "n": int(run["config"]["n"]),
                    "half_width": float(run["config"]["half_width"]),
                    "shell_deficit": float(run["shell_mean_deficit"]),
                    "saturating": saturating,
                }
            )
    rows.sort(key=lambda row: (row["n"], row["half_width"]))
    return rows


def normalize(values: list[float]) -> list[float]:
    scale = sum(values) / max(len(values), 1)
    scale = max(scale, 1.0e-12)
    return [value / scale for value in values]


def main() -> None:
    args = parse_args()
    eta_values = parse_float_list(args.eta_values)
    rows = load_rows(args.inputs)

    by_n: dict[int, dict[float, dict[str, float]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), {})[float(row["half_width"])] = row

    n_values = sorted(by_n)
    if len(n_values) < 2:
        raise ValueError("Need at least two resolution branches for eta shape calibration.")

    coarse_n = n_values[0]
    fine_n = n_values[-1]
    matched_half_widths = sorted(set(by_n[coarse_n]).intersection(by_n[fine_n]))

    scan_rows: list[dict[str, object]] = []
    for eta in eta_values:
        coarse_values = [
            by_n[coarse_n][half_width]["shell_deficit"] + eta * by_n[coarse_n][half_width]["saturating"]
            for half_width in matched_half_widths
        ]
        fine_values = [
            by_n[fine_n][half_width]["shell_deficit"] + eta * by_n[fine_n][half_width]["saturating"]
            for half_width in matched_half_widths
        ]
        coarse_norm = normalize(coarse_values)
        fine_norm = normalize(fine_values)
        pair_rows: list[dict[str, float]] = []
        squared_errors: list[float] = []
        abs_errors: list[float] = []
        for half_width, coarse_value, fine_value in zip(matched_half_widths, coarse_norm, fine_norm):
            abs_error = abs(coarse_value - fine_value)
            abs_errors.append(abs_error)
            squared_errors.append(abs_error**2)
            pair_rows.append(
                {
                    "half_width": half_width,
                    "coarse_normalized": coarse_value,
                    "fine_normalized": fine_value,
                    "absolute_error": abs_error,
                }
            )
        mse = sum(squared_errors) / max(len(squared_errors), 1)
        mae = sum(abs_errors) / max(len(abs_errors), 1)
        scan_rows.append(
            {
                "eta": eta,
                "matched_pairs": pair_rows,
                "coarse_values": coarse_values,
                "fine_values": fine_values,
                "coarse_normalized_values": coarse_norm,
                "fine_normalized_values": fine_norm,
                "mean_absolute_shape_error": mae,
                "mean_squared_shape_error": mse,
            }
        )

    best_by_mae = min(scan_rows, key=lambda item: item["mean_absolute_shape_error"])
    best_by_mse = min(scan_rows, key=lambda item: item["mean_squared_shape_error"])

    payload = {
        "coarse_n": coarse_n,
        "fine_n": fine_n,
        "matched_half_widths": matched_half_widths,
        "scan": scan_rows,
        "best_by_mae": best_by_mae,
        "best_by_mse": best_by_mse,
        "interpretation": {
            "purpose": "Choose a provisional eta for the additive saturating reduced Q_p family by matching the normalized half-width dependence across resolutions.",
            "normalization": "Each branch is normalized by its own mean over the matched half-width set before comparison.",
            "warning": "This is a shape-consistency calibration only; it does not determine an absolute physical scale.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

"""Scan re-expressed additive saturating Q_p probes with geometry-tied scales.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: branch-wise spread of re-expressed additive saturating Q_p probes
Primary role: replace the bare epsilon of the additive saturating family with geometry-derived branch scales
Key limitation: this is still a reduced ansatz scan, not a derivation of Q_p.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan geometry-scaled additive saturating Q_p probes.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Geometry-aware sweep JSON files")
    parser.add_argument("--eta-values", default="0.25,0.5,1.0,1.5,2.0,3.0")
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


def load_rows(paths: list[Path]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for run in payload.get("runs", []):
            summary = run["summary"]
            shell_deficit = float(run["shell_mean_deficit"])
            effective_radius = float(summary["effective_radius"])
            equivalent_deficit_radius = float(summary["equivalent_deficit_radius"])
            saturating = equivalent_deficit_radius / max(effective_radius + equivalent_deficit_radius, 1.0e-12)
            rows.append(
                {
                    "n": int(run["config"]["n"]),
                    "half_width": float(run["config"]["half_width"]),
                    "shell_deficit": shell_deficit,
                    "saturating": saturating,
                    "ratio": shell_deficit / max(saturating, 1.0e-12),
                }
            )
    rows.sort(key=lambda row: (row["n"], row["half_width"]))
    return rows


def mean(values: list[float]) -> float:
    return sum(values) / max(len(values), 1)


def median(values: list[float]) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def main() -> None:
    args = parse_args()
    eta_values = parse_float_list(args.eta_values)
    rows = load_rows(args.inputs)

    by_n: dict[int, list[dict[str, float]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), []).append(row)

    branch_scales = {
        str(n): {
            "mean_ratio": mean([row["ratio"] for row in entries]),
            "median_ratio": median([row["ratio"] for row in entries]),
            "ratio_of_means": mean([row["shell_deficit"] for row in entries]) / max(mean([row["saturating"] for row in entries]), 1.0e-12),
        }
        for n, entries in by_n.items()
    }

    scan_rows: list[dict[str, object]] = []
    for eta in eta_values:
        entry: dict[str, object] = {"eta": eta, "by_n": {}}
        for n, entries in sorted(by_n.items()):
            scales = branch_scales[str(n)]
            values_mean_ratio = [row["shell_deficit"] + eta * scales["mean_ratio"] * row["saturating"] for row in entries]
            values_median_ratio = [row["shell_deficit"] + eta * scales["median_ratio"] * row["saturating"] for row in entries]
            values_ratio_of_means = [
                row["shell_deficit"] + eta * scales["ratio_of_means"] * row["saturating"] for row in entries
            ]
            entry["by_n"][str(n)] = {
                "half_width_values": [row["half_width"] for row in entries],
                "candidate_mean_ratio_scale": metric_span(values_mean_ratio),
                "candidate_median_ratio_scale": metric_span(values_median_ratio),
                "candidate_ratio_of_means_scale": metric_span(values_ratio_of_means),
            }
        scan_rows.append(entry)

    best_by_n: dict[str, object] = {}
    for n in sorted(by_n):
        best_mean = min(scan_rows, key=lambda item: item["by_n"][str(n)]["candidate_mean_ratio_scale"]["relative_span"])
        best_median = min(scan_rows, key=lambda item: item["by_n"][str(n)]["candidate_median_ratio_scale"]["relative_span"])
        best_rom = min(scan_rows, key=lambda item: item["by_n"][str(n)]["candidate_ratio_of_means_scale"]["relative_span"])
        best_by_n[str(n)] = {
            "mean_ratio_scale": {"eta": best_mean["eta"], "candidate_span": best_mean["by_n"][str(n)]["candidate_mean_ratio_scale"]},
            "median_ratio_scale": {"eta": best_median["eta"], "candidate_span": best_median["by_n"][str(n)]["candidate_median_ratio_scale"]},
            "ratio_of_means_scale": {"eta": best_rom["eta"], "candidate_span": best_rom["by_n"][str(n)]["candidate_ratio_of_means_scale"]},
        }

    payload = {
        "branch_scales": branch_scales,
        "scan": scan_rows,
        "best_by_n": best_by_n,
        "interpretation": {
            "purpose": "Replace the bare epsilon of the additive saturating family with branch geometry scales derived from shell-deficit-to-saturating ratios.",
            "warning": "These re-expressions are still reduced probes; better numerical conditioning does not make the resulting scale physical by itself.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

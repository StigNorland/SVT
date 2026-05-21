"""Calibrate the additive saturating Q_p strength by cross-branch consistency.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: matched-half-width consistency between coarse and fine branches
Primary role: choose a provisional eta for the additive saturating reduced Q_p family using an explicit numerical criterion
Key limitation: this is a consistency-based calibration only; it does not derive a physical coupling constant.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calibrate additive saturating Q_p strength by cross-branch consistency.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Geometry-aware sweep JSON files")
    parser.add_argument("--eta-values", default="0.02,0.05,0.1,0.15,0.2,0.3,0.5,0.75,1.0,1.5,2.0,3.0,4.0,5.0,7.5,10.0")
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


def relative_mismatch(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-12)


def main() -> None:
    args = parse_args()
    eta_values = parse_float_list(args.eta_values)
    rows = load_rows(args.inputs)

    by_n: dict[int, dict[float, dict[str, float]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), {})[float(row["half_width"])] = row

    n_values = sorted(by_n)
    if len(n_values) < 2:
        raise ValueError("Need at least two resolution branches for eta calibration.")

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
        pair_rows: list[dict[str, float]] = []
        mismatches: list[float] = []
        for half_width, coarse_value, fine_value in zip(matched_half_widths, coarse_values, fine_values):
            mismatch = relative_mismatch(coarse_value, fine_value)
            mismatches.append(mismatch)
            pair_rows.append(
                {
                    "half_width": half_width,
                    "coarse_value": coarse_value,
                    "fine_value": fine_value,
                    "relative_mismatch": mismatch,
                }
            )
        coarse_span = metric_span(coarse_values)
        fine_span = metric_span(fine_values)
        mean_mismatch = sum(mismatches) / max(len(mismatches), 1)
        score = mean_mismatch + 0.5 * (coarse_span["relative_span"] + fine_span["relative_span"])
        scan_rows.append(
            {
                "eta": eta,
                "matched_pairs": pair_rows,
                "coarse_span": coarse_span,
                "fine_span": fine_span,
                "mean_relative_mismatch": mean_mismatch,
                "score": score,
            }
        )

    best_by_score = min(scan_rows, key=lambda item: item["score"])
    best_by_mismatch = min(scan_rows, key=lambda item: item["mean_relative_mismatch"])

    payload = {
        "coarse_n": coarse_n,
        "fine_n": fine_n,
        "matched_half_widths": matched_half_widths,
        "scan": scan_rows,
        "best_by_score": best_by_score,
        "best_by_mismatch": best_by_mismatch,
        "interpretation": {
            "purpose": "Choose a provisional eta for the additive saturating reduced Q_p family by balancing branch-internal spread against coarse-fine consistency at matched half-width.",
            "score_definition": "score = mean_relative_mismatch + 0.5 * (coarse_relative_span + fine_relative_span)",
            "warning": "This is a numerical consistency calibration, not a physical derivation of eta.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

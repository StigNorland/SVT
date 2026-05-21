"""Build a checkpoint artifact for the provisionally calibrated additive saturating Q_p ansatz.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: calibrated additive saturating Q_p values, branch spans, normalized cross-branch shape agreement
Primary role: package the current eta-calibrated reduced Q_p ansatz into one reusable checkpoint artifact
Key limitation: eta remains a provisional consistency-based calibration rather than a derived physical constant.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a checkpoint for the calibrated additive saturating Q_p ansatz.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Geometry-aware sweep JSON files")
    parser.add_argument("--eta", type=float, default=0.5, help="Provisionally calibrated additive saturating strength")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def metric_span(values: list[float]) -> dict[str, float]:
    if not values:
        return {"min": 0.0, "max": 0.0, "span": 0.0, "relative_span": 0.0}
    v_min = min(values)
    v_max = max(values)
    span = v_max - v_min
    scale = max(abs(v_min), abs(v_max), 1.0e-12)
    return {"min": v_min, "max": v_max, "span": span, "relative_span": span / scale}


def normalize(values: list[float]) -> list[float]:
    scale = sum(values) / max(len(values), 1)
    scale = max(scale, 1.0e-12)
    return [value / scale for value in values]


def load_rows(paths: list[Path], eta: float) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for run in payload.get("runs", []):
            summary = run["summary"]
            shell_deficit = float(run["shell_mean_deficit"])
            effective_radius = float(summary["effective_radius"])
            equivalent_deficit_radius = float(summary["equivalent_deficit_radius"])
            saturating = equivalent_deficit_radius / max(effective_radius + equivalent_deficit_radius, 1.0e-12)
            q_p_value = shell_deficit + eta * saturating
            rows.append(
                {
                    "source": str(path),
                    "n": int(run["config"]["n"]),
                    "half_width": float(run["config"]["half_width"]),
                    "steps_completed": int(summary["steps_completed"]),
                    "residual_norm": float(summary["residual_norm"]),
                    "shell_deficit": shell_deficit,
                    "effective_radius": effective_radius,
                    "equivalent_deficit_radius": equivalent_deficit_radius,
                    "saturating": saturating,
                    "q_p_calibrated": q_p_value,
                }
            )
    rows.sort(key=lambda row: (row["n"], row["half_width"], row["steps_completed"]))
    return rows


def main() -> None:
    args = parse_args()
    rows = load_rows(args.inputs, args.eta)

    by_n: dict[int, list[dict[str, float]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), []).append(row)

    by_n_summary = {
        str(n): {
            "half_width_values": [float(row["half_width"]) for row in entries],
            "shell_deficit": metric_span([float(row["shell_deficit"]) for row in entries]),
            "q_p_calibrated": metric_span([float(row["q_p_calibrated"]) for row in entries]),
        }
        for n, entries in sorted(by_n.items())
    }

    matched_pairs: list[dict[str, float]] = []
    n_values = sorted(by_n)
    if len(n_values) >= 2:
        coarse_entries = {float(row["half_width"]): row for row in by_n[n_values[0]]}
        fine_entries = {float(row["half_width"]): row for row in by_n[n_values[-1]]}
        half_widths = sorted(set(coarse_entries).intersection(fine_entries))
        coarse_values = [float(coarse_entries[half_width]["q_p_calibrated"]) for half_width in half_widths]
        fine_values = [float(fine_entries[half_width]["q_p_calibrated"]) for half_width in half_widths]
        coarse_norm = normalize(coarse_values)
        fine_norm = normalize(fine_values)
        for half_width, coarse_value, fine_value, coarse_value_norm, fine_value_norm in zip(
            half_widths, coarse_values, fine_values, coarse_norm, fine_norm
        ):
            matched_pairs.append(
                {
                    "half_width": half_width,
                    "coarse_value": coarse_value,
                    "fine_value": fine_value,
                    "coarse_normalized": coarse_value_norm,
                    "fine_normalized": fine_value_norm,
                    "absolute_shape_error": abs(coarse_value_norm - fine_value_norm),
                }
            )

    payload = {
        "eta": args.eta,
        "rows": rows,
        "summary": {
            "shell_deficit": metric_span([float(row["shell_deficit"]) for row in rows]),
            "q_p_calibrated": metric_span([float(row["q_p_calibrated"]) for row in rows]),
        },
        "by_n": by_n_summary,
        "matched_pairs": matched_pairs,
        "interpretation": {
            "purpose": "Checkpoint artifact for the provisionally calibrated additive saturating reduced Q_p ansatz.",
            "calibration_reference": "Uses the current shape-consistency calibration eta = 0.5 unless overridden.",
            "warning": "This is still a reduced ansatz checkpoint rather than a derived monopole calibration.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

"""Scan local-geometry re-expressions of the additive saturating Q_p probe.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: branch-wise spread of local-geometry additive Q_p probes
Primary role: test whether run-local geometric scales outperform both shell deficit alone and branch-scale re-expressions
Key limitation: this remains a reduced ansatz scan rather than a derivation of Q_p.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan local-geometry additive Q_p probes.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Geometry-aware sweep JSON files")
    parser.add_argument("--eta-values", default="0.1,0.25,0.5,1.0,1.5,2.0,3.0,4.0,5.0")
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
            deficit_volume = float(summary["deficit_volume"])
            compactness = equivalent_deficit_radius / max(effective_radius, 1.0e-12)
            saturating = equivalent_deficit_radius / max(effective_radius + equivalent_deficit_radius, 1.0e-12)
            volume_fraction = deficit_volume / max(effective_radius**3 + deficit_volume, 1.0e-12)
            rows.append(
                {
                    "n": int(run["config"]["n"]),
                    "half_width": float(run["config"]["half_width"]),
                    "shell_deficit": shell_deficit,
                    "compactness": compactness,
                    "saturating": saturating,
                    "volume_fraction": volume_fraction,
                }
            )
    rows.sort(key=lambda row: (row["n"], row["half_width"]))
    return rows


def main() -> None:
    args = parse_args()
    eta_values = parse_float_list(args.eta_values)
    rows = load_rows(args.inputs)

    by_n: dict[int, list[dict[str, float]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), []).append(row)

    scan_rows: list[dict[str, object]] = []
    for eta in eta_values:
        entry: dict[str, object] = {"eta": eta, "by_n": {}}
        for n, entries in sorted(by_n.items()):
            values_shell_saturating = [
                row["shell_deficit"] + eta * row["shell_deficit"] * row["saturating"] for row in entries
            ]
            values_shell_compactness = [
                row["shell_deficit"] + eta * row["shell_deficit"] * row["compactness"] for row in entries
            ]
            values_shell_volume_fraction = [
                row["shell_deficit"] + eta * row["shell_deficit"] * row["volume_fraction"] for row in entries
            ]
            values_shell_mixed_local = [
                row["shell_deficit"] + eta * row["shell_deficit"] * 0.5 * (row["saturating"] + row["volume_fraction"])
                for row in entries
            ]
            entry["by_n"][str(n)] = {
                "half_width_values": [row["half_width"] for row in entries],
                "candidate_shell_saturating_local": metric_span(values_shell_saturating),
                "candidate_shell_compactness_local": metric_span(values_shell_compactness),
                "candidate_shell_volume_fraction_local": metric_span(values_shell_volume_fraction),
                "candidate_shell_mixed_local": metric_span(values_shell_mixed_local),
            }
        scan_rows.append(entry)

    best_by_n: dict[str, object] = {}
    for n in sorted(by_n):
        best_shell_saturating = min(
            scan_rows,
            key=lambda item: item["by_n"][str(n)]["candidate_shell_saturating_local"]["relative_span"],
        )
        best_shell_compactness = min(
            scan_rows,
            key=lambda item: item["by_n"][str(n)]["candidate_shell_compactness_local"]["relative_span"],
        )
        best_shell_volume_fraction = min(
            scan_rows,
            key=lambda item: item["by_n"][str(n)]["candidate_shell_volume_fraction_local"]["relative_span"],
        )
        best_shell_mixed = min(
            scan_rows,
            key=lambda item: item["by_n"][str(n)]["candidate_shell_mixed_local"]["relative_span"],
        )
        best_by_n[str(n)] = {
            "shell_saturating_local": {
                "eta": best_shell_saturating["eta"],
                "candidate_span": best_shell_saturating["by_n"][str(n)]["candidate_shell_saturating_local"],
            },
            "shell_compactness_local": {
                "eta": best_shell_compactness["eta"],
                "candidate_span": best_shell_compactness["by_n"][str(n)]["candidate_shell_compactness_local"],
            },
            "shell_volume_fraction_local": {
                "eta": best_shell_volume_fraction["eta"],
                "candidate_span": best_shell_volume_fraction["by_n"][str(n)]["candidate_shell_volume_fraction_local"],
            },
            "shell_mixed_local": {
                "eta": best_shell_mixed["eta"],
                "candidate_span": best_shell_mixed["by_n"][str(n)]["candidate_shell_mixed_local"],
            },
        }

    payload = {
        "scan": scan_rows,
        "best_by_n": best_by_n,
        "interpretation": {
            "purpose": "Test run-local geometry scales as re-expressions of the additive saturating reduced Q_p family.",
            "warning": "Local numerical improvement alone does not establish a physical Q_p map.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

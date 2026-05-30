"""Scan purely additive local-geometry Q_p probes without shell-deficit weighting.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: branch-wise spread of pure additive local-geometry Q_p probes
Primary role: test whether local geometric scales enter additively (no Pi_shell multiplier)
             outperform both shell deficit alone and the shell-weighted local-scale family
Key limitation: this remains a reduced ansatz scan rather than a derivation of Q_p.

The correction term is

    Pi_Q = Pi_shell + eta * G_local

where G_local is one of four local geometric scales.  This is the same G_local family
tested in q_p_two_factor_local_scale_scan, but with the Pi_shell multiplier removed.
The saturating variant at a given eta therefore reproduces the bare additive scan exactly,
providing a cross-check baseline.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan purely additive local-geometry Q_p probes (no shell-deficit multiplier)."
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="Geometry-aware sweep JSON files")
    parser.add_argument(
        "--eta-values",
        default="0.1,0.25,0.5,1.0,1.5,2.0,3.0,4.0,5.0,7.5,10.0",
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
            saturating = equivalent_deficit_radius / max(
                effective_radius + equivalent_deficit_radius, 1.0e-12
            )
            volume_fraction = deficit_volume / max(
                effective_radius**3 + deficit_volume, 1.0e-12
            )
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
            values_saturating = [
                row["shell_deficit"] + eta * row["saturating"] for row in entries
            ]
            values_compactness = [
                row["shell_deficit"] + eta * row["compactness"] for row in entries
            ]
            values_volume_fraction = [
                row["shell_deficit"] + eta * row["volume_fraction"] for row in entries
            ]
            values_mixed = [
                row["shell_deficit"]
                + eta * 0.5 * (row["saturating"] + row["volume_fraction"])
                for row in entries
            ]
            entry["by_n"][str(n)] = {
                "half_width_values": [row["half_width"] for row in entries],
                "candidate_saturating": metric_span(values_saturating),
                "candidate_compactness": metric_span(values_compactness),
                "candidate_volume_fraction": metric_span(values_volume_fraction),
                "candidate_mixed": metric_span(values_mixed),
            }
        scan_rows.append(entry)

    best_by_n: dict[str, object] = {}
    for n in sorted(by_n):
        best_saturating = min(
            scan_rows,
            key=lambda item: item["by_n"][str(n)]["candidate_saturating"]["relative_span"],
        )
        best_compactness = min(
            scan_rows,
            key=lambda item: item["by_n"][str(n)]["candidate_compactness"]["relative_span"],
        )
        best_volume_fraction = min(
            scan_rows,
            key=lambda item: item["by_n"][str(n)]["candidate_volume_fraction"]["relative_span"],
        )
        best_mixed = min(
            scan_rows,
            key=lambda item: item["by_n"][str(n)]["candidate_mixed"]["relative_span"],
        )
        best_by_n[str(n)] = {
            "saturating": {
                "eta": best_saturating["eta"],
                "candidate_span": best_saturating["by_n"][str(n)]["candidate_saturating"],
            },
            "compactness": {
                "eta": best_compactness["eta"],
                "candidate_span": best_compactness["by_n"][str(n)]["candidate_compactness"],
            },
            "volume_fraction": {
                "eta": best_volume_fraction["eta"],
                "candidate_span": best_volume_fraction["by_n"][str(n)]["candidate_volume_fraction"],
            },
            "mixed": {
                "eta": best_mixed["eta"],
                "candidate_span": best_mixed["by_n"][str(n)]["candidate_mixed"],
            },
        }

    payload = {
        "scan": scan_rows,
        "best_by_n": best_by_n,
        "interpretation": {
            "purpose": (
                "Test purely additive local geometric scales as Q_p probes, "
                "with no Pi_shell multiplier on the correction term. "
                "The saturating variant cross-checks the bare additive scan."
            ),
            "warning": (
                "Local numerical improvement alone does not establish a physical Q_p map."
            ),
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

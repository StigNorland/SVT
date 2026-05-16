"""Scan a branch-normalized additive saturating Q_p probe.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: branch-wise spread of normalized additive saturating Q_p probes
Primary role: replace a bare additive coefficient with a branch-scaled dimensionless eta
Key limitation: this is still a reduced ansatz scan, not a derivation of Q_p.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan a branch-normalized additive saturating Q_p probe.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Geometry-aware sweep JSON files")
    parser.add_argument("--eta-values", default="0.25,0.5,1.0,1.5,2.0,3.0,4.0")
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

    branch_scales = {
        str(n): sum(row["shell_deficit"] for row in entries) / max(len(entries), 1)
        for n, entries in by_n.items()
    }

    scan_rows: list[dict[str, object]] = []
    for eta in eta_values:
        entry: dict[str, object] = {"eta": eta, "by_n": {}}
        for n, entries in sorted(by_n.items()):
            scale = branch_scales[str(n)]
            values = [row["shell_deficit"] + eta * scale * row["saturating"] for row in entries]
            entry["by_n"][str(n)] = {
                "half_width_values": [row["half_width"] for row in entries],
                "shell_deficit_scale": scale,
                "candidate_span": metric_span(values),
            }
        scan_rows.append(entry)

    best_by_n: dict[str, object] = {}
    for n in sorted(by_n):
        best = min(scan_rows, key=lambda item: item["by_n"][str(n)]["candidate_span"]["relative_span"])
        best_by_n[str(n)] = {
            "eta": best["eta"],
            "shell_deficit_scale": best["by_n"][str(n)]["shell_deficit_scale"],
            "candidate_span": best["by_n"][str(n)]["candidate_span"],
        }

    payload = {
        "branch_scales": branch_scales,
        "scan": scan_rows,
        "best_by_n": best_by_n,
        "interpretation": {
            "purpose": "Test a dimensionless normalized additive saturating Q_p family using branch mean shell deficit as the correction scale.",
            "warning": "A numerically preferred eta is not yet a physical constant, and branch normalization is itself only a provisional device.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

"""Probe simple two-factor Q_p candidates from geometry-aware sweep outputs.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: shell deficit, equivalent deficit radius, simple combined Q_p candidates
Primary role: explore whether a two-factor static-branch ansatz is more stable than shell suppression alone for issue #14
Key limitation: this script probes reduced candidate forms only; it does not derive Q_p or alpha_G.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe simple two-factor Q_p candidates from geometry-aware sweep JSON files.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Sweep JSON files produced by trefoil_breather_refinement.py")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def metric_span(values: list[float]) -> dict[str, float]:
    if not values:
        return {"min": 0.0, "max": 0.0, "span": 0.0, "relative_span": 0.0}
    v_min = min(values)
    v_max = max(values)
    span = v_max - v_min
    scale = max(abs(v_min), abs(v_max), 1.0e-12)
    return {
        "min": v_min,
        "max": v_max,
        "span": span,
        "relative_span": span / scale,
    }


def build_row(source: Path, run: dict[str, object]) -> dict[str, object]:
    summary = run["summary"]
    shell_deficit = float(run["shell_mean_deficit"])
    effective_radius = float(summary["effective_radius"])
    equivalent_deficit_radius = float(summary["equivalent_deficit_radius"])

    # Reduced two-factor candidates. These are intentionally simple probes,
    # not endorsed formulas.
    q_p_linear = shell_deficit * equivalent_deficit_radius
    q_p_area = shell_deficit * equivalent_deficit_radius**2
    q_p_volume = shell_deficit * equivalent_deficit_radius**3
    q_p_volume_compact = shell_deficit * (equivalent_deficit_radius / max(effective_radius, 1.0e-12)) ** 3
    q_p_shell_compact = shell_deficit * (equivalent_deficit_radius / max(effective_radius, 1.0e-12))
    q_p_shell_compact_sq = shell_deficit * (equivalent_deficit_radius / max(effective_radius, 1.0e-12)) ** 2
    q_p_shell_saturating = shell_deficit * (
        equivalent_deficit_radius / max(effective_radius + equivalent_deficit_radius, 1.0e-12)
    )
    compactness = equivalent_deficit_radius / max(effective_radius, 1.0e-12)
    q_p_candidate_add_compact_01 = shell_deficit + 0.1 * compactness
    q_p_candidate_add_compact_001 = shell_deficit + 0.01 * compactness
    q_p_candidate_add_saturating_01 = shell_deficit + 0.1 * (
        equivalent_deficit_radius / max(effective_radius + equivalent_deficit_radius, 1.0e-12)
    )

    return {
        "source": str(source),
        "n": int(run["config"]["n"]),
        "half_width": float(run["config"]["half_width"]),
        "steps_completed": int(summary["steps_completed"]),
        "residual_norm": float(summary["residual_norm"]),
        "shell_deficit": shell_deficit,
        "effective_radius": effective_radius,
        "equivalent_deficit_radius": equivalent_deficit_radius,
        "q_p_candidate_linear": q_p_linear,
        "q_p_candidate_area": q_p_area,
        "q_p_candidate_volume": q_p_volume,
        "q_p_candidate_volume_compact": q_p_volume_compact,
        "q_p_candidate_shell_compact": q_p_shell_compact,
        "q_p_candidate_shell_compact_sq": q_p_shell_compact_sq,
        "q_p_candidate_shell_saturating": q_p_shell_saturating,
        "q_p_candidate_add_compact_01": q_p_candidate_add_compact_01,
        "q_p_candidate_add_compact_001": q_p_candidate_add_compact_001,
        "q_p_candidate_add_saturating_01": q_p_candidate_add_saturating_01,
    }


def main() -> None:
    args = parse_args()
    rows: list[dict[str, object]] = []
    for path in args.inputs:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for run in payload.get("runs", []):
            rows.append(build_row(path, run))

    rows.sort(key=lambda row: (row["n"], row["half_width"], row["steps_completed"]))

    summary = {
        "shell_deficit": metric_span([float(row["shell_deficit"]) for row in rows]),
        "q_p_candidate_linear": metric_span([float(row["q_p_candidate_linear"]) for row in rows]),
        "q_p_candidate_area": metric_span([float(row["q_p_candidate_area"]) for row in rows]),
        "q_p_candidate_volume": metric_span([float(row["q_p_candidate_volume"]) for row in rows]),
        "q_p_candidate_volume_compact": metric_span([float(row["q_p_candidate_volume_compact"]) for row in rows]),
        "q_p_candidate_shell_compact": metric_span([float(row["q_p_candidate_shell_compact"]) for row in rows]),
        "q_p_candidate_shell_compact_sq": metric_span([float(row["q_p_candidate_shell_compact_sq"]) for row in rows]),
        "q_p_candidate_shell_saturating": metric_span(
            [float(row["q_p_candidate_shell_saturating"]) for row in rows]
        ),
        "q_p_candidate_add_compact_01": metric_span([float(row["q_p_candidate_add_compact_01"]) for row in rows]),
        "q_p_candidate_add_compact_001": metric_span([float(row["q_p_candidate_add_compact_001"]) for row in rows]),
        "q_p_candidate_add_saturating_01": metric_span(
            [float(row["q_p_candidate_add_saturating_01"]) for row in rows]
        ),
    }

    by_n: dict[int, list[dict[str, object]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), []).append(row)

    by_n_summary = {
        str(n): {
            "half_width_values": [float(row["half_width"]) for row in entries],
            "shell_deficit": metric_span([float(row["shell_deficit"]) for row in entries]),
            "q_p_candidate_linear": metric_span([float(row["q_p_candidate_linear"]) for row in entries]),
            "q_p_candidate_area": metric_span([float(row["q_p_candidate_area"]) for row in entries]),
            "q_p_candidate_volume": metric_span([float(row["q_p_candidate_volume"]) for row in entries]),
            "q_p_candidate_volume_compact": metric_span(
                [float(row["q_p_candidate_volume_compact"]) for row in entries]
            ),
            "q_p_candidate_shell_compact": metric_span(
                [float(row["q_p_candidate_shell_compact"]) for row in entries]
            ),
            "q_p_candidate_shell_compact_sq": metric_span(
                [float(row["q_p_candidate_shell_compact_sq"]) for row in entries]
            ),
            "q_p_candidate_shell_saturating": metric_span(
                [float(row["q_p_candidate_shell_saturating"]) for row in entries]
            ),
            "q_p_candidate_add_compact_01": metric_span(
                [float(row["q_p_candidate_add_compact_01"]) for row in entries]
            ),
            "q_p_candidate_add_compact_001": metric_span(
                [float(row["q_p_candidate_add_compact_001"]) for row in entries]
            ),
            "q_p_candidate_add_saturating_01": metric_span(
                [float(row["q_p_candidate_add_saturating_01"]) for row in entries]
            ),
        }
        for n, entries in sorted(by_n.items())
    }

    payload = {
        "rows": rows,
        "summary": summary,
        "by_n": by_n_summary,
        "interpretation": {
            "purpose": "Compare simple two-factor Q_p probes against shell deficit alone.",
            "warning": "Lower spread here does not make a candidate physical; it only makes it a numerically cleaner reduced ansatz to investigate next.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

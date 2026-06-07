"""Compare geometry-level Q_p calibration diagnostics across saved states.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: compactness ratio, deficit-volume ratio, shell-to-volume ratio
Primary role: small comparison harness for geometry constraints relevant to issue #14
Key limitation: this is a comparison tool for candidate diagnostics, not a calibration solver.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare saved cq_geometry_proxy outputs.")
    parser.add_argument("inputs", nargs="+", type=Path, help="JSON files produced by cq_geometry_proxy.py")
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


def main() -> None:
    args = parse_args()
    rows: list[dict[str, object]] = []
    for path in args.inputs:
        payload = json.loads(path.read_text(encoding="utf-8"))
        config = payload["config"]
        summary = payload["summary"]
        geom = payload["geometry"]
        rows.append(
            {
                "source": str(path),
                "n": int(config["n"]),
                "half_width": float(config["half_width"]),
                "steps_completed": int(summary["steps_completed"]),
                "residual_norm": float(summary["residual_norm"]),
                "shell_deficit": float(geom["shell_deficit"]),
                "deficit_volume": float(geom["deficit_volume"]),
                "equivalent_deficit_radius": float(geom["equivalent_deficit_radius"]),
                "compactness_ratio": float(geom["compactness_ratio"]),
                "deficit_volume_over_radius_cubed": float(geom["deficit_volume_over_radius_cubed"]),
                "shell_to_volume_ratio": float(geom["shell_to_volume_ratio"]),
            }
        )

    rows.sort(key=lambda row: (row["n"], row["half_width"]))
    payload = {
        "rows": rows,
        "summary": {
            "compactness_ratio": metric_span([float(row["compactness_ratio"]) for row in rows]),
            "deficit_volume_over_radius_cubed": metric_span(
                [float(row["deficit_volume_over_radius_cubed"]) for row in rows]
            ),
            "shell_to_volume_ratio": metric_span([float(row["shell_to_volume_ratio"]) for row in rows]),
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

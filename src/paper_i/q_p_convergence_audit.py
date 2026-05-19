"""Audit whether the static trefoil branch is converged enough for Q_p extraction.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: shell density/deficit drift across half_width and across resolution
Primary role: quantify the current numerical ceiling on any reduced Q_p extracted from saved static states
Key limitation: this script audits saved sweep and continuation outputs only; it does not improve the solver itself.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Q_p-relevant convergence from geometry-aware sweep outputs.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Geometry-aware sweep JSON files")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def relative_drift(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-12)


def load_rows(paths: list[Path]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if "runs" in payload:
            for run in payload.get("runs", []):
                rows.append(
                    {
                        "source": path.as_posix(),
                        "n": int(run["config"]["n"]),
                        "half_width": float(run["config"]["half_width"]),
                        "steps_completed": int(run["summary"].get("total_steps_effective", run["summary"].get("steps_completed", 0))),
                        "shell_mean_density": float(run["shell_mean_density"]),
                        "shell_mean_deficit": float(run["shell_mean_deficit"]),
                        "residual_norm": float(run["summary"]["residual_norm"]),
                        "projected_residual_norm": float(run["summary"].get("projected_residual_norm", run["summary"]["residual_norm"])),
                        "deficit_volume": float(run["summary"]["deficit_volume"]),
                        "equivalent_deficit_radius": float(run["summary"]["equivalent_deficit_radius"]),
                    }
                )
            continue

        if "rows" in payload:
            for entry in payload.get("rows", []):
                config = entry.get("config", {})
                chunks = entry.get("chunks", [])
                if not chunks:
                    continue
                last = chunks[-1]
                summary = last["summary"]
                shell_mean_density = float(last.get("shell_mean_density", summary["far_field_shell_density"]))
                rows.append(
                    {
                        "source": path.as_posix(),
                        "n": int(config["n"]),
                        "half_width": float(config["half_width"]),
                        "steps_completed": int(summary.get("total_steps_effective", summary.get("steps_completed", 0))),
                        "shell_mean_density": shell_mean_density,
                        "shell_mean_deficit": 1.0 - shell_mean_density,
                        "residual_norm": float(last.get("raw_residual_norm", summary["residual_norm"])),
                        "projected_residual_norm": float(last.get("projected_residual_norm", summary.get("projected_residual_norm", summary["residual_norm"]))),
                        "deficit_volume": float(last["deficit_volume"]),
                        "equivalent_deficit_radius": float(summary["equivalent_deficit_radius"]),
                    }
                )

    latest: dict[tuple[int, float], dict[str, float]] = {}
    for row in rows:
        key = (int(row["n"]), float(row["half_width"]))
        current = latest.get(key)
        if current is None or int(row["steps_completed"]) > int(current["steps_completed"]):
            latest[key] = row

    deduped = sorted(latest.values(), key=lambda row: (row["n"], row["half_width"]))
    return deduped


def main() -> None:
    args = parse_args()
    rows = load_rows(args.inputs)

    by_n: dict[int, list[dict[str, float]]] = {}
    by_half_width: dict[float, list[dict[str, float]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), []).append(row)
        by_half_width.setdefault(float(row["half_width"]), []).append(row)

    within_branch = {}
    for n, entries in sorted(by_n.items()):
        within_branch[str(n)] = {}
        for key in ["shell_mean_density", "shell_mean_deficit", "deficit_volume", "equivalent_deficit_radius", "residual_norm", "projected_residual_norm"]:
            values = [float(entry[key]) for entry in entries]
            v_min = min(values)
            v_max = max(values)
            within_branch[str(n)][key] = {
                "min": v_min,
                "max": v_max,
                "relative_drift": relative_drift(v_min, v_max),
            }

    cross_resolution = {}
    for half_width, entries in sorted(by_half_width.items()):
        if len(entries) < 2:
            continue
        entries = sorted(entries, key=lambda entry: entry["n"])
        coarse = entries[0]
        fine = entries[-1]
        cross_resolution[str(half_width)] = {
            "coarse_n": int(coarse["n"]),
            "fine_n": int(fine["n"]),
            "shell_mean_density": {
                "coarse": float(coarse["shell_mean_density"]),
                "fine": float(fine["shell_mean_density"]),
                "relative_drift": relative_drift(float(coarse["shell_mean_density"]), float(fine["shell_mean_density"])),
            },
            "shell_mean_deficit": {
                "coarse": float(coarse["shell_mean_deficit"]),
                "fine": float(fine["shell_mean_deficit"]),
                "relative_drift": relative_drift(float(coarse["shell_mean_deficit"]), float(fine["shell_mean_deficit"])),
            },
            "deficit_volume": {
                "coarse": float(coarse["deficit_volume"]),
                "fine": float(fine["deficit_volume"]),
                "relative_drift": relative_drift(float(coarse["deficit_volume"]), float(fine["deficit_volume"])),
            },
            "equivalent_deficit_radius": {
                "coarse": float(coarse["equivalent_deficit_radius"]),
                "fine": float(fine["equivalent_deficit_radius"]),
                "relative_drift": relative_drift(
                    float(coarse["equivalent_deficit_radius"]), float(fine["equivalent_deficit_radius"])
                ),
            },
            "residual_norm": {
                "coarse": float(coarse["residual_norm"]),
                "fine": float(fine["residual_norm"]),
                "relative_drift": relative_drift(float(coarse["residual_norm"]), float(fine["residual_norm"])),
            },
            "projected_residual_norm": {
                "coarse": float(coarse["projected_residual_norm"]),
                "fine": float(fine["projected_residual_norm"]),
                "relative_drift": relative_drift(float(coarse["projected_residual_norm"]), float(fine["projected_residual_norm"])),
            },
        }

    shell_density_ceiling = max(
        item["shell_mean_density"]["relative_drift"] for item in cross_resolution.values()
    ) if cross_resolution else 0.0
    shell_density_best_case = min(
        item["shell_mean_density"]["relative_drift"] for item in cross_resolution.values()
    ) if cross_resolution else 0.0

    payload = {
        "rows": rows,
        "within_branch": within_branch,
        "cross_resolution": cross_resolution,
        "ceiling": {
            "best_case_shell_mean_density_cross_resolution_drift": shell_density_best_case,
            "worst_case_shell_mean_density_cross_resolution_drift": shell_density_ceiling,
            "statement": "Any reduced Q_p extracted from the current static states inherits at least this level of coarse-fine uncertainty before additional modeling uncertainty is added.",
        },
        "interpretation": {
            "purpose": "Quantify whether the static trefoil branch is independently converged in half_width and resolution before further Q_p ansatz fitting.",
            "warning": "Large shell-deficit drift means reduced Q_p fitting can fall below the current solver noise floor.",
            "residual_note": "For constrained continuation states, projected_residual_norm is the relevant stationarity measure; raw residual_norm includes forbidden off-manifold directions.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

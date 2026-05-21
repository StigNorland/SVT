"""Compare constrained fine-grid box-size trend across selected plateau/source-flat states.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: deficit volume, asymptotic static-source coefficient, shell density, projected residual
Primary role: compare the trusted constrained fine-grid reference states across half_width values
Key limitation: this only compares saved continuation artifacts; it does not generate new states.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare constrained fine-grid box-size trend across saved states.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Continuation JSON artifacts to compare")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def relative_change(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-12)


def load_rows(paths: list[Path]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for entry in payload.get("rows", []):
            chunks = entry.get("chunks", [])
            if not chunks:
                continue
            last = chunks[-1]
            summary = last["summary"]
            rows.append(
                {
                    "source": str(path),
                    "n": int(entry["config"]["n"]),
                    "half_width": float(entry["config"]["half_width"]),
                    "steps_completed": int(summary.get("total_steps_effective", summary.get("steps_completed", 0))),
                    "stop_reason": entry.get("stop_reason", "unknown"),
                    "deficit_volume": float(last["deficit_volume"]),
                    "q_p_asymptotic_fit": float(last["q_p_asymptotic_fit"]),
                    "shell_mean_density": float(last["shell_mean_density"]),
                    "raw_residual_norm": float(last.get("raw_residual_norm", summary["residual_norm"])),
                    "projected_residual_norm": float(last.get("projected_residual_norm", summary.get("projected_residual_norm", summary["residual_norm"]))),
                }
            )
    best_by_half_width: dict[float, dict[str, object]] = {}
    for row in rows:
        key = float(row["half_width"])
        current = best_by_half_width.get(key)
        if current is None:
            best_by_half_width[key] = row
            continue
        current_score = (
            1 if current["stop_reason"] == "plateau_reached" else 0,
            int(current["n"]),
            int(current["steps_completed"]),
        )
        row_score = (
            1 if row["stop_reason"] == "plateau_reached" else 0,
            int(row["n"]),
            int(row["steps_completed"]),
        )
        if row_score > current_score:
            best_by_half_width[key] = row

    selected = sorted(best_by_half_width.values(), key=lambda row: (row["half_width"], row["n"], row["steps_completed"]))
    return selected


def build_payload(rows: list[dict[str, object]]) -> dict[str, object]:
    trend = []
    for index, row in enumerate(rows):
        item = dict(row)
        if index > 0:
            prev = rows[index - 1]
            item["delta_from_previous"] = {
                "from_half_width": float(prev["half_width"]),
                "deficit_volume_relative_change": relative_change(float(prev["deficit_volume"]), float(row["deficit_volume"])),
                "q_p_asymptotic_fit_relative_change": relative_change(
                    float(prev["q_p_asymptotic_fit"]), float(row["q_p_asymptotic_fit"])
                ),
                "shell_mean_density_relative_change": relative_change(
                    float(prev["shell_mean_density"]), float(row["shell_mean_density"])
                ),
                "projected_residual_relative_change": relative_change(
                    float(prev["projected_residual_norm"]), float(row["projected_residual_norm"])
                ),
            }
        trend.append(item)

    return {
        "rows": rows,
        "trend": trend,
        "interpretation": {
            "purpose": "Compare the constrained fine-grid box-size trend across the currently trusted plateau or source-flat states.",
            "warning": "Differences here mix box-size and any remaining resolution differences between the chosen reference states.",
        },
    }


def main() -> None:
    args = parse_args()
    rows = load_rows(args.inputs)
    payload = build_payload(rows)
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

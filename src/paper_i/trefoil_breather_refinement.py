"""Refinement sweep harness for the static trefoil-breather prototype.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: final energy, residual norm, effective radius, depressed fraction, shell density
Primary role: first grid / box sensitivity harness for issue #13 milestone 4
Key limitation: compares the early prototype solver only; it does not validate a closure-grade Y-junction result.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import Nondimensionalisation, OutputStatus, RelaxationControls, ScriptMetadata

from trefoil_breather_static import TrefoilConfig, coordinate_grid, relax
from trefoil_observables import shell_mean_density


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("final_energy", "residual_norm", "effective_radius", "depressed_fraction", "shell_mean_density"),
    diagnostics=("grid_sensitivity", "box_sensitivity"),
    issue_refs=("#13",),
    limitations=(
        "Uses the early static prototype solver rather than a closure-grade Y-junction solver.",
    ),
)


def parse_int_list(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def parse_float_list(text: str) -> list[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refinement sweep for the static trefoil-breather prototype.")
    parser.add_argument("--n-values", default="24,32,40")
    parser.add_argument("--half-width-values", default="5.0,6.0,7.0")
    parser.add_argument("--major-radius", type=float, default=2.8)
    parser.add_argument("--minor-radius", type=float, default=0.85)
    parser.add_argument("--smoothing-radius", type=float, default=0.2)
    parser.add_argument("--log-pressure", type=float, default=0.5)
    parser.add_argument("--step-size", type=float, default=0.005)
    parser.add_argument("--max-steps", type=int, default=40)
    parser.add_argument("--tolerance", type=float, default=2.0e-3)
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


def build_comparison_summary(runs: list[dict[str, object]]) -> dict[str, object]:
    energies = [float(run["summary"]["final_energy"]) for run in runs]
    residuals = [float(run["summary"]["residual_norm"]) for run in runs]
    radii = [float(run["summary"]["effective_radius"]) for run in runs]
    depressed = [float(run["summary"]["depressed_fraction"]) for run in runs]
    shell_densities = [float(run["shell_mean_density"]) for run in runs]

    by_n: dict[int, list[dict[str, object]]] = {}
    by_half_width: dict[float, list[dict[str, object]]] = {}
    for run in runs:
        n = int(run["config"]["n"])
        half_width = float(run["config"]["half_width"])
        by_n.setdefault(n, []).append(run)
        by_half_width.setdefault(half_width, []).append(run)

    return {
        "global": {
            "final_energy": metric_span(energies),
            "residual_norm": metric_span(residuals),
            "effective_radius": metric_span(radii),
            "depressed_fraction": metric_span(depressed),
            "shell_mean_density": metric_span(shell_densities),
        },
        "by_n": {
            str(n): {
                "half_width_values": [float(entry["config"]["half_width"]) for entry in entries],
                "final_energy": metric_span([float(entry["summary"]["final_energy"]) for entry in entries]),
                "residual_norm": metric_span([float(entry["summary"]["residual_norm"]) for entry in entries]),
                "effective_radius": metric_span([float(entry["summary"]["effective_radius"]) for entry in entries]),
            }
            for n, entries in sorted(by_n.items())
        },
        "by_half_width": {
            str(half_width): {
                "n_values": [int(entry["config"]["n"]) for entry in entries],
                "final_energy": metric_span([float(entry["summary"]["final_energy"]) for entry in entries]),
                "residual_norm": metric_span([float(entry["summary"]["residual_norm"]) for entry in entries]),
                "effective_radius": metric_span([float(entry["summary"]["effective_radius"]) for entry in entries]),
            }
            for half_width, entries in sorted(by_half_width.items())
        },
    }


def main() -> None:
    args = parse_args()
    n_values = parse_int_list(args.n_values)
    half_width_values = parse_float_list(args.half_width_values)
    controls = RelaxationControls(
        step_size=args.step_size,
        max_steps=args.max_steps,
        tolerance=args.tolerance,
    )

    runs: list[dict[str, object]] = []
    for n in n_values:
        for half_width in half_width_values:
            cfg = TrefoilConfig(
                n=n,
                half_width=half_width,
                major_radius=args.major_radius,
                minor_radius=args.minor_radius,
                smoothing_radius=args.smoothing_radius,
                log_pressure=args.log_pressure,
            )
            psi, summary = relax(cfg, controls)
            x, y, z = coordinate_grid(cfg)
            shell_density = shell_mean_density(
                psi,
                x,
                y,
                z,
                shell_inner=max(0.7 * half_width, 0.0),
                shell_outer=0.95 * half_width,
            )
            runs.append(
                {
                    "config": asdict(cfg),
                    "summary": asdict(summary),
                    "shell_mean_density": shell_density,
                }
            )

    payload = {
        "metadata": {
            "problem_type": SCRIPT_METADATA.problem_type,
            "status": SCRIPT_METADATA.status.value,
            "nondimensionalisation": SCRIPT_METADATA.nondimensionalisation,
            "observables": SCRIPT_METADATA.observables,
            "diagnostics": SCRIPT_METADATA.diagnostics,
            "issue_refs": SCRIPT_METADATA.issue_refs,
            "limitations": SCRIPT_METADATA.limitations,
        },
        "nondimensionalisation": asdict(Nondimensionalisation()),
        "controls": asdict(controls),
        "runs": runs,
        "comparison_summary": build_comparison_summary(runs),
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

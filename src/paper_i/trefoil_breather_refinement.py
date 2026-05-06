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
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

"""Refinement sweep for the asymmetric closed Y-junction relaxation + extraction.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: final energy, mu_0_grid, N_Y / L, F_int, plus the line / node decomposition
Primary role: grid + box sensitivity gate for the asymmetric (+1,+1,-1) closed
              Y-junction.  This is the first multi-filament configuration with a
              stable seeded geometry, so it is the first candidate to promote
              from `prototype` to `validation` on the Y-junction track.
Key limitation: extraction parameters (r_tube, r_node, cal_half_width) are held
                fixed across the sweep; mu_0 is grid-spacing-dependent.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, RelaxationControls, ScriptMetadata
from trefoil_y_junction_closed_asym_static import (
    YJunctionClosedAsymConfig,
    coordinate_grid,
    relax,
)
from trefoil_y_junction_closed_observables import ExtractionConfig, extract


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=(
        "final_energy",
        "residual_norm",
        "mu_0_grid",
        "N_Y_per_filament_length",
        "F_factor_interior",
    ),
    diagnostics=("grid_sensitivity", "box_sensitivity"),
    issue_refs=("#13",),
    limitations=(
        "Extraction parameters (r_tube, r_node, cal_half_width) are held fixed across the sweep.",
        "Asymmetric (+1, +1, -1) closed theta-graph Y-junction only.",
    ),
)


def parse_int_list(text: str) -> list[int]:
    return [int(p.strip()) for p in text.split(",") if p.strip()]


def parse_float_list(text: str) -> list[float]:
    return [float(p.strip()) for p in text.split(",") if p.strip()]


def steps_for_n(n: int, base_n: int = 24, base_steps: int = 200, cap: int = 400) -> int:
    scale = (n / base_n) ** 2
    return min(cap, int(round(base_steps * scale)))


def run_one(
    n: int,
    half_width: float,
    max_steps: int,
    r_tube: float,
    r_node: float,
    cal_half_width: float,
    output_dir: Path,
    state_tag: str,
) -> dict:
    cfg = YJunctionClosedAsymConfig(n=n, half_width=half_width)
    controls = RelaxationControls(
        step_size=0.01,
        max_steps=max_steps,
        tolerance=2.0e-3,
        min_step_size=1.0e-5,
        max_step_size=5.0e-2,
        check_interval=10,
        patience_intervals=3,
        energy_tol=1.0e-9,
    )
    psi, relax_summary = relax(cfg, controls)

    x_grid, y_grid, z_grid = coordinate_grid(cfg)
    state = {
        "cfg": asdict(cfg),
        "psi": psi,
        "x": x_grid,
        "y": y_grid,
        "z": z_grid,
    }
    ec = ExtractionConfig(
        r_tube=r_tube,
        r_node=r_node,
        cal_half_width=cal_half_width,
    )
    extract_summary = extract(state, ec)

    state_path = (
        output_dir
        / f"y-junction-closed-asym-state-n{n}-hw{int(half_width)}-{max_steps}steps-{state_tag}.npz"
    )
    state_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        state_path,
        psi_real=psi.real,
        psi_imag=psi.imag,
        x=x_grid,
        y=y_grid,
        z=z_grid,
        config=json.dumps(asdict(cfg)),
        controls=json.dumps(asdict(controls)),
        summary=json.dumps(asdict(relax_summary)),
    )

    return {
        "n": n,
        "half_width": half_width,
        "max_steps": max_steps,
        "state_path": str(state_path).replace("\\", "/"),
        "extraction_config": asdict(ec),
        "relaxation": asdict(relax_summary),
        "extraction": asdict(extract_summary),
    }


def summarize_runs(runs: list[dict]) -> list[dict]:
    rows = []
    for run in runs:
        ext = run["extraction"]
        rlx = run["relaxation"]
        rows.append(
            {
                "n": run["n"],
                "half_width": run["half_width"],
                "max_steps": run["max_steps"],
                "final_energy": rlx["final_energy"],
                "residual_norm": rlx["residual_norm"],
                "min_density": rlx["min_density"],
                "e_interior": ext["e_interior"],
                "e_filaments": ext["e_filaments"],
                "e_node_top": ext["e_node_top"],
                "e_node_bottom": ext["e_node_bottom"],
                "e_bulk_residual": ext["e_bulk_residual"],
                "mu_0_grid": ext["mu_0_grid"],
                "l_filament_total_tube": ext["l_filament_total_tube"],
                "n_y_per_xi": ext["n_y_per_xi"],
                "n_y_per_filament_length": ext["n_y_per_filament_length"],
                "f_factor_interior": ext["f_factor_interior"],
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Asymmetric closed Y-junction refinement sweep.")
    parser.add_argument("--n-values", default="24,32,48")
    parser.add_argument("--half-width-values", default="5,6,7")
    parser.add_argument("--r-tube", type=float, default=2.0)
    parser.add_argument("--r-node", type=float, default=2.0)
    parser.add_argument("--cal-half-width", type=float, default=0.5)
    parser.add_argument("--state-tag", default="2026-05-17")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("papers/SSV-I/data"),
        help="Directory in which to save per-run .npz state files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    n_values = parse_int_list(args.n_values)
    hw_values = parse_float_list(args.half_width_values)

    runs: list[dict] = []
    for n in n_values:
        for hw in hw_values:
            max_steps = steps_for_n(n)
            print(
                f"[run] n={n} hw={hw} steps={max_steps}",
                file=sys.stderr,
                flush=True,
            )
            run = run_one(
                n=n,
                half_width=hw,
                max_steps=max_steps,
                r_tube=args.r_tube,
                r_node=args.r_node,
                cal_half_width=args.cal_half_width,
                output_dir=args.state_dir,
                state_tag=args.state_tag,
            )
            runs.append(run)

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
        "extraction_settings": {
            "r_tube": args.r_tube,
            "r_node": args.r_node,
            "cal_half_width": args.cal_half_width,
        },
        "step_scaling_rule": "max_steps = min(400, 200 * (n / 24)^2)",
        "runs": runs,
        "summary_table": summarize_runs(runs),
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

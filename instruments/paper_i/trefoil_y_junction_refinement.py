"""Refinement sweep for the open three-prong Y-junction relaxation + observables.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: final relaxed energy, residual norm, mu_0_grid, N_Y, F
Primary role: first grid + box sensitivity gate for the Y-junction track on issue #13.
Key limitation: the extractor's tube and node radii are held fixed across the sweep,
                so this measures the (n, hw) sensitivity of the chosen extraction
                convention rather than of any geometry-free invariant.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, RelaxationControls, ScriptMetadata
from trefoil_y_junction_static import YJunctionConfig, coordinate_grid, relax
from trefoil_y_junction_observables import ExtractionConfig, extract


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
        "Extraction parameters (r_tube, r_node) are held fixed across the sweep.",
        "Open three-prong Y geometry only.",
    ),
)


def parse_int_list(text: str) -> list[int]:
    return [int(p.strip()) for p in text.split(",") if p.strip()]


def parse_float_list(text: str) -> list[float]:
    return [float(p.strip()) for p in text.split(",") if p.strip()]


def steps_for_n(n: int, base_n: int = 24, base_steps: int = 200, cap: int = 400) -> int:
    """Scale max relaxation steps with grid refinement so that physical evolution
    time is comparable across resolutions (gradient flow time step ~ dx^2),
    capped at a practical maximum to avoid wasted steps past the energy plateau.
    """
    scale = (n / base_n) ** 2
    return min(cap, int(round(base_steps * scale)))


def cal_window_for(half_width: float) -> tuple[float, float]:
    """Pick a self-calibration arc-length slab that fits inside the smallest box.

    Starts just outside the default node ball and stops one xi inside the boundary
    anchor margin so we stay clear of both the junction and the pinned shells.
    """
    cal_start = 2.5
    cal_stop = max(cal_start + 0.5, half_width - 1.5)
    return cal_start, cal_stop


def run_one(
    n: int,
    half_width: float,
    max_steps: int,
    r_tube: float,
    r_node: float,
    cal_start: float,
    cal_stop: float,
    output_dir: Path,
    state_tag: str,
) -> dict:
    cfg = YJunctionConfig(n=n, half_width=half_width)
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
        cal_start=cal_start,
        cal_stop=cal_stop,
    )
    extract_summary = extract(state, ec)

    state_path = (
        output_dir
        / f"y-junction-state-n{n}-hw{int(half_width)}-{max_steps}steps-{state_tag}.npz"
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
                "e_interior": ext["e_interior"],
                "mu_0_grid": ext["mu_0_grid"],
                "l_filament_total": ext["l_filament_total"],
                "n_y_per_xi": ext["n_y_per_xi"],
                "n_y_per_filament_length": ext["n_y_per_filament_length"],
                "f_factor_interior": ext["f_factor_interior"],
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Y-junction refinement sweep.")
    parser.add_argument("--n-values", default="24,32,48")
    parser.add_argument("--half-width-values", default="5,6,7")
    parser.add_argument("--r-tube", type=float, default=2.0)
    parser.add_argument("--r-node", type=float, default=2.0)
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
            cal_start, cal_stop = cal_window_for(hw)
            print(
                f"[run] n={n} hw={hw} steps={max_steps} cal=[{cal_start:.1f},{cal_stop:.1f}]",
                file=sys.stderr,
                flush=True,
            )
            run = run_one(
                n=n,
                half_width=hw,
                max_steps=max_steps,
                r_tube=args.r_tube,
                r_node=args.r_node,
                cal_start=cal_start,
                cal_stop=cal_stop,
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
            "cal_window_rule": "cal_start=2.5, cal_stop=max(3.0, half_width-1.5)",
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

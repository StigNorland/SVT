"""Continue saved trefoil states in step chunks and track convergence-sensitive observables.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: deficit volume, shell density, residual norm, asymptotic static-source coefficient
Primary role: extend saved prototype states without restarting, so convergence of delta V_p and Q_p can be measured directly
Key limitation: this still uses the prototype static trefoil relaxer and linearised scalar-sector Green's function.
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

from shared_numerics import Nondimensionalisation, OutputStatus, ScriptMetadata, RelaxationControls
from trefoil_breather_static import (
    RunSummary,
    TrefoilConfig,
    coordinate_grid,
    load_saved_state,
    relax,
    save_state,
)
from trefoil_observables import deficit_volume


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("deficit_volume", "shell_mean_density", "residual_norm", "q_p_asymptotic_fit"),
    diagnostics=("continuation", "chunkwise_convergence", "static_source_tracking"),
    issue_refs=("#13", "#14"),
    limitations=(
        "Uses the prototype static relaxer rather than a closure-grade Y-junction solver.",
        "Uses the linearised scalar LogSE static Green's function only.",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Continue saved trefoil states in step chunks.")
    parser.add_argument("states", nargs="+", type=Path, help="Saved .npz states from trefoil_breather_static.py")
    parser.add_argument("--step-chunks", default="100", help="Comma-separated extra-step chunks to run sequentially.")
    parser.add_argument("--until-plateau", action="store_true", help="Repeat a fixed chunk size until the source observables flatten.")
    parser.add_argument("--plateau-chunk-size", type=int, default=100, help="Chunk size used when --until-plateau is active.")
    parser.add_argument("--max-chunks", type=int, default=8, help="Maximum number of chunks to run in plateau mode.")
    parser.add_argument("--plateau-hits-required", type=int, default=2, help="Consecutive chunks that must satisfy the plateau criteria.")
    parser.add_argument("--delta-v-tol", type=float, default=0.02, help="Maximum allowed relative change in delta V_p for a plateau hit.")
    parser.add_argument("--q-p-tol", type=float, default=0.02, help="Maximum allowed relative change in Q_p^eff for a plateau hit.")
    parser.add_argument("--shell-density-tol", type=float, default=0.005, help="Maximum allowed absolute change in shell density for a plateau hit.")
    parser.add_argument("--residual-tol", type=float, default=0.05, help="Residual norm threshold for a plateau hit.")
    parser.add_argument("--probe-radii", default="8,10,12,16,20", help="Comma-separated radii for Q_p tail extraction.")
    parser.add_argument("--xi", type=float, default=1.0, help="Carrier healing length xi in the current nondimensionalisation.")
    parser.add_argument("--c", type=float, default=1.0, help="Long-wavelength carrier speed c in the current nondimensionalisation.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for continued states and JSON summaries.")
    parser.add_argument("--output", type=Path, help="Optional aggregate JSON output path.")
    return parser.parse_args()


def parse_int_list(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


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


def relative_change(previous: float, current: float) -> float:
    return abs(current - previous) / max(abs(previous), abs(current), 1.0e-12)


def green_static(radius: np.ndarray, xi: float, c: float) -> np.ndarray:
    radius = np.asarray(radius, dtype=float)
    out = np.empty_like(radius)
    nonzero = radius > 1.0e-12
    out[nonzero] = (1.0 - np.exp(-2.0 * radius[nonzero] / xi)) / (4.0 * math.pi * c * c * radius[nonzero])
    out[~nonzero] = 1.0 / (2.0 * math.pi * c * c * xi)
    return out


def q_p_asymptotic_fit(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    probe_radii: list[float],
    xi: float,
    c: float,
) -> tuple[float, dict[str, float]]:
    x, y, z = coordinate_grid(cfg)
    spacing = cfg.grid.spacing
    deficit = np.clip(1.0 - np.abs(psi) ** 2, 0.0, None)
    cell_volume = spacing**3

    samples: list[float] = []
    for radius in probe_radii:
        distance = np.sqrt((x - radius) ** 2 + y * y + z * z)
        potential = float(np.sum(deficit * green_static(distance, xi=xi, c=c)) * cell_volume)
        samples.append(float(4.0 * math.pi * c * c * radius * potential))

    tail_count = min(3, len(samples))
    tail_values = samples[-tail_count:]
    return float(sum(tail_values) / max(len(tail_values), 1)), metric_span(tail_values)


def controls_for_chunk(saved_controls: RelaxationControls, extra_steps: int) -> RelaxationControls:
    return RelaxationControls(
        step_size=saved_controls.step_size,
        max_steps=extra_steps,
        tolerance=saved_controls.tolerance,
        conserve_l2_norm=saved_controls.conserve_l2_norm,
        min_step_size=saved_controls.min_step_size,
        max_step_size=saved_controls.max_step_size,
        check_interval=saved_controls.check_interval,
        patience_intervals=saved_controls.patience_intervals,
        energy_tol=saved_controls.energy_tol,
        relative_energy_tol=saved_controls.relative_energy_tol,
        line_search_shrink=saved_controls.line_search_shrink,
        max_backtracks=saved_controls.max_backtracks,
        reference_spacing=saved_controls.reference_spacing,
    )


def base_stem(path: Path) -> str:
    stem = path.stem
    cont_marker = "-continued-total"
    if cont_marker in stem:
        return stem.split(cont_marker, 1)[0]
    return stem


def continuation_path(output_dir: Path, source_path: Path, total_steps: int, suffix: str) -> Path:
    return output_dir / f"{base_stem(source_path)}-continued-total{total_steps}{suffix}"


def continue_one_state(
    state_path: Path,
    step_chunks: list[int],
    plateau: dict[str, object] | None,
    probe_radii: list[float],
    xi: float,
    c: float,
    output_dir: Path,
) -> dict[str, object]:
    cfg, saved_controls, psi, saved_summary = load_saved_state(state_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    start_total_steps = int(saved_summary.get("total_steps_effective", saved_summary.get("steps_completed", 0)))
    current_total_steps = start_total_steps
    current_state_path = state_path
    chunk_rows: list[dict[str, object]] = []
    plateau_hits = 0
    stop_reason = "chunk_schedule_completed"

    for chunk_index, extra_steps in enumerate(step_chunks, start=1):
        controls = controls_for_chunk(saved_controls, extra_steps)
        psi, summary = relax(cfg, controls, initial_psi=psi, continued_from_steps=current_total_steps)
        current_total_steps = summary.total_steps_effective

        state_out = continuation_path(output_dir, state_path, current_total_steps, ".npz")
        json_out = continuation_path(output_dir, state_path, current_total_steps, ".json")
        save_state(state_out, psi, cfg, controls, summary)

        q_p_fit, q_p_tail_span = q_p_asymptotic_fit(psi, cfg, probe_radii, xi=xi, c=c)
        row = {
            "chunk_index": chunk_index,
            "source_state": str(current_state_path),
            "continued_state": str(state_out),
            "summary_path": str(json_out),
            "extra_steps": extra_steps,
            "summary": asdict(summary),
            "deficit_volume": deficit_volume(psi, cfg.grid.spacing),
            "shell_mean_density": float(summary.far_field_shell_density),
            "residual_norm": (
                float(summary.projected_residual_norm)
                if controls.conserve_l2_norm
                else float(summary.residual_norm)
            ),
            "raw_residual_norm": float(summary.residual_norm),
            "projected_residual_norm": float(summary.projected_residual_norm),
            "q_p_asymptotic_fit": q_p_fit,
            "q_p_asymptotic_tail_span": q_p_tail_span,
        }
        if chunk_rows:
            previous = chunk_rows[-1]
            delta_v_rel = relative_change(float(previous["deficit_volume"]), float(row["deficit_volume"]))
            q_p_rel = relative_change(float(previous["q_p_asymptotic_fit"]), float(row["q_p_asymptotic_fit"]))
            shell_abs = abs(float(row["shell_mean_density"]) - float(previous["shell_mean_density"]))
            plateau_metrics = {
                "delta_v_relative_change": delta_v_rel,
                "q_p_relative_change": q_p_rel,
                "shell_density_absolute_change": shell_abs,
                "residual_norm": float(row["residual_norm"]),
            }
        else:
            plateau_metrics = None
        row["plateau_metrics"] = plateau_metrics
        json_out.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
        chunk_rows.append(row)
        current_state_path = state_out

        if plateau is not None and plateau_metrics is not None:
            plateau_hit = (
                plateau_metrics["delta_v_relative_change"] <= plateau["delta_v_tol"]
                and plateau_metrics["q_p_relative_change"] <= plateau["q_p_tol"]
                and plateau_metrics["shell_density_absolute_change"] <= plateau["shell_density_tol"]
                and plateau_metrics["residual_norm"] <= plateau["residual_tol"]
            )
            row["plateau_hit"] = plateau_hit
            if plateau_hit:
                plateau_hits += 1
            else:
                plateau_hits = 0
            row["plateau_hits_consecutive"] = plateau_hits
            if plateau_hits >= plateau["hits_required"]:
                stop_reason = "plateau_reached"
                break
        elif plateau is not None:
            row["plateau_hit"] = False
            row["plateau_hits_consecutive"] = plateau_hits

    if plateau is not None and stop_reason != "plateau_reached" and len(chunk_rows) >= plateau["max_chunks"]:
        stop_reason = "max_chunks_reached"

    return {
        "initial_state": str(state_path),
        "config": asdict(cfg),
        "starting_total_steps": start_total_steps,
        "stop_reason": stop_reason,
        "chunks": chunk_rows,
    }


def main() -> None:
    args = parse_args()
    if args.until_plateau:
        step_chunks = [args.plateau_chunk_size] * args.max_chunks
        plateau = {
            "delta_v_tol": args.delta_v_tol,
            "q_p_tol": args.q_p_tol,
            "shell_density_tol": args.shell_density_tol,
            "residual_tol": args.residual_tol,
            "hits_required": args.plateau_hits_required,
            "max_chunks": args.max_chunks,
            "chunk_size": args.plateau_chunk_size,
        }
    else:
        step_chunks = parse_int_list(args.step_chunks)
        plateau = None
    probe_radii = parse_float_list(args.probe_radii)

    rows = [
        continue_one_state(
            state_path=state,
            step_chunks=step_chunks,
            plateau=plateau,
            probe_radii=probe_radii,
            xi=args.xi,
            c=args.c,
            output_dir=args.output_dir,
        )
        for state in args.states
    ]

    final_rows = [row["chunks"][-1] for row in rows if row["chunks"]]
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
        "probe_radii": probe_radii,
        "step_chunks": step_chunks,
        "plateau": plateau,
        "rows": rows,
        "final_chunk_summary": {
            "deficit_volume": metric_span([float(row["deficit_volume"]) for row in final_rows]),
            "shell_mean_density": metric_span([float(row["shell_mean_density"]) for row in final_rows]),
            "residual_norm": metric_span([float(row["residual_norm"]) for row in final_rows]),
            "q_p_asymptotic_fit": metric_span([float(row["q_p_asymptotic_fit"]) for row in final_rows]),
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

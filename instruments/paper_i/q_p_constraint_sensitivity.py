"""Compare source and topology retention under constrained vs unconstrained continuation from the same saved state.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: deficit volume, Q_p^eff, projected/raw residuals, cumulative Q_p(<r) samples, winding retention
Primary role: test whether the interior L2 constraint is selecting the static source/topology branch.
Key limitation: both branches still use the same prototype trefoil relaxer and boundary treatment.
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

from shared_numerics import Nondimensionalisation, OutputStatus, RelaxationControls, ScriptMetadata
from trefoil_breather_static import TrefoilConfig, coordinate_grid, load_saved_state, relax, save_state


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("deficit_volume", "q_p_effective", "projected_residual_norm", "cumulative_curve", "topology_winding_retention"),
    diagnostics=("branch_sensitivity", "constraint_choice", "same_state_comparison", "topology_retention"),
    issue_refs=("#13", "#14"),
    limitations=(
        "Compares only constrained vs unconstrained continuation from the same saved prototype state.",
        "Does not yet test alternative local closure constraints or alternative trefoil skeletons.",
        "Uses a local winding-retention diagnostic, not a full knot invariant.",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare constrained vs unconstrained continuation from the same saved state.")
    parser.add_argument("states", nargs="+", type=Path, help="Saved .npz states used as common branch starts.")
    parser.add_argument("--extra-steps", type=int, default=100, help="Continuation steps per branch variant.")
    parser.add_argument("--probe-radius", type=float, default=12.0)
    parser.add_argument("--sample-radii", default="2,4,6,8", help="Comma-separated radii for cumulative Q_p(<r) samples.")
    parser.add_argument("--xi", type=float, default=1.0)
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def parse_float_list(text: str) -> list[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def green_static(radius: np.ndarray, xi: float, c: float) -> np.ndarray:
    radius = np.asarray(radius, dtype=float)
    out = np.empty_like(radius)
    nonzero = radius > 1.0e-12
    out[nonzero] = (1.0 - np.exp(-2.0 * radius[nonzero] / xi)) / (4.0 * math.pi * c * c * radius[nonzero])
    out[~nonzero] = 1.0 / (2.0 * math.pi * c * c * xi)
    return out


def metric_span(values: list[float]) -> dict[str, float]:
    if not values:
        return {"min": 0.0, "max": 0.0, "span": 0.0, "relative_span": 0.0}
    v_min = min(values)
    v_max = max(values)
    span = v_max - v_min
    scale = max(abs(v_min), abs(v_max), 1.0e-12)
    return {"min": v_min, "max": v_max, "span": span, "relative_span": span / scale}


def variant_controls(saved_controls: RelaxationControls, extra_steps: int, conserve_l2_norm: bool) -> RelaxationControls:
    return RelaxationControls(
        step_size=saved_controls.step_size,
        max_steps=extra_steps,
        tolerance=saved_controls.tolerance,
        conserve_l2_norm=conserve_l2_norm,
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


def q_p_total_and_samples(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    probe_radius: float,
    sample_radii: list[float],
    xi: float,
    c: float,
) -> tuple[float, list[dict[str, float]]]:
    x, y, z = coordinate_grid(cfg)
    spacing = cfg.grid.spacing
    cell_volume = spacing**3
    radius = np.sqrt(x * x + y * y + z * z)
    deficit = np.clip(1.0 - np.abs(psi) ** 2, 0.0, None)
    distance_to_probe = np.sqrt((x - probe_radius) ** 2 + y * y + z * z)
    kernel = green_static(distance_to_probe, xi=xi, c=c)

    total_potential = float(np.sum(deficit * kernel) * cell_volume)
    total_q = float(4.0 * math.pi * c * c * probe_radius * total_potential)

    samples = []
    for sample_radius in sample_radii:
        mask = radius <= sample_radius
        potential = float(np.sum(deficit[mask] * kernel[mask]) * cell_volume)
        q_val = float(4.0 * math.pi * c * c * probe_radius * potential)
        samples.append(
            {
                "radius": float(sample_radius),
                "q_p_effective": q_val,
                "normalized_fraction": q_val / max(total_q, 1.0e-12),
            }
        )
    return total_q, samples


def deficit_volume_value(psi: np.ndarray, cfg: TrefoilConfig) -> float:
    return float(np.sum(np.clip(1.0 - np.abs(psi) ** 2, 0.0, None)) * cfg.grid.spacing**3)


def run_variant(
    state_path: Path,
    label: str,
    conserve_l2_norm: bool,
    extra_steps: int,
    sample_radii: list[float],
    probe_radius: float,
    xi: float,
    c: float,
    output_dir: Path,
) -> dict[str, object]:
    cfg, saved_controls, psi0, saved_summary = load_saved_state(state_path)
    continued_from_steps = int(saved_summary.get("total_steps_effective", saved_summary.get("steps_completed", 0)))
    controls = variant_controls(saved_controls, extra_steps=extra_steps, conserve_l2_norm=conserve_l2_norm)
    psi, summary = relax(cfg, controls, initial_psi=psi0, continued_from_steps=continued_from_steps)
    total_q, cumulative_samples = q_p_total_and_samples(psi, cfg, probe_radius, sample_radii, xi, c)

    stem = state_path.stem
    out_state = output_dir / f"{stem}-{label}-plus{extra_steps}.npz"
    out_json = output_dir / f"{stem}-{label}-plus{extra_steps}.json"
    save_state(out_state, psi, cfg, controls, summary)

    payload = {
        "source_state": str(state_path),
        "variant": label,
        "controls": asdict(controls),
        "summary": asdict(summary),
        "deficit_volume": deficit_volume_value(psi, cfg),
        "q_p_effective": total_q,
        "cumulative_samples": cumulative_samples,
        "topology": {
            "loop_radius": float(summary.topology_loop_radius),
            "mean_winding": float(summary.topology_mean_winding),
            "winding_std": float(summary.topology_winding_std),
            "min_winding": float(summary.topology_min_winding),
            "max_winding": float(summary.topology_max_winding),
            "unit_fraction": float(summary.topology_unit_fraction),
        },
        "saved_state": str(out_state),
    }
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    payload["summary_path"] = str(out_json)
    return payload


def compare_variants(constrained: dict[str, object], unconstrained: dict[str, object]) -> dict[str, object]:
    c_q = float(constrained["q_p_effective"])
    u_q = float(unconstrained["q_p_effective"])
    c_v = float(constrained["deficit_volume"])
    u_v = float(unconstrained["deficit_volume"])
    c_top = constrained["topology"]
    u_top = unconstrained["topology"]
    curve_rows = []
    c_samples = {float(row["radius"]): row for row in constrained["cumulative_samples"]}
    u_samples = {float(row["radius"]): row for row in unconstrained["cumulative_samples"]}
    for radius in sorted(c_samples):
        c_row = c_samples[radius]
        u_row = u_samples[radius]
        curve_rows.append(
            {
                "radius": radius,
                "constrained_q_p_effective": float(c_row["q_p_effective"]),
                "unconstrained_q_p_effective": float(u_row["q_p_effective"]),
                "constrained_fraction": float(c_row["normalized_fraction"]),
                "unconstrained_fraction": float(u_row["normalized_fraction"]),
                "raw_relative_difference": abs(float(c_row["q_p_effective"]) - float(u_row["q_p_effective"]))
                / max(abs(float(c_row["q_p_effective"])), abs(float(u_row["q_p_effective"])), 1.0e-12),
                "fraction_difference": abs(float(c_row["normalized_fraction"]) - float(u_row["normalized_fraction"])),
            }
        )
    return {
        "deficit_volume_relative_difference": abs(c_v - u_v) / max(abs(c_v), abs(u_v), 1.0e-12),
        "q_p_effective_relative_difference": abs(c_q - u_q) / max(abs(c_q), abs(u_q), 1.0e-12),
        "topology_mean_winding_difference": abs(float(c_top["mean_winding"]) - float(u_top["mean_winding"])),
        "topology_unit_fraction_difference": abs(float(c_top["unit_fraction"]) - float(u_top["unit_fraction"])),
        "curve_samples": curve_rows,
    }


def main() -> None:
    args = parse_args()
    sample_radii = parse_float_list(args.sample_radii)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for state in args.states:
        constrained = run_variant(
            state,
            label="constrained",
            conserve_l2_norm=True,
            extra_steps=args.extra_steps,
            sample_radii=sample_radii,
            probe_radius=args.probe_radius,
            xi=args.xi,
            c=args.c,
            output_dir=args.output_dir,
        )
        unconstrained = run_variant(
            state,
            label="unconstrained",
            conserve_l2_norm=False,
            extra_steps=args.extra_steps,
            sample_radii=sample_radii,
            probe_radius=args.probe_radius,
            xi=args.xi,
            c=args.c,
            output_dir=args.output_dir,
        )
        rows.append(
            {
                "source_state": str(state),
                "constrained": constrained,
                "unconstrained": unconstrained,
                "comparison": compare_variants(constrained, unconstrained),
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
        "extra_steps": int(args.extra_steps),
        "probe_radius": float(args.probe_radius),
        "sample_radii": sample_radii,
        "rows": rows,
        "summary": {
            "q_p_effective_relative_difference": metric_span(
                [float(row["comparison"]["q_p_effective_relative_difference"]) for row in rows]
            ),
            "deficit_volume_relative_difference": metric_span(
                [float(row["comparison"]["deficit_volume_relative_difference"]) for row in rows]
            ),
            "topology_mean_winding_difference": metric_span(
                [float(row["comparison"]["topology_mean_winding_difference"]) for row in rows]
            ),
            "topology_unit_fraction_difference": metric_span(
                [float(row["comparison"]["topology_unit_fraction_difference"]) for row in rows]
            ),
        },
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

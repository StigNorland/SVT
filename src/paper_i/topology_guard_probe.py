"""Compare topology-aware early relaxation variants from the same fresh initial trefoil state.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, c = 1
Primary observables: deficit volume, residuals, winding retention
Primary role: first probe of whether topology-aware acceptance rules change early branch selection.
Key limitation: uses the prototype trefoil relaxer and only tests one local winding/pressure family.
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
from trefoil_breather_static import TrefoilConfig, initial_state, relax, save_state


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("deficit_volume", "residual_norm", "topology_winding_retention"),
    diagnostics=("same_initial_condition", "topology_guard", "topology_pressure", "topology_flow", "topology_phase_flow", "topology_loop_flow", "topology_winding_flow", "early_branch_selection"),
    issue_refs=("#13", "#14"),
    limitations=(
        "Compares only a baseline constrained branch against one hard-guard, one soft-pressure, one topology-flow, one topology-phase-flow, one topology-loop-flow, and one topology-winding-flow branch.",
        "Uses the local winding-retention diagnostic rather than a full knot invariant.",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare early trefoil relaxation with and without a topology guard.")
    parser.add_argument("--n", type=int, default=48)
    parser.add_argument("--half-width", type=float, default=7.0)
    parser.add_argument("--major-radius", type=float, default=2.8)
    parser.add_argument("--minor-radius", type=float, default=0.85)
    parser.add_argument("--smoothing-radius", type=float, default=0.2)
    parser.add_argument("--log-pressure", type=float, default=0.5)
    parser.add_argument("--step-size", type=float, default=0.005)
    parser.add_argument("--max-steps", type=int, default=80)
    parser.add_argument("--tolerance", type=float, default=2.0e-3)
    parser.add_argument("--topology-mean-winding-min", type=float, default=0.5)
    parser.add_argument("--topology-unit-fraction-min", type=float, default=0.5)
    parser.add_argument("--topology-alignment-score-min", type=float, default=0.65)
    parser.add_argument("--topology-pressure-weight", type=float, default=500.0)
    parser.add_argument("--topology-flow-weight", type=float, default=0.0)
    parser.add_argument("--topology-phase-flow-weight", type=float, default=0.0)
    parser.add_argument("--topology-loop-flow-weight", type=float, default=0.0)
    parser.add_argument("--topology-winding-flow-weight", type=float, default=0.0)
    parser.add_argument("--topology-anchor-amplitude-min", type=float, default=0.15)
    parser.add_argument("--topology-anchor-amplitude-cutoff", type=float, default=0.95)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def controls(args: argparse.Namespace, mode: str) -> RelaxationControls:
    hard_guard = mode == "topology_hard_guard"
    pressure = mode == "topology_pressure"
    flow = mode == "topology_flow"
    phase_flow = mode == "topology_phase_flow"
    loop_flow = mode == "topology_loop_flow"
    winding_flow = mode == "topology_winding_flow"
    return RelaxationControls(
        step_size=args.step_size,
        max_steps=args.max_steps,
        tolerance=args.tolerance,
        conserve_l2_norm=True,
        topology_hard_guard=hard_guard,
        topology_mean_winding_min=args.topology_mean_winding_min if hard_guard else None,
        topology_unit_fraction_min=args.topology_unit_fraction_min if hard_guard else None,
        topology_alignment_score_min=args.topology_alignment_score_min if (hard_guard or pressure) else None,
        topology_pressure_weight=args.topology_pressure_weight if pressure else 0.0,
        topology_flow_weight=args.topology_flow_weight if flow else 0.0,
        topology_phase_flow_weight=args.topology_phase_flow_weight if phase_flow else 0.0,
        topology_loop_flow_weight=args.topology_loop_flow_weight if loop_flow else 0.0,
        topology_winding_flow_weight=args.topology_winding_flow_weight if winding_flow else 0.0,
        topology_anchor_amplitude_min=args.topology_anchor_amplitude_min,
        topology_anchor_amplitude_cutoff=args.topology_anchor_amplitude_cutoff,
    )


def main() -> None:
    args = parse_args()
    cfg = TrefoilConfig(
        n=args.n,
        half_width=args.half_width,
        major_radius=args.major_radius,
        minor_radius=args.minor_radius,
        smoothing_radius=args.smoothing_radius,
        log_pressure=args.log_pressure,
    )
    psi0 = initial_state(cfg)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for label in ("baseline", "topology_hard_guard", "topology_pressure", "topology_flow", "topology_phase_flow", "topology_loop_flow", "topology_winding_flow"):
        ctrl = controls(args, mode=label)
        psi, summary = relax(cfg, ctrl, initial_psi=psi0, continued_from_steps=0)
        state_path = args.output_dir / f"trefoil-{label}-n{cfg.n}-hw{cfg.half_width:g}-steps{args.max_steps}.npz"
        json_path = args.output_dir / f"trefoil-{label}-n{cfg.n}-hw{cfg.half_width:g}-steps{args.max_steps}.json"
        save_state(state_path, psi, cfg, ctrl, summary)
        row = {
            "label": label,
            "controls": asdict(ctrl),
            "summary": asdict(summary),
            "saved_state": str(state_path),
            "summary_path": str(json_path),
        }
        json_path.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
        rows.append(row)

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
        "config": asdict(cfg),
        "rows": rows,
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

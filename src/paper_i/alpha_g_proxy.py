"""Prototype alpha_G proxy extraction from static trefoil sweep outputs.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: shell deficit, far-field moment, effective radius, residual norm
Primary role: first conservative bridge from issue #13 static sweeps to issue #14 gravity extraction
Key limitation: this script does not predict alpha_G; it only extracts provisional
dimensionless suppression proxies from the best available static far-field diagnostics.
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

from shared_numerics import Nondimensionalisation, OutputStatus, ScriptMetadata


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("shell_mean_deficit", "far_field_moment", "effective_radius", "residual_norm"),
    diagnostics=("box_sensitivity", "resolution_sensitivity", "run_selection"),
    issue_refs=("#14",),
    limitations=(
        "Does not produce a first-principles alpha_G value.",
        "Uses shell-averaged static far-field observables as provisional suppression proxies only.",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract provisional alpha_G proxies from static trefoil sweep outputs.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Sweep JSON files from trefoil_breather_refinement.py")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def load_payload(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_run_record(source: Path, run: dict[str, object]) -> dict[str, object]:
    config = run["config"]
    summary = run["summary"]
    shell_density = float(run["shell_mean_density"])
    shell_deficit = float(run["shell_mean_deficit"])
    far_moment = float(run["far_field_moment"])
    effective_radius = float(summary["effective_radius"])
    residual = float(summary["residual_norm"])
    half_width = float(config["half_width"])
    n = int(config["n"])

    # Primary proxy: the shell deficit is currently the most stable simple outer-region
    # scalar across the long static sweeps, so this is the conservative bridge quantity.
    proxy_shell = shell_deficit

    # Secondary cross-check: convert the far-field moment into a dimensionless geometric
    # ratio using the box scale, while keeping it clearly separate from the primary proxy.
    proxy_moment = far_moment / max(half_width, 1.0e-12)

    # A very lightweight ranking score for choosing representative runs: prefer small
    # residual and large half-width, without pretending this is a convergence proof.
    selection_score = residual / max(half_width, 1.0e-12)

    return {
        "source": str(source),
        "n": n,
        "half_width": half_width,
        "steps_completed": int(summary["steps_completed"]),
        "residual_norm": residual,
        "effective_radius": effective_radius,
        "shell_mean_density": shell_density,
        "shell_mean_deficit": shell_deficit,
        "far_field_moment": far_moment,
        "alpha_g_proxy_shell_deficit": proxy_shell,
        "alpha_g_proxy_moment_scaled": proxy_moment,
        "selection_score": selection_score,
    }


def main() -> None:
    args = parse_args()
    records: list[dict[str, object]] = []
    for path in args.inputs:
        payload = load_payload(path)
        runs = payload.get("runs", [])
        for run in runs:
            records.append(build_run_record(path, run))

    records.sort(key=lambda item: (item["n"], item["steps_completed"], item["half_width"]))
    best_shell = min(records, key=lambda item: item["alpha_g_proxy_shell_deficit"])
    best_moment = min(records, key=lambda item: item["alpha_g_proxy_moment_scaled"])
    representative = min(records, key=lambda item: item["selection_score"])

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
        "records": records,
        "summary": {
            "primary_proxy_definition": "alpha_g_proxy_shell_deficit = 1 - shell_mean_density",
            "secondary_proxy_definition": "alpha_g_proxy_moment_scaled = far_field_moment / half_width",
            "best_shell_proxy_run": best_shell,
            "best_moment_proxy_run": best_moment,
            "representative_run": representative,
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

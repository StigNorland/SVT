"""Prototype geometric constraint extractor for the proton monopole calibration.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: deficit volume, equivalent deficit radius, shell deficit
Primary role: expose geometry-level quantities that may later constrain the Q_p calibration
Key limitation: this script does not solve for C_Q; it only records candidate geometric factors.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from trefoil_observables import deficit_volume, equivalent_deficit_radius


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract candidate geometric constraints from a saved trefoil state.")
    parser.add_argument("state", type=Path, help="Path to a .npz state saved by trefoil_breather_static.py")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = np.load(args.state, allow_pickle=False)
    psi = data["psi_real"] + 1j * data["psi_imag"]
    x = data["x"]
    y = data["y"]
    z = data["z"]
    config = json.loads(str(data["config"]))
    summary = json.loads(str(data["summary"]))

    spacing = float(x[1, 0, 0] - x[0, 0, 0]) if x.shape[0] > 1 else 0.0
    dv = deficit_volume(psi, spacing)
    req = equivalent_deficit_radius(psi, spacing)
    shell_deficit = float(summary["far_field_shell_deficit"])
    effective_r = float(summary["effective_radius"])

    payload = {
        "state": str(args.state),
        "config": config,
        "summary": summary,
        "geometry": {
            "deficit_volume": dv,
            "equivalent_deficit_radius": req,
            "shell_deficit": shell_deficit,
            "effective_radius": effective_r,
            "compactness_ratio": req / max(effective_r, 1.0e-12),
            "deficit_volume_over_radius_cubed": dv / max(effective_r**3, 1.0e-12),
            "shell_to_volume_ratio": shell_deficit / max(dv, 1.0e-12),
        },
        "interpretation": {
            "role": "candidate geometric constraints for the unresolved Q_p calibration",
            "warning": "These ratios are geometry diagnostics only; none should be read as a solved C_Q value.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

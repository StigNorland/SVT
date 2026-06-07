"""Radial far-field profile tool for saved static trefoil states.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1
Primary observables: shell-averaged density and density deficit as functions of radius
Primary role: inspect outer-region structure of saved trefoil states for issue #13 and the later alpha_G path
Key limitation: this is a diagnostic reader for saved prototype states, not a gravity extractor.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute radial far-field profiles from a saved trefoil state.")
    parser.add_argument("state", type=Path, help="Path to a .npz file produced by trefoil_breather_static.py --save-state")
    parser.add_argument("--bins", type=int, default=24)
    parser.add_argument("--r-min", type=float)
    parser.add_argument("--r-max", type=float)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def radial_profile(
    psi: np.ndarray,
    radius: np.ndarray,
    bins: int,
    r_min: float | None,
    r_max: float | None,
) -> list[dict[str, float]]:
    rho = np.abs(psi) ** 2
    deficit = np.clip(1.0 - rho, 0.0, None)

    low = float(np.min(radius)) if r_min is None else r_min
    high = float(np.max(radius)) if r_max is None else r_max
    edges = np.linspace(low, high, bins + 1)

    rows: list[dict[str, float]] = []
    for i in range(bins):
        lo = float(edges[i])
        hi = float(edges[i + 1])
        mask = (radius >= lo) & (radius < hi if i < bins - 1 else radius <= hi)
        if not np.any(mask):
            rows.append(
                {
                    "r_inner": lo,
                    "r_outer": hi,
                    "r_mid": 0.5 * (lo + hi),
                    "mean_density": 1.0,
                    "mean_deficit": 0.0,
                    "count": 0,
                }
            )
            continue
        rows.append(
            {
                "r_inner": lo,
                "r_outer": hi,
                "r_mid": 0.5 * (lo + hi),
                "mean_density": float(np.mean(rho[mask])),
                "mean_deficit": float(np.mean(deficit[mask])),
                "count": int(np.count_nonzero(mask)),
            }
        )
    return rows


def main() -> None:
    args = parse_args()
    data = np.load(args.state, allow_pickle=False)
    psi = data["psi_real"] + 1j * data["psi_imag"]
    x = data["x"]
    y = data["y"]
    z = data["z"]
    radius = np.sqrt(x * x + y * y + z * z)

    payload = {
        "state": str(args.state),
        "config": json.loads(str(data["config"])),
        "summary": json.loads(str(data["summary"])),
        "bins": args.bins,
        "profile": radial_profile(psi, radius, args.bins, args.r_min, args.r_max),
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

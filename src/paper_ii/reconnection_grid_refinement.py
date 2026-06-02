"""Issue #15: grid-refinement sweep for the reconnection supplement at canonical c=1.

Status: candidate
Problem type: dynamic
Nondimensionalisation: xi = 1, rho0 = 1, c = 1 (log_pressure = 0.5)
Primary observables: saddle_excess, cap_radius, cap_volume, cos_phi,
                     energy_drift_pct, norm_drift_pct
Primary role: Issue #15 closure item 1 -- extend the existing refinement sweep
              (which stopped at n=48 with log_pressure=8) to n=64 and n=96 at
              the canonical static-branch c=1 convention (log_pressure=0.5).
              Records the new diagnostics (cap_volume, energy_drift, norm_drift)
              added in this session.

Usage:
    python reconnection_grid_refinement.py [--output OUTPUT.json]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from dataclasses import asdict
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, ScriptMetadata
from paper_ii.reconnection_supplement import Config, AnalyseResult, analyse, evolve_path

warnings.filterwarnings("ignore")

SCRIPT_METADATA = ScriptMetadata(
    problem_type="dynamic",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1 (log_pressure = 0.5)",
    observables=(
        "saddle_excess",
        "cap_radius",
        "cap_volume",
        "cos_phi",
        "energy_drift_pct",
        "norm_drift_pct",
    ),
    diagnostics=("grid_refinement_sweep", "c_eff_canonical"),
    issue_refs=("#15",),
    limitations=(
        "Sweeps n at fixed length=24 and dt=0.001; other axes not varied here.",
        "Radiated-mode spectrum not yet implemented (issue #15 task 4).",
        "Initial-condition sensitivity not tested (gated on cross-grid stability).",
    ),
)

# Fixed parameters for all runs
LENGTH = 24.0
DT = 0.001
STEPS = 200
SNAPSHOTS = 17
LOG_PRESSURE = 0.5   # canonical c=1
LAMBDA_PERP_VALUES = (0.0, 10.0)

# Grid sizes: extend previous sweep (n=16,24,32,48) to n=64 and n=96
GRID_SIZES = (16, 24, 32, 48, 64, 96)

TOPOLOGIES = (("opposite", 1.0, -1.0), ("same", 1.0, 1.0))


def run_one(n: int, lam: float, topology: str, lower: float, upper: float) -> dict:
    cfg = Config(
        n=n, length=LENGTH, dt=DT, steps=STEPS, snapshots=SNAPSHOTS,
        log_pressure=LOG_PRESSURE, lambda_perp=lam,
    )
    t0 = time.perf_counter()
    try:
        path = evolve_path(cfg, lower, upper)
        res: AnalyseResult = analyse(path, cfg)
        elapsed = time.perf_counter() - t0
        return {
            "n": n, "length": LENGTH, "dt": DT, "log_pressure": LOG_PRESSURE,
            "lambda_perp": lam, "topology": topology,
            "saddle_index": res.saddle_index,
            "saddle_excess": res.saddle_excess,
            "cap_radius": res.cap_radius,
            "cap_volume": res.cap_volume,
            "cos_phi": res.cos_phi,
            "energy_drift_pct": res.energy_drift_pct,
            "norm_drift_pct": res.norm_drift_pct,
            "elapsed_s": elapsed,
            "error": "",
        }
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        nan = float("nan")
        return {
            "n": n, "length": LENGTH, "dt": DT, "log_pressure": LOG_PRESSURE,
            "lambda_perp": lam, "topology": topology,
            "saddle_index": -1,
            "saddle_excess": nan, "cap_radius": nan, "cap_volume": nan,
            "cos_phi": nan, "energy_drift_pct": nan, "norm_drift_pct": nan,
            "elapsed_s": elapsed, "error": f"{type(exc).__name__}: {exc}",
        }


def spread_pct(vals: list[float]) -> float:
    finite = [v for v in vals if not (v != v)]
    if len(finite) < 2:
        return float("nan")
    lo, hi = min(finite), max(finite)
    mid = np.mean(finite)
    return (hi - lo) / max(abs(mid), 1e-300) * 100.0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Issue #15 grid refinement sweep (canonical c=1).")
    p.add_argument("--output", type=Path, default=None)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    rows: list[dict] = []

    print(f"Reconnection grid refinement sweep  log_pressure={LOG_PRESSURE} (c_eff=1)  length={LENGTH}")
    print(f"Grid sizes: {GRID_SIZES}")
    print()

    for lam in LAMBDA_PERP_VALUES:
        print(f"--- lambda_perp = {lam} ---")
        for topo, lower, upper in TOPOLOGIES:
            print(f"  {topo}:")
            for n in GRID_SIZES:
                row = run_one(n, lam, topo, lower, upper)
                rows.append(row)
                err = row["error"]
                if err:
                    print(f"    n={n:3d}  ERROR: {err}")
                else:
                    print(
                        f"    n={n:3d}  saddle={row['saddle_index']:2d}  "
                        f"excess={row['saddle_excess']:.4g}  "
                        f"cap_r={row['cap_radius']:.4g}  cap_vol={row['cap_volume']:.4g}  "
                        f"cos_phi={row['cos_phi']:.4f}  "
                        f"dE={row['energy_drift_pct']:.3g}%  "
                        f"dN={row['norm_drift_pct']:.3g}%  "
                        f"({row['elapsed_s']:.1f}s)"
                    )

    # Convergence summary at lambda_perp=10, opposite topology
    print()
    print("=== Convergence summary: lambda_perp=10, opposite topology ===")
    ref_rows = [r for r in rows if abs(r["lambda_perp"] - 10.0) < 1e-6 and r["topology"] == "opposite" and not r["error"]]
    for key in ("saddle_excess", "cap_radius", "cos_phi"):
        vals = [r[key] for r in ref_rows]
        ns = [r["n"] for r in ref_rows]
        sp = spread_pct(vals)
        print(f"  {key:15s}  n={ns}  values={[round(v,4) for v in vals]}  spread={sp:.1f}%  "
              f"gate(<5%): {'PASS' if sp < 5.0 else 'FAIL'}")

    output_data = {
        "config": {
            "length": LENGTH, "dt": DT, "steps": STEPS,
            "log_pressure": LOG_PRESSURE, "grid_sizes": list(GRID_SIZES),
        },
        "rows": rows,
        "metadata": {k: str(v) for k, v in asdict(SCRIPT_METADATA).items()},
    }

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as fh:
            json.dump(output_data, fh, indent=2, default=str)
        print(f"\nWrote {len(rows)} rows to {args.output}")
    else:
        print("\n(use --output to save JSON)")


if __name__ == "__main__":
    main()

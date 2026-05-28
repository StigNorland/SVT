"""Issue #13 Run 2: N_Y * F cutoff-invariance sweep across topology-preserving states.

Status: candidate
Problem type: static (post-processing of saved 3D states)
Nondimensionalisation: xi = 1, rho0 = 1, c = 1
Primary observables: n_y_straight(R), f_factor_straight_int(R), n_y_times_f_straight(R)
Primary role: Issue #13 closure Run 2 -- check whether the product N_Y * F is
              cutoff-invariant or stationary at some geometric scale across the
              available topology-preserving NPZ states (n = 24, 48, 72 at
              half-width 6 xi).  Pure post-processing; no fresh 3D relaxation.

Usage: python static_closure_cutoff_invariance_sweep.py --output OUT.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, ScriptMetadata


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=(
        "n_y_straight",
        "f_factor_straight_int",
        "n_y_times_f_straight",
    ),
    diagnostics=("min_density", "topology_preservation_proxy"),
    issue_refs=("#13",),
    limitations=(
        "Post-processing only; uses existing topology-preserving NPZ states (n=24, 48, 72).",
        "Cutoff is the straight-vortex calibration R; not derived geometrically here.",
        "Does not include a no-penalty control (the no-penalty states have zero vortex links).",
    ),
)


DATA_ROOT = Path("papers/SSV-I/data").resolve() if Path("papers/SSV-I/data").exists() else (
    Path(__file__).resolve().parents[2] / "papers" / "SSV-I" / "data"
)


PYTHON = sys.executable

EXTRACTOR = Path(__file__).resolve().parent / "trefoil_breather_observables.py"


@dataclass(frozen=True)
class StateEntry:
    label: str
    n: int
    half_width: float
    mu_penalty: float
    rho_target: float
    state_path: Path


STATES: tuple[StateEntry, ...] = (
    StateEntry("n24_mu1000",  24, 6.0, 1000.0, None,
               DATA_ROOT / "trefoil-lperp-krylov-penalty-mu1000-n24-hw6-800steps-2026-05-18.npz"),
    StateEntry("n24_mu400_rho001", 24, 6.0, 400.0, 0.01,
               DATA_ROOT / "penalty-mu400-rho0p01-n24-hw6-1600steps-2026-05-18.npz"),
    StateEntry("n48_best",    48, 6.0, None, None,
               DATA_ROOT / "penalty-best-n48-hw6-800steps-2026-05-19.npz"),
    StateEntry("n48_mu1000",  48, 6.0, 1000.0, None,
               DATA_ROOT / "penalty-n48-mu1000-2026-05-19.npz"),
    StateEntry("n48_mu2500_rho005", 48, 6.0, 2500.0, 0.05,
               DATA_ROOT / "penalty-n48-mu2500-rho0p05-2026-05-19.npz"),
    StateEntry("n72_mu2000_rho005", 72, 6.0, 2000.0, 0.05,
               DATA_ROOT / "penalty-n72-mu2000-rho0p05-2026-05-19.npz"),
)


# Cutoff radii to sweep (in units of xi). Spans the range used in the
# f-factor-grid-converged-checkpoint.md table plus the canonical R=1.18.
R_VALUES = (0.5, 0.8, 1.0, 1.18, 1.5, 2.0, 3.0)


def run_extractor(state: Path, r_max: float) -> dict:
    if not state.exists():
        return {"_error": f"state not found: {state}"}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        result = subprocess.run(
            [
                PYTHON,
                str(EXTRACTOR),
                str(state),
                "--straight-vortex-r-max",
                f"{r_max}",
                "--output",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if result.returncode != 0:
            return {"_error": f"extractor failed (code {result.returncode}): {result.stderr[:300]}"}
        with tmp_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data.get("summary", {})
    except subprocess.TimeoutExpired:
        return {"_error": "extractor timed out (>600s)"}
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Issue #13 Run 2: N_Y * F cutoff-invariance sweep.")
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    t_start = time.perf_counter()
    for state in STATES:
        if not state.state_path.exists():
            print(f"  ! missing state: {state.state_path}  -- skipping label {state.label}")
            continue
        for r in R_VALUES:
            t0 = time.perf_counter()
            summary = run_extractor(state.state_path, r)
            elapsed = time.perf_counter() - t0
            err = summary.get("_error")
            ny_s = summary.get("n_y_straight", float("nan"))
            f_s = summary.get("f_factor_straight_int", float("nan"))
            ny_f = summary.get("n_y_times_f_straight", float("nan"))
            min_rho = summary.get("min_density", float("nan"))
            print(
                f"  {state.label:25s}  R={r:4.2f}  "
                f"N_Y={ny_s:8.3f}  F={f_s:7.3f}  N_Y*F={ny_f:9.3f}  "
                f"min_rho={min_rho:.3e}  ({elapsed:5.1f}s)" + (f"  ERROR: {err}" if err else "")
            )
            rows.append({
                "label": state.label,
                "n": state.n,
                "half_width": state.half_width,
                "mu_penalty": state.mu_penalty,
                "rho_target": state.rho_target,
                "R_cutoff": r,
                "n_y_straight": ny_s,
                "f_factor_straight_int": f_s,
                "n_y_times_f_straight": ny_f,
                "min_density": min_rho,
                "elapsed_s": elapsed,
                "error": err or "",
            })
    total = time.perf_counter() - t_start
    print(f"\nTotal sweep time: {total:.1f}s")

    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()

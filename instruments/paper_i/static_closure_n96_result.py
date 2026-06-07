"""Issue #13 Run 1: process n=96 cross-grid result and compare with n=72.

Status: candidate
Problem type: static (post-processing of n=96 and n=72 NPZ states)
Primary observables: N_Y, F, N_Y*F at R = 1.18 xi and at R_sc = 0.923 xi
Primary role: Issue #13 Run 1 -- check if the cross-grid spread drops to <5%
              when n is refined from 72 to 96 at fixed penalty config
              (mu=2000, rho=0.05).

Usage:
    python static_closure_n96_result.py [--output OUTPUT.json]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, ScriptMetadata

SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("n_y_straight", "f_factor_straight_int", "n_y_times_f_straight"),
    diagnostics=("cross_grid_spread_pct", "min_density"),
    issue_refs=("#13",),
    limitations=(
        "Comparison is at fixed (mu=2000, rho=0.05) only; other penalty configs not tested.",
        "R = 1.18 xi is empirical; R_sc = 0.923 xi is first-principles.",
    ),
)

DATA_ROOT = (
    Path("papers/SSV-I/data").resolve()
    if Path("papers/SSV-I/data").exists()
    else Path(__file__).resolve().parents[2] / "papers" / "SSV-I" / "data"
)
PYTHON = sys.executable
EXTRACTOR = Path(__file__).resolve().parent / "trefoil_breather_observables.py"

R_VALUES = (1.18, 0.92314)  # empirical canonical + first-principles R_sc


def run_extractor(state: Path, r_max: float) -> dict:
    if not state.exists():
        return {"_error": f"not found: {state}"}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        result = subprocess.run(
            [PYTHON, str(EXTRACTOR), str(state),
             "--straight-vortex-r-max", f"{r_max:.6f}",
             "--output", str(tmp_path)],
            capture_output=True, text=True, timeout=600,
        )
        if result.returncode != 0:
            return {"_error": f"extractor failed: {result.stderr[:200]}"}
        with tmp_path.open() as fh:
            data = json.load(fh)
        return data.get("summary", {})
    except subprocess.TimeoutExpired:
        return {"_error": "timeout"}
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def find_n96_state() -> Path | None:
    candidates = sorted(DATA_ROOT.glob("penalty-n96-mu2000-rho0p05-*.npz"))
    if not candidates:
        candidates = sorted(DATA_ROOT.glob("penalty-n96-*.npz"))
    return candidates[-1] if candidates else None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Issue #13 Run 1: n=96 cross-grid result.")
    p.add_argument("--output", type=Path, default=None)
    return p.parse_args()


def main() -> None:
    args = parse_args()

    n72_state = DATA_ROOT / "penalty-n72-mu2000-rho0p05-2026-05-19.npz"
    n96_state = find_n96_state()

    if n96_state is None:
        print("ERROR: n=96 state not found.  Run is still in progress.")
        sys.exit(1)

    print(f"n=72 state: {n72_state.name}")
    print(f"n=96 state: {n96_state.name}")
    print()

    rows: list[dict] = []
    for label, state, n in [("n72_mu2000_rho005", n72_state, 72), ("n96_mu2000_rho005", n96_state, 96)]:
        for r in R_VALUES:
            t0 = time.perf_counter()
            summary = run_extractor(state, r)
            elapsed = time.perf_counter() - t0
            err = summary.get("_error")
            ny = summary.get("n_y_straight", float("nan"))
            f  = summary.get("f_factor_straight_int", float("nan"))
            nyf = summary.get("n_y_times_f_straight", float("nan"))
            min_rho = summary.get("min_density", float("nan"))
            print(
                f"  {label}  n={n}  R={r:.4f}  "
                f"N_Y={ny:.3f}  F={f:.3f}  N_Y*F={nyf:.3f}  "
                f"min_rho={min_rho:.2e}  ({elapsed:.1f}s)"
                + (f"  ERROR: {err}" if err else "")
            )
            rows.append({
                "label": label, "n": n, "R_cutoff": r,
                "n_y_straight": ny, "f_factor_straight_int": f,
                "n_y_times_f_straight": nyf, "min_density": min_rho,
                "elapsed_s": elapsed, "error": err or "",
            })

    # Decision rule
    print()
    print("=== Decision rule ===")
    for r in R_VALUES:
        n72_row = next((r2 for r2 in rows if r2["n"] == 72 and abs(r2["R_cutoff"] - r) < 1e-5), None)
        n96_row = next((r2 for r2 in rows if r2["n"] == 96 and abs(r2["R_cutoff"] - r) < 1e-5), None)
        if n72_row is None or n96_row is None:
            continue
        for key in ("n_y_straight", "f_factor_straight_int", "n_y_times_f_straight"):
            v72 = n72_row[key]
            v96 = n96_row[key]
            if v72 == v72 and v96 == v96 and v72 != 0:
                spread = abs(v96 - v72) / abs(v72) * 100
                gate = "PASS" if spread < 5.0 else "FAIL"
                print(f"  R={r:.4f}  {key:30s}  n=72={v72:.3f}  n=96={v96:.3f}  spread={spread:.1f}%  {gate}")

    output_data = {"rows": rows, "metadata": {k: str(v) for k, v in vars(SCRIPT_METADATA).items()}}
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w") as fh:
            json.dump(output_data, fh, indent=2)
        print(f"\nWrote to {args.output}")


if __name__ == "__main__":
    main()

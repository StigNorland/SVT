"""Issue #13 Run 3: N_Y * F at self-consistent vortex-profile cutoff R_sc.

Status: candidate
Problem type: static (post-processing of saved 3D states)
Nondimensionalisation: xi = 1, rho0 = 1, c = 1
Primary observables: R_sc, n_y_straight(R_sc), f_factor_straight_int(R_sc),
                     n_y_times_f_straight(R_sc)
Primary role: Issue #13 closure Run 3 -- replace the empirical R = 1.18 xi
              cutoff with a geometrically derived cutoff R_sc defined as the
              radius at which the LogSE straight-vortex profile crosses
              rho = |psi|^2 = 0.5.  R_sc is the same for all states (it is a
              property of the LogSE vortex ODE at the fixed log_pressure used
              in the relaxer), so this run asks: does N_Y * F(R_sc) converge
              as n increases at fixed penalty config?

Usage:
    python static_closure_self_consistent_r.py [--output OUTPUT.json]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, ScriptMetadata
from paper_i.vortex_profile import VortexProfile


SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=(
        "R_sc",
        "n_y_straight",
        "f_factor_straight_int",
        "n_y_times_f_straight",
    ),
    diagnostics=("min_density", "n", "half_width"),
    issue_refs=("#13",),
    limitations=(
        "R_sc is derived from the straight-vortex ODE profile (log_pressure=0.5), "
        "not from the 3D relaxed geometry.  It is therefore the same for all states, "
        "and this run tests convergence of N_Y*F at a fixed geometric scale, not a "
        "state-specific scale.",
        "Does not include n=96 state if not yet computed.",
        "Post-processing only; uses existing topology-preserving NPZ states.",
    ),
)


DATA_ROOT = (
    Path("papers/SSV-I/data").resolve()
    if Path("papers/SSV-I/data").exists()
    else Path(__file__).resolve().parents[2] / "papers" / "SSV-I" / "data"
)

PYTHON = sys.executable
EXTRACTOR = Path(__file__).resolve().parent / "trefoil_breather_observables.py"


@dataclass(frozen=True)
class StateEntry:
    label: str
    n: int
    half_width: float
    mu_penalty: float | None
    rho_target: float | None
    state_path: Path


STATES: tuple[StateEntry, ...] = (
    StateEntry(
        "n24_mu400_rho001", 24, 6.0, 400.0, 0.01,
        DATA_ROOT / "penalty-mu400-rho0p01-n24-hw6-1600steps-2026-05-18.npz",
    ),
    StateEntry(
        "n48_best", 48, 6.0, None, None,
        DATA_ROOT / "penalty-best-n48-hw6-800steps-2026-05-19.npz",
    ),
    StateEntry(
        "n48_mu1000", 48, 6.0, 1000.0, None,
        DATA_ROOT / "penalty-n48-mu1000-2026-05-19.npz",
    ),
    StateEntry(
        "n48_mu2500_rho005", 48, 6.0, 2500.0, 0.05,
        DATA_ROOT / "penalty-n48-mu2500-rho0p05-2026-05-19.npz",
    ),
    StateEntry(
        "n72_mu2000_rho005", 72, 6.0, 2000.0, 0.05,
        DATA_ROOT / "penalty-n72-mu2000-rho0p05-2026-05-19.npz",
    ),
)


def _find_n96_state() -> StateEntry | None:
    """Find an n=96 state if one has been produced."""
    candidates = sorted(DATA_ROOT.glob("penalty-n96-*-mu2000-rho0p05-*.npz"))
    if not candidates:
        candidates = sorted(DATA_ROOT.glob("penalty-n96-*.npz"))
    if candidates:
        p = candidates[-1]  # most recent
        return StateEntry("n96_mu2000_rho005", 96, 6.0, 2000.0, 0.05, p)
    return None


def compute_r_sc(log_pressure: float = 0.5) -> float:
    """Radius (in xi) at which the LogSE straight-vortex profile crosses |psi|^2 = 0.5.

    This is the first-principles geometric cutoff: beyond r_sc, a neighbouring vortex
    contributes less than half the local condensate density, so the straight-vortex
    calibration integral should not extend further without double-counting.
    """
    prof = VortexProfile.solve(x_min=1e-4, x_max=20.0, n=4000)
    rs = np.linspace(0.01, 5.0, 10000)
    f2 = np.array([prof.value(r) ** 2 for r in rs])
    idx = int(np.searchsorted(f2, 0.5))
    if idx >= len(rs):
        raise RuntimeError("f^2=0.5 crossing not found in [0.01, 5.0] xi")
    # Linear interpolation between idx-1 and idx for precision
    if idx > 0:
        r0, r1 = rs[idx - 1], rs[idx]
        f0, f1 = f2[idx - 1], f2[idx]
        r_sc = r0 + (0.5 - f0) / (f1 - f0) * (r1 - r0)
    else:
        r_sc = float(rs[idx])
    return float(r_sc)


def run_extractor(state_path: Path, r_max: float) -> dict:
    if not state_path.exists():
        return {"_error": f"state not found: {state_path}"}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        result = subprocess.run(
            [
                PYTHON,
                str(EXTRACTOR),
                str(state_path),
                "--straight-vortex-r-max",
                f"{r_max:.6f}",
                "--output",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if result.returncode != 0:
            return {"_error": f"extractor failed ({result.returncode}): {result.stderr[:300]}"}
        with tmp_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("summary", {})
    except subprocess.TimeoutExpired:
        return {"_error": "extractor timed out (>600s)"}
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Issue #13 Run 3: N_Y*F at self-consistent R_sc.")
    p.add_argument("--output", type=Path, default=None)
    return p.parse_args()


def main() -> None:
    args = parse_args()

    r_sc = compute_r_sc(log_pressure=0.5)
    print(f"R_sc (f^2=0.5 crossing, log_pressure=0.5): {r_sc:.5f} xi")
    print()

    states = list(STATES)
    n96 = _find_n96_state()
    if n96 is not None:
        print(f"Found n=96 state: {n96.state_path.name}")
        states.append(n96)
    else:
        print("No n=96 state found; run will use n=24/48/72 only.")
    print()

    results: list[dict] = []
    for entry in states:
        if not entry.state_path.exists():
            print(f"  SKIP (missing): {entry.label}")
            continue
        t0 = time.perf_counter()
        summary = run_extractor(entry.state_path, r_sc)
        elapsed = time.perf_counter() - t0
        err = summary.get("_error")
        ny = summary.get("n_y_straight", float("nan"))
        f = summary.get("f_factor_straight_int", float("nan"))
        nyf = summary.get("n_y_times_f_straight", float("nan"))
        min_rho = summary.get("min_density", float("nan"))
        print(
            f"  {entry.label:25s}  n={entry.n:3d}  "
            f"N_Y={ny:8.3f}  F={f:7.3f}  N_Y*F={nyf:9.3f}  "
            f"min_rho={min_rho:.2e}  ({elapsed:.1f}s)"
            + (f"  ERROR: {err}" if err else "")
        )
        results.append(
            {
                "label": entry.label,
                "n": entry.n,
                "half_width": entry.half_width,
                "mu_penalty": entry.mu_penalty,
                "rho_target": entry.rho_target,
                "R_sc": r_sc,
                "n_y_straight": ny,
                "f_factor_straight_int": f,
                "n_y_times_f_straight": nyf,
                "min_density": min_rho,
                "elapsed_s": elapsed,
                "error": err or "",
            }
        )

    # Cross-grid spread at R_sc across all valid n=48+ states
    valid = [r for r in results if not r["error"] and r["n"] >= 48 and not np.isnan(r["n_y_times_f_straight"])]
    if len(valid) >= 2:
        nyf_vals = [r["n_y_times_f_straight"] for r in valid]
        spread = (max(nyf_vals) - min(nyf_vals)) / np.mean(nyf_vals) * 100
        print(f"\n  N_Y*F spread across n>=48 states at R_sc: {spread:.1f}%  "
              f"(range {min(nyf_vals):.1f}..{max(nyf_vals):.1f})")
        print(f"  Closure gate (<5%): {'PASS' if spread < 5 else 'FAIL'}")

    output = {
        "R_sc": r_sc,
        "results": results,
        "metadata": {k: str(v) for k, v in asdict(SCRIPT_METADATA).items()},
    }
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as fh:
            json.dump(output, fh, indent=2)
        print(f"\nWrote results to {args.output}")
    else:
        print("\n(use --output to save JSON)")


if __name__ == "__main__":
    main()

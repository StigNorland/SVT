"""Refinement and sensitivity sweeps for the restricted 2-mode BdG diagnostic.

Status: validation
Problem type: static
Primary role: validation asset for issue #16 — measures which restricted-BdG
observables are stable under grid refinement and box-size changes, and which
drift materially.

For each sweep axis (grid n, box half_width, background profile resolution,
background profile extent x_max) the script reports omega_minus, omega_plus,
and the underlying A/B block entries. A quantity is reported as "stable" if
the maximum-vs-minimum relative spread across the sweep is below 1%, otherwise
"drifts materially".

The reference point is n=61, half_width=6, profile_n=2400, profile_x_max=20.
Each sweep varies one axis with the others held at this reference.
"""

from __future__ import annotations

import argparse
import csv
import time
from dataclasses import dataclass
from pathlib import Path

from restricted_bdg_matrix import compute_restricted_bdg
from toroidal_projection_integrals import ProjectionConfig


REFERENCE = dict(
    n=61,
    half_width=6.0,
    profile_n=2400,
    profile_x_max=20.0,
)


GRID_SWEEP = (21, 31, 41, 51, 61, 81)
BOX_SWEEP = (3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
PROFILE_N_SWEEP = (600, 1200, 2400, 4800)
PROFILE_XMAX_SWEEP = (15.0, 20.0, 25.0, 30.0)


@dataclass(frozen=True)
class SweepRow:
    sweep: str
    value: float
    elapsed_s: float
    omega_minus: float
    omega_plus: float
    omega_minus_sq: float
    omega_plus_sq: float
    a_rr: float
    a_rc: float
    a_cc: float
    b_rr: float
    b_rc: float
    b_cc: float


def cfg_with(**overrides: object) -> ProjectionConfig:
    params = {**REFERENCE, **overrides}
    return ProjectionConfig(
        n=int(params["n"]),
        half_width=float(params["half_width"]),
        chi_parity="sin",
        orthogonalize_chi=True,
        profile="numerical",
        profile_n=int(params["profile_n"]),
        profile_x_max=float(params["profile_x_max"]),
        workers=1,
        curvature_coeffs=(),
        phase_coeffs=(),
        inner_outer_stiffness=0.0,
    )


def run_point(sweep: str, value: float, cfg: ProjectionConfig) -> SweepRow:
    t0 = time.perf_counter()
    nan = float("nan")
    try:
        result = compute_restricted_bdg(cfg)
        elapsed = time.perf_counter() - t0
        return SweepRow(
            sweep=sweep,
            value=value,
            elapsed_s=elapsed,
            omega_minus=result.omega_minus,
            omega_plus=result.omega_plus,
            omega_minus_sq=result.omega_minus_sq,
            omega_plus_sq=result.omega_plus_sq,
            a_rr=result.a_block.rr,
            a_rc=result.a_block.rc,
            a_cc=result.a_block.cc,
            b_rr=result.b_block.rr,
            b_rc=result.b_block.rc,
            b_cc=result.b_block.cc,
        )
    except Exception as exc:  # noqa: BLE001 – per-point isolation for sweeps
        elapsed = time.perf_counter() - t0
        print(f"  ! point {sweep}={value} failed after {elapsed:.1f}s: {type(exc).__name__}: {exc}")
        return SweepRow(
            sweep=sweep, value=value, elapsed_s=elapsed,
            omega_minus=nan, omega_plus=nan, omega_minus_sq=nan, omega_plus_sq=nan,
            a_rr=nan, a_rc=nan, a_cc=nan, b_rr=nan, b_rc=nan, b_cc=nan,
        )


def write_csv(rows: list[SweepRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "sweep", "value", "elapsed_s",
            "omega_minus", "omega_plus", "omega_minus_sq", "omega_plus_sq",
            "a_rr", "a_rc", "a_cc",
            "b_rr", "b_rc", "b_cc",
        ])
        for r in rows:
            writer.writerow([
                r.sweep, f"{r.value:.6g}", f"{r.elapsed_s:.3f}",
                f"{r.omega_minus:.12e}", f"{r.omega_plus:.12e}",
                f"{r.omega_minus_sq:.12e}", f"{r.omega_plus_sq:.12e}",
                f"{r.a_rr:.12e}", f"{r.a_rc:.12e}", f"{r.a_cc:.12e}",
                f"{r.b_rr:.12e}", f"{r.b_rc:.12e}", f"{r.b_cc:.12e}",
            ])


def relative_spread(values: list[float]) -> float:
    finite = [v for v in values if v == v and abs(v) > 0]
    if len(finite) < 2:
        return 0.0
    lo, hi = min(finite), max(finite)
    pivot = max(abs(lo), abs(hi))
    return (hi - lo) / pivot if pivot > 0 else 0.0


def summarise(rows: list[SweepRow]) -> str:
    columns = [
        ("omega_minus", lambda r: r.omega_minus),
        ("omega_plus", lambda r: r.omega_plus),
        ("a_rr", lambda r: r.a_rr),
        ("a_rc", lambda r: r.a_rc),
        ("a_cc", lambda r: r.a_cc),
        ("b_rr", lambda r: r.b_rr),
        ("b_rc", lambda r: r.b_rc),
        ("b_cc", lambda r: r.b_cc),
    ]
    by_sweep: dict[str, list[SweepRow]] = {}
    for r in rows:
        by_sweep.setdefault(r.sweep, []).append(r)

    lines = []
    for sweep, group in by_sweep.items():
        values = [r.value for r in group]
        lines.append(f"\n=== sweep: {sweep}  ({len(group)} points, range {min(values):g}..{max(values):g}) ===")
        lines.append(f"{'observable':<14s}  {'min':>14s}  {'max':>14s}  {'rel-spread':>11s}  {'verdict':<10s}")
        for name, getter in columns:
            vals = [getter(r) for r in group]
            spread = relative_spread(vals)
            verdict = "stable" if spread < 0.01 else "drifts"
            lo, hi = min(vals), max(vals)
            lines.append(f"{name:<14s}  {lo:14.6e}  {hi:14.6e}  {spread:10.3%}  {verdict:<10s}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refinement and sensitivity sweeps for restricted_bdg_matrix.")
    parser.add_argument("--sweeps", default="grid,box,profile_n,profile_xmax",
                        help="Comma-separated list of sweeps to run.")
    parser.add_argument("--output", type=Path,
                        default=Path("papers/SSV-I/data/validation-refinement-restricted-bdg-2026-05-27.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requested = {s.strip() for s in args.sweeps.split(",") if s.strip()}
    rows: list[SweepRow] = []

    print(f"Reference config: {REFERENCE}")
    print(f"Running sweeps: {sorted(requested)}")
    print()

    if "grid" in requested:
        print(f"--- grid sweep: n in {GRID_SWEEP} ---")
        for n in GRID_SWEEP:
            cfg = cfg_with(n=n)
            row = run_point("grid_n", float(n), cfg)
            rows.append(row)
            print(f"  n={n:3d}  elapsed={row.elapsed_s:6.1f}s  "
                  f"omega_minus={row.omega_minus:.6e}  omega_plus={row.omega_plus:.6e}")

    if "box" in requested:
        print(f"\n--- box sweep: half_width in {BOX_SWEEP} ---")
        for hw in BOX_SWEEP:
            cfg = cfg_with(half_width=hw)
            row = run_point("box_hw", hw, cfg)
            rows.append(row)
            print(f"  hw={hw:4.1f}  elapsed={row.elapsed_s:6.1f}s  "
                  f"omega_minus={row.omega_minus:.6e}  omega_plus={row.omega_plus:.6e}")

    if "profile_n" in requested:
        print(f"\n--- profile_n sweep: profile_n in {PROFILE_N_SWEEP} ---")
        for pn in PROFILE_N_SWEEP:
            cfg = cfg_with(profile_n=pn)
            row = run_point("profile_n", float(pn), cfg)
            rows.append(row)
            print(f"  profile_n={pn:5d}  elapsed={row.elapsed_s:6.1f}s  "
                  f"omega_minus={row.omega_minus:.6e}  omega_plus={row.omega_plus:.6e}")

    if "profile_xmax" in requested:
        print(f"\n--- profile_xmax sweep: profile_x_max in {PROFILE_XMAX_SWEEP} ---")
        for xm in PROFILE_XMAX_SWEEP:
            cfg = cfg_with(profile_x_max=xm)
            row = run_point("profile_xmax", xm, cfg)
            rows.append(row)
            print(f"  profile_xmax={xm:4.1f}  elapsed={row.elapsed_s:6.1f}s  "
                  f"omega_minus={row.omega_minus:.6e}  omega_plus={row.omega_plus:.6e}")

    write_csv(rows, args.output)
    print(f"\nWrote {len(rows)} rows to {args.output}")
    print(summarise(rows))


if __name__ == "__main__":
    main()

"""Refinement and sensitivity sweeps for the dynamic-branch reconnection supplement.

Status: validation
Problem type: dynamic
Primary role: issue #16 dynamic-side baseline -- sweep grid n, box length,
and timestep dt for src/paper_ii/reconnection_supplement.py at fixed
lambda_perp and topology, and record which of {saddle_excess, cap_radius,
cos_phi} are stable and which drift materially under each axis.

The reference configuration matches the existing example sweeps in
papers/SSV-II/data/: n=32, length=18, dt=0.001, steps=200, snapshots=17,
log_pressure=8.  Two topologies (opposite circulation, same circulation)
are computed for each point per the supplement's own convention.

A quantity is reported "stable" if its relative spread across the swept
axis is below 5%, otherwise "drifts materially".  The 5% threshold is
deliberately looser than the static-side 1% gate: reconnection
observables sit on a moving target (the time-dependent saddle), so a
single-percent reproducibility is not a useful gate at this resolution.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from dataclasses import dataclass
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, ScriptMetadata
from paper_ii.reconnection_supplement import Config, analyse, evolve_path


SCRIPT_METADATA = ScriptMetadata(
    problem_type="dynamic",
    status=OutputStatus.VALIDATION,
    nondimensionalisation="xi = 1, rho0 = 1, c_eff = sqrt(2*log_pressure) (non-canonical)",
    observables=(
        "saddle_index",
        "saddle_excess",
        "cap_radius",
        "cos_phi",
    ),
    diagnostics=(
        "grid_refinement_sweep",
        "box_size_sweep",
        "timestep_sweep",
    ),
    issue_refs=("#16",),
    limitations=(
        "Refinement sweep only at single lambda_perp value per axis.",
        "Sound-speed convention diverges from canonical c = 1 (inherited from reconnection_supplement.py).",
        "Cap radius depends on the volume-vs-radial-slice extraction method choice; both methods sweep at the volume default.",
    ),
)


# Reference configuration. Matches papers/SSV-II/data/example sweeps.
REFERENCE = dict(
    n=32,
    length=18.0,
    dt=0.001,
    steps=200,
    snapshots=17,
    log_pressure=8.0,
    lambda_perp=10.0,
)

GRID_SWEEP = (16, 24, 32, 48)
LENGTH_SWEEP = (12.0, 15.0, 18.0, 24.0)
DT_SWEEP = (0.0005, 0.001, 0.002)

# Two topologies the supplement scans.
TOPOLOGIES = (("opposite", 1.0, -1.0), ("same", 1.0, 1.0))


@dataclass(frozen=True)
class SweepRow:
    sweep: str
    value: float
    topology: str
    elapsed_s: float
    saddle_index: int
    saddle_excess: float
    cap_radius: float
    cap_volume: float
    cos_phi: float
    energy_drift_pct: float
    norm_drift_pct: float
    error: str = ""


def make_config(**overrides: object) -> Config:
    params = {**REFERENCE, **overrides}
    return Config(
        n=int(params["n"]),
        length=float(params["length"]),
        dt=float(params["dt"]),
        steps=int(params["steps"]),
        snapshots=int(params["snapshots"]),
        log_pressure=float(params["log_pressure"]),
        lambda_perp=float(params["lambda_perp"]),
    )


def run_point(sweep: str, value: float, label: str, lower: float, upper: float, **overrides: object) -> SweepRow:
    cfg = make_config(**overrides)
    t0 = time.perf_counter()
    try:
        path = evolve_path(cfg, lower, upper)
        res = analyse(path, cfg)
        elapsed = time.perf_counter() - t0
        return SweepRow(
            sweep=sweep,
            value=value,
            topology=label,
            elapsed_s=elapsed,
            saddle_index=res.saddle_index,
            saddle_excess=res.saddle_excess,
            cap_radius=res.cap_radius,
            cap_volume=res.cap_volume,
            cos_phi=res.cos_phi,
            energy_drift_pct=res.energy_drift_pct,
            norm_drift_pct=res.norm_drift_pct,
        )
    except Exception as exc:  # noqa: BLE001
        elapsed = time.perf_counter() - t0
        nan = float("nan")
        return SweepRow(
            sweep=sweep, value=value, topology=label, elapsed_s=elapsed,
            saddle_index=-1, saddle_excess=nan, cap_radius=nan, cap_volume=nan,
            cos_phi=nan, energy_drift_pct=nan, norm_drift_pct=nan,
            error=f"{type(exc).__name__}: {exc}",
        )


def write_csv(rows: list[SweepRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "sweep", "value", "topology", "elapsed_s",
            "saddle_index", "saddle_excess", "cap_radius", "cap_volume",
            "cos_phi", "energy_drift_pct", "norm_drift_pct", "error",
        ])
        for r in rows:
            writer.writerow([
                r.sweep, f"{r.value:.6g}", r.topology, f"{r.elapsed_s:.3f}",
                r.saddle_index, f"{r.saddle_excess:.9e}",
                f"{r.cap_radius:.9e}", f"{r.cap_volume:.9e}",
                f"{r.cos_phi:.9e}", f"{r.energy_drift_pct:.6g}",
                f"{r.norm_drift_pct:.6g}", r.error,
            ])


def relative_spread(values: list[float]) -> float:
    finite = [v for v in values if v == v and abs(v) > 0]
    if len(finite) < 2:
        return 0.0
    lo, hi = min(finite), max(finite)
    pivot = max(abs(lo), abs(hi))
    return (hi - lo) / pivot if pivot > 0 else 0.0


def summarise(rows: list[SweepRow]) -> str:
    cols = [
        ("saddle_excess", lambda r: r.saddle_excess),
        ("cap_radius", lambda r: r.cap_radius),
        ("cos_phi", lambda r: r.cos_phi),
    ]
    out = []
    seen: dict[tuple[str, str], list[SweepRow]] = {}
    for r in rows:
        seen.setdefault((r.sweep, r.topology), []).append(r)
    for (sweep, topo), group in seen.items():
        values = [r.value for r in group]
        out.append(f"\n=== sweep: {sweep} ({topo}) — {len(group)} points, range {min(values):g}..{max(values):g} ===")
        out.append(f"{'observable':<14s}  {'min':>12s}  {'max':>12s}  {'rel-spread':>11s}  {'verdict':<10s}")
        for name, getter in cols:
            vals = [getter(r) for r in group]
            spread = relative_spread(vals)
            verdict = "stable" if spread < 0.05 else "drifts"
            out.append(f"{name:<14s}  {min(vals):12.5e}  {max(vals):12.5e}  {spread:10.2%}  {verdict:<10s}")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Refinement and sensitivity sweeps for the dynamic-branch reconnection supplement.")
    p.add_argument("--sweeps", default="grid,length,dt")
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    requested = {s.strip() for s in args.sweeps.split(",") if s.strip()}
    rows: list[SweepRow] = []

    print(f"Reference config: {REFERENCE}")
    print(f"Running sweeps: {sorted(requested)}")
    print()

    if "grid" in requested:
        print(f"--- grid sweep: n in {GRID_SWEEP} (length={REFERENCE['length']}, dt={REFERENCE['dt']}) ---")
        for n in GRID_SWEEP:
            for label, lo, hi in TOPOLOGIES:
                row = run_point("grid_n", float(n), label, lo, hi, n=n)
                rows.append(row)
                err = f"  ERROR {row.error}" if row.error else ""
                print(f"  n={n:3d}  {label:9s}  {row.elapsed_s:6.1f}s  saddle={row.saddle_index:3d}  excess={row.saddle_excess:.4e}  cap={row.cap_radius:.4e}  cos_phi={row.cos_phi:.4e}{err}")

    if "length" in requested:
        print(f"\n--- length sweep: length in {LENGTH_SWEEP} (n={REFERENCE['n']}, dt={REFERENCE['dt']}) ---")
        for L in LENGTH_SWEEP:
            for label, lo, hi in TOPOLOGIES:
                row = run_point("length", L, label, lo, hi, length=L)
                rows.append(row)
                err = f"  ERROR {row.error}" if row.error else ""
                print(f"  L={L:5.1f}  {label:9s}  {row.elapsed_s:6.1f}s  saddle={row.saddle_index:3d}  excess={row.saddle_excess:.4e}  cap={row.cap_radius:.4e}  cos_phi={row.cos_phi:.4e}{err}")

    if "dt" in requested:
        print(f"\n--- dt sweep: dt in {DT_SWEEP} (n={REFERENCE['n']}, length={REFERENCE['length']}, steps adjusted to preserve total time) ---")
        ref_total_time = REFERENCE["steps"] * REFERENCE["dt"]
        for dt in DT_SWEEP:
            steps_adj = int(round(ref_total_time / dt))
            for label, lo, hi in TOPOLOGIES:
                row = run_point("dt", dt, label, lo, hi, dt=dt, steps=steps_adj)
                rows.append(row)
                err = f"  ERROR {row.error}" if row.error else ""
                print(f"  dt={dt:.5f} steps={steps_adj:4d}  {label:9s}  {row.elapsed_s:6.1f}s  saddle={row.saddle_index:3d}  excess={row.saddle_excess:.4e}  cap={row.cap_radius:.4e}  cos_phi={row.cos_phi:.4e}{err}")

    write_csv(rows, args.output)
    print(f"\nWrote {len(rows)} rows to {args.output}")
    print(summarise(rows))


if __name__ == "__main__":
    main()

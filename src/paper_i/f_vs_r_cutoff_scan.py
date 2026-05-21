"""Sweep the straight-vortex cutoff R and report F(R), N_Y(R), and implied proton mass.

Science question
---------------
Is F_straight(R) = e_interior / (l_curve * mu_0_str(R)) approximately constant
over the natural window R ∈ [0.8, 1.5] xi, or does it vary monotonically?
The paper uses F ≈ 4.47 at R = 1.18 xi (inter-strand half-spacing of a trefoil
with minor_radius = 0.85 xi).  This script quantifies the cutoff sensitivity so
the paper can report an honest systematic uncertainty.

Two acceptable outcomes:
  - F is stable in the window → "essentially cutoff-independent" becomes a real claim.
  - F drifts → the fractional drift goes into the proton-mass error bar honestly.

Usage
-----
python src/paper_i/f_vs_r_cutoff_scan.py  STATE [STATE ...]  [options]

Typical call:
  python src/paper_i/f_vs_r_cutoff_scan.py  \\
    papers/SSV-I/data/penalty-mu400-rho0p01-n24-hw6-1600steps-2026-05-18.npz \\
    papers/SSV-I/data/penalty-best-n48-hw6-800steps-2026-05-19.npz \\
    papers/SSV-I/data/penalty-n72-mu2000-rho0p05-2026-05-19.npz \\
    --anchor-thickness-xi 1.0 --output papers/SSV-I/data/f-vs-r-scan.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from paper_i.trefoil_breather_observables import (  # noqa: E402
    ExtractionConfig,
    extract,
    load_state,
    mu_0_straight_vortex,
)

# Paper constants (physical, used only for converting to MeV)
N_Y_PAPER = 3.007       # topological crossing-count factor
MU0_MEV = 70.025        # m_e / alpha in MeV

# Default R grid: dense around the physical cutoff at 1.18 xi, wider flanks
DEFAULT_R_GRID = [0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.18, 1.3, 1.5, 1.7, 2.0, 2.5, 3.0]


def scan_one_state(
    state_path: Path,
    r_grid: list[float],
    anchor_thickness_xi: float,
) -> list[dict]:
    """Run the R-sweep for a single state file.  Returns a list of row dicts."""
    state = load_state(state_path)
    cfg = state["cfg"]
    n = int(cfg["n"])
    hw = float(cfg["half_width"])
    log_p = float(cfg.get("log_pressure", 0.5))

    rows = []
    for r in r_grid:
        ec = ExtractionConfig(
            r_tube=1.5,
            r_cavity=1.5,
            cal_arc_half_width=0.5,
            anchor_thickness_xi=anchor_thickness_xi,
            straight_vortex_r_max=r,
        )
        s = extract(state, ec)
        mp_implied = N_Y_PAPER * s.f_factor_straight_int * MU0_MEV
        rows.append(
            {
                "state": state_path.name,
                "n": n,
                "hw": hw,
                "log_pressure": log_p,
                "R_xi": r,
                "mu0_str": s.mu_0_straight,
                "F_str": s.f_factor_straight_int,
                "N_Y_str": s.n_y_straight,
                "N_Y_str_times_F": s.n_y_times_f_straight,
                "mp_implied_MeV": mp_implied,
                "e_interior": s.e_interior,
                "l_curve": s.l_curve_geometric,
                "min_density": s.min_density,
            }
        )
    return rows


def local_slope(rows: list[dict], r_target: float) -> float:
    """Logarithmic slope d ln F / d ln R at the point nearest r_target,
    estimated from the two neighbouring points.  Returns nan if not available."""
    rs = [r["R_xi"] for r in rows]
    fs = [r["F_str"] for r in rows]
    idx = min(range(len(rs)), key=lambda i: abs(rs[i] - r_target))
    if idx == 0 or idx == len(rs) - 1:
        return float("nan")
    dr_lo = rs[idx] - rs[idx - 1]
    dr_hi = rs[idx + 1] - rs[idx]
    df_lo = fs[idx] - fs[idx - 1]
    df_hi = fs[idx + 1] - fs[idx]
    # central difference of ln F w.r.t. ln R
    dlnf = 0.5 * (df_lo / dr_lo + df_hi / dr_hi) * (rs[idx] / fs[idx])
    return float(dlnf)


def stability_in_window(rows: list[dict], r_lo: float, r_hi: float) -> dict:
    """Report F and m_p at r_lo, paper R=1.18, and r_hi."""
    def nearest(target):
        return min(rows, key=lambda r: abs(r["R_xi"] - target))

    row_lo = nearest(r_lo)
    row_ref = nearest(1.18)
    row_hi = nearest(r_hi)
    f_lo, f_ref, f_hi = row_lo["F_str"], row_ref["F_str"], row_hi["F_str"]
    if math.isnan(f_ref) or f_ref == 0:
        return {}
    return {
        "window_lo_xi": r_lo,
        "window_hi_xi": r_hi,
        "F_at_lo": f_lo,
        "F_at_ref_1p18": f_ref,
        "F_at_hi": f_hi,
        "delta_F_pct_lo_to_ref": 100.0 * (f_ref - f_lo) / f_ref,
        "delta_F_pct_ref_to_hi": 100.0 * (f_ref - f_hi) / f_ref,
        "mp_at_lo_MeV": row_lo["mp_implied_MeV"],
        "mp_at_ref_MeV": row_ref["mp_implied_MeV"],
        "mp_at_hi_MeV": row_hi["mp_implied_MeV"],
    }


def print_table(rows: list[dict]) -> None:
    hdr = f"{'state':>40s}  {'n':>4s}  {'R/xi':>6s}  {'mu0_str':>9s}  "
    hdr += f"{'F_str':>7s}  {'mp/MeV':>8s}  {'N_Y_str':>8s}"
    print(hdr)
    print("-" * len(hdr))
    prev_state = None
    for r in rows:
        if r["state"] != prev_state:
            if prev_state is not None:
                print()
            prev_state = r["state"]
        f = r["F_str"]
        mp = r["mp_implied_MeV"]
        ny = r["N_Y_str"]
        mu = r["mu0_str"]
        marker = " <-- paper R" if abs(r["R_xi"] - 1.18) < 0.05 else ""
        print(
            f"{r['state']:>40s}  {r['n']:>4d}  {r['R_xi']:>6.2f}  "
            f"{mu:>9.4f}  {f:>7.3f}  {mp:>8.1f}  {ny:>8.1f}{marker}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sweep straight-vortex cutoff R and report F(R) + implied proton mass."
    )
    parser.add_argument("states", nargs="+", type=Path, help=".npz trefoil state files")
    parser.add_argument(
        "--r-grid",
        nargs="+",
        type=float,
        default=DEFAULT_R_GRID,
        help="R values in xi units (default: 13-point grid from 0.5 to 3.0)",
    )
    parser.add_argument(
        "--anchor-thickness-xi",
        type=float,
        default=1.0,
        help="Physical boundary exclusion thickness for e_interior (default 1.0 xi)",
    )
    parser.add_argument("--output", type=Path, help="Write JSON results to this file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    r_grid = sorted(set(args.r_grid))

    all_rows: list[dict] = []
    per_state_diagnostics: list[dict] = []

    for state_path in args.states:
        if not state_path.exists():
            print(f"WARNING: {state_path} not found, skipping.", file=sys.stderr)
            continue
        print(f"\nScanning {state_path.name} ...", file=sys.stderr)
        rows = scan_one_state(state_path, r_grid, args.anchor_thickness_xi)
        all_rows.extend(rows)

        slope = local_slope(rows, 1.18)
        stab = stability_in_window(rows, 0.9, 1.5)
        per_state_diagnostics.append(
            {
                "state": state_path.name,
                "n": rows[0]["n"] if rows else None,
                "d_lnF_d_lnR_at_1p18": slope,
                "stability_window": stab,
            }
        )

    print()
    print_table(all_rows)

    # Summary of stability
    print("\n--- Stability summary ---")
    for d in per_state_diagnostics:
        s = d["stability_window"]
        if not s:
            continue
        print(
            f"{d['state']} (n={d['n']}):  "
            f"F(0.90)={s['F_at_lo']:.3f}  F(1.18)={s['F_at_ref_1p18']:.3f}  F(1.50)={s['F_at_hi']:.3f}"
        )
        print(
            f"  d_lnF/d_lnR at 1.18xi = {d['d_lnF_d_lnR_at_1p18']:.2f}"
            f"  dF(0.9->1.18) = {s['delta_F_pct_lo_to_ref']:+.1f}%"
            f"  dF(1.18->1.5) = {s['delta_F_pct_ref_to_hi']:+.1f}%"
        )
        print(
            f"  m_p(0.90)={s['mp_at_lo_MeV']:.0f} MeV  "
            f"m_p(1.18)={s['mp_at_ref_MeV']:.0f} MeV  "
            f"m_p(1.50)={s['mp_at_hi_MeV']:.0f} MeV  "
            f"(observed 938 MeV)"
        )

    payload = {
        "scan_parameters": {
            "r_grid": r_grid,
            "anchor_thickness_xi": args.anchor_thickness_xi,
            "N_Y_paper": N_Y_PAPER,
            "mu0_MeV": MU0_MEV,
        },
        "rows": all_rows,
        "diagnostics": per_state_diagnostics,
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nResults written to {args.output}", file=sys.stderr)
    else:
        print("\n" + json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

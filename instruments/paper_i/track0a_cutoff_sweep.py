"""#77 Track 0a: re-extract N_Y and F at asymptotic-regime cutoff radii.

Pre-registered decision rule (2026-06-02):
  PASS: spread(n_y_straight, n=72 vs n=96) < 5% at any R_cutoff in {1.5, 2.0, 2.5, 3.0} xi
  FAIL: all tested R_cutoff values give spread >= 5%

Also checks:
  - n_y_per_curve_length (arc-length normalised, Track 1)
  - N_Y_phys from ring formula with C_LogSE = 1.880 (Track 0b)

Root cause context:
  At R = 1.18 xi the straight-vortex profile integral is 71% above its asymptotic
  value (core transition zone). At R >= 2.0 xi it is <= 9% above. The hypothesis
  is that n_y_straight diverges as n^1.35 precisely because 1.18 xi is inside the
  transition zone. Moving to R >= 2.0 xi should give a near-asymptotic mu_0 that
  is grid-independent.

Usage:
    python track0a_cutoff_sweep.py [--output OUTPUT.json]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from paper_i.trefoil_breather_observables import (
    ExtractionConfig,
    extract,
    load_state,
    mu_0_straight_vortex,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# States to compare — must share the same penalty config (mu=2000, rho=0.05)
_REPO = Path(__file__).resolve().parents[2]

STATES = [
    ("n48_mu2500", _REPO / "papers/SSV-I/data/penalty-n48-mu2500-rho0p05-2026-05-19.npz"),
    ("n72_mu2000", _REPO / "papers/SSV-I/data/penalty-n72-mu2000-rho0p05-2026-05-19.npz"),
    ("n96_mu2000", _REPO / "papers/SSV-I/data/penalty-n96-mu2000-rho0p05-400steps-2026-06-02.npz"),
]

# Cutoff radii to sweep (xi units)
R_CUTOFFS = [1.18, 1.50, 2.00, 2.50, 3.00]

# Fixed extraction parameters (matching proton_geometric_r_probe.py convention)
R_TUBE_FIXED = 1.5         # tube radius around vortex curve
R_CAVITY = 1.5             # central cavity ball
CAL_ARC_HALF_WIDTH = 0.5
ANCHOR_THICKNESS_XI = 1.0

# Physics-based calibration from ring formula (Track 0b)
C_LOGSE = 1.880            # computed in vortex_ring_core_constant.py


def n_y_physics(e_line: float, e_cavity: float, major_radius: float) -> float:
    """N_Y_phys = (e_line + e_cavity) / mu_0_phys(R_ring)
    where mu_0_phys = pi * (ln(8 * R_ring) - C_LogSE).
    Independent of R_cutoff.
    """
    arg = 8.0 * major_radius
    if arg <= 0:
        return float("nan")
    mu = math.pi * (math.log(arg) - C_LOGSE)
    if mu <= 0:
        return float("nan")
    return (e_line + e_cavity) / mu


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def spread_pct(a: float, b: float) -> float:
    mid = (a + b) / 2.0
    if mid <= 0 or not math.isfinite(a) or not math.isfinite(b):
        return float("nan")
    return abs(a - b) / mid * 100.0


def run(output_path: Path | None) -> None:
    # Load all states upfront
    loaded: dict[str, dict] = {}
    for label, path in STATES:
        p = Path(path)
        if not p.exists():
            print(f"  WARNING: {path} not found, skipping {label}")
            continue
        print(f"Loading {label} ({p.name})...")
        loaded[label] = load_state(p)
        cfg = loaded[label]["cfg"]
        print(f"  n={cfg['n']}, major_radius={cfg['major_radius']:.3f}, "
              f"minor_radius={cfg['minor_radius']:.3f}")

    print()
    results: list[dict] = []

    for R in R_CUTOFFS:
        print(f"=== R_cutoff = {R:.2f} xi ===")
        print(f"  (r_tube fixed at {R_TUBE_FIXED:.2f}, straight_vortex_r_max = {R:.2f})")

        ec = ExtractionConfig(
            r_tube=R_TUBE_FIXED,
            r_cavity=R_CAVITY,
            cal_arc_half_width=CAL_ARC_HALF_WIDTH,
            anchor_thickness_xi=ANCHOR_THICKNESS_XI,
            straight_vortex_r_max=R,
        )

        row_vals: dict[str, dict] = {}
        for label, state in loaded.items():
            obs = extract(state, ec)
            major_r = float(state["cfg"]["major_radius"])
            ny_phys = n_y_physics(obs.e_line, obs.e_cavity, major_r)
            row_vals[label] = {
                "n": obs.n,
                "n_y_straight": obs.n_y_straight,
                "n_y_per_curve_length": obs.n_y_per_curve_length,
                "n_y_per_xi": obs.n_y_per_xi,
                "n_y_phys": ny_phys,
                "f_factor_straight_int": obs.f_factor_straight_int,
                "n_y_times_f_straight": obs.n_y_times_f_straight,
                "mu_0_straight": obs.mu_0_straight,
                "l_curve_geometric": obs.l_curve_geometric,
                "major_radius": major_r,
            }
            print(f"  {label:15s}  n={obs.n:3d}  "
                  f"n_y_straight={obs.n_y_straight:8.3f}  "
                  f"n_y_per_curve={obs.n_y_per_curve_length:8.4f}  "
                  f"n_y_phys={ny_phys:8.3f}  "
                  f"F={obs.f_factor_straight_int:7.4f}")

        # Spreads between n=72 and n=96 (the primary comparison)
        if "n72_mu2000" in row_vals and "n96_mu2000" in row_vals:
            v72 = row_vals["n72_mu2000"]
            v96 = row_vals["n96_mu2000"]
            spreads = {
                "n_y_straight":        spread_pct(v72["n_y_straight"], v96["n_y_straight"]),
                "n_y_per_curve_length":spread_pct(v72["n_y_per_curve_length"], v96["n_y_per_curve_length"]),
                "n_y_phys":            spread_pct(v72["n_y_phys"], v96["n_y_phys"]),
                "f_factor_straight_int":spread_pct(v72["f_factor_straight_int"], v96["f_factor_straight_int"]),
                "n_y_times_f_straight":spread_pct(v72["n_y_times_f_straight"], v96["n_y_times_f_straight"]),
            }
            gate_ny   = "PASS" if spreads["n_y_straight"]         < 5.0 else "FAIL"
            gate_arc  = "PASS" if spreads["n_y_per_curve_length"] < 5.0 else "FAIL"
            gate_phys = "PASS" if spreads["n_y_phys"]             < 5.0 else "FAIL"
            gate_nyf  = "PASS" if spreads["n_y_times_f_straight"] < 5.0 else "FAIL"
            print(f"  Spreads (n72 vs n96):")
            print(f"    n_y_straight:        {spreads['n_y_straight']:6.1f}%  [{gate_ny}]")
            print(f"    n_y_per_curve_len:   {spreads['n_y_per_curve_length']:6.1f}%  [{gate_arc}]  (Track 1)")
            print(f"    n_y_phys (0b):       {spreads['n_y_phys']:6.1f}%  [{gate_phys}]  (Track 0b)")
            print(f"    F_straight:          {spreads['f_factor_straight_int']:6.1f}%")
            print(f"    N_Y*F:               {spreads['n_y_times_f_straight']:6.1f}%  [{gate_nyf}]")
        else:
            spreads = {}
            gate_ny = gate_arc = gate_phys = gate_nyf = "N/A"

        results.append({
            "R_cutoff": R,
            "rows": row_vals,
            "spreads_n72_n96": spreads,
            "gate_n_y_straight": gate_ny,
            "gate_n_y_per_curve": gate_arc,
            "gate_n_y_phys": gate_phys,
            "gate_n_y_times_f": gate_nyf,
        })
        print()

    # Summary
    print("=" * 65)
    print("SUMMARY — pre-registered gate: spread < 5% on n_y_straight (n72 vs n96)")
    print("=" * 65)
    print(f"  {'R_cutoff':>9s}  {'n_y_str spread':>15s}  {'n_y_arc spread':>15s}  "
          f"{'n_y_phys spread':>16s}  {'N_Y*F spread':>13s}")
    print("  " + "-" * 72)
    for r in results:
        sp = r["spreads_n72_n96"]
        if not sp:
            continue
        gn = r["gate_n_y_straight"]
        ga = r["gate_n_y_per_curve"]
        gp = r["gate_n_y_phys"]
        gf = r["gate_n_y_times_f"]
        print(f"  {r['R_cutoff']:9.2f}  "
              f"{sp.get('n_y_straight', float('nan')):11.1f}% [{gn}]  "
              f"{sp.get('n_y_per_curve_length', float('nan')):11.1f}% [{ga}]  "
              f"{sp.get('n_y_phys', float('nan')):12.1f}% [{gp}]  "
              f"{sp.get('n_y_times_f_straight', float('nan')):9.1f}% [{gf}]")

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as fh:
            json.dump(results, fh, indent=2, default=str)
        print(f"\nWrote results to {output_path}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=None)
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.output)

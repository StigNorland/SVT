"""Proton geometric-R probe.

Companion to papers/SSV-I/proton-geometric-r-prereg.md.

For each saved topology-preserving trefoil-breather state, extract a
geometric scale R_geom directly from the relaxed density field (no
imposition), then evaluate the form factor F(R_geom) and compare across
grids.

Two R_geom definitions are computed, both pre-registered:

  R_geom_centerline: minimum inter-strand distance, measured by finding
    the local minima of |psi|^2 in a meridional (r - R_major, z) slice
    at fixed phi=0, then taking half the minimum pairwise distance.

  R_geom_profile: deficit-weighted RMS distance from the major ring
    centerline (effective minor radius of the relaxed configuration).
    Simpler, always well-defined.

For each state and each R_geom definition, we report:
  - R_geom value
  - F at the canonical R = 1.18 xi
  - F at R = R_geom
  - F at R = R_geom_profile * 1.388 (the paper's geometric ratio
    1.18/0.85, applied to the per-state R_geom_profile)
  - Per-state n_y_straight, f_factor, mu_0_straight at each R

Run: python proton_geometric_r_probe.py (from src/paper_i).
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict
from pathlib import Path

import numpy as np

from trefoil_breather_observables import load_state, extract, ExtractionConfig


DATA = Path(__file__).resolve().parents[2] / "papers" / "SSV-I" / "data"

# The three topology-preserving states named in
# papers/SSV-I/static-3d-closure-status-2026-05-28.md
STATES = [
    DATA / "penalty-mu400-rho0p01-n24-hw6-1600steps-2026-05-18.npz",
    DATA / "penalty-best-n48-hw6-800steps-2026-05-19.npz",
    DATA / "penalty-n72-mu2000-rho0p05-2026-05-19.npz",
]


def deficit_weighted_minor_rms(state: dict) -> float:
    """R_geom_profile: deficit-weighted RMS distance from the major ring
    centerline. Deficit weight w = max(0, 1 - |psi|^2 / rho_0); we use
    rho_0 = 1 by the saved-state convention.

    s(r, z) = sqrt((sqrt(x^2+y^2) - R_major)^2 + z^2) is the meridional
    distance from the major ring centerline at radius R_major.
    """
    psi = state["psi"]
    x = state["x"]
    y = state["y"]
    z = state["z"]
    cfg = state["cfg"]
    R_major = float(cfg["major_radius"])

    rho = np.abs(psi) ** 2
    w = np.maximum(0.0, 1.0 - rho)
    r_cyl = np.sqrt(x**2 + y**2)
    s = np.sqrt((r_cyl - R_major) ** 2 + z**2)

    total_w = float(w.sum())
    if total_w <= 0.0:
        return float("nan")
    s_rms_sq = float((w * s**2).sum() / total_w)
    return math.sqrt(s_rms_sq)


def centerline_half_spacing(state: dict, n_phi_samples: int = 24) -> float:
    """R_geom_centerline: meridional minimum inter-strand distance / 2.

    Samples n_phi_samples azimuthal angles phi_k. At each phi_k, projects
    the density onto the meridional slice and finds the in-slice local
    minima of |psi|^2 (vortex core hits). Returns half the minimum
    cross-slice pairwise distance, averaged over phi.

    This is a simple discrete approximation; uses grid-nearest sampling
    rather than a full meridional interpolation.
    """
    psi = state["psi"]
    x = state["x"]
    y = state["y"]
    z = state["z"]
    cfg = state["cfg"]
    R_major = float(cfg["major_radius"])
    rho = np.abs(psi) ** 2

    # We compute phi at every grid point and bin by phi
    r_cyl = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)

    half_spacings = []
    phi_grid = np.linspace(-math.pi, math.pi, n_phi_samples, endpoint=False)
    dphi = (2 * math.pi / n_phi_samples) * 0.5  # half bin width

    for phi_c in phi_grid:
        # nearest-azimuth slice: grid points whose phi is within +/- dphi
        # Handle wrap-around at +/-pi.
        dphi_diff = np.abs(((phi - phi_c) + math.pi) % (2 * math.pi) - math.pi)
        mask = dphi_diff < dphi
        if not mask.any():
            continue

        s_vals = (r_cyl[mask] - R_major)  # signed radial offset
        z_vals = z[mask]
        rho_vals = rho[mask]
        # Find the K=2 lowest-density positions (trefoil at fixed phi-slice
        # has 2 strand-crossings)
        order = np.argsort(rho_vals)
        K = min(3, len(order))  # be tolerant if K>3 strands appear
        picks = order[:K]
        coords = list(zip(s_vals[picks].tolist(), z_vals[picks].tolist()))
        # pairwise distance, take min
        if len(coords) < 2:
            continue
        min_d = math.inf
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                a, b = coords[i], coords[j]
                d = math.hypot(a[0] - b[0], a[1] - b[1])
                if 0.0 < d < min_d:
                    min_d = d
        if math.isfinite(min_d):
            half_spacings.append(0.5 * min_d)

    if not half_spacings:
        return float("nan")
    return float(np.mean(half_spacings))


def run_one_state(state_path: Path) -> dict:
    state = load_state(state_path)
    cfg = state["cfg"]
    n = int(cfg["n"])
    hw = float(cfg["half_width"])
    minor_radius_seed = float(cfg["minor_radius"])

    # Two geometric R candidates
    r_profile = deficit_weighted_minor_rms(state)
    r_centerline = centerline_half_spacing(state)

    # The paper's geometric ratio R/minor = 1.18/0.85 = 1.388 (computed
    # for a trefoil with seed minor_radius=0.85). Apply that ratio to the
    # per-state R_profile to get a "geometric R" if the relaxed minor
    # differs from the seed.
    paper_ratio = 1.18 / 0.85
    r_profile_scaled = r_profile * paper_ratio

    # Evaluate F (and N_Y_str and N_Y*F) at the three candidate R values
    # plus the imposed paper value 1.18 for comparison.
    r_points = {
        "paper_1.18": 1.18,
        "R_profile": r_profile,
        "R_profile_x_paper_ratio": r_profile_scaled,
        "R_centerline_half": r_centerline,
    }

    rows = []
    for label, r_val in r_points.items():
        if not math.isfinite(r_val) or r_val <= 0:
            rows.append({"label": label, "R_xi": r_val, "F": float("nan"), "N_Y_str": float("nan"), "N_Y_x_F": float("nan")})
            continue
        ec = ExtractionConfig(r_tube=1.5, r_cavity=1.5, cal_arc_half_width=0.5,
                              anchor_thickness_xi=1.0, straight_vortex_r_max=r_val)
        s = extract(state, ec)
        rows.append({
            "label": label,
            "R_xi": float(r_val),
            "mu_0_str": float(s.mu_0_straight),
            "F": float(s.f_factor_straight_int),
            "N_Y_str": float(s.n_y_straight),
            "N_Y_x_F": float(s.n_y_times_f_straight),
        })

    return {
        "state": state_path.name,
        "n": n,
        "hw": hw,
        "minor_radius_seed": minor_radius_seed,
        "R_geom_profile": r_profile,
        "R_geom_centerline_half": r_centerline,
        "R_geom_profile_x_paper_ratio": r_profile_scaled,
        "extractions": rows,
    }


def print_results(results: list[dict]) -> None:
    print("=== Per-state R_geom values ===")
    print(f"{'state':>50s}  {'n':>3s}  {'hw':>3s}  {'seed_minor':>10s}  {'R_profile':>10s}  {'R_centr_half':>13s}")
    for r in results:
        print(f"{r['state'][:50]:>50s}  {r['n']:>3d}  {r['hw']:>3.0f}  {r['minor_radius_seed']:>10.4f}  "
              f"{r['R_geom_profile']:>10.4f}  {r['R_geom_centerline_half']:>13.4f}")
    print()

    print("=== F and N_Y * F at each cutoff choice, per state ===")
    for r in results:
        print(f"\n{r['state'][:60]} (n={r['n']}, hw={r['hw']:.0f})")
        print(f"  {'cutoff label':>26s}  {'R/xi':>7s}  {'F':>7s}  {'N_Y_str':>10s}  {'N_Y_str*F':>10s}")
        for row in r["extractions"]:
            R = row["R_xi"]
            F = row["F"]
            NY = row.get("N_Y_str", float("nan"))
            NYF = row.get("N_Y_x_F", float("nan"))
            print(f"  {row['label']:>26s}  {R:>7.3f}  {F:>7.3f}  {NY:>10.3f}  {NYF:>10.3f}")

    # Cross-state agreement at each cutoff choice
    print("\n=== Cross-state agreement of F(R) at each cutoff choice ===")
    labels = [row["label"] for row in results[0]["extractions"]]
    print(f"{'label':>30s}  {'F values across grids':>40s}  {'spread_pct':>12s}")
    for label in labels:
        fs = [row["F"] for r in results for row in r["extractions"] if row["label"] == label and not math.isnan(row["F"])]
        if not fs:
            continue
        spread = 100 * (max(fs) - min(fs)) / np.mean(fs) if fs else float("nan")
        print(f"{label:>30s}  {str([f'{f:.3f}' for f in fs]):>40s}  {spread:>11.1f}%")


def main() -> None:
    results = []
    for sp in STATES:
        if not sp.exists():
            print(f"missing: {sp.name}")
            continue
        print(f"processing {sp.name} ...")
        r = run_one_state(sp)
        results.append(r)
    print()
    print_results(results)


if __name__ == "__main__":
    main()

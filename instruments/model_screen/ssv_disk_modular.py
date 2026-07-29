"""Issue #166 sub-calculation 6: corrected-SSV modular flow on a 2D disk.

Pre-registration:
https://github.com/StigNorland/SVT/issues/166#issuecomment-5124053592

The candidate screen is a two-spatial-dimensional Gaussian field with the
corrected SSV/Bogoliubov dispersion (c_s=1),

    omega^2 = khat^2 (1 + xi^2 khat^2).

Thus xi is a gapless k^2-to-k^4 crossover length, not the scalar mass used by
the earlier #166 toy calculations.  The ground-state covariance is restricted
to a disk and the complete bosonic modular kernels are reconstructed.

This is a necessary-condition test for geometric ball modular flow.  It inserts
no gravitational kernel and supplies no RT/Wald or bulk-state map.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import modular_locality as gaussian


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VII-b" / "results"


def disk_sites(N: int, R: float) -> tuple[np.ndarray, np.ndarray]:
    """Integer lattice sites and radial coordinates for a centered disk."""
    center = 0.5 * (N + 1)
    sites = []
    radii = []
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            radius = float(np.hypot(x - center, y - center))
            if radius <= R:
                sites.append((x, y))
                radii.append(radius)
    return np.asarray(sites, dtype=int), np.asarray(radii, dtype=float)


def disk_correlators(N: int, R: float, xi: float) -> tuple:
    """Restricted X,P for the Dirichlet square and corrected-SSV dispersion."""
    sites, radii = disk_sites(N, R)
    modes = np.arange(1, N + 1)
    k = np.pi * modes / (N + 1)
    eigen_1d = 4.0 * np.sin(0.5 * k) ** 2
    laplace_eigen = eigen_1d[:, None] + eigen_1d[None, :]
    omega = np.sqrt(laplace_eigen * (1.0 + xi * xi * laplace_eigen))

    norm = np.sqrt(2.0 / (N + 1))
    basis_1d = norm * np.sin(np.outer(np.arange(1, N + 1), k))
    restricted_modes = np.asarray(
        [
            np.outer(basis_1d[x - 1], basis_1d[y - 1]).ravel()
            for x, y in sites
        ]
    )
    omega_flat = omega.ravel()
    X = (restricted_modes / (2.0 * omega_flat)) @ restricted_modes.T
    P = (restricted_modes * (0.5 * omega_flat)) @ restricted_modes.T
    return X, P, sites, radii


def _fro_fraction(matrix: np.ndarray, mask: np.ndarray) -> float:
    total = np.linalg.norm(matrix)
    if total == 0:
        return 0.0
    return float(np.linalg.norm(np.where(mask, matrix, 0.0)) / total)


def kernel_diagnostics(
    H_pi: np.ndarray,
    H_phi: np.ndarray,
    sites: np.ndarray,
    radii: np.ndarray,
    R: float,
) -> dict:
    """Complete-kernel diagnostics; H_phi range <=2 is treated as local.

    Range two is retained because the corrected SSV Hamiltonian itself contains
    L^2.  Counting that finite stencil as bilocal would manufacture a negative.
    """
    diagonal_all = np.diag(H_pi)
    # The one-site entangling layer is cutoff-dominated on a pixelated disk.
    # CHM is a continuum bulk profile, so validate it on the fixed inner 75%;
    # the complete-matrix diagnostics below still retain every disk site.
    profile_mask = radii <= 0.75 * R
    diagonal = diagonal_all[profile_mask]
    profile_radii = radii[profile_mask]
    boundary_radius = R + 0.5
    beta = (
        np.maximum(boundary_radius**2 - profile_radii**2, 0.0)
        / boundary_radius
    )
    scale = float(np.dot(diagonal, beta) / np.dot(beta, beta))
    fitted = scale * beta
    diagonal_residual = float(
        np.linalg.norm(diagonal - fitted) / np.linalg.norm(diagonal)
    )
    profile_correlation = float(np.corrcoef(diagonal, beta)[0, 1])

    n = len(sites)
    off_diagonal = ~np.eye(n, dtype=bool)
    hpi_offdiag = _fro_fraction(H_pi, off_diagonal)

    displacement = sites[:, None, :] - sites[None, :, :]
    manhattan = np.abs(displacement).sum(axis=2)
    beyond_range_two = manhattan > 2
    hphi_bilocal = _fro_fraction(H_phi, beyond_range_two)

    combined = float(
        np.sqrt(
            diagonal_residual**2
            + hpi_offdiag**2
            + hphi_bilocal**2
        )
    )
    return {
        "profile_correlation": profile_correlation,
        "profile_interior_site_count": int(profile_mask.sum()),
        "Hpi_CHM_diagonal_residual": diagonal_residual,
        "Hpi_offdiagonal_fraction": hpi_offdiag,
        "Hphi_beyond_range2_fraction": hphi_bilocal,
        "combined_complete_kernel_residual": combined,
        "CHM_fit_scale": scale,
    }


def analyze_case(N: int, R: int, R_over_xi: float | None) -> dict:
    xi = 0.0 if R_over_xi is None else R / R_over_xi
    X, P, sites, radii = disk_correlators(N=N, R=R, xi=xi)
    H_pi = gaussian.modular_H_pi(X, P)
    H_phi = gaussian.modular_H_phi(X, P)
    Xr, Pr = gaussian.reconstruct_covariance(H_pi, H_phi)
    reconstruction_error = float(
        max(
            np.max(np.abs(Xr - X)) / np.max(np.abs(X)),
            np.max(np.abs(Pr - P)) / np.max(np.abs(P)),
        )
    )
    diagnostics = kernel_diagnostics(H_pi, H_phi, sites, radii, R)
    return {
        "N": N,
        "R": R,
        "site_count": len(sites),
        "R_over_xi": "infinity" if R_over_xi is None else R_over_xi,
        "xi_lattice": xi,
        "covariance_reconstruction_error": reconstruction_error,
        **diagnostics,
    }


def blind_nonlocal_control(R: int = 6) -> dict:
    """The complete-kernel metric must see an explicit long-range bilocal."""
    sites, radii = disk_sites(4 * R + 8, R)
    n = len(sites)
    boundary_radius = R + 0.5
    beta = np.maximum(boundary_radius**2 - radii**2, 0.0) / boundary_radius
    H_pi_local = np.diag(beta)
    H_phi_local = np.eye(n)
    local = kernel_diagnostics(H_pi_local, H_phi_local, sites, radii, R)

    H_pi_bilocal = H_pi_local.copy()
    displacement = sites[:, None, :] - sites[None, :, :]
    distances = np.linalg.norm(displacement, axis=2)
    far = distances > 1.2 * R
    H_pi_bilocal[far] = 0.25 * np.sqrt(
        beta[:, None] * beta[None, :]
    )[far]
    bilocal = kernel_diagnostics(H_pi_bilocal, H_phi_local, sites, radii, R)
    baseline = max(local["combined_complete_kernel_residual"], 1e-12)
    return {
        "local_residual": local["combined_complete_kernel_residual"],
        "bilocal_residual": bilocal["combined_complete_kernel_residual"],
        "increase_factor": bilocal["combined_complete_kernel_residual"] / baseline,
        "detected": (
            bilocal["combined_complete_kernel_residual"]
            > 5.0 * baseline
        ),
    }


def _spread_fraction(values: list[float]) -> float:
    mean = float(np.mean(values))
    return float((max(values) - min(values)) / mean) if mean else float("inf")


def run(
    refinements: tuple[tuple[int, int], ...] = ((24, 4), (28, 5), (32, 6)),
) -> dict:
    # The preregistered IR condition is R/xi >= 4.  Sample 4, 8 and 16 so a
    # classification cannot hinge on calling the edge of that range "the IR."
    ratios = (None, 16.0, 8.0, 4.0, 1.0)
    rows = [
        analyze_case(N=N, R=R, R_over_xi=ratio)
        for N, R in refinements
        for ratio in ratios
    ]
    controls = blind_nonlocal_control()

    grouped = {}
    for N, R in refinements:
        case_rows = [row for row in rows if row["N"] == N and row["R"] == R]
        baseline = next(
            row["combined_complete_kernel_residual"]
            for row in case_rows
            if row["R_over_xi"] == "infinity"
        )
        for row in case_rows:
            row["residual_ratio_to_conformal"] = (
                row["combined_complete_kernel_residual"] / baseline
            )
        grouped[(N, R)] = case_rows

    crossover_ratios = [
        next(
            row["residual_ratio_to_conformal"]
            for row in grouped[pair]
            if row["R_over_xi"] == 1.0
        )
        for pair in refinements
    ]
    ir_ratios = [
        next(
            row["residual_ratio_to_conformal"]
            for row in grouped[pair]
            if row["R_over_xi"] == 16.0
        )
        for pair in refinements
    ]
    crossover_spread = _spread_fraction(crossover_ratios)
    ir_spread = _spread_fraction(ir_ratios)

    covariance_ok = max(
        row["covariance_reconstruction_error"] for row in rows
    ) < 1e-4
    conformal_correlations = [
        row["profile_correlation"]
        for row in rows
        if row["R_over_xi"] == "infinity"
    ]
    conformal_ok = min(conformal_correlations) > 0.97
    blind_ok = controls["detected"]
    refinement_ok = crossover_spread < 0.25 and ir_spread < 0.25
    controls_ok = covariance_ok and conformal_ok and blind_ok and refinement_ok

    headline = grouped[refinements[-1]]
    cross = next(row for row in headline if row["R_over_xi"] == 1.0)
    ir = next(row for row in headline if row["R_over_xi"] == 16.0)
    baseline = next(
        row for row in headline if row["R_over_xi"] == "infinity"
    )
    excess_diagnostics = sum(
        cross[name] > 3.0 * baseline[name]
        for name in (
            "Hpi_CHM_diagonal_residual",
            "Hpi_offdiagonal_fraction",
            "Hphi_beyond_range2_fraction",
        )
    )
    t1 = (
        controls_ok
        and cross["residual_ratio_to_conformal"] > 3.0
        and excess_diagnostics >= 2
    )
    t2 = t1 and ir["residual_ratio_to_conformal"] <= 1.5
    t3 = controls_ok and not t1
    ir_failure = (
        controls_ok and ir["residual_ratio_to_conformal"] > 1.5
    )

    if not controls_ok:
        verdict = "INVALID: one or more preregistered controls failed"
    elif t2:
        verdict = (
            "T1+T2: finite-scale modular flow is non-geometric, with IR-only "
            "recovery; standard all-scale reconstruction fails, coarse-grained "
            "IR correspondence remains open"
        )
    elif t1 and ir_failure:
        verdict = (
            "CLEAN NEGATIVE for this candidate: non-geometricity persists into "
            "the tested IR"
        )
    elif t1:
        verdict = "T1: finite-scale non-geometric; IR classification unresolved"
    else:
        verdict = (
            "T3: no preregistered crossover excess; R1 remains open at this "
            "necessary-condition level"
        )

    return {
        "model": "2D corrected-SSV Gaussian, omega^2=khat^2(1+xi^2 khat^2)",
        "refinements": [list(pair) for pair in refinements],
        "rows": rows,
        "blind_nonlocal_control": controls,
        "control_C1_covariance_ok": bool(covariance_ok),
        "control_C2_conformal_profile_ok": bool(conformal_ok),
        "control_C3_blind_nonlocal_ok": bool(blind_ok),
        "control_C4_refinement_ok": bool(refinement_ok),
        "crossover_ratio_spread": crossover_spread,
        "ir_ratio_spread": ir_spread,
        "IR_recovery_tested_at_R_over_xi": 16.0,
        "controls_ok": bool(controls_ok),
        "headline_excess_diagnostic_count": int(excess_diagnostics),
        "T1_finite_scale_nongeometric": bool(t1),
        "T2_IR_only_recovery": bool(t2),
        "T3_R1_remains_open": bool(t3),
        "IR_geometricity_failure": bool(ir_failure),
        "verdict": verdict,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    report = run()
    print("=" * 76)
    print("#166 corrected-SSV 2+1D disk modular test")
    print("=" * 76)
    print(f"\nMODEL: {report['model']}")
    print("\nCONTROLS")
    print(f"  C1 covariance reconstruction: {report['control_C1_covariance_ok']}")
    print(f"  C2 conformal disk profile:    {report['control_C2_conformal_profile_ok']}")
    print(f"  C3 blind bilocal guard:       {report['control_C3_blind_nonlocal_ok']}")
    print(f"  C4 refinement:                {report['control_C4_refinement_ok']}")
    print("\n N   R   R/xi      corr    diag-res   Hpi-off   Hphi-far  combined  /CFT")
    for row in report["rows"]:
        print(
            f"{row['N']:2d}  {row['R']:2d}  {str(row['R_over_xi']):>8s}  "
            f"{row['profile_correlation']:+.4f}  "
            f"{row['Hpi_CHM_diagonal_residual']:.4f}     "
            f"{row['Hpi_offdiagonal_fraction']:.4f}    "
            f"{row['Hphi_beyond_range2_fraction']:.4f}    "
            f"{row['combined_complete_kernel_residual']:.4f}   "
            f"{row['residual_ratio_to_conformal']:.2f}"
        )
    print(f"\nVERDICT: {report['verdict']}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    output = RESULTS / "ssv_disk_modular_receipt.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"\nreceipt -> {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

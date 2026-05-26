"""Full cubic-vertex one-loop self-energy for the muon and electron BdG modes.

Second-stage calculation building on muon_cubic_self_energy.py:

  - Build the BdG matrix at the converged weak-form / combined-Kelvin /
    full-second-variation / smooth-window configuration.
  - Diagonalize. Identify the muon-target eigenmode (lowest positive
    omega in the Kelvin-weighted band) and the electron breather
    eigenmode (lowest positive omega in the m=0 core band).
  - For each external eigenmode, compute the one-loop cubic-vertex
    self-energy

        Sigma_a(omega_a) = sum_{b,c} |V_{a,b,c}|^2 / (omega_a - omega_b - omega_c + i*eps)

    where the matrix element uses the proper Bogoliubov density-perturbation
    profile delta_rho_n = 2 Re[psi_0^* (U_n + V_n^*)] with full angular
    sampling around the torus.

  - Report Re[Sigma_mu/omega_mu - Sigma_e/omega_e] as the candidate
    relative shift to the muon-electron mass ratio.

Status: prototype.

Run example:

  python src/paper_i/muon_cubic_full_self_energy.py \
      --n 31 --half-width 5 --profile-n 800 --kelvin-phi-n 128 --phi-samples 16
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from kelvin_augmented_bdg import (
    AzimuthalMode,
    build_bdg,
    build_modes,
    is_kelvin_mode,
)
from toroidal_background import ToroidalBackground
from toroidal_projection_integrals import ProjectionConfig, projection_window_weight


# ---------------------------------------------------------------------------
# Grid + mode-profile precomputation
# ---------------------------------------------------------------------------
@dataclass
class GridArrays:
    n: int
    r_axis: np.ndarray         # shape (n,)
    z_axis: np.ndarray         # shape (n,)
    cell_area: np.ndarray      # shape (n, n) -- includes 2*pi*r*dr*dz*window
    psi0: np.ndarray           # shape (n, n) complex -- background field
    psi0_amp_sq: np.ndarray    # shape (n, n) real -- |psi_0|^2 with floor
    g3: np.ndarray             # shape (n, n) -- cubic coupling -b/(6 |psi|^4)


def precompute_grid(bg: ToroidalBackground, cfg: ProjectionConfig, b_coupling: float) -> GridArrays:
    n = cfg.n
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    r_axis = np.array([r_min + (i + 0.5) * cfg.dr for i in range(n)])
    z_axis = np.array([z_min + (j + 0.5) * cfg.dz for j in range(n)])
    cell_area = np.zeros((n, n))
    psi0 = np.zeros((n, n), dtype=complex)
    for i, r in enumerate(r_axis):
        if r <= 0.0:
            continue
        for j, z in enumerate(z_axis):
            cell_area[i, j] = 2.0 * math.pi * r * cfg.dr * cfg.dz * projection_window_weight(bg, r, z, cfg)
            psi0[i, j] = bg.psi0(r, z)
    psi0_amp_sq = np.maximum(np.abs(psi0) ** 2, 1.0e-12)
    g3 = -b_coupling / (6.0 * psi0_amp_sq * psi0_amp_sq)
    return GridArrays(n, r_axis, z_axis, cell_area, psi0, psi0_amp_sq, g3)


def precompute_mode_fields(modes: list[AzimuthalMode], grid: GridArrays) -> np.ndarray:
    """Return array shape (N_modes, n, n) -- phi_i(r, z) evaluated on grid."""
    n = grid.n
    fields = np.zeros((len(modes), n, n), dtype=complex)
    for k, mode in enumerate(modes):
        for i, r in enumerate(grid.r_axis):
            for j, z in enumerate(grid.z_axis):
                fields[k, i, j] = mode.field(r, z)
    return fields


# ---------------------------------------------------------------------------
# BdG diagonalisation -> eigenmodes with Bogoliubov u, v coefficients
# ---------------------------------------------------------------------------
@dataclass
class BogoMode:
    omega: float
    u_coeffs: np.ndarray       # shape (N_modes,) complex
    v_coeffs: np.ndarray       # shape (N_modes,) complex
    m_phi: int                 # azimuthal sector (BdG block label)
    weight_core: float         # |u|^2 + |v|^2 weight on m=0 core modes
    weight_kelvin: float       # weight on Kelvin (m=+/-1) modes


def diagonalise_bdg(h: list[list[complex]], modes: list[AzimuthalMode]) -> list[BogoMode]:
    """Diagonalise the BdG Nambu matrix and package eigenmodes.

    Filter to positive-omega eigenvalues with small imaginary part and
    positive Bogoliubov (Krein) norm. Bogoliubov-normalise to |u|^2 - |v|^2 = 1
    so that the density-perturbation amplitudes are in physical units.
    Tag each with its azimuthal sector by inspecting which input modes
    carry significant weight in u and v.
    """
    H = np.array(h, dtype=complex)
    eigvals, eigvecs = np.linalg.eig(H)
    N = len(modes)
    bogo_modes: list[BogoMode] = []
    for k in range(2 * N):
        val = eigvals[k]
        if abs(val.imag) > 1.0e-4:
            continue
        omega = val.real
        if omega < 1.0e-5:
            continue
        vec = eigvecs[:, k]
        u = vec[:N]
        v = vec[N:]
        # Bogoliubov-normalise: |u|^2 - |v|^2 = 1.
        krein = float(np.real(np.vdot(u, u) - np.vdot(v, v)))
        if abs(krein) < 1.0e-10:
            # Near-zero Krein norm: Goldstone or unphysical artifact; skip.
            continue
        if krein < 0:
            # Negative-Krein partner; skip (its positive partner appears elsewhere).
            continue
        scale = 1.0 / math.sqrt(krein)
        u = u * scale
        v = v * scale
        # Determine azimuthal sector by majority weight.
        # All input modes contributing to a single BdG block share m_phi,
        # because the BdG operator is block-diagonal in m_phi.
        weight_by_m: dict[int, float] = {}
        for i, mode in enumerate(modes):
            w = abs(u[i]) ** 2 + abs(v[i]) ** 2
            weight_by_m[mode.m_phi] = weight_by_m.get(mode.m_phi, 0.0) + w
        m_phi = max(weight_by_m, key=lambda m: weight_by_m[m])
        # Core / Kelvin weights from the mode names.
        core_idx = [i for i, m in enumerate(modes) if not is_kelvin_mode(m)]
        kelvin_idx = [i for i, m in enumerate(modes) if is_kelvin_mode(m)]
        wc = float(sum(abs(u[i]) ** 2 + abs(v[i]) ** 2 for i in core_idx))
        wk = float(sum(abs(u[i]) ** 2 + abs(v[i]) ** 2 for i in kelvin_idx))
        norm = wc + wk
        bogo_modes.append(
            BogoMode(omega=omega, u_coeffs=u, v_coeffs=v, m_phi=m_phi,
                     weight_core=wc / norm if norm else 0.0,
                     weight_kelvin=wk / norm if norm else 0.0)
        )
    bogo_modes.sort(key=lambda m: m.omega)
    return bogo_modes


# ---------------------------------------------------------------------------
# Density-perturbation amplitudes A_+ (r, z) per BdG eigenmode
# ---------------------------------------------------------------------------
def density_amplitudes(
    bogo_modes: list[BogoMode],
    mode_fields: np.ndarray,
    grid: GridArrays,
) -> np.ndarray:
    """Return array shape (N_bogo, n, n) of complex amplitudes A_+(r,z) such that

      delta_rho_n(r, z, phi) = A_+(r,z) * e^{i m_n phi} + A_+^*(r,z) * e^{-i m_n phi}

    derived from A_+(r,z) = psi_0^*(r,z) u_n(r,z) + psi_0(r,z) v_n(r,z)
    where u_n(r,z) = sum_i u_coeffs[i] * phi_i(r,z) and similarly for v_n.
    """
    N_bogo = len(bogo_modes)
    n = grid.n
    out = np.zeros((N_bogo, n, n), dtype=complex)
    psi0_c = grid.psi0.conjugate()
    for idx, bogo in enumerate(bogo_modes):
        # u_n(r,z) field summed over input modes
        u_field = np.einsum("i,ijk->jk", bogo.u_coeffs, mode_fields)
        v_field = np.einsum("i,ijk->jk", bogo.v_coeffs, mode_fields)
        out[idx] = psi0_c * u_field + grid.psi0 * v_field
    return out


# ---------------------------------------------------------------------------
# Cubic-vertex matrix element with angular sampling
# ---------------------------------------------------------------------------
def cubic_matrix_element(
    A_a: np.ndarray, m_a: int,
    A_b: np.ndarray, m_b: int,
    A_c: np.ndarray, m_c: int,
    grid: GridArrays,
    phi_samples: int = 16,
) -> complex:
    """Compute V_{a,b,c} = int g_3 delta_rho_a delta_rho_b delta_rho_c d^3x
    by sampling phi.

    delta_rho_n(r, z, phi) = A_n * e^{i m_n phi} + A_n^* * e^{-i m_n phi}

    The phi integral is a discrete average × (2*pi / phi_samples) × phi_samples
    = 2*pi factor (this 2*pi is NOT in cell_area; we add it here).
    """
    phis = 2.0 * math.pi * np.arange(phi_samples) / phi_samples
    dphi = 2.0 * math.pi / phi_samples
    total = 0.0 + 0.0j
    # The integrand on the meridional grid is:
    #   integrand(r, z) = g_3 * (1/(2pi)) * sum over phi of delta_rho_a delta_rho_b delta_rho_c
    # The cell_area includes 2*pi*r*dr*dz already (with the angular jacobian
    # for an *azimuthally-uniform* field). For an angular-dependent integrand
    # we need the FULL angular integral, not 2*pi factor. So we divide by 2*pi
    # to remove the already-included angular jacobian, then add the phi-sum * dphi.
    for phi in phis:
        rho_a = A_a * np.exp(1j * m_a * phi) + A_a.conjugate() * np.exp(-1j * m_a * phi)
        rho_b = A_b * np.exp(1j * m_b * phi) + A_b.conjugate() * np.exp(-1j * m_b * phi)
        rho_c = A_c * np.exp(1j * m_c * phi) + A_c.conjugate() * np.exp(-1j * m_c * phi)
        integrand = grid.g3 * rho_a * rho_b * rho_c
        # cell_area already has 2*pi*r*dr*dz; the 2*pi was the trivial angular
        # integral assuming an angular-uniform integrand. We need to replace
        # that with the explicit phi sample × dphi. Net factor: (1/(2*pi)) * dphi
        total += np.sum(integrand * grid.cell_area) * dphi / (2.0 * math.pi)
    return complex(total)


def self_energy(
    external: BogoMode,
    bogo_modes: list[BogoMode],
    A_amps: np.ndarray,
    grid: GridArrays,
    phi_samples: int = 16,
    eps: float = 1.0e-3,
) -> complex:
    """Compute Sigma_a(omega_a) = sum_{b,c} |V_{a,b,c}|^2 / (omega_a - omega_b - omega_c + i*eps)."""
    omega_a = external.omega
    m_a = external.m_phi
    A_a = A_amps[bogo_modes.index(external)] if external in bogo_modes else None
    if A_a is None:
        # Match by identity manually if needed
        for idx, mode in enumerate(bogo_modes):
            if mode is external:
                A_a = A_amps[idx]
                break
    sigma = 0.0 + 0.0j
    for ib, mode_b in enumerate(bogo_modes):
        for ic, mode_c in enumerate(bogo_modes):
            # Avoid double-counting: only b <= c. Symmetry factor 1 if b == c,
            # else 2.
            if ic < ib:
                continue
            sym = 1.0 if ib == ic else 2.0
            V = cubic_matrix_element(
                A_a, m_a,
                A_amps[ib], mode_b.m_phi,
                A_amps[ic], mode_c.m_phi,
                grid, phi_samples=phi_samples,
            )
            denom = omega_a - mode_b.omega - mode_c.omega + 1j * eps
            sigma += sym * abs(V) ** 2 / denom
    return sigma


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Full cubic-vertex one-loop self-energy for the muon eigenmode."
    )
    parser.add_argument("--n", type=int, default=31)
    parser.add_argument("--half-width", type=float, default=5.0)
    parser.add_argument("--profile-n", type=int, default=800)
    parser.add_argument("--alpha", type=float, default=1.0 / 137.035999084)
    parser.add_argument("--core-basis", choices=("two", "four"), default="four")
    parser.add_argument("--kelvin-seed", choices=("helicity", "displacement", "breathing", "combined"), default="combined")
    parser.add_argument("--current-curl-model", choices=("linear", "full"), default="full")
    parser.add_argument("--reduced-operator-form", choices=("strong", "weak"), default="weak")
    parser.add_argument("--projection-window", choices=("hard", "smooth"), default="smooth")
    parser.add_argument("--window-radius", type=float, default=4.0)
    parser.add_argument("--window-taper", type=float, default=1.0)
    parser.add_argument("--kelvin-phi-n", type=int, default=128)
    parser.add_argument("--kelvin-core-radius", type=float, default=1.0)
    parser.add_argument("--lambda-perp", type=float, default=0.815243293607)  # pi/4 * 1.038
    parser.add_argument("--phi-samples", type=int, default=16, help="Angular samples for cubic integral.")
    parser.add_argument("--b-coupling", type=float, default=1.0)
    parser.add_argument("--epsilon", type=float, default=1.0e-3, help="Small imaginary part in resolvent.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("SSV-I -- full cubic-vertex one-loop self-energy")
    print(f"grid n={args.n}, hw={args.half_width}, kelvin_phi_n={args.kelvin_phi_n}, "
          f"phi_samples={args.phi_samples}")
    print(f"lambda_perp={args.lambda_perp:.9e}")
    print()

    from vortex_profile import VortexProfile
    vortex = VortexProfile.solve(n=args.profile_n, x_max=20.0)
    bg = ToroidalBackground(alpha=args.alpha, f0=vortex.value, f0_prime=vortex.derivative)

    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        profile="numerical",
        profile_n=args.profile_n,
        profile_x_max=20.0,
        chi_parity="sin",
        projection_window=args.projection_window,
        window_radius=args.window_radius,
        window_taper=args.window_taper,
    )

    include_four = args.core_basis == "four"
    modes = build_modes(bg, cfg, include_core_four=include_four, kelvin_seed=args.kelvin_seed)
    print(f"input modes: {len(modes)}")

    grid = precompute_grid(bg, cfg, args.b_coupling)
    mode_fields = precompute_mode_fields(modes, grid)
    print(f"grid arrays ready: {grid.n}x{grid.n}, |psi_0|^2 at core "
          f"= {grid.psi0_amp_sq[grid.n//2, grid.n//2]:.4e}")

    # Build the BdG matrix using the existing infrastructure.
    h = build_bdg(
        bg, modes, cfg,
        operator_model="logse",
        kelvin_dispersion="self-induction",
        chiral_mix=0.0,
        bridge_model="current-curl",
        lambda_perp=args.lambda_perp,
        kelvin_phi_n=args.kelvin_phi_n,
        kelvin_core_radius=args.kelvin_core_radius,
        current_curl_model=args.current_curl_model,
        reduced_operator_form=args.reduced_operator_form,
    )
    bogo_modes = diagonalise_bdg(h, modes)
    print(f"positive-omega Bogoliubov eigenmodes: {len(bogo_modes)}")
    print()

    # Density-perturbation amplitudes for spectrum diagnostics
    A_amps_for_diag = density_amplitudes(bogo_modes, mode_fields, grid)
    A_norm = np.sqrt(np.sum(np.abs(A_amps_for_diag) ** 2 * grid.cell_area[None, :, :], axis=(1, 2)))

    print("BdG spectrum:")
    print(f"{'#':>3} {'omega':>12} {'m_phi':>6} {'core_w':>8} {'kelvin_w':>8} {'|A_+|_L2':>10}")
    for i, b in enumerate(bogo_modes):
        marker = ""
        if A_norm[i] < 1.0e-3 * max(A_norm):
            marker = " (suppressed density -- Goldstone-like)"
        print(f"{i:>3} {b.omega:>12.6f} {b.m_phi:>+6d} "
              f"{b.weight_core:>8.3f} {b.weight_kelvin:>8.3f} {A_norm[i]:>10.3e}{marker}")
    print()

    # Identify the muon-target and electron-breather eigenmodes using:
    # - Density-perturbation L2 norm above a small fraction of the max
    #   (excludes Goldstone-like phase modes)
    # - Muon: closest m=+/-1 with sizeable density perturbation
    # - Electron: lowest m=0 with sizeable density perturbation
    target_omega_mu = 0.207
    rho_floor = 1.0e-2 * max(A_norm)
    physical_idx = [i for i in range(len(bogo_modes)) if A_norm[i] > rho_floor]

    candidates_muon = sorted(
        [(abs(bogo_modes[i].omega - target_omega_mu), bogo_modes[i])
         for i in physical_idx if abs(bogo_modes[i].m_phi) == 1],
        key=lambda t: t[0],
    )
    muon_mode = candidates_muon[0][1] if candidates_muon else None
    m0_modes = [bogo_modes[i] for i in physical_idx if bogo_modes[i].m_phi == 0]
    m0_modes.sort(key=lambda m: m.omega)
    electron_mode = m0_modes[0] if m0_modes else None

    if muon_mode is None or electron_mode is None:
        print("Could not identify muon and electron eigenmodes")
        return

    print(f"muon-target mode:    omega = {muon_mode.omega:.6f}  m_phi = {muon_mode.m_phi:+d}  "
          f"core/kelvin = {muon_mode.weight_core:.3f}/{muon_mode.weight_kelvin:.3f}")
    print(f"electron mode:       omega = {electron_mode.omega:.6f}  m_phi = {electron_mode.m_phi:+d}  "
          f"core/kelvin = {electron_mode.weight_core:.3f}/{electron_mode.weight_kelvin:.3f}")
    print()

    # Density-perturbation amplitudes
    print("Computing density-perturbation amplitudes...")
    A_amps = density_amplitudes(bogo_modes, mode_fields, grid)

    # Cubic-vertex self-energies
    print("Computing Sigma_mu(omega_mu)...")
    sigma_mu = self_energy(muon_mode, bogo_modes, A_amps, grid,
                           phi_samples=args.phi_samples, eps=args.epsilon)
    print(f"  Sigma_mu = {sigma_mu.real:+.6e} + i {sigma_mu.imag:+.6e}")
    print(f"  Sigma_mu / omega_mu = {(sigma_mu / muon_mode.omega).real:+.6e}")
    print()

    print("Computing Sigma_e(omega_e)...")
    sigma_e = self_energy(electron_mode, bogo_modes, A_amps, grid,
                          phi_samples=args.phi_samples, eps=args.epsilon)
    print(f"  Sigma_e = {sigma_e.real:+.6e} + i {sigma_e.imag:+.6e}")
    print(f"  Sigma_e / omega_e = {(sigma_e / electron_mode.omega).real:+.6e}")
    print()

    delta = (sigma_mu / muon_mode.omega).real - (sigma_e / electron_mode.omega).real
    print(f"RESIDUAL RELATIVE SHIFT  Delta = Sigma_mu/omega_mu - Sigma_e/omega_e")
    print(f"  = {delta:+.6e}")
    print()
    omega_ratio = muon_mode.omega / electron_mode.omega
    print(f"tree-level omega_mu/omega_e            = {omega_ratio:.6f}")
    print(f"first-pass corrected ratio            = {omega_ratio * (1.0 + delta):.6f}")
    print(f"target omega_mu/omega_c                = 0.207000")


if __name__ == "__main__":
    main()

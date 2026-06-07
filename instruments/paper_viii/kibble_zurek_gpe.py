"""
SSV-VIII Prediction C1: Kibble-Zurek defect density from the LogSE
void-to-saturation transition.

Numerical strategy. The bulk LogSE
    i hbar d_t Psi = -(hbar^2/2 m_0) nabla^2 Psi
                    + b ln(|Psi|^2 / rho_0) Psi
linearised around the void state |Psi|^2 -> 0 is destabilising for any small
fluctuation; the saturated state |Psi|^2 = rho_0 is the late-time attractor.
The relevant quench parameter is the effective chemical potential mu(t)
(equivalently the saturation pressure b ln rho_0) ramped from below
to above its critical value at finite rate 1/tau_Q.

For the *defect-counting* purpose only the universality class matters --
the long-wavelength dynamics of the symmetry-breaking transition in 2D
are captured by the dissipative time-dependent Ginzburg-Landau (TDGL)
equation, which is in the same KZ universality class as the
finite-temperature LogSE crossover. We therefore solve

    d_t Psi = nabla^2 Psi + ( mu(t) - g |Psi|^2 ) Psi + eta(x,t)

with mu(t) = mu_0 + (mu_f - mu_0) t/tau_Q, eta a complex white-noise
Gaussian forcing, g = 1, and periodic boundary conditions. The
phase-defect density n_def is extracted by phase-winding count and the
Kibble-Zurek scaling
    n_def * xi^d ~ (tau_0/tau_Q)^( d nu / (1 + nu z) )
is extracted from a tau_Q scan. The fitted exponent is reported and
compared with mean-field (nu = 1/2, z = 2 => 2D exponent 0.5) and
3D XY (nu ~ 0.67, z = 2 in 3D => exponent ~ 0.86).

The 2D mean-field exponent and a quench-rate window are then used to
predict the equivalent 3D dimensionless defect density at a
cosmologically realistic tau_Q / tau_0 = O(H^-1 / xi/c), yielding the
order-of-magnitude prediction for eta = n_baryon / n_photon.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------


@dataclass
class QuenchParams:
    N: int = 64
    L: float = 64.0
    dt: float = 0.05
    tau_Q: float = 100.0
    mu_initial: float = -1.0
    mu_final: float = +1.0
    g: float = 1.0
    noise_amp: float = 0.05      # thermal noise std-dev
    settle_steps: int = 800      # steps after quench ends to let defects
                                 # annihilate towards the asymptotic density
    seed: int = 0


def evolve(params: QuenchParams) -> tuple[np.ndarray, np.ndarray]:
    """Stochastic 2D TDGL evolution. Returns (|Psi|^2, arg Psi)."""
    rng = np.random.default_rng(params.seed)
    N, L, dt = params.N, params.L, params.dt
    dx = L / N

    # Initial state: small random complex fluctuations (the "void")
    psi = (
        params.noise_amp
        * (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N)))
    )

    # Spectral Laplacian operator (linear part handled implicitly each step)
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    K2 = KX**2 + KY**2

    # Quench: linear ramp of mu over t in [0, tau_Q]
    quench_steps = int(round(params.tau_Q / dt))
    total_steps = quench_steps + params.settle_steps

    sqrt_dt = math.sqrt(dt)
    noise_scale = params.noise_amp * sqrt_dt / dx  # standard scaling for
                                                    # 2D real noise on a grid

    for n in range(total_steps):
        t = n * dt
        if n < quench_steps:
            mu = (
                params.mu_initial
                + (params.mu_final - params.mu_initial) * (t / params.tau_Q)
            )
        else:
            mu = params.mu_final

        # Linear half-step in Fourier space (Laplacian + mu)
        # Operator: L = -K2 + mu  (note sign convention; nabla^2 -> -K2)
        # exp(L dt/2)
        Lop = -K2 + mu
        prop = np.exp(Lop * (0.5 * dt))
        psi = np.fft.ifft2(prop * np.fft.fft2(psi))

        # Nonlinear full-step in real space: subtract g|psi|^2 psi explicitly
        rho = np.abs(psi) ** 2
        psi = psi * np.exp(-params.g * rho * dt)

        # Noise (Euler-Maruyama on a unit-variance complex grid)
        psi = psi + noise_scale * (
            rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
        )

        # Linear half-step
        psi = np.fft.ifft2(prop * np.fft.fft2(psi))

    rho_final = np.abs(psi) ** 2
    phase_final = np.angle(psi)
    return rho_final, phase_final


# ---------------------------------------------------------------------------
# Defect counting (phase-winding plaquettes)
# ---------------------------------------------------------------------------


def count_defects(phase: np.ndarray, rho: np.ndarray, rho_cut: float) -> int:
    """Count plaquettes around which the phase winds by +/- 2 pi.
    Only count plaquettes whose four corners all have rho > rho_cut
    (so we exclude regions where the order parameter is still near zero
    and the phase is meaningless).
    """
    def wrap(x):
        return (x + np.pi) % (2 * np.pi) - np.pi

    p = phase
    d1 = wrap(np.roll(p, -1, axis=0) - p)
    d2 = wrap(np.roll(np.roll(p, -1, axis=0), -1, axis=1) - np.roll(p, -1, axis=0))
    d3 = wrap(np.roll(p, -1, axis=1) - np.roll(np.roll(p, -1, axis=0), -1, axis=1))
    d4 = wrap(p - np.roll(p, -1, axis=1))
    winding = np.round((d1 + d2 + d3 + d4) / (2 * np.pi))

    r = rho
    r1 = np.roll(r, -1, axis=0)
    r2 = np.roll(np.roll(r, -1, axis=0), -1, axis=1)
    r3 = np.roll(r, -1, axis=1)
    saturated = (r > rho_cut) & (r1 > rho_cut) & (r2 > rho_cut) & (r3 > rho_cut)

    n_pos = int(np.sum((winding > 0) & saturated))
    n_neg = int(np.sum((winding < 0) & saturated))
    return n_pos + n_neg


# ---------------------------------------------------------------------------
# Driver: scan quench rate, extract KZ exponent, compare with eta
# ---------------------------------------------------------------------------


def run_scan(output_path: Path) -> dict:
    tau_Q_values = [20.0, 40.0, 80.0, 160.0, 320.0]
    n_seeds = 6
    L = 160.0
    N = 160
    rho_cut = 0.05  # exclude defect cores; saturated bulk has rho ~ 0.9

    table = []
    for tau_Q in tau_Q_values:
        counts = []
        for seed in range(n_seeds):
            params = QuenchParams(N=N, L=L, dt=0.1, tau_Q=tau_Q, seed=seed)
            print(f"  tau_Q={tau_Q}, seed={seed} ...", flush=True)
            rho, phase = evolve(params)
            counts.append(count_defects(phase, rho, rho_cut))
        mean = float(np.mean(counts))
        std = float(np.std(counts))
        area = L * L
        n_def = mean / area
        table.append(
            dict(tau_Q=tau_Q, mean_count=mean, std=std, density=n_def)
        )

    # Fit n_def ~ tau_Q^(-alpha) in log-log
    logs_x = np.log([row["tau_Q"] for row in table])
    logs_y = np.log([row["density"] for row in table])
    slope, intercept = np.polyfit(logs_x, logs_y, 1)
    alpha_fit = -float(slope)

    # 2D mean field (nu = 1/2, z = 2): alpha_2D = d nu / (1 + nu z) = 0.5
    # 3D XY (nu = 0.6717, z = 2): alpha_3D = 3 * 0.6717 / (1 + 1.3434) ~ 0.86
    nu_XY = 0.6717
    exp3D_XY = 3 * nu_XY / (1 + nu_XY * 2)

    # Cosmological eta estimate:
    #   n_def_3D * xi^3 ~ (tau_0/tau_Q)^alpha_3D
    # Take alpha_3D = 3/4 (mean field). Then for eta = 6e-10:
    #   tau_Q/tau_0 = eta^(-1/alpha_3D)
    eta_obs = 6e-10
    tau_ratio_MF = eta_obs ** (-1.0 / 0.75)
    tau_ratio_XY = eta_obs ** (-1.0 / exp3D_XY)

    # In SSV the natural unit is tau_0 = xi/c (the LogSE characteristic time)
    # and tau_Q is the Hubble time at the saturation epoch: tau_Q = H^-1.
    # H^-1 / (xi/c) is a huge dimensionless ratio. With xi ~ 10^-15 m
    # (proton-size healing length from Paper I) and H^-1 ~ 4.4e17 s:
    #   tau_Q/tau_0 = H^-1 c / xi ~ 4.4e17 * 3e8 / 1e-15 = 1.3e41.
    tau_Q_cosmo = 1.3e41
    eta_pred_MF = tau_Q_cosmo ** (-0.75)
    eta_pred_XY = tau_Q_cosmo ** (-exp3D_XY)

    result = dict(
        grid=dict(N=N, L=L),
        seeds=n_seeds,
        scan=table,
        fitted_alpha_2D=alpha_fit,
        meanfield_alpha_2D=0.5,
        meanfield_alpha_3D=0.75,
        XY_alpha_3D=exp3D_XY,
        eta_observed=eta_obs,
        tau_Q_over_tau_0_required_MF=tau_ratio_MF,
        tau_Q_over_tau_0_required_XY=tau_ratio_XY,
        cosmological_tau_Q_over_tau_0=tau_Q_cosmo,
        eta_predicted_MF=eta_pred_MF,
        eta_predicted_XY=eta_pred_XY,
    )

    output_path.write_text(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "kibble_zurek_results.json"
    res = run_scan(out)
    print(json.dumps(res, indent=2))

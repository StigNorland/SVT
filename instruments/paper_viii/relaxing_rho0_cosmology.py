"""Prediction C2 helper: slowly relaxing rho_0 cosmology.

The issue #51 closure condition asks for either a numerical Lambda from the
SSV equation of state or an observational discriminator between LambdaCDM and
slow relaxation of the saturated background rho_0.

The current papers do not specify the absolute saturation pressure P_0, so the
numerical Lambda route is underdetermined.  This module encodes the minimal
observable route:

    Lambda_eff(a) = Lambda_0 a^beta,

where beta = d ln Lambda_eff / d ln a.  beta = 0 is exactly LambdaCDM.  A
nonzero beta is the distinctive C2 signal and is equivalent, for the constant
beta toy model, to w_eff = -1 - beta / 3.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class Cosmology:
    """Flat matter + radiation + dark-energy baseline."""

    h0_km_s_mpc: float = 67.4
    omega_m: float = 0.315
    omega_r: float = 9.2e-5

    @property
    def omega_de(self) -> float:
        return 1.0 - self.omega_m - self.omega_r


def lambda_ratio(z: float | np.ndarray, beta: float) -> float | np.ndarray:
    """Return Lambda_eff(z) / Lambda_eff(0) for a constant beta model."""

    return np.power(1.0 / (1.0 + np.asarray(z)), beta)


def w_eff(beta: float) -> float:
    """Constant-w equivalent of Lambda_eff(a) = Lambda_0 a^beta."""

    return -1.0 - beta / 3.0


def e2(z: float | np.ndarray, beta: float = 0.0, cosmo: Cosmology = Cosmology()) -> float | np.ndarray:
    """Dimensionless Hubble function squared, E(z)^2 = H(z)^2 / H0^2."""

    z_arr = np.asarray(z, dtype=float)
    zp1 = 1.0 + z_arr
    return (
        cosmo.omega_r * zp1**4
        + cosmo.omega_m * zp1**3
        + cosmo.omega_de * lambda_ratio(z_arr, beta)
    )


def e_z(z: float | np.ndarray, beta: float = 0.0, cosmo: Cosmology = Cosmology()) -> float | np.ndarray:
    """Dimensionless Hubble function E(z)."""

    return np.sqrt(e2(z, beta=beta, cosmo=cosmo))


def hubble_fractional_residual(
    z: float | np.ndarray,
    beta: float,
    cosmo: Cosmology = Cosmology(),
) -> float | np.ndarray:
    """Fractional H(z) residual relative to beta = 0 LambdaCDM."""

    return e_z(z, beta=beta, cosmo=cosmo) / e_z(z, beta=0.0, cosmo=cosmo) - 1.0


def comoving_distance_mpc(
    z: float,
    beta: float = 0.0,
    cosmo: Cosmology = Cosmology(),
    n_grid: int = 4097,
) -> float:
    """Flat-universe line-of-sight comoving distance in Mpc."""

    if z < 0:
        raise ValueError("redshift must be non-negative")
    if z == 0:
        return 0.0

    c_km_s = 299_792.458
    grid = np.linspace(0.0, z, n_grid)
    integral = np.trapezoid(1.0 / e_z(grid, beta=beta, cosmo=cosmo), grid)
    return float((c_km_s / cosmo.h0_km_s_mpc) * integral)


def luminosity_distance_mpc(
    z: float,
    beta: float = 0.0,
    cosmo: Cosmology = Cosmology(),
    n_grid: int = 4097,
) -> float:
    """Flat-universe luminosity distance in Mpc."""

    return (1.0 + z) * comoving_distance_mpc(z, beta=beta, cosmo=cosmo, n_grid=n_grid)


def distance_modulus_residual(
    z: float,
    beta: float,
    cosmo: Cosmology = Cosmology(),
    n_grid: int = 4097,
) -> float:
    """SN distance-modulus residual, Delta mu(beta) relative to LambdaCDM."""

    dl = luminosity_distance_mpc(z, beta=beta, cosmo=cosmo, n_grid=n_grid)
    dl_lcdm = luminosity_distance_mpc(z, beta=0.0, cosmo=cosmo, n_grid=n_grid)
    if dl_lcdm == 0:
        return 0.0
    return float(5.0 * math.log10(dl / dl_lcdm))


def bao_dm_fractional_residual(
    z: float,
    beta: float,
    cosmo: Cosmology = Cosmology(),
    n_grid: int = 4097,
) -> float:
    """Fractional transverse BAO D_M residual relative to LambdaCDM.

    In a flat model D_M equals the line-of-sight comoving distance.  The sound
    horizon r_d cancels in the fractional residual if r_d is held fixed by the
    high-redshift calibration.
    """

    dm = comoving_distance_mpc(z, beta=beta, cosmo=cosmo, n_grid=n_grid)
    dm_lcdm = comoving_distance_mpc(z, beta=0.0, cosmo=cosmo, n_grid=n_grid)
    if dm_lcdm == 0:
        return 0.0
    return float(dm / dm_lcdm - 1.0)


def sample_observable_table(
    betas: Iterable[float] = (-0.1, 0.1),
    redshifts: Iterable[float] = (0.3, 0.8, 1.5, 2.5),
    cosmo: Cosmology = Cosmology(),
) -> list[dict[str, float]]:
    """Build a small table of C2 observables for a few beta values."""

    rows: list[dict[str, float]] = []
    for beta in betas:
        for z in redshifts:
            rows.append(
                {
                    "beta": float(beta),
                    "z": float(z),
                    "w_eff": w_eff(beta),
                    "lambda_ratio": float(lambda_ratio(z, beta)),
                    "delta_H_over_H": float(hubble_fractional_residual(z, beta, cosmo=cosmo)),
                    "delta_DM_over_DM": bao_dm_fractional_residual(z, beta, cosmo=cosmo),
                    "delta_mu_mag": distance_modulus_residual(z, beta, cosmo=cosmo),
                }
            )
    return rows


def build_result() -> dict:
    cosmo = Cosmology()
    return {
        "model": "Lambda_eff(a) = Lambda_0 a^beta",
        "beta_definition": "beta = d ln Lambda_eff / d ln a",
        "lcdm_limit": {"beta": 0.0, "w_eff": -1.0},
        "planck_2018_baseline": asdict(cosmo) | {"omega_de": cosmo.omega_de},
        "sample_observables": sample_observable_table(cosmo=cosmo),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate issue #51 C2 observable table.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("instruments/paper_viii/relaxing_rho0_cosmology_results.json"),
    )
    args = parser.parse_args()

    result = build_result()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

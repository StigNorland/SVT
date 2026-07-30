"""Generated Paper II values for the corrected profile propagation (#220)."""

from __future__ import annotations

from functools import lru_cache
import math

import numpy as np

from paper_i.corrected_vortex_profile import CorrectedVortexProfile

from lperp_core_integral import compute_core_integrals
from vortex_cap_mass import ALPHA, PHI_GR, line_tension
import wmass_cap_scale_resolution as wmass
import issue_218_values as paper_i_values
import series_values


R_MAX = 15.0
N_PROFILE = 4000


@lru_cache(maxsize=1)
def _profile():
    return CorrectedVortexProfile.solve(
        x_min=1.0e-4,
        x_max=R_MAX,
        n=N_PROFILE,
    )


@lru_cache(maxsize=1)
def _integrals() -> tuple[float, float, float]:
    profile = _profile()
    return compute_core_integrals(
        np.asarray(profile.xs),
        np.asarray(profile.fs),
        np.asarray(profile.fps),
        R_MAX,
    )


@lru_cache(maxsize=1)
def _line_tension() -> dict[str, float]:
    return line_tension(_profile(), R_MAX)


def profile_slope() -> float:
    return _profile().slope


def i_curl() -> float:
    return _integrals()[0]


def j_bend() -> float:
    return _integrals()[1]


def k_bend() -> float:
    return _integrals()[2]


def jk_over_four() -> float:
    _, j_value, k_value = _integrals()
    return (j_value + k_value) / 4.0


def tau() -> float:
    return _line_tension()["tau"]


def lambda_bend_local() -> float:
    return ALPHA**-2 * jk_over_four()


def lambda_bend_gap() -> float:
    required = PHI_GR**3 / ALPHA**3
    return required / lambda_bend_local()


def linear_running_shortfall_pct() -> float:
    required = PHI_GR**3 / ALPHA**3
    candidate = lambda_bend_local() * (PHI_GR / ALPHA)
    return 100.0 * (1.0 - candidate / required)


def local_equilibrium_radius() -> float:
    return wmass.R_equilibrium_xi(lambda_bend_local(), tau())


def local_equilibrium_mass_gev() -> float:
    return wmass.m_W_from_Rcap(local_equilibrium_radius())


def candidate_cap_tau_correction_pct() -> float:
    return 100.0 * tau() / (PHI_GR / ALPHA)


def conditional_w_mass_gev() -> float:
    return wmass.m_W_from_Rcap(PHI_GR / ALPHA)


def candidate_proton_pion_ratio_low() -> float:
    return paper_i_values.candidate_product_low() / 2.0


def candidate_proton_pion_ratio_high() -> float:
    return paper_i_values.candidate_product_high() / 2.0


def candidate_proton_pion_deviation_low_pct() -> float:
    observed = (
        series_values.proton_mass_mev()
        / series_values.charged_pion_mass_mev()
    )
    return 100.0 * (candidate_proton_pion_ratio_low() / observed - 1.0)


def candidate_proton_pion_deviation_high_pct() -> float:
    observed = (
        series_values.proton_mass_mev()
        / series_values.charged_pion_mass_mev()
    )
    return 100.0 * (candidate_proton_pion_ratio_high() / observed - 1.0)

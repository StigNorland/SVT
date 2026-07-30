"""Generated-value source for the Paper I issue #218 recalculation.

This module performs saved-state post-processing only.  It does not regenerate
or relax any 3D field.  Results are cached within one receipt/check process so
each saved state is loaded once.
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np

from corrected_vortex_profile import CorrectedVortexProfile
from series_values import (
    electron_mass_mev,
    inverse_fine_structure,
    proton_mass_mev,
)
from trefoil_breather_observables import (
    ExtractionConfig,
    extract,
    load_state,
    mu_0_straight_vortex,
)
from vortex_profile import VortexProfile


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "papers" / "SSV-I" / "data"
RADII = (1.0, 1.18, 1.5, 2.0, 3.0)
STATE_PATHS = {
    24: DATA_ROOT / "penalty-mu400-rho0p01-n24-hw6-1600steps-2026-05-18.npz",
    48: DATA_ROOT / "penalty-best-n48-hw6-800steps-2026-05-19.npz",
    72: DATA_ROOT / "penalty-n72-mu2000-rho0p05-2026-05-19.npz",
}


@lru_cache(maxsize=1)
def form_factor_table() -> dict[tuple[int, float], float]:
    """Re-extract corrected form factors from the three recorded states."""
    table: dict[tuple[int, float], float] = {}
    for n, path in STATE_PATHS.items():
        state = load_state(path)
        for radius in RADII:
            cfg = ExtractionConfig(
                r_tube=1.5,
                r_cavity=1.5,
                cal_arc_half_width=0.5,
                anchor_thickness_xi=1.0,
                straight_vortex_r_max=radius,
            )
            table[(n, radius)] = float(
                extract(state, cfg).f_factor_straight_int
            )
    return table


def _f(n: int, radius: float) -> float:
    return form_factor_table()[(n, radius)]


def form_factor_n24_r100() -> float:
    return _f(24, 1.0)


def form_factor_n24_r118() -> float:
    return _f(24, 1.18)


def form_factor_n24_r150() -> float:
    return _f(24, 1.5)


def form_factor_n24_r200() -> float:
    return _f(24, 2.0)


def form_factor_n24_r300() -> float:
    return _f(24, 3.0)


def form_factor_n48_r100() -> float:
    return _f(48, 1.0)


def form_factor_n48_r118() -> float:
    return _f(48, 1.18)


def form_factor_n48_r150() -> float:
    return _f(48, 1.5)


def form_factor_n48_r200() -> float:
    return _f(48, 2.0)


def form_factor_n48_r300() -> float:
    return _f(48, 3.0)


def form_factor_n72_r100() -> float:
    return _f(72, 1.0)


def form_factor_n72_r118() -> float:
    return _f(72, 1.18)


def form_factor_n72_r150() -> float:
    return _f(72, 1.5)


def form_factor_n72_r200() -> float:
    return _f(72, 2.0)


def form_factor_n72_r300() -> float:
    return _f(72, 3.0)


def fine_grid_form_factor_low() -> float:
    return form_factor_n72_r118()


def fine_grid_form_factor_high() -> float:
    return form_factor_n48_r118()


def fine_grid_form_factor_mean() -> float:
    return 0.5 * (
        fine_grid_form_factor_low() + fine_grid_form_factor_high()
    )


def candidate_n_y() -> float:
    return 3.007


def energy_star_mev() -> float:
    return electron_mass_mev() * inverse_fine_structure()


def candidate_product_low() -> float:
    return candidate_n_y() * fine_grid_form_factor_low()


def candidate_product_high() -> float:
    return candidate_n_y() * fine_grid_form_factor_high()


def candidate_mass_low_mev() -> float:
    return candidate_product_low() * energy_star_mev()


def candidate_mass_high_mev() -> float:
    return candidate_product_high() * energy_star_mev()


def candidate_mass_low_deviation_pct() -> float:
    return 100.0 * (candidate_mass_low_mev() / proton_mass_mev() - 1.0)


def candidate_mass_high_deviation_pct() -> float:
    return 100.0 * (candidate_mass_high_mev() / proton_mass_mev() - 1.0)


def cutoff_log_slope() -> float:
    return math.log(form_factor_n72_r150() / form_factor_n72_r118()) / math.log(
        1.5 / 1.18
    )


def cutoff_drop_pct() -> float:
    return 100.0 * (
        1.0 - form_factor_n72_r150() / form_factor_n72_r118()
    )


def _tension_for_profile(
    profile: VortexProfile,
    r_max: float = 1.18,
    n_pts: int = 4000,
) -> float:
    rs = np.linspace(1.0e-4, r_max, n_pts)
    fs = np.array([profile.value(r) for r in rs])
    fps = np.array([profile.derivative(r) for r in rs])
    rho = fs * fs
    energy_density = 0.5 * (fps * fps + fs * fs / (rs * rs))
    energy_density += 0.5 * (
        rho * np.log(np.maximum(rho, 1.0e-300)) - rho + 1.0
    )
    return float(np.trapezoid(2.0 * math.pi * rs * energy_density, rs))


@lru_cache(maxsize=1)
def legacy_to_corrected_nyf_factor() -> float:
    legacy = VortexProfile.solve(x_min=1.0e-4, x_max=20.0, n=4000)
    legacy_tension = _tension_for_profile(legacy)
    corrected_tension = mu_0_straight_vortex(0.5, 1.18)
    return (legacy_tension / corrected_tension) ** 2


def corrected_combined_n_y_f() -> float:
    rows = json.loads(
        (DATA_ROOT / "geometry-continuation-2026-06-03.json").read_text(
            encoding="utf-8"
        )
    )
    selected = next(
        row for row in rows if row["R"] == 2.5 and row["a"] == 0.85
    )
    return float(selected["n_y_times_f"]) * legacy_to_corrected_nyf_factor()


@lru_cache(maxsize=1)
def corrected_profile() -> CorrectedVortexProfile:
    return CorrectedVortexProfile.solve(x_min=1.0e-4, x_max=20.0, n=4000)


def half_density_radius() -> float:
    profile = corrected_profile()
    lo, hi = 0.0, 4.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if profile.value(mid) ** 2 < 0.5:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

"""Focused guards for issue #220's Paper II profile propagation."""

from __future__ import annotations

import math
from pathlib import Path
import sys

import numpy as np
import pytest


SRC_ROOT = Path(__file__).resolve().parents[2]
for sub in ("paper_i", "paper_ii"):
    path = str(SRC_ROOT / sub)
    if path not in sys.path:
        sys.path.insert(0, path)

from corrected_vortex_profile import CorrectedVortexProfile  # noqa: E402
from vortex_profile import VortexProfile as LegacyVortexProfile  # noqa: E402
from lperp_core_integral import compute_core_integrals  # noqa: E402
from vortex_cap_mass import line_tension  # noqa: E402


@pytest.fixture(scope="module")
def profiles():
    kwargs = {"x_min": 1.0e-4, "x_max": 15.0, "n": 2400}
    return (
        CorrectedVortexProfile.solve(**kwargs),
        LegacyVortexProfile.solve(**kwargs),
    )


def _arrays(profile):
    return (
        np.asarray(profile.xs),
        np.asarray(profile.fs),
        np.asarray(profile.fps),
    )


def test_active_and_control_coefficients_are_distinct(profiles):
    corrected, legacy = profiles
    assert corrected.LOG_COEFFICIENT == 1.0
    assert legacy.LOG_COEFFICIENT == 2.0
    assert corrected.slope == pytest.approx(
        legacy.slope / math.sqrt(2.0),
        rel=2.0e-4,
    )


def test_core_integrals_obey_exact_coordinate_scaling(profiles):
    corrected, legacy = profiles
    corrected_values = compute_core_integrals(*_arrays(corrected), 15.0)
    legacy_values = compute_core_integrals(*_arrays(legacy), 15.0)
    i_corr, j_corr, k_corr = corrected_values
    i_legacy, j_legacy, k_legacy = legacy_values
    assert i_corr == pytest.approx(i_legacy / 2.0, rel=1.0e-3)
    assert j_corr == pytest.approx(j_legacy / 2.0, rel=1.0e-3)
    assert k_corr == pytest.approx(k_legacy, rel=1.0e-3)


def test_corrected_line_tension_uses_shifted_energy_and_single_log_tail(profiles):
    corrected, _ = profiles
    result = line_tension(corrected, 15.0)
    expected_tail = math.pi * math.log(result["r_cap"] / 15.0)
    assert result["tau_tail"] == pytest.approx(expected_tail, rel=1.0e-12)
    assert result["tau"] == pytest.approx(18.624, rel=5.0e-4)


def test_only_explicit_legacy_control_import_remains():
    paper_ii = SRC_ROOT / "paper_ii"
    direct_consumers = {
        "lperp_core_integral.py",
        "lr_su4_cross_term_audit.py",
        "chiral_cap_equilibrium.py",
        "lperp_bphys_check.py",
        "vortex_cap_mass.py",
    }
    for name in direct_consumers:
        source = (paper_ii / name).read_text(encoding="utf-8")
        if name == "lperp_bphys_check.py":
            assert "VortexProfile as LegacyVortexProfile" in source
            assert "CorrectedVortexProfile" in source
        else:
            assert "from vortex_profile import VortexProfile" not in source
            assert "CorrectedVortexProfile" in source

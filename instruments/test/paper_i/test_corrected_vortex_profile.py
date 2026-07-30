"""Focused controls for the issue #218 corrected vortex baseline."""

import math
import sys
from pathlib import Path

import pytest


PAPER_I = Path(__file__).resolve().parents[2] / "paper_i"
if str(PAPER_I) not in sys.path:
    sys.path.insert(0, str(PAPER_I))

from corrected_vortex_profile import CorrectedVortexProfile  # noqa: E402
from vortex_profile import VortexProfile, vortex_rhs  # noqa: E402
from vortex_ring_core_constant import (  # noqa: E402
    corrected_core_constant_from_legacy,
    h7_result,
)


def test_legacy_and_corrected_coefficients_are_explicitly_distinct():
    assert VortexProfile.LOG_COEFFICIENT == 2.0
    assert CorrectedVortexProfile.LOG_COEFFICIENT == 1.0


def test_rhs_negative_control_rejects_the_legacy_coefficient():
    x, f, fp = 1.3, 0.7, 0.2
    _, legacy_fpp = vortex_rhs(
        x, f, fp, log_coefficient=VortexProfile.LOG_COEFFICIENT
    )
    _, corrected_fpp = vortex_rhs(
        x, f, fp, log_coefficient=CorrectedVortexProfile.LOG_COEFFICIENT
    )
    assert legacy_fpp != corrected_fpp
    assert legacy_fpp - corrected_fpp == pytest.approx(
        f * math.log(f * f)
    )


def test_independent_solvers_obey_the_exact_coordinate_rescaling():
    root2 = math.sqrt(2.0)
    legacy = VortexProfile.solve(
        x_min=1.0e-4 / root2,
        x_max=10.0,
        n=1200,
    )
    corrected = CorrectedVortexProfile.solve(
        x_min=1.0e-4,
        x_max=10.0 * root2,
        n=1200,
    )

    assert corrected.slope * root2 == pytest.approx(
        legacy.slope, rel=3.0e-4
    )
    for legacy_x in (0.1, 0.5, 1.0, 3.0, 7.0):
        corrected_x = root2 * legacy_x
        assert corrected.value(corrected_x) == pytest.approx(
            legacy.value(legacy_x), rel=3.0e-4, abs=2.0e-5
        )
        assert corrected.derivative(corrected_x) * root2 == pytest.approx(
            legacy.derivative(legacy_x), rel=6.0e-4, abs=2.0e-5
        )


def test_corrected_profile_boundary_and_monotonicity_controls():
    profile = CorrectedVortexProfile.solve(x_max=12.0, n=1400)
    samples = [profile.value(0.1 * i) for i in range(1, 101)]
    assert profile.value(0.0) == 0.0
    assert 0.0 < profile.slope < 1.0
    assert all(0.0 <= value <= 1.0001 for value in samples)
    assert all(right >= left - 2.0e-5 for left, right in zip(samples, samples[1:]))
    assert profile.value(12.0) == pytest.approx(1.0)


def test_core_constant_coordinate_transformation_has_required_log_shift():
    legacy_c = 1.88
    assert corrected_core_constant_from_legacy(legacy_c) == pytest.approx(
        legacy_c + 0.5 * math.log(2.0)
    )


def test_h7_optimizer_starts_inside_domain_for_corrected_core_constant():
    result = h7_result(2.2263)
    assert result["r_e"] > math.exp(2.2263) / 8.0
    assert math.isfinite(result["err_mu_pct"])
    assert math.isfinite(result["err_tau_pct"])

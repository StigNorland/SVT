"""Focused operator controls for the issue #218 BdG normalization."""

import sys
from pathlib import Path

import pytest


PAPER_I = Path(__file__).resolve().parents[2] / "paper_i"
if str(PAPER_I) not in sys.path:
    sys.path.insert(0, str(PAPER_I))

from direct_bdg_projection import l_operator, m_operator  # noqa: E402
from corrected_vortex_profile import CorrectedVortexProfile  # noqa: E402
from toroidal_projection_integrals import (  # noqa: E402
    ProjectionConfig,
    logse_stiffness_integrand,
)
from vortex_core_mode_spectrum import (  # noqa: E402
    bdg_spectrum,
    build_radial_grid,
)


class UniformBackground:
    xi = 1.0

    @staticmethod
    def psi0(r: float, z: float) -> complex:
        return 1.0 + 0.0j


def test_profile_matched_uniform_bdg_blocks_are_l_one_m_one():
    bg = UniformBackground()
    cfg = ProjectionConfig(half_width=1.0, n=200)

    def constant_field(r: float, z: float) -> complex:
        return 1.0 + 0.0j

    assert l_operator(
        bg, constant_field, 1.0, 0.0, cfg, "profile-logse"
    ) == pytest.approx(1.0)
    assert m_operator(
        bg, constant_field, 1.0, 0.0, cfg, "profile-logse"
    ) == pytest.approx(1.0)


def test_corrected_kinetic_term_is_minus_laplacian_not_minus_half_laplacian():
    bg = UniformBackground()
    cfg = ProjectionConfig(half_width=1.0, n=200)

    def radial_quadratic(r: float, z: float) -> complex:
        return complex(r * r)

    # The cylindrical Laplacian of r^2 is four, while the uniform
    # profile-matched potential contributes +r^2=+1 at r=1.
    assert l_operator(
        bg, radial_quadratic, 1.0, 0.0, cfg, "profile-logse"
    ) == pytest.approx(-3.0, abs=2.0e-10)


def test_longitudinal_logse_density_hessian_has_positive_sign():
    bg = UniformBackground()
    cfg = ProjectionConfig(half_width=1.0, n=200)

    def real_constant_mode(r: float, z: float) -> complex:
        return 1.0 + 0.0j

    # delta(|psi|^2)=2 for this real mode.  The normalized Hessian
    # contribution is 1/2 * delta-rho^2/rho = +2.
    assert logse_stiffness_integrand(
        bg, real_constant_mode, real_constant_mode, 1.0, 0.0, cfg
    ) == pytest.approx(2.0)


def test_translation_goldstone_mode_is_retained_as_a_signed_bdg_partner():
    profile = CorrectedVortexProfile.solve(x_max=10.0, n=1000)
    r, dr = build_radial_grid(8.0, 160)

    minus = bdg_spectrum(-1, profile, r, dr, n_modes=4)
    plus = bdg_spectrum(1, profile, r, dr, n_modes=4)

    assert abs(minus[0]) < 0.04
    assert minus[0] == pytest.approx(-plus[0], abs=1.0e-8)

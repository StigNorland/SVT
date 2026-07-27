"""Tests for #184 E3 — SSV-II's Aharonov-Bohm sector, machine-checked.

These lock in *negative* results. A failure here means either the finding was
wrong or the paper changed; both require re-opening the damage report, never a
silent edit of the assertion.
"""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_ii")
if p not in sys.path:
    sys.path.insert(0, p)

from ssv_ii_ab_audit_2026 import (  # noqa: E402
    E_CHARGE,
    E_MASS,
    M0,
    RHO0,
    aharonov_bohm_phase,
    berry_phase_dimension,
    dims,
    flux_lhs_dimension,
    flux_quantisation_consistent,
    flux_rhs_dimension,
    haldane_wu_is_loop_invariant,
    haldane_wu_phase,
    is_dimensionless,
    required_e_dimension,
    required_rho_perp_dimension,
    step_star_is_circular,
)


# --- E3a: Haldane-Wu is extensive, an AB phase is topological --------------

def test_haldane_wu_phase_grows_with_enclosed_area():
    """gamma_C = 2 pi N_C is unbounded as the loop grows at fixed density."""
    small = haldane_wu_phase(number_density=1.0, area=1.0)
    large = haldane_wu_phase(number_density=1.0, area=1000.0)
    assert large == 1000 * small


def test_haldane_wu_phase_is_not_loop_invariant():
    """The decisive structural difference from an AB phase."""
    assert haldane_wu_is_loop_invariant() is False


def test_aharonov_bohm_phase_depends_only_on_winding_number():
    """SSV-II eq:AB_SSV needs exactly this: no geometry, no density."""
    assert aharonov_bohm_phase(3) == 3 * aharonov_bohm_phase(1)


def test_haldane_wu_cannot_reproduce_ab_phase_for_all_loops():
    """No fixed prefactor maps 2 pi N_C onto 2 pi n for every loop.

    Fix n and enclose it with two loops of different area: the Haldane-Wu phase
    differs, the AB phase does not. So the identification at main.tex:832 fails
    independently of any coupling constant.
    """
    n = 1
    ab = aharonov_bohm_phase(n)
    hw_small = haldane_wu_phase(1.0, 1.0)
    hw_large = haldane_wu_phase(1.0, 4.0)
    assert hw_small != hw_large
    for scale in (ab / hw_small, ab / hw_large):
        assert not (
            abs(scale * hw_small - ab) < 1e-12
            and abs(scale * hw_large - ab) < 1e-12
        )


# --- E3b/E3c: the symbol ``e`` ---------------------------------------------

def test_berry_phase_not_dimensionless_when_e_is_a_charge():
    """main.tex:838 as printed, with e the elementary charge of eq:AB_standard."""
    assert berry_phase_dimension(E_CHARGE) != {}
    assert not is_dimensionless(E_CHARGE)


def test_berry_phase_dimensionless_only_when_e_is_a_mass():
    assert berry_phase_dimension(E_MASS) == {}


def test_required_e_dimension_is_mass():
    assert required_e_dimension() == dims(M0)


def test_step_star_is_circular():
    """e/m_0 = 1 is an identity of the notation, not a derived result."""
    assert step_star_is_circular() is True


# --- E3d: eq:flux_quantisation ---------------------------------------------

def test_flux_quantisation_is_dimensionally_inconsistent():
    assert flux_quantisation_consistent(RHO0) is False


def test_flux_mismatch_is_inverse_area_per_time():
    """LHS/RHS differs by L^-2 T^-1 -- not absorbable into a dimensionless alpha."""
    lhs, rhs = flux_lhs_dimension(), flux_rhs_dimension()
    assert lhs != rhs
    keys = set(lhs) | set(rhs)
    delta = {k: lhs.get(k, 0) - rhs.get(k, 0) for k in keys}
    delta = {k: v for k, v in delta.items() if v != 0}
    assert len(delta) == 2
    assert set(delta.values()) == {-2, -1}


def test_required_rho_perp_is_not_a_density():
    """rho_perp would have to be M T L^-1, so rho_perp = alpha rho_0 cannot hold."""
    assert required_rho_perp_dimension() != dims(RHO0)

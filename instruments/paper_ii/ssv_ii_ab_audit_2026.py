"""SSV-II Aharonov-Bohm sector audit (#184, 2026-07-27).

Machine-checkable form of the E3 finding, so it is reproducible rather than
asserted in prose.  Mirrored by
``instruments/test/paper_ii/test_ssv_ii_ab_audit_2026.py``.

Context
-------
The C-gate left SSV-II C4 (``HaldaneWu1985``) as ``PENDING-PRIMARY`` because the
1985 PRL is pre-arXiv and paywalled, and the E-gate deferred every claim that
depended on it.  The open-access proxy ``polkinghorne2021`` (arXiv:2101.07438)
has since settled it: the Haldane-Wu geometric phase is ``gamma_C = 2 pi N_C``
with ``N_C`` the number of *condensate atoms* enclosed by the vortex path.

That reopens SSV-II ``main.tex:829-869``, which this module checks.

Findings encoded here
---------------------
E3a  the Haldane-Wu phase is *extensive*: it scales with enclosed area times
     density, so it is unbounded as the loop grows and is NOT invariant under
     deformation of the loop.  An Aharonov-Bohm phase must be both.  So
     Haldane-Wu cannot supply SSV-II eq:AB_SSV whatever the prefactor.
E3b  eq (838), gamma_Berry = (e/hbar) n kappa_0, is dimensionless only if the
     symbol ``e`` carries the dimensions of MASS -- in SI and in natural units
     alike.  It is used as an electric charge four equations earlier
     (eq:flux_quantisation, Phi_0 = h/e).
E3c  therefore step (star), ``e/m_0 = 1``, is not a physical consequence of the
     medium having one mass scale; it is forced by whatever makes eq (838)
     dimensionally well formed.  The argument is circular.
E3d  eq:flux_quantisation is dimensionally inconsistent as printed: with
     rho_perp = alpha rho_0 a mass density, c rho_perp kappa_0 has dimensions
     M T^-2, while the asserted h has M L^2 T^-1.  The mismatch is L^-2 T^-1.

     (This docstring, and SSV-II main.tex, previously gave both dimensions one
     power of T out -- M T^-3 and M L^2 T^-2, the latter an energy rather than an
     action.  The MISMATCH, which is the load-bearing quantity and what the code
     below actually computes, was correct throughout; only the two intermediate
     dimensions quoted in prose were wrong.  Found by the #198 Part B checker,
     instruments/tools/dimensions.py, in a paper that had already passed the
     C/E/N gates -- which is the argument for having the checker.)

Nothing here depends on the D1 branch decision; these are unit identities.
"""

from __future__ import annotations

from sympy.physics.units import Dimension
from sympy.physics.units.definitions.dimension_definitions import (
    charge, length, mass, time)
from sympy.physics.units.systems.si import dimsys_SI

# --------------------------------------------------------------------------
# dimensions of the symbols SSV-II uses in sec:aharonov_bohm
# --------------------------------------------------------------------------

DIMENSIONLESS: dict = {}

HBAR = mass * length**2 / time          # J s;  h and hbar share dimensions
C = length / time
M0 = mass                               # order-parameter mass
KAPPA0 = HBAR / M0                      # kappa_0 = h/m_0, circulation  L^2/T
RHO0 = mass / length**3                 # vacuum MASS density (SSV-I, E5)
E_CHARGE = charge                       # e read as an electric charge
E_MASS = mass                           # e read as a mass


def dims(expr: Dimension) -> dict:
    """Dimensional dependencies, with the SI system's own normalisation."""
    return dict(dimsys_SI.get_dimensional_dependencies(expr))


def is_dimensionless(expr: Dimension) -> bool:
    return dims(expr) == DIMENSIONLESS


# --------------------------------------------------------------------------
# E3a -- Haldane-Wu is extensive, an AB phase is topological
# --------------------------------------------------------------------------

def haldane_wu_phase(number_density, area):
    """gamma_C = 2 pi N_C, with N_C the enclosed condensate ATOM number.

    Verbatim source: polkinghorne2021 abstract and Eq. (S1); see
    ``papers/cited/notes/polkinghorne2021.md``.
    """
    from math import pi
    return 2 * pi * number_density * area


def aharonov_bohm_phase(n):
    """gamma_AB = 2 pi n -- depends only on the enclosed winding number.

    Deliberately takes no loop geometry: that is the whole point of the
    contrast with :func:`haldane_wu_phase`.
    """
    from math import pi
    return 2 * pi * n


def haldane_wu_is_loop_invariant(number_density=1.0) -> bool:
    """False.  Enlarging the loop at fixed enclosed defect changes the phase."""
    return haldane_wu_phase(number_density, 1.0) == haldane_wu_phase(
        number_density, 2.0)


# --------------------------------------------------------------------------
# E3b/E3c -- what must ``e`` be for eq (838) to have units?
# --------------------------------------------------------------------------

def berry_phase_dimension(e_dimension):
    """Dimensions of SSV-II eq (838):  gamma = (e/hbar) * n * kappa_0."""
    return dims(e_dimension * KAPPA0 / HBAR)


def required_e_dimension():
    """Solve (e/hbar) kappa_0 = 1 for e.  Gives hbar/kappa_0 = m_0: a MASS."""
    return dims(HBAR / KAPPA0)


def step_star_is_circular() -> bool:
    """True.

    eq (838) is well formed only when ``e`` has mass dimension; the paper's
    medium has a single mass scale m_0; so ``e = m_0`` and ``e/m_0 = 1`` is an
    identity of the notation, not a derived coincidence.  Step (star) at
    ``main.tex:853`` therefore cannot carry the weight put on it.
    """
    return required_e_dimension() == dims(M0) and not is_dimensionless(
        E_CHARGE * KAPPA0 / HBAR)


# --------------------------------------------------------------------------
# E3d -- eq:flux_quantisation
# --------------------------------------------------------------------------

def flux_lhs_dimension(rho_perp=RHO0, e_dimension=E_CHARGE):
    """Phi_B = (c_perp rho_perp / e) * n * kappa_0, as printed at main.tex:820."""
    return dims(C * rho_perp * KAPPA0 / e_dimension)


def flux_rhs_dimension(e_dimension=E_CHARGE):
    """The asserted result n * h/e = n * Phi_0."""
    return dims(HBAR / e_dimension)


def flux_quantisation_consistent(rho_perp=RHO0) -> bool:
    return flux_lhs_dimension(rho_perp) == flux_rhs_dimension()


def required_rho_perp_dimension():
    """What rho_perp would have to be:  h/(c kappa_0) = m_0/c,  i.e. M T L^-1.

    Not a density of any kind -- so ``rho_perp = alpha rho_0`` cannot be right
    as printed, whatever the value of alpha.
    """
    return dims(HBAR / (C * KAPPA0))


if __name__ == "__main__":  # pragma: no cover
    print("E3a  Haldane-Wu loop-invariant?      ", haldane_wu_is_loop_invariant())
    print("E3b  gamma with e = charge           ", berry_phase_dimension(E_CHARGE))
    print("E3b  gamma with e = mass             ", berry_phase_dimension(E_MASS))
    print("E3b  e must have dimensions          ", required_e_dimension())
    print("E3c  step (star) circular?           ", step_star_is_circular())
    print("E3d  flux LHS                        ", flux_lhs_dimension())
    print("E3d  flux RHS (h/e)                  ", flux_rhs_dimension())
    print("E3d  consistent?                     ", flux_quantisation_consistent())
    print("E3d  rho_perp would have to be       ", required_rho_perp_dimension())

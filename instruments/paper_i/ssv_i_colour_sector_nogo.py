"""SSV-I colour sector: what three relative phases can and cannot furnish (#183).

Context
-------
The #182 audit withdrew the proton "Y-junction of three quantized vortex
filaments" (D2): it is absent from the cited sources and forbidden in a
one-component U(1) condensate, where quantized circulation forces sum(n_i) = 0
at any node.  The dependent identifications -- *quarks* with three independent
filaments, *colour* with phase orientation at the node -- were marked
UNSUPPORTED because they presuppose the junction.

The author's assessment (2026-07-27) is that three-filaments = quarks is not
merely unsupported but **wrong**, and that repairing it is future work rather
than an editing matter.  This module checks whether a structural obstruction
can be stated precisely, so the open problem is posed sharply for whoever picks
it up.

Result
------
There is one, and it is not about the junction at all -- it survives even if a
three-leg node were somehow admitted.

SSV-I obtains colour from "120 degree separation in phase space" among three
legs.  Three legs carry three phases, one of which is the overall (gauge) phase,
leaving **two** independent relative phases.  Locking them at 120 degrees gives
the cyclic group **Z_3**.

Z_3 is the **centre** of SU(3), not SU(3).  It reproduces exactly the countable
features that made the identification attractive -- there are three of them, and
only Z_3-neutral combinations are physical (triality) -- while supplying **none**
of the non-abelian content: SU(3) has 8 generators, the construction reaches at
most the 2-dimensional Cartan subalgebra, so the **6 off-diagonal (root)
generators are missing**.  Those are precisely the generators that *change*
colour: the gluons.

So the construction can produce a three-ness and a neutrality condition, but no
colour-changing dynamics, no gluons, and no asymptotic freedom.  That is a
different physical claim from QCD colour, not an approximation to it.

Two further obstructions, recorded but not the subject of this module:

* **Fractional charge.**  Quarks carry +-1/3, +-2/3.  Quantized circulation is
  integer-valued; fractional winding in a *one-component* condensate is
  forbidden by the same argument that forbids the junction.
* **Spin.**  Quarks are spin-1/2.  Issue #178 established pi_3(S^1) = 0: the
  bare theory has no fermionic solitons at all.

Mirrored by ``instruments/test/paper_i/test_ssv_i_colour_sector_nogo.py``.
"""

from __future__ import annotations

import numpy as np

OMEGA = np.exp(2j * np.pi / 3)


# --------------------------------------------------------------------------
# what three relative phases actually generate
# --------------------------------------------------------------------------

def independent_relative_phases(n_legs: int = 3) -> int:
    """n legs carry n phases; the overall phase is gauge, leaving n-1."""
    return n_legs - 1


def z3_elements() -> list[np.ndarray]:
    """The 120-degree phase-locked configurations, as 3x3 matrices."""
    return [OMEGA**k * np.eye(3) for k in range(3)]


def z3_is_abelian() -> bool:
    els = z3_elements()
    return all(
        np.allclose(a @ b, b @ a) for a in els for b in els
    )


# --------------------------------------------------------------------------
# SU(3), and what is missing
# --------------------------------------------------------------------------

def gell_mann() -> list[np.ndarray]:
    """The 8 generators of su(3)."""
    l = [np.zeros((3, 3), dtype=complex) for _ in range(8)]
    l[0][0, 1] = l[0][1, 0] = 1
    l[1][0, 1], l[1][1, 0] = -1j, 1j
    l[2][0, 0], l[2][1, 1] = 1, -1
    l[3][0, 2] = l[3][2, 0] = 1
    l[4][0, 2], l[4][2, 0] = -1j, 1j
    l[5][1, 2] = l[5][2, 1] = 1
    l[6][1, 2], l[6][2, 1] = -1j, 1j
    l[7] = np.diag([1, 1, -2]).astype(complex) / np.sqrt(3)
    return l


def su3_dimension() -> int:
    return len(gell_mann())


def cartan_dimension() -> int:
    """Rank of su(3): the diagonal generators, lambda_3 and lambda_8."""
    return sum(
        1 for g in gell_mann() if np.allclose(g, np.diag(np.diag(g)))
    )


def missing_generators() -> int:
    """The off-diagonal (root) generators -- the colour-CHANGING ones."""
    return su3_dimension() - cartan_dimension()


def z3_is_the_centre_of_su3() -> bool:
    """Every Z_3 element commutes with every su(3) generator, and Z_3 elements
    are the only scalars in SU(3) that do so."""
    return all(
        np.allclose(z @ g, g @ z) for z in z3_elements() for g in gell_mann()
    )


def phase_construction_reaches_su3() -> bool:
    """False.  Relative phases furnish an abelian group; SU(3) is not abelian."""
    return not z3_is_abelian()


if __name__ == "__main__":  # pragma: no cover
    print(f"independent relative phases (3 legs) : {independent_relative_phases()}")
    print(f"Z_3 abelian?                         : {z3_is_abelian()}")
    print(f"Z_3 is the centre of SU(3)?          : {z3_is_the_centre_of_su3()}")
    print(f"dim SU(3)                            : {su3_dimension()}")
    print(f"  reachable (Cartan)                 : {cartan_dimension()}")
    print(f"  MISSING (gluons/root generators)   : {missing_generators()}")
    print(f"phase construction reaches SU(3)?    : {phase_construction_reaches_su3()}")

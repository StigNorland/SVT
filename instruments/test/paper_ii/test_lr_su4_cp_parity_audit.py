"""Tests for #81 sign audit: a parity/CPT obstruction makes the sign of λ_cw moot.
The chiral 16 and its mirror 16bar are CP conjugates (SU(4)'s 3rd colour bit makes
P_c CP-odd), so any CP-even chiral-shear energy keeps them degenerate."""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_ii")
if p not in sys.path:
    sys.path.insert(0, p)

from cp1_logse_16_assembly import even_parity_weights, odd_parity_weights  # noqa: E402
from lr_su4_cp_parity_audit import (  # noqa: E402
    J,
    OMEGA,
    Coupling,
    candidate_couplings,
    chirality_is_forced_by_cp_even_dynamics,
    colour_parity,
    cp_conjugate,
    cp_flips_Pc_keeps_Pw,
    cp_maps_16_to_16bar,
    cp_swaps_sectors,
    sector,
    weak_parity,
)

ALLW = set(even_parity_weights()) | set(odd_parity_weights())


# ---- Layer 1: CP action on the tested bit structure ----------------------

def test_cp_is_involution_flipping_all_bits():
    for w in ALLW:
        assert cp_conjugate(cp_conjugate(w)) == w
        assert cp_conjugate(w) == tuple(-x for x in w)


def test_cp_bijects_16_onto_16bar():
    assert cp_maps_16_to_16bar()
    assert {cp_conjugate(w) for w in even_parity_weights()} == set(odd_parity_weights())


def test_cp_flips_colour_parity_keeps_weak_parity():
    """The crux: 3 colour bits ⇒ P_c CP-odd; 2 weak bits ⇒ P_w CP-even."""
    assert cp_flips_Pc_keeps_Pw()
    for w in ALLW:
        assert colour_parity(cp_conjugate(w)) == -colour_parity(w)
        assert weak_parity(cp_conjugate(w)) == +weak_parity(w)


def test_16_is_diagonal_16bar_is_antidiagonal():
    assert all(sector(w) == "diagonal" for w in even_parity_weights())
    assert all(sector(w) == "anti-diagonal" for w in odd_parity_weights())


def test_cp_swaps_diagonal_and_antidiagonal():
    assert cp_swaps_sectors()


# ---- Layer 2: parity of candidate couplings ------------------------------

def test_current_and_vorticity_parities():
    assert (J.C, J.P) == (-1, -1)              # C-odd polar vector
    assert (OMEGA.C, OMEGA.P) == (-1, +1)      # C-odd pseudovector


def test_natural_cross_term_is_cp_even_and_cannot_force():
    cross = Coupling("omega_c.omega_w", (OMEGA, OMEGA), "")
    assert cross.P == +1 and cross.C == +1 and cross.CP == +1
    assert not cross.can_force_chirality


def test_only_parity_odd_couplings_can_force_chirality():
    for c in candidate_couplings():
        assert c.can_force_chirality == (c.P == -1)
    # j_c . omega_w is the P-odd one that could force it (= the postulate)
    j_omega = Coupling("j_c.omega_w", (J, OMEGA), "")
    assert j_omega.P == -1 and j_omega.CP == -1 and j_omega.can_force_chirality


# ---- Verdict -------------------------------------------------------------

def test_chirality_not_forced_by_cp_even_dynamics():
    assert chirality_is_forced_by_cp_even_dynamics() is False

"""Regression tests for #80 Pass 6: the 16 as Pati-Salam, two demands = one structure."""

from fractions import Fraction

from cp1_logse_16_assembly import even_parity_weights, field_of
from pati_salam_16_unification import (
    chirality_lock_is_parity,
    full_32_irreps,
    pati_salam_decomposition,
    pati_salam_irrep,
    su4_b_minus_L_generator,
    su4_generator_is_traceless,
    su4_rep,
    weak_T3R,
    wrong_chirality_irreps,
)


def test_b_minus_L_is_su4_cartan_generator():
    g = su4_b_minus_L_generator()
    assert g == [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(-1)]
    assert su4_generator_is_traceless()          # traceless => valid SU(4) generator
    assert sum(g) == 0


def test_16_is_pati_salam_4_2_1_plus_4bar_1_2():
    assert pati_salam_decomposition() == {"(4,2,1)": 8, "(4bar,1,2)": 8}
    assert sum(pati_salam_decomposition().values()) == 16


def test_left_fields_in_4_right_fields_in_4bar():
    left = {"Q", "L"}
    right = {"u^c", "d^c", "e^c", "nu^c"}
    for w in even_parity_weights():
        if field_of(w) in left:
            assert su4_rep(w) == "4"
            assert pati_salam_irrep(w).endswith(",2,1)")     # SU(2)_L doublet
        elif field_of(w) in right:
            assert su4_rep(w) == "4bar"
            assert pati_salam_irrep(w).endswith(",1,2)")     # SU(2)_R doublet


def test_su2R_pairs_are_doublets():
    # u^c/d^c and nu^c/e^c carry T3_R = +/-1/2; left fields carry T3_R = 0
    for w in even_parity_weights():
        if field_of(w) in ("u^c", "d^c", "e^c", "nu^c"):
            assert abs(abs(weak_T3R(w)) - 0.5) < 1e-12
        else:
            assert abs(weak_T3R(w)) < 1e-12


def test_chirality_lock_equals_parity():
    # the central claim: demand (a) and demand (b) are ONE structure
    assert chirality_lock_is_parity()


def test_product_gives_32_connected_gives_16():
    assert full_32_irreps() == {
        "(4,2,1)": 8, "(4bar,1,2)": 8, "(4,1,2)": 8, "(4bar,2,1)": 8,
    }
    # the chirality lock drops exactly the two wrong-handed combos
    assert wrong_chirality_irreps() == {"(4,1,2)", "(4bar,2,1)"}

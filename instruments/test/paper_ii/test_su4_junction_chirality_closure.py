"""Regression tests for #80 Pass 7: SU(4) junction + the chirality-ZZ2 postulate."""

import itertools

from su4_junction_chirality_closure import (
    analyse_su4_junction,
    b_minus_L_in_cartan_span,
    balanced_phase_space_dimension_n,
    diagonal_selects_one_generation,
    index2_subgroups_of_z2xz2,
    permutations_form_s4,
    sector_parities,
    states_invariant_under,
    su4_cartan_generators,
    z2xz2_sector_contents,
)
from su3_y_junction import lie_closure


def test_four_leg_balance_has_rank_3():
    assert balanced_phase_space_dimension_n(4) == 3      # = rank SU(4)


def test_cartan_is_abelian_dim_3():
    assert lie_closure(su4_cartan_generators()) == 3     # u(1)^3, not su(4)=15


def test_b_minus_L_lives_in_the_cartan():
    assert b_minus_L_in_cartan_span()


def test_permutations_are_weyl_s4():
    assert permutations_form_s4()                        # order 24 = Weyl(SU(4))


def test_su4_junction_verdict_is_partial_with_bL():
    v = analyse_su4_junction()
    assert v.balanced_dim == 3
    assert v.generated_algebra_dim == 3
    assert v.bL_in_cartan
    assert v.weyl_is_s4 and v.weyl_order == 24
    assert v.verdict.startswith("PARTIAL")


def test_z2xz2_has_four_sectors_of_eight():
    contents = z2xz2_sector_contents()
    assert set(contents.values()) == {8}
    assert len(contents) == 4
    assert sum(contents.values()) == 32


def test_only_diagonal_quotient_gives_one_generation():
    gen = {"Q": 6, "u^c": 3, "d^c": 3, "L": 2, "e^c": 1, "nu^c": 1}
    results = {
        name: (states_invariant_under(sub) == gen)
        for name, sub in index2_subgroups_of_z2xz2().items()
    }
    # exactly one of the three ZZ2 quotients yields the SM generation
    assert sum(results.values()) == 1
    assert any("DIAGONAL" in name and ok for name, ok in results.items())


def test_diagonal_is_the_chirality_lock():
    assert diagonal_selects_one_generation()
    # the diagonal keeps P_c = P_w; verify directly on all 32
    kept = [w for w in itertools.product((+1, -1), repeat=5)
            if sector_parities(w) in {(+1, +1), (-1, -1)}]
    assert len(kept) == 16
    for w in kept:
        pc, pw = sector_parities(w)
        assert pc == pw

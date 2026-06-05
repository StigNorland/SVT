"""Regression tests for #79: SSV Y-junction phase-balance -> SU(3)? analysis."""

import numpy as np

from su3_y_junction import (
    analyse,
    balanced_phase_space_dimension,
    cartan_generators_from_balanced_phases,
    gell_mann,
    is_diagonal,
    lie_closure,
    permutation_matrices,
    permutations_act_as_weyl_on_cartan,
    permutations_form_s3,
)


def test_gell_mann_count_and_diagonal_split():
    gm = gell_mann()
    assert len(gm) == 8
    assert sum(is_diagonal(L) for L in gm) == 2          # lambda_3, lambda_8
    assert sum(not is_diagonal(L) for L in gm) == 6      # lambda_1,2,4,5,6,7


def test_gell_mann_are_traceless_hermitian():
    for L in gell_mann():
        assert np.allclose(L, L.conj().T)                # Hermitian
        assert abs(np.trace(L)) < 1e-12                  # traceless


def test_balanced_phase_space_is_rank_two():
    # three phases minus one balance constraint = 2 = rank SU(3)
    assert balanced_phase_space_dimension() == 2


def test_continuous_moves_generate_abelian_cartan_not_su3():
    cartan = cartan_generators_from_balanced_phases()
    assert len(cartan) == 2
    # the two Cartan generators commute (abelian)
    A, B = cartan
    assert np.allclose(A @ B - B @ A, 0.0)
    # the Lie algebra they generate has dimension 2, NOT 8
    assert lie_closure(cartan) == 2


def test_full_su3_closure_sanity():
    # control: the full Gell-Mann set does close to dim-8 su(3)
    assert lie_closure(gell_mann()) == 8


def test_permutations_form_weyl_s3():
    assert permutations_form_s3()
    assert len(permutation_matrices()) == 6
    assert permutations_act_as_weyl_on_cartan()


def test_cartan_generators_are_diagonal_traceless():
    for G in cartan_generators_from_balanced_phases():
        assert is_diagonal(G)
        assert abs(np.trace(G)) < 1e-12


def test_verdict_is_partial():
    v = analyse()
    assert v.balanced_dim == 2
    assert v.su3_dim == 8
    assert v.generated_algebra_dim == 2
    assert v.realised_gellmann_diagonal == 2
    assert v.missing_gellmann_offdiagonal == 6
    assert v.permutations_are_s3
    assert v.weyl_action_ok
    assert v.verdict.startswith("PARTIAL")

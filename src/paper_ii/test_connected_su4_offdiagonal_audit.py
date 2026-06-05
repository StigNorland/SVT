"""Tests for the connected-SU(4) cheap audit: the natural total-current chiral-shear
term is SU(4)-invariant (off-diagonal generators survive, lie_closure=15=connected),
while the per-colour sector form is Cartan-only (lie_closure=3=product)."""

import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_ii")
if p not in sys.path:
    sys.path.insert(0, p)

from su3_y_junction import lie_closure  # noqa: E402
from connected_su4_offdiagonal_audit import (  # noqa: E402
    _is_symmetry,
    all_su4_generators,
    b_minus_L_generator,
    cartan_generators,
    offdiagonal_generators,
    realised_symmetry_dim,
    sector_functional,
    total_current,
)


def test_generator_set_sizes():
    assert len(cartan_generators()) == 3
    assert len(offdiagonal_generators()) == 12
    assert len(all_su4_generators()) == 15


def test_generators_are_traceless_hermitian():
    for T in all_su4_generators():
        assert np.allclose(T, T.conj().T)          # Hermitian
        assert abs(np.trace(T)) < 1e-12            # traceless ⇒ su(4)


def test_lie_closure_reproduces_su4_and_junction_cartan():
    assert lie_closure(all_su4_generators()) == 15      # full su(4)
    assert lie_closure(cartan_generators()) == 3        # u(1)^3 = the #79/#80 answer


def test_total_current_is_fully_su4_invariant():
    """The natural generalisation of Im(ψ*∇ψ) is SU(4)-invariant under all 15."""
    for T in all_su4_generators():
        assert _is_symmetry(total_current, T)
    assert realised_symmetry_dim(total_current) == 15   # CONNECTED


def test_sector_current_is_cartan_only():
    """The per-colour form survives only the 3 Cartan (diagonal phase) generators."""
    cart = cartan_generators()
    for T in cart:
        assert _is_symmetry(sector_functional, T)
    for T in offdiagonal_generators():
        assert not _is_symmetry(sector_functional, T)
    assert realised_symmetry_dim(sector_functional) == 3    # PRODUCT


def test_b_minus_L_is_symmetry_of_both():
    """B−L is a Cartan element, realised in both pictures — consistent with #80."""
    bl = b_minus_L_generator()
    assert _is_symmetry(total_current, bl)
    assert _is_symmetry(sector_functional, bl)

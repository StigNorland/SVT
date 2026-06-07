"""Tests for #87 B3 — chirality ℤ₂ as the CP¹ spin framing.

Claims:
  - the spin Berry connection a and curvature b carry the same (C,P) as (j, ω);
  - the framing lock j_c·b_spin lands in the #81 P-odd/CP-odd slot (can force χ);
  - flipping the framing ℤ₂ reverses the selected sector;
  - the scalar theory has no P-odd carrier (so chirality was a postulate)."""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_ii")
if p not in sys.path:
    sys.path.insert(0, p)

from chirality_spin_framing_b3 import (  # noqa: E402
    A_SPIN,
    B_SPIN,
    chirality_lock_coupling,
    framing_flip_flips_selection,
    framing_helicity_coupling,
    issue81_required_coupling,
    lock_matches_issue81_slot,
    scalar_theory_has_no_carrier,
    spin_operands_match_current_operands,
)
from lr_su4_cp_parity_audit import J, OMEGA  # noqa: E402


def test_spin_operands_match_current_operands():
    assert spin_operands_match_current_operands()
    assert (A_SPIN.C, A_SPIN.P) == (J.C, J.P)
    assert (B_SPIN.C, B_SPIN.P) == (OMEGA.C, OMEGA.P)


def test_framing_helicity_is_parity_odd():
    """a·b is P-odd (CP-odd) — the intrinsic spinor handedness."""
    h = framing_helicity_coupling()
    assert h.P == -1 and h.CP == -1 and h.can_force_chirality


def test_lock_matches_issue81_required_slot():
    """j_c·b_spin has the same (C,P,CP) as the #81 j_c·ω_w slot and can force χ."""
    assert lock_matches_issue81_slot()
    lock, req = chirality_lock_coupling(), issue81_required_coupling()
    assert (lock.C, lock.P, lock.CP) == (req.C, req.P, req.CP) == (1, -1, -1)
    assert lock.can_force_chirality


def test_framing_z2_flip_selects_opposite_chirality():
    assert framing_flip_flips_selection()


def test_scalar_theory_needs_a_postulate():
    """No P-odd carrier in the scalar U(1) theory ⇒ chirality must be postulated."""
    assert scalar_theory_has_no_carrier()

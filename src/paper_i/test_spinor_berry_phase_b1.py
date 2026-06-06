"""Tests for #87 B1 — spinor BdG azimuthal holonomy.

Pre-registered claims (see spinor-berry-phase-b1.md):
  C1  chiral symmetry σ_z H σ_z = −H holds on the ring (ℤ₂-protecting symmetry);
  C2  the Berry phase is ℤ₂-quantised to {0, π} for every m (no continuous drift);
  C3  spin-orbit-locked regime |m|<1 ⇒ γ_B = π ⇒ rung offset ½ ⇒ muon = (3/2)μ₀;
  C4  scalar / unlocked regime |m|>1 ⇒ γ_B = 0 ⇒ integer ladder (reproduces #76);
  C5  the winding number tracks the regime (1 vs 0) and the gap closes only at
      |m| = 1 — so the 0↔π jump is a protected topological transition.
"""

import math
import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from spinor_berry_phase_b1 import (  # noqa: E402
    berry_phase,
    chiral_symmetry_residual,
    gap_min,
    rung_offset,
    scalar_limit_berry_phase,
    winding_number,
)

LOCKED = (0.0, 0.3, 0.6, 0.9)        # |m| < 1: spin-orbit lock wins
UNLOCKED = (1.1, 1.5, 3.0, 50.0)     # |m| > 1: anisotropy / scalar limit


def test_chiral_symmetry_holds():
    """C1 — σ_z H σ_z + H = 0 everywhere on the ring."""
    for m in LOCKED + UNLOCKED:
        assert chiral_symmetry_residual(m) < 1e-12


def test_berry_phase_is_z2_quantised():
    """C2 — γ_B ∈ {0, π} for every m (never an intermediate value)."""
    for m in np.linspace(-2.0, 2.0, 21):
        if abs(abs(m) - 1.0) < 1e-3:
            continue                     # skip the gap-closing point
        g = berry_phase(float(m))
        assert min(abs(g - 0.0), abs(g - math.pi)) < 1e-6


def test_locked_regime_gives_pi_and_muon_offset():
    """C3 — |m|<1 ⇒ γ_B = π and ladder offset ½ (muon = 3/2 rung)."""
    for m in LOCKED:
        assert abs(berry_phase(m) - math.pi) < 1e-6
        assert abs(rung_offset(m) - 0.5) < 1e-6


def test_unlocked_regime_gives_zero_integer_ladder():
    """C4 — |m|>1 ⇒ γ_B = 0 (integer ladder; the #76 scalar sector)."""
    for m in UNLOCKED:
        assert berry_phase(m) < 1e-6
        assert rung_offset(m) < 1e-6


def test_scalar_limit_reproduces_issue76_null():
    """C4 — the m→∞ (no internal spin) limit gives γ_B = 0, the #76 result."""
    assert scalar_limit_berry_phase() < 1e-6


def test_winding_and_gap_track_the_transition():
    """C5 — winding = 1 (locked) / 0 (unlocked); gap closes only near |m|=1."""
    for m in LOCKED:
        assert winding_number(m) == 1
    for m in UNLOCKED:
        assert winding_number(m) == 0
    # gap is large away from the transition, small as |m|→1
    assert gap_min(0.0) > 1.5
    assert gap_min(3.0) > 1.5
    assert gap_min(0.95) < 0.2


def test_protection_robust_within_a_phase():
    """C3/C5 — γ_B = π is stable across the whole locked phase (not fine-tuned):
    every |m|<1 gives exactly π, so it cannot be a tuned/continuous coincidence."""
    phases = [berry_phase(m) for m in (0.0, 0.1, 0.4, 0.7, 0.95)]
    assert all(abs(g - math.pi) < 1e-6 for g in phases)

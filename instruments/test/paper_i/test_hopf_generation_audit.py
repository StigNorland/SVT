"""Tests for #115 Gate 1 + Gate 3 (first pass) — CP¹ Hopf-charge sectors as
candidate lepton generations.

These guard the three findings of the opening pass:
  G1a  the A_{n,m} ansätze realise three DISTINCT, correctly quantised Hopf
       sectors: H ratios 1 : 2 : 3 (normalisation-free claim).
  G1b  the spin texture n̂ = z†σz is invariant under z ↦ e^{iθ}z, so electric
       charge (the U(1) winding) is orthogonal to Hopf charge.
  G3   the canonical (Faddeev–Niemi) energy is decisively too FLAT for the
       generation mass hierarchy: E(Q2)/E(Q1) ≪ m_μ/m_e = 206.8.  This is a
       negative-result guard — if a future change makes the baseline functional
       suddenly look steep enough, that is a bug, not a discovery.
"""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from hopf_generation_audit import (  # noqa: E402
    run_hopf_charge,
    electric_charge_orthogonality,
    summary,
)

# A coarser grid keeps the suite fast while staying well inside the integer bands.
GRID_N = 64
HALF = 8.0


def test_g1a_hopf_sectors_quantised():
    """H magnitudes ≈ 1, 2, 3 and ratios ≈ 1, 2, 3 (sign is orientation)."""
    rows = [run_hopf_charge(n, m, GRID_N, HALF) for (n, m) in [(1, 1), (2, 1), (3, 1)]]
    H = [r["H"] for r in rows]
    for h, q in zip(H, (1, 2, 3)):
        assert abs(abs(h) - q) < 0.05 * q, f"|H|={abs(h):.3f} not ≈ {q}"
    ratios = [h / H[0] for h in H]
    assert abs(ratios[1] - 2.0) < 0.05
    assert abs(ratios[2] - 3.0) < 0.05


def test_g1b_electric_charge_orthogonal_to_hopf():
    """n̂ = z†σz is invariant under a U(1) phase ⇒ electric charge is preserved
    when Hopf charge is stacked."""
    assert electric_charge_orthogonality() < 1e-12


def test_g3_energy_far_too_flat_for_hierarchy():
    """Canonical hopfion energetics give an O(1) step, not the ×207 / ×17 the
    masses demand.  Pre-registered FAIL of the baseline functional."""
    s = summary(GRID_N, HALF)
    # The first step is short by more than two orders of magnitude.
    assert s["E_ratio_2_1"] < 5.0, s["E_ratio_2_1"]
    assert s["E_ratio_2_1"] < 0.05 * s["required_mu_over_e"]
    # Sanity: the energy does at least increase with Q (not collapsing).
    assert s["Etot"][2] > s["Etot"][1] > s["Etot"][0]


def test_g3_chiral_shear_is_skyrme_and_also_too_flat():
    """SSV chiral-shear |∇×j|² on a bare texture (j ∝ a) IS the Skyrme structure
    (∫|∇×a|²/E4 Q-independent) and scales just as flatly — closing the
    'maybe chiral-shear is steeper than Faddeev–Niemi' escape hatch."""
    s = summary(GRID_N, HALF)
    cr = s["chi_over_E4"]
    # Ratio ≈ ¼ and roughly Q-independent ⇒ same structure as the Skyrme term.
    # (Spread is grid-limited: ~7% at N=64, ~1% at N=96; the structural point is
    # that it is a single O(1) constant, not a Q-growing factor.)
    mean = sum(cr) / len(cr)
    assert 0.2 < mean < 0.3, cr
    assert max(cr) - min(cr) < 0.15 * mean, cr
    # And therefore equally too flat: e→μ step ≪ 207.
    assert s["Echi_ratio_2_1"] < 5.0, s["Echi_ratio_2_1"]
    assert s["Echi_ratio_2_1"] < 0.05 * s["required_mu_over_e"]

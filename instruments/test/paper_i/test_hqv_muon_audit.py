"""Tests for #94 — HQV electron does NOT rescue the muon γ_B=π.

Pre-registered claims (plan on #94):
  C1  meridional holonomy C_ϑ (links core) = π — the electron's spin-½ (#87 B2)
  C2  azimuthal holonomy C_φ (along core) = 0 — muon NOT rescued (= #91)
  C3  free HQV has half charge ⇒ excluded by charge quantization
  C4  forcing azimuthal spin winding costs positive energy (no benefit)
  C5  IQV and 2-HQV are degenerate at leading log (no drive to split)
  C6  verdict: electron = IQV; muon = coincidence (final); pion = 2μ₀ survives
"""

import math
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from hqv_muon_audit import (  # noqa: E402
    azimuthal_berry_phase,
    azimuthal_spin_winding_cost,
    free_defect_charge,
    hqv_free_charge_excluded,
    iqv_vs_2hqv_leading_log,
    meridional_berry_phase,
    verdict,
)


def test_meridional_holonomy_is_pi():
    """C1 — the HQV disclination links the core → spin-½ ℤ₂ phase π."""
    assert abs(meridional_berry_phase() - math.pi) < 1e-6


def test_azimuthal_holonomy_is_zero():
    """C2 — z is φ-independent → A_φ=0 → muon γ_B=0 (reproduces #91)."""
    assert azimuthal_berry_phase() < 1e-6


def test_two_circles_differ():
    """The decisive point: the two holonomies live on orthogonal circles."""
    assert abs(meridional_berry_phase() - math.pi) < 1e-6
    assert azimuthal_berry_phase() < 1e-6


def test_free_hqv_charge_excluded():
    """C3 — free HQV has half charge (non-integer) ⇒ excluded."""
    assert free_defect_charge(0.5) == 0.5
    assert hqv_free_charge_excluded()


def test_iqv_unit_charge_allowed():
    """An IQV (n=1) has integer charge — the allowed free object."""
    q = free_defect_charge(1.0)
    assert abs(q - round(q)) < 1e-9


def test_azimuthal_winding_costs_energy():
    """C4 — forcing a major-ring spin winding costs positive energy, no benefit."""
    cost = azimuthal_spin_winding_cost(spin_stiffness=1.0, R=137.0)
    assert cost > 0.0
    # cost falls as 1/R (large rings cheaper) but never zero/negative
    assert azimuthal_spin_winding_cost(1.0, 274.0) < cost


def test_iqv_2hqv_degenerate_at_leading_log():
    """C5 — equal phase/spin stiffness ⇒ no energetic drive to split into HQVs."""
    ll = iqv_vs_2hqv_leading_log(R=137.0, xi=1.0)
    assert abs(ll["E_IQV"] - ll["E_2HQV_leading"]) < 1e-9


def test_verdict():
    """C6 — assembled verdict: HQV rejected, muon coincidence, pion survives."""
    r = verdict()
    assert abs(r["meridional_gamma_B_over_pi"] - 1.0) < 1e-6
    assert r["azimuthal_gamma_B_over_pi"] < 1e-6
    assert r["hqv_free_excluded"]
    assert r["electron_is_IQV"]
    assert "COINCIDENCE" in r["muon_status"]
    assert "survives" in r["pion_2mu0"]

"""Tests for #95 — SSV mass-sector parameter count.

Claims:
  C1  μ₀ = m_e/α
  C2  each particle mass = (pure topological number) · μ₀
  C3  every mass ratio m_X/m_e depends only on α and topology (no vacuum params)
  C4  ρ₀ is fixed by the m_e normalisation (not independent); m₀ cancels from ratios
  C5  the R_e relation defines γ(α) ⇒ α is not predicted (irreducible)
  C6  exactly 2 irreducible inputs (m_e, α)
"""

import sys
from pathlib import Path

import sympy as sp

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from mass_sector_parameter_count import (  # noqa: E402
    alpha,
    alpha_is_predicted,
    F,
    gamma_of_alpha,
    irreducible_inputs,
    m0_cancels_from_ratios,
    mass_ratio_to_electron,
    mu0,
    m_e,
    n_irreducible_inputs,
    particle_mass,
    ratio_depends_only_on_alpha_and_topology,
    rho0_fixed_by_me,
)


def test_mu0_is_me_over_alpha():
    assert sp.simplify(mu0() - m_e / alpha) == 0


def test_particle_masses_are_number_times_mu0():
    assert sp.simplify(particle_mass("pion") - 2 * mu0()) == 0
    assert sp.simplify(particle_mass("muon") - sp.Rational(3, 2) * mu0()) == 0
    assert sp.simplify(particle_mass("proton") - 3 * F * mu0()) == 0


def test_mass_ratios_are_parameter_free():
    """C3 — m_X/m_e depends only on α (and F for the proton), no vacuum params."""
    assert sp.simplify(mass_ratio_to_electron("pion") - 2 / alpha) == 0
    assert sp.simplify(mass_ratio_to_electron("muon") - sp.Rational(3, 2) / alpha) == 0
    assert sp.simplify(mass_ratio_to_electron("proton") - 3 * F / alpha) == 0
    for name in ("pion", "muon", "proton"):
        assert ratio_depends_only_on_alpha_and_topology(name)


def test_rho0_fixed_and_m0_cancels():
    """C4 — ρ₀ is determined by the m_e normalisation; m₀ cancels from ratios."""
    rho0_expr = rho0_fixed_by_me()
    assert m_e in rho0_expr.free_symbols and alpha in rho0_expr.free_symbols
    assert m0_cancels_from_ratios()


def test_alpha_not_predicted():
    """C5 — γ depends on α (the relation defines γ(α)) ⇒ α is not predicted."""
    assert alpha in gamma_of_alpha().free_symbols
    assert alpha_is_predicted() is False


def test_two_irreducible_inputs():
    assert n_irreducible_inputs() == 2
    joined = " ".join(irreducible_inputs()).lower()
    assert "m_e" in joined and "alpha" in joined

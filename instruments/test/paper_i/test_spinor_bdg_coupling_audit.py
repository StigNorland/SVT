"""Tests for #91 — spinor BdG winding-regime audit.

Pre-registered claims from the plan posted on #91:
  T1  δj from z₀_⊥ channel = 0 for constant z₀ (z₀†z₀_⊥ = 0 kills every term)
  T2  Fourier bridge IQV = 0 (φ-independent kernel → Fourier orthogonality)
  T3  Fourier bridge HQV ≠ 0 (e^{iφ} kernel → nonzero, confirms test sensitivity)
  T4  Numerical IQV bridge ≈ 0 to quadrature precision
  T5  Numerical HQV bridge ≈ 1 (normalised)
  T6  Pre-registered verdict: CLEAN NO, |V|=0, |m|→∞, γ_B=0, muon=NUMERICAL COINCIDENCE
"""

import sys
import math
from pathlib import Path

import sympy as sp

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from spinor_bdg_coupling_audit import (  # noqa: E402
    current_variation_from_perp_channel,
    fourier_bridge_integral_iqv,
    fourier_bridge_integral_hqv,
    hqv_mode_periodicity,
    iqv_verdict,
    numerical_bridge_hqv,
    numerical_bridge_iqv,
)


def test_delta_j_from_perp_channel_is_zero():
    """T1 — δj from z₀_⊥ channel vanishes exactly by z₀†z₀_⊥ = 0."""
    assert current_variation_from_perp_channel() == 0


def test_fourier_bridge_iqv_is_zero():
    """T2 — the IQV bridge integral vanishes by Fourier orthogonality."""
    assert fourier_bridge_integral_iqv() == 0


def test_fourier_bridge_hqv_is_nonzero():
    """T3 — HQV control: e^{iφ} kernel gives ∫e^{-iφ}·e^{iφ} dφ = 2πV ≠ 0."""
    result = fourier_bridge_integral_hqv()
    V = sp.Symbol("V_rz")
    assert sp.simplify(result - 2 * sp.pi * V) == 0


def test_numerical_bridge_iqv_is_zero():
    """T4 — numerical quadrature: IQV bridge ≈ 0 to 1e-3 (trapezoid)."""
    assert numerical_bridge_iqv() < 1e-3


def test_numerical_bridge_hqv_is_unity():
    """T5 — numerical quadrature: HQV control bridge ≈ 1 to 1e-3."""
    assert abs(numerical_bridge_hqv() - 1.0) < 1e-3


def test_iqv_verdict_clean_no():
    """T6 — the pre-registered decision rule gives CLEAN NO for IQV."""
    r = iqv_verdict()
    assert r["V_magnitude_iqv"] == 0.0
    assert r["m_parameter"] == float("inf")
    assert r["gamma_B"] == 0.0
    assert r["verdict"] == "CLEAN NO"
    assert "NUMERICAL COINCIDENCE" in r["muon_status"]


def test_hqv_mechanism_is_topology_not_matrix_element():
    """HQV gives γ_B=π from half-integer effective quantum number, not from |V|."""
    h = hqv_mode_periodicity()
    assert "half-integer" in h["effective_quantum_number"]
    assert "NO spin-orbit matrix element" in h["mechanism"]
    assert "π" in h["berry_phase"]

"""Tests for #87 Part A — the CP¹/spinor decomposition identities that
underwrite the safety notes (pion=2μ₀, α/R_e/Madelung, Goldstone decoupling).

Each numeric residual must vanish to machine precision; the O(ε) Berry-phase
coupling must vanish identically (symbolic)."""

import sys
from pathlib import Path

import sympy as sp

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from cp1_safety_checks import (  # noqa: E402
    all_residuals,
    berry_connection_closed_form,
    linear_decoupling_coefficient,
    residual_berry_real,
    residual_grad_decomposition,
    residual_mermin_ho,
    residual_uniform_n_current,
    residual_uniform_n_energy,
    _max_abs_residual,
)

TOL = 1e-9


def test_berry_connection_is_real():
    """(I1) a = −i z†∂z is real for z†z = 1."""
    assert _max_abs_residual(residual_berry_real()) < TOL


def test_berry_closed_form():
    """a = cos²(β/2)γ₁' + sin²(β/2)γ₂' — the standard CP¹ connection."""
    x = sp.symbols("x", real=True)
    beta = sp.Function("beta", real=True)(x)
    g1 = sp.Function("gamma1", real=True)(x)
    g2 = sp.Function("gamma2", real=True)(x)
    expected = sp.cos(beta / 2) ** 2 * g1.diff(x) + sp.sin(beta / 2) ** 2 * g2.diff(x)
    assert sp.simplify(berry_connection_closed_form() - expected) == 0


def test_energy_decomposition():
    """(I2) |∂Ψ|² = (∂A)² + A²(∂θ)² + A²|∂z|² + 2A²(∂θ)a."""
    assert _max_abs_residual(residual_grad_decomposition()) < TOL


def test_mermin_ho_current():
    """(I3) Im(Ψ†∂Ψ) = A²(∂θ + a)."""
    assert _max_abs_residual(residual_mermin_ho()) < TOL


def test_uniform_n_reduces_to_scalar_energy():
    """(I2′) constant spinor ⇒ scalar LogSE energy density exactly."""
    assert _max_abs_residual(residual_uniform_n_energy()) < TOL


def test_uniform_n_reduces_to_scalar_current():
    """(I3′) constant spinor ⇒ scalar current exactly (a=0 ⇒ j unchanged)."""
    assert _max_abs_residual(residual_uniform_n_current()) < TOL


def test_spin_waves_decouple_at_linear_order():
    """(I4) transverse δz about constant z₀ gives a = O(ε²): no linear spin↔EM
    coupling — the load-bearing fact for A3 Goldstone safety."""
    assert linear_decoupling_coefficient() == 0


def test_all_residuals_machine_zero():
    for label, val in all_residuals().items():
        assert val < TOL, f"{label} residual too large: {val}"

"""#87 Part A — symbolic safety checks for the CP¹/spinor extension of SSV.

Issue #83 promotes the scalar order parameter Ψ to a two-component spinor
    Ψ_a = √(ρ/ρ₀) · e^{iθ} · z_a ,   z = (z₁, z₂),  z†z = 1,
i.e. an overall amplitude A = √(ρ/ρ₀), an overall U(1) phase θ, and an internal
CP¹ direction z (the new spin texture; n̂ = z†σz ∈ S²).  Every Part-A safety
result (pion = 2μ₀, α = c⊥/c, R_e = ξ/α, Madelung, Goldstone safety) rests on a
single algebraic question: how do the LogSE energy density |∇Ψ|² and the
probability current j = (ħ/2m₀i)(Ψ†∇Ψ − ∇Ψ†Ψ) decompose under this map, and
what survives when the spin texture is trivial?

This module derives the decomposition (one spatial coordinate x, which is all
the gradient algebra needs) and verifies four load-bearing identities used by
the analytic notes in papers/SSV-I/results/spinor/ :

  (I1)  Berry connection a ≡ −i z†z' is REAL  (since z†z = 1).
  (I2)  |∇Ψ|²  =  (∂A)² + A²(∂θ)² + A²|∂z|² + 2 A²(∂θ) a
              =  (ρ/ρ₀)[ ¼(∂ lnρ)² + (∂θ)² + |∂z|² + 2 a ∂θ ].
        The first two terms are the scalar result; the last two are the only
        new pieces and BOTH vanish when z is constant (uniform n̂).
  (I3)  Mermin–Ho: Im(Ψ†∂Ψ) = A²(∂θ + a), so j = (ħ/m₀)(ρ/ρ₀)(∇θ + a).
        At a = 0 (uniform n̂) j is exactly the scalar current ⇒ |∇×j|² (the
        chiral-shear / EM sector) is unchanged on uniform-n̂ configurations.
  (I4)  Decoupling: expanding z = z₀ + ε·δz about a CONSTANT z₀ with z₀†δz = 0
        (the physical transverse spin fluctuation), the Berry connection has NO
        O(ε) part: a = O(ε²).  Hence the spin waves do not couple to the
        density/phase (sound) channel or to ∇×j (photon) at linear order.

Verification strategy.  These are analytic identities that are polynomial in
the fields and their first derivatives, so substituting GENERIC analytic test
functions for (A, θ, β, γ₁, γ₂) and confirming every residual vanishes to
machine precision at several sample points is conclusive (a nonzero polynomial
identity cannot vanish on a generic curve).  This avoids sympy's slow/looping
``simplify`` on e^{iθ}·(complex Function) products while remaining rigorous.
The Bloch-angle Berry connection (I1) is shown in closed form for the record.
"""

from __future__ import annotations

import sympy as sp

x = sp.symbols("x", real=True)


# --------------------------------------------------------------------------
# Field builders.  A spinor z(x) in Bloch angles satisfies z†z = 1 identically.
# --------------------------------------------------------------------------

def spinor_from_angles(beta, g1, g2) -> sp.Matrix:
    """z = (cos(β/2) e^{iγ₁}, sin(β/2) e^{iγ₂}); z†z = 1 by construction."""
    return sp.Matrix([sp.cos(beta / 2) * sp.exp(sp.I * g1),
                      sp.sin(beta / 2) * sp.exp(sp.I * g2)])


def _dag(v: sp.Matrix) -> sp.Matrix:
    return v.conjugate().T


def berry_connection(z: sp.Matrix) -> sp.Expr:
    """a = −i z†∂_x z (a scalar expression in x)."""
    return (-sp.I * (_dag(z) * z.diff(x)))[0, 0]


def psi(A, theta, z) -> sp.Matrix:
    """Ψ_a = A e^{iθ} z_a."""
    return A * sp.exp(sp.I * theta) * z


def grad_sq(Psi: sp.Matrix) -> sp.Expr:
    """|∂_x Ψ|² = Σ_a |∂_x Ψ_a|²  (real)."""
    d = Psi.diff(x)
    return (_dag(d) * d)[0, 0]


def im_current(Psi: sp.Matrix) -> sp.Expr:
    """Im(Ψ†∂_x Ψ) computed as (w − w̄)/(2i); j_phys = (ħ/m₀)·this."""
    w = (_dag(Psi) * Psi.diff(x))[0, 0]
    return (w - sp.conjugate(w)) / (2 * sp.I)


# --------------------------------------------------------------------------
# Bloch closed form for the Berry connection (light enough to simplify).
# --------------------------------------------------------------------------

def berry_connection_closed_form() -> sp.Expr:
    """a in Bloch angles: a = cos²(β/2) γ₁' + sin²(β/2) γ₂'."""
    beta = sp.Function("beta", real=True)(x)
    g1 = sp.Function("gamma1", real=True)(x)
    g2 = sp.Function("gamma2", real=True)(x)
    z = spinor_from_angles(beta, g1, g2)
    return sp.simplify(berry_connection(z))


# --------------------------------------------------------------------------
# Generic analytic test fields and numeric residual evaluation.
# --------------------------------------------------------------------------

def _test_fields():
    """Generic, non-degenerate analytic fields for (A>0, θ, β, γ₁, γ₂)."""
    A = sp.exp(-(x**2) / 4) + sp.Rational(3, 4)        # > 0 everywhere
    theta = sp.sin(x) + x / 3
    beta = x**2 / 3 + sp.Rational(1, 5)
    g1 = sp.cos(x)
    g2 = x / 2 - sp.sin(2 * x)
    return A, theta, beta, g1, g2


def _max_abs_residual(expr: sp.Expr, samples=(-1.3, -0.4, 0.7, 1.9, 2.5)) -> float:
    """Largest |expr| over sample x values (real + imag parts)."""
    worst = 0.0
    for x0 in samples:
        v = complex(expr.subs(x, sp.Float(x0)).evalf())
        worst = max(worst, abs(v))
    return worst


def residual_grad_decomposition() -> sp.Expr:
    """(I2) |∂Ψ|² − [ (∂A)² + A²(∂θ)² + A²|∂z|² + 2A²(∂θ)a ]."""
    A, theta, beta, g1, g2 = _test_fields()
    z = spinor_from_angles(beta, g1, g2)
    Psi = psi(A, theta, z)
    a = berry_connection(z)
    dz = z.diff(x)
    grad_z_sq = (_dag(dz) * dz)[0, 0]
    rhs = A.diff(x) ** 2 + A**2 * theta.diff(x) ** 2 \
        + A**2 * grad_z_sq + 2 * A**2 * theta.diff(x) * a
    return grad_sq(Psi) - rhs


def residual_mermin_ho() -> sp.Expr:
    """(I3) Im(Ψ†∂Ψ) − A²(∂θ + a)."""
    A, theta, beta, g1, g2 = _test_fields()
    z = spinor_from_angles(beta, g1, g2)
    Psi = psi(A, theta, z)
    a = berry_connection(z)
    return im_current(Psi) - A**2 * (theta.diff(x) + a)


def residual_berry_real() -> sp.Expr:
    """(I1) a − ā."""
    _, _, beta, g1, g2 = _test_fields()
    a = berry_connection(spinor_from_angles(beta, g1, g2))
    return a - sp.conjugate(a)


def residual_uniform_n_energy() -> sp.Expr:
    """(I2′) at ∂z = 0: |∂Ψ|² − [(∂A)² + A²(∂θ)²] (scalar LogSE density)."""
    A, theta, beta, g1, g2 = _test_fields()
    z = spinor_from_angles(beta, g1, g2).subs(x, sp.Integer(0))  # constant spinor
    Psi = A * sp.exp(sp.I * theta) * z
    return grad_sq(Psi) - (A.diff(x) ** 2 + A**2 * theta.diff(x) ** 2)


def residual_uniform_n_current() -> sp.Expr:
    """(I3′) at ∂z = 0: Im(Ψ†∂Ψ) − A²∂θ (scalar current)."""
    A, theta, beta, g1, g2 = _test_fields()
    z = spinor_from_angles(beta, g1, g2).subs(x, sp.Integer(0))
    Psi = A * sp.exp(sp.I * theta) * z
    return im_current(Psi) - A**2 * theta.diff(x)


def linear_decoupling_coefficient() -> sp.Expr:
    """(I4) d a/dε at ε=0 for z = (1,0) + ε(0,w(x)); must be identically 0."""
    eps = sp.symbols("epsilon", real=True)
    w = sp.Function("w")(x)
    z = sp.Matrix([sp.Integer(1), sp.Integer(0)]) + eps * sp.Matrix([sp.Integer(0), w])
    a = (-sp.I * (_dag(z) * z.diff(x)))[0, 0]
    return sp.simplify(sp.diff(a, eps).subs(eps, 0))


def all_residuals() -> dict[str, float]:
    """Max |residual| for the numerically-checked identities (should be ~0)."""
    return {
        "(I1) a real": _max_abs_residual(residual_berry_real()),
        "(I2) energy decomposition": _max_abs_residual(residual_grad_decomposition()),
        "(I3) Mermin-Ho current": _max_abs_residual(residual_mermin_ho()),
        "(I2') uniform-n energy -> scalar": _max_abs_residual(residual_uniform_n_energy()),
        "(I3') uniform-n current -> scalar": _max_abs_residual(residual_uniform_n_current()),
    }


def main() -> None:
    print("=" * 74)
    print("#87 Part A — CP¹/spinor decomposition: safety identities")
    print("=" * 74)
    print("  Ψ_a = √(ρ/ρ₀) e^{iθ} z_a ,  z†z = 1 ,  a ≡ −i z†∂z (Berry connection)")
    print()
    print("  Closed form  a = cos²(β/2) γ₁' + sin²(β/2) γ₂'  (real):")
    sp.pprint(berry_connection_closed_form())
    print()

    res = all_residuals()
    allzero = True
    for label, val in res.items():
        ok = val < 1e-9
        allzero &= ok
        print(f"  {'OK ' if ok else 'FAIL'}  max|residual| {label:34s} = {val:.2e}")

    lin = linear_decoupling_coefficient()
    ok4 = lin == 0
    allzero &= ok4
    print(f"  {'OK ' if ok4 else 'FAIL'}  (I4) O(ε) Berry coupling (decoupling)      = {lin}")
    print()
    print("=" * 74)
    if allzero:
        print("ALL IDENTITIES HOLD.  Consequences:")
        print("  • Uniform n̂ ⇒ energy density AND current are EXACTLY the scalar")
        print("    ones ⇒ pion=2μ₀ (A1) and c_s, ξ, α, R_e (A2) are untouched.")
        print("  • The only new terms (A²|∂z|², 2A²(∂θ)a) vanish at ∇z=0 and, by")
        print("    (I4), have no O(ε) coupling to the sound/EM channels ⇒ the 2")
        print("    spin-wave modes decouple from sound and photon at linear order (A3).")
    else:
        print("AT LEAST ONE IDENTITY FAILED — the decomposition claim is wrong.")
    print("=" * 74)


if __name__ == "__main__":
    main()

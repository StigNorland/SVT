"""#189 E1/E2 -- the Gausson under both sign conventions, done symbolically.

SSV-VII-a's section "Saturation by the Gausson" rested on two claims:

  (a) the LogSE admits an exact Gaussian stationary state, the BBM Gausson,
      of width sigma^2 = hbar^2/(2 m b);
  (b) evaluating Dx*Dp on that state *derives* the hbar/2 prefactor "directly
      from the LogSE itself, without importing it from the standard
      wave-packet calculation".

The #182 audit found both defective, and the owner recorded the resolution as
prose on issue #189. This module turns that prose into a computation, so the
negative result is checkable rather than trusted.

  E1  Substituting the Gaussian ansatz into the LogSE and requiring the x^2
      terms to cancel fixes sigma^2 = -hbar^2/(2 m s b), where s = -1 for the
      `- b Psi ln` convention SSV-VII-a prints and s = +1 for the `+ b ln`
      convention SSV-I adopted (and SSV-II, SSV-IV, SSV-V print).

        s = -1, b > 0 :  sigma^2 > 0  -- the Gausson exists (VII-a's own eq)
        s = +1, b > 0 :  sigma^2 < 0  -- NO normalisable Gaussian exists

      The Gausson is a solution of the branch SSV-I (#183) rejected, because
      that branch makes the uniform vacuum modulationally unstable and cannot
      support c_s = c.

  E2  Dx*Dp = hbar/2 for ANY normalised Gaussian, of any width, with b
      appearing nowhere in the calculation. The width-independence VII-a
      offered as evidence that the result is robust is instead the tell that
      the LogSE contributed nothing: it is a property of Gaussians.

      `laplace_uncertainty_product` is the negative control. Without it, E2
      shows only that Gaussians give hbar/2, not that being Gaussian is what
      does the work -- and a check that cannot fail is not a check (FM3).

Run:  python instruments/paper_vii_a/logse_gaussian.py
"""

from __future__ import annotations

import sympy as sp

# ---------------------------------------------------------------- symbols
x, t = sp.symbols("x t", real=True)
sigma = sp.symbols("sigma", positive=True)      # a WIDTH: positive by definition
m, hbar, b = sp.symbols("m hbar b", positive=True)
rho0, E = sp.symbols("rho_0 E", positive=True)
lam = sp.symbols("lambda", positive=True)

#: Sign of the logarithmic term as each paper prints it, in
#:     i hbar d_t Psi = -hbar^2/(2m) d_x^2 Psi + s * b * Psi * ln(|Psi|^2/rho_0)
#: SSV-VII-a line 321 prints `- b\,\Psi\,\ln`; SSV-I line 272, SSV-II 2667,
#: SSV-IV 1409 and SSV-V 637 all print `+b\ln`.  One grep over the series is
#: the whole of #189, which is why it is generalised as #205.
CONVENTIONS = {"vii_a_minus": -1, "adopted_plus": +1}


def gausson_width_squared(convention: str):
    """sigma^2 forced by requiring a Gaussian to solve the LogSE.

    The substitution is done with the logarithm expanded by hand --
    ln(A^2 exp(-x^2/sigma^2)/rho_0) = ln(A^2/rho_0) - x^2/sigma^2 -- because
    sympy raises PolynomialError trying to collect powers out of a log of an
    exponential.  Expanding it is exact, not an approximation.
    """
    s = CONVENTIONS[convention]
    amp2 = 1 / sp.sqrt(sp.pi * sigma**2)             # |A|^2 for a normalised Gaussian
    profile = sp.exp(-x**2 / (2 * sigma**2))

    # i hbar d_t Psi = E Psi for Psi = psi(x) exp(-i E t / hbar), so the
    # stationary equation is  E psi = -hbar^2/(2m) psi'' + s b psi ln(|psi|^2/rho_0)
    kinetic = -hbar**2 / (2 * m) * sp.diff(profile, x, 2) / profile
    log_term = s * b * (sp.log(amp2 / rho0) - x**2 / sigma**2)
    residual = sp.expand(kinetic + log_term - E)

    # E is a constant, so every x^2 term must cancel.  That single condition
    # fixes sigma^2; the x^0 part merely fixes E and is not used.
    coeff_x2 = sp.simplify(sp.expand(residual).coeff(x, 2))
    solutions = sp.solve(sp.Eq(coeff_x2, 0), sigma**2, dict=True)
    if not solutions:
        raise ValueError(f"{convention}: no sigma^2 satisfies the x^2 balance")
    return sp.simplify(solutions[0][sigma**2])


def gausson_width_squared_unconstrained(convention: str):
    """The same result with sigma carrying no positivity assumption.

    ``sigma`` above is declared positive, which is right for a width but means
    sympy could in principle discard a negative root before it is seen.  This
    repeats the solve on a plain symbol so that E1's negative conclusion cannot
    be an artefact of the assumption used to state it.
    """
    s = CONVENTIONS[convention]
    w = sp.symbols("w", nonzero=True)            # w = sigma^2, sign unknown
    # d^2/dx^2 exp(-x^2/(2w)) / exp(...) = x^2/w^2 - 1/w
    kinetic = -hbar**2 / (2 * m) * (x**2 / w**2 - 1 / w)
    log_term = s * b * (sp.log(1 / sp.sqrt(sp.pi * w) / rho0) - x**2 / w)
    coeff_x2 = sp.simplify(sp.expand(kinetic + log_term - E).coeff(x, 2))
    return sp.simplify(sp.solve(sp.Eq(coeff_x2, 0), w, dict=True)[0][w])


def gaussian_exists(convention: str, b_positive: bool = True) -> bool:
    """Is the width real, i.e. does a normalisable Gaussian exist?"""
    w = gausson_width_squared_unconstrained(convention)
    value = w.subs({hbar: 1, m: 1, b: 1 if b_positive else -1})
    return bool(sp.simplify(value) > 0)


def zloshchastiev_length_squared():
    """a^2 = hbar^2/(2 m |b|), the LogSE's single length scale."""
    return hbar**2 / (2 * m * sp.Abs(b))


def uncertainty_product(width=None):
    """Dx*Dp for an arbitrary normalised Gaussian.  No b anywhere.

    This is E2: the calculation VII-a performs, done with the width left free
    and the LogSE nowhere in sight.  If the answer still comes out hbar/2 then
    the LogSE contributed nothing to it.
    """
    w = sigma if width is None else width
    psi = (sp.pi * w**2) ** sp.Rational(-1, 4) * sp.exp(-x**2 / (2 * w**2))
    norm = sp.integrate(psi**2, (x, -sp.oo, sp.oo))
    dx2 = sp.simplify(sp.integrate(x**2 * psi**2, (x, -sp.oo, sp.oo)) / norm)
    dp2 = sp.simplify(
        sp.integrate((hbar * sp.diff(psi, x))**2, (x, -sp.oo, sp.oo)) / norm)
    return sp.simplify(sp.sqrt(dx2 * dp2))


def laplace_uncertainty_product():
    """The negative control: a normalised NON-Gaussian state.

    psi ~ exp(-|x|/lambda) is normalisable with finite Dx and Dp.  If this also
    returned hbar/2, E2's conclusion would be empty -- saturation would be a
    property of every state rather than of Gaussians, and the test would be
    measuring nothing.
    """
    psi = sp.exp(-sp.Abs(x) / lam)
    norm = sp.integrate(psi**2, (x, -sp.oo, sp.oo))
    dx2 = sp.simplify(sp.integrate(x**2 * psi**2, (x, -sp.oo, sp.oo)) / norm)
    # d/dx exp(-|x|/lam) = -sign(x)/lam * psi, and sign(x)^2 = 1 away from 0
    dp2 = sp.simplify(hbar**2 / lam**2)
    return sp.simplify(sp.sqrt(dx2 * dp2))


def report() -> str:
    lines = ["#189 E1/E2 -- LogSE Gaussian, both conventions", ""]
    for name, s in CONVENTIONS.items():
        w = gausson_width_squared_unconstrained(name)
        sign = "+" if s > 0 else "-"
        lines.append(f"  {name:16s} ({sign}b ln)   sigma^2 = {w}")
        lines.append(f"                     normalisable Gaussian at b>0: "
                     f"{gaussian_exists(name)}")
    lines += [
        "",
        f"  |sigma^2| == Zloshchastiev a^2 : "
        f"{sp.simplify(sp.Abs(gausson_width_squared_unconstrained('vii_a_minus')) - zloshchastiev_length_squared()) == 0}",
        "",
        f"  E2  any normalised Gaussian  : Dx*Dp = {uncertainty_product()}",
        f"      negative control (Laplace): Dx*Dp = {laplace_uncertainty_product()}"
        f"  ({sp.nsimplify(laplace_uncertainty_product() / hbar)} hbar)",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())

# The Gausson under both LogSE sign conventions (\#189 E1/E2) — **NEGATIVE**

**Status: `MISDERIVED`, confirmed by symbolic substitution.** SSV-VII-a's
§"Saturation by the Gausson" fails twice over, and this note records the
computation that makes both failures checkable rather than asserted.

Pre-registered on [#189](https://github.com/StigNorland/SVT/issues/189),
child of [#182](https://github.com/StigNorland/SVT/issues/182). Script
`instruments/paper_vii_a/logse_gaussian.py`; tests
`instruments/test/paper_vii_a/test_logse_gaussian.py` (12). No receipt: every
result here is a closed-form symbolic identity, so there is no number to record
and nothing to drift.

## The two findings

**E1 — the Gausson does not exist on the branch SSV-I adopted.** Substituting
the Gaussian ansatz into

    i hbar d_t Psi = -hbar^2/(2m) d_x^2 Psi + s * b * Psi * ln(|Psi|^2/rho_0)

and requiring the `x^2` terms to cancel (so that `E` is a constant) fixes the
width uniquely:

| convention | printed by | `sigma^2` | consequence at `b > 0` |
|---|---|---|---|
| `s = -1`, i.e. `- b Psi ln` | **SSV-VII-a** (line 321) | `+hbar^2/(2mb)` | Gausson exists — VII-a's `eq:gausson` is **algebraically correct in its own convention** |
| `s = +1`, i.e. `+ b ln` | SSV-I (272), SSV-II (2667), SSV-IV (1409), SSV-V (637) | `-hbar^2/(2mb)` | `sigma^2 < 0` — **no normalisable Gaussian exists** |

SSV-I (\#183) rejected the attractive branch because it makes the uniform
vacuum modulationally unstable and cannot support `c_s = c`. On the branch
actually adopted, §"Saturation by the Gausson" has **no solution to stand on**,
and particles must be *topological* rather than bright solitons.

The two widths differ only in sign (`test_the_two_conventions_differ_only_by_
the_sign_of_sigma_squared`). This matters for how the finding is stated:
**VII-a did not miscalculate.** It wrote a correct equation for a theory the
series has since rejected.

**Checkbox 2 of \#189 — consistent.** `|sigma^2| = hbar^2/(2m|b|)` is exactly
Zloshchastiev's length `a`, on both branches. The LogSE has a *single* length
scale, appearing as the bright-soliton width for one sign and as the healing
length `xi` for the other.

**E2 — the `hbar/2` is imported, not derived, on either branch.** VII-a claimed
the prefactor follows "directly from the LogSE itself, without importing it from
the standard wave-packet calculation", offering as evidence that the result is
independent of the Gausson width `sigma` and therefore of `b`.

That independence is the tell. Computed here for an **arbitrary** normalised
Gaussian, with `b`, `rho_0` and the LogSE nowhere in the calculation:

    Dx * Dp = hbar/2

for every width tested, and `b` does not appear in the result's free symbols at
all. The LogSE contributed only the claim that its stationary state is Gaussian
— and under E1 it has no such state.

## The negative control, and why it is the point

E2 as stated so far shows only that *Gaussians* give `hbar/2`. That is not yet
an argument, because it would look identical if **every** normalisable state
saturated the bound. A check that cannot fail is not a check (FM3), so the
module computes a normalised non-Gaussian:

| state | `Dx * Dp` |
|---|---|
| any Gaussian, any width | `hbar/2` |
| Laplace, `psi ~ exp(-\|x\|/lambda)` | `sqrt(2)/2 hbar ≈ 0.707 hbar` |

Saturation is therefore a property of Gaussianity specifically, not of
normalisability — which is exactly the claim E2 needs and exactly what makes
VII-a's derivation circular.

## Method note

The substitution expands the logarithm by hand,
`ln(A^2 exp(-x^2/sigma^2)/rho_0) = ln(A^2/rho_0) - x^2/sigma^2`, because sympy
raises `PolynomialError` collecting powers out of a log of an exponential. The
expansion is exact, not an approximation.

`sigma` is declared positive in the module — correct for a width, but it could
in principle let sympy discard a negative root before it is seen. E1 is
therefore solved a second time on an unconstrained symbol
(`gausson_width_squared_unconstrained`), and
`test_positivity_assumption_does_not_manufacture_the_result` requires the two
to agree where a solution legitimately exists. **The negative conclusion is not
an artefact of the assumption used to state it.**

## What this does not settle

Whether the uncertainty principle is recoverable as "hydraulic stiffness of the
vacuum" in the sense VII-a intends, from a **topological** defect rather than a
bright soliton. That question shares a root with \#196 and \#178: the bare
one-component order parameter may simply not carry the required structure, in
which case the replacement is not a substitution but a change of theory.

## Cross-paper consequence

Five papers print the logarithmic term; four print `+b ln` and SSV-VII-a prints
`-b ln`. One grep over the series is the whole of \#189, and nothing in the
repository ran it. `test_the_series_sign_conventions_are_still_what_189_found`
freezes the measurement so it cannot change silently; generalising it to all
symbols and units is [#205](https://github.com/StigNorland/SVT/issues/205).

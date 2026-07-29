# SSV-VII-a — E-gate report

Gate: **E-GATE COMPLETE** · #189 · supersedes the partial report of 2026-07-27

Scope: all 21 equations / 23 labels of `papers/SSV-VII-a/main.tex`. The earlier
version of this file covered E1–E2 only, i.e. one subsection.

| # | Location | Finding | Verdict |
|---|---|---|---|
| E1 | `eq:gausson` | the Gausson exists only on the branch #183 rejected | **`MISDERIVED`** |
| E2 | `eq:gausson-saturation` | `hbar/2` is imported, not derived, on either branch | **`MISDERIVED`** |
| E3 | `eq:Veff-coulomb` | Coulomb reduction credited to Paper I; it is Paper II's | **`MISATTRIBUTED`** |
| E4 | `eq:born-derived` | the basin argument assumes the Born exponent it concludes | **`MISDERIVED`** |
| E5 | `eq:polar` vs `eq:gausson-Dx` | `rho` carries two normalisation conventions | **defect, recorded** |
| E6 | `eq:gamma-k` | `kappa` is written without the index its definition gives it | **notation, recorded** |
| — | `eq:continuity`–`eq:euler`, `eq:Q`, `eq:phase_quantisation`, `eq:circulation`, `eq:U_expand`, `eq:schrodinger`, `eq:rydberg`, `eq:superposition`, `eq:born` | checked, no defect found | `OK` |

## E1 — the Gausson does not exist under the adopted branch

**Now machine-checked** (`instruments/paper_vii_a/logse_gaussian.py`), where the
2026-07-27 report asserted it. Substituting the Gaussian ansatz and requiring
the `x^2` terms to cancel fixes `sigma^2 = -hbar^2/(2 m s b)`:

| convention | `sigma^2` at `b>0` | |
|---|---|---|
| `-b Psi ln` (VII-a, line 321) | `+hbar^2/(2mb)` | Gausson exists |
| `+b ln` (SSV-I, II, IV, V) | `-hbar^2/(2mb)` | **no normalisable Gaussian** |

**Independent confirmation.** BBM's own paper defines `ell = hbar/sqrt(2mb)`,
i.e. `ell^2 = hbar^2/(2mb)` — quoted verbatim in `papers/cited/notes/bbm1976.md`
— which is exactly the width the substitution returns for VII-a's convention.
The symbolic result and the primary source agree without either being fitted to
the other.

**Stated precisely:** VII-a did not miscalculate. It wrote a correct equation
for a theory the series has since rejected. `|sigma^2| = hbar^2/(2m|b|)` equals
Zloshchastiev's `a^2` on both branches (checkbox 2 of #189, **consistent**), so
the LogSE has one length scale wearing two faces.

## E2 — the `hbar/2` is imported, not derived

Computed for an **arbitrary** normalised Gaussian with `b` and `rho_0` absent
from the calculation: `Dx*Dp = hbar/2`, and `b` does not appear in the result's
free symbols.

The 2026-07-27 report stopped here. That was not enough: the observation would
look identical if *every* normalisable state saturated the bound, in which case
"the Gaussian is what does the work" would be empty. The negative control:

| state | `Dx*Dp` |
|---|---|
| any Gaussian, any width | `hbar/2` |
| Laplace, `psi ~ exp(-\|x\|/lambda)` | `sqrt(2)/2 hbar ≈ 0.707 hbar` |

Saturation is specific to Gaussianity, not to normalisability — which is the
claim E2 needs, and which is what makes VII-a's derivation circular.

## E3 — the Coulomb potential is credited to the wrong paper

`eq:Veff-coulomb` was justified as "the content of Paper I's electromagnetism
sector". It is not there. Paper I fixes `alpha = c_perp/c` and states the chiral
stiffness acts "in the statics of charged defects (**Paper II's Coulomb
sector**)" (`SSV-I/main.tex:374`). The Bernoulli-pressure derivation of
`F_C = alpha hbar c / r^2` is `SSV-II/main.tex:490` ff.

Compounding it: SSV-II's own claim table records the Coulomb coupling as
**empirical `alpha`**. So the `1/r` form is derived and the strength is an
input, making the Rydberg recovery a **consistency** result given
`{m_e, alpha, c}` — not a prediction. VII-a's "direct consequence … with no
fresh numerical input" was half right: no *fresh* input, but not derived.

Repaired in place, and `SSV-II` added to VII-a's citations, which previously did
not include the paper its central potential comes from.

## E4 — the Born basin argument assumes its own conclusion

This is E2's error in a second place, and it was not previously identified.

    eps_k = |c_k|^2 |psi_k|^2   ->   Gamma_k ∝ eps_k   ->   P_k ∝ |c_k|^2

The first arrow **is** the Born weight: the premise that delivered energy
density is quadratic in amplitude. It is the same assumption the preceding
paragraph offers as the informal consistency argument. Cancelling `kappa`
removes a factor common to every branch; it cannot change an exponent that
entered at step one.

**Internal contradiction, now resolved.** The paper asserted "the Born rule is a
derived consequence … not merely a consistency statement" while its own
testable-claims list said the basin calculation "is the calculation needed
before the measurement section can be promoted from physical interpretation to
formal derivation". Two statements about the same result, in one document,
pointing opposite ways — FM7. Resolved toward the weaker claim, per standing
rule 1.

**What survives:** given (a) rate linear in delivered energy density, (b) a
threshold mode common to all branches so `kappa` is genuinely `k`-independent,
and (c) unit normalisation, the reconnection-threshold model reproduces Born
weights rather than a competing rule. That is a real constraint on the
measurement model. It is not a derivation of the exponent.

## E5 — `rho` carries two conventions

`eq:polar` declares `rho` the **mass density** with `|Psi|^2 = rho`. But
`eq:gausson-Dx` gives `(Dx)^2 = sigma^2/2`, which requires
`∫|Psi|^2 dx = 1` — a probability density. Both are used, and `rho_0` inside
the logarithm inherits whichever is in force.

Harmless for `eq:continuity`–`eq:euler` (`Q` is invariant under
`rho -> lambda rho`), but it is one symbol with two dimensions, which is the
FM4 class that survived the entire #182 audit in three other papers. Now stated
once in §"Polar decomposition" rather than left implicit; generalised as #205.

## E6 — `kappa` notation

`kappa ≡ ∫ g |psi_k|^2 dV` contains `psi_k`, so as written it carries a `k`
index. The cancellation in `eq:born-derived` requires it not to. The
branch-independence is an assumption and is now stated as one rather than
hidden in the notation.

## Consequence

§"Saturation by the Gausson" is retained as an explicitly labelled
rejected-branch record (owner's decision, 2026-07-28), mirroring Paper I's
handling of its rejected sign. The `resultbox` claiming the prefactor was
derived is replaced by its negation. The Born paragraph keeps its argument and
loses its conclusion.

Both negative results are guarded against silent re-upgrade: the E1/E2 pair by
`test_logse_gaussian.py` (12 tests) and a `claims.py` predicate anchored to the
paper's own text.

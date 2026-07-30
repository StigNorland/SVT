# Route D result: Kelvin-mode degeneracy and the 8ⁿ rule (2026-06-05)

**Issue:** [#78](https://github.com/StigNorland/SVT/issues/78) Task D.
**Verdict: the 8ⁿ closed-shell rule is REFUTED as a first-principles degeneracy.**
Both sub-tests come back negative.

> **Issue #218 correction (2026-07-30).** The coefficient-one profile gives
> \(C_{\rm LogSE}=2.226289\), not \(1.880\), and the corrected BdG kinetic
> block is \(-\nabla^2\), not \(-\nabla^2/2\). Recalculation leaves the
> refutation intact. It also corrects the group-theory wording below:
> axial \(U(1)\) labels one-dimensional complex \(m\) sectors; a chiral vortex
> does not have a reflection symmetry that enforces a degenerate \(+m/-m\)
> doublet.

## Part (b): does the generation ratio collapse 8.59 → 8 with the real C?

**No.** Script: `instruments/paper_i/vortex_ring_core_constant.py`.

The Lamb ring-energy formula `E(R) = πR[ln(8R/ξ) − C]` was inverted against the
lepton masses with the core constant `C` taken from the corrected LogSE vortex
profile (`C_LogSE = 2.226289`):

| C | best-fit R_e/ξ | best-fit q | q/8 |
|---|---|---|---|
| 2.000 (thin-ring) | 1.014 | 8.587 | 1.073 |
| **2.226289 (corrected LogSE)** | **1.271** | **8.587** | **1.073** |
| 1.000 | 0.373 | 8.587 | 1.073 |
| 0.000 | 0.137 | 8.587 | 1.073 |

The best-fit generation ratio `q = 8.587` is **independent of C** — it is fixed
by the lepton mass ratios alone (the geometric-series fit `m_n ∝ E(R_e qⁿ)`),
while `C` only sets the absolute `R_e`. So using the physically-correct core
constant does **not** bring `q` to 8; the `8ⁿ` rule stays a ~7.3% approximation,
not an exact relation. With corrected \(C=2.226289\), the fixed
`R={1,8,64}ξ` control is not admissible because its \(R=\xi\) reference has
\(\ln 8-C<0\); the fitted-radius control instead gives \(R_e/\xi=1.271\).

## Part (a): does the first closed shell have degeneracy 8 = (1s+3p)×2?

**No.** Script: `instruments/paper_i/vortex_core_mode_spectrum.py`.

Linearising the LogSE about the straight singly-wound vortex `Ψ₀ = f(r)e^{iθ}`
and solving the radial Bogoliubov-de Gennes problem per azimuthal index `m`:

At \(L=12\,\xi,\ n=300\), the corrected signed spectrum contains the
translation partners \(\omega=\pm0.0133\) in the \(m=\mp1\) sectors. Moving
the boundary to \(L=16\,\xi\) reduces this finite-box lift to
\(\lvert\omega\rvert=0.0071\). Other absolute frequencies are
discretisation- and box-dependent and are not used as predictions.

### The group-theory reason (robust, independent of the numerics)

A vortex ring has **axial U(1) symmetry** (rotation about the ring axis) and
nothing more. Its normal modes are labelled by a single azimuthal integer `m`.
The complex irreducible representations of \(U(1)\) are one-dimensional, and
the wound background breaks the reflection that could pair \(+m\) and \(-m\).
There is therefore no symmetry-protected `(1, 2, 2, 2, …)` tower.

The atomic magic number **8 = (1s + 3p) × 2** comes from **SO(3)**: the 3-fold
degeneracy of the `l=1` p-orbitals (`m_l = −1, 0, +1`) plus the `l=0` s-orbital,
times 2 for spin. A vortex ring has no SO(3) — there is no 3-fold-degenerate
"p-shell." **The ring's actual symmetry does not produce a closure at 8.**
The "8" in the empirical `q ≈ 8.59` is therefore *not* a
Kelvin-mode shell-closure degeneracy.

## Combined conclusion

The closed-shell hypothesis in `notes/volovik-mapping.md` is **refuted**:

1. The empirical generation ratio is `8.587`, not `8`, and the real LogSE core
   constant does not close the 7% gap.
2. The vortex ring's symmetry (U(1)) cannot produce the atomic magic number 8;
   that number is an SO(3) artifact with no analog here.

The `8ⁿ` ladder remains a **numerical curiosity at the ~5–7% level**, consistent
with the Path-A finding that the whole mass ladder is a two-coincidence
numerology on present evidence. It is *not* a first-principles degeneracy law.

The `notes/volovik-mapping.md` closed-shell section should be updated to record
this refutation.

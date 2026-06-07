# Route D result: Kelvin-mode degeneracy and the 8ⁿ rule (2026-06-05)

**Issue:** [#78](https://github.com/StigNorland/SVT/issues/78) Task D.
**Verdict: the 8ⁿ closed-shell rule is REFUTED as a first-principles degeneracy.**
Both sub-tests come back negative.

## Part (b): does the generation ratio collapse 8.59 → 8 with the real C?

**No.** Script: `instruments/paper_i/vortex_ring_core_constant.py`.

The Lamb ring-energy formula `E(R) = πR[ln(8R/ξ) − C]` was inverted against the
lepton masses with the core constant `C` taken from the *real* LogSE vortex
profile (`C_LogSE = 1.880`, vs the thin-ring `C ≈ 2`):

| C | best-fit R_e/ξ | best-fit q | q/8 |
|---|---|---|---|
| 2.000 (thin-ring) | 1.014 | 8.587 | 1.073 |
| **1.880 (real LogSE)** | **0.899** | **8.587** | **1.073** |
| 1.000 | 0.373 | 8.587 | 1.073 |
| 0.000 | 0.137 | 8.587 | 1.073 |

The best-fit generation ratio `q = 8.587` is **independent of C** — it is fixed
by the lepton mass ratios alone (the geometric-series fit `m_n ∝ E(R_e qⁿ)`),
while `C` only sets the absolute `R_e`. So using the physically-correct core
constant does **not** bring `q` to 8; the `8ⁿ` rule stays a ~7.3% approximation,
not an exact relation. The fixed-`R={1,8,64}ξ` rule with the real C=1.880 gives
the muon mass to only −56% (because the implied `R_e` shifts to 0.90 ξ).

## Part (a): does the first closed shell have degeneracy 8 = (1s+3p)×2?

**No.** Script: `instruments/paper_i/vortex_core_mode_spectrum.py`.

Linearising the LogSE about the straight singly-wound vortex `Ψ₀ = f(r)e^{iθ}`
and solving the radial Bogoliubov-de Gennes problem per azimuthal index `m`:

| m | degeneracy | lowest ω (sim units) |
|---|---|---|
| 0 | 1 | 0.153, 0.359, 0.578, … |
| ±1 | 2 | 0.252, 0.471, 0.701, … |
| ±2 | 2 | 0.348, 0.583, 0.826, … |
| ±3 | 2 | 0.435, 0.684, 0.940, … |
| ±4 | 2 | 0.521, 0.784, 1.054, … |

**Cumulative state count by |m|: 1, 3, 5, 7, 9, …** — the *odd* numbers.

### The group-theory reason (robust, independent of the numerics)

A vortex ring has **axial U(1) symmetry** (rotation about the ring axis) and
nothing more. Its normal modes are labelled by a single azimuthal integer `m`,
with degeneracy 1 for `m=0` and 2 for `|m|≥1` (the `±m` doublet). The mode tower
is therefore `(1, 2, 2, 2, …)`, cumulative `(1, 3, 5, 7, …)`.

The atomic magic number **8 = (1s + 3p) × 2** comes from **SO(3)**: the 3-fold
degeneracy of the `l=1` p-orbitals (`m_l = −1, 0, +1`) plus the `l=0` s-orbital,
times 2 for spin. A vortex ring has no SO(3) — there is no 3-fold-degenerate
"p-shell." Even adding a ×2 core-chirality factor only rescales the U(1) tower to
`(2, 6, 10, …)`; **no combination of the ring's actual symmetry produces a
closure at 8.** The "8" in the empirical `q ≈ 8.59` is therefore *not* a
Kelvin-mode shell-closure degeneracy.

(Caveat: the `m=±1` branch did not collapse to an exact translation zero-mode —
a finite-box lift in this bounded radial solve — so the absolute frequencies are
illustrative. The *degeneracy structure* `(1,2,2,…)` is exact from the U(1)
symmetry and is the load-bearing result.)

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

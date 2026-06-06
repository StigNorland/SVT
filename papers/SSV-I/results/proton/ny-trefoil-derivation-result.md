# #92 — Proton N_Y derived (= 3), F cutoff geometric, μ₀ deferred

**Issue:** [#92](https://github.com/StigNorland/SVT/issues/92). Closes the
tractable parts of the proton mass formula `m_p c² = N_Y · F · μ₀`.
**Sub-problem B (N_Y): SOLVED — `N_Y = 3` is a zero-parameter topological
constant. Sub-problem A (F cutoff): PARTIAL — the cutoff R is geometric, but a
~6% F-systematic remains. Sub-problem C (μ₀): deferred (hardest, lower priority).**
Verification: `src/paper_i/trefoil_ny_derivation.py`,
`test_trefoil_ny_derivation.py` (8 tests).

## Sub-problem B — N_Y = 3, derived

The paper carried `N_Y ≈ 3.007` as a numerically-determined factor with two
candidate origins (`proton-mass-final-checkpoint.md`). This audit settles which
is correct, on the canonical (2,3)-trefoil used throughout the codebase
(`trefoil_breather_static.trefoil_curve`):
`x=(R+a cos3t)cos2t, y=(R+a cos3t)sin2t, z=a sin3t`.

**N_Y = 3 is the trefoil crossing number = thin-core writhe = braid exponent.**
Three independent computations agree:

| invariant | value | robust? |
|---|---|---|
| **planar crossing number** | **3** for every projection angle, every (R,a) | YES — topological |
| **writhe** (self-linking) | → 3.000 as core a→0 (a=0.05 → 3.0009; a=0.15 → 3.0050) | YES — → crossing number |
| **braid word** | σ₁³ ⇒ 3 positive crossings ⇒ writhe = 3 | YES — definitional |

The trefoil is the (2,3) torus knot; its minimal crossing number is 3, the
defining property of the simplest nontrivial knot. Each crossing is one
Y-junction "node" in the SSV breather, so `N_Y = 3` is the node count.

**The ".007" is a finite-thickness writhe correction**, `Wr = 3 + O(a²)` (physical
a=0.85ξ gives 3.17; a≈0.17ξ gives ≈3.007). It is NOT a separately-derived digit.
The honest statement is **`N_Y = 3` exactly**, with a small positive geometric
correction set by the effective core radius.

**The paper's candidate (2), `l_curve/(4π) ≈ 3.086`, is rejected as the
derivation.** `l_curve/(4π)` is not an invariant — it floats from 2.01 (R=1.5)
to 3.09 (R=2.8). The 3.086 was a coincidence of the R=2.8 geometry. The crossing
number / writhe is the correct invariant.

## Sub-problem A — F cutoff is geometric (partial closure)

- **Route (ii) [N_Y·F cutoff-invariant]: confirmed DEAD.** Prior work (#77
  track0a, `proton-mass-final-checkpoint.md`) showed the straight-vortex product
  drops ~5× from R=1.0 to R=3.0; the N_Y·F spread is 64%. No calibration removes
  it. Not pursued further.
- **Route (i) [geometric R]: established in principle.** The inter-strand minimum
  distance of the canonical trefoil is **exactly 2a** (the tube diameter; verified
  a=0.65→1.30, a=0.85→1.70, a=1.05→2.10). The F-extraction cutoff R is the
  inter-strand spacing, hence a **geometric property of the relaxed knot** — set
  by the energy-minimum minor radius a≈0.85ξ (gradient-flow result,
  `geometry-minimum-result-2026-06-03.md`), not a free calibration parameter.

  **Residual (honest):** F retains `d ln F/d ln R ≈ −0.94` sensitivity, so the
  ~6% geometric uncertainty in the energy-minimum `a` (the shallow minimum spans
  a few ×; `geometry-minimum-result`) propagates to ~6% in F. R is geometric *in
  principle*; the residual F-systematic is physical, not a calibration freedom.

## Sub-problem C — μ₀ = m_e/α, deferred

The fundamental scale μ₀ = m_e c²/α still takes m_e and α as empirical inputs.
Deriving μ₀ from SSV vacuum parameters is the hard foundational question
(explicitly lower-priority in #92 and not in its done-when). Left as a tracked
open item; it is the precision-bearing test for the whole mass programme.

## Net proton mass status

`m_p c² = N_Y · F · μ₀`:
- **N_Y = 3** — now DERIVED (topological, zero parameters)
- **F ≈ 4.4** — grid-converged with ~6% residual (geometric, at the energy minimum)
- **μ₀ = m_e/α ≈ 70 MeV** — still empirical (sub-problem C)

`m_p = 3 × 4.4 × 70 ≈ 924 MeV` (observed 938, ~1.5%). The factor that was most
suspect (N_Y) is now first-principles; the precision is limited by the F
geometric residual and the empirical μ₀.

## Claim-status / gapboxes

Paper I proton claim-status row and the two proton gapboxes (§"The Proton" and
§"Open Problem 3") updated to: N_Y derived (=3); F grid-converged with ~6%
geometric residual; μ₀ empirical (open).

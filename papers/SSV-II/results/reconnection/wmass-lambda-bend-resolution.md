# Resolving the W-mass cap bending-stiffness shortfall (#105)

**Issue:** #105 · **Date:** 2026-06-07 · **Branch:** `issue-105-wmass-lambda-bend`
**Script:** `instruments/paper_ii/wmass_cap_scale_resolution.py`
**Test:** `instruments/test/paper_ii/test_wmass_cap_scale_resolution.py`
**Builds on:** `lperp_core_integral` (J+K core integrals), `chiral_cap_equilibrium`
(cubic), `vortex_cap_mass` (τ); related #97 (cap-radius grid convergence), #15.

## Pre-registration

The W mass in Paper II §`sec:W_rayleigh` is a *conditional prediction, open one
step*: `R_cap = φ/α` (hence `m_W ≈ 78.9 GeV`, 1.8% from PDG) follows from the cap
equilibrium cubic `R³ + τR² = λ_bend` **iff** the bending stiffness
`λ_bend = φ³/α³ ≈ 1.09×10⁷ ξ³` can be sourced from the chiral-shear sector. The
local curvature correction gives only `λ_bend^local = λ_⊥(J+K)/4 ≈ 4.7×10⁴ ξ³` —
**a factor 232 short.**

**Decision rule (from #105):** the issue closes when the cap radius / `m_W` is
obtained *without the unexplained 232× fudge* — the `1/α` scale arising from the
framework rather than back-solved from `m_W` — by any one of routes A–D, to the
precision already claimed. Derivation preferred. A correctly-negative exhaustion
(demotion to coincidence) is an equally valid closure (rule 1).

## Results

### E — Normalization audit (cheap; done first)

`m_W = π φ² (m_e/α²)` with `m_e/α² = 9.60 GeV` and **two** caps. Back-solving the
observed `m_W = 80.37 GeV` gives `R_cap = 1.633 ξ/α`. **The `1.70 ξ/α` stated at
main.tex line 1393 is stale** (`1.70² → 87 GeV`, not 78.9); the correct fit is
`1.633`, and `φ = 1.618` matches it to **0.91%** — i.e. the golden-ratio
identification is *better* than the text implies. Target re-pinned.

### A — Local curvature is structurally insufficient (confirmed, with diagnosis)

`λ_bend^local = (J+K)/4 · α⁻²` is **inherently `α⁻²`** because `λ_⊥ = α⁻²` and
`(J+K)/4 = 2.50` is an O(1) core integral. The required stiffness is `α⁻³`, so

```
gap = (φ³ / ((J+K)/4)) · (1/α) = 1.693 × 137 = 232.
```

**The shortfall is exactly one power of `1/α = R*/ξ` (the ring/core ratio).**
Feeding the local stiffness into the equilibrium cubic puts the cap at
`R_eq ≈ 31 ξ ≈ α^(−2/3)` — **not** the ring scale `ξ/α = 137 ξ` — giving
`m_W ≈ 1.6 GeV` (51× too small). No local curvature correction can ever reach the
ring scale. Route A (strictly local) is **falsified**, structurally, not just
numerically.

### B — Resolution: the cap scale is the inherited electron ring scale ✅

The reconnecting defects **are** electron-scale rings of radius `R* = ξ/α`
(derived in Paper I from the Lamb energy minimisation). A reconnection cap cannot
be smaller than the ring throats it joins, so `R_cap = O(1)·R*`, hence

```
m_W ~ P0 · R_cap² · ξ ~ m_e (R*/ξ)² = m_e/α² ≈ 9.6 GeV.
```

**The `1/α²` scale of `m_W` is therefore framework-derived** (it is the ring/core
ratio squared, the same `R* = ξ/α` that fixes the electron in Paper I). The 232×
"shortfall" was an **artefact of trying to set `R_cap` by a local bending
equilibrium**, which is not the mechanism that sets the cap scale. The residual
prefactor `π φ² ≈ 8.2` (two caps × π × cap aspect `φ²`) is O(1); only `φ` remains
coincidence-grade — at the same level as the other weak-sector O(1)'s
(`tan²θ_W` within 1.5×, `m_Z` tree-level within 1.3%).

### A′ — Sharpest open form (recorded, not the closure)

If one *retains* the bending-equilibrium picture, the required stiffness is
exactly `λ_⊥` evaluated at the **cap** scale with a linear running `λ_⊥(k) ~ 1/k`:

```
λ_bend = (J+K)/4 · α⁻² · (R_cap/ξ) = (J+K)/4 · φ/α³ = 1.04×10⁷ ξ³,
```

within **4.4%** of `φ³/α³`. Both B and A′ say the same thing — the relevant scale
is the ring (cap) scale `ξ/α`, not the core scale `ξ`. Whether the chiral-shear
dispersion actually runs linearly is an *undelivered* derivation, so A′ does not
close #105 on its own; B does.

## Verdict

**#105 resolved by route B.** The 232× shortfall is dissolved: it was an artefact
of an inappropriate sub-model (local bending equilibrium for `R_cap`). The `m_W`
**scale** `~ m_e/α²` is **derived** from the inherited electron ring radius
`R* = ξ/α`. The remaining `π φ²` prefactor is O(1), with `φ` coincidence-grade.

## Claim-status change (rule 5)

| Claim | Before | After |
|---|---|---|
| `m_W` order of magnitude (`~ m_e/α² ~ 10 GeV`) | suggestive | **derived** (inherited ring scale) |
| `λ_bend = φ³/α³` "from local chiral shear" | open gapbox (232× short) | **retired** — local curvature is structurally `α⁻²`; not the mechanism |
| `R_cap = φ/α` exact value (`m_W = 78.9 GeV`) | conditional prediction | **scale derived; `φ` O(1) coincidence** (0.9% match) |

## Honest residuals / what is *not* claimed (rule 1)

- `φ` is **not** derived — it remains a numerical coincidence (a pinch-off aspect
  ratio). The full `m_W` value is therefore "scale-derived, coefficient-coincidence."
- The ring-scale inheritance is an analytic/structural argument; the direct
  numerical confirmation (cap radius ∝ `R*` in the relaxed event) is route C and
  remains **open under #97** (the desktop-feasible form is the `R_cap ∝ √λ_⊥`
  scaling test, blocked on cap-radius grid convergence). #97 stays open.
- Routes A (non-local enhancement) and D (Seifert/Casimir) are neither needed nor
  refuted; A′ shows what an enhancement would have to be.

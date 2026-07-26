# Issue #166 sub-calculation 2 — the screen spin-2 stress sector

> **⚠ CORRECTION (sub-calc 3, [induced-polarization-issue166.md](induced-polarization-issue166.md)).**
> The "short-range → massive bulk mode → R2-leaning" reading below is **wrong**,
> and is retracted. It used the *membrane-paradigm* inference (screen stress =
> graviton boundary value, so its range is the graviton's range). For an
> *induced* metric (Sakharov; the correct reading for SSV) the logic reverses:
> the short-range stress is the **polarisation** that induces a **local** Einstein
> term, and the graviton stays **massless by diffeomorphism invariance** (a
> theorem; precondition = the conserved stress shown here). Sub-calc 3 computes
> the induced coefficient: `1/16πG ∝ +1/ξ²` (positive, `R²=0.999`, L-stable). So
> the short-range result is a **feature** (locality), not the death-knell stated
> below. Read this note for the *stress-exists-and-is-conserved* result only; the
> range/verdict claims are superseded.

**Status: necessary condition PASSES, with a scale catch.** A conserved,
two-polarisation **spin-2 stress sector exists** on the screen — nonzero,
transverse (Ward identity), and conformal — for a *conformal* screen. This is
demonstrated, not named (it clears #166's "no naming a scalar bilinear spin-2"
bar). ~~**But SSV's scale `ξ` makes that spin-2 stress short-range (Yukawa):** it
can source only a short-range / **massive** bulk mode, not the long-range
massless graviton real gravity needs.~~ *(superseded — see correction above:
short-range stress induces a local, massless-by-symmetry, positive-G Einstein
term; ξ sets G, not the range.)*

Pre-registered on [#166](https://github.com/StigNorland/SVT/issues/166) before
the computation. Script `instruments/model_screen/screen_stress_spin2.py`; tests
`instruments/test/model_screen/test_screen_stress_spin2.py` (5: Ward, power law,
spin-2 two-polarisation swap, massive Yukawa, verdict); receipt
`screen_stress_spin2_receipt.json`.

## Why this is the decisive object

Even though the SSV order parameter is scalar, every local field theory has a
stress tensor `T_μν` — a **spin-2 conserved current** (point 4 of #166). The
question is not whether *a* spin-2 object exists (it must) but whether the screen
carries a **conserved, two-polarisation** stress response with the correct Ward
identities — the thing #166 forbids assembling by hand.

## Method

Free scalar, `D = 4` Euclidean, minimal stress tensor
`T_μν = ∂_μφ ∂_νφ − ½δ_μν(∂φ)²`. The two-point function follows from Wick:
`⟨T_μν T_ρσ⟩ = W_μρW_νσ + W_μσW_νρ − δ_ρσ(W²)_μν − δ_μν(W²)_ρσ + ½δ_μνδ_ρσ tr(W²)`
with `W_μν(r) = ⟨∂_μφ ∂_νφ⟩ = A(D−2)[δ_μν/r^D − D r_μr_ν/r^{D+2}]`. On the screen
tangent plane {1,2}: trace `θ = ½(T₁₁+T₂₂)` is spin-0; the traceless pair
`σ₊ = ½(T₁₁−T₂₂)`, `σ× = T₁₂` is spin-2 (plus/cross). The massive (SSV-like)
screen uses the lattice propagator `1/(m²+k̂²)` (scale `ξ ~ 1/m`).

## Positive controls (all pass)

| control | result | meaning |
|---|---|---|
| **C1** Ward / conservation | `∂^μC / C = 7×10⁻⁷` | the stress response is **transverse** (a conserved current, not a bilinear) |
| **C2** conformal power law | `r^{2D}·|C|` spread `= 0` | massless `⟨TT⟩ ∝ 1/r⁸` — the `C_T` structure |
| **C3** spin-2, two polarisations | swap holds exactly | `σ₊` and `σ×` exchange under a 45° rotation of the separation — the `|n|=2` law |
| **C4** massive Yukawa | `μ = 0.407` vs lattice mass `0.397` | massive propagator → `W, ⟨TT⟩ ~ e^{−2μr}`, **short-range** |

## Result (spin-2 two-point vs separation angle ψ)

| ψ | ⟨σ₊σ₊⟩ | ⟨σ×σ×⟩ | ⟨σ₊σ×⟩ |
|---|---|---|---|
| 0     | +0.0128 | −0.0077 | 0 |
| π/8   | +0.0026 | +0.0026 | +0.0103 |
| π/4   | −0.0077 | +0.0128 | 0 |

The spin-2 sector is **nonzero**, and `⟨σ₊σ₊⟩(0) = ⟨σ×σ×⟩(π/4)` exactly — the two
polarisations rotate into each other with period π/2, the signature of a genuine
`|n|=2` (spin-2) two-point function.

## Verdict (against the #166 rules)

- **Spin-2 raw material with correct structure: PRESENT.** Nonzero, transverse
  (Ward), two-polarisation, conformal — a *demonstrated* conserved spin-2 stress,
  not a named bilinear. Another R1 necessary condition cleared.
- **Scale catch → R2-leaning.** SSV's `ξ` makes the spin-2 stress **short-range**
  (Yukawa, `μ ≈ m`). A short-range screen stress sources a short-range / **massive**
  bulk mode, not the long-range massless graviton. The massless-graviton
  reconstruction requires a **conformal** screen; SSV's scale `ξ` gives a
  non-conformal one → the honest reading is **R2**: a consistent
  superfluid-plus-container whose gravity is short-range / massive, unless the
  screen is conformal at horizon scales (its scale `ξ` says it is not).

## Honesty items and scope (rule 1)

- **Not a soft positive.** "Spin-2 exists" is the *minimum* any local QFT gives; I
  have only shown SSV clears the necessary structural bar (Ward + two
  polarisations), not that it *derives* gravity. #166's R1 remains open.
- **Not yet decided.** The two remaining R1 items are untouched: does the bulk TT
  response *follow from the screen state* (not be imposed as in #162), and does the
  normalisation **fix `G`** rather than rename it (the `C_T ↔ 1/G` datum). Those,
  plus the massless-vs-massive graviton question here, are where R1/R2 finally
  separate.
- **Minimal vs improved stress tensor.** I used the minimal `T_μν`; the spin-2
  (traceless) projection is improvement-independent, so the two-polarisation
  result stands. The exact `C_T` / trace sector would need the conformal
  improvement — deferred to the normalisation calculation.

## Net

Two necessary conditions for the bulk–screen duality now pass in validated
computations: modular flow stays geometric (#166 sub-calc 1) **and** the screen
carries a demonstrated conserved spin-2 stress (this note). Neither is a soft
positive; both are the raw materials R1 requires. The decisive turn is the
**scale**: SSV's `ξ` forces the spin-2 stress short-range → a massive/short-range
graviton, not long-range GR. Whether the screen can be conformal at horizon scales
(and whether its normalisation fixes `G` instead of renaming it) is where the
duality finally lives (R1) or reduces to a consistent-but-imported container (R2).

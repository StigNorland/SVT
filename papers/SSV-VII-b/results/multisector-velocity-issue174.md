# No-go map (II) — a bosonic superfluid has no natural universal `c` (tree level)

**Status: NEGATIVE (confirms #172 in SSV's own variables).** Two *coupled* bosonic
sectors of a superfluid have **different sound speeds** — different "speeds of
light." Even with **identical** components, turning on the inter-sector coupling
`g12` splits them, and the splitting is **zero only at the fully fine-tuned point**
(identical components *and* `g12 = 0`). So a bosonic superfluid does **not** supply
the universal `c` that Lorentz invariance requires — the tree-level manifestation
of the naturalness no-go, computed directly in SSV's variables.

Pre-registered on [#174](https://github.com/StigNorland/SVT/issues/174) before the
computation. Script `instruments/model_lorentz/multisector_velocity.py`; tests
`instruments/test/model_lorentz/test_multisector_velocity.py` (6); receipt
`multisector_velocity_receipt.json`.

## Scope (honest — rule 1)

The *full* naturalness problem is about **radiative** corrections amplifying
velocity differences (power-law vs logarithmic convergence), which needs
interactions/holography free-field tools cannot reach. This note does the
tractable, decisive **tree-level** piece: *do two coupled bosonic sectors even
share a common `c`?* If not already at tree level, there is no universal `c` to
protect — and the radiative story (which makes it worse) is moot for the
existence question.

## Method

Two-component Bogoliubov superfluid (masses `m_i`, densities `n_i`, intra-couplings
`g_i`, inter-coupling `g12`). The two branches:

    ω±² = ½(E1²+E2²) ± ½√((E1²−E2²)² + 16 g12² n1 n2 ε1 ε2),   ε_i = k²/2m_i,
    E_i² = ε_i(ε_i + 2 g_i n_i).

Low-`k` sound speeds `c_i² = g_i n_i/m_i`, and

    c±² = ½[(c1²+c2²) ± √((c1²−c2²)² + 4W²)],   W² = g12² n1 n2/(m1 m2),

so the **sector velocity splitting** `Δ(c²) = c+²−c−² = √((c1²−c2²)² + 4W²) ≥ 0`,
zero **iff** `c1=c2` *and* `g12=0`. Stability (miscibility): `g12² < g1 g2`.

## Positive controls (all pass)

| control | result | meaning |
|---|---|---|
| **C1** degenerate when tuned | `c+ = c−` at `g12=0`, identical | the *one* point with a single speed |
| **C2** numeric = analytic | BdG low-`k` slopes match `c±` to `<10⁻³` | the dispersion solver is correct |
| **C3** high-`k` → `z=2` | `ω/(k²/2m) = 1.001` | each branch becomes the free-particle (`z=2`) UV — ties to the crossover story |

## Result

Identical components (`m,n,g` equal), coupled at `g12 = 0.5`:
**`c+ = 1.225`, `c− = 0.707` → `Δc/c̄ = 0.54`** — a **54 % difference** in the two
sectors' speeds of light, from coupling alone.

| `g12` (identical comps) | `Δc/c̄` | | asymmetry `g2` (decoupled) | `Δc/c̄` |
|---|---|---|---|---|
| 0.0 | **0.000** | | 1.0 | **0.000** |
| 0.2 | 0.202 | | 1.3 | 0.131 |
| 0.4 | 0.417 | | 1.6 | 0.234 |
| 0.6 | 0.667 | | 2.0 | 0.343 |
| 0.8 | 1.000 | | | |

Both knobs split the speeds; `Δc = 0` occurs **only** at the fully fine-tuned point
(identical **and** decoupled), and coupling **increases** the split.

## Verdict (against the pre-registered rule)

- **T: NO natural universal `c`.** The sector velocity splitting vanishes only under
  full fine-tuning (identical components *and* `g12=0`); any generic coupled or
  asymmetric configuration gives an O(1) split, and coupling makes it worse. A
  bosonic superfluid does **not** supply a universal speed of light across its
  low-energy sectors — the naturalness no-go, made concrete and SSV-specific at
  tree level.

**Net:** #172 said (from the literature) that a bosonic superfluid lacks a
universal-`c` protection; this computes it directly — coupled sectors carry
different speeds of light, tunable to a common value only by hand. The negative is
firm and reinforces the standalone closure.

## Honesty items and scope (rule 1)

- **Tree-level only.** This shows there is *no universal `c` to begin with* (and
  coupling worsens it). The **radiative amplification** (Collins et al.) and its
  **power-law/holographic cure** (Bednik–Pujolàs–Sibiryakov) are beyond free-field
  tools and remain with #172's literature grounding.
- **This is the negative, computed — not a new obstruction.** It is the tree-level
  face of #172, in SSV's variables; it does not add a *second* no-go.
- **The cure is unchanged.** A universal `c` for coupled bosonic sectors needs a
  symmetry/strong dynamics the bare superfluid lacks — i.e., the holographic
  container (#172), which supplies the power-law lock. Whether SSV's specific dual
  achieves it stays the open, strong-coupling question.

## Net

The naturalness no-go is now grounded on both sides: **established in the
literature** (#172) and **computed in SSV's own two-component superfluid** (this
note). A bosonic superfluid has no universal speed of light without fine-tuning; the
only cure is the strong/holographic container. Holography remains doubly essential
— for the transverse gravity *and* for the universal `c` — with the SSV-specific
power-law lock the remaining open computation.

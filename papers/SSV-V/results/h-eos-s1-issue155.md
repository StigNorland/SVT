# H-EOS S1 — surface gravity, Unruh T, and the trans-Planckian robustness margin of a flowing LogSE dumb-hole; the Jacobson route closes in form (issue #155)

**Status: R1(a) — the flowing LogSE dumb-hole has a regular acoustic horizon
with surface gravity and Unruh/Hawking temperature matching the Visser
analogue-gravity forms, and thermality is robust for scale-separated horizons
(margin M = ξ/(π r_H) → 0). Together with S2 (area-law dS), the Jacobson route
closes IN FORM: δQ = T·dS ⇒ ∇²Φ = 4πG_eff·e/c² with G_eff = 1/(4ħc·η). The
missingness is, again, entirely in the coefficient — G's magnitude overshoots
by (a_p/ℓ_P)² ≈ 1.69×10³⁸, the conceded sub-grain input. "Form yes, G no"
through the full chain. The genuine new content is the quantified W4/#148
caveat: the margin is O(1) at grain-scale (local Rindler) horizons, so the
acoustic-horizon thermodynamics is robust only conditionally on horizon ≫
grain.**

Pre-registered on issue [#155](https://github.com/StigNorland/SVT/issues/155)
(S1(a)/S1(b)/S1(c) in the body; the instrument design, the four quantities, the
robustness margin, and the decision rules posted as a comment *before
computing*, rule 6). Owner's scope: analytic + scale-separation margin (not a
full dispersive mode-propagation solver). Script
`instruments/paper_v/dumb_hole_surface_gravity.py`; receipt
`papers/SSV-V/results/heos_s1_receipt.json`; figure
`papers/SSV-V/figures/heos_s1_dumbhole.png`; tests
`instruments/test/paper_v/test_dumb_hole_surface_gravity.py` (6).

## What was computed

The acoustic metric is **kinematic** — fixed algebraically by the flow
(ρ, v, c_s) with no back-reaction (Visser 1997, gr-qc/9712010, §14: "form yes,
G no"). A 3D mass-conserving radial sink `v(r) = c_s (r_H/r)²` (a radial sink,
not a pure vortex, is required for a true horizon — Visser §5/§8) crosses the
density-independent LogSE sound speed `c_s = √B0` at the acoustic horizon `r_H`.

| quantity | analytic | numeric | agreement |
|---|---|---|---|
| surface gravity `g_H = ½\|∂_r(c_s²−v²)\|_{r_H}` (Visser eq 70) | `2c_s²/r_H` | from the profile | rel-err **1.3×10⁻⁶** |
| Hawking/Unruh `kT_H = ħg_H/(2πc_s)` (eq 118) | `c_s/(π r_H)` | `g_H/(2πc_s)` | rel-err **1.3×10⁻⁶** |
| dispersion `ω²=c_s²k²+k⁴/4` group velocity | superluminal ∀k; excess `(3/8)k²/c_s` | measured coeff **0.375** | exact |

**The negative-capable test — trans-Planckian robustness (W4/#148).** The LogSE
phonon dispersion is **superluminal for all k>0** (`v_g = (c_s²+k²/2)/√(c_s²+k²/4) > c_s`,
excess `(3/8)k²/c_s`), so high-k modes outrun sound and leak across the horizon
(Corley–Jacobson 1996; Unruh–Schützhold 2005). Thermality is robust iff the
surface-gravity frequency sits below the dispersion frequency:

> **margin `M = g_H ξ/(2πc_s²) = ξ/(π r_H)`** — robust iff `M ≪ 1`.

Measured: `M = 0.113, 0.056, 0.028, 0.014, 0.0070, 0.0035` for
`r_H/ξ = 2.8, 5.7, 11, 23, 45, 91` — monotone → 0 (robust for scale-separated
horizons), crossing `M = 1` at the grain scale `r_H = ξ/π ≈ 0.23`.

## Verdict: R1(a), and the carried negative

- **R1(a) (form):** a regular acoustic horizon exists; `g_H` and `T_H` match
  the Visser forms to 10⁻⁶; thermality is robust for `r_H ≫ ξ`. This is the
  *expected, kinematic* side (rule 1): the analogue-gravity result is generic;
  the LogSE specialization just confirms it.
- **S1(b):** the area-law `dS = η dA` input is **S2 (R1)** — cited, not
  recomputed.
- **S1(c) — the Jacobson route closes in form.** Imposing `δQ = T_H·dS` on the
  local horizon (Jacobson 1995; VII-b §5.1) yields `∇²Φ = 4πG_eff·e/c²` with
  `G_eff = 1/(4ħc·η)`. The S2 coefficient `η = c₂ = 3.69` is **O(1) per ξ²**, so
  `G_eff ~ ξ²c³/ħ` (grain scale) and overshoots `G_N` by
  `(a_p/ℓ_P)² = 1/α_G = (m_P/m_p)² ≈ 1.69×10³⁸`.
  **Guard (rule 1):** `(a_p/ℓ_P)² = 1/α_G` is the #122 *identity* (`ℓ_P` and
  `α_G` both contain `G`), **not** a derivation; G's magnitude stays conceded
  (D-b, #154). S1(c) shows only that the *form* closes and the magnitude is
  *exactly* the conceded overshoot.

## The genuine new content (rule 1): the W4/#148 caveat, quantified

The margin `M = ξ/(π r_H)` is fantastically small for astrophysical horizons
(`r_H` km-scale, `ξ` sub-grain ⇒ `M ~ 10⁻⁴⁰`) but **O(1) for the local Rindler
horizons of the Jacobson construction at grain-scale acceleration**. The
Jacobson derivation requires the Clausius relation to hold on *every* local
Rindler horizon at *every* point — including horizons whose acceleration scale
approaches the grain. There, the superluminal LogSE dispersion makes the horizon
leaky and the Hawking thermality is not guaranteed. So the acoustic-horizon
thermodynamics underpinning the compliance law is robust **conditionally on
horizon ≫ grain** — the same ≲10⁻¹⁷ local-Lorentz protection #148 already owes
(W4), now made quantitative for the gravity sector. This does not overturn R1(a)
(the construction works for the macroscopic horizons that matter for gravity),
but it is a recorded, non-trivial limitation and a falsifiable handle: a regime
where local horizons are forced to the grain scale would break the route.

## Consequences (applied this branch)

- **SSV-V §7.2** (surface gravity / Hawking T): the schematic
  `κ = c⁴/(GM)` / `T_H` argument is supplemented with the concrete kinematic
  dumb-hole computation (`g_H = 2c_s²/r_H`, `T_H = c_s/(π r_H)`, both verified)
  and the trans-Planckian robustness margin `M = ξ/(π r_H)` with its grain-scale
  caveat.
- **SSV-V §7** forward note (added in S2): updated — the surface-gravity / Unruh
  legs are now **delivered (S1)**; together with the area-law input (S2) the
  Jacobson route closes in form, coefficient `η→G` conceded.
- **Claim-status (rule 5):** "acoustic-horizon surface gravity & Unruh T from
  the medium" → **derived (kinematic)**; "Jacobson route closes (form)" →
  **derived (form), conditional on horizon ≫ grain (W4)**; "G magnitude" stays
  **conceded input**.

## Status

#155 S1 resolves the analytic half: **R1(a)**, surface gravity + Unruh T match
Visser, thermality robust for scale-separated horizons, and the Clausius closure
delivers the compliance form with the conceded `(a_p/ℓ_P)²` overshoot. Together
with **S2** (area-law `dS`, [h-eos-s2-issue155](h-eos-s2-issue155.md)) the
Jacobson route is complete **in form**. Still live on #155: **H-A0-IR** (the a₀
coefficient + the duality over-constraint falsifier — the same G must fit η,
a₀=cH₀/2π, and a_p/ℓ_P). See [project-holographic-screen-bridge] and
[ref-visser-acoustic-black-holes].

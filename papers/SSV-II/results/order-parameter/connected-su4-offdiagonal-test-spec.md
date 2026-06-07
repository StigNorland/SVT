# Spec — the off-diagonal SU(4) test: is SSV's colour a connected symmetry or just labels? (2026-06-05)

**Status: SPEC + pre-registered decision rule. No solver yet — written before coding,
per the project habit (cf. `lr-su4-logse-spec.md`).** This is the colour-sector twin
of the spinor decision #83: #83 asks whether the field carries a *spin* orientation;
this asks whether it carries a *colour* orientation — or only colour *labels*.

## The question

#79/#80 delivered the **kinematic** skeleton of SU(4) colour from a 4-valent
junction: the Cartan `u(1)³`, the Weyl group `S₄`, and `B−L` inside the Cartan
(`su4_junction_chirality_closure.analyse_su4_junction` → `lie_closure` returns **3**,
not 15). That is *case (b)*: charges + a discrete relabeling. The open **dynamical**
question:

> Does an SSV order parameter realise SU(4) as a **connected** symmetry — i.e. are
> the **12 off-diagonal generators** (the ladder operators that rotate one colour
> into another, incl. quark↔lepton since lepton = 4th colour) genuine dynamical
> symmetries — or do only the Cartan + Weyl survive (colour = separate boxes)?

- **CONNECTED (case a):** colour is a rotatable internal orientation, like spin. One
  genuinely unified field; the over-constrained SSV win.
- **PRODUCT (case b):** colour is discrete labels; the SU(4) was bookkeeping, and
  SSV is "several fields" in single-field clothing.

## The discriminator (two coupled measurements)

1. **Off-diagonal matrix element.** For each off-diagonal generator `T_ij` of su(4)
   (the raising/lowering operator mixing colour components `i,j` of the order
   parameter `z ∈ C⁴`, including `i,4` = quark↔lepton), compute the dynamical
   bridge matrix element between the colour-`i` and colour-`j` single-defect sectors
   under the SSV energy operator. **Non-vanishing** ⇒ the sectors talk ⇒ candidate
   connected. **Vanishing by a selection rule** ⇒ product (the #76 outcome).
2. **Lie-algebra closure.** Feed the *dynamically realised* generators (the Cartan,
   plus every off-diagonal `T_ij` whose matrix element survives) to `lie_closure`.
   - returns **15** = `dim su(4)` ⇒ **CONNECTED**;
   - returns **3** = `u(1)³` ⇒ **PRODUCT** (today's kinematic answer);
   - returns an intermediate (e.g. 8 = an su(3) subalgebra, 6 = so(4), …) ⇒
     **PARTIAL** — report which subgroup is realised.

These reuse, not reinvent: `lie_closure` (already returns 3 for the kinematic case),
and the #76 `chiral_overlap` bridge pattern (`instruments/paper_i/chiral_bridge_projection.py`),
which already encodes how a dynamical operator's matrix element between two modes
either survives or vanishes by an azimuthal selection rule.

## The mechanism, concretely

Take the multi-component order parameter of `lr-su4-logse-spec.md`: colour carried
by `z = (z₁,z₂,z₃,z₄) ∈ C⁴` (4 = quarks + lepton), **shared condensate density**
`ρ = Σ|z_a|²`, LogSE skeleton + chiral-shear `L_perp`. An off-diagonal generator
`T_ij` acts as a continuous SU(2) rotation in the `(z_i,z_j)` plane. The functional
is connected-SU(4)-symmetric **iff** `E[z]` is invariant under every such rotation.

- The **shared-ρ log potential** `p(ρ ln ρ − ρ + 1)` depends only on `ρ = Σ|z_a|²`
  ⇒ it *is* SU(4)-invariant (it can't tell the colours apart). Good sign for (a).
- The **gradient term** `Σ_a ½|∇z_a|²` is also SU(4)-invariant. Good sign.
- The **chiral-shear `L_perp`** is where it can break: if it couples the *individual*
  sector currents `j_a = Im(z_a*∇z_a)` in a colour-dependent way (e.g. only the
  diagonal `Σ|∇×j_a|²`), it is invariant only under the Cartan + permutations, **not**
  the off-diagonal rotations. If it depends only on the *total* current
  `j = Σ_a j_a` (i.e. `|∇×j_total|²`), it is fully SU(4)-invariant.

So the test sharpens to: **does the SSV chiral-shear term see the total colour
current (connected) or the individual sector currents (product)?** This is a concrete,
decidable property of the master-equation `L_perp`, exactly analogous to the #81
"is the cross term P-even or P-odd" question.

## CHEAP ANALYTIC ROUTE FIRST (do before any solver — the #81 lesson)

Before the 3D relaxer, run the **selection-rule audit** of the off-diagonal overlap,
generalising `chiral_overlap`:

- Compute `⟨ colour-j defect | Ô_Lperp | colour-i defect ⟩` for one off-diagonal
  `T_ij` (e.g. quark↔lepton, `i=1,j=4`) at the straight-vortex / single-mode level,
  symbolically where possible.
- Decide whether it **vanishes by an azimuthal / sector selection rule** (as the #76
  bridge did via `m_a=m_b` and `m_a+m_b=0`), or is generically nonzero.
- This is days, not weeks, and may decide the whole question — as the #81 cheap route
  + CP/parity audit did, without ever building the full solver.

## PRE-REGISTERED DECISION RULE (fixed before runs)

Let `M_ij` = the convergence-validated off-diagonal matrix element, `σ` its noise
floor (grid/regrid scatter), and `d = lie_closure(realised generators)`.

- **CONNECTED (case a):** `|M_ij| ≥ 5σ` for the off-diagonal generators AND `d = 15`,
  both grid-converged (regrid/continuation; not a `dx¹` lattice artifact, per the
  Peierls–Nabarro lesson). → SSV realises one connected SU(4) field.
- **PRODUCT (case b):** `M_ij` vanishes by a selection rule (analytic) OR
  `|M_ij| < 5σ` after convergence, with `d = 3`. → colour is labels; the SU(4) is
  bookkeeping; SSV is effectively several fields.
- **PARTIAL:** `d ∈ {4,…,14}` — report the realised subalgebra (which off-diagonal
  generators survive) and treat as a refined-but-incomplete connectivity.
- **Robustness rider:** the verdict must survive `λ_perp` natural-value choices and
  the chiral-shear "total vs sector current" form being read from the master
  equation, not chosen to taste; a verdict that flips under these is **INCONCLUSIVE**.

## Why this is the honest frontier

The pattern across #78/#80/#81: the **discrete** skeleton (Cartan, Weyl, charges,
multiplicities, anomaly) falls out *for free* and is done; the **continuous,
connecting** structure (off-diagonal generators here; the half-integer ℤ₂ for spin
in #83; the parity-odd chirality in #81) keeps needing something the scalar field
lacks. A scalar-with-junctions gives **labels**; a field with genuine internal
orientation gives **rotations**. This test is the colour-side measurement of that one
recurring fork.

## Reuse map

| need | reuse |
|---|---|
| Lie-algebra dimension of realised generators | `lie_closure` (`su3_y_junction` / re-exported) |
| off-diagonal generators, Cartan, B−L | `su4_junction_chirality_closure.{su4_cartan_generators,b_minus_L_direction}` |
| dynamical bridge matrix element + selection-rule structure | `instruments/paper_i/chiral_bridge_projection.py` (`chiral_overlap`, `current_variation_m`) |
| multi-component shared-ρ functional + L_perp lift | `lr-su4-logse-spec.md`; `lperp_helpers.py` |
| 3D relaxer (only if the cheap route is positive/inconclusive) | `trefoil_gradient_flow_static.py`, `gradient_flow_numba.py` |

## Milestones

1. **(this note)** spec + pre-registered rule. ✔
2. **Cheap selection-rule audit** of one off-diagonal overlap (quark↔lepton),
   generalising `chiral_overlap`. Gate: if it vanishes by a rule → PRODUCT, stop.
3. **Full test** (only if needed): multi-component relaxer → realised generators →
   `lie_closure` → 15 / 3 / intermediate, against the rule.
4. **Decision**, with script, tests, and a result note; posted to the tracking issue.

## Cautions

- The chiral-shear "total vs sector current" reading is load-bearing — settle it from
  the master equation, like the #81 CP-parity reading, before trusting any number.
- These selection-rule nulls have bitten twice (#76 muon bridge; #81 needing P-odd).
  A vanishing `M_ij` is a clean negative, not a bug.
- `.venv/bin/python` (Python not on PATH).

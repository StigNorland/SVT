# Issue #170 — can the bulk–screen reconstruction be *presentist*? (Lifshitz z≠1 modular locality)

**Status: cautionary NEGATIVE — a real but partial tension.** At the relativistic
point (`z=1`, eternalist) the screen's modular flow is geometric (the CHM boost,
far-tail 1.8% = sub-calc 1). At **SSV's physical UV** (`z=2`, the Bogoliubov
quadratic dispersion — a *preferred-foliation* / presentist screen) a **robust,
N-converged non-local component appears** in the modular Hamiltonian (far-tail
**7% ≈ 3.9× the z=1 value**, the largest of any screen tested). So the preferred
foliation **degrades the geometricity** that the boost-based entanglement→gravity
reconstruction (#166) requires — exactly as the absence of Lorentz boosts
(no Bisognano–Wichmann/CHM theorem) predicts. **Honest bounds:** it is a *partial*
(~7%) non-locality, not an order-1 collapse, and its `z`-dependence is
**non-monotonic**, so this is a **tension, not a clean law**.

Pre-registered on [#170](https://github.com/StigNorland/SVT/issues/170) before
the computation. Script `instruments/model_screen/lifshitz_modular.py`; tests
`instruments/test/model_screen/test_lifshitz_modular.py` (4); receipt
`lifshitz_modular_receipt.json`.

## Why this is the presentism test

SSV has a preferred frame (the condensate) — what a presentist "now" needs. But
the #166 reconstruction was borrowed from **AdS/CFT, which is eternalist** (fully
Lorentz/conformally invariant). The presentism-compatible holographies are the
**preferred-foliation** ones (Lifshitz / Hořava, anisotropic scaling with
dynamical exponent `z≠1`), and that is also SSV's own UV: the Bogoliubov
dispersion is linear in the IR (`z=1`) and **quadratic past ξ (`z=2`)**. The
first necessary condition of the reconstruction — a **geometric** modular
Hamiltonian — is the local **boost** (CHM), a theorem of Lorentz boost symmetry.
A `z≠1` screen has **no boost** (its absence *is* the preferred time). So the
presentist feature is precisely what can make the modular Hamiltonian non-local.

## Method

Free scalar, Dirichlet chain (reuse sub-calc 1), Lifshitz dispersion
`ω_k = (k̂²)^{z/2}` (`z=1` = relativistic massless; `z=2` = SSV's UV). Modular
`H_π` from the Gaussian correlators (Peschel–Eisler; valid for any dispersion).
Non-locality = far-tail weight of `H_π` at `|i−j| ≥ ℓ/2`.

## Result

| z | S | far-tail(H_π) |
|---|---|---|
| 1.00 (relativistic) | 0.702 | **0.0178** (geometric = sub-calc 1) |
| 1.25 | 0.994 | 0.0112 |
| 1.50 | 1.325 | 0.0135 |
| 1.75 | 1.704 | 0.0282 |
| 2.00 (SSV UV) | 2.147 | **0.0695** (≈ 3.9×) |

**Robustness (the honesty check — rule 1).** The `z=2` far-tail is **converged in
chain size**: `0.06951` at `N = 800, 1600, 2400, 3200` (unchanged) — so it is
*physical*, not the finite-size/IR artifact that spoiled sub-calc 1's periodic
ring. It stays elevated across block sizes (`0.074 / 0.070 / 0.067` at
`ℓ = 24/40/60`, ratio 4–5×). The `z=1` control reproduces the geometric CHM
value.

## Verdict (against the pre-registered rule)

- **Pre-registered comparison** (far-tail `z=2` ≫ `z=1`) is met **robustly**
  (3.9×, N-converged) → the preferred foliation **degrades** the modular
  geometricity → the boost-based reconstruction's *first* necessary condition is
  weakened for a presentist screen.
- **Honest qualifications (rule 1):**
  1. **Partial, not total.** 7% far-tail is the largest seen, but not order-1 —
     a degradation, not a collapse.
  2. **Non-monotonic in z.** Extending the sweep: `0.018 (z=1) → 0.014 (1.5) →
     0.070 (2.0) → 0.037 (2.5) → 0.065 (4.0)`. The far-tail does *not* grow
     cleanly with `z`, so it is a **crude single-number probe**; the robust fact
     is the specific `z=1`-vs-`z=2` contrast, and `z=2` is the physically relevant
     case.

**Net:** presentism (a preferred foliation) and the boost-based entanglement→
gravity reconstruction are in **genuine tension, sharpest at SSV's physical
`z=2`** — a cautionary negative. The very feature SSV wants for a "now" (no boost)
is what erodes the CHM-geometric modular flow the #166 reconstruction leans on.

## Honesty items and scope (rule 1)

- **Standard reconstruction only.** This tests the *boost-based* Faulkner–VR
  geometricity condition. A non-geometric modular Hamiltonian breaks *that*
  machinery — it does **not** prove that no *modified*, non-relativistic
  (Lifshitz-holographic) reconstruction could exist. Whether a `z≠1` holographic
  reconstruction (e.g. via a Lifshitz RT prescription) recovers the bulk shear is
  a separate, open question.
- **Crude probe.** The far-tail is one scalar; the non-monotonic `z`-dependence
  says it does not cleanly rank "non-geometricity." A sharper diagnostic (e.g. the
  ABCH bilocal coefficient, or the first-law residual `δS − δ⟨K^{CHM}⟩` directly)
  would strengthen or soften the tension — the natural next probe.
- **1D screen.** As in sub-calc 1, this is a `d=1` boundary; the TT-graviton
  sector needs `d ≥ 3`. This tests the modular/geometricity link, not the full
  `d≥3` reconstruction.

## Net

The presentism-compatible container SSV needs (preferred foliation, `z=2`) is the
case where the boost-based reconstruction is most strained: the modular flow
picks up a robust non-local component absent in the eternalist (`z=1`) case. This
is a genuine tension — holography can supply SSV's *gravity* (relativistic
z=1-flavoured, #166), but making that same reconstruction *presentist* is not
free. The honest open question: does a *non-relativistic* holographic
reconstruction close where the boost-based one strains?

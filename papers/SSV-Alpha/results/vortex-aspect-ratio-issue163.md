# Issue #163 [MODEL 2/2] — α as a vortex aspect ratio: the circularity test

**Status: R2 — clean NEGATIVE, on two independent counts (circularity + no
α-free minimum).**
The SSV-Alpha hypothesis is that minimising the LogSE + chiral-shear functional
over toroidal vortices, *without inserting α*, yields a stable equilibrium with
`R*/ξ = α⁻¹ ≈ 137.036`. As the SSV machinery currently stands this cannot be
tested affirmatively: **the aspect ratio is inserted, not derived**, so the
pre-registered circularity guard fires. α remains a *conceded input*; the
information-content-per-resolution-cell reading (from the #161 session) stays
**interpretive**, not physical.

Pre-registered on [#163](https://github.com/StigNorland/SVT/issues/163) before
the computation. Script
`instruments/model_alpha/vortex_aspect_ratio.py`; tests
`instruments/test/model_alpha/test_vortex_aspect_ratio.py` (5: positive control,
LogSE collapse, reduced-balance coupling inversion, circularity, verdict);
receipt `vortex_aspect_ratio_receipt.json`.

## What was pre-registered

- **R1 (derived):** a stable equilibrium with `R*/ξ = 137.036 ± tol` and **no α
  inserted anywhere**.
- **R2 (clean negative):** no stable α-free equilibrium, **or** the aspect ratio
  depends on a constant pinned by α (circularity).
- **Circularity guard:** if a constant in the functional is itself fixed by α,
  the result is circular → automatic R2 regardless of the number that emerges.

## (A) Circularity — the aspect ratio is inserted, not derived *(load-bearing)*

The electron ring radius enters the existing SSV toroidal machinery **as the
nondimensionalisation**:

- `instruments/paper_i/thin_ring_alpha_correction.py` header:
  *"Nondimensionalisation: xi = 1, R_e / xi = alpha^{-1}"*.
- `ToroidalBackground(alpha=α)` sets `r_e = 1/α` directly; the finite-α scans
  loop over α values (including the physical `7.297e-3`) and read off
  `ring_radius = r_e = α⁻¹`.

And the coupling that would *set* the ring size is itself α: the Coulomb near
field is `F_C = α ħc / r²` (SSV-Alpha), with α *defined* as the chiral-shear
coupling. So `R*/ξ` depends on a constant pinned by α — the circularity guard
fires. **`R*/ξ = α⁻¹` is the input nondimensionalisation, computed here as
137.036, i.e. exactly what was put in.**

## (B) No α-free minimum — the pure-LogSE ring collapses

The only α-free object is the pure-LogSE ring (chiral-shear off, `λ_perp = 0`).
Its thin-core (Kelvin) energy `E(r) = r[ln(8r) − 2]` has

| r | dE/dr = ln(8r) − 1 |
|---|---|
| 1   | **+1.079** |
| 137 | **+6.000** |

`dE/dr > 0` across the entire physical range `r ≥ 1` → the energy is lowered by
*shrinking*; there is no stable large-radius equilibrium. This is exactly the
**collapse** that `instruments/paper_i/lepton_ring_static.py` detects for
pure-LogSE rings. Without a stabilising coupling there is no `R*` at all — let
alone 137.

## (C) Reduced balance — `r*` is set by the coupling *(illustrative, caveated)*

Add a generic outward stabiliser `g/r^p` to the ring tension and minimise. The
equilibrium `r*(g)` is fixed by the input coupling — you get out what you tune in:

- coupling needed to place `r* = 137` (Coulomb-like `p = 1`): **g ≈ 1.13×10⁵**.
- `r*` if the coupling equals α (7.3×10⁻³): **none** — a small coupling opens no
  large ring; the ring collapses.

So 137 requires a **large** inserted coupling, the *opposite* of the small α — a
small coupling gives a small (or no) ring. The claimed `R*/ξ = α⁻¹` (large ring
from small coupling) is not the natural output of a tension-vs-stabiliser
balance; it is imposed. *(Caveat: the exact SSV chiral-shear term may differ in
its R-dependence; (C) corroborates but the load-bearing claim is (A).)*

## Verdict and decision rules

- **R1 (derived): not met** — α is the nondimensionalisation, not an output.
- **R2 (clean negative): TRIGGERED**, on both independent counts: (A) the aspect
  ratio depends on a constant pinned by α (circularity), and (B) the α-free ring
  has no stable equilibrium (collapse).

## Honesty items (rule 1)

- **This does not prove α is underivable.** It proves the *present* machinery
  inserts it. A genuine derivation would require fixing the chiral-shear coupling
  by α-*independent* physics (a topological/geometric constant), then showing the
  minimisation returns 137.036. SSV-Alpha itself calls this "the central open
  calculation… that remains to be done"; it remains not done, and the existing
  toroidal code is circular by construction.
- **Consequence for the #161 session's α reading.** The
  information-content-per-resolution-cell interpretation (`α⁻¹ = R*/ξ = extent in
  resolution cells`) was flagged as gaining teeth *only if* this minimisation
  landed on 137.036 without inserting α. It does not. So the reading stays
  **interpretive**, and #161 §A's claim-status for α is **unchanged: conceded
  input.**
- No fitted constants were introduced; the negative needs none.

## Net

The two-model post-#161 program closes with two honest results in the same
spirit: **#162** — the superfluid's gravity-sector response is generic (SSV
superfluous), with the effect/cause dictionary confirmed; **#163** — the one
place an internal magnitude might have been derived (α as a defect-geometry
eigenvalue) is, as implemented, circular: `R*/ξ = α⁻¹` is the input, not the
output, and the α-free ring collapses. Both leave the #161 ledger intact and
better-grounded: gravity belongs to the container, and α remains a conceded
input pending an α-independent fixing of the chiral-shear coupling.

# Grid-Invariant F Extraction: The True F is ~2.5, Not 4.47 (2026-05-19)

This note resolves the F-factor grid-convergence puzzle from
`f-factor-grid-convergence-checkpoint.md`.  The "F grows with finer grid"
trend was largely an integration-domain artefact: the extractor's
`anchor_shell = 2 cells` becomes thinner in physical units as dx shrinks,
letting more boundary background leak into `e_interior` and inflating F.

## The fix

Added `--anchor-thickness-xi` to `trefoil_breather_observables.py`.  When set
to a positive value, the anchor shell is computed as
`anchor_cells = round(anchor_thickness_xi / dx)`, giving a grid-invariant
physical boundary exclusion.  Default behaviour unchanged (cell-based) for
backward compatibility.

## Result: F is approximately grid-converged at ~2.5, not 4.47

Re-extracting on the n=24/48/72 hw=6 penalty-preserved states with
`--anchor-thickness-xi 1.0` (matching the n=24 cell-based default):

| grid | dx (xi) | OLD F (cell) | NEW F (1.0 xi) | e_interior | mu_0 | n_y |
|---|---:|---:|---:|---:|---:|---:|
| n=24 | 0.500 | 4.547 | 4.547 (unchanged) | 607.7 | 3.577 | 37.4 |
| n=48 | 0.250 | 6.886 | **2.825** | 450.0 | 4.803 | 33.2 |
| n=72 | 0.167 | 8.208 | **2.435** | 478.8 | 5.556 | 35.4 |

Going from n=48 to n=72 changes F by **-14%**, suggesting the fine-grid
limit is around F ~ 2.0-2.5.

## What's happening

Three quantities matter:
1. **e_interior** (numerator): roughly stable across n=48 and n=72 (450 vs
   479, ~6% spread).  This is what the anchor-shell fix repaired.
2. **mu_0** (per-length tube energy, denominator): **grows with refinement**
   (3.58 -> 4.80 -> 5.56).  The kinetic term in the tube resolves sharper
   gradients at finer dx, so per-length tube energy is genuinely larger.
3. **n_y** (vortex line length in xi, denominator): roughly stable (37, 33, 35).

F decreases at fine grid because mu_0 grows faster than e_interior.
This is a property of how the extractor defines F, not a numerical bug.

## Implications

### The paper's F = 4.47 is a coarse-grid result

At n=24, the cell-based anchor accidentally gave the right physical
exclusion (1.0 xi), so the F=4.55 we got matched the paper at 1.7%.  But
at the genuine fine-grid limit, F drops to ~2.5.

The paper's proton mass calculation:
- Paper: N_Y * F * 70 MeV = 3.007 * 4.47 * 70 = 941 MeV (close to 938 MeV)
- True grid-converged: 3.007 * 2.5 * 70 = 527 MeV (43% below proton mass)

**The "0.3% precision" claim in the paper rests on a coarse-grid F.  With
proper grid convergence, the prediction is off by ~40%.**

### What can be salvaged

1. **The topology-preservation mechanism is solid**: penalty term preserves
   trefoil topology robustly across all tested grids.  This part of the
   work stands.

2. **The framework is consistent**: F as defined IS a well-defined integral.
   Its grid-converged value just isn't 4.47.  A different choice of
   calibration (e.g., a `mu_0` that's already converged) might give a
   different F that matches the paper.

3. **The paper might still be salvageable** if the relevant calibration
   `mu_0` is defined in physical units that don't depend on the calculation
   grid (e.g., the chiral scale 70 MeV itself).  Then F is whatever ratio
   keeps the product mu * F = constant.  The paper's value 4.47 would then
   be the value of F at the paper's chosen calibration grid, with the
   product enforced to give 941 MeV by construction.

### What's not yet investigated

- **Does F asymptote at higher n?**  n=72 was already 2-4 hours; n=96
  would be 6-12 hours; n=128 would be a day+.  The trend from 2.83 to
  2.43 (-14%) suggests the asymptote is below 2.4 but possibly not very
  much below.
- **Is the tube-only F (numerator = e_line + e_cavity only, exclude bulk
  residual) more grid-stable?**  This would test whether the bulk residual
  energy is the source of remaining grid dependence.
- **Does the paper's mu_0 calibration match ours?**  We use an arc-length
  slab of the resolved tube.  If the paper uses a different definition
  (e.g., the asymptotic per-length tension of a straight infinite vortex),
  mu_0 would be a different number and F would adjust.

## Bottom line

The 2% match to paper F=4.47 was a coarse-grid coincidence on the order
of 2x.  The grid-converged F using our calibration is ~2.5.  Whether this
breaks the paper's framework or just reflects a different calibration
convention is the open question.

The penalty-mechanism topology-preservation result is unaffected and remains
the substantive contribution of this session.

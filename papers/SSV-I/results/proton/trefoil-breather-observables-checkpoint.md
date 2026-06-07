# Trefoil-Knot Observables Checkpoint

This note records the first single-curve `N_Y` / `F` extractor, applied to the
existing `(2,3)`-trefoil-knot relaxed states produced by
`trefoil_breather_static.py`.

Artifacts:

- `instruments/paper_i/trefoil_breather_observables.py`
- `papers/SSV-I/data/trefoil-breather-observables-n48-hw5-400steps-2026-05-17.json`

## What The Extractor Does

The closed-knot analogue of `trefoil_y_junction_closed_observables.py`. Since
the `(2,3)`-trefoil knot is a single continuous closed curve with no
Y-junctions, the decomposition is:

- one **line tube** of radius `r_tube` around the knot curve (uses the same
  `trefoil_curve` sampler as the relaxation script)
- one **cavity ball** of radius `r_cavity` at the origin (where the paper
  expects the central breather depression)
- everything else inside the box minus the anchor shell is **bulk residual**

Self-calibration uses an arc-length slab around `s = L / 3` (an arbitrary
non-symmetric point on the closed curve). `mu_0_grid` here is the energy per
unit arc-length of a continuously curved knotted vortex line; it bakes in
curvature effects and is not directly comparable to the open-Y straight-line
`mu_0`.

## Results Across All Six Saved Trefoil States

| `n` | `hw` | `min_rho` | `r_{min}` | `E_int` | `E_line` | `E_cav` | `E_bulk` | `mu_0` | `L_tube` | `N_Y / L` | `F^int` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 24 | 5 | 0.957 | 0.36 | 1.23 | 0.45 | 0.13 | 0.64 | 0.005 | 28.45 | 3.78 | 2.11 |
| 24 | 6 | 0.987 | 0.43 | 0.97 | 0.30 | 0.07 | 0.60 | 0.005 | 30.98 | 2.15 | 2.64 |
| 24 | 7 | 0.995 | 0.51 | 0.76 | 0.20 | 0.02 | 0.53 | 0.004 | 31.39 | 1.64 | 3.34 |
| 48 | 5 | **0.007** | 0.99 | 48.12 | 22.05 | 7.69 | 18.38 | 0.234 | 30.39 | **4.18** | **1.62** |
| 48 | 6 | 0.308 | 0.22 | 32.77 | 11.80 | 3.39 | 17.59 | 0.191 | 30.99 | 2.57 | 2.16 |
| 48 | 7 | 0.773 | 0.25 | 24.24 | 6.63 | 1.11 | 16.50 | 0.141 | 31.09 | 1.77 | 3.13 |

`min_rho` is the deepest density anywhere in the relaxed state; `r_{min}` is
the distance from origin to that deepest point.

## Three Findings From The Table

### Finding 1: The trefoil has dissolved in five of the six saved states

All n=24 cases have `min_rho >= 0.957` — essentially uniform background. The
n=48 hw=6 and hw=7 cases have `min_rho` of 0.31 and 0.77 — partial
dissolution. Only `n=48, hw=5, 400 steps` retains deep cores
(`min_rho = 0.007`).

The pattern is consistent: closed vortex curves shrink under pure LogSE
gradient flow without external pinning. Finer grid and smaller box slow the
shrinkage; the smallest viable box at the highest tested resolution barely
preserves the structure for 400 steps. Larger box or coarser grid loses it.

This is the same instability that broke the symmetric closed Y-junction in
the previous checkpoint. Different topology, same root cause: the LogSE
energy decreases monotonically when a closed vortex contracts, and there is
no topological barrier in this functional that stops it.

### Finding 2: The extractor cannot detect topology loss on its own

The n=24 hw=7 row reports `N_Y/L = 1.64`, `F^int = 3.34` — superficially
reasonable numbers. But `E_interior = 0.76`: there is essentially no
structure in the box. The extractor still computes ratios because both the
numerator `(E_line + E_cavity)` and the denominator `mu_0 * L_tube` shrink
together when the field flattens.

The `min_rho` column is the only reliable indicator that the configuration
survived relaxation. `min_rho < 0.1` is a useful first cut for "the knot is
still present"; anything above ~0.5 should be flagged as dissolved before
its `N_Y / F` numbers are reported.

### Finding 3: Even the best-preserved state has spawned extra structure inside the cavity

The viable `n=48, hw=5` state has its deepest density at
`(0.31, -0.94, -0.10)`, `r = 0.99 xi` from origin. But the trefoil curve's
inner radius is `R - r = 2.8 - 0.85 = 1.95 xi`. The curve never approaches
within `r = 0.99` of origin. So the deepest density of the relaxed state is
in the central cavity, **not on the seeded knot curve**.

The most likely interpretation: during relaxation the knot has shed
additional vortex line (small ring(s)) into the central cavity. The "best"
state is therefore not just a relaxed trefoil knot but the trefoil plus
emitted cavity vortices.

This complicates the interpretation of the n=48 hw=5 numbers. `E_cavity = 7.69`
is substantial (16% of `E_interior`); some of that comes from the seeded
breather depression but some comes from the spawned vortex structure.

## Anchor Behaviour, In Contrast To The Y Geometries

A diagnostic point that comes out cleanly here: `E_anchor_shell = 0.88` on
the viable state, only 1.8% of `E_total = 49.00`. Compare to the open Y
(86%) and the symmetric closed Y (77%).

The reason is the multipole structure of the asymptotic vortex velocity
field:

- **Open Y**: three filaments emanating to infinity from a single node →
  monopole-like velocity, energy density `~ 1/r^2`, log- or linear-divergent
  total → anchor shell catches a large boundary-region contribution
- **Symmetric closed Y**: three `+1` filaments converging at each pole gives
  a `+3` winding monopole at each pole, still long-range and box-sensitive
- **(2,3)-trefoil knot**: closed continuous loop with zero monopole moment →
  asymptotic field decays as a dipole or faster, no log-divergent tail →
  anchor shell carries essentially nothing

This means the trefoil-knot geometry is the **only** topology in the repo
where `F^int` is naturally a finite, box-convergent quantity. The closed
theta-graph Y-junction would have been finite too if the seed had been
stable.

## Cross-Topology Comparison

The numbers we have for each topology after the most-defensible relaxation:

| topology | `N_Y / L` | `F^int` | comment |
|---|---:|---:|---|
| Open Y (n=48, hw=7) | 1.22 | 2.41 | anchor pins endpoints, F diverges with hw |
| Open Y (n=48, hw=8) | 1.15 | 2.57 | same trend |
| Closed Y theta `(+1,+1,+1)` (n=24, hw=6) | 0.56 | 30.65 | seed dissolved; numbers measure the wrong geometry |
| Trefoil knot (n=48, hw=5) | **4.18** | **1.62** | best-preserved closed configuration, no anchor artifact |

Paper I quotes `N_Y ~ 3.007` and `F ~ 4.47`. The trefoil-knot
`N_Y / L = 4.18` is in the same ballpark as `N_Y = 3.007` for the first
time, but the comparison is geometry-dependent (the paper's "Y-junction"
language does not literally match a `(2,3)`-trefoil knot) and the trefoil's
own dependence on `(n, hw)` is huge.

## What This Settles And Does Not Settle

Settles:

- the single-curve extractor mechanics work and additively account for
  `E_interior`
- the `(2,3)`-trefoil knot in this repo dissolves under pure LogSE gradient
  flow for almost all tested `(n, hw)`, leaving only one usable state
- the trefoil-knot geometry has a structurally clean anchor (essentially no
  boundary artifact) thanks to higher-multipole asymptotic field
- `min_rho` is the right first-line gate for whether any extractor output is
  meaningful

Does not settle:

- the actual physical `N_Y` of the proton-scale Y-junction (none of the
  tested configurations is both stable and matches the paper's geometry)
- whether the trefoil-knot `N_Y / L = 4.18` is converged: only one viable
  state exists, with no refinement gate available
- whether the cavity vortices in the n=48 hw=5 state are physical or a
  numerical artifact

## Next Pieces

Three plausible follow-ups, in increasing order of code cost:

1. **Longer / better-controlled relaxation of the `n = 48, hw = 5` trefoil**
   state, with a tighter early-stopping rule on the energy plateau, to check
   whether the cavity vortices are transient or settled. Cheapest piece;
   answers whether the surviving state is a real local minimum.
2. **Asymmetric `(+1, +1, -1)` closed Y-junction** prototype, the original
   "next piece" from the closed-Y observables checkpoint. Removes the `+3`
   monopole instability and should give a stable closed Y-junction whose
   `N_Y / F` can be compared head-to-head with the trefoil knot's numbers.
3. **Add a topology-pinning term** to the relaxation functional so any
   seeded configuration survives long enough to be measured. This is a
   bigger change (modifies the gradient flow) but it is the only way to
   measure `N_Y` for configurations that are not local minima of the bare
   LogSE functional.

# Trefoil Knot Dissolution Checkpoint

This note records a probe run that closes out the trefoil-knot refinement gate
question and consolidates the broader finding that has been emerging across
the closed-topology track: **none of the seeded vortex configurations
tested so far are stable LogSE solitons under pure gradient flow**.

Artifacts:

- `papers/SSV-I/data/trefoil-state-n48-hw5-800steps-2026-05-17.npz`
- `papers/SSV-I/data/trefoil-state-n48-hw5-800steps-2026-05-17.json`

## The Probe

The asymmetric closed Y refinement gate landed but the gate did not pass.
The natural fallback was the `(2, 3)`-trefoil knot, where one cell
(`n = 48, hw = 5, 400 steps`) had preserved deep cores (`min_rho = 0.007`)
and yielded the cleanest closed-topology numbers in the repo
(`N_Y / L = 4.18`, `F^int = 1.62`, anchor fraction 1.8%).

The question was whether this cell was a true local minimum or a transient
midway through dissolution. The test was simple: rerun the same
configuration with double the step count and check whether the knot is
still there.

## Result

| step count | `min_rho` | `final_E` | `depressed_fraction` | `deficit_volume` | `effective_radius` |
|---:|---:|---:|---:|---:|---:|
| 400 (existing) | **0.007** | 49.00 | substantial | substantial | substantial |
| 800 (new) | **0.972** | small | **0.000** | 4.62 | 3.57 |

Between step 400 and step 800 the configuration fully dissolved into trivial
background. `min_rho` went from `0.007` (deep vortex cores) to `0.972` (essentially uniform). `depressed_fraction` collapsed to zero.

So the `n = 48, hw = 5` state used in the trefoil observables checkpoint was
not a converged minimum. It was the relaxation caught at an intermediate
moment in its slide toward the trivial vacuum.

## What This Settles

The trefoil-knot configuration in `trefoil_breather_static.py`, under pure
LogSE gradient flow with uniform-background boundary anchor, is **not** a
stable soliton at any `(n, hw)` in the tested range. The dissolution rate
depends on `(n, hw)`:

- coarser grid: faster dissolution (curvature-driven shrinkage is poorly
  resolved, more numerical damping)
- larger box: faster dissolution (more room for the knot to contract before
  meeting the anchor)

The previously reported `n = 48, hw = 5, 400 steps` result was a fortunate
choice of step count that placed us on the slow tail of dissolution at the
"compressively-supported" smallest box, not at a true minimum. The number
`N_Y / L = 4.18` from that state should be downgraded from "the closest
match to the paper's `N_Y = 3.007`" to "a snapshot of a half-relaxed
configuration".

## The Broader Pattern

All four topologies tried so far in this branch:

| topology | stable under pure LogSE? | failure mode |
|---|:---:|---|
| Open Y `(+1,+1,+1)` | partial | anchor pins filament endpoints; cores survive but `F` diverges with `hw` |
| Closed Y sym `(+1,+1,+1)` | no | `+3` monopole at each pole fissions; cores migrate to equatorial outer ring |
| Closed Y asym `(+1,+1,-1)` | yes, but | cores survive; `F` diverges linearly with `hw`; bulk has long-range structure |
| `(2, 3)`-trefoil knot | no | curvature-driven shrinkage; configuration dissolves between 400 and 800 steps |

The only configuration that produced both stable seeded cores **and** a
finite-extent bulk was the asymmetric closed Y, and even that did not pass
the box-convergence gate.

This is consistent with the paper's own remark in Appendix
`app:minimisation`:

> "with the chiral non-local shear term ($\lambda=2000$), the energy
> functional is minimised on a 3D grid using gradient descent."

The paper's stabilisation comes from the chiral non-local shear term, the
`L_perp` piece of the full `L + L_perp` functional. Our prototype scripts
implement only `L` (the bare LogSE). Without `L_perp`, vortex configurations
are not topologically protected and gradient flow drives them toward the
trivial vacuum.

## Cross-Topology Comparison, Corrected

| topology | best `min_rho` | `N_Y / L` | `F^int` | comment |
|---|---:|---:|---:|---|
| Open Y (n=48, hw=8) | n/a | 1.15 | 2.57 (`log hw` divergent) | anchor-pinned filament endpoints; pure-LogSE artefact |
| Closed Y sym (n=24, hw=6) | 0.012 | 0.56 | 30.65 | seed dissolved + reorganised |
| Closed Y asym (n=48) | 0.0001 | 1.93 - 2.70 | 2.71 - 5.49 (`linear hw`) | stable cores; bulk diverges; not at minimum |
| Trefoil knot (n=48, hw=5, 400 steps) | 0.007 | 4.18 | 1.62 | **transient, not a minimum**; fully dissolved by 800 steps |
| Paper I quoted | n/a | 3.007 | 4.47 | uses `L + L_perp`; cannot be reproduced with pure `L` |

The asymmetric closed Y remains the only repo configuration with a
genuinely stable seed at the cost of a divergent bulk. The trefoil knot's
clean-anchor behaviour was real, but only because the field was on its way
to becoming trivial.

## What This Does Not Settle

- whether the configurations would be stable under a different relaxation
  scheme (e.g. norm-conserving Sobolev gradient flow, or projected
  topological-sector gradient flow)
- whether the asymmetric closed Y's linear `F` divergence has a clean
  physical interpretation in the `L`-only sector or is itself an artefact
- what the actual `L_perp` term looks like operationally, and what its
  parameter `lambda = 2000` does to the relaxation

## Implications For Paper I

Two things follow directly:

- the numerical "evidence" for `N_Y = 3.007` and `F = 4.47` is currently
  contingent on the `L_perp` term that is not yet in any repo prototype.
  Reproducing those numbers from first principles requires implementing
  `L_perp`.
- the Workstream 2 exit gate (per
  `docs/numerical-minimisation-roadmap.md`: "the relaxed breather is
  stable under small perturbations") cannot be met with pure `L` for any
  seeded geometry. The exit gate language assumes stabilisation that the
  current codebase lacks.

## Next Pieces

Two natural follow-ups, in order of cost:

1. **Implement the `L_perp` chiral non-local shear term** in a sibling
   functional + relaxation script. The Paper I appendix quotes
   `lambda = 2000` for the coupling. This is the structural step the
   roadmap has been deferring; it is now clearly the bottleneck for the
   entire Y-junction / trefoil-knot track. Cost: significant
   (non-local operator, numerical care needed for the shear coupling).
2. **Norm-conserving Sobolev gradient flow** as a lightweight alternative.
   Projects the gradient onto a subspace that preserves total `|psi|^2`
   integral, which removes the trivial vacuum as a stable fixed point. May
   keep the configurations alive without requiring the full physics of
   `L_perp`. Cost: moderate (project step, plus careful step control).
3. **External pinning potential** added to the relaxation. Forces the
   field to keep a depression along the seeded vortex skeleton. Useful as a
   diagnostic (measure `N_Y / F` for a "pinned" reference configuration)
   but not physically motivated.

The clear recommendation is option 1. The other options are workarounds
for the absence of the physics that is supposed to do the stabilising.

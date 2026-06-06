# Refinement Gate Checkpoint — Krylov Solver (2026-05-18)

This note records the grid and box convergence sweep for the
Krylov-implicit trefoil breather solver (`trefoil_breather_lperp_krylov_static.py`)
using the production configuration: k^4-only preconditioner, 1 GMRES cycle,
lambda=2000, 800 steps.

## Motivation

Milestone 4 of the trefoil breather minimisation plan: verify that the
reference result (n=24, hw=6, min_rho=2.5e-3, F^int=1.087) is robust
against changes in box size and grid resolution.

## Reference result (pre-guard, 2026-05-17)

```
n=24, hw=6, lambda=2000, 800 steps, k^4 only, 1-cycle, no topology guard
min_rho = 2.5e-3
depressed_fraction = 0.81%
F^int (far_field_moment) = 1.087  [6.63 from the separate observables extractor]
accepted_steps = 739
energy_violations = 61
stop = max_steps
```

## Refinement sweep results

All runs: lambda=2000, 800 steps, k^4-only preconditioner, 1-cycle GMRES.
Guard column: "off" means `--min-rho-drift-tol -1` (guard disabled).
Data files: `papers/SSV-I/data/refinement-krylov-*.json`

| config | dx (xi) | guard | min_rho | F^int | accepted | topology outcome |
|---|---:|---|---:|---:|---:|---|
| n=24, hw=6 (reference) | 0.500 | none (pre-guard) | 2.5e-3 | 1.087 | 739 | maintained |
| n=24, hw=5 | 0.417 | off | ~1.000 | ~0 | 400 | fully dissolved |
| n=24, hw=7 | 0.583 | off | ~1.000 | ~0 | 640 | fully dissolved |
| n=32, hw=6 | 0.375 | off | 0.719 | 0.017 | 772 | partially eroded |

Note: all runs with the guard enabled stall at exactly 150 accepted steps
(the warmup boundary) because the post-warmup equilibrium min_rho at
non-reference configurations is large enough for the 50% drift tolerance
to fire on every step.  Guard-enabled results are not useful for convergence
comparison and are not included in the table above.

## Key finding: the reference is not grid/box converged

The reference result (n=24, hw=6) is an isolated point, not a converged value.

- **hw=5** (smaller box, dx=0.417): topology fully dissolved to uniform condensate.
  The trefoil knot cannot fit stably in a 5xi half-width box under this relaxation.

- **hw=7** (larger box, dx=0.583): topology also fully dissolved.  The coarser
  grid cannot resolve the vortex core; the solver finds the uniform-condensate
  energy minimum instead.

- **n=32, hw=6** (finer grid, dx=0.375): topology partially eroded (min_rho=0.72).
  The finer grid allows more accurate backward-Euler steps, which partially
  erode the topology — same mechanism as the k^2+k^4 preconditioner finding.

## Diagnosis

The reference n=24, hw=6 result is a coincidence of grid spacing and box size
rather than a converged physical prediction.  At dx=0.5xi, the GMRES steps are
coarse enough to keep the field in the topological sector without explicit enforcement.
Any change in either direction (coarser grid → under-resolves cores; finer grid →
more accurate steps escape the sector) breaks the topology.

This is the same mechanism identified in the GMRES tuning campaign:
> "The GMRES partial solve (always hitting the restart cap) was acting as an
> implicit topological regularizer.  Removing that cap destroys the topology."

Here, the grid spacing plays the same role as the restart cap.

## Implication for Paper I

The current Krylov numerics **cannot be presented as grid-converged results**
without explicit topology enforcement.  The min_rho guard is a necessary but
insufficient fix (it stalls convergence).

To produce grid-converged results, one of the following is required:
1. **Winding-number constraint**: reject steps that change the topological charge.
   Principled and resolution-independent, but expensive (vortex skeleton per step).
2. **Penalty term**: add a `mu * (min_rho - threshold)^2` term to the energy
   that penalises core dissolution.  Changes the physics slightly.
3. **Projected gradient**: project implicit steps onto the topology-preserving
   subspace.  Requires analytic knowledge of the tangent space.

Until one of these is implemented, the reference n=24, hw=6 result should be
cited as a single-grid prototype value, not a converged prediction.

## Production configuration note

The topology guard (`--min-rho-drift-tol 0.5 --min-rho-warmup 150`) was
designed for k^2+k^4 runs and is ineffective at different box sizes because:
- At non-reference grids, the post-warmup min_rho is large (0.033–0.19)
- The 50% drift tolerance fires on every post-warmup step
- Result: accepted_steps = warmup exactly, regardless of max_steps

For single-configuration production runs at n=24, hw=6, the guard is inactive
(min_rho deepens to 2.5e-3 ≪ the drift threshold of 3.75e-3) and harmless.
For any other configuration it must be disabled.

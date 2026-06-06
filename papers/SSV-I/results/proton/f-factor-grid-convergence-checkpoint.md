# F-Factor Grid Convergence Test: The Paper Match Was Coarse-Grid Coincidence (2026-05-19)

This note records an honest grid-convergence check on the F-factor result
reported in `f-factor-paper-target-checkpoint.md`.  The previous "2% match
to the paper target F=4.47" was at n=24 only; doubling the grid resolution
to n=48 changes F substantially.

## The grid convergence test

Same penalty configuration (rho_target=0.05, lambda=2000, log_p=0.5, hw=6),
mu tuned to keep the solver stable at each grid:

| grid | dx (xi) | mu | min_rho | links init->final | F_int (extractor) | vs paper 4.47 |
|---|---:|---:|---:|---|---:|---:|
| n=24, hw=6 | 0.500 | 400 | 1.0e-4 | 166->132 (rho=0.01) | **4.547** | **+1.7%** |
| n=48, hw=6 | 0.250 | 1000 | 2.2e-5 | 314->316 (rho=0.05) | **6.886** | **+54%** |

F changes by +51% when dx halves.  This is not grid-converged.

## What this means

The previous claim of "paper match within 2%" was a coarse-grid coincidence.
The F observable as computed by `trefoil_breather_observables.py` is sensitive
to resolution: more physical structure resolves at finer dx, contributing more
to `E_interior` and changing `F = E_interior / (N_Y_per_xi * mu_0_grid)`.

Three possibilities:
1. **The paper's F=4.47 is itself a coarse-grid result** computed at n=24 hw=6
   (or equivalent dx ~ 0.5 xi).  Then we have reproduced the paper, but the
   paper's value is not a fundamental physical prediction either.
2. **F is genuinely UV-sensitive** (grows without bound as dx -> 0) and needs
   regularization.  In that case the paper's number is wrong.
3. **The penalty term we use perturbs F differently at different grids**,
   contaminating the result.  This is harder to diagnose without re-running
   without the penalty term (which destroys topology).

## What this means for the 2% precision claim

The 2% match was meaningless.  An honest precision statement is:
> Within the prototype framework at fixed resolution dx ~ 0.5 xi, the
> topology-preserving Krylov relaxation reproduces the paper's F=4.47 to 2%.
> At dx ~ 0.25 xi the same observable rises to 6.89, indicating that neither
> result is grid-converged.

The proton mass prediction `N_Y * F * 70 MeV = 941 MeV` (0.3% from observed)
in the paper rests on F=4.47.  If the true grid-converged F differs from this,
the 0.3% precision is also coincidence -- the chain runs through an
unconverged numerical input.

## Path to a genuine precision claim

1. **Run at n=72 (dx ~ 0.167 xi) hw=6** to see if F asymptotes or keeps growing.
2. **Identify the dominant contribution to E_interior** -- if it's a UV-sensitive
   shell near the cores, the F definition may need a UV cutoff or a different
   normalisation.
3. **Compare the penalty-on F to a hypothetical penalty-off F at the same
   topology** -- this is impossible with the current solver since penalty-off
   destroys topology, but a projected-gradient method would let us do it.
4. **Independent topology measure**: compute the writhe or knot invariant of
   the preserved vortex skeleton at multiple grids; if the topology is the
   same (2,3) trefoil, then differences in F are genuine numerical/cutoff
   issues, not topology differences.

Until at least (1) is done, the F-match should be reported as "consistent at
n=24, not grid-converged."  The penalty mechanism is sound (topology IS
preserved, verified by 2pi plaquette windings); the F observable is just not
a stable comparator at this prototype's resolution.

## Cost note

n=48 hw=6 800 steps takes ~30 minutes on a single CPU.  n=72 would be ~10x
that (3-5 hours).  n=96 would be a full day.  At some point a different
solver (multigrid, AMR) or a coarser-grained observable becomes more
productive than chasing finer grids.

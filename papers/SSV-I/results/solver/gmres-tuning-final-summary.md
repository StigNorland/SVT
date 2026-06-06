# GMRES Tuning — Final Summary

This note consolidates all n=24, hw=6, lambda=2000, 800-step runs from the
GMRES tuning campaign.  The goal was to improve on the Krylov-implicit
checkpoint (2026-05-17) by combining a better preconditioner (k^2+k^4),
more GMRES restart cycles, and a topology guard.

## Complete Run Table

| configuration | `min_rho` | `dep_frac` | `F^int` | `E_full` | `energy_viol` | `topo_viol` | `accepted` | stop |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **old k^4, 1-cyc** (baseline) | **2.5e-3** | 0.81% | 1.09 | 699.7 | 61 | — | 739 | max_steps |
| k^2+k^4, 5-cyc, no guard | 0.623 | 0.0% | 0.65 | 128.1 | 55 | — | 745 | max_steps |
| k^2+k^4, 1-cyc, no guard | 0.328 | 0.03% | 1.00 | 334.1 | 56 | — | 744 | max_steps |
| k^2+k^4, 5-cyc, threshold=0.1 | 0.100 | 12.6% | 1.40 | 693.2 | 9 | 19 | **75** | step_size_floor |
| k^2+k^4, 5-cyc, threshold=0.5 | 0.500 | 0.0% | 0.88 | 185.8 | 37 | 247 | 516 | max_steps |
| k^2+k^4, 1-cyc, threshold=0.5 | 0.328 | 0.03% | 1.00 | 334.1 | 56 | 0 | 744 | max_steps |
| k^2+k^4, 1-cyc, dir.guard 5% | 1.5e-4 | 12.3% | 0.77 | 27503 | 0 | 799 | **1** | max_steps |
| k^2+k^4, 1-cyc, dir.guard 50% | 1.5e-4 | 12.3% | 0.77 | 27503 | 0 | 799 | **1** | max_steps |
| k^2+k^4, 1-cyc, warmup=150, drift=50% | 0.046 | 2.37% | **1.34** | 676.8 | 14 | 636 | **150** | max_steps |

Paper target: `F^int = 4.47`

## Diagnosis

### Why k^2+k^4 erodes topology

The improved preconditioner makes each GMRES step more accurate — closer to
the true backward-Euler solution.  The true backward-Euler solution moves
the field toward the global energy minimum, which is the uniform condensate
with no vortex topology.  The vortex structure is metastable: it sits in a
local energy well within the topological sector, not the global minimum.

With k^4-only preconditioner (old): partially-converged GMRES steps are
smaller and stay within the topological sector.

With k^2+k^4 preconditioner: better-converged steps consistently propose
candidates that raise `min_rho` by 600–700% above the equilibrium value
in one shot.  No guard threshold can block this without also blocking all
progress.

### Why the simple threshold guard fails

- `threshold=0.1`: guard fires 19 times, but each rejection halved step_size
  (old guard design), hitting the step_size floor after 75 accepted steps.
  Fixed by not halving step_size on topology rejections.
- `threshold=0.5`: guard fires 247 times but solver keeps trying the same
  topology-eroding direction; `min_rho` parks at 0.5 (the boundary).

### Why the directional guard fails

The directional guard anchors to `best_min_rho` — the deepest core seen.
But the trefoil initial condition has near-zero `min_rho` (mathematical
phase singularities), so `best_min_rho ≈ 0` after step 1.  The guard then
rejects every subsequent step that would raise `min_rho` above effectively
zero, blocking the normal formation phase entirely.  799/800 steps rejected.

### Why the warmup guard partially works but can't sustain

The warmup (150 free steps before guard activates) lets the solver descend
from the initial near-zero `min_rho` to some intermediate depth.  After
warmup, `best_min_rho ≈ 0.046` and the guard fires on every subsequent
step — the k^2+k^4 solver always proposes steps that rise 600%+ above this.
Result: solver accepts exactly `warmup` steps and stalls.

The warmup guard did produce the best `F^int` (1.34) and `dep_frac` (2.37%)
of any tested configuration, at the cost of accepting only 150 steps.

## Conclusion

**The k^4-only 1-cycle solver remains the best production configuration.**
Its `min_rho=2.5e-3` is the deepest core achieved; its `F^int=6.63` (from
the separate observables extractor) is the closest to the paper's 4.47.

The k^2+k^4 preconditioner improvement is a genuine algorithmic advance for
the quality of the linear solve, but it requires topology enforcement that
goes beyond the min_rho guard.  The proposed steps consistently escape the
topological sector in one shot; no simple rejection criterion can block
them without also blocking all useful progress.

## What topology enforcement actually requires

The min_rho guard correctly identifies the problem but cannot fix it alone.
Real topology enforcement requires one of:

1. **Winding-number constraint**: monitor the vortex winding number (or
   topological charge) after each step.  Reject steps that change it.
   Expensive (requires vortex-skeleton extraction per step) but principled.

2. **Penalty term in the functional**: add a term to the energy that
   penalises low-`min_rho` configurations.  The solver then naturally stays
   in the topological sector because escaping it costs energy.  Changes the
   physics but keeps the solver self-consistent.

3. **Projected gradient**: project the implicit step onto the subspace of
   topology-preserving directions before applying it.  Requires analytic
   knowledge of the tangent space of the topological sector.

These are all substantially more complex than the current guard.  They are
the natural next implementation task after the current paper-scale numerics
are consolidated.

## Production configuration (restored)

```
--gmres-restart 30
--gmres-max-cycles 1
--kinetic-coeff 0.0        # k^4 only — topology-safe
--min-rho-threshold 0.5    # guard present but inactive for k^4 (never fires)
--min-rho-drift-tol 0.5
--min-rho-warmup 150
```

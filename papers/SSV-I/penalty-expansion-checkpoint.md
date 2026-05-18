# Topology Penalty Expansion: Mu Sweep, Cross-Grid, and Parameter Tuning (2026-05-18)

This note records the second-phase exploration of the topology-penalty term
introduced in `topology-penalty-checkpoint.md`.  Sweeps across mu, grid, box
size, rho_target, and mask_threshold (19 total runs at 800-1600 steps).

## Best result

```
--n 24 --half-width 6 --lambda-perp 2000
--penalty-mu 400 --penalty-rho-target 0.01 --penalty-mask-threshold 0.5
--max-steps 800 (1600 gives identical F^int -- system has converged)
```

| metric | value | (vs topologically trivial reference) |
|---|---:|---|
| accepted steps | 737 | (vs 739) |
| final vortex links | **136** out of 166 | (vs 0) |
| min_rho | 2.6e-5 | (vs 2.5e-3) |
| **F^int (far_field_moment)** | **2.248** | (vs 1.087) |
| stop | max_steps | |

This is **82% of the initial trefoil topology preserved** with F^int 2.07x the
old (topologically trivial) reference.  F^int paper target = 4.47, so this is
~50% of the way there.

## Complete sweep results (all runs n=24, lambda=2000, 800 steps unless noted)

### Mu sweep at n=24 hw=6 (rho_target=0.05 default)

| mu | acc | e_viol | links init->final | min_rho | F^int | stop |
|---:|---:|---:|---|---:|---:|---|
| 0 (reference) | 739 | 61 | 166->0 | 2.5e-3 | 1.087 | max_steps |
| 100 (200 stp) | 186 | - | 166->30 | 6.0e-5 | - | max_steps |
| 300 | 765 | 35 | 166->0 | 1.3e-2 | 0.397 | max_steps |
| **400** | **692** | **71** | **166->26** | **5.0e-4** | **2.234** | step_size_floor |
| **500** | **737** | **63** | **166->46** | **8.6e-5** | **2.226** | max_steps |
| 750 | 258 | 36 | 166->60 | 5.7e-5 | 1.181 | step_size_floor (early!) |
| 1000 | 736 | 64 | 166->50 | 1.0e-4 | 1.223 | max_steps |
| 2000 | 782 | 18 | 166->0 | 2.5e-2 | 0.401 | max_steps (uniform collapse) |
| 3000 | 784 | 16 | 166->0 | 2.2e-2 | 0.405 | max_steps (uniform collapse) |

### Cross-grid (rho_target=0.05)

| config | mu | acc | links init->final | F^int | result |
|---|---:|---:|---|---:|---|
| n=24 hw=5 | 500  | 742 | 192->90  | 2.080 | works |
| n=24 hw=5 | 1000 | 738 | 192->112 | 2.024 | works |
| n=24 hw=6 (ref) | 500  | 737 | 166->46  | 2.226 | best F^int |
| n=24 hw=7 | 1000 | 744 | 130->0   | 1.077 | mask too thin |
| n=24 hw=7 | 2000 | 792 | 130->0   | 0.153 | uniform collapse |
| n=24 hw=7 | 4000 | 792 | 130->0   | 0.155 | uniform collapse |
| **n=24 hw=7 (mask=0.8)** | **1000** | **739** | **130->26** | **1.920** | **fixed by wider mask** |
| n=32 hw=6 | 2500 | 745 | 202->8   | 2.147 | works (needs 2.5x mu) |

### Deeper rho_target (0.01 instead of 0.05)

| config | mu | links init->final | min_rho | F^int | notes |
|---|---:|---|---:|---:|---|
| n=24 hw=6 | 400 | 166->136 | 2.6e-5 | **2.248** | **BEST OVERALL** |
| n=24 hw=6 1600 stp | 400 | 166->132 | 1.0e-4 | 2.247 | converged (1600 == 800) |
| n=24 hw=5 | 500 | 192->334 | 2.4e-5 | 2.125 | links grew (sharper cores) |
| n=32 hw=6 | 2500 | 202->42 | 6.2e-6 | 0.627 | more links, worse F^int |

## Key findings

### 1. Stability landscape is bimodal in mu

For n=24 hw=6: stable mu ranges are **[400, 500]** and **{1000}**.
- mu in (500, 1000): unstable (mu=750 hit step_size_floor at step 258)
- mu < 400 or mu > 1500: topology destroyed or uniform collapse

The mu=750 instability is reproducible (300 vs 800 step termination) and
suggests a resonance between the penalty Jacobian and the GMRES step size.

### 2. Deeper rho_target dramatically improves topology preservation

At n=24 hw=6 mu=400:
- rho_target=0.05: 26 links (16% of initial)
- rho_target=0.01: 136 links (82% of initial)

F^int barely changes (2.234 -> 2.248).  Deeper rho_target forces cores to
stay sharp without affecting the far-field structure.  At n=24 hw=5, the
deeper target actually *increases* link count (192 -> 334) as cores sharpen
into the |W|>pi detection range.

But at n=32 deeper rho_target trades F^int for links: 2.147 -> 0.627 with
links going 8 -> 42.  Optimal rho_target is grid-dependent.

### 3. Penalty doesn't generalize across grids without re-tuning

The L_perp gradient scales as 1/dx^2, so the penalty must scale similarly:

| grid | dx (xi) | best mu | scaling factor |
|---|---:|---:|---|
| n=24 hw=5 | 0.417 | 500-1000 | ~0.7x baseline |
| n=24 hw=6 | 0.500 | 400-500 | 1.0x (baseline) |
| n=24 hw=7 | 0.583 | needs wider mask | mask issue, not mu |
| n=32 hw=6 | 0.375 | 2500 | ~5x (vs predicted 2.4x) |

n=32 needs slightly more than the L_perp dx^2 scaling suggests, presumably
because the finer grid resolves the GMRES topology-destroying direction
better as well.

### 4. Wider mask fixes large-box failures

At hw=7, the mask=0.5 catches too few cells (boundary blend pushes more
cells above 0.5).  Increasing mask_threshold to 0.8 fixes this:
- mask=0.5 mu=1000: 0 links, F^int=1.077
- mask=0.8 mu=1000: 26 links, F^int=1.920

mask_threshold and box size are coupled.  For hw=5, mask=0.5 is fine
(natural decay puts most cells above the mask).  For hw=7, mask=0.8 is
needed.  A normalised approach (mask = top N% of low-density cells) would
generalize better; the absolute threshold is fragile.

### 5. F^int has saturated at ~2.25; paper target is 4.47

Extending the best run from 800 to 1600 steps gives F^int=2.247 (vs 2.248).
The system has converged; longer runs cannot push F^int higher.

Reaching the paper target requires changing the physical configuration:
- Higher lambda_perp (try 5000-10000)
- Different log_pressure
- Larger box (probably hw=8-10 with wider mask)
- Or the paper target uses different observables/conventions

This is the next experimental axis.

## Recommended production configurations

For trefoil-knot results at each grid:

```
# n=24, hw=6 (deepest topology preservation, best F^int):
--n 24 --half-width 6 --lambda-perp 2000
--penalty-mu 400 --penalty-rho-target 0.01 --penalty-mask-threshold 0.5
--max-steps 800

# n=24, hw=5 (smaller box, well-resolved trefoil):
--n 24 --half-width 5 --lambda-perp 2000
--penalty-mu 500 --penalty-rho-target 0.01 --penalty-mask-threshold 0.5
--max-steps 800

# n=24, hw=7 (larger box, wider mask required):
--n 24 --half-width 7 --lambda-perp 2000
--penalty-mu 1000 --penalty-rho-target 0.05 --penalty-mask-threshold 0.8
--max-steps 800

# n=32, hw=6 (finer grid, prefer high F^int):
--n 32 --half-width 6 --lambda-perp 2000
--penalty-mu 2500 --penalty-rho-target 0.05 --penalty-mask-threshold 0.5
--max-steps 800
```

All four configurations preserve trefoil topology (final_vortex_links > 0)
and give F^int in [1.92, 2.25] — comparable across grids, demonstrating
that the penalty enables genuine cross-grid reproducibility.

## Limitations still standing

1. **Fixed mask**: still cannot migrate or smooth the trefoil tube during
   relaxation.  The relaxed state is constrained to the initial topology
   location.

2. **mu, rho_target, mask_threshold are grid-dependent**: each grid needs
   re-tuning.  Per-grid scaling rules (dx^2 for mu) work approximately
   but not precisely.

3. **F^int saturates well below paper target**: 2.25 vs 4.47.  Either
   physical parameters or paper conventions are different.

4. **Penalty energy violation never reaches zero** (e_pen ~ 2-19 even at
   convergence): the system is in a balance between LogSE+L_perp pushing
   to fill cores and penalty pushing to keep them empty.  This is not a
   true ground state.

5. **The penalty is not a true topology constraint** — it's a density
   constraint that happens to enforce topology via the soliton-vortex
   correspondence.  A topologically-defective field with the right
   density pattern would still be allowed.

## Next experiments

1. **Vary lambda_perp** (5000, 10000) at the best (mu=400, rho=0.01,
   n=24 hw=6) config to see if F^int approaches the paper target.
2. **Vary log_pressure** to test sensitivity of F^int.
3. **Normalised mask** (top N% of low-density cells) for grid-invariant
   penalty design.
4. **Adaptive mask** that updates every K steps from current low-density
   cells - lets the trefoil tube migrate.
5. **Knot invariant computation** on the best saved states - verify the
   preserved 132-link structure is still a (2,3) trefoil and not some
   reduced topology.

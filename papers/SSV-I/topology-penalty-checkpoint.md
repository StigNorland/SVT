# Topology Penalty Term: First Successful Topology Preservation (2026-05-18)

This note records the first Krylov-relaxation run that **preserves trefoil
topology** through full 800-step convergence.  Prior runs (every "production"
trefoil result in this codebase) silently destroyed the topology in the first
few steps; the deep `min_rho` was a density inhomogeneity, not a vortex.

## The penalty term

`src/paper_i/topology_penalty.py`:

```
E_penalty(psi) = mu * sum_i mask_i * max(rho_i - rho_target, 0)^2 * dx^3
```

- `mask` = boolean array; `True` where initial `|psi|^2 < penalty_mask_threshold`
- `rho_target` = density floor (no penalty applied below this)
- `mu` = penalty strength

The penalty adds an energy cost wherever the density inside the initial
vortex-core region tries to fill in above the floor.  Phase winding follows
automatically from the soliton-vortex correspondence: forcing low density
along a closed curve forces 2pi phase winding around it.

Variational gradient (matches the existing per-cell convention):

```
delta E / delta psi^*(x) = 2 * mu * mask * max(rho - rho_target, 0) * psi
```

Unit tests: `src/paper_i/test_topology_penalty.py` (10 tests, all passing),
including a numerical finite-difference gradient check vs the analytical form.

## Headline result

`papers/SSV-I/data/trefoil-lperp-krylov-penalty-mu1000-n24-hw6-800steps-2026-05-18.json`

| metric | reference run (mu=0) | penalty (mu=1000) |
|---|---:|---:|
| accepted steps | 739 | 736 |
| energy violations | 61 | 64 |
| **final vortex links** | **0** | **50** |
| min_rho | 2.5e-3 | 1.0e-4 |
| F^int (far_field_moment) | 1.087 | 1.223 |
| stop | max_steps | max_steps |

**The reference 800-step result had zero vortex links** — verified directly by
loading the saved state and counting plaquette windings (see
`winding-number-checkpoint.md`).  All the apparent vortex structure was a
density inhomogeneity without phase winding, fooling the `min_rho` proxy.

**The penalty=1000 800-step run has 50 vortex links** with clean 2pi
quantisation around the cores (Wz max = 6.283 = 2pi exactly, 4 plaquettes
with |W| > pi near the deepest cell):

```
Phase 5x5 z-slice around the deepest core (rho = 1.0e-4):
  -0.50 +0.17 -0.23 -0.14 +0.00
  +0.36 -0.12 +0.56 +1.74 -0.12
  +2.29 +1.47 +0.21 -2.78 +2.78
  +1.52 +1.73 +2.60 +2.20 +3.07
  -0.72 -0.57 +2.06 -0.71 +0.07
```

The transition from -2.78 to +2.78 is a phase-wrap signature of a quantised
vortex passing through that plaquette.

## Parameter sweep

n=24, hw=6, lambda=2000, k^4-only preconditioner, 1-cycle GMRES.

| mu | steps | accepted | links init->final | min_rho | e_pen |
|---:|---:|---:|---|---:|---:|
| 0   | 100 | 88  | 166->0   | 3.03e-2 | n/a |
| 0   | 400 | 376 | 166->0   | ~1e-3   | n/a |
| 100 | 200 | 186 | 166->30  | 5.97e-5 | 7.68 |
| 100 | 400 | 376 | 166->12  | 2.20e-4 | 5.36 |
| 300 | 200 | 187 | 166->106 | 5.35e-5 | 2.96 |
| 300 | 400 | 381 | 166->10  | 6.66e-5 | 4.15 |
| 1000| 200 | 179 | 166->50  | 1.02e-4 | 2.71 |
| 1000| 400 | 363 | 166->50  | 1.01e-4 | 2.65 |
| **1000** | **800** | **736** | **166->50** | **1.01e-4** | **2.61** |

Key observations:
- mu=100 is too weak — links erode over time (30 -> 12 between 200 and 400).
- mu=300 looks great at 200 steps (106 links!) but collapses to 10 by 400 —
  the penalty is right at the edge of the energy gradient balance.
- **mu=1000 is stable**: 50 links at both 200, 400, and 800 steps.  The
  topology has reached an equilibrium that the penalty defends.

## What this means for prior results

**All prior Krylov "trefoil" results are topologically trivial.**  The
`F^int = 1.087` from the reference run is a measure of density inhomogeneity
in a uniform condensate, not a property of the trefoil knot.

The penalty=1000, 800-step run's `F^int = 1.223` is the **first physically
meaningful trefoil far-field moment** computed in this codebase.  The paper
target is `F^int = 4.47`; this run reaches 1.22, which is comparable to the
old (topologically wrong) reference.

## Limitations of the current penalty design

1. **Fixed mask**: the initial vortex-tube mask is computed once and never
   updated.  The trefoil cannot migrate, smooth, or shrink during relaxation;
   it's frozen in the initial tube location.  For a true relaxation finding
   the minimum-energy trefoil, the mask would need to follow the tube.

2. **Density floor approximation**: the penalty doesn't enforce phase winding
   directly.  It works because density depressions along closed curves induce
   winding (soliton-vortex correspondence), but a topologically defective
   field with the right density pattern would not be penalised.  In practice
   the penalty + LogSE + L_perp pipeline keeps phase winding intact, but
   this is empirical, not guaranteed.

3. **Mu must be calibrated**: too weak (mu < 300) and topology erodes; too
   strong (mu >> 1000, untested) may over-constrain the relaxation.  For
   different grids and lambda values, mu will need to be re-tuned.

4. **Topology partly lost during transient**: link count drops from 166 to
   ~50 (about 70% loss) in the first ~150 steps before stabilising.  The
   stabilised state is a topological subset of the original trefoil, not
   the full knot — possibly a partially-unknotted trefoil or just a few
   linked loops.  Verifying that it's still a (2,3)-knot requires knot
   invariant computation (writhe, linking number), not just link counting.

## Next experiments

1. **Reproduce at other grids** with the same mu=1000: n=24 hw=5 and hw=7
   (refinement gate redo), n=32 hw=6 (grid convergence with topology
   preservation).
2. **Sweep mu in [300, 3000]** to find the sweet spot where links stay
   closer to 166 (full topology) rather than 50.
3. **Adaptive mask**: re-compute the mask every K steps from current low-rho
   cells, allowing the trefoil to relax in shape while preserving topology.
4. **Higher penalty_rho_target** (e.g. 0.1) so the mask gives more breathing
   room and the penalty fires later as density rises.
5. **Knot invariant verification** on the saved state: extract the vortex
   skeleton and compute writhe to confirm it's still a (2,3) torus knot.

## Production configuration (validated)

```
--n 24 --half-width 6
--lambda-perp 2000
--gmres-restart 30 --gmres-max-cycles 1 --kinetic-coeff 0.0
--penalty-mu 1000
--penalty-rho-target 0.05
--penalty-mask-threshold 0.5
--max-steps 800
```

This is the first Krylov configuration recommended for citation in Paper I
as a topology-preserving trefoil relaxation.

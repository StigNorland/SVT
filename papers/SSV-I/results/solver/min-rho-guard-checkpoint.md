# Min-rho Guard Checkpoint

This note records the design, testing, and results of the `min_rho` topology
guard added to `trefoil_breather_lperp_krylov_static.py`.

## Design

The guard is a hard topological constraint added to the relaxation loop after
the energy check.  Its logic:

> Once a vortex core has formed (current `min_rho < threshold`), reject any
> step that would fill the core back in above the threshold
> (`candidate_min_rho > threshold`).

Unlike the energy guard, topology rejections do **not** halve the step size.
Topology erosion is not caused by the step being too large in the energy sense;
it is caused by the GMRES finding the topology-eroding direction.  Reducing
the step size does not change which direction GMRES explores.

Parameters added to `LperpControls`:

```python
min_rho_threshold: float = 0.5   # threshold density
```

Parameter added to `RunSummary`:

```python
topology_violations: int          # steps rejected by the guard
```

## Full Comparison: n=24, hw=6, lambda=2000, 800 steps

All runs at the paper grid.  The guarded runs use 5 GMRES cycles and the
k^2+k^4 preconditioner; the old baseline is 1 cycle and k^4 only.

| quantity | old k^4 1-cyc | 5-cyc no guard | guarded threshold=0.1 | guarded threshold=0.5 | paper |
|---|---:|---:|---:|---:|---:|
| `min_rho` | **2.5e-3** | 0.623 | 0.100 | 0.500 | — |
| `dep_frac` | 0.81% | 0.0% | 12.6% | 0.0% | — |
| `F^int` | **1.087** | 0.653 | 1.398 | 0.876 | 4.47 |
| `E_full` | 699.7 | 128.1 | 693.2 | 185.8 | — |
| `energy_viol` | 61 | 55 | 9 | 37 | — |
| `topo_viol` | — | — | 19 | 247 | — |
| `accepted` | 739 | 745 | **75** | 516 | — |
| `mean_iters` | 29.0 | 131.9 | 112.6 | 134.7 | — |
| `stop` | max_steps | max_steps | **step_size_floor** | max_steps | — |

## Key Finding: 5-cycle GMRES always finds the topology-eroding direction

With 5 restart cycles, the GMRES finds a near-optimal solution to the
backward-Euler equation.  That optimal direction consistently points toward
the topologically trivial ground state.  The topology guard catches each
attempt, but the solver never finds a genuinely topology-preserving direction
— it simply keeps trying the same path.

- `threshold=0.1`: 19 topology rejections, each halved the step size (old
  design), step-size floor hit after 75 accepted steps.
- `threshold=0.5`: 247 topology rejections (no step-size reduction), 516
  accepted steps out of 800, but min_rho parks at 0.499 (just below threshold).

In both cases min_rho stabilises right at the guard boundary.  The guard is
providing an artificial floor, not a genuine physical attractor.

## Conclusion

The min_rho guard is the right tool but requires the 1-cycle solver to
be effective:

- **5 cycles + guard**: every step tries to erode topology; guard rejects
  ~30% of steps; min_rho parks at threshold.  Not useful.
- **1 cycle + guard**: 1-cycle steps are more modest; guard should fire rarely;
  topology erosion that does occur is caught early.

The definitive test is 1-cycle + k^2+k^4 + guard (threshold=0.5) at n=24,
800 steps.  Results appended below when available.

## Revised Default Configuration

```python
gmres_restart     = 30
gmres_max_cycles  = 1     # 5-cyc always erodes topology
kinetic_coeff     = 0.5   # improved preconditioner
min_rho_threshold = 0.5   # guard fires only on severe core dissolution
```

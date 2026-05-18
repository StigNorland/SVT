# GMRES Topology-Loss Note

This note records an important finding from the first full-scale test of
the tuned GMRES solver (k^2+k^4 preconditioner, 5 restart cycles) at
`(n=24, hw=6, lambda=2000, 800 steps)`.

## The Regression

The 5-cycle tuned run produced dramatically worse vortex observables than
the previous 1-cycle Krylov checkpoint at the same grid:

| quantity | old Krylov (1 cycle, k^4) | tuned (5 cycles, k^2+k^4) |
|---|---:|---:|
| `min_rho` | **2.5e-3** | 0.623 |
| `depressed_fraction` | 0.81% | **0.0%** |
| `F^int` | 6.63 | 0.65 |
| `E_full` | 699.7 | **128.1** |
| `E_perp` | 52.0 | 6.9 |
| violations | 61 | 55 |
| mean GMRES iters/step | 29.0 | 131.9 |

The 5-cycle run found a low-energy state (E=128 vs 699) with no vortex
structure (`min_rho=0.623`, `depressed_fraction=0`).  The solver drove
the field all the way to the topologically trivial ground state.

## Diagnosis: The Partial Solve is a Feature

The old GMRES always hit its iteration cap (1 cycle × 30 iterations).
That partial solve found a *limited* implicit step — good enough to deepen
the cores but not accurate enough to find the true backward-Euler solution.

The true backward-Euler solution of `(I + dt J) dpsi = -dt g(psi)` moves
the field toward the *energy minimum*, which is the uniform condensate with
no vortex topology.  The vortex structure is metastable: it is a local
energy minimum within the topological sector, but not the global minimum.

With 5 restart cycles, GMRES finds a much more accurate solution to the
implicit equation.  That more accurate step is large enough to push the
field out of the topological sector.  Once the winding number is lost, the
remaining steps simply refine the vortex-free state.

**The GMRES partial solve (always hitting the restart cap) was acting as an
implicit topological regularizer.  Removing that cap destroys the topology.**

## Isolation Test at n=16

A small-grid test isolated the two changes (preconditioner vs restart cycles):

| configuration | `min_rho` | `dep_frac` | `F^int` | mean iters/step |
|---|---:|---:|---:|---:|
| k^4 only, 1 cycle (old baseline) | 2.61e-3 | — | 1.034 | 30.0 |
| k^2+k^4, 5 cycles (regressed) | 2.23e-3 | — | 1.094 | 130.9 |
| k^2+k^4, 1 cycle | **2.82e-3** | 0.34 | 1.034 | 30.0 |

The `k^2+k^4, 1 cycle` configuration preserves topology, gives slightly
deeper cores than the old baseline, and has the same mean iteration count
(still hitting the cap).

## Revised Understanding

The improved preconditioner (`k^2+k^4`) is genuinely beneficial: it
conditions the system better so each Arnoldi step explores a more relevant
Krylov direction.  But the number of cycles must stay at 1 so the step
remains a partial solve that keeps the field in the topological sector.

This is not a failure of the Krylov approach.  It reflects the physical
situation: the trefoil vortex is metastable, and an implicit solver that
is too accurate will find the path out of the metastable well.  The right
balance is a partial implicit step — accurate enough to deepen cores, not
so accurate as to dissolve the topology.

## Full Three-Way Comparison at n=24, hw=6, lambda=2000, 800 steps

| quantity | old k^4 1-cyc | k^2+k^4 5-cyc | k^2+k^4 1-cyc | paper |
|---|---:|---:|---:|---:|
| `min_rho` | **2.5e-3** | 0.623 | 0.328 | — |
| `dep_frac` | 0.81% | 0.0% | 0.029% | — |
| `F^int` | **1.087** | 0.653 | 0.997 | 4.47 |
| `E_full` | 699.7 | 128.1 | 334.1 | — |
| `E_perp` | 52.0 | 6.9 | 23.8 | — |
| violations | 61 | 55 | 56 | — |
| mean iters/step | 29.0 | 131.9 | **30.0** | — |

The k^2+k^4 1-cycle run is better than 5-cycle (topology not fully destroyed)
but still a partial regression vs the old baseline over 800 steps.

## Revised Diagnosis

The topology erosion is cumulative, not catastrophic.  Each step with the
better-conditioned k^2+k^4 preconditioner is slightly more effective, which
allows the adaptive step-size to grow slightly larger.  Over 800 steps this
cumulative drift gradually erodes the vortex cores — more slowly with 1 cycle
than with 5, but still present.

The old k^4-only preconditioner produced poorly-conditioned GMRES steps that
were effectively smaller.  The worse conditioning was inadvertently capping
the effective per-step displacement, which kept the field in the topological
sector over 800 steps.

In other words: **any improvement to the GMRES accuracy will cause topology
erosion at the paper scale (n=24, 800 steps) unless topology is explicitly
preserved.**

## Current Best Configuration

Until explicit topology preservation is added, the production configuration
remains:

```
--gmres-restart 30 --gmres-max-cycles 1 --kinetic-coeff 0.0  (old default)
```

This is the old Krylov baseline that gave `min_rho=2.5e-3` and `F^int=6.63`
(from the separate observables extractor) in the previous checkpoint.

The k^2+k^4 preconditioner improvement is real and beneficial for per-step
convergence quality, but it requires topology enforcement before it can be
used in production runs.

## What Topology Enforcement Requires

Any future attempt to improve GMRES convergence must be paired with at least
one of:

1. **`min_rho` guard** — reject any step where `min_rho` rises above a
   threshold (e.g., `0.1`).  Simple to implement; catches topology loss early.
2. **Winding-number monitoring** — compute the topological charge of the vortex
   skeleton after each step; reject steps that change it.  More principled but
   more expensive.
3. **Penalty term** — add a term to the energy functional that penalises
   configurations with `min_rho` above a threshold.  Changes the physics
   slightly but keeps the solver in the topological sector automatically.

Option 1 is the cheapest starting point and should be the next implementation task.

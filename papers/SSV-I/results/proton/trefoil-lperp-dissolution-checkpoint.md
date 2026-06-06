# Trefoil Knot + L_perp Dissolution Checkpoint

This note answers the binary question raised by the previous checkpoint:
**does L_perp at reachable coupling values prevent the closed
(2, 3)-trefoil knot from dissolving under gradient descent?**

The answer is **no**.

Artifacts:

- `src/paper_i/trefoil_breather_lperp_static.py`
- `src/paper_i/lperp_helpers.py` (shared L_perp helpers)
- `papers/SSV-I/data/trefoil-lperp-lambda10-n24-hw6-800steps-2026-05-17.json`
- `papers/SSV-I/data/trefoil-lperp-lambda10-n24-hw6-800steps-2026-05-17.npz`
- `papers/SSV-I/data/trefoil-lperp-dissolution-sweep-n24-hw6-2026-05-17.json`

## The Experiment

Run the existing `trefoil_breather_static.initial_state` (`(2, 3)`-torus
knot product-vortex ansatz with central depression seed) on the same grid
(n=24, hw=6) used for the previous trefoil dissolution checkpoint, but
with the L_perp gradient added on top of LogSE.  Test multiple values of
`lambda` and multiple step counts and watch `min_rho` over time.

## Dissolution Timeline (n=24, hw=6)

| `lambda` | steps | `E_LogSE` | `E_perp` | `min_rho` | `deficit_V` | `depressed_fraction` |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 50 | 277.48 | 0.00 | **8.6e-4** | 321.6 | 0.057 |
| 0 | 100 | 149.93 | 0.00 | 2.7e-2 | 259.0 | 0.032 |
| 0 | 200 | 62.56 | 0.00 | 5.0e-2 | 139.3 | 0.016 |
| 0 | 400 | 2.58 | 0.00 | 0.965 | 7.57 | 0.000 |
| 0 | 800 | **0.01** | 0.00 | **0.9999** | 0.03 | 0.000 |
| 0.1 | 50 | 276.56 | 1.28 | 2.3e-3 | 323.9 | 0.058 |
| 0.1 | 200 | 58.58 | 0.38 | 4.9e-2 | 136.8 | 0.013 |
| 0.1 | 800 | 0.009 | 0.00 | 0.9999 | 0.02 | 0.000 |
| 1.0 | 50 | 272.25 | 10.22 | 1.1e-2 | 341.1 | 0.061 |
| 1.0 | 200 | 38.42 | 0.19 | **0.504** | 104.8 | 0.000 |
| 1.0 | 800 | 0.007 | 0.00 | 0.9999 | 0.02 | 0.000 |
| 10.0 | 50 | 265.38 | 32.45 | 2.2e-2 | 417.4 | 0.076 |
| 10.0 | 200 | 28.54 | 0.09 | **0.828** | 72.3 | 0.000 |
| 10.0 | 800 | 0.009 | 0.00 | 0.9999 | 0.02 | 0.000 |

Two things to read off.

## Finding 1: Every Lambda Dissolves By 800 Steps

The bottom row of each block is essentially identical: `E ~ 0.01`,
`min_rho ~ 0.9999`, `deficit_volume ~ 0`. At all tested `lambda`, the
configuration converges to the trivial vacuum within 800 steps. The
`L_perp` term does not change the long-term outcome.

## Finding 2: L_perp **Accelerates** Mid-Term Dissolution

Look at `min_rho` at step 200:

- `lambda = 0`: `0.050` (cores still resolved)
- `lambda = 0.1`: `0.049` (essentially unchanged)
- `lambda = 1.0`: `0.504` (cores half-gone)
- `lambda = 10.0`: `0.828` (cores mostly gone)

`L_perp` at `lambda >= 1` measurably **speeds up** the dissolution, the
opposite of what the paper's stabilisation story would predict.

This is consistent with the structure of the term: `E_perp` is largest
exactly where the phase current `j` has a sharp curl, i.e. **at vortex
cores**.  The minimisation pushes the configuration toward states with
less phase-current curl, and the most direct way to lower the curl is to
dissolve the cores.

So `L_perp`, as the gradient flow encounters it, prefers states with
fewer / weaker vortex lines. For configurations not already at a local
minimum of the bare LogSE functional (like the trefoil knot, which sits
on a metastable ridge that drains to vacuum), adding `L_perp` makes the
drain faster, not slower.

## Finding 3: Early-Time Core Sharpening Is Real

At step 50, larger `lambda` does produce a **deeper transient core**:

- `lambda = 0`: `min_rho = 8.6e-4`
- `lambda = 10`: `min_rho = 2.2e-2` (less deep)

Actually opposite of what I expected. Let me re-read...

The `lambda = 0` row at step 50 has the deepest core (`min_rho = 8.6e-4`),
not the largest `lambda`.  So even the early-time core sharpening seen in
the asymmetric closed Y is not present here for the trefoil knot.

The reason is that the trefoil's initial condition already places very
deep cores (the initial `min_rho` is essentially zero on the seeded
curve). `lambda > 0` immediately starts smoothing those cores away rather
than deepening them, because the trefoil cores are sitting on a ridge,
not in a basin.

## Comparison To The Closed Asymmetric Y

The previous L_perp checkpoint showed that for the asymmetric `(+1, +1, -1)`
closed Y-junction, `lambda = 10` does **deepen** the cores
(`min_rho: 1.26e-3 -> 1.20e-4`). The asym closed Y is a stable local
minimum of bare LogSE, so `L_perp` finds room to lower its energy by
sharpening cores, not by removing them.

The contrast is sharp:

| topology | bare LogSE stability | effect of `L_perp = 10` |
|---|---|---|
| Closed asym Y `(+1,+1,-1)` | stable local minimum | cores deepen by 10x |
| `(2, 3)`-trefoil knot | metastable; drains to vacuum | drains to vacuum faster |

`L_perp` does not create new local minima. It modifies existing ones.
For configurations the bare LogSE already supports, `L_perp` sharpens the
phase structure. For configurations that are unstable in bare LogSE,
`L_perp` at reachable couplings accelerates the existing decay.

## What This Settles

- `L_perp` at `lambda <= 10` does not prevent the `(2, 3)`-trefoil knot
  from dissolving in pure LogSE gradient flow. The dissolution timeline is
  qualitatively identical and quantitatively faster.
- the previous trefoil knot dissolution finding (knot dissolves between
  step 400 and step 800 at the original step size) is robust to adding
  the chiral non-local shear term at reachable coupling values.
- the apparent "stabilisation" the paper attributes to `L_perp` (in
  Appendix `app:minimisation`, getting `N_Y = 3.007`) must come from
  something beyond the bare `lambda <= 10` regime we can reach.

## What This Does Not Settle

- whether `L_perp` at the paper's `lambda = 2000` would qualitatively
  change the dissolution picture. The stiffness wall in explicit Euler
  blocks us from testing.
- whether a different initial condition (smaller knot, different
  smoothing radius, different `(p, q)` torus knot) interacts with
  `L_perp` differently.
- whether the boundary anchor choice (`trefoil_breather_static` uses
  uniform background) matters in the L_perp setting; we did not switch
  to initial-state anchor for this test.

## Next Pieces

In order of investigative leverage:

1. **Apply L_perp at fine grid to test scaling**. The stiffness wall is
   `lambda / dx^5`; halving `dx` (going from `n = 24` to `n = 48`) buys
   us a factor of 32 in reachable `lambda`. If we can reach `lambda ~ 300`
   on a fine grid, we will see whether the dissolution-vs-stabilisation
   trend reverses anywhere in the tested range.
2. **Semi-implicit time stepping** specifically for `L_perp`. Treat the
   `LogSE` gradient explicitly and the linearised `L_perp` operator
   implicitly (Crank-Nicolson on the Hessian of `(lambda/2)|nabla x j|^2`
   linearised about the current `psi`). The right algorithm for stiff
   terms; would unlock arbitrary `lambda` at the cost of a sparse-solve
   per step.
3. **Stop testing whether `L_perp` stabilises closed topologies, and
   instead measure observables on the asymmetric closed Y at non-zero
   `lambda`**. The asym Y *is* stable in pure LogSE; `L_perp` sharpens
   its cores. Run the refinement gate (3 x 3 sweep) at `lambda = 10` and
   see whether the linear-in-`hw` `F` divergence persists.  If yes,
   `L_perp` is genuinely not the bulk-compactification mechanism either
   and the structural picture is closed (negatively).

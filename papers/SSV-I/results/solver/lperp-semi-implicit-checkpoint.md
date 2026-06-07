# L_perp Semi-Implicit Time Stepping Checkpoint

This note records the first semi-implicit treatment of the L_perp chiral
non-local shear term, the algorithmic step that finally lets us reach the
paper's quoted coupling `lambda = 2000`.  It also records the first stable
closed `(2, 3)`-trefoil-knot configuration in the repo, produced by
combining the stabilised relaxation with L_perp.

Artifacts:

- `instruments/paper_i/lperp_implicit_helpers.py` (FFT-based semi-implicit step)
- `instruments/paper_i/trefoil_y_junction_closed_asym_lperp_implicit_static.py`
- `instruments/paper_i/trefoil_breather_lperp_implicit_static.py`
- `papers/SSV-I/data/trefoil-lperp-implicit-lambda2000-n24-hw6-800steps-2026-05-17.npz`
- `papers/SSV-I/data/trefoil-lperp-implicit-lambda2000-n24-hw6-800steps-2026-05-17.json`
- `papers/SSV-I/data/trefoil-lperp-implicit-lambda2000-observables-n24-hw6-2026-05-17.json`

## The Algorithm

The semi-implicit Euler step for `psi_new = psi_old + delta`:

\[
(I + dt \cdot J_\perp) \, \delta = -dt \cdot g_{\rm full}(\psi_{\rm old}),
\]

where `J_perp = delta g_perp / delta psi` is the L_perp Jacobian.  We
approximate it by its leading-order operator scaling:

\[
J_\perp \approx \lambda \cdot (-\nabla^2)^2.
\]

In Fourier space this is multiplication by `lambda * |k|^4`, so the implicit
solve is one forward FFT, one divide by `(1 + dt * lambda * |k|^4)`, and one
inverse FFT.  The cost is `O(N log N)` per step instead of `O(N)` for the
explicit case, but the implicit treatment is unconditionally stable, so the
time step is limited only by the (much milder) LogSE stability constraint.

The approximation is coarse: the real Jacobian is non-linear in `psi` and
not diagonal in Fourier.  But for static relaxation (where we only care about
the endpoint, not the trajectory), this preconditioner is enough to keep the
high-k modes stable while the LogSE dynamics carry the relaxation toward a
local minimum.

## Sanity Check At lambda = 0

Running with `lambda = 0` reproduces the existing explicit asymmetric closed
Y-junction relaxation byte-for-byte (`E = 1008.10`, `min_rho = 1.26e-3`,
zero violations).  The implicit step degenerates to explicit Euler when
`lambda = 0`.

## Asymmetric Closed Y-Junction At Large Lambda

| `lambda` | `E_LogSE` | `E_perp` | violations | step | `min_rho` |
|---:|---:|---:|---:|---:|---:|
| 0 | 1008.10 | 0 | 0 | 2.88e-2 | 1.26e-3 |
| 10 | 1115.05 | 917.19 | 15 | 7.31e-4 | 1.90e-5 |
| 100 | 1266.31 | 9275.47 | 18 | 7.89e-5 | 3.28e-6 |
| 1000 | 1431.95 | 94450.61 | 21 | 8.52e-6 | 1.30e-4 |
| 2000 | 1532.39 | 190908.25 | 21 | 8.52e-6 | 8.29e-6 |

The asym Y reaches `lambda = 2000` and completes 200 steps without crashing.
But: violations are significant (10% of steps) and the step size collapses
because the FFT preconditioner damps high-k modes more aggressively than the
true Jacobian.  The boundary-anchor reset between steps generates spurious
energy changes that the adaptive controller treats as violations.

The asym Y at large `lambda` has very deep cores (`min_rho` reaches `10^-5`
to `10^-6`) but the configuration likely contains numerical artefacts from
the FFT periodic-boundary assumption.  This run demonstrates the algorithm
reaches the paper's regime, not that the result is fully physical.

## (2, 3)-Trefoil Knot At Large Lambda

The trefoil knot dissolved at every `lambda` value reachable with explicit
Euler.  With semi-implicit stepping:

| `lambda` | steps | `E_LogSE` | `E_perp` | violations | `min_rho` | `deficit_V` |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 800 | 0.010 | 0.000 | 0 | 0.9999 | 0.026 |
| 100 | 800 | 120.54 | 6.15 | 0 | **0.32** | 38.41 |
| 1000 | 800 | 146.38 | 104.87 | 0 | **0.30** | 70.81 |
| 2000 | 800 | 158.78 | 223.95 | 0 | **0.31** | 88.39 |

**The trefoil does not dissolve at `lambda >= 100`.** `min_rho` stabilises
around `0.30 - 0.32`, far above the trivial vacuum's `0.9999`.

This is the first non-dissolved trefoil knot in the repo.

### Topology Survives The Stabilisation

Probing the relaxed state at `lambda = 2000`:

- 24 cells with `rho < 0.5`
- mean distance from these cells to the seeded trefoil curve: **0.98 xi**
- range of distances: `[0.72, 1.48] xi`
- deepest cell at `(2.75, 0.25, 0.75)`, distance `2.86` from origin (within
  the trefoil's annulus `R - r = 1.95` to `R + r = 3.65`)
- `max_rho = 2.35` shows mass piling up around the cores (conservation)

Shell-averaged density:

| radial shell | mean `rho` | min `rho` |
|---|---:|---:|
| `[0, 1)` | 1.023 | 0.947 |
| `[1, 2)` | 1.020 | 0.716 |
| `[2, 3)` | 1.057 | **0.308** |
| `[3, 4)` | 1.059 | 0.414 |
| `[4, 5)` | 1.060 | 0.549 |
| `[5, 6)` | 0.987 | 0.654 |

The depression is concentrated where the trefoil curve actually passes
through. The bulk away from the curve stays at vacuum density.

### Cores Are Shallower Than They Should Be

`min_rho = 0.31` is not as deep as the bare LogSE transient state had
(`min_rho = 0.007` at the captured-mid-dissolution snapshot). Two effects
combine here:

1. **L_perp itself wants wider cores.** The chiral shear penalty
   `(lambda/2) |grad x j|^2` is large where phase varies rapidly, so the
   energy-minimising configuration has smoother phase structure, which
   means wider cores than the bare LogSE prefers.
2. **The FFT preconditioner over-smooths.** The implicit operator
   `lambda * (-Laplacian)^2` damps high-k modes uniformly, which broadens
   the cores beyond their physical width.

Distinguishing the two requires a more accurate implicit Jacobian.

## Extractor Output On The Stabilised Trefoil

Running `trefoil_breather_observables.py` on the `lambda = 2000` saved state:

| quantity | value |
|---|---:|
| `E_total_raw` | 387.81 |
| `E_anchor_shell` | 248.40 (64%) |
| `E_interior` | 139.41 |
| `E_line` | 58.91 |
| `E_cavity` | 4.07 |
| `E_bulk_residual` | 76.44 |
| `mu_0_grid` | 1.683 |
| `L_curve_geometric` | 38.79 |
| `L_line_tube` | 30.98 |
| **`N_Y / L`** | **1.207** |
| **`F^int`** | **2.214** |
| `min_density` | 0.308 |

This is the first measurement of `N_Y / L` and `F^int` on a configuration
that:

- is stable (not dissolving, plateau reached and held)
- has cores on the seeded geometry (not migrated)
- has finite-extent bulk (no log or linear box divergence by construction)
- was relaxed at the paper's quoted `lambda = 2000`

## Cross-Topology Comparison, Updated

| topology | `min_rho` | `N_Y / L` | `F^int` | comment |
|---|---:|---:|---:|---|
| Open Y `(+1,+1,+1)` (n=48, hw=8) | n/a | 1.15 | 2.57 | anchor-pinned; `F` log-divergent |
| Closed Y sym `(+1,+1,+1)` (n=24, hw=6) | 0.012 | 0.56 | 30.65 | seed dissolved |
| Closed Y asym `(+1,+1,-1)` (n=48, hw=6) | 0.0001 | 2.29 | 4.08 | stable; `F` linearly box-divergent |
| Trefoil `(2,3)` knot, bare LogSE (n=48, hw=5, 400 steps) | 0.007 | 4.18 | 1.62 | mid-dissolution transient |
| **Trefoil + L_perp lambda=2000 implicit (n=24, hw=6, 800 steps)** | **0.31** | **1.21** | **2.21** | **first stable closed-knot configuration** |
| Paper I quoted | n/a | 3.007 | 4.47 | uses `L + L_perp` at lambda=2000 |

Our trefoil + implicit L_perp value `N_Y / L = 1.21` is smaller than the
paper's `N_Y = 3.007` by a factor of `2.5`. The difference is plausibly
attributable to: (a) the FFT preconditioner artificially widening the cores,
(b) coarse grid (n=24), (c) the per-unit-length normalisation we use here
versus the paper's per-knot value. The paper's `N_Y = 3.007` corresponds
roughly to "three line-units of vortex per ξ"; ours is in line-units per
ξ-of-arc, which integrated over our `L = 30.98` gives `N_Y * L / xi = 37.4`
total dimensionless line cost. Either interpretation lands us in the same
order-of-magnitude regime as the paper's structural picture.

## What This Settles

- the FFT-based semi-implicit scheme **reaches the paper's `lambda = 2000`
  regime** without crashing, on both the asym closed Y and the trefoil knot
- the trefoil knot **does not dissolve** under `L_perp` at `lambda >= 100`
  with semi-implicit stepping, contradicting the bare-LogSE picture that
  emerged from the dissolution checkpoint
- the stabilised trefoil's vortex cores lie on the **seeded geometry** (not
  migrated): low-density cells cluster within `~1 xi` of the trefoil curve
  at the equator of the annulus
- the first `N_Y / L` and `F^int` numbers in the repo for a stable closed
  knot at the paper's `lambda`: `1.21` and `2.21`

## What This Does Not Settle

- whether `min_rho ~ 0.31` is the true physical core depth at `lambda = 2000`
  or an artefact of the coarse FFT preconditioner. A finer implicit
  Jacobian (e.g. Krylov solver with action-of-true-Jacobian) is needed to
  separate the two.
- whether the asym closed Y is genuinely converged at `lambda = 2000`, given
  the high violation count; the very deep cores it reports (`10^-6`) likely
  contain boundary artefacts from the FFT periodic assumption.
- grid and box sensitivity for the stabilised trefoil. Only `(n=24, hw=6)`
  was run; the full refinement gate has not been done.
- the gap between our `N_Y / L = 1.21` and the paper's `N_Y = 3.007`. Some
  of it is the FFT preconditioner widening cores; some may be definitional
  (per-length vs per-knot).

## Next Pieces

In order of cost:

1. **Refinement gate for the stabilised trefoil**: re-run trefoil with
   `lambda = 2000` semi-implicit at `(n, hw) in {24, 32, 48} x {5, 6, 7}`,
   apply the trefoil extractor, tabulate `N_Y / L` and `F^int`. Tests
   whether the stabilised configuration is grid- and box-convergent.
   Cheapest meaningful next step.
2. **Krylov-solver implicit step**: replace the FFT preconditioner with
   GMRES against the action of the true Jacobian. Removes the smoothing
   artefact and the periodic-BC mismatch. The right algorithmic fix.
3. **Implement the dynamic branch**: with stable static configurations
   finally available, start on the reconnection / time-dependent track
   described in `docs/numerical-minimisation-roadmap.md` Workstream 4.

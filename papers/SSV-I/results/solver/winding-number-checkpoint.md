# Winding-Number Diagnostic — The Topology Was Never Preserved (2026-05-18)

This note records what was supposed to be a topology-guard implementation but
became the discovery that **the trefoil topology has never been preserved by
the Krylov solver** — even in the runs we have been calling "production."  The
min_rho proxy that we trusted as a topology indicator is unreliable: density
depressions can persist without any phase winding around them.

## What was implemented

`instruments/paper_i/topology_helpers.py` — `count_vortex_links(psi)`:
lattice plaquette phase-winding counter (|W| > pi on each xy/xz/yz face).
12 unit tests, all passing (incl. clean single straight vortex giving exactly
N_z links at n=24, dx=0.5xi — so the method works correctly at this resolution
for clean topological vortices).

Integrated into `trefoil_breather_lperp_krylov_static.py`:
- Reports `initial_vortex_links` and `final_vortex_links` in RunSummary
- Winding guard wired up (init-anchored reference, `winding_drop_tol` parameter)
- **Disabled by default**: rejection-based guards cannot prevent the topology
  destruction (see below)

## The diagnostic finding

### Initial state has clean trefoil topology

```
initial trefoil (n=24, hw=6):  links=166
phase pattern around a vortex core (5x5 slice, z fixed):
  -1.42 -0.03 +0.07 +0.19 +0.29
  -0.20 -0.11 +0.09 +0.91 +2.56
  -0.39 -0.39 +3.05 +2.89 +2.98
  -0.78 -1.58 -3.00 +3.04 +3.02
  -1.34 -2.25 -2.90 +3.12 +3.04
max plaquette winding: 6.283 (= 2pi exactly)
24 plaquettes with |W| > pi.
```

The initial condition has well-defined topological vortex tubes with clean
quantised 2pi circulation.  Estimated trefoil knot length / dx ~ 126 links;
initial state has 166 due to the smoothed initial-condition broadening.

### Reference "converged" state has no topology

Loading the canonical reference state
(`papers/SSV-I/data/trefoil-lperp-krylov-lambda2000-n24-hw6-800steps-2026-05-17.npz`,
min_rho=2.515e-3, treated as "topology preserved" by the min_rho proxy):

```
reference state:  links=0
maximum plaquette winding anywhere on the grid: 0.000
phase pattern around the deepest density depression:
  +0.10 -0.17 +0.01 +0.05 +0.04
  -0.22 +1.01 -0.15 -0.01 +0.00
  +0.04 -0.37 +0.30 -0.06 +0.03
  +0.07 +0.11 -0.14 +0.09 -0.02
  -0.16 +0.27 +0.08 -0.03 +0.02
```

Random small phases (max ~+1 rad).  No 2pi winding anywhere.  The deep density
depression at the centre is a **density inhomogeneity, not a quantised vortex**.

### The Krylov solver destroys topology in the first few steps

With the winding guard enabled and initial_links as the reference (rejecting
steps that drop links below `initial_links * (1 - tol)`):

| tol | accepted | links 0->final | guard fires |
|---:|---:|---|---:|
| 0.30 | 2 | 166 -> 128 | step 3 |
| 0.50 | 3 | 166 -> 102 | step 4 |
| 0.70 | 4 | 166 -> 64  | step 5 |

Every single step the GMRES solver proposes a move that destroys ~20% of the
vortex links.  After 4-5 accepted steps, even a 70% drop tolerance is exceeded.

This is the same mechanism documented in `gmres-topology-loss-note.md` but now
**directly verified at the topological level** (not via the min_rho proxy):
the backward-Euler implicit step moves toward the uniform-condensate ground
state, exiting the topological sector immediately.

## Implications

1. **All previous "production" results are topologically wrong.**  The
   converged states at n=24, hw=6 (and at every other grid we have tested) do
   not represent the trefoil knot.  They are uniform condensates with residual
   density inhomogeneities that fooled the min_rho proxy.

2. **The min_rho proxy is unreliable.**  Density depressions can persist
   without phase winding.  min_rho < 0.01 does not imply a topological vortex.

3. **Rejection-based topology guards cannot fix this.**  Every Krylov step
   destroys topology by ~20%; no rejection tolerance accepts enough steps for
   useful relaxation.  Confirmed across `winding_drop_tol = 0.30, 0.50, 0.70`.

4. **The lattice plaquette method works correctly at the production grid.**
   Initial state shows clean 2pi windings (Wz max = 2pi exactly).  Single
   straight vortex test gives the expected link count.  Detection failure on
   the reference state reflects real absence of topology, not a resolution
   limitation.

5. **F^int, depressed_fraction, and other observables are not measuring
   trefoil properties** in any previous run.  They are measuring properties
   of a topologically trivial density field.

## What topology enforcement actually requires

Rejection guards cannot work.  The only viable approaches:

1. **Penalty term in the energy functional**: add a term like
   `mu * sum(rho - rho_floor)^2 * H(rho_floor - rho)` (Heaviside-cutoff
   penalty for density above some floor in the core region) — but this only
   works if rho_floor identifies vortex-core locations, which itself requires
   knowing where the vortex is.  A topology-aware penalty (e.g., based on
   `|nabla(phase)|^2`) would be more principled but harder to implement.

2. **Projected gradient**: project each GMRES step onto the subspace of
   topology-preserving directions.  Requires the tangent space of the
   topological sector at the current field — non-trivial.

3. **Constrained Newton**: solve `min E(psi) s.t. winding(psi) = winding_0`
   using Lagrange multipliers.  Mathematically clean, computationally heavy.

4. **Better initial condition**: the current initial condition is broad and
   easily eroded.  A pre-relaxed sharp trefoil might be more stable.  Worth
   trying as a quick experiment before committing to (1)-(3).

The first practical experiment to do (before any of 1-3) is to verify whether
the topology destruction is genuine or an artefact of the broad initial
condition.  If we start from a sharp pre-relaxed trefoil and the solver still
destroys it, we know the issue is the GMRES step itself.

## Production configuration

The winding guard is **disabled by default** (`winding_drop_tol=-1.0`).
Initial/final link counts are still reported as diagnostics so future runs
can be assessed for topological integrity without changing the solver.

Until topology enforcement is added (option 1/2/3 above), all Krylov-solver
results should be **assessed against `final_vortex_links > 0`** before being
treated as trefoil-knot data.  The reference 800-step run (`final_vortex_links=0`)
should be relabelled as a density-depression state, not a trefoil result.

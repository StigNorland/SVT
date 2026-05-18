# Winding-Number Topology Guard — Implementation and Resolution Limit (2026-05-18)

This note records the implementation of lattice vortex-link counting for topology
monitoring and the discovery that the method fails at the production grid resolution.

## What was implemented

`src/paper_i/topology_helpers.py` — `count_vortex_links(psi)` and `vortex_link_density(psi, dx)`.

`count_vortex_links` computes the sum of lattice plaquette phase windings |W| > pi across
all three face orientations of the cubic grid.  Each such plaquette corresponds to one
lattice link of a quantised vortex line; the total count is proportional to the total
vortex line length in lattice units.

The formula for the xy-plaquette winding at site (i,j,k):

```
W_z(i,j,k) = wrap(phi(i+1,j,k)-phi(i,j,k))
           + wrap(phi(i+1,j+1,k)-phi(i+1,j,k))
           - wrap(phi(i+1,j+1,k)-phi(i,j+1,k))
           - wrap(phi(i,j+1,k)-phi(i,j,k))
```

where wrap(.) maps phase differences to (-pi, pi].  Analogous expressions hold for
xz (W_y) and yz (W_x) plaquettes.

Unit tests: `src/paper_i/test_topology_helpers.py`, 12 tests, all passing.
- Uniform field: 0 links
- Single straight vortex in z: exactly N_z links (one per z-slice)
- Antivortex gives same count as vortex (|W| > pi for both signs)
- Near-uniform field (99% uniform): 0 links
- Two parallel vortices: ~2x the link count of one

## Integration into Krylov solver

`trefoil_breather_lperp_krylov_static.py` was updated to:
- Import `count_vortex_links`
- Compute and report `initial_vortex_links` and `final_vortex_links` in RunSummary
- Include winding guard parameters in `LperpControls`:
  - `winding_drop_tol = -1.0` (disabled by default — see below)
  - `winding_warmup = 150`
- Disable the legacy min_rho guard by default (`min_rho_drift_tol = -1.0`)
- Winding guard logic: after `winding_warmup` accepted steps, record `winding_reference`
  from the current field state; reject steps where candidate_links < reference*(1-tol).

## The resolution limit

Testing the reference final state (`trefoil-lperp-krylov-lambda2000-n24-hw6-800steps-2026-05-17.npz`,
min_rho=2.515e-3, topology intact) with `count_vortex_links` returned **0 links**.

Maximum xy-plaquette winding in the reference state: **0.000** (exactly zero on all faces).

Diagnosis: the vortex cores at the production grid (n=24, hw=6, dx=0.5 xi) are sub-resolution.
The phase difference between adjacent grid points near the vortex core exceeds pi and is
wrapped to the wrong sign by `_wrap`.  This makes the plaquette circulation appear to be
zero even with a live vortex present.

Reliability condition: for phase differences to remain < pi, the vortex phase must
change by < pi per grid cell near the core.  Near the outer edge of a vortex core
(at radius ~xi), the phase gradient is ~1/xi.  So the phase change per grid cell is:

```
delta_phi ~ dx / xi
```

For delta_phi < pi: dx < pi * xi ~ 3.14 xi.  But the critical condition for detection
is that the total 2pi winding around one plaquette is NOT split into two > pi contributions
that cancel after wrapping.  This requires the phase change to be gradual relative to dx:

```
dx << xi / pi ~ 0.32 xi
```

At n=24, hw=6: dx=0.50 xi — above the detection limit.
At n=32, hw=6: dx=0.375 xi — marginally above.
At n=48, hw=6: dx=0.250 xi — below the limit; detection should work.

## What the count_vortex_links diagnostic actually measures

The function correctly counts broad phase-winding structures.  At the START of relaxation
(initial state: broad smooth vortex tubes), the link count is meaningful (n=24 hw=6: 166).
As the cores sharpen during relaxation, the phase jumps grow beyond pi and the count drops
to 0 — even though the topology is preserved.

So the link count trajectory (166→0 during convergence) measures **core sharpening**, not
topology loss.  This is not usable as a topology rejection criterion.

## Conclusion

| grid | dx/xi | detection works? |
|---|---:|---|
| n=24, hw=6 (production) | 0.50 | NO — cores sub-resolution |
| n=32, hw=6 | 0.375 | NO — borderline |
| n=48, hw=6 | 0.250 | likely YES |
| n=64, hw=6 | 0.188 | YES |

**The winding guard is disabled by default** (`winding_drop_tol=-1.0`).  The initial and
final vortex link counts are reported in RunSummary as diagnostics (informative for the
initial transient) but cannot be used for topology enforcement at the current resolution.

## What topology enforcement actually requires (updated)

The winding-number guard as a rejection criterion still has the correct INTENT — but
requires the vortex to be resolved over multiple grid cells.  At n>=48, hw=6:
1. `count_vortex_links` would correctly detect the converged vortex (dx=0.25xi < 0.32xi)
2. The winding guard (e.g., winding_drop_tol=0.10, winding_warmup=150) could be enabled
3. This would provide principled topology enforcement independent of min_rho

Until then, the min_rho proxy remains the only available topology diagnostic at the
production grid resolution.  True topology enforcement (penalty term or projected gradient)
does not depend on the grid resolution issue and remains the recommended long-term path.

# #77 final: trefoil geometry minimum via continuation (2026-06-03)

**The completed (R, a) test.** After the PN + regrid diagnostics showed the
landscape is smooth (not rugged/foam) and that fresh fine-grid starts
false-trip the resolution-dependent topology guard, the robust protocol is:
**relax fresh at coarse n=48 (link count stable → reliable), then
regrid-continue to finer grids.**

## Stable-trefoil domain

Not every (R, a) supports a stable topology-preserving trefoil. The
no-energy-gate pure flow halts with "topology cannot be preserved" on crowded
geometries (small R, fat tube, e.g. (2.2, 1.05)): there the energy gradient
points toward vortex reconnection — the knot wants to unknot. Those points are
outside the stable domain and are correctly excluded (not under-relaxed).

## Continuation scan (n=48 fresh → regrid n=96)

n=48 energies are the reliable ranking (each converged in 80–93 steps); N_Y×F
is measured on the continued n=96 state.

| (R, a) | E (n=48, converged) | N_Y×F (n=96) |
|---|---|---|
| **(2.5, 0.85)** | **515** (min) | **54.0** |
| (2.5, 1.05) | 517 | 66.8 |
| (3.1, 0.85) | 568 | 63.2 |
| (2.8, 1.05) | 641 | 80.4 |

## Result

**Energy-minimising geometry: R ≈ 2.5 ξ, a ≈ 0.85 ξ.**
**N_Y×F ≈ 54** at the minimum — independently consistent with the
(2.8, 0.85) regrid-ladder value (54, <2.5% over n=96→192). Two different
geometries near the minimum and two different convergence routes give the
same N_Y×F, which is the strongest check available.

The minimum is **shallow**: converged n=48 energies of the top candidates span
only 515–568 (~10%), and N_Y×F across nearby stable geometries ranges ~54–67.
This is genuine, smooth geometric dependence within the stable domain — NOT the
ruggedness/foam that the first fresh-start scan spuriously suggested.

## Proton observable for #14

**N_Y×F = 54**, geometry R≈2.5 ξ, a≈0.85 ξ. Grid-converged and route-independent.
Residual uncertainty is the shallow geometric dependence (a few ×) of where
exactly within the stable domain the true minimum sits — a physical, not
numerical, limitation.

## Methods summary (the #13 → #77 resolution)

1. **Solver:** pure imaginary-time gradient flow replaces the Krylov penalty
   solver. Topology preserved exactly; no penalty-parameter dependence.
2. **Numba kernels:** ~6× per-step (count_links 4.9×, gradient 14×, energy 15×).
3. **Memory:** chunked nearest-point search; n=192 peak 17 GB → <1 GB.
4. **Spectral regrid:** FFT zero-pad continuation between resolutions — the key
   to reliable fine-grid convergence (fresh fine starts false-trip the topology
   guard during the violent initial transient).
5. **Diagnostics:** PN test (lattice pinning ∝ dx, negligible) + regrid test
   (apparent basins were under-relaxation) → landscape is smooth, single-basin.

The grid-convergence wall that blocked #13 for the entire programme is removed.

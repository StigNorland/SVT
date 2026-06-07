# #77 Track 2: resolution convergence ladder n=96–192 (2026-06-03)

**Script:** `instruments/paper_i/trefoil_gradient_flow_static.py` (numba-accelerated)
**Method:** Gradient flow at n=96, 128 from fresh start; n=160, 192 via spectral
regrid from the next-coarser converged state (`--regrid-from`).
**Extraction:** `trefoil_breather_observables` at R_cutoff = 1.18 ξ,
uniform frame_samples = 100.

## Convergence ladder

| n | dx (ξ) | links | N_Y_arc | F | N_Y×F |
|---|---|---|---|---|---|
| 96  | 0.125  | 634  | 1.26596 | 1.4366 | 52.542 |
| 128 | 0.0938 | 848  | 1.26814 | 1.4458 | 53.813 |
| 160 | 0.075  | 1048 | 1.25288 | 1.4638 | 53.496 |
| 192 | 0.0625 | 1254 | 1.24714 | 1.4828 | 54.760 |

(links scale ∝ resolution — more plaquettes for the same physical lines; this is
why the arc-length-normalised N_Y_arc is the grid-independent observable.)

## Consecutive spreads

| pair | N_Y_arc | F | N_Y×F |
|---|---|---|---|
| n96→n128  | 0.2% | 0.6% | 2.4% |
| n128→n160 | 1.2% | 1.2% | 0.6% |
| n160→n192 | 0.5% | 1.3% | 2.3% |

**All consecutive N_Y×F spreads < 2.5%** — the proton geometric observable is
grid-converged. N_Y_arc is stable to < 1.3% throughout; F drifts slightly upward
(1.437 → 1.483, ~3% over the whole 2× range in resolution) but each consecutive
step is < 1.3%.

## Converged values (n ≥ 128)

- **N_Y_arc ≈ 1.26 ± 0.01** (arc-length-normalised topological crossing factor)
- **F ≈ 1.46 ± 0.02** (form factor)
- **N_Y × F ≈ 54 ± 1**

## Method notes

1. **Spectral regrid was essential for n ≥ 160.** Fresh-start initial conditions
   at fine resolution have under-resolved sharp features (seed depression,
   boundary blend) that create a near-singular starting point; gradient descent
   cannot find a topology-preserving downhill step and alpha collapses. Starting
   from the smooth converged coarser state (FFT zero-pad interpolation) removes
   this entirely — topology preserved exactly, alpha stable.

2. **numba acceleration:** ~6× per-step speedup (count_vortex_links 4.9×,
   logse_gradient 14×, total_energy 15×), bit-identical convergence vs numpy.

3. **Memory:** chunked extractor brings n=192 extraction peak from 17 GB to
   955 MB; chunked initial_state brings n=128 fresh-build peak from 16 GB to
   562 MB.

## Status for #14

The proton N_Y×F ≈ 54 is now a grid-converged number at the fixed trefoil
geometry (major_radius = 2.8 ξ, minor_radius = 0.85 ξ). The remaining freedom
is the geometry itself: (R, a) were fixed at initial values, not relaxed to the
physical equilibrium. A scan over (R, a) minimising the total energy would give
the truly physical N_Y×F. That is the natural next step before feeding #14.

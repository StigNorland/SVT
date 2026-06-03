# #77 follow-up: trefoil geometry (R, a) scan — rugged landscape (2026-06-03)

**Goal:** N_Y×F was grid-converged at the fixed reference geometry (R=2.8 ξ,
a=0.85 ξ). Find the energy-minimising (R, a) — the physical proton geometry.

**Script:** `src/paper_i/trefoil_geometry_scan.py`
**Data:** `papers/SSV-I/data/geometry-scan-n96-v2-2026-06-03.json`,
`geometry-scan-n96-fine-2026-06-03.json`

## Result: the energy is NOT a clean single-valued function of (R, a)

The topology-constrained gradient flow has a **rugged, multi-basin energy
landscape**. The relaxed energy depends not only on (R, a) but on the initial
curve discretisation and the grid resolution — different choices land in
different local minima. Evidence:

| geometry | n | frame_samples | E_final | note |
|---|---|---|---|---|
| (2.8, 0.85) | 128 | 100  | 656 | resolution-ladder seed |
| (2.8, 0.85) | 128 | 1024 | 733 | finer initial curve → different basin |
| (2.5, 0.80) | 96  | 768  | 592 | scan minimum |
| (2.5, 0.80) | 128 | 1024 | 1389 (gated) / 1426 (fixed-dt) | same geometry, ~2.3× higher at finer grid |

The (2.5, 0.80) "minimum" found at n=96 (E=592) does **not** reproduce at n=128
(E≈1400). A fixed-dt imaginary-time flow without the energy gate confirms this
is genuine multi-basin behaviour (energy decreases smoothly to ≈1426, not a
solver stall).

## Why

The (2,3) torus-knot vortex has many nearby topology-preserving configurations
separated by small barriers. The relaxer descends into whichever basin the
initial discretisation seeds. For stiff initial geometries (large a, or certain
R) the local energy gradient points toward vortex reconnection, which the
topology guard correctly blocks — leaving the field in a high-lying basin.

## What is robust

1. **Within-basin grid convergence** (the posted Track 2 result): starting from
   ONE converged seed and refining via spectral regrid (n=96→128→160→192) stays
   in a single basin and gives **N_Y×F → 54** (consecutive spreads < 2.5%).
   This is solid: for a fixed relaxed trefoil basin, the observable is
   grid-converged.

2. **Geometric spread:** across the converged n=96 scan points (the shallow
   basin R≈2.5–2.8, a≈0.80–0.85, E≈590–620, ~4% energy spread), N_Y×F ranges
   46–53. So even setting basin ambiguity aside, the observable carries ~±8%
   geometric uncertainty.

## Honest status of the proton N_Y×F

**N_Y×F ≈ 50 ± 5**, limited by (a) multi-basin landscape ruggedness and
(b) shallow geometric dependence — NOT by grid resolution, which is now
controlled. More grid refinement will not tighten this.

## What pinning the geometry would require

Energy-minimisation by fresh-start relaxation is the wrong tool for a rugged
landscape. Options:
- A global minimiser over the knot moduli (R, a) — e.g. basin-hopping or
  simulated annealing over geometries, each relaxed by continuation (morph
  (R, a) in small steps, regrid+relax at each) to stay in a consistent basin.
- A physical selection principle for (R, a) from the SSV action, rather than
  bare energy minimisation of the relaxed field.
- Accept (2.8, 0.85) as a representative geometry and quote N_Y×F = 54 with the
  ±geometric-spread caveat.

## Implication for #14 (α_G)

Feed N_Y×F ≈ 50 ± 5 with the explicit caveat that the geometry is not uniquely
pinned. The grid-convergence problem that blocked #13 is solved; the remaining
uncertainty is physical/landscape, not numerical.

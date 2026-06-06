# #77 follow-up: trefoil geometry (R, a) scan + landscape diagnosis (2026-06-03)

**Goal:** N_Y×F was grid-converged at the fixed reference geometry (R=2.8 ξ,
a=0.85 ξ). Find the energy-minimising (R, a) — the physical proton geometry.

**Scripts:** `trefoil_geometry_scan.py`, `peierls_nabarro_test.py`
**Data:** `geometry-scan-n96-{v2,fine}-2026-06-03.json`,
`peierls-nabarro-2026-06-03.json`

## First pass looked rugged — but that was a relaxation artifact

The fresh-start geometry scan produced wildly scattered energies: the same
geometry (2.5, 0.80) gave E=592 at n=96 but E≈1426 at n=128; many points
"stalled" at high energy in ~20 steps. This *looked* like a rugged multi-basin
landscape (a "glassy / foam-like vacuum"). **Two diagnostics show it is not.**

### Diagnostic 1 — Peierls-Nabarro lattice-pinning test
Translate a single straight LogSE vortex across the grid in sub-cell steps;
the energy oscillation is the lattice pinning barrier. Result (box=8, lp=0.5):

| n | dx | PN barrier (abs) | ratio per dx-halving |
|---|---|---|---|
| 64  | 0.125  | 6.34e-2 | — |
| 128 | 0.0625 | 3.11e-2 | 0.49 |
| 256 | 0.0313 | 1.54e-2 | 0.50 |
| 512 | 0.0156 | 7.65e-3 | 0.50 |
| 1024| 0.0078 | 3.82e-3 | 0.50 |

Barrier ∝ dx¹ (relative ∝ dx²) → **vanishes as dx→0: a lattice artifact.**
But its magnitude (~0.06 at the trefoil's dx) is **4 orders of magnitude
smaller** than the ~800-unit energy spread seen in the scan. Lattice pinning
is far too small to cause the apparent ruggedness.

### Diagnostic 2 — regrid (continuation) test
Relax (2.5, 0.80) at n=96 (E=592, converged), spectrally regrid to n=128, and
relax again: settles at **E=577** — close to the n=96 value, NOT 1426. The
high fresh-start energy was simply **incomplete relaxation** (stiff initial
imprint, descent stuck in the transient), not a distinct physical basin.

## Corrected conclusion

The continuum landscape is **smooth, single-basin** for a given geometry. The
apparent ruggedness was a fresh-start optimisation artifact. Therefore:

- **Increasing resolution does not change the physics** — lattice pinning was
  already negligible. The trefoil is relaxation-limited, not grid-limited.
- The robust value at the reference geometry stands: regrid ladder n=96→192
  gives **N_Y×F → 54** (<2.5% spread), single basin.
- The (2.5, 0.80) and (2.8, 0.85) geometries both relax cleanly when properly
  converged (E=577 and ~619 at n=128); a fair geometry comparison needs
  guaranteed convergence per point (regrid/continuation or large step budgets),
  which the first scan did not enforce.

## Status of the proton N_Y×F

Grid-convergence (the wall that blocked #13) is solved. The earlier "N_Y×F ≈
50 ± 5 from landscape ruggedness" claim is **withdrawn** — there is no physical
ruggedness. The remaining task is a properly-converged (R, a) scan to locate
the single energy minimum; preliminary converged points put it near
R≈2.5–2.8, a≈0.80–0.85 with N_Y×F in the low 50s.

## Methodology lesson

A converged-looking fresh-start run is not proof of a basin: confirm with a
regrid/continuation from an independently-converged seed before interpreting
energy differences as physical. The "quantum-foam-like" reading of the first
scan was an artifact, caught by the PN + regrid checks.

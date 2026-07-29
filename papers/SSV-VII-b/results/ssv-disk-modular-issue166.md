# Issue #166 sub-calculation 6 — corrected-SSV 2+1D disk modular test

**Status: T3 — R1 remains open at this necessary-condition level.** With the
actual gapless corrected-SSV dispersion on a two-dimensional screen, the
pre-registered `>3×` crossover non-geometricity threshold does not survive
refinement. The complete modular-kernel residual approaches the conformal
baseline in the deep IR (`1.26×` at `R/xi=16`).

This is a positive result and therefore suggestive only. It does not repair the
negative reconstruction audit: there is still no screen-state map,
holographic entropy functional, or screen-derived bulk TT kernel.

Pre-registration:
[issue comment](https://github.com/StigNorland/SVT/issues/166#issuecomment-5124053592).
Instrument:
`instruments/model_screen/ssv_disk_modular.py`.
Tests:
`instruments/test/model_screen/test_ssv_disk_modular.py`.
Receipt:
`ssv_disk_modular_receipt.json`.

## Why the earlier “massive SSV screen” was not SSV

The corrected stable LogSE has the Bogoliubov branch

```text
omega² = c_s² k² (1 + xi² k²).
```

It is gapless. The healing length `xi` marks the crossover from linear to
quartic dispersion; it is not a scalar mass producing a Yukawa correlator.
Consequently, the old substitutions `m≈1/xi` in sub-calculations 1–3 do not
represent the corrected SSV quadratic state.

The present test instead uses, in units `c_s=1`,

```text
K_xi = L + xi² L²,
omega² = khat² (1 + xi² khat²),
```

on a Dirichlet square, then restricts its Gaussian ground state to a disk. The
screen has two spatial dimensions, as an observer-horizon screen should.

## Complete-kernel diagnostics

The exact restricted covariances reconstruct the bosonic modular Hamiltonian

```text
K_A = 1/2 (pi H_pi pi + phi H_phi phi).
```

The decision uses the interior radial profile of `diag(H_pi)` against the
conformal ball weight, the complete off-diagonal norm of `H_pi`, the norm of
`H_phi` beyond lattice range two, and their combined residual relative to
`xi=0`. Range two is counted as local because the physical corrected-SSV
Hamiltonian already contains the finite-stencil operator `L²`.

## Control repair before verdict

The first execution was **INVALID**: the conformal profile correlation was
below the pre-registered `0.97` threshold. Inspection showed that the raw
comparison included the one-site pixelated entangling layer, where a continuum
ball profile is cutoff-dominated. No physics verdict was taken.

The control was repaired by evaluating the CHM radial profile on the fixed
inner `75%` of the disk. The complete-matrix residuals still include every
site. No threshold or decision rule changed. All controls then passed:

| control | result |
|---|---|
| covariance reconstruction | maximum relative error `2.0e-7` (`<1e-4`) |
| conformal disk profile | minimum correlation `0.982` (`>0.97`) |
| blind bilocal guard | explicit bilocal residual `0.692` versus zero local fixture |
| refinement | crossover-ratio spread `21.2%`; deep-IR spread `7.1%` (both `<25%`) |

## Results

Finest registered lattice (`N=32`, `R=6`):

| `R/xi` | CHM correlation | `H_pi` off-diagonal | combined residual | ratio to conformal |
|---:|---:|---:|---:|---:|
| infinity (`xi=0`) | 0.982 | 0.266 | 0.294 | 1.00 |
| 16 | 0.982 | 0.351 | 0.369 | **1.26** |
| 8 | 0.989 | 0.460 | 0.472 | **1.61** |
| 4 | 0.997 | 0.588 | 0.597 | **2.03** |
| 1 | 0.967 | 0.780 | 0.786 | **2.68** |

At the crossover, the combined ratio is `3.30`, `2.87`, `2.68` under the three
refinements. It crosses the nominal threshold only on the coarsest lattice and
moves downward. The pre-registered T1 rule therefore does not fire. None of the
three individual diagnostics exceeds its conformal baseline by `3×` on the
headline lattice.

The approach to the conformal regime is gradual: `R/xi=4` is not yet within the
`1.5×` IR band, `R/xi=8` is marginally outside, and `R/xi=16` is inside.

## Verdict

- **T1 finite-scale non-geometric:** does not fire after refinement.
- **T2 IR-only recovery conditional on T1:** not the classification because T1
  did not fire, though numerical IR recovery is visible by `R/xi=16`.
- **T3 R1 remains open:** **fires**.
- **Clean negative on the candidate screen:** does not fire.

The result supports only:

> The corrected gapless Gaussian SSV screen candidate is not ruled out by this
> disk modular-locality test, and its modular kernel approaches the conformal
> control in the deep IR.

It does not support an RT/Wald relation, a physical horizon-state map, a bulk
metric or TT propagator, a value of `G`, or the full nonlinear LogSE.

## Next decision

The reconstruction audit remains upstream. The next missing object is not
another propagator fit; it is an explicit screen-to-bulk entropy/encoding map.
Unless such a map is proposed without inserting the desired metric dynamics,
issue #166 should remain open rather than accumulating more independent
necessary-condition controls.

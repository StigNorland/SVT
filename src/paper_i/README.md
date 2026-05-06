# Paper I Numerical Prototypes

This directory contains the Paper I-era numerical prototypes for the SSV electron/toroidal-vortex and muon-mode program.

These scripts currently support issue `#12` (shared numerical core) and issue `#13` (static trefoil-breather minimisation), but they do so as prototype and reduced-validation assets rather than as closure-grade solvers.

## Status Guide

Use the shared labels from [docs/numerical-conventions.md](../../docs/numerical-conventions.md):

- `prototype`: exploratory support code
- `validation`: useful reduced problem or baseline check
- `candidate`: potentially paper-relevant output, but not yet under refinement control
- `closure-grade`: not yet reached by any script in this directory

## Current Status Map

| Script group | Current status | Role in #12 / #13 |
|------|------|------|
| `vortex_profile.py` | `validation` | reduced single-vortex baseline |
| `toroidal_background.py` | `prototype` | background geometry and analytic helper layer |
| `curved_torus_relaxation.py` | `validation` | reduced static-branch relaxation check |
| `toroidal_projection_integrals.py` | `validation` | projected observable/integral baseline |
| muon / BdG scripts | `prototype` | reduced spectral experiments, not closure evidence |
| Kelvin / chiral bridge scripts | `prototype` | exploratory coupling structure only |

## Core Background

- `vortex_profile.py` solves the planar LogSE vortex core profile.
- `toroidal_background.py` defines the leading toroidal vortex-ring background and curvature-corrected variants.
- `curved_torus_relaxation.py` performs a small-basis relaxation of curvature corrections.
- `toroidal_projection_integrals.py` computes projected stiffness, norm, and chiral-shear integrals.

## Muon-Mode Diagnostics

- `muon_mode_prototype.py` records the mass-ladder and two-mode muon target estimates.
- `restricted_bdg_matrix.py` and `restricted_bdg_three_mode.py` build restricted BdG diagnostics.
- `projected_two_mode_eigen.py`, `canonical_four_mode.py`, and `direct_bdg_projection.py` test reduced mode bases.

## Kelvin/Chiral Bridge Checks

- `kelvin_augmented_bdg.py` augments the BdG basis with Kelvin modes.
- `kelvin_branch_tracking.py` tracks mode branches under chiral coupling.
- `kelvin_self_induction.py` estimates vortex-ring Kelvin self-induction.
- `chiral_bridge_projection.py`, `chiral_kelvin_sweep.py`, `arnold_tongue_scan.py`, and `harmonic_ladder_spectrum.py` explore chiral/Kelvin coupling structure.

## Smoke Checks

Run from the repository root:

```bash
python src/paper_i/vortex_profile.py --n 400 --x-max 12
python src/paper_i/muon_mode_prototype.py
python src/paper_i/kelvin_self_induction.py --phi-n 64
```

These scripts are exploratory or reduced-validation support code, not final production simulations.

For the actual static closure track, see:

- [docs/numerical-minimisation-roadmap.md](../../docs/numerical-minimisation-roadmap.md)
- [papers/SSV-I/trefoil-breather-minimisation-plan.md](../../papers/SSV-I/trefoil-breather-minimisation-plan.md)

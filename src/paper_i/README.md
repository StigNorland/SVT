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
| `trefoil_breather_static.py` | `candidate` | first concrete static 3D trefoil-breather prototype for `#13` |
| `trefoil_observables.py` | `candidate` | shared observables for the static trefoil prototype and sweeps |
| `trefoil_breather_refinement.py` | `candidate` | first grid / box sensitivity harness for `#13` milestone 4 |
| `trefoil_farfield_profile.py` | `candidate` | radial outer-density diagnostic for saved trefoil states |
| `trefoil_farfield_compare.py` | `candidate` | profile-to-profile far-field comparison helper |
| `alpha_g_proxy.py` | `candidate` | first conservative bridge from static far-field diagnostics to the proton acoustic monopole suppression track in issue `#14` |
| `cq_geometry_proxy.py` | `candidate` | first geometry-level constraint extractor for the unresolved monopole calibration in issue `#14` |
| `cq_geometry_compare.py` | `candidate` | comparison harness for geometry-level monopole-calibration diagnostics across saved states |
| muon / BdG scripts | `prototype` | reduced spectral experiments, not closure evidence |
| Kelvin / chiral bridge scripts | `prototype` | exploratory coupling structure only |

## Core Background

- `vortex_profile.py` solves the planar LogSE vortex core profile.
- `toroidal_background.py` defines the leading toroidal vortex-ring background and curvature-corrected variants.
- `curved_torus_relaxation.py` performs a small-basis relaxation of curvature corrections.
- `toroidal_projection_integrals.py` computes projected stiffness, norm, and chiral-shear integrals.
- `trefoil_breather_static.py` seeds and relaxes a first static 3D trefoil-breather prototype.
- `trefoil_observables.py` centralises the early static-branch observables.
- `trefoil_breather_refinement.py` compares early observables across grid and box settings.
- `trefoil_farfield_profile.py` reads a saved relaxed state and reports radial shell-averaged density/deficit.
- `trefoil_farfield_compare.py` compares two saved radial far-field profile JSON files.
- `alpha_g_proxy.py` extracts provisional estimators for the proton acoustic monopole suppression from static sweep JSON artifacts.
- `cq_geometry_proxy.py` extracts deficit-volume and compactness diagnostics from saved static states for the later `Q_p` calibration path.
- `cq_geometry_compare.py` compares the saved geometry diagnostics across coarse and fine representative states.
- `trefoil_breather_refinement.py` now also reports deficit-volume and compactness-style geometry summaries for gravity-branch comparison.
- `q_p_two_factor_probe.py` compares simple reduced two-factor `Q_p` candidates against shell deficit alone.
- `q_p_two_factor_scan.py` scans the additive saturating reduced `Q_p` family over a small coefficient range.

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
python src/paper_i/trefoil_breather_static.py --n 40 --max-steps 100
python src/paper_i/trefoil_breather_refinement.py --n-values 24,32 --half-width-values 5,6 --max-steps 30
python src/paper_i/trefoil_farfield_profile.py papers/SSV-I/data/example-trefoil-state.npz --bins 16
python src/paper_i/trefoil_farfield_compare.py papers/SSV-I/data/profile-a.json papers/SSV-I/data/profile-b.json
python src/paper_i/alpha_g_proxy.py papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-2026-05-06.json
python src/paper_i/cq_geometry_proxy.py papers/SSV-I/data/trefoil-state-n24-hw5-200steps-2026-05-06.npz
python src/paper_i/cq_geometry_compare.py papers/SSV-I/data/cq-geometry-n24-hw5-200steps-2026-05-06.json papers/SSV-I/data/cq-geometry-n48-hw7-400steps-2026-05-06.json
python src/paper_i/muon_mode_prototype.py
python src/paper_i/kelvin_self_induction.py --phi-n 64
```

These scripts are exploratory or reduced-validation support code, not final production simulations.

For the actual static closure track, see:

- [docs/numerical-minimisation-roadmap.md](../../docs/numerical-minimisation-roadmap.md)
- [papers/SSV-I/trefoil-breather-minimisation-plan.md](../../papers/SSV-I/trefoil-breather-minimisation-plan.md)

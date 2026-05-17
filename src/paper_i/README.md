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
| `q_p_two_factor_pure_additive_local_scan.py` | `candidate` | pure additive local-geometry Q_p scan for issue `#14` |
| `trefoil_y_junction_static.py` | `prototype` | first open three-prong Y-junction relaxation for `N_Y` / `F` on issue `#13` |
| `trefoil_y_junction_observables.py` | `prototype` | first `N_Y` / `F` extractor with self-calibration on saved Y-junction states |
| `trefoil_y_junction_refinement.py` | `prototype` | first grid + box sensitivity sweep for the Y-junction track |
| `trefoil_y_junction_closed_static.py` | `prototype` | closed-topology theta-graph Y-junction prototype to remove the open-Y `F` divergence |
| `trefoil_y_junction_closed_observables.py` | `prototype` | arc-aware `N_Y` / `F` extractor for closed theta-graph states (revealed `+3` monopole instability of the symmetric seed) |
| `trefoil_breather_observables.py` | `prototype` | single-curve `N_Y` / `F` extractor for the `(2,3)`-trefoil-knot states from `trefoil_breather_static.py` |
| `trefoil_y_junction_closed_asym_static.py` | `prototype` | asymmetric `(+1,+1,-1)` closed Y-junction; first multi-filament configuration with stable seeded geometry and finite `F^int` |
| `trefoil_y_junction_closed_asym_refinement.py` | `prototype` | first grid + box sensitivity sweep for the asymmetric closed Y-junction track |
| `trefoil_y_junction_closed_asym_lperp_static.py` | `prototype` | asymmetric closed Y-junction with the `L_perp` chiral non-local shear term added to the relaxation gradient |
| `trefoil_breather_lperp_static.py` | `prototype` | `(2,3)`-trefoil knot relaxation with `L_perp` added; binary test of whether L_perp at reachable couplings prevents dissolution |
| `lperp_helpers.py` | `prototype` | shared L_perp gradient + energy helpers used by the per-geometry L_perp scripts |
| `lperp_implicit_helpers.py` | `prototype` | FFT-based semi-implicit step for L_perp; unlocks the paper's `lambda = 2000` regime |
| `trefoil_y_junction_closed_asym_lperp_implicit_static.py` | `prototype` | asym closed Y-junction with L_perp via semi-implicit time stepping |
| `trefoil_breather_lperp_implicit_static.py` | `prototype` | trefoil knot + L_perp via semi-implicit stepping; first **stable** closed-knot configuration in the repo |
| `lperp_krylov_helpers.py` | `prototype` | matrix-free GMRES + FFT left-preconditioner for fully implicit Krylov L_perp solver |
| `trefoil_breather_lperp_krylov_static.py` | `prototype` | trefoil + L_perp via true-Jacobian Krylov implicit step; 100x deeper cores than FFT-only |
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
- `q_p_two_factor_normalized_scan.py` tests a branch-normalized variant of the additive saturating reduced `Q_p` family.
- `q_p_two_factor_reexpress_scan.py` tests geometry-tied re-expressions of the additive saturating reduced `Q_p` family.
- `q_p_two_factor_local_scale_scan.py` tests run-local geometric re-expressions of the additive saturating reduced `Q_p` family.
- `q_p_two_factor_pure_additive_local_scan.py` tests the same local geometric scales purely additively, with no `Pi_shell` multiplier on the correction term.
- `trefoil_y_junction_static.py` relaxes the open three-prong Y-junction (three vortex filaments meeting at a central node, 120 deg apart in the equatorial plane) using a product-vortex ansatz with initial-state boundary anchoring.
- `trefoil_y_junction_observables.py` extracts `mu_0_grid`, `E_filaments`, `E_node`, `E_bulk_residual`, `N_Y`, and `F` from a saved Y-junction state, with self-calibration from straight filament sections of the same state.
- `trefoil_y_junction_refinement.py` runs the relaxation + extraction across a `(n, half_width)` grid for the Y-junction track and tabulates the refinement-gate observables.
- `trefoil_y_junction_closed_static.py` relaxes a closed theta-graph Y-junction (three arcs in meridian planes connecting two Y-nodes on the `z`-axis), the compact-closed analogue of the open three-prong Y.
- `trefoil_y_junction_closed_observables.py` extracts `N_Y`, `F`, and energy decomposition from a saved closed Y-junction state using arc-aware tube assignment and two node balls.
- `trefoil_breather_observables.py` extracts `N_Y`, `F`, and energy decomposition (line tube + cavity ball + bulk residual) from a saved `(2,3)`-trefoil-knot state.
- `trefoil_y_junction_closed_asym_static.py` relaxes the asymmetric `(+1, +1, -1)` closed Y-junction; one sign flip in the phase ansatz removes the `+3` monopole fission instability that destroyed the symmetric seed.
- `trefoil_y_junction_closed_asym_refinement.py` runs the asymmetric-closed-Y relaxation + extraction across a `(n, half_width)` grid and tabulates the refinement-gate observables.
- `trefoil_y_junction_closed_asym_lperp_static.py` adds the `L_perp = (lambda / 2) integral |curl j|^2` energy term to the asymmetric closed Y-junction relaxation; first implementation of the chiral non-local shear sector in the repo.
- `trefoil_breather_lperp_static.py` adds `L_perp` on top of the `(2,3)`-trefoil knot initial condition; tested whether the chiral non-local shear term prevents the curvature-driven dissolution we observed at `lambda = 0`.
- `lperp_helpers.py` provides shared `grad_psi`, `current`, `curl3`, `lperp_energy`, `lperp_gradient` functions used by the per-geometry L_perp scripts.
- `lperp_implicit_helpers.py` provides `fourier_k_squared` and `semi_implicit_step`: an FFT-based semi-implicit Euler step that absorbs the L_perp leading stiffness (approximated as `lambda * (-Laplacian)^2`) into the implicit operator.
- `trefoil_y_junction_closed_asym_lperp_implicit_static.py` runs the asymmetric closed Y-junction with semi-implicit L_perp stepping; reaches the paper's `lambda = 2000` regime.
- `trefoil_breather_lperp_implicit_static.py` runs the `(2,3)`-trefoil knot with semi-implicit L_perp stepping; produces the first stable closed-knot configuration in the repo.
- `lperp_krylov_helpers.py` provides matrix-free GMRES + FFT left-preconditioner. Used by the Krylov-implicit static scripts to solve the linearised backward-Euler equation `(I + dt J_true) dpsi = -dt g_full` without scipy.
- `trefoil_breather_lperp_krylov_static.py` runs the trefoil + L_perp with true-Jacobian Krylov-implicit stepping; deepest stable cores in the repo (`min_rho ~ 2.5e-3` at `lambda = 2000`), and the first configuration whose `F^int` matches the paper's quoted order of magnitude.

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
python src/paper_i/q_p_two_factor_reexpress_scan.py papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-geom-2026-05-06.json papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-geom-2026-05-06.json
python src/paper_i/q_p_two_factor_local_scale_scan.py papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-geom-2026-05-06.json papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-geom-2026-05-06.json
python src/paper_i/q_p_two_factor_pure_additive_local_scan.py papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-geom-2026-05-06.json papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-geom-2026-05-06.json
python src/paper_i/trefoil_y_junction_static.py --n 24 --half-width 6 --max-steps 200
python src/paper_i/trefoil_y_junction_observables.py papers/SSV-I/data/y-junction-state-n24-hw6-200steps-2026-05-16.npz
python src/paper_i/trefoil_y_junction_refinement.py --n-values "24,32" --half-width-values "5,6"
python src/paper_i/trefoil_y_junction_closed_static.py --n 24 --half-width 6 --max-steps 200
python src/paper_i/trefoil_y_junction_closed_observables.py papers/SSV-I/data/y-junction-closed-state-n24-hw6-200steps-2026-05-17.npz
python src/paper_i/trefoil_breather_observables.py papers/SSV-I/data/trefoil-state-n48-hw5-400steps-2026-05-06.npz
python src/paper_i/trefoil_y_junction_closed_asym_static.py --n 24 --half-width 6 --max-steps 200
python src/paper_i/trefoil_y_junction_closed_asym_refinement.py --n-values "24,32" --half-width-values "5,6"
python src/paper_i/trefoil_y_junction_closed_asym_lperp_static.py --n 24 --half-width 6 --max-steps 200 --lambda-perp 10 --step-size 0.002
python src/paper_i/trefoil_breather_lperp_static.py --n 24 --half-width 6 --max-steps 400 --lambda-perp 10 --step-size 0.002
python src/paper_i/trefoil_y_junction_closed_asym_lperp_implicit_static.py --n 24 --half-width 6 --max-steps 200 --lambda-perp 2000
python src/paper_i/trefoil_breather_lperp_implicit_static.py --n 24 --half-width 6 --max-steps 800 --lambda-perp 2000
python src/paper_i/trefoil_breather_lperp_krylov_static.py --n 24 --half-width 6 --max-steps 200 --lambda-perp 2000
python src/paper_i/muon_mode_prototype.py
python src/paper_i/kelvin_self_induction.py --phi-n 64
```

These scripts are exploratory or reduced-validation support code, not final production simulations.

For the actual static closure track, see:

- [docs/numerical-minimisation-roadmap.md](../../docs/numerical-minimisation-roadmap.md)
- [papers/SSV-I/trefoil-breather-minimisation-plan.md](../../papers/SSV-I/trefoil-breather-minimisation-plan.md)

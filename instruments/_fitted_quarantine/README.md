# Quarantined: fitted / calibrated / falsified-ladder scripts

**Do not cite results from anything in this folder as a parameter-free or
first-principles SSV prediction.** These scripts either (a) back-solve a free
constant to a known experimental target, (b) select a "provisional" constant by
a consistency criterion rather than deriving it, or (c) implement the
alpha-harmonic muon/lepton mass ladder that was falsified as a dynamical
spectrum in `papers/SSV-I/path-b-eigenvalue-result.md`.

Moved here 2026-05-30 per the approved audit `papers/fitting-cleanup-audit.md`.
History is preserved (`git mv`), so past results remain reproducible by
checking out earlier commits or copying a script back into `instruments/paper_i/`.
Tracking issue: GitHub #66.

Additional SSV-VI-a exploratory material was moved here on 2026-06-09 after the
Paper VI-a calculation audit.  The live calculation is
`instruments/paper_vi_a/derive_C.py`; the quarantined
`paper_vi_a/calibration_analysis_failed_exploration.py` contains older
flat-velocity, healing-length, and acoustic-matching routes that miss the
observed calibration constant by many orders of magnitude.  The quarantined
`paper_vi_a/calculate_velocity_profile_toy_vortex.py` is a toy vortex-drag
plotter and is not the SSV-VI-a rotation-curve model.  Neither should be cited
as support for the manuscript.

## Why these are not derivations

### Ladder / muon (falsified by Path B)

Path B solved the committed L+L_perp toroidal-breather BdG spectrum honestly
and pre-registered the decision rule. Result: the muon hits omega/omega_c =
0.207 only in the single published `helicity` basis and drifts +-13% (or
vanishes) under Galerkin basis enrichment; the charged-pion rung (2 mu0) is
absent in every basis; the spectrum is not evenly spaced. The "ladder" is
therefore a two-coincidence numerology (mu, pi+- near 3/2 and 2 times
m_e/alpha), not a derived eigenmode spectrum. Path A statistics and Path B
write-up live in `papers/SSV-I/`.

Quarantined ladder / muon scripts:

- `paper_i/muon_mode_prototype.py` -- hardcodes `muon_ratio_draft = 0.207` and
  contains `coupling_for_target_lower_root` / `coupling_for_target_upper_root`:
  explicit back-solvers of the two-mode coupling G to the muon target. Its
  legitimate constants (alpha, m_e, mu0 = m_e/alpha) are inlined where still
  needed (e.g. the Path B probe) rather than imported from here.
- `paper_i/harmonic_ladder_spectrum.py` -- scores the BdG spectrum against
  half-integer rungs of the muon-derived `mu0_ratio`;
  `nearest_half_integer_rung` is look-elsewhere snapping in code.
- `paper_i/projected_two_mode_eigen.py` -- prints omega / target vs the muon
  draft.
- `paper_i/thin_ring_delta_relax_sweep.py` -- produces `delta_relax = +0.038`,
  the tuning that pulls lambda_perp so the muon lands on 0.207.
- `paper_i/muon_lambda_band_sweep.py`, `muon_branch_identity_tracking.py`,
  `muon_cubic_self_energy.py`, `muon_cubic_full_self_energy.py`,
  `kelvin_branch_tracking.py`, `chiral_kelvin_sweep.py` -- muon-target
  eigenmode support (track / sweep the hybrid core+Kelvin branch toward 0.207).
- `paper_i/arnold_tongue_scan.py`, `canonical_four_mode.py` -- additional
  scripts that scored their eigenvalues against `muon_ratio_draft`; surfaced
  during the live-tree import audit.

Two shared infrastructure files that *also* printed a muon-target diagnostic
were KEPT live (their reusable helpers are used by `direct_bdg_projection.py`
and the Path B probe), with the `muon_ratio_draft`-dependent print blocks
stripped from their `main()`:

- `instruments/paper_i/restricted_bdg_matrix.py` -- the "Muon target comparison"
  block in `main()` was removed; everything else unchanged.
- `instruments/paper_i/restricted_bdg_three_mode.py` -- the closing
  `target omega_mu/omega_c` / `closest/target` lines in `main()` were
  removed; everything else unchanged.

### Proton Q_p two-factor calibration (recompute dependents)

These set the proton sector's reduced Q_p / eta factor by calibration, not
derivation. Their own docstrings say so ("eta remains a provisional
consistency-based calibration rather than a derived physical constant").

- Calibration: `paper_i/q_p_two_factor_eta_calibration.py`,
  `q_p_two_factor_eta_shape_calibration.py`,
  `q_p_two_factor_calibrated_checkpoint.py`.
- Exploratory scans of the same un-derived ansatz (moved together, per audit
  Q2): `q_p_two_factor_scan.py`, `q_p_two_factor_probe.py`,
  `q_p_two_factor_normalized_scan.py`, `q_p_two_factor_reexpress_scan.py`,
  `q_p_two_factor_local_additive_scan.py`,
  `q_p_two_factor_local_modulated_scan.py`,
  `q_p_two_factor_local_scale_scan.py`,
  `q_p_two_factor_pure_additive_local_scan.py`,
  `q_p_cumulative_curve_compare.py`, `q_p_halo_window_scan.py`,
  `q_p_source_mechanism_probe.py`, `q_p_preboundary_plateau_check.py`.

## What stayed in `instruments/paper_i/` (and why)

Genuine validation / diagnostics that report honest error bars and do NOT set
a constant by fitting were kept live: `f_vs_r_cutoff_scan.py` (exposes the
F-factor cutoff sensitivity -- it is the evidence that the proton F is not
converged), `q_p_convergence_audit.py`, `q_p_constraint_sensitivity.py`,
`q_p_kernel_integral.py`, `q_p_static_potential.py`,
`static_closure_cutoff_invariance_sweep.py`,
`validation_sweep_restricted_bdg.py`, `trefoil_state_continuation_sweep.py`,
and the shared operator machinery (`kelvin_augmented_bdg.py`,
`restricted_bdg_matrix.py`, `restricted_bdg_three_mode.py`,
`toroidal_projection_integrals.py`, `toroidal_background.py`,
`direct_bdg_projection.py`, `thin_ring_alpha_correction.py`,
`curved_torus_relaxation.py`). The Path B reproduction
`path_b_spectrum_probe.py` is also live and self-contained.

## Running these for historical audit

Scripts that import shared operator machinery (e.g. `kelvin_augmented_bdg`)
will not run from this folder as-is, because that machinery stays in
`instruments/paper_i/`. To reproduce a past fitted number, either `git checkout` the
commit before the move (2026-05-30), or copy the script back into
`instruments/paper_i/` temporarily. They are kept for provenance, not for live use.

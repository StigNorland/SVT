# Fitting / calibration cleanup audit (2026-05-30)

**Status: PROPOSAL FOR APPROVAL. Nothing has been moved, deleted, or edited
yet.** This is the inventory you asked to see before any cleanup. It classifies
every script that touches fitting/calibration/target-back-solving, lists the
paper claims that rest on each, and proposes a per-item action. Once you approve
(in whole or with edits), I execute the moves + README + paper edits + tracking
issue.

## Method / classification rule

I separated three categories, because they must NOT be treated alike:

- **FIT** = the script back-solves a free constant to a known experimental
  target, or selects a "provisional" constant by a consistency criterion. These
  are not derivations. *Action: move to a quarantine folder; dependent non-ladder
  results must be recomputed without them.*
- **LADDER** = part of the muon/charged-lepton alpha-harmonic ladder claim that
  Path B already falsified (`papers/SSV-I/path-b-eigenvalue-result.md`). *Action:
  governed by the Path B null, NOT recomputed. Quarantine + cite the null.*
- **KEEP** = genuine validation: convergence, cutoff-invariance, sensitivity, or
  robustness sweeps that report honest error bars and do not set a constant by
  fitting. *Action: leave in place.*

The distinction between FIT and KEEP is the load-bearing judgement here; I have
erred toward flagging, and each KEEP is justified below so you can overrule.

---

## Tier LADDER — muon / charged-lepton ladder (already falsified by Path B)

These produce or score the muon = 3/2 mu0 ladder. Path B showed the result is
basis-dependent and the pion rung is absent. Do NOT recompute; quarantine and
point to the Path B null.

| Script | Why it's ladder/fit | Note |
|--------|---------------------|------|
| `instruments/paper_i/muon_mode_prototype.py` | hardcodes `muon_ratio_draft = 0.207`; contains `coupling_for_target_lower_root` / `_upper_root` — explicit back-solvers of the coupling G to the muon target | core of the ladder claim |
| `instruments/paper_i/harmonic_ladder_spectrum.py` | classifies BdG spectrum against half-integer rungs of the muon-derived `mu0_ratio`; `nearest_half_integer_rung` is look-elsewhere snapping | Path B driver |
| `instruments/paper_i/projected_two_mode_eigen.py` | prints `omega/target` against `muon_ratio_draft` | diagnostic of the same target |
| `instruments/paper_i/thin_ring_delta_relax_sweep.py` | produces `delta_relax = +0.038`, the tuning that pulls lambda_perp so the muon lands on 0.207 | calibration feeding the ladder |
| `instruments/paper_i/muon_lambda_band_sweep.py` | sweeps lambda band around the muon target | ladder-support |
| `instruments/paper_i/muon_branch_identity_tracking.py` | tracks the muon eigen-branch | ladder-support |
| `instruments/paper_i/muon_cubic_self_energy.py`, `muon_cubic_full_self_energy.py` | muon self-energy toward the target | ladder-support |
| `instruments/paper_i/kelvin_branch_tracking.py`, `chiral_kelvin_sweep.py` | track/sweep the Kelvin hybrid branch used to reach 0.207 | ladder-support |

Dependent paper text (governed by Path B null, to be rewritten, not recomputed):
- `papers/SSV-I/main.tex` §leptons / mass-ladder lines ~102, 147–148 ("muon mass
  to 0.6% ... without free parameters"), and the muon open-problem section.
- `papers/SSV-II/main.tex` abstract+intro lines ~147–148 (same ladder claim
  inherited).
- All `papers/SSV-I/notes/muon-*.md` and `papers/SSV-I/muon-*.md` working notes.

---

## Tier FIT — non-ladder calibrations (recompute dependents WITHOUT them)

These set the **proton** sector's free factors by calibration, not derivation.
This is the part your instruction targets: "all calculations that have used them
(and are not part of the ladder claim) need to be done again."

| Script | Why it's a fit | Self-flagged? |
|--------|----------------|---------------|
| `instruments/paper_i/q_p_two_factor_eta_calibration.py` | "choose a provisional eta ... does not derive a physical coupling constant" | yes, in docstring |
| `instruments/paper_i/q_p_two_factor_eta_shape_calibration.py` | shape-calibration of the same eta | by name |
| `instruments/paper_i/q_p_two_factor_calibrated_checkpoint.py` | "eta remains a provisional consistency-based calibration rather than a derived physical constant" | yes, in docstring |

Exploratory scans of the same **non-derived** two-factor Q_p ansatz (they do not
themselves fit, but they exist only to explore the un-derived ansatz family and
have no standalone validation value):

- `q_p_two_factor_scan.py`, `q_p_two_factor_probe.py`,
  `q_p_two_factor_normalized_scan.py`, `q_p_two_factor_reexpress_scan.py`,
  `q_p_two_factor_local_additive_scan.py`,
  `q_p_two_factor_local_modulated_scan.py`,
  `q_p_two_factor_local_scale_scan.py`,
  `q_p_two_factor_pure_additive_local_scan.py`,
  `q_p_cumulative_curve_compare.py`, `q_p_halo_window_scan.py`,
  `q_p_source_mechanism_probe.py`, `q_p_preboundary_plateau_check.py`.
  *Proposed: quarantine with the calibration trio (they are the search that the
  calibration summarises). Flag for your confirmation — see Open Questions Q2.*

Dependent NON-ladder paper claims that must be **recomputed** (or demoted) if
their inputs were calibrated:
- **Proton mass** `m_p = N_Y F mu0` (SSV-I §proton; F approx 4.47 at R=1.18 xi).
  Note SSV-I already concedes (lines ~603, 1604) that F "requires a grid-invariant
  calibration" and is "not grid-converged." So this is half-acknowledged already.
- **`m_p/m_pi = N_Y F / 2 approx 6.72`** (SSV-II §Higgs, closure #34 in
  `papers/numerical-closures-report.md`) — inherits F.
- **`alpha(m_p/m_e) = N_Y F`** consistency identity (closure #34) — inherits F.
- **Newton's constant consistency** `G = alpha_G hbar c alpha^2/(N_p^2 m_e^2)`
  "matches the mass ladder to 0.6%" (SSV-II §gravity) — inherits both F and the
  ladder mu0; already labelled "consistency check, not derivation."

---

## Tier KEEP — genuine validation (leave in place)

Each of these reports robustness/convergence/error-bars and does NOT set a
constant by fitting. Justification given so you can overrule any.

| Script | Why it is validation, not fitting |
|--------|-----------------------------------|
| `instruments/paper_i/f_vs_r_cutoff_scan.py` | quantifies F's cutoff sensitivity *to put an honest error bar on the proton mass* — this is the diagnostic that EXPOSES the F calibration, keep it as evidence |
| `instruments/paper_i/q_p_convergence_audit.py` | "audits saved states only; does not improve the solver" — pure convergence audit |
| `instruments/paper_i/static_closure_cutoff_invariance_sweep.py` | Issue #13 cutoff-invariance post-processing |
| `instruments/paper_i/validation_sweep_restricted_bdg.py` | "Status: validation" — grid/box refinement stability |
| `instruments/paper_i/q_p_static_potential.py` | static-source diagnostic from saved states (Green's function), no fit |
| `instruments/paper_i/q_p_convergence_audit.py`, `trefoil_state_continuation_sweep.py` | convergence of delta V_p / Q_p |
| `instruments/paper_i/q_p_constraint_sensitivity.py`, `q_p_kernel_integral.py` | sensitivity / kernel diagnostics |
| `instruments/paper_ii/*` (g2_form_factor_loop, tau_identification, vortex_cap_mass, proton_breather_1d, chiral_cap_equilibrium, reconnection_*) | structural/loop calculations and identifications; none back-solve a free constant. tau uses the *ladder* mu_mu as an input though — see Q3 |
| `instruments/paper_v/`, `vi_a/`, `vi_b/`, `vii_b/`, `viii/`, `iv/` | galaxy/BH/KZ/deflection; `calibration_analysis.py` *verifies* an empirical constant across galaxies (anchor, not a fit of SSV theory) — but flag Q4 |

---

## Proposed execution (after your approval)

1. Create `instruments/_fitted_quarantine/` (keeps imports findable; out of the live
   tree). Move all Tier FIT + Tier LADDER scripts there, preserving
   subpaths (`paper_i/...`). Use `git mv` so history follows.
2. Write `instruments/_fitted_quarantine/README.md`: what each script fit, what target,
   why it is not a derivation, and the pointer to Path B + this audit.
3. Mark dependent claims in the papers:
   - LADDER claims: rewrite to the Path B null wording (muon = lowest mode of one
     truncated basis near 0.207, NOT a converged parameter-free prediction; pion
     != rung 2 dynamically; "alpha-harmonic ladder" demoted to numerology).
   - FIT (proton) claims: tag each dependent number with a gapbox noting its
     input was calibrated and is pending recomputation.
4. Tracking issue: **#66** (https://github.com/StigNorland/SVT/issues/66),
   linked from umbrella #30, enumerating each dependent calculation with the
   quarantined script it must be weaned off.
5. Leave Tier KEEP untouched.

---

## Open questions for you (before I execute)

- **Q1 — quarantine vs delete.** You said "move to a separate folder." Confirm
  `instruments/_fitted_quarantine/` (reversible, keeps reproducibility of past claims) vs
  a hard delete.
- **Q2 — the ~12 `q_p_two_factor_*` scan scripts.** Quarantine them with the
  calibration trio (my recommendation, since they only explore the un-derived
  ansatz), or keep them as exploration history?
- **Q3 — the tau.** `tau_identification.py` / SSV-II §Tau use `m_mu` as a binding
  quantum (`m_tau = 2 m_p - m_mu`). That imports the ladder muon. Recompute as a
  dependent, or treat the tau's use of the *measured* muon mass as legitimate
  (it cites PDG values, not the 0.207 eigenmode)?
- **Q4 — galaxy `calibration_analysis.py` (SSV-VI-a).** It calibrates C against
  galaxies. In or out of scope? (My read: out — it's an empirical astro anchor,
  not a fit of SSV's own free constant — but you decide.)
- **Q5 — recompute scope.** "Done again" for the proton F-factor means deriving
  a grid-invariant F from first principles (hard, possibly open). Acceptable
  interim: demote the affected numbers to gapboxes pending that derivation,
  rather than block on a derivation that may not exist yet?

# Path B pre-registration: does the L+L_perp spectrum produce the muon AND pion rungs?

**Date:** 2026-05-30. Written BEFORE inspecting any new spectrum output, so the
decision rule cannot be tuned to the result. Companion to the Path A statistical
scan (which found the "14-particle ladder" is carried by exactly two particles,
pi+- and mu, at ~1-in-50-to-1000 under the null depending on look-elsewhere).

## What Path A handed to Path B

Path A's honest verdict: only two rungs are statistically supported -- the muon
at 3/2 mu0 and the charged pion at 2 mu0, on the parameter-free leptonic mass
scale mu0 = m_e/alpha = 70.02 MeV. Everything beyond those two is filler. So
Path B does not need the whole table; it needs *those two specific rungs* to
fall out of a dynamical eigenvalue solve without hand-insertion.

## The operator (no new freedom introduced)

The toroidal breather BdG operator already implemented in
`src/paper_i/kelvin_augmented_bdg.py::build_bdg`:

    H = [[ L,  M ], [ -M*, -L* ]]

with L = -1/2 nabla^2_cyl + (log|psi0|^2 + 1) (profile-logse model), plus the
projected current-curl block scaled by lambda_perp, plus the Kelvin
self-induction shift. Background psi0 from `restricted_bdg_matrix.build_background`.

I will run it through `src/paper_i/harmonic_ladder_spectrum.py` with its
**committed default parameters** and will NOT adjust lambda_perp, delta_relax,
kelvin_core_radius, kelvin_phi_n, the grid, or any other knob to improve the
result. If I vary anything it is only to test convergence/robustness, reported
in both directions.

## The circularity I must not hide

The yardstick `mu0_ratio = (2/3) * muon_ratio_draft = (2/3)*0.207 = 0.138` is
DERIVED FROM the muon target 0.207, which is itself hardcoded
(`muon_mode_prototype.py:34`). The repo's own paper-ready note is candid that
the muon point reaches 0.207 only via a tuned `delta_relax=0.038` and cross-m
current-curl terms its author flags as spurious (selection-rule-violating). So:

- Landing one eigenvalue near 0.207 proves NOTHING -- it was calibrated to.
- The non-circular content is entirely in the SECOND rung and the SPACING.

## Pre-registered decision rule

The operator scale is set by the L, L_perp and Kelvin blocks; mu0_ratio=0.138
does NOT enter `build_bdg`, it is only a classification yardstick. So I test:

**Primary (the decisive question, lifted verbatim from the repo's own open
question, muon-paper-ready-section.md:54):** With parameters held at the muon
calibration, does the stable spectrum contain a SECOND distinct stable
(real, |Im|<1e-5, positive) eigenfrequency near rung 2 (omega/omega_c ~ 0.276),
in addition to the muon mode near rung 3/2 (~0.207)?

  - PASS: two distinct stable modes, one within 5% of 0.207 and one within 5%
    of 0.276, with no comparably-good stable mode at a non-rung location
    between them.
  - FAIL: only one stable mode (the calibrated muon), OR a dense thicket of
    stable modes with no preference for rungs (then "nearest-rung" hits are
    look-elsewhere artifacts, not a ladder).

**Secondary (non-circular scale check):** Is the rung SPACING an output, not an
input? Specifically, is the gap between the first and second stable rung-modes
approximately equal to mu0_ratio=0.138 (i.e. half the muon frequency), WITHOUT
mu0_ratio having been fed to the operator? Even spacing of >=2 stable modes is
the signature of a real ladder; uneven spacing falsifies "harmonic series."

**Tertiary (robustness):** Does the second-mode result survive turning OFF the
admitted-spurious cross-m current-curl terms, and does it survive a grid change?
If the second rung only exists with the spurious terms, it is an artifact.

## Outcome commitment

- Two clean rungs at 3/2 and 2 with ~0.138 spacing, surviving the robustness
  checks -> Path B confirms a genuine (two-rung) leptonic ladder. Report it.
- One mode only, or rungs that vanish without the spurious terms -> the ladder
  is a single calibrated point. Drop the spectrum interpretation cleanly, as
  the repo's own note 5 (line 58) already anticipates.

Either way the result is reported straight, including which knobs were on.

---

**EXECUTED 2026-05-30.** Outcome: FAIL. The muon hits 0.207 only in the single
published `helicity` basis and drifts +-13% (or vanishes) under Galerkin
enrichment -- not converged. The pion window is empty in all four bases. The
spectrum is not evenly spaced. Neither carrier survives as a genuine
eigenfrequency. Full write-up: `path-b-eigenvalue-result.md`.

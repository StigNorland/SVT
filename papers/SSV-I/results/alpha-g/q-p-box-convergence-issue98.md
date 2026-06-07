# Q_p box-convergence gate — alpha_G stays blocked (#98)

**Issue:** #98 · **Date:** 2026-06-07 · **Branch:** `issue-98-qp-box-convergence`
**Driver:** `instruments/paper_i/q_p_box_convergence.py`
**Test:** `instruments/test/paper_i/test_q_p_box_convergence.py`
**Reuses:** `q_p_static_potential.py` (free-space screened-Green's-fn far field), saved
#77 static states. **Related:** #14 (alpha_G status), #108 (the box-contamination lesson).

## Pre-registration

Per plan `quiet-inventing-hare` (approved): before mapping the #77 static trefoil
geometry to `Q_p` → `alpha_G`, gate the `Q_p` far-field estimators on a **box-sweep**
(vary `half_width` at fixed dx), a **grid-sweep** (vary `n` at fixed box), and a
**shell plateau**, applying the #108 lesson that grid-refinement at fixed box can mask
box-contamination. **Decision rule:** PASS (all spreads `< 5%`, pedestal a small
fraction of the charge) → attempt `Q_p → alpha_G` as candidate/bounded. FAIL (any
estimator tracks the box, or the charge is background-dominated) → `alpha_G` stays
blocked. Honest negative is a valid closure (rule 1).

## Result — FAIL on every axis (from existing saved states; no new solves needed)

`deficit_volume = ∫(1-|ψ|²)dV` (the `Q_p^LW` charge) and the free-space asymptotic
`1/r` coefficient, across the matched saved families:

| family (fixed) | sweep | deficit_volume | spread |
|---|---|---|---|
| trefoil, n=48 | hw 5,6,7 | 115.7, 90.7, 61.5 | **60.7%** |
| y-junction, n=48 | hw 5,6,7,8 | 185.9, 256.2, 334.4, 419.1 | **78.0%** |
| gradient-flow, hw6 (#77 ref) | n 48,72,96,128,160 | 276.8, 281.8, 294.8, 291.5, 212.9 | **30.1%** |

- **Box axis** (the decisive one): `Q_p` swings **60–78%** across `hw5–8`, and the
  trend **reverses** between the trefoil (falls with box) and y-junction (rises with
  box) ansätze — the opposite of a box-stable physical charge.
- **Grid axis**: even at the fixed #77 box `hw6`, the best-relaxed states spread
  **30%** and non-monotonically (`n160` drops to 212). Resolution does not rescue it.

## Mechanism — the charge is a boundary/box-filling pedestal, not the proton

The outer-shell deficit times the box volume, `shell_deficit × (2·hw)³`, **equals or
exceeds** `deficit_volume` (pedestal fraction **1.04–1.37**). I.e. `|ψ|²` is depressed
*toward the box boundary* rather than recovering to 1, and the far-field "monopole
charge" is dominated by this box-filling background — not the localized `R≈2.5ξ`
source. This is the static cousin of the #108 cap tracking the box: the available
boxes (`hw ≤ 8ξ`) provide no clean `source ≪ shell ≪ box` window, so the screened
far field is pedestal-limited.

## Verdict

**`alpha_G` stays BLOCKED.** No raw far-field scalar (`deficit_volume`, `q_p_fit`,
`1 − shell_mean_density`) may be promoted to `Q_p`/`alpha_G` — they are box-pedestal
artefacts, swinging 60–78% with the box. This matches and sharpens the existing
`issue-14-alpha-g-extraction-status` conclusion: the bottleneck is not calibration
(`C_Q`) but a box/boundary-converged source charge, which does not exist in the
current static branch.

## What would unblock it (not pursued here)

Either (a) a **background-subtracting source isolation** (extract the localized charge
after removing the box-filling pedestal — the naive `deficit_volume − pedestal` even
goes slightly negative, so a principled subtraction / multipole projection is needed),
or (b) **hard-BC / large-box** relaxation where the background → 0 (`source ≪ box`).
Both are the static analog of the petascale separation that closed the dynamic
route-C in #108. New solves were **not** run: the existing states already fail the
gate decisively, and resolution/relaxation refinement cannot remove a boundary
pedestal.

## Claim-status (rule 5)

| Claim | Before | After |
|---|---|---|
| `Q_p` from static far field | candidate, "tighten until stable" | **not box-converged** — pedestal-dominated (60–78% box spread) |
| `alpha_G` | blocked | **blocked, with mechanism** — needs pedestal-subtracted source or `source ≪ box`; not a calibration problem |

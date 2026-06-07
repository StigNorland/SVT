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

## Radial decay diagnostic — the moment is formally divergent

After the box-convergence gate, the radial power-law of the outer deficit was
measured by fitting `log(deficit_mean(r)) vs log(r)` in the outer 30–80% of the
half-width:

| State | exponent s (deficit ~ r^s) | convergence requirement |
|---|---|---|
| gradient-flow-n128-hw6-5000steps (best #77 ref) | **−2.88** | need s < −3 |
| trefoil-state-n48-hw7-400steps | **−1.78** | need s < −3 |

For `Q_p = ∫ r² · deficit(r) dr` to converge, the integrand `r² · r^s = r^(s+2)`
must be integrable, i.e. `s+2 < −1`, i.e. `s < −3`. Neither state satisfies this:
the LogSE algebraic healing tail `1−f(r) ~ 1/(4r²)` gives `s ≈ −2` by construction,
so the monopole charge integral **diverges**. This means **no box size yields a
finite, box-independent `Q_p`** — the quantity grows with the box regardless of
resolution. The 60–78% box swings and the pedestal fraction ≥ 1 are therefore
inevitable, not a numerical artefact.

This sharpens the "unblock" requirement: not a bigger computer, but a
**convergent source observable**. The carrier operator `C_Q` (flagged in #14 as
unresolved) must physically suppress the 1/r² tail to produce a convergent
source; `q_p_kernel_integral.py`'s `(a_p/ξ)³` suppression is a candidate but
must be derived, not fitted. Until then, `∫(1−|ψ|²) dV` and its Green's-fn
projection are structurally divergent quantities.

Implementation: `radial_decay_exponent()` in
`instruments/paper_i/q_p_box_convergence.py`; pinned in
`instruments/test/paper_i/test_q_p_box_convergence.py` (asserts s > −3, i.e. the
integral diverges, for the n24-hw6 state).

## Ruled out — Madelung centrifugal subtraction does not restore box-stability

A natural rescue (the ADM-style move) is to split the deficit into a **centrifugal**
part (the circulation depletion from the phase field, `~½|v|²` with `v = ∇θ`, which
should *not* source the long-range acoustic potential) and a **compressional** part
(the genuine density healing, the gravitating source). The hope: the compressional
residual is localized + exponentially decaying, hence box-stable even in a small box.

Tested on the trefoil `hw5,6,7` family:

| quantity | hw5 | hw6 | hw7 | box spread |
|---|---|---|---|---|
| raw deficit | 115.7 | 90.7 | 61.5 | 60.7% |
| compressional residual (`deficit − ½|v|²`) | 67.2 | 57.6 | 37.4 | **55.1%** |
| residual, far shell `[0.4,0.8]·hw` | 42.0 | 32.8 | 20.2 | **68.9%** |

The subtraction removes magnitude but **none of the box-dependence** — the residual
tracks the box at 55% (far shell 69%), essentially the same as the raw 61%/73%. At
`hw ≤ 7ξ` against a `~2.5ξ` loop there is no region simultaneously far from every
vortex strand *and* inside the box, so the local GP balance `½|v|²` is core-
contaminated (its volume integral, 1536 for n128, exceeds the raw deficit) and has no
clean regime to act in. **Confirms the obstruction is scale separation, not the choice
of observable**: no local exterior/interior projector recovers a box-stable `Q_p` at
achievable resolutions. (Prototype only; not promoted to a committed driver.)

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

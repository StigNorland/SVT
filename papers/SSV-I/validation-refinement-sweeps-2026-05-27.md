# Validation refinement and sensitivity sweeps — static branch (2026-05-27)

**Status:** validation result for issue [#16].
**Branch:** static (Paper I).
**Baseline:** `src/paper_i/restricted_bdg_matrix.py` — the restricted 2-mode BdG
diagnostic from projected quadrature Hessians.
**Sweep harness:** `src/paper_i/validation_sweep_restricted_bdg.py`.
**Raw data:** `papers/SSV-I/data/validation-refinement-restricted-bdg-2026-05-27.csv`.

## What was tested

For the restricted 2-mode BdG diagnostic at the reference configuration
`(n=61, half_width=6, profile_n=2400, profile_x_max=20)`, the script varies
one axis at a time and records the reduced observables `omega_minus`,
`omega_plus`, and the underlying A/B block entries. A quantity is reported
as **stable** if its relative spread (max-min)/max across the sweep is
under 1%, otherwise **drifts materially**.

Sweep axes:

| axis              | range              | resolution |
|-------------------|--------------------|-----------:|
| grid `n`          | 21..81             |  6 points  |
| box `half_width`  | 3..8               |  6 points  |
| `profile_n`       | 600..4800          |  4 points  |
| `profile_x_max`   | 15..30             |  4 points  |

## Headline findings

### 1. `omega_minus` is non-real at every sampled point

`omega_minus_sq < 0` for all 18 successful sweep points. The restricted
2-mode subspace (amplitude-R and phase-chi modes) does not contain the
lower BdG branch as a real eigenvalue at any tested resolution. The
quantity `omega_minus` printed by `restricted_bdg_matrix.py` is therefore
**never a real frequency** at the reference geometry — it is `nan` by
construction. This is consistent with the script's own caveat
("the next refinement is direct projection of the differential BdG
operator L/M"), but the implication for paper text is sharper than the
caveat suggests: the lower-branch number from this script is **not a
prediction**, it is a `nan`.

### 2. Reduced observables drift heavily with grid `n` and box `hw`

Relative spread across the grid-refinement sweep
`n = 21, 31, 41, 51, 61, 81` at fixed reference geometry:

| observable    | min            | max            | rel spread | verdict |
|---------------|----------------|----------------|-----------:|---------|
| `omega_plus`  |  5.190766e-01  |  1.390902e+00  |    62.7%   | drifts  |
| `A_RR`        | -2.933881e-01  | -1.939690e-01  |    33.9%   | drifts  |
| `A_Rchi`      |  6.274867e-02  |  8.771340e-02  |    28.5%   | drifts  |
| `A_chichi`    |  6.258958e-01  |  1.430236e+00  |    56.2%   | drifts  |
| `B_RR`        |  3.905204e-01  |  4.103540e-01  |     4.8%   | drifts  |
| `B_Rchi`      |  1.661492e-01  |  1.887088e-01  |    12.0%   | drifts  |
| `B_chichi`    |  1.745853e-01  |  1.920192e-01  |     9.1%   | drifts  |

Relative spread across the box-size sweep
`half_width = 3, 4, 5, 6, 7, 8` at fixed `n=61`:

| observable    | min            | max            | rel spread | verdict |
|---------------|----------------|----------------|-----------:|---------|
| `omega_plus`  |  7.557938e-01  |  2.254584e+00  |    66.5%   | drifts  |
| `A_RR`        | -2.509110e-01  | -7.804321e-02  |    68.9%   | drifts  |
| `A_Rchi`      | -5.821467e-02  |  1.038767e-01  |   156.0%   | drifts  |
| `A_chichi`    |  8.392353e-01  |  2.298321e+00  |    63.5%   | drifts  |
| `B_RR`        |  3.435088e-01  |  4.057075e-01  |    15.3%   | drifts  |
| `B_Rchi`      |  1.384618e-01  |  3.125275e-01  |    55.7%   | drifts  |
| `B_chichi`    | -1.243653e-01  |  2.965990e-01  |   141.9%   | drifts  |

`omega_plus` goes monotonically *down* with increasing box: 2.255 at hw=3
to 0.756 at hw=8. This is the classic signature of a non-converged
spectrum dominated by box-boundary effects: making the box larger lets
the mode spread out, lowering its kinetic-energy density. Doubling the
box halves `omega_plus`. No plateau is visible within the swept range.

### 3. Background-profile parameters are well-converged

Relative spread for `profile_n = 600, 1200, 2400, 4800` (background
vortex-profile grid resolution) and for `profile_x_max = 15, 20`
(profile domain extent — see failure note below):

| sweep            | `omega_plus` spread | verdict |
|------------------|--------------------:|---------|
| `profile_n`      |              0.012% | stable  |
| `profile_x_max`  |              0.000% | stable  |

The 1D background profile solver is converged at `profile_n >= 600`. The
restricted-BdG run does **not** depend materially on background
resolution within the tested range.

### 4. The vortex-profile shooting solver fails at `x_max >= 25`

```
RuntimeError: Could not bracket the vortex shooting slope.
  File "vortex_profile.py", line 79, in find_bracket
```

`vortex_profile.solve` succeeds at `x_max = 15, 20` and fails at
`x_max = 25, 30`. The current shooting setup is at the upper edge of its
own stability boundary at `x_max = 20`. Any future study that needs to
extend the planar profile beyond the unit-circle far-field (for example,
to probe the asymptotic tail more carefully) needs a more robust
shooting harness or a different integration scheme.

## What this means for paper claims

The numbers printed by `restricted_bdg_matrix.py` at any single
`(n, half_width)` are **not** converged predictions of the SSV reduced
BdG spectrum. Specifically:

- `omega_plus` shifts by a factor of ~2.7 across the swept grid range
  and by a factor of ~3.0 across the swept box range.
- `omega_minus` is `nan` at every reference point — the lower BdG
  branch is outside this 2-mode subspace.

The `omega_plus` value at `(n=61, hw=6) = 1.281` should be cited only
as a **diagnostic checkpoint** for the projected-Hessian formulation,
not as a prediction of any physical frequency. The actual muon-mass
predictions for Paper I come from `kelvin_augmented_bdg.py` /
`muon_branch_identity_tracking.py`, which uses an enlarged basis
(10-mode combined: 4 core + 3 Kelvin per sign) and the differential L/M
operator the caveat refers to. Those are the numbers in the paper text;
the restricted 2-mode script is the small-basis validation asset that
fed into that work and remains useful as a fast sanity check, not as a
source of derived numbers.

## Recommendations

1. **Labelling.** Update `src/paper_i/restricted_bdg_matrix.py` with a
   module-level docstring matching the format already used in
   `src/paper_i/curved_torus_relaxation.py`
   (`Status: validation; Problem type: static; Primary observables: ...;
   Primary role: small-basis prototype, not closure-grade evidence`).
   Similarly for `src/paper_i/vortex_profile.py`.

2. **Prototypes summary.** Add a "validation status" line for each
   reduced-problem script in
   `papers/SSV-I/numerical-prototypes-summary.md`, distinguishing
   prototype/validation/derived per the issue. The
   `restricted_bdg_matrix.py` entry should be marked **prototype** with
   a pointer to this memo.

3. **Box-size convergence is the dominant issue.** Future validation
   work on `kelvin_augmented_bdg.py` should swap the existing hw=6
   reference for a converged-in-hw protocol. The matched-spacing-trio
   series already in `papers/SSV-I/data/` partially addresses this, but
   the current memo's box-sweep finding strongly suggests that any
   single-`hw` claim should carry a range bar from at least
   `hw ∈ {5, 6, 7}` matched-spacing runs.

4. **Profile-extent stability.** The shooting-failure at `x_max >= 25`
   is a real numerical limitation. Document it in the
   `vortex_profile.py` docstring and don't request `x_max > 22` from
   downstream callers without first hardening the shooter.

## Falsifiability

If the restricted-BdG `omega_plus` were claimed as a derived prediction,
the box-sensitivity result (factor of ~3 spread across hw=3..8) would
falsify that claim. The framing recommended above (diagnostic
checkpoint, not derived prediction) is consistent with the data.

## Out of scope for this memo

- The dynamic branch baseline (`src/paper_ii/reconnection_supplement.py`)
  is left as follow-up work under issue #16. Scope was static-only this
  session.
- Sensitivity of `kelvin_augmented_bdg.py` to the same axes is partially
  covered by the existing matched-spacing series. A unified
  refinement/sensitivity report for that script (with this memo's
  format) is a natural next step.

[#16]: https://github.com/StigNorland/SVT/issues/16

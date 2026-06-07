# Tube-pinch cap harness pre-registration and exploratory scan (#108)

**Issue:** #108, linked from #97.
**Script:** `instruments/paper_ii/tube_pinch_cap_harness.py`.

## Pre-registration

A cap radius is eligible for a #97 scaling test only if the trace passes
all event markers: opening, localization, an interior peak in cap radius
or cap-plane depletion, and closing/relaxation after the peak. Monotonic
spreading or monotonic healing is an honest negative.

The imposed throat scale is `R0 = kappa sqrt(lambda_perp) xi` unless a
fixed-radius control is requested. Lambda sweeps use canonical `c = 1`
(`log_pressure = 0.5`) and fixed physical duration. Cap localization and
radius use a smooth physical axial weight around the most depleted cap
plane, avoiding a grid-dependent single-slice diagnostic.

## Exploratory scan

| ansatz | lambda_perp | kappa | half-L/R0 | edge | kick | R0 | cap? | peak R | opening | closing | localization | reason |
|---|---:|---:|---:|---:|---:|---:|:---:|---:|---:|---:|---:|---|
| long_tube | 0.5 | 2.5 | 1.25 | 1 | -1.5 | 1.768 | no | 6.038 | 0.719 | 0.000 | 0.140 | no interior cap peak; no closing/relaxation after peak |
| long_tube | 0.5 | 2.5 | 1.25 | 1 | 0 | 1.768 | no | 2.674 | 0.001 | 0.000 | 0.271 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |
| long_tube | 0.5 | 2.5 | 1.25 | 1 | 1.5 | 1.768 | no | 6.038 | 0.719 | 0.000 | 0.140 | no interior cap peak; no closing/relaxation after peak |
| long_tube | 0.5 | 3 | 1.25 | 1 | -1.5 | 2.121 | yes | 5.613 | 0.578 | 0.136 | 0.128 | pass |
| long_tube | 0.5 | 3 | 1.25 | 1 | 0 | 2.121 | no | 2.923 | 0.000 | 0.000 | 0.232 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |
| long_tube | 0.5 | 3 | 1.25 | 1 | 1.5 | 2.121 | yes | 5.613 | 0.578 | 0.136 | 0.128 | pass |
| long_tube | 1 | 2.5 | 1.25 | 1 | -1.5 | 2.500 | no | 7.444 | 0.664 | 0.000 | 0.122 | no interior cap peak; no closing/relaxation after peak |
| long_tube | 1 | 2.5 | 1.25 | 1 | 0 | 2.500 | no | 3.250 | 0.002 | 0.000 | 0.199 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |
| long_tube | 1 | 2.5 | 1.25 | 1 | 1.5 | 2.500 | no | 7.444 | 0.664 | 0.000 | 0.122 | no interior cap peak; no closing/relaxation after peak |
| long_tube | 1 | 3 | 1.25 | 1 | -1.5 | 3.000 | no | 6.637 | 0.491 | 0.000 | 0.104 | cap-plane depletion is not localized enough; no interior cap peak; no closing/relaxation after peak |
| long_tube | 1 | 3 | 1.25 | 1 | 0 | 3.000 | no | 3.642 | 0.002 | 0.000 | 0.167 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |
| long_tube | 1 | 3 | 1.25 | 1 | 1.5 | 3.000 | no | 6.637 | 0.491 | 0.000 | 0.104 | cap-plane depletion is not localized enough; no interior cap peak; no closing/relaxation after peak |
| long_tube | 2 | 2.5 | 1.25 | 1 | -1.5 | 3.536 | no | 7.425 | 0.478 | 0.011 | 0.097 | cap-plane depletion is not localized enough; no interior cap peak; no closing/relaxation after peak |
| long_tube | 2 | 2.5 | 1.25 | 1 | 0 | 3.536 | no | 4.151 | 0.007 | 0.000 | 0.142 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |
| long_tube | 2 | 2.5 | 1.25 | 1 | 1.5 | 3.536 | no | 7.425 | 0.478 | 0.011 | 0.097 | cap-plane depletion is not localized enough; no interior cap peak; no closing/relaxation after peak |
| long_tube | 2 | 3 | 1.25 | 1 | -1.5 | 4.243 | no | 7.770 | 0.407 | 0.026 | 0.107 | cap-plane depletion is not localized enough; no closing/relaxation after peak |
| long_tube | 2 | 3 | 1.25 | 1 | 0 | 4.243 | no | 4.757 | 0.005 | 0.000 | 0.118 | no opening above pre-registered tolerance; cap-plane depletion is not localized enough; no interior cap peak; no closing/relaxation after peak |
| long_tube | 2 | 3 | 1.25 | 1 | 1.5 | 4.243 | no | 7.770 | 0.407 | 0.026 | 0.107 | cap-plane depletion is not localized enough; no closing/relaxation after peak |
| short_cap | 0.5 | 3 | 0.08 | 0.75 | -1.5 | 2.121 | yes | 5.648 | 0.880 | 0.154 | 0.153 | pass |
| short_cap | 0.5 | 3 | 0.08 | 0.75 | 1.5 | 2.121 | yes | 5.648 | 0.880 | 0.154 | 0.153 | pass |
| short_cap | 0.5 | 3 | 0.25 | 0.75 | -1.5 | 2.121 | yes | 5.648 | 0.799 | 0.154 | 0.150 | pass |
| short_cap | 0.5 | 3 | 0.25 | 0.75 | 1.5 | 2.121 | yes | 5.648 | 0.799 | 0.154 | 0.150 | pass |
| short_cap | 1 | 3 | 0.08 | 0.75 | -1.5 | 3.000 | no | 6.637 | 0.831 | 0.000 | 0.136 | no interior cap peak; no closing/relaxation after peak |
| short_cap | 1 | 3 | 0.08 | 0.75 | 1.5 | 3.000 | no | 6.637 | 0.831 | 0.000 | 0.136 | no interior cap peak; no closing/relaxation after peak |
| short_cap | 1 | 3 | 0.25 | 0.75 | -1.5 | 3.000 | no | 6.637 | 0.688 | 0.000 | 0.130 | no interior cap peak; no closing/relaxation after peak |
| short_cap | 1 | 3 | 0.25 | 0.75 | 1.5 | 3.000 | no | 6.637 | 0.688 | 0.000 | 0.130 | no interior cap peak; no closing/relaxation after peak |
| short_cap | 2 | 3 | 0.08 | 0.75 | -1.5 | 4.243 | yes | 7.818 | 0.770 | 0.037 | 0.172 | pass |
| short_cap | 2 | 3 | 0.08 | 0.75 | 1.5 | 4.243 | yes | 7.818 | 0.770 | 0.037 | 0.172 | pass |
| short_cap | 2 | 3 | 0.25 | 0.75 | -1.5 | 4.243 | yes | 7.819 | 0.554 | 0.037 | 0.158 | pass |
| short_cap | 2 | 3 | 0.25 | 0.75 | 1.5 | 4.243 | yes | 7.819 | 0.554 | 0.037 | 0.158 | pass |
| short_cap | 4 | 3 | 0.08 | 0.75 | -1.5 | 6.000 | no | 9.781 | 0.640 | 0.000 | 0.179 | no closing/relaxation after peak |
| short_cap | 4 | 3 | 0.08 | 0.75 | 1.5 | 6.000 | no | 9.781 | 0.640 | 0.000 | 0.179 | no closing/relaxation after peak |
| short_cap | 4 | 3 | 0.25 | 0.75 | -1.5 | 6.000 | no | 9.785 | 0.326 | 0.000 | 0.151 | no closing/relaxation after peak |
| short_cap | 4 | 3 | 0.25 | 0.75 | 1.5 | 6.000 | no | 9.785 | 0.326 | 0.000 | 0.151 | no closing/relaxation after peak |
| fixed_radius_control | 0 |  | 1.25 | 1 | 0 | 3.000 | no | 3.614 | 0.000 | 0.000 | 0.167 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |
| fixed_radius_control | 0.5 |  | 1.25 | 1 | 0 | 3.000 | no | 3.616 | 0.000 | 0.000 | 0.167 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |
| fixed_radius_control | 1 |  | 1.25 | 1 | 0 | 3.000 | no | 3.642 | 0.002 | 0.000 | 0.167 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |
| fixed_radius_control | 2 |  | 1.25 | 1 | 0 | 3.000 | no | 3.734 | 0.006 | 0.001 | 0.166 | no opening above pre-registered tolerance; no interior cap peak; no closing/relaxation after peak |

## Matched-grid refinement

Best exploratory event: `short_cap`, `lambda_perp=2`, `kappa=3`,
`half-L/R0=0.08`, `edge=0.5`, `kick=1.5`, `T=0.025`.

| n | cap? | R at depletion peak | max R | opening | closing | localization | reason |
|---:|:---:|---:|---:|---:|---:|---:|---|
| 24 | yes | 7.819 | 8.381 | 0.786 | 0.037 | 0.173 | pass |
| 32 | yes | 8.019 | 8.660 | 0.733 | 0.036 | 0.145 | pass |
| 40 | yes | 7.619 | 8.336 | 0.758 | 0.203 | 0.173 | pass |
| 48 | yes | 7.661 | 8.368 | 0.713 | 0.106 | 0.184 | pass |

Radius-at-depletion-peak spread across the matched grids: **5.15%**.
Actual radius-peak spread across the same grids: **3.85%**.

The stricter radius-at-depletion-peak value remains the candidate-grade
gate for this result note. The radius-peak diagnostic is recorded because
it shows that most of the remaining spread is timing/phase selection, not
loss of the cap event itself.

## Verdict

10 exploratory configurations passed the event-marker gate,
but the best matched-grid refinement is not yet candidate-grade.
The remaining blocker is not cap existence but a grid-converged cap
radius below the pre-registered 5% spread gate.

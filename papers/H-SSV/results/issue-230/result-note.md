# Issue #230 — matched dwarf result and status report

## Decision

**UNSUPPORTED.** The audit does not identify an internal-update source and does
not activate the host/shared-screen model. This is a completed negative audit,
not evidence that galaxies lack screens under the H-SSV ontology.

## What was actually comparable

The frozen matching rule selected 7 unique SPARC controls
(including the named DDO154 anchor) for the five robust UDG summaries. The robust
UDGs have outer dynamical-to-baryonic summary ratios spanning
`0.414`--`2.13`; the matched SPARC controls span
`5.31`--`9.64`. This restates the viewed
contrast in a common summary statistic; it is not a radial decomposition.

Gate A fails for the stronger comparison. SPARC publishes reusable radial
velocities, errors, and gas/disc/bulge contributions. The homogeneous six-UDG
paper publishes two-ring kinematics as one circular-speed summary per galaxy.
The resolved AGC 114905 paper shows five nearly independent rings and baryonic
curves, but its source archive has no numeric radial table and states that data
are available from the author on request. Plot digitization was excluded by the
protocol. Thus NFW, pISO, cored-log, and retained LogSVT reductions could not be
fitted to both classes under one radial likelihood.

## Internal-proxy diagnostic

The best non-null frozen proxy model by leave-one-galaxy-out RMSE was
`gamma_dyn_plus_fgas`: RMSE `0.4370` dex versus `0.5400`
dex for the intercept (ratio `0.809`). Its
UDG-versus-SPARC class-holdout ratio was
`1.176`. Proxy threshold passes in
the primary suite: `[]`.
Even a numerical pass could not earn support because the same radial data
contract is absent; the viewed sample also cannot be confirmation. Geometry and
AGC 749290 sensitivities are retained in `proxy-comparison.csv`.

Gas turbulence and SFR surface density could not be used as homogeneous matched
predictors: four UDG dispersions are upper limits, SPARC has no corresponding
catalogue field here, and the source table does not print individual SFRs.

## SPARC-only radial control fits

The common radial baseline was executable only for the controls. Under primary
baryons its AICc winners were `{'k2': 3, 'k2_L': 1, 'k2_Q': 1, 'pISO': 2}`. For DDO154 the
winner was `k2_Q` with confidence set
`['k2_Q']`. These fits verify that a mass-discrepant slow
dwarf can prefer an extra radial response within the frozen candidate set. They
cannot tell why the UDG class differs, because no corresponding UDG fits were
possible. Full scores, covariance diagnostics, boundary flags, optimizer status,
and light/heavy baryon sensitivities are in `model-comparison.csv`.

## Shared-state gate

Gate C was not activated. The six UDGs were selected to be fairly isolated and
the inspected sources do not supply true host membership, relative velocity,
or orbital-history metadata. Projected proximity would violate the frozen rule.
No group latent, host covariance, anisotropy, backsplash memory, or
active-versus-quiescent host test was therefore fitted. There is no evidence for
a shared screen and no quantum-entanglement claim.

## Conventional alternatives and limitations

The primary papers already identify inclination as the dominant AGC 114905
systematic and flag AGC 749290's oversampling. They discuss regular rotation,
small asymmetric-drift corrections, isolation, long dynamical times, and low
turbulence, but selection, geometry, disc non-axisymmetry, disequilibrium, and
mass-profile uncertainty remain conventional explanations that this summary
audit cannot eliminate. DF2/DF4 remain in a separate future Jeans/tracer track.

## Status report

- Gate A provenance, eligibility, matching, quality exclusions, and DF2/DF4
  separation: complete.
- Gate B dimensionally valid proxies, deterministic prediction, geometry
  sensitivity, SPARC radial baselines, covariance/boundary/optimizer reporting:
  complete to the available-data boundary.
- Gate C: correctly not activated; required host metadata are absent and the
  discovery sample is isolated.
- Decision: source hypothesis unsupported on current reusable data. No paper,
  universal-screen, or entanglement claim is promoted.

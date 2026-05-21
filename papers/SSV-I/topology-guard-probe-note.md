# Topology Guard Probe Note

This note records the first pilot run of a topology-aware acceptance rule in the static trefoil prototype.

Artifacts:

- [topology-guard-probe-2026-05-17.json](../../papers/SSV-I/data/topology-guard-probe-2026-05-17.json)
- [topology-guard-probe-2026-05-17b.json](../../papers/SSV-I/data/topology-guard-probe-2026-05-17b.json)
- [topology-guard-probe-2026-05-17w10.json](../../papers/SSV-I/data/topology-guard-probe-2026-05-17w10.json)
- [topology-guard-probe-2026-05-17w50.json](../../papers/SSV-I/data/topology-guard-probe-2026-05-17w50.json)
- [topology-guard-probe-2026-05-17w100.json](../../papers/SSV-I/data/topology-guard-probe-2026-05-17w100.json)
- [topology-phase-flow-probe-2026-05-17w01.json](../../papers/SSV-I/data/topology-phase-flow-probe-2026-05-17w01.json)
- [topology-phase-flow-probe-2026-05-17w05.json](../../papers/SSV-I/data/topology-phase-flow-probe-2026-05-17w05.json)
- [topology-loop-flow-probe-2026-05-17w01.json](../../papers/SSV-I/data/topology-loop-flow-probe-2026-05-17w01.json)
- [topology-loop-flow-probe-2026-05-17w05.json](../../papers/SSV-I/data/topology-loop-flow-probe-2026-05-17w05.json)
- [topology-loop-flow-probe-2026-05-17w2.json](../../papers/SSV-I/data/topology-loop-flow-probe-2026-05-17w2.json)
- [topology-winding-flow-probe-2026-05-17w05.json](../../papers/SSV-I/data/topology-winding-flow-probe-2026-05-17w05.json)
- [topology-winding-flow-probe-2026-05-17w2.json](../../papers/SSV-I/data/topology-winding-flow-probe-2026-05-17w2.json)

Saved states:

- [trefoil-baseline-n48-hw7-steps80.npz](../../papers/SSV-I/data/topology-guard-probe-2026-05-17/trefoil-baseline-n48-hw7-steps80.npz)
- [trefoil-topology_guarded-n48-hw7-steps80.npz](../../papers/SSV-I/data/topology-guard-probe-2026-05-17/trefoil-topology_guarded-n48-hw7-steps80.npz)

## Setup

All branches start from the same fresh `n = 48`, `half_width = 7` initial trefoil state.

- baseline branch: standard constrained flow
- hard-guard branch: same constrained flow, but candidate steps are rejected if
  - `topology_mean_winding < 0.5`, or
  - `topology_unit_fraction < 0.5`
- soft-pressure branch: same constrained flow, but the acceptance test adds a topology penalty when those winding floors are undershot

## Main Result

The topology-aware closure rules do change early branch selection.

In the first three-way pilot:

- baseline branch reaches `80` steps and ends with
  - `projected_residual_norm ~ 0.139`
  - `deficit_volume ~ 253.07`
  - `topology_mean_winding = 0.5`
  - `topology_unit_fraction = 0.5`

- hard-guard branch stops earlier at `50` steps with `step_size_floor`, and ends with
  - `projected_residual_norm ~ 0.294`
  - `deficit_volume ~ 275.94`
  - `topology_mean_winding = 0.5`
  - `topology_unit_fraction = 0.5`

- with very strong topology pressure (`weight = 500`), the soft-pressure branch collapses onto the hard-guard behaviour

## Pressure Scan

The follow-up weight scan is the most useful part of this probe.

- `weight = 10`:
  - behaves like baseline
  - reaches `80` steps
  - `projected_residual_norm ~ 0.139`
  - `deficit_volume ~ 253.07`
  - winding remains at the baseline edge value

- `weight = 50`:
  - gives a genuinely intermediate branch
  - stops at `53` steps with `step_size_floor`
  - `projected_residual_norm ~ 0.255`
  - `deficit_volume ~ 273.69`
  - `topology_mean_winding = 0.333`
  - `topology_unit_fraction = 0.333`

- `weight = 100`:
  - essentially the same intermediate branch as `50`
  - still softer than the hard guard, but clearly no longer baseline-like

So there is a real soft-pressure regime:

- too weak: no effect
- too strong: becomes a disguised hard barrier
- intermediate: bends branch selection without fully locking the solver

## Interpretation

This first probe is useful even though it is not yet a success case.

It shows:

- a hard topology guard can keep the branch from sliding past the chosen winding floor
- but the current explicit relaxer then struggles to continue descending smoothly
- a medium-strength topology pressure can create an intermediate branch instead of an all-or-nothing hard stop
- the price is still a larger residual and a heavier source than the baseline branch

So the repo has now moved from a vague idea to a concrete numerical tradeoff:

- source-stable branches in the current prototype tend to lose winding
- winding-guarded branches can be retained, but the current controller becomes stiff and stops early

## Consequence

The next topology-aware closure step should not be another free-form source fit.

It should be one of:

- soften the topology guard into a penalty rather than a hard rejection
- change the constraint from global interior `L2` to a more local branch/core measure
- improve the near-guard controller so the solver does not immediately fall to step-size floor

This is the first explicit evidence that topology-preserving closure will likely require a different continuation manifold, not just a post-processing filter. The soft-pressure scan also suggests that this should be approached as a tuned bias within the flow, not only as a hard admissibility rule.

## Flow Follow-up

The later flow-based probes sharpened the picture.

- the broad topology-flow anchor is smooth but does not lift the topology score above the baseline branch
- the phase-aware flow anchor is also smooth and slightly reshapes the source, but still leaves
  - `topology_alignment_score ~ 0.25`
  - `topology_unit_fraction ~ 0.25`
- the new loop-circulation correction acts directly on the sampled circulation loops and changes the geometry more strongly than the earlier flow anchors, but it still does not improve local winding retention in the tested regime

For the `hw = 7` pilot at `80` steps:

- baseline:
  - `projected_residual_norm ~ 0.1389`
  - `deficit_volume ~ 253.07`
  - `topology_alignment_score = 0.25`

- loop-flow `weight = 0.5`:
  - `projected_residual_norm ~ 0.1385`
  - `deficit_volume ~ 253.31`
  - `topology_alignment_score = 0.25`

- loop-flow `weight = 2.0`:
  - `projected_residual_norm ~ 0.1377`
  - `deficit_volume ~ 253.89`
  - `topology_alignment_score = 0.25`

So the current loop-based correction is a cleaner actuator than the pressure branch, but it is still not acting on the right quantity strongly enough to preserve or restore the seeded local winding.

## Winding-Error Follow-up

The next refinement replaced the loop-field mismatch with a direct winding-error correction built from the discrete phase-increment mismatch around each sampled circulation loop.

That is the closest flow-based test so far to the actual topology diagnostic, and it still does not improve the retained winding in the tested `hw = 7` pilot.

- winding-flow `weight = 0.5`:
  - `projected_residual_norm ~ 0.13888`
  - `deficit_volume ~ 253.07`
  - `topology_alignment_score = 0.25`

- winding-flow `weight = 2.0`:
  - `projected_residual_norm ~ 0.13891`
  - `deficit_volume ~ 253.07`
  - `topology_alignment_score = 0.25`

So even when the flow correction is built directly from loop circulation error rather than local complex-value mismatch, the branch still lands on the same low-winding state as the baseline branch.

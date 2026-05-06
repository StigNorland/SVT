# First `C_Q` Geometry Note

This note records the first geometry-level quantities extracted to constrain the unresolved monopole calibration in the gravity branch.

Artifacts:

- `papers/SSV-I/data/trefoil-state-n24-hw5-200steps-2026-05-06.npz`
- `papers/SSV-I/data/trefoil-state-n48-hw7-400steps-2026-05-06.npz`
- `papers/SSV-I/data/cq-geometry-n24-hw5-200steps-2026-05-06.json`
- `papers/SSV-I/data/cq-geometry-n48-hw7-400steps-2026-05-06.json`

The point is not to solve `C_Q`. It is to test whether the static branch already contains geometry information that a pure shell-deficit estimator throws away.

## Quantities Extracted

For each saved state, the repo now records:

- `deficit_volume`
- `equivalent_deficit_radius`
- `shell_deficit`
- `effective_radius`
- `compactness_ratio = equivalent_deficit_radius / effective_radius`
- `deficit_volume_over_radius_cubed`
- `shell_to_volume_ratio`

These are geometry diagnostics only. None of them should be read as a solved calibration factor.

## First Comparison

Representative coarse case:

- `n = 24`, `half_width = 5`, `200` steps
- `shell_deficit = 0.00691`
- `deficit_volume = 5.78`
- `equivalent_deficit_radius = 1.11`
- `compactness_ratio = 0.339`
- `deficit_volume_over_radius_cubed = 0.164`

Representative finer case:

- `n = 48`, `half_width = 7`, `400` steps
- `shell_deficit = 0.02695`
- `deficit_volume = 61.52`
- `equivalent_deficit_radius = 2.45`
- `compactness_ratio = 0.498`
- `deficit_volume_over_radius_cubed = 0.516`

## Interpretation

The main lesson is qualitative but important:

- shell suppression and interior deficit geometry do not move in lockstep
- the finer, larger-box state carries much more integrated deficit geometry than the shell deficit alone would suggest
- this means the unresolved `C_Q` factor is very unlikely to be eliminable by shell deficit alone

That is a useful negative result. It tells the gravity branch to expect at least two ingredients:

1. an outer-shell suppression estimator
2. an interior geometric factor tied to the effective deficit volume

In other words, the current static branch already suggests that the future map from breather geometry to `Q_p` will probably not collapse to a one-scalar formula.

## Current Read

The repo can now say one step more than before:

- `1 - shell_mean_density` is still the best simple first estimator
- but a believable `Q_p` map will likely need an additional geometric factor built from the interior deficit structure

That makes the next technical step for `#14` clearer: add these geometry quantities to the broader static-branch outputs and compare them across more than two representative states before proposing any reduced calibration ansatz.

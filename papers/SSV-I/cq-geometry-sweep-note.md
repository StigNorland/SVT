# Geometry-Aware Sweep Checkpoint

This note records the first sweep-level comparison outputs that include the new gravity-facing geometry quantities directly in the static refinement harness.

Artifacts:

- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-geom-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-geom-2026-05-06.json`

These runs now carry:

- `deficit_volume`
- `equivalent_deficit_radius`
- `compactness_ratio`
- `deficit_volume_over_radius_cubed`
- `shell_to_volume_ratio`

in the sweep summary itself, not only through separately saved states.

## Coarse Branch (`n = 24`, 200 steps)

Across `half_width = 5, 6, 7`:

- `shell_mean_density` relative span: about `0.0059`
- `equivalent_deficit_radius` relative span: about `0.306`
- `compactness_ratio` relative span: about `0.528`
- `shell_to_volume_ratio` relative span: about `0.580`

This says the coarse long-run branch is extremely stable at the outer shell, but the interior geometry quantities still vary materially with box size.

## Fine Branch (`n = 48`, 400 steps)

Across `half_width = 5, 6, 7`:

- `shell_mean_density` relative span: about `0.101`
- `equivalent_deficit_radius` relative span: about `0.190`
- `compactness_ratio` relative span: about `0.450`
- `shell_to_volume_ratio` relative span: about `0.596`

This is the more interesting branch for the gravity calibration question. Among the geometry-facing quantities, `equivalent_deficit_radius` is currently the most stable of the new interior measures. It is still far from closure-grade, but it is behaving better than the more compressed combined ratios.

## Current Read

The current evidence suggests:

- shell suppression remains the most stable outer diagnostic
- `equivalent_deficit_radius` is the most promising simple interior geometric companion
- the more aggressively combined ratios (`compactness_ratio`, `shell_to_volume_ratio`, `deficit_volume_over_radius_cubed`) are not yet stable enough to support a reduced `C_Q` ansatz

That points to a practical next step for `#14`: treat the current reduced geometry model as a two-factor candidate,

1. outer-shell suppression
2. equivalent deficit radius

rather than trying to collapse everything immediately into one derived calibration scalar.

# Trefoil Soft-Boundary Box-Size Sweep: 60 vs 100 Steps

This note compares the fixed-resolution (`n = 24`) soft-boundary box-size sweeps at `60` and `100` relaxation steps:

- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-60steps-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-100steps-2026-05-06.json`

The goal is to check whether longer relaxation is still changing the outer-region diagnostics materially, or whether the static branch is beginning to approach a more stable box-size regime.

## Comparison Summary

Global relative spans across `half_width = 5, 6, 7`:

| quantity | 60 steps | 100 steps | change |
|---|---:|---:|---:|
| residual norm | 0.296 | 0.263 | -0.032 |
| shell mean density | 0.195 | 0.051 | -0.144 |
| shell mean deficit | 0.507 | 0.302 | -0.205 |
| far-field moment | 0.208 | 0.077 | -0.131 |
| depressed fraction | 0.604 | 0.590 | -0.014 |

Representative per-box values:

| half-width | shell density at 60 | shell density at 100 | far-field moment at 60 | far-field moment at 100 |
|---|---:|---:|---:|---:|
| `5` | 0.677 | 0.849 | 0.577 | 0.244 |
| `6` | 0.770 | 0.870 | 0.524 | 0.264 |
| `7` | 0.841 | 0.895 | 0.457 | 0.263 |

## Interpretation

The main improvement from `60` to `100` steps is not just that the state relaxes further. The more important point is that the box-size dependence of the outer-region diagnostics drops substantially:

- `shell_mean_density` improves from a relative span of about `19.5%` to about `5.1%`
- `far_field_moment` improves from about `20.8%` to about `7.7%`
- `residual_norm` also improves, but much more modestly, from about `29.6%` to about `26.3%`

This suggests the static branch is beginning to enter a more interpretable outer-region regime. The solver is still not closure-grade, and the depressed-fraction diagnostics remain visibly box-sensitive, but the simpler far-field quantities are no longer drifting at the same rate as they were at `60` steps.

At the current prototype level, this strengthens the case for using `shell_mean_density` as the primary simple far-field proxy for the later `alpha_G` branch, with `far_field_moment` as a secondary cross-check rather than the leading scalar.

## Current Reading

The `100`-step sweep looks less like raw solver drift and more like the start of a plateau in the easiest outer-region observables. That is not yet enough to claim quantitative closure, but it is enough to justify one more escalation step:

- either extend the same sweep to a longer run such as `150` steps to test whether the far-field quantities flatten further,
- or begin a matched `n = 28` comparison to see whether the same stabilization pattern survives increased resolution.

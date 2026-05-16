# Trefoil Long-Run and Resolution Check

This note records three follow-up runs on the soft-boundary static trefoil branch:

- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-150steps-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-100steps-2026-05-06.json`

The aim was to answer two different questions:

1. Does the `n = 24` branch continue to stabilize if we push the relaxation beyond `100` steps?
2. Does the same behavior survive if we double the linear resolution to `n = 48`?

## Long-Run Trend at `n = 24`

Selected global box-size spans across `half_width = 5, 6, 7`:

| quantity | 100 steps | 150 steps | 200 steps |
|---|---:|---:|---:|
| residual norm (relative span) | 0.263 | 0.103 | 0.402 |
| shell mean density (relative span) | 0.051 | 0.012 | 0.017 |
| far-field moment (relative span) | 0.077 | 0.460 | 0.791 |

Absolute far-field moments:

| half-width | 100 steps | 150 steps | 200 steps |
|---|---:|---:|---:|
| `5` | 0.2440 | 0.0666 | 0.0114 |
| `6` | 0.2644 | 0.1029 | 0.0334 |
| `7` | 0.2633 | 0.1233 | 0.0546 |

The important reading is:

- `shell_mean_density` keeps improving and is already very stable by `150` steps
- by `200` steps the shell density remains close to `1` across all tested box sizes
- the raw far-field moment is also shrinking strongly in absolute magnitude

The moment's relative span becomes much worse at `150` and `200` steps, but that is partly a ratio artifact: once the moment gets small, even modest absolute differences between boxes inflate the relative-span measure. The shell-density diagnostic is therefore the more reliable stability gauge in this regime.

## Resolution Check at `n = 48`

The doubled-resolution `100`-step run does **not** land in the same numerical regime as the `n = 24`, `100`-step run.

Signs of trouble:

- nonzero rejected steps appear (`4` to `5` per run)
- energy monotonicity violations appear (`4` to `5`)
- final adaptive step sizes are reduced below the coarse-grid ceiling
- residuals are much larger:
  - `n = 24`: about `0.122` to `0.165`
  - `n = 48`: about `0.209` to `0.588`
- shell densities are much worse:
  - `n = 24`: about `0.849` to `0.895`
  - `n = 48`: about `0.642` to `0.861`

This means the doubled-cell run is not evidence against the `n = 24` long-run trend. It is evidence that the current solver controls do not yet scale cleanly with resolution. In other words, the coarse-grid branch may be approaching a plateau, but the fine-grid branch is still under-relaxed or numerically stressed.

## Current Reading

At the present prototype stage, the clean conclusion is:

- longer relaxation at `n = 24` is genuinely improving the outer shell
- `shell_mean_density` is the most trustworthy simple far-field diagnostic so far
- the current `n = 48` run should be treated as a solver-scaling warning, not as a physical contradiction

The next technical step should be a resolution-aware control pass before reading too much into fine-grid differences. The most likely targets are:

- scale the initial step size with grid spacing
- tighten the adaptive-controller logic for finer grids
- or run the `n = 48` branch longer with smaller starting steps before comparing it directly to the relaxed `n = 24` branch

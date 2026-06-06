# Trefoil `n = 48` Scaled-Control Check

This note records the first doubled-resolution rerun after adding grid-spacing-aware step scaling to the static trefoil relaxer:

- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-100steps-scaled-2026-05-06.json`

The purpose of this run was not to claim convergence. It was to test whether the finer grid could be moved into a numerically healthier regime before comparing it to the relaxed `n = 24` branch.

## What Improved

Compared with the earlier unscaled `n = 48`, `100`-step run:

- rejected steps dropped from `4-5` per case to `0`
- energy monotonicity violations dropped from `4-5` per case to `0`
- the final adaptive step size stayed below the coarse-grid ceiling in a controlled way

That means the controller is now respecting the finer spatial scale better than before. This is a real solver improvement, not just a cosmetic change.

## What Did Not Improve Yet

The branch is still not in the same relaxation regime as the mature `n = 24` long runs:

- residual norms remain large:
  - `0.582`, `0.376`, `0.262` for `half_width = 5, 6, 7`
- shell mean density is still far from the `n = 24`, `200`-step values:
  - scaled `n = 48`, `100` steps: `0.606`, `0.759`, `0.848`
  - relaxed `n = 24`, `200` steps: `0.993`, `0.983`, `0.977`

So the new result should be read as:

- the fine-grid run is now more numerically trustworthy,
- but it is still under-relaxed relative to the coarse-grid long-run branch.

## Current Reading

The earlier `n = 48` warning was partly a controller problem. The new run shows that clearly. But after fixing the worst of that controller mismatch, the doubled-resolution branch still needs more relaxation work before it can be compared directly to the coarse-grid plateau story.

The next sensible experiments are:

- rerun the scaled `n = 48` branch at `150` or `200` steps,
- or lower the initial coarse-equivalent step again for `n = 48` and test whether residuals fall faster with fewer outer-shell distortions.

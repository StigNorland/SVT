# Optional n=64 tube-pinch cap check (#108)

**Issue:** #108, linked from #97.
**Script:** `instruments/paper_ii/tube_pinch_cap_harness.py`.
**Date:** 2026-06-07.

This is an optional high-grid check of the best short-cap refinement target from
`tube-pinch-cap-harness-issue108.md`:

```text
lambda_perp = 2
kappa = 3
half-L/R0 = 0.08
edge = 0.5
kick = 1.5
T = 0.025
n = 64
fft_workers = 8
```

The run completed in `297.3 s` with `7784` split-step iterations and passed the
pre-registered cap-event gate:

| n | cap? | peak R | opening | closing | localization |
|---:|:---:|---:|---:|---:|---:|
| 64 | yes | 7.859 | 0.731 | 0.216 | 0.155 |

Combining the default refinement radii for `n = 24, 32, 40, 48` with this
optional `n = 64` point gives a five-grid peak-radius spread of `5.14%`. This
confirms that the event persists at `n=64`, but it remains just above the
pre-registered `<5%` candidate-grade radius-convergence gate.

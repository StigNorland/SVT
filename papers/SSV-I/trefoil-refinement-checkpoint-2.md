# Trefoil Refinement Checkpoint 2

This note records the second saved refinement checkpoint for issue [#13](https://github.com/StigNorland/SVT/issues/13), after improving the relaxation logic in the static trefoil prototype.

Data file:

- [papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06b.json](C:/Users/stino/Documents/New%20project/SVT/papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06b.json)

Command used:

```bash
python src/paper_i/trefoil_breather_refinement.py \
  --n-values 20,24 \
  --half-width-values 5.0,6.0 \
  --max-steps 40 \
  --step-size 0.005 \
  --output papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06b.json
```

## What Changed Since Checkpoint 1

The static relaxer now uses:

- accepted/rejected step logic
- adaptive step-size growth and shrinkage
- explicit stop-reason reporting
- best-state tracking

This checkpoint is still prototype-level, but it is a cleaner probe of the solver than the earlier fixed-step run.

## Main Readout

From the saved `comparison_summary`:

- global relative span in final energy: about `0.246`
- global relative span in residual norm: about `0.279`
- global relative span in effective radius: about `0.169`
- global relative span in depressed fraction: about `0.415`
- global relative span in shell mean density: about `0.198`

## Comparison To Checkpoint 1

The most important improvement is in the residuals.

- Checkpoint 1 global residual relative span: about `0.400`
- Checkpoint 2 global residual relative span: about `0.279`

And the absolute residual levels are lower as well in the small test set.

The new by-half-width summaries are also informative:

- at fixed box size, energy relative span across `n=20,24` is now only about `4.2%` to `4.5%`
- at fixed box size, effective-radius relative span across `n=20,24` is now only about `3.0%` to `3.2%`

That suggests the current prototype is becoming less resolution-sensitive than box-sensitive in this small regime.

## Interpretation

Three things stand out.

1. The relaxation controller is helping.
   The solver is still not converged in the closure-grade sense, but it is producing more stable and more interpretable sweep behaviour.

2. Box-size effects are now easier to see cleanly.
   Once the step logic became less crude, the `by_half_width` blocks showed that the remaining spread is not just a resolution artefact.

3. The prototype still is not ready to support `N_Y` or `F`.
   Residuals remain too large, and the observables still move materially with setup changes.

## What This Means For #13

This checkpoint is a real numerical improvement, not just a documentation update.

It supports the next move being:

1. add a simple far-field diagnostic from the saved relaxed state
2. test whether larger boxes reduce the remaining box-size drift
3. only after that start asking whether any static observable is nearing a plateau

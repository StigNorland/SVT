# Trefoil Box-Size Sweep Note: Soft Boundary, 60 Steps

This note records the first longer fixed-resolution box-size sweep after introducing the soft outer-boundary blend.

Artifact:

- [papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-60steps-2026-05-06.json](../../papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-60steps-2026-05-06.json)

Command used:

```bash
python instruments/paper_i/trefoil_breather_refinement.py \
  --n-values 24 \
  --half-width-values 5.0,6.0,7.0 \
  --max-steps 60 \
  --step-size 0.005 \
  --workers 3 \
  --output papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-60steps-2026-05-06.json
```

## Why This Checkpoint Matters

The earlier soft-boundary test at `20` steps did not visibly separate itself from the old behaviour.

This longer sweep is important because it answers the obvious next question:

- was the boundary change ineffective,
- or had the prototype simply not relaxed long enough for the difference to show up?

The present result supports the second reading.

## Main Readout

From the saved `comparison_summary`:

- global relative span in residual norm: about `0.296`
- global relative span in shell mean density: about `0.195`
- global relative span in far-field moment: about `0.208`

Compared with the earlier `20`-step fixed-`n=24` box sweep:

- residuals are much lower in absolute terms
- the far-field moment is much less volatile
- the outer-region story is cleaner

## Interpretation

Three things are now clearer.

1. The longer relaxation matters.
   The prototype reaches a substantially cleaner regime by `60` steps than it did by `20`.

2. The soft-boundary treatment is beginning to show up in the diagnostics once the state is allowed to evolve longer.
   The earlier short run was too premature to judge the boundary change.

3. Box-size dependence is still present, but the outer-region quantities are becoming more interpretable.
   In particular, the weighted far-field moment no longer looks wildly unstable relative to the simpler shell summaries.

## Current Best Reading

At this point the static branch seems to be entering a more useful diagnostic regime:

- `far_field_shell_density` remains the most transparent simple outer-region scalar
- `far_field_moment` is still secondary, but now worth tracking rather than dismissing immediately

## What This Means For #13

This checkpoint is the first one that suggests the static branch may be ready for more systematic box-size studies rather than just emergency solver triage.

The next sensible move is:

1. compare the `20`-step and `60`-step box sweeps explicitly in prose
2. push one more step to `100` only if the runtime remains reasonable
3. then decide whether any far-field quantity is actually approaching a plateau

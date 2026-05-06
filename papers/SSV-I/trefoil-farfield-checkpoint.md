# Trefoil Far-Field Checkpoint

This note records the first saved far-field-enabled checkpoint for issue [#13](https://github.com/StigNorland/SVT/issues/13).

Data file:

- [papers/SSV-I/data/trefoil-refinement-farfield-checkpoint-2026-05-06.json](C:/Users/stino/Documents/New%20project/SVT/papers/SSV-I/data/trefoil-refinement-farfield-checkpoint-2026-05-06.json)

Command used:

```bash
python src/paper_i/trefoil_breather_refinement.py \
  --n-values 20,24 \
  --half-width-values 5.0 \
  --max-steps 20 \
  --step-size 0.005 \
  --output papers/SSV-I/data/trefoil-refinement-farfield-checkpoint-2026-05-06.json
```

## What Was Added

This checkpoint extends the early static-branch sweep with three outer-region diagnostics:

- far-field shell density
- far-field shell deficit
- far-field moment

These are still prototype diagnostics. They are not yet a first-principles extraction of `\alpha_G`.

## Main Readout

From the saved `comparison_summary`:

- relative span in effective radius: about `0.031`
- relative span in shell mean density: about `0.016`
- relative span in shell mean deficit: about `0.029`
- relative span in far-field moment: about `0.141`

## Interpretation

The most important result is that the simple shell-density diagnostic is currently the most stable of the far-field quantities.

That matters because it suggests a sensible ordering for the gravity branch:

1. use shell density or shell deficit as the first outer-region stability diagnostic
2. treat the weighted far-field moment as a secondary quantity until the relaxed state is cleaner
3. only after the shell quantities behave robustly under larger sweeps should they be promoted into a more physical `\alpha_G`-facing observable

## Current Best Candidate

At this stage, the best simple far-field diagnostic is:

- `far_field_shell_density`

Why:

- its relative span in this small `n=20,24` test is only about `1.6%`
- it is more stable than the weighted outer moment
- it pairs naturally with the shell-deficit view already used in the checkpoint summaries

## What This Means For #13

This checkpoint does not close the static branch, but it does sharpen the path forward.

The next useful static-branch step is:

1. repeat the far-field-enabled sweep with larger box sizes
2. confirm whether shell density remains the most stable outer-region quantity
3. only then build a first dedicated gravity-extraction proxy on top of that quantity

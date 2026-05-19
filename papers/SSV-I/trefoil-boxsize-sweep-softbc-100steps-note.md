# Trefoil Box-Size Sweep Note: Soft Boundary, 100 Steps

This note records the `100`-step fixed-resolution box-size sweep for the static trefoil prototype with the soft outer-boundary blend enabled.

Artifact:

- [papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-100steps-2026-05-06.json](papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-100steps-2026-05-06.json)

Command used:

```bash
python src/paper_i/trefoil_breather_refinement.py \
  --n-values 24 \
  --half-width-values 5.0,6.0,7.0 \
  --max-steps 100 \
  --step-size 0.005 \
  --workers 3 \
  --output papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-100steps-2026-05-06.json
```

## Why This Checkpoint Matters

The 60-step note already suggested that longer relaxation was moving the static branch into a cleaner diagnostic regime.

This 100-step run is the first checkpoint where the outer-region summaries begin to look plausibly close to a plateau rather than merely less unstable.

## Main Readout

From the saved `comparison_summary`:

- global relative span in residual norm: about `0.263`
- global relative span in shell mean density: about `0.051`
- global relative span in far-field moment: about `0.077`

These are the most encouraging outer-region numbers seen so far in the static branch.

## Comparison To 60 Steps

Relative to the 60-step soft-boundary sweep:

- residual spread is lower
- shell-density spread is much lower
- far-field moment spread is much lower

The especially important change is the shell-density behaviour:

- at 60 steps, shell-density relative span was about `0.195`
- at 100 steps, shell-density relative span is about `0.051`

That is a substantial improvement.

## Interpretation

Three things now look likely.

1. The current prototype needs longer relaxation before its outer-region diagnostics are worth judging.
   Short runs were still dominated by transient adjustment.

2. The soft-boundary treatment and the adaptive relaxer are starting to work together.
   The branch is no longer showing the same level of box-size contamination in the simplest outer scalar.

3. `far_field_shell_density` is emerging as the most promising first far-field proxy.
   It is now much more stable than the shell-deficit ratio and slightly cleaner than the weighted moment.

## Current Best Candidate For The Static Gravity Branch

At this stage, the best simple quantity to carry forward toward the later `\alpha_G` work is still:

- `far_field_shell_density`

not because it is already derived, but because it is now the most stable and transparent outer-region summary in the current prototype.

## What This Means For #13

This checkpoint is the first one that justifies talking about a possible approach toward a plateau in the outer-region diagnostics.

The next sensible step is not to promote a claim yet, but to compare the `60`-step and `100`-step runs directly in one short note and decide whether another longer run is still buying much.

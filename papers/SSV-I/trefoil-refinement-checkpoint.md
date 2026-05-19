# Trefoil Refinement Checkpoint

This note records the first saved refinement checkpoint for issue [#13](https://github.com/StigNorland/SVT/issues/13).

Data file:

- [papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06.json](../../papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06.json)

Command used:

```bash
python src/paper_i/trefoil_breather_refinement.py \
  --n-values 20,24 \
  --half-width-values 5.0,6.0 \
  --max-steps 20 \
  --step-size 0.005 \
  --output papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06.json
```

## What This Checkpoint Is

This is an early prototype sensitivity run for the static trefoil-breather track.

It is useful because it already measures how the first trefoil prototype shifts with:

- grid size `n`
- box half-width

It is not yet a closure-grade result for `N_Y`, `F`, or proton mass.

## Main Readout

From the saved `comparison_summary`:

- global relative span in final energy: about `0.214`
- global relative span in residual norm: about `0.400`
- global relative span in effective radius: about `0.136`
- global relative span in depressed fraction: about `0.427`
- global relative span in shell mean density: about `0.205`

## Interpretation

Three things are already clear.

1. Effective radius is behaving better than the other reported quantities.
   Its relative span is around `13.6%`, while energy and shell-density diagnostics drift more strongly and residual/depressed-fraction drift even more.

2. The solver is numerically calm but not yet converged in the stronger sense needed for closure.
   All four runs completed with zero energy-monotonicity violations, which is a useful health signal, but the residual norms remain large and configuration-dependent.

3. Box size and resolution both still matter materially.
   The by-`n` and by-half-width summaries show that the prototype is not yet in a refinement-stable regime.

## What This Means For #13

This checkpoint supports the current status labels:

- `trefoil_breather_static.py` should remain `candidate`
- the refinement harness is doing the right job
- no quantity from this branch should yet be promoted to `closure-grade`

## Best Next Step

The next improvement should target reduced drift, not broader claim language.

The most useful follow-up is:

1. strengthen the relaxation loop and stopping logic
2. add a simple far-field diagnostic derived from the saved state
3. only then start testing whether any observable is approaching a stable plateau under refinement

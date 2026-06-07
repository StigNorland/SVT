# Trefoil Box-Size Sweep Note

This note records the first clean box-size-only sweep for the static trefoil prototype at fixed resolution.

Artifact:

- [papers/SSV-I/data/trefoil-boxsize-sweep-n24-2026-05-06.json](../../papers/SSV-I/data/trefoil-boxsize-sweep-n24-2026-05-06.json)

Command used:

```bash
python instruments/paper_i/trefoil_breather_refinement.py \
  --n-values 24 \
  --half-width-values 5.0,6.0,7.0 \
  --max-steps 20 \
  --step-size 0.005 \
  --workers 3 \
  --output papers/SSV-I/data/trefoil-boxsize-sweep-n24-2026-05-06.json
```

## Why This Sweep Matters

Earlier comparisons mixed two effects:

- grid resolution
- box size

This sweep removes that ambiguity by holding `n=24` fixed and varying only `half_width`.

## Main Readout

From the saved `comparison_summary`:

- global relative span in residual norm: about `0.428`
- global relative span in effective radius: about `0.205`
- global relative span in shell mean density: about `0.291`
- global relative span in shell mean deficit: about `0.714`
- global relative span in far-field moment: about `0.548`

The actual trend is monotonic in the tested range:

- larger box size gives lower residual norm
- larger box size gives larger effective radius
- larger box size gives higher far-field shell density
- larger box size gives lower far-field shell deficit
- larger box size gives lower far-field moment

## Interpretation

This is the clearest signal yet that the static branch is still box-size limited.

In the current prototype:

1. the outer-region diagnostics are strongly box dependent
2. the weighted far-field moment is especially sensitive
3. even the simpler shell-density summary still moves substantially with domain size

That means the current far-field scalar quantities are useful as diagnostics, but not yet stable enough to support a gravity-facing claim.

## Best Current Far-Field Quantity

Even in this sweep, `far_field_shell_density` remains the most interpretable simple outer-region quantity.

It is still moving too much, but it behaves more transparently than the weighted moment and is easier to connect to the qualitative radial-profile story already saved in the repo.

## What This Means For #13

The static branch has now reached a clearer stage:

- resolution-only behaviour is improving
- box-size dependence is now the dominant visible issue

That means the next useful solver work should focus on reducing domain sensitivity rather than adding more derived quantities on top of the current state.

# Constrained Fine-Grid Box-Size Trend: `half_width = 6, 7, 8`

This note records the direct constrained fine-grid box-size comparison after the `L2`-constrained flow and projected-residual updates.

Artifact:

- `papers/SSV-I/data/trefoil-boxsize-trend-6-7-8-2026-05-17.json`

Reference states used:

- `half_width = 6`, `n = 48`, plateaued with projected residual
- `half_width = 7`, `n = 48`, plateaued constrained-flow state
- `half_width = 8`, `n = 64`, plateaued constrained-flow state

The `half_width = 5` branch is intentionally excluded from the interpretation below because it remains the known undersized-box failure case.

## Selected Reference Values

`half_width = 6`:

- `delta V_p = 90.646`
- `Q_p^eff = 90.356`
- shell density `= 0.92474`
- projected residual `= 0.00527`

`half_width = 7`:

- `delta V_p = 61.511`
- `Q_p^eff = 61.108`
- shell density `= 0.96830`
- projected residual `= 0.03599`

`half_width = 8`:

- `delta V_p = 249.630`
- `Q_p^eff = 246.770`
- shell density `= 0.91752`
- projected residual `= 0.02800`

## Relative Trend

From `half_width = 6 -> 7`:

- `delta V_p` changes by about `32.1%`
- `Q_p^eff` changes by about `32.4%`
- shell density changes by about `4.5%`

From `half_width = 7 -> 8`:

- `delta V_p` changes by about `75.4%`
- `Q_p^eff` changes by about `75.2%`
- shell density changes by about `5.2%`

## Interpretation

This is the clearest current box-size diagnostic in the repo.

The constrained-flow and projected-residual fixes were real improvements: they gave clean plateaued states and removed the false impression that `half_width = 6` was still obviously unsettled just because of the raw residual. But those fixes did **not** deliver box-size convergence of the integrated proton source.

The key point is that `half_width = 8` does not sit close to `7`. It lands in a very different source regime:

- `Q_p^eff` jumps from about `61` to about `247`
- `delta V_p` jumps by essentially the same factor

That jump is far too large to interpret as a small boundary correction.

So the current constrained fine-grid story is:

- `half_width = 5` is too small and should be treated as a failure case
- `half_width = 6` and `7` are locally well-behaved constrained-flow states
- `half_width = 8` shows that the integrated source is still strongly box-sensitive

## Consequence

The repo should no longer treat `half_width = 6, 7` as an adequate large-box reference set for gravity extraction.

The direct static-potential method remains the right diagnostic object, but its output is still dominated by domain dependence of the underlying static trefoil state.

The next gravity-facing question is therefore not another reduced fit. It is whether the present static branch is physically supposed to generate an integrated source that keeps reorganizing with box size, or whether the current breather/support definition is still missing a large-box closure condition.

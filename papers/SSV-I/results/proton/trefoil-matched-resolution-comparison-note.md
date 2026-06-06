# Trefoil Matched-Resolution Comparison

This note compares the static trefoil branch across the two most informative resolution tracks currently in the repo:

- coarse branch: `n = 24`
- fine branch: `n = 48`

The purpose is to answer a narrow question: do the two branches tell the same numerical story once each one is followed far enough along its own relaxation path?

## Runs Compared

Coarse branch:

- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-100steps-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-150steps-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-2026-05-06.json`

Fine branch:

- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-100steps-scaled-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-150steps-scaled-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-200steps-scaled-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-scaled-2026-05-06.json`

## Shared Trend

Both branches show the same qualitative behavior:

- longer relaxation improves the outer shell
- larger boxes relax more cleanly than the smallest box
- `shell_mean_density` is the most reliable simple far-field proxy
- the smallest tested box, `half_width = 5`, is the slowest to settle

So the current resolution story is no longer “coarse and fine grids disagree.” It is “coarse and fine grids point the same way, but the finer grid takes longer to get there.”

## Representative Progression

Shell mean density by branch:

| case | `half_width = 5` | `half_width = 6` | `half_width = 7` |
|---|---:|---:|---:|
| `n = 24`, `100` steps | 0.849 | 0.870 | 0.895 |
| `n = 24`, `150` steps | 0.958 | 0.947 | 0.948 |
| `n = 24`, `200` steps | 0.993 | 0.983 | 0.977 |
| `n = 48`, `100` steps | 0.606 | 0.759 | 0.848 |
| `n = 48`, `150` steps | 0.644 | 0.790 | 0.871 |
| `n = 48`, `200` steps | 0.695 | 0.829 | 0.900 |
| `n = 48`, `400` steps | 0.874 | 0.945 | 0.973 |

Residual norm by branch:

| case | `half_width = 5` | `half_width = 6` | `half_width = 7` |
|---|---:|---:|---:|
| `n = 24`, `100` steps | 0.165 | 0.141 | 0.122 |
| `n = 24`, `150` steps | 0.090 | 0.100 | 0.090 |
| `n = 24`, `200` steps | 0.034 | 0.052 | 0.057 |
| `n = 48`, `100` steps | 0.582 | 0.376 | 0.262 |
| `n = 48`, `150` steps | 0.408 | 0.267 | 0.187 |
| `n = 48`, `200` steps | 0.321 | 0.211 | 0.150 |
| `n = 48`, `400` steps | 0.182 | 0.115 | 0.073 |

## Interpretation

Three points stand out.

First, the coarse grid is still the cheapest place to see the onset of an outer-shell plateau. By `n = 24`, `200` steps, the shell density is already very close to `1` across all tested box sizes.

Second, the fine grid is not contradicting that picture. Its numbers move in the same direction, and by `n = 48`, `400` steps, the `half_width = 7` case is nearly aligned with the coarse-grid long-run shell density, while `half_width = 6` is clearly in the same regime.

Third, the remaining mismatch is concentrated in the smallest box. That makes the unresolved issue look more like finite-domain plus slower fine-grid relaxation than like a basic failure of the static branch.

## Current Reading

At the present prototype stage, the fairest summary is:

- `n = 24` provides the first affordable plateau signal
- `n = 48` is beginning to confirm that signal under stricter resolution
- the confirmation is incomplete, with `half_width = 5` still lagging

That is strong enough to support the repo-level claim that the static branch now shows a coherent multiresolution trend, even though it is not yet closure-grade.

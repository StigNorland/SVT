# Trefoil `n = 48` at 400 Steps

This note records the scaled-control `n = 48` box-size sweep at `400` relaxation steps:

- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-scaled-2026-05-06.json`

The point of this run was to test whether the doubled-resolution branch could approach the same settled outer-shell regime already seen in the coarse-grid `n = 24`, `200`-step sweep.

## Main Outcome

The answer is: **yes, partially**.

The `n = 48` branch is now clearly following the same qualitative trend as the relaxed `n = 24` branch, but it has not caught up uniformly across box sizes.

## Key Comparison

Shell mean density:

| case | `half_width = 5` | `half_width = 6` | `half_width = 7` |
|---|---:|---:|---:|
| `n = 24`, `200` steps | 0.993 | 0.983 | 0.977 |
| `n = 48`, `400` steps | 0.874 | 0.945 | 0.973 |

Residual norm:

| case | `half_width = 5` | `half_width = 6` | `half_width = 7` |
|---|---:|---:|---:|
| `n = 24`, `200` steps | 0.034 | 0.052 | 0.057 |
| `n = 48`, `400` steps | 0.182 | 0.115 | 0.073 |

## Interpretation

This is the strongest evidence so far that the fine-grid branch is not contradicting the coarse-grid story. It is converging in the same direction, just more slowly.

The box-by-box reading is:

- `half_width = 7` is now very close in shell density and not far off in residual
- `half_width = 6` is clearly in the same qualitative regime, though still not as relaxed
- `half_width = 5` remains the laggard and still looks under-relaxed relative to the larger boxes

That makes the current picture much cleaner:

- the scaled controller fixed the worst numerical pathology on the fine grid
- longer runs at `n = 48` do continue to improve the outer shell
- the remaining gap is now best read as slower fine-grid relaxation, especially for the smallest box, rather than as a sign that the coarse-grid plateau was spurious

## Current Reading

At prototype level, the static branch now supports a more confident statement:

- `n = 24` gives the first cheap plateau signal
- `n = 48` is beginning to confirm that signal under stricter resolution, but with a longer relaxation timescale

The next clean comparison should be a direct matched-resolution note across:

- `n = 24`: `100`, `150`, `200`
- `n = 48`: `100`, `150`, `200`, `400`

That will let the repo say explicitly that the resolution story is now "same trend, slower on the finer grid" rather than "coarse and fine grids disagree."

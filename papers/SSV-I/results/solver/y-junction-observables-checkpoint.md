# Y-Junction Observables Checkpoint

This note records the first concrete extractor for the Paper I closure quantities `N_Y` and `F` from a relaxed Y-junction state.

Artifacts:

- `instruments/paper_i/trefoil_y_junction_observables.py`
- `papers/SSV-I/data/y-junction-observables-n24-hw6-200steps-2026-05-17.json` (canonical run)
- `papers/SSV-I/data/y-junction-observables-sensitivity-n24-hw6-200steps-2026-05-17.json` (sensitivity scan)

## What The Extractor Computes

Given a relaxed Y-junction state on a 3D grid, the script:

1. Recovers each filament's signed arc-length `s_k` from the origin and perpendicular distance `d_k` from its axis, using the same 120-deg equatorial frame as the relaxation script.
2. Assigns each grid cell to its nearest filament (Voronoi-by-filament).
3. Defines three masks:
   - **Filament tubes:** cells closer to filament `k` than any other, with `d_k < r_tube`, `s_k > 0`, outside the node ball, and outside the boundary-anchor shell.
   - **Junction ball:** cells with `|x| < r_node`, outside the anchor shell.
   - **Bulk residual:** interior cells outside both tubes and the node ball.
4. Integrates the LogSE energy density inside each mask.
5. Self-calibrates `mu_0_grid` from a slab `s_k in [cal_start, cal_stop]` along each filament, where the field looks like a straight isolated vortex.
6. Reports:
   - per-volume normalisation: `N_Y^xi = (E_filaments + E_node) / mu_0_grid`
   - per-filament-length normalisation: `N_Y^L = (E_filaments + E_node) / (mu_0_grid * L_filament_total)`
   - interior form factor: `F^int = E_interior / (N_Y^xi * mu_0_grid)`

## Headline Numbers For The 200-Step n=24 hw=6 State

At the default extraction parameters `r_tube = r_node = 2.0`, `cal_start = 2.5`, `cal_stop = 4.5`:

| quantity | value |
|---|---:|
| `E_total_raw` | `857.0` |
| `E_anchor_shell` | `740.8` |
| `E_interior` (physical) | `116.22` |
| `E_filaments` | `41.13` |
| `E_node` | `13.93` |
| `E_bulk_residual` | `61.17` |
| `mu_0_grid` | `3.911` |
| `mu_0_per_filament` | `[3.924, 3.924, 3.886]` |
| `L_filament_total` | `10.98` |
| `N_Y^xi` | `14.08` |
| `N_Y^L` | `1.282` |
| `F^int` | `2.11` |

Two diagnostics matter:

- `mu_0_per_filament` agrees across the three filaments to within `1%`. The self-calibration slab is in a regime where the field looks like a straight isolated vortex on this grid.
- 86% of `E_total_raw` lives in the boundary-anchor shells. This is a discretisation artifact of the `np.roll` gradient operator on pinned outer cells, not a physical contribution. `E_interior` is the right denominator for `F`.

## Sensitivity Scan

Varying `r_tube` and `r_node` over `{1.5, 2.0, 2.5, 3.0}` and `{1.5, 2.0, 2.5}` respectively, with the calibration slab held at `s in [2.5, 4.5]`:

| `r_tube` | `r_node` | `mu_0_grid` | `N_Y^L` | `F^int` | `E_fil` | `E_node` | `E_bulk` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.5 | 1.5 | 3.161 | 1.103 | 2.618 | 36.28 | 8.11 | 71.83 |
| 1.5 | 2.0 | 3.161 | 1.284 | 2.454 | 33.43 | 13.93 | 68.87 |
| 1.5 | 2.5 | 3.161 | 1.613 | 2.238 | 29.31 | 22.62 | 64.30 |
| 2.0 | 1.5 | 3.911 | 1.139 | 2.230 | 44.01 | 8.11 | 64.09 |
| 2.0 | 2.0 | 3.911 | 1.282 | 2.111 | 41.13 | 13.93 | 61.17 |
| 2.0 | 2.5 | 3.911 | 1.553 | 1.955 | 36.84 | 22.62 | 56.77 |
| 2.5 | 1.5 | 4.345 | 1.226 | 2.046 | 48.70 | 8.11 | 59.41 |
| 2.5 | 2.0 | 4.345 | 1.346 | 1.946 | 45.81 | 13.93 | 56.49 |
| 2.5 | 2.5 | 4.345 | 1.579 | 1.812 | 41.51 | 22.62 | 52.10 |
| 3.0 | 1.5 | 4.480 | 1.397 | 1.974 | 50.77 | 8.11 | 57.34 |
| 3.0 | 2.0 | 4.480 | 1.518 | 1.880 | 47.88 | 13.93 | 54.41 |
| 3.0 | 2.5 | 4.480 | 1.741 | 1.756 | 43.58 | 22.62 | 50.03 |

Three structural observations follow.

**`E_interior` is invariant.**
`E_filaments + E_node + E_bulk_residual = 116.22` in every row. The partition shifts between the three buckets as the cut-off radii move, but the total physical interior energy does not depend on the extractor parameters.

**`mu_0_grid` depends on `r_tube` alone, not on `r_node`.**
The calibration slab uses the same filament-tube mask as the tube integration, so widening `r_tube` from `1.5` to `3.0` lifts `mu_0_grid` from `3.16` to `4.48`. This is the logarithmic energy tail of an isolated vortex being progressively captured. The right asymptotic value of `mu_0_grid` is approached, but slowly; no single tube radius is "correct" without a convergence study.

**`N_Y` and `F` are extractor-parameter-dependent, but their product times `mu_0` reproduces `E_interior` identically.**
By construction `N_Y^xi * F^int * mu_0_grid = E_interior`. The three quantities individually are conventions; only their product is invariant.

## Comparison To The Paper

Paper I quotes `N_Y ~ 3.007` and `F ~ 4.47` for the closed compact proton breather, with `N_Y * F * mu_0 ~ 13.44 * mu_0 = m_p c^2`.

Our open three-prong Y in a box with `L_filament_total ~ 11 xi` gives:

- `N_Y^L ~ 1.28` (the per-unit-length junction excess over a straight calibration filament)
- `F^int ~ 2.11` (interior breather cost in line/node-cost units)
- `N_Y^L * F^int ~ 2.7` — distinct from `13.44`, which is expected: the paper's `N_Y * F` is on the compact closed object with three roughly `1 xi` filaments, whereas our scan has long open filaments and a wider breather cavity.

The per-filament-length invariant `N_Y^L ~ 1.28` is the cleanest first comparable: a straight isolated filament would give exactly `1.0`, so the `0.28` excess is the structural junction-cost signature of the three-filament node. The paper's `N_Y ~ 3.007` decomposes as `3 + 0.007` where the `0.007` is the analogous junction excess on `3 xi` of filament. Their `0.007` is two orders of magnitude smaller than our `0.28`, which is consistent with the difference between a compact closed object (small junction influence per unit filament) and our extended open Y (junction influence persists further along the filaments before they look isolated).

## What This Settles And Does Not Settle

Settles:

- a working extractor produces all of `mu_0_grid`, `E_filaments`, `E_node`, `E_bulk_residual`, `N_Y` in two normalisations, and `F` in two conventions
- self-calibration is consistent across the three filaments to `1%`
- the boundary-anchor energy artifact has been isolated and excluded from `F`
- the partition is parameter-dependent but `E_interior` is invariant

Does not settle:

- the closed compact configuration on which the paper's `N_Y ~ 3.007` is defined still does not exist in code; this is open three-prong Y measurement only
- grid and box-size sensitivity for the extracted quantities have not been measured
- the asymptotic `mu_0_grid` (as `r_tube -> infinity`) has not been determined cleanly
- no winding-number / topology check has been added; topology preservation across relaxation is currently only inferred from energy and density diagnostics

## Next Pieces

Two natural follow-ups, in increasing order of cost:

1. **Grid + box sensitivity of `N_Y^L`.** Re-run the Y-junction relaxation at `n in {24, 32, 48}` and `half_width in {5, 6, 7}`, run the extractor at the canonical `(r_tube, r_node) = (2.0, 2.0)` setting, and report whether `N_Y^L` and `F^int` move outside their per-state tolerance band under refinement. This is the validation gate for the open Y.
2. **Closed trefoil topology.** Replace the open three-prong skeleton with a closed trefoil-knot skeleton (three filaments meeting at one or two nodes and closing). Re-run the extractor. This is the geometry on which the paper's quoted `N_Y ~ 3.007` is defined.

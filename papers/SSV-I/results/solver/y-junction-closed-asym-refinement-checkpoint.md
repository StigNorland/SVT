# Asymmetric Closed Y-Junction Refinement Gate Checkpoint

This note records the first grid + box sensitivity sweep of the asymmetric
`(+1, +1, -1)` closed Y-junction relaxation + extractor, and the surprising
finding it exposed: stable seeded cores do not imply box-size-convergent
observables.

Artifacts:

- `instruments/paper_i/trefoil_y_junction_closed_asym_refinement.py`
- `papers/SSV-I/data/y-junction-closed-asym-refinement-2026-05-17.json`
- per-run states `y-junction-closed-asym-state-n{n}-hw{hw}-{steps}steps-2026-05-17.npz`

## Sweep Design

The 3 x 3 grid:

- `n in {24, 32, 48}`
- `half_width in {5, 6, 7}`
- step counts scaled as `min(400, 200 * (n / 24)^2)`: 200, 356, 400
- extraction parameters fixed: `r_tube = r_node = 2.0`, `cal_half_width = 0.5`

This mirrors the open-Y refinement so the two can be compared directly.

## Main Sweep Results

| `n` | `hw` | `min_rho` | `final_E` | `E_int` | `E_fil` | `E_top` | `E_bot` | `E_bulk` | `mu_0` | `L_tube` | `N_Y / L` | `F^int` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 24 | 5 | 0.0022 | 764.96 | 134.22 | 33.23 | 13.09 | 12.84 | 75.06 | 2.193 | 15.04 | 1.794 | 2.269 |
| 24 | 6 | 0.0012 | 1001.53 | 176.07 | 24.22 | 12.94 | 12.72 | 126.20 | 1.410 | 15.00 | 2.358 | 3.531 |
| 24 | 7 | 0.0102 | 1222.02 | 213.99 | 20.48 | 12.24 | 12.06 | 169.21 | 1.053 | 14.91 | 2.851 | 4.779 |
| 32 | 5 | 0.0010 | 949.81 | 147.58 | 31.82 | 12.81 | 12.65 | 90.30 | 1.983 | 15.08 | 1.916 | 2.576 |
| 32 | 6 | 0.0013 | 1243.40 | 191.52 | 24.25 | 12.33 | 12.18 | 142.76 | 1.349 | 15.19 | 2.380 | 3.928 |
| 32 | 7 | 0.0037 | 1517.41 | 231.74 | 20.81 | 12.32 | 12.19 | 186.42 | 1.070 | 15.11 | 2.802 | 5.114 |
| 48 | 5 | 0.0005 | 1325.52 | 163.84 | 35.13 | 12.73 | 12.63 | 103.35 | 2.044 | 15.29 | **1.935** | **2.709** |
| 48 | 6 | 0.0001 | 1738.67 | 214.33 | 27.23 | 12.74 | 12.62 | 161.75 | 1.515 | 15.16 | **2.289** | **4.076** |
| 48 | 7 | 0.0002 | 2125.72 | 262.24 | 22.95 | 12.46 | 12.33 | 214.50 | 1.161 | 15.24 | **2.699** | **5.493** |

## Finding 1: Cores Survive Across The Entire Sweep

`min_rho` stays at or below `0.01` everywhere. The deepest cores
(`min_rho ~ 1e-4`) appear at `n = 48`, where the finer grid better resolves
the vortex axis. In contrast to the symmetric closed Y where the cores
migrated away from the seed entirely, the asymmetric configuration preserves
the seeded structure across all `(n, hw)`.

The two pole-ball energies are remarkably consistent: `E_top` and `E_bot`
are both close to `12.5` in every cell (range `12.06` to `13.09`). The pole
regions hold a stable, grid- and box-independent amount of energy. This is
the signature of well-formed singly-quantized monopoles at the two
Y-nodes — exactly what the `(+1, +1, -1)` sign pattern was designed to
produce.

## Finding 2: `N_Y / L` Grid-Converges But Box-Diverges

Holding `hw` fixed and refining `n`:

- `hw = 5`: `1.794 -> 1.916 -> 1.935`. Coarse-to-fine change `7%`.
  `n = 32` to `n = 48`: only `1%`.
- `hw = 6`: `2.358 -> 2.380 -> 2.289`. Non-monotonic, range `4%`.
- `hw = 7`: `2.851 -> 2.802 -> 2.699`. Coarse-to-fine `5%`. `n = 32` to
  `n = 48`: `4%`.

Grid convergence is acceptable: `n = 32` and `n = 48` agree to a few
percent at every `hw`. So the `n -> infinity` limit is well-defined.

Holding `n = 48` and growing the box:

- `hw = 5, 6, 7`: `N_Y / L = 1.935 -> 2.289 -> 2.699`. **Monotone
  increasing by `40%` across `hw in [5, 7]`.**

This is the opposite of the open Y, where `N_Y / L` decreased with `hw`.
But the asym closed Y is similarly not at a stable asymptote in the
tested range.

## Finding 3: `F^int` Grows Linearly With Box Size

This is the unexpected result. Fitting `F^int(hw)` at `n = 48`:

| `hw` | `F^int` measured | linear: `-4.260 + 1.392 * hw` | residual | log: `-10.615 + 8.252 * log(hw)` | residual |
|---:|---:|---:|---:|---:|---:|
| 5 | 2.7086 | 2.7003 | +0.008 | 2.6655 | +0.043 |
| 6 | 4.0759 | 4.0925 | -0.017 | 4.1700 | -0.094 |
| 7 | 5.4929 | 5.4846 | +0.008 | 5.4419 | +0.051 |

The linear fit residuals are below `0.02`. The log fit residuals are
3-6 x larger. `F^int` grows essentially **linearly** with `hw`.

For comparison, the open Y had `F = 0.30 + 1.09 * log(hw)` — a
slower-growing logarithmic divergence. The asymmetric closed Y, despite
being topologically closed, has a **stronger** box-size divergence than
the open Y, not a weaker one.

## Why The Closed Topology Did Not Compactify The Field

The expected story was that closing the configuration removes the long-range
`1/r^2` velocity tails that drive the open-Y divergence: a finite,
topologically-closed vortex configuration should produce only dipolar or
faster-decaying asymptotic fields, giving convergent total energy.

That story is correct for the `(2, 3)`-trefoil knot, which has
`E_anchor_shell / E_total = 1.8%` (a tiny boundary artifact) and behaves
like a true compact object.

It does **not** play out for the asymmetric theta-graph Y-junction.
`E_anchor_shell` is around `80%` of `E_total` in every cell of the sweep,
similar to the symmetric case, and `E_bulk_residual` grows linearly with `hw`
while the seeded line and node energies stay roughly constant or shrink.

Possible reasons (none fully diagnosed here):

1. The `(+1, +1, -1)` sign pattern breaks the 3-fold rotational symmetry
   of the seeded skeleton. The relaxed field develops asymmetric long-range
   modes that the symmetric trefoil knot does not have.
2. The two Y-nodes with opposite-sign net winding form a topological dipole
   with strength `1`, separated by `2 * node_radius = 5 xi`. This dipole has
   a finite asymptotic field, but the bulk energy contribution may still
   accumulate linearly in `hw` before falling off.
3. The cores have migrated slightly from the seeded positions (seen in the
   single-cell extraction note for filament 2 cores near `phi = 240 deg` at
   `r = 2.93` rather than the seeded `r = 2.5`). The relaxed configuration
   may not be a strictly local minimum, but a slowly-drifting saddle.

## Cross-Topology Comparison Update

Re-running the comparison table from the asymmetric prototype note, with the
refinement gate added:

| topology | best `min_rho` | `N_Y / L` | `F^int` | `F^int(hw)` behaviour | `E_anchor` fraction |
|---|---:|---:|---:|---|---:|
| Open Y `(+1,+1,+1)` (n=48) | n/a | 1.15 - 1.39 | 2.06 - 2.57 | `~ 0.30 + 1.09 log(hw)` | n/a |
| Closed Y sym `(+1,+1,+1)` (n=24, hw=6) | 0.012 | 0.56 | 30.65 | dissolved seed; numbers meaningless | 77% |
| Closed Y asym `(+1,+1,-1)` (n=48) | **0.0001** | **1.94 - 2.70** | **2.71 - 5.49** | **`~ -4.26 + 1.39 hw`** | 80% |
| Trefoil knot (n=48, hw=5) | 0.007 | 4.18 | 1.62 | n/a (only viable cell) | **1.8%** |
| Paper I quoted | n/a | 3.007 | 4.47 | n/a | n/a |

The asymmetric closed Y is now the configuration with the deepest, most
stable seeded cores in the repo. It is also the only configuration where
`F^int` is **linearly** divergent in `hw`. That is a real measurement, not
a numerical glitch.

## Gate Verdict

`N_Y / L`:

- grid-convergent at `(n >= 32, hw fixed)` to a few percent
- box-divergent: monotone increasing by `40%` across `hw in [5, 7]`, no
  plateau

`F^int`:

- grid-convergent at fixed `hw`
- box-divergent as `F ~ a + b * hw` with `b ~ 1.39`, fitting linearly to
  better than `0.02` residual across the tested range

Neither observable passes a validation gate.

The intended promotion from `prototype` to `validation` does **not**
happen. The asymmetric closed Y has stable cores but does not produce
box-independent observables.

## What This Settles And Does Not Settle

Settles:

- the `(+1, +1, -1)` phase sign pattern produces a configuration with
  stable, deeply-resolved cores in every `(n, hw)` cell we tested. The
  `+3 -> +1` monopole fix works at the level of preserving the seeded
  geometry.
- the asymmetric closed Y is **not** the right candidate for a clean
  box-convergent `F^int` measurement. Its box dependence is linear, worse
  than the open Y's logarithmic divergence.
- the `(2, 3)`-trefoil knot remains the only topology in the repo whose
  anchor-shell fraction is small (`1.8%`) — the right candidate for a
  compact asymptotic field.

Does not settle:

- the physical origin of the asym closed Y's linear `F` divergence (we
  speculated above but did not test)
- whether the cores have actually settled to a local minimum or are still
  slowly drifting (relaxation only run for 200 steps per cell)
- whether the trefoil knot's `N_Y / L = 4.18` is grid- and box-converged;
  only the `(n = 48, hw = 5)` cell preserved any structure for that
  geometry
- whether a different closed topology (e.g. a `(p, q)`-torus knot with
  three components, or a closed configuration with proper vorticity
  cancellation) could combine the asym Y's seed stability with the trefoil
  knot's clean asymptotics

## Next Pieces

Three plausible follow-ups, in increasing order of cost:

1. **Refinement gate for the `(2, 3)`-trefoil knot** at `(n = 48, hw in
   {5, 6, 7})` with longer step counts, to test whether the marginal cells
   (hw = 6 partial, hw = 7 mostly-dissolved at 400 steps) can be stabilised
   with more relaxation time. Cheapest piece; tests if the trefoil's
   clean-anchor behaviour can be exhibited at multiple boxes for a real
   refinement gate.
2. **Investigate the asym closed Y `E_bulk` linear-in-`hw` source** by
   looking at the spatial distribution of energy density: where exactly is
   the bulk energy concentrated, and does it match a dipolar tail or a more
   exotic asymptotic pattern? This is a diagnostic piece, not a new geometry.
3. **`(+1, +1, +1, -1, -1, -1)` six-arc configuration** that pairs each
   filament with an anti-image, fully cancelling all net pole winding. This
   would test whether further reducing the net topological charge actually
   compactifies the bulk in the closed Y-junction family.

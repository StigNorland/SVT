# Closed Y-Junction Observables Checkpoint

This note records the first arc-aware `N_Y` / `F` extractor and an unexpected structural finding it exposed about the closed theta-graph Y-junction.

Artifacts:

- `src/paper_i/trefoil_y_junction_closed_observables.py`
- `papers/SSV-I/data/y-junction-closed-observables-n24-hw6-200steps-2026-05-17.json`

## What The Extractor Does

The arc-aware variant of `trefoil_y_junction_observables.py`:

1. Reconstructs the three arc curves from the saved state's config (samples each arc at `samples_per_arc = 200` points).
2. For each grid cell, finds the nearest sample on each arc and records the perpendicular distance `d_k` and the cumulative arc-length parameter `s_k` at that nearest sample.
3. Voronoi assigns each cell to its nearest arc.
4. Defines three tube masks (one per arc) and **two** node-ball masks (one at each pole).
5. Self-calibrates `mu_0_grid` from an equatorial slab `s_k in [s_total/2 - cal_half_width, s_total/2 + cal_half_width]` along each arc, where the arc is farthest from both Y-nodes.
6. Reports the same `N_Y^xi`, `N_Y^L`, `F^int` quantities as the open-Y extractor, plus per-arc geometric and tube-derived arc lengths.

## Run On The 200-Step Closed-Y State (n=24, hw=6)

| quantity | value |
|---|---:|
| `E_total_raw` | `288.98` |
| `E_anchor_shell` | `223.92` (77.5%) |
| `E_interior` | `65.07` |
| `E_filaments` (3 arc tubes) | **`2.07`** |
| `E_node_top` (around `(0,0,+2.5)`) | **`0.026`** |
| `E_node_bottom` (around `(0,0,-2.5)`) | **`0.024`** |
| `E_bulk_residual` | `62.94` |
| `mu_0_grid` | `0.253` |
| `L_filament_tube` | `15.00` |
| `L_filament_geometric` | `23.56` |
| `N_Y^L` | `0.560` |
| `F^int` | `30.65` |

The extractor is mechanically correct: per-arc tube volumes are reasonable, the calibration slab fits inside the geometric arc length, and `E_filaments + E_node_top + E_node_bottom + E_bulk_residual = E_interior` to numerical precision. But the headline numbers are nonsense compared to expectations:

- `E_filaments = 2.07` is ~20x smaller than the open Y's `41.13` at the same `(n, hw)`
- `E_node_top` and `E_node_bottom` are essentially zero
- `E_bulk_residual` is `62.94`, accounting for 97% of the interior energy

That last line is the diagnostic: virtually all of the physical interior energy lives **outside** the seeded arc tubes and node balls. The seeded geometry no longer matches where the field is doing work.

## Why: The Seeded Topology Dissolved

A density probe of the relaxed state shows the actual vortex cores at:

- 88 grid cells with `rho < 0.1`
- all in the equatorial plane (`z = 0` to within one cell)
- phi distribution clustered at `(60, 180, 300) deg`, **rotated 60 deg from the seeded `(0, 120, 240) deg`** filament directions
- at cylindrical radius `r_cyl ~ 5.2 - 6.3 xi`, far outside the seeded `arc_radius = 2.5`

Cross-tabulating energy by region (excluding the anchor shell):

| region | energy |
|---|---:|
| `r < 2` around top pole | `0.026` |
| `r < 2` around bottom pole | `0.024` |
| `r_cyl > 4`, `|z| < 3` (equatorial outer ring) | **`52.08`** (80%) |
| `r_cyl <= 4`, excluding poles | `7.78` |

The energy is concentrated in an equatorial outer ring, not in the seeded theta-graph skeleton.

## Mechanism

The seeded product-vortex ansatz with three `+1`-winding arcs converging at each pole places a `+3` winding monopole at each Y-node. In 2D, multiply-quantized vortices are known to be unstable to fission into single-charge vortices. The same dynamics apply here: the `+3` monopole at each pole dissociates into three `+1` cores. Energy minimisation then pushes those cores outward (away from their mutual repulsion) until they settle in the equatorial belt where the box geometry and anchor shell constrain them.

The relaxation did not fail. It found a stable configuration. But that configuration is **not** the theta-graph seeded by the initial condition. The seeded topology is unstable in pure LogSE gradient flow.

## What This Settles And Does Not Settle

Settles:

- the arc-aware extractor mechanics work (per-arc tube + two-node-ball decomposition, equatorial-slab self-calibration, all quantities additive to `E_interior`)
- the symmetric `(+1, +1, +1)` closed Y-junction is **not** a LogSE soliton at the seeded geometry; it dissociates and the cores migrate to a different configuration
- the same instability presumably affects the symmetric `(+1, +1, +1)` open Y-junction too, but the open Y's box-boundary anchor pinned the filament endpoints and prevented dissolution; the open Y's measured `N_Y/L ~ 1.2` was thus a number for an artificially-stabilised configuration

Does not settle:

- whether any closed Y-junction topology is a stable LogSE soliton (we only tried the simplest one)
- the actual `N_Y` and `F` for whatever configuration **is** stable in this geometry (we would need to identify the relaxed core positions and re-build an extractor around those)
- whether the existing `trefoil_breather_static.py` `(2,3)`-trefoil knot state (no Y-junctions, single continuous closed curve) is stable; that geometry does not have the `+3` monopole problem and is a separate candidate

## Implications For Paper I

The paper's `N_Y ~ 3.007` and `F ~ 4.47` are reported as numerical minimisation outputs for the proton's three-filament Y-junction. The current finding shows that the simplest symmetric closed realisation of that geometry does not minimise to a stable Y-junction at all. Either:

- the paper's configuration uses an asymmetric phase pattern (e.g. `(+1, +1, -1)`) that produces a `+1` rather than `+3` monopole at the node, removing the fission instability
- or the paper's configuration uses external pinning (a confining potential or fixed boundary conditions on the filaments) that holds the cores in place
- or the paper's quoted numbers are for the unstable seed rather than the relaxed minimum

The first option is the most physical and consistent with the paper's "colour charge as `120 deg` phase" picture: phase offsets do not change the topology, but a sign flip on one filament does, and it is the sign-flipped configuration that has the right `+1` net winding at each node.

## Next Piece

The natural follow-up is the **asymmetric `(+1, +1, -1)` closed Y-junction**.

Concrete shape:

- copy `trefoil_y_junction_closed_static.py` to a sibling script
- reverse the phase winding of one of the three arcs (flip the sign of one `theta_k` in the product-vortex sum)
- this gives net winding `+1 + 1 - 1 = +1` at the top pole and `-1` at the bottom pole, both safely single-quantized
- re-run the relaxation, re-extract, check that the cores stay near the seeded arcs
- if yes, this is the first stable closed Y-junction in the repo, and `N_Y` / `F` for it can finally be compared to the paper's quoted numbers

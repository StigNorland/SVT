# Closed Y-Junction Prototype Checkpoint

This note records the first compact-closed Y-junction relaxation in the repo.

Artifacts:

- `src/paper_i/trefoil_y_junction_closed_static.py`
- `papers/SSV-I/data/y-junction-closed-checkpoint-n24-hw6-200steps-2026-05-17.json`
- `papers/SSV-I/data/y-junction-closed-state-n24-hw6-200steps-2026-05-17.npz`
- `papers/SSV-I/data/y-junction-closed-checkpoint-n24-hw6-600steps-2026-05-17.json`
- `papers/SSV-I/data/y-junction-closed-state-n24-hw6-600steps-2026-05-17.npz`

## Why This Geometry

The open three-prong Y had a `log(hw)` (or possibly linear) `F^int` divergence under box-size refinement. That is a structural property of three filaments emanating to infinity from one node: the asymptotic vortex velocity field falls off too slowly for the kinetic-energy integral to converge.

The closed compact topology removes this. The simplest minimal-change closed configuration is the **theta-graph**: two Y-junctions joined by three arcs.

- two Y-nodes at `(0, 0, +h)` and `(0, 0, -h)`
- three vortex filaments connecting them, each in a meridian plane at `120 deg` apart
- each filament is a half-ellipse with equatorial radius `arc_radius` and polar half-axis `node_radius`
- 3-fold rotational symmetry about the `z`-axis

Default geometry: `arc_radius = node_radius = 2.5`, so each filament is a great-circle arc on a sphere of radius `2.5 xi`. With `half_width = 6`, the closed structure has roughly `3 xi` of clearance to the box boundary on all sides.

## Initial Condition

The same product-vortex ansatz used for the open Y, lifted to three arcs:

\[
\Psi(\vec x) = \prod_{k=1}^{3} \tanh\!\left(\frac{d_k(\vec x)}{\sqrt{2}\,\xi}\right)
\exp\!\left(i \sum_{k=1}^{3} \theta_k(\vec x)\right),
\]

where for each arc `k`:

- the curve is sampled at `samples_per_arc = 200` points along `alpha in [0, pi]`
- for each grid point the nearest sample on arc `k` is identified
- `d_k` is the perpendicular distance to the nearest sample
- `theta_k` is the azimuthal angle around the local arc tangent, using the in-meridian-plane perpendicular `e1` and the azimuthal direction `e2` as the reference frame

The phase ansatz puts unit vortex winding around each arc and lets the field naturally form `|psi| = 0` at the two Y-nodes (where all three `amp_k -> 0`).

## Boundary Anchor

Reuses the initial-state anchor from the open-Y script. For the compact closed configuration this is precautionary: the filaments do not reach the boundary, so the initial-state field at the outer shells is essentially the multi-vortex asymptotic pattern with `|psi|` close to `1`. Anchoring to that pattern prevents the outer shells from drifting during relaxation.

## Run Numbers (n = 24, hw = 6)

200-step run:

| quantity | value |
|---|---:|
| initial energy | `433.57` |
| final energy | `288.98` (33% reduction) |
| monotonicity violations | `0` |
| residual norm | `0.665` |
| min density | `0.0119` |
| max density | `0.9995` |
| depressed fraction | `2.66%` |
| deficit volume | `191.57` |
| equivalent deficit radius | `3.58` |
| effective radius | `5.81` |
| far-field shell density | `0.842` |

600-step run plateaus at the same numbers:

- final energy `288.94` (`-0.04` vs 200-step)
- residual norm `0.666`
- min density `0.0158`

The plateau is reached within `200` steps, the same pattern observed for the open Y.

## Anchor-Shell vs Interior Energy

A direct decomposition of the 200-step state:

- `E_total = 288.98`
- `E_anchor_shell = 223.92` (77.5% of `E_total`)
- `E_interior = 65.07`

The anchor-shell fraction is still large because the closed configuration has a non-trivial asymptotic phase pattern: walking around the structure, the cumulative phase variation is non-zero, so the discrete `np.roll` gradients at the pinned outer shells generate cost when wrapping faces to each other. The interior energy `E_interior = 65.07` is the physical quantity.

For comparison the open Y at the same `(n=24, hw=6)` had `E_interior = 116.22` with a similar 86% anchor-shell fraction. The closed configuration has roughly half the interior energy of the open Y, despite having `~2x` total filament length (`~23.6 xi` geometric arc length vs `~10.98 xi` measured tube length for the open Y). The per-filament-length energy density is correspondingly smaller, which is plausible because curved filaments interact constructively with their neighbours in the theta-graph and the bulk between them is less perturbed than along the open Y's three straight rays to the boundary.

## What This Settles And Does Not Settle

Settles:

- a compact closed Y-junction can be initialised, anchored, and relaxed on the same grid + relaxation machinery as the open Y
- the relaxation is stable: zero monotonicity violations, energy plateau reached within `~200` steps, cores well-resolved (min density `~0.01`)
- the structural assumption that closed topology removes the open-Y `F` divergence is implementation-ready: the same extractor logic can now be applied to a configuration without filament endpoints at the box boundary

Does not settle:

- `N_Y` and `F` themselves are not yet measured for this geometry; the open-Y extractor assumes three straight half-line filaments and will not work on arc filaments without adjustment
- the asymptotic phase-pattern contribution to `E_anchor_shell` has not been characterised analytically; we observe it numerically but have not proven that `E_interior` itself is box-size-convergent
- grid and box-size sensitivity for the closed configuration are not yet measured
- no comparison to the existing closed `(2,3)` trefoil knot prototype (`trefoil_breather_static.py`) on equal footing

## Next Piece

The natural follow-up is the **arc-aware extractor**.

Concrete shape:

- read a saved closed-Y state
- sample each arc curve at many points
- for each grid cell, identify the nearest arc, compute perpendicular distance and arc-length parameter
- tube mask per arc: `d_k < r_tube`, `alpha_k in (alpha_min, alpha_max)` to exclude both Y-nodes
- two junction balls: one around each Y-node `|x - (0,0,+h)| < r_node` and `|x - (0,0,-h)| < r_node`
- self-calibrate `mu_0_grid` from a slab around `alpha = pi/2` (the equator) where each filament looks most like an isolated curved vortex
- report `N_Y^L = (E_filaments + E_node_top + E_node_bottom) / (mu_0_grid * L_filament_total)` and the corresponding `F^int`

Once that produces numbers, the closed-Y refinement gate can be run across `(n, hw)` and the box-convergence of `F` (the open-Y showed `log(hw)` divergence; the closed-Y should plateau) can be measured directly.

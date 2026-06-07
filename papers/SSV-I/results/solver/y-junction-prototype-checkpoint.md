# Y-Junction Prototype Checkpoint

This note records the first concrete 3D realisation of the open three-prong Y-junction geometry on which Paper I's `N_Y` and `F` are defined.

Artifacts:

- `instruments/paper_i/trefoil_y_junction_static.py`
- `papers/SSV-I/data/y-junction-checkpoint-n24-hw6-200steps-2026-05-16.json`
- `papers/SSV-I/data/y-junction-state-n24-hw6-200steps-2026-05-16.npz`
- `papers/SSV-I/data/y-junction-checkpoint-n24-hw6-600steps-2026-05-16.json`
- `papers/SSV-I/data/y-junction-state-n24-hw6-600steps-2026-05-16.npz`

## Why This Is The Right Object

Paper I defines the proton mass closure as

\[
m_p c^2 = N_Y \cdot F \cdot \mu_0,
\quad \mu_0 = m_e / \alpha \approx 70 \text{ MeV},
\]

where `N_Y` is the dimensionless node-cost factor from the 3D minimisation of three vortex filaments meeting at a central node, and `F = E_{breather}^{3D} / (N_Y \mu_0)` is the breather form factor.

Both quantities are defined on a Y-junction (three filaments + node), not on the closed trefoil filament that the existing `trefoil_breather_static.py` relaxes. The prototype here is the first script in the repo whose geometry actually matches the definition.

## Geometry

Three vortex filaments emanate from the origin as straight half-lines in the equatorial plane at `0`, `120`, `240` degrees. The initial condition uses the canonical product-vortex ansatz:

\[
\Psi(\vec x) = \prod_{k=1}^{3} \tanh\!\left(\frac{d_{\rm eff}^{(k)}(\vec x)}{\sqrt 2 \, \xi}\right)
\exp\!\left(i \sum_{k=1}^{3} \theta_k(\vec x)\right),
\]

with `d_eff^(k) = sqrt(d_perp^2 + max(0, -s)^2)` extending each filament smoothly as a half-line from the origin, and `theta_k` the azimuthal angle around filament `k`.

The 120 degree phase balance at the node is not added as an extra colour offset — it is a geometric consequence of summing the three azimuthal angles, which produces unit winding around each filament and total winding 3 around the central node.

## Boundary Anchor

The single non-trivial design decision was the boundary condition.

A first run with the same uniform-background anchor used by `trefoil_breather_static.py` (outer shells pinned to `\Psi = 1`) caused the entire Y-junction to dissolve in 200 steps: final energy `0.63`, min density `0.993`, depressed fraction `0.0`. The open filament ends retracted from the box and the topology vanished.

The fix is to anchor the outer shells to the initial-state field rather than to uniform background. Physically this represents the filaments continuing into the surrounding bulk beyond the simulation box, which is the implicit setup behind the paper's quoted `N_Y`.

With the initial-state anchor in place, the same 200-step run preserves the topology cleanly:

- final energy: `857.0` (from initial `901.0`)
- min density: `0.032` — matches `tanh^2(\Delta x / 2 \sqrt 2)` exactly, so the cores hit the analytic tanh depth at one half-spacing from the filament axis
- max density: `1.000`
- depressed fraction: `5.4%`
- deficit volume: `235.7`
- effective radius: `4.45`
- zero monotonicity violations across all 200 steps

The 600-step run barely moves these numbers (final energy `856.4`, deficit volume `234.7`, same min density), confirming that the relaxation reaches a quasi-stationary plateau well before 200 steps. The tanh ansatz was already near-optimal locally.

## Residual Norm Interpretation

The reported `residual_norm` is around `1.3` and does not decrease after the energy plateau. This is largely a diagnostic artefact: the gradient at the pinned outer shells is re-zeroed every step by the anchor, but those cells still contribute to the global residual norm. The interior is at or near a local minimum; the boundary cells perpetually disagree with the gradient flow.

The next step (`N_Y` / `F` extractor) will need a tube-localised energy decomposition, which will simultaneously give a cleaner interior-only residual measure.

## What This Checkpoint Settles And Does Not Settle

Settles:

- the Y-junction geometry can be initialised, anchored, and relaxed without losing the topology
- the product-vortex ansatz with initial-state anchoring is a stable starting substrate
- the existing observables (`deficit_volume`, `effective_radius`, far-field shell density, etc.) carry over without modification
- relaxation reaches a plateau within roughly 200 steps on the coarse branch

Does not settle:

- `N_Y` is not yet measured — no filament / junction energy decomposition exists
- `F` is not yet measured — no `E_breather^{3D} / (N_Y \mu_0)` calculation exists
- topology preservation is not numerically certified — no winding-number check
- grid and box sensitivity for this geometry are not yet measured
- the closed trefoil knot topology is not implemented; this is the open three-prong Y

## Next Piece

The natural follow-up is the `N_Y` / `F` extractor.

Concrete shape:

- read a saved relaxed Y-junction state
- define a tubular neighbourhood of each filament out to some `r_tube ~ few \xi`
- integrate the LogSE energy density inside the union of the three tubes -> `E_filaments`
- integrate the LogSE energy density inside a junction ball of radius `r_node ~ few \xi` -> `E_junction`
- integrate the LogSE energy density everywhere -> `E_total = E_breather^{3D}`
- report `N_Y = (E_filaments + E_junction) / \mu_0_grid`, where `\mu_0_grid` is the per-unit-length filament energy obtained from a calibration run at the same grid spacing
- report `F = E_total / (N_Y \cdot \mu_0_grid)`

That is the smallest piece that produces the actual Paper I closure observables.

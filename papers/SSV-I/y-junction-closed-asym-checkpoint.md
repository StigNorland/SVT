# Asymmetric Closed Y-Junction Checkpoint

This note records the asymmetric `(+1, +1, -1)` closed Y-junction prototype,
designed to remove the `+3` winding monopole at each pole that destroyed the
symmetric closed seed.

Artifacts:

- `src/paper_i/trefoil_y_junction_closed_asym_static.py`
- `papers/SSV-I/data/y-junction-closed-asym-checkpoint-n24-hw6-200steps-2026-05-17.json`
- `papers/SSV-I/data/y-junction-closed-asym-state-n24-hw6-200steps-2026-05-17.npz`
- `papers/SSV-I/data/y-junction-closed-asym-checkpoint-n24-hw6-600steps-2026-05-17.json`
- `papers/SSV-I/data/y-junction-closed-asym-state-n24-hw6-600steps-2026-05-17.npz`
- `papers/SSV-I/data/y-junction-closed-asym-observables-n24-hw6-200steps-2026-05-17.json`

## What Changed

Same skeleton as `trefoil_y_junction_closed_static.py` (theta-graph, three arcs
in meridian planes at `120 deg`, two Y-nodes at `(0, 0, +-2.5)`). Same
product-vortex amplitude `amp = prod_k tanh(d_k / sqrt(2) xi)`. The only
modification is the phase sum:

\[
\phi_{\rm total}(x) = \sum_{k=1}^{3} \sigma_k \theta_k(x),
\]

with the sign pattern `sigma = (+1, +1, -1)`. The third arc carries unit
**anti**-winding around its tangent direction.

The topological consequence:

- symmetric `(+1, +1, +1)`: net winding `+3` at each Y-node → multi-quantum
  monopole → unstable to fission into single-charge cores
- asymmetric `(+1, +1, -1)`: net winding `+1 + 1 - 1 = +1` at each Y-node →
  singly-quantized monopole → no fission instability

## Run At n=24, hw=6

| step count | `final_E` | `min_rho` | `depressed_frac` | `residual` |
|---:|---:|---:|---:|---:|
| 200 | `1001.53` | `0.0012` | `6.35%` | `1.371` |
| 600 | `1000.66` | `0.0010` | `6.15%` | `1.372` |

Plateau reached well before 200 steps: 200 → 600 changes `final_E` by `0.88`
out of `1001`, `min_rho` by `0.0002`. Zero monotonicity violations across
either run.

Critically, `min_rho ~ 0.001` means the **vortex cores survive intact**, in
sharp contrast to the symmetric variant where they dissolved and migrated to
the equatorial outer ring.

## Extractor Output (n=24, hw=6, 200 steps)

Run the existing `trefoil_y_junction_closed_observables.py` against the
asymmetric state (same arc geometry, so the extractor is reusable):

| quantity | asymmetric | symmetric (for comparison) |
|---|---:|---:|
| `E_total_raw` | `1001.53` | `288.98` |
| `E_anchor_shell` | `825.47` (82.4%) | `223.92` (77.5%) |
| `E_interior` | `176.07` | `65.07` |
| `E_filaments` | **`24.22`** | **`2.07`** |
| `E_node_top` | **`12.94`** | **`0.026`** |
| `E_node_bottom` | **`12.72`** | **`0.024`** |
| `E_bulk_residual` | `126.20` | `62.94` |
| `mu_0_grid` | `1.41` | `0.253` |
| `mu_0_per_filament` | `[1.96, 1.20, 1.07]` | `[0.23, 0.29, 0.23]` |
| `N_Y / L` | `2.36` | `0.56` |
| `F^int` | `3.53` | `30.65` |

The structural difference jumps out:

- `E_filaments + E_node_top + E_node_bottom` goes from `2.12` (symmetric, 3% of
  `E_interior`) to **`49.88`** (asymmetric, 28% of `E_interior`). The seeded
  geometry is no longer a ghost; it carries real energy.
- `mu_0_grid` jumps from `0.25` to `1.41`. The calibration slab now sees a
  proper vortex line at the seeded position, not just background.
- `mu_0_per_filament` is no longer uniform: `[1.96, 1.20, 1.07]`. The
  asymmetric `(+1, +1, -1)` pattern breaks the three-fold symmetry, so the
  three filaments are no longer interchangeable. Filament 0 has the highest
  per-length energy in this convention.
- `F^int` drops by an order of magnitude (`30.65 -> 3.53`). The symmetric
  case's `30.65` was nonsensical because the denominator (`mu_0`) was
  measuring dissolved background; the asymmetric `3.53` is in a physically
  reasonable range for the first time.

## Core Locations

Low-density cells (`rho < 0.1`) of the relaxed asymmetric state:

| `phi` bin | count | mean `r_{cyl}` | `z` range |
|---|---:|---:|---|
| `[30, 60)` | 48 | 3.51 | `[-3.8, +3.8]` |
| `[60, 120)` | 28 | 3.63 | `[-3.8, +3.8]` |
| `[120, 180)` | 36 | 3.90 | `[-2.8, +2.8]` |
| `[180, 240)` | 16 | **2.93** | `[-2.8, +2.8]` |
| `[240, 300)` | 8 | 6.27 | `[-2.8, +2.8]` |
| `[300, 360)` | 48 | 4.31 | `[-2.8, +2.8]` |

Compare to the symmetric case where low-density cells clustered in the
equatorial plane only at `r > 5` and `phi = (60, 180, 300) deg`. The
asymmetric configuration:

- has cores distributed across most `phi` bins (more representative of the
  seeded three-arc structure)
- has `z`-extent up to `+-3.8 xi` (the arcs span `z in [-2.5, +2.5]`, so the
  cores are roughly where the arcs are)
- the `phi in [180, 240)` bin has 16 cells at `r = 2.93`, very close to the
  seeded filament 2 position (`phi = 240 deg`, `r = 2.5` at the equator)

The asymmetric cores are not at the seeded positions exactly but they are
recognisably close to the three-arc skeleton, especially for filament 2 (the
sign-flipped one). The seeded geometry survives in a way the symmetric one
did not.

## What This Settles

- the symmetric `(+1, +1, +1)` closed Y-junction's dissolution was driven
  specifically by the `+3` monopole instability at each pole, not by some
  more fundamental issue with the closed theta-graph topology
- a single sign flip in the phase ansatz is sufficient to make the
  configuration robustly survive relaxation, with cores roughly at the seeded
  positions
- `N_Y / L = 2.36` and `F^int = 3.53` are the first closed Y-junction
  numbers in the repo that are based on a real seeded geometry rather than a
  dissolved or reorganised one

## What This Does Not Settle

- the asymmetric configuration breaks the `120 deg` color-symmetry the paper
  emphasises. Whether this maps to the paper's "proton Y-junction" is a
  physics question, not a numerical one
- 72% of `E_interior` still lives in `E_bulk_residual`, so the extractor's
  seeded tubes do not capture most of the energy. The asymmetric phase
  pattern produces extended-bulk velocity structure that the local
  decomposition cannot localise. Larger `r_tube` would catch more but at the
  cost of overlap between tubes
- per-filament `mu_0` ranges from `1.07` to `1.96` (factor of 1.8), reflecting
  the broken symmetry. Which calibration slab to use is no longer
  unambiguous; the simple mean is what we report but it averages across
  inequivalent filaments
- only one `(n, hw)` cell was run; no refinement gate yet

## Comparison With Other Topologies

| topology | `min_rho` | `N_Y / L` | `F^int` | `E_anchor / E_total` | comment |
|---|---:|---:|---:|---:|---|
| Open Y `(+1,+1,+1)` (n=48, hw=7) | n/a | `1.22` | `2.41` | n/a | anchor pins endpoints |
| Closed Y sym `(+1,+1,+1)` (n=24, hw=6) | `0.012` | `0.56` | `30.65` | 77% | seed dissolved + reorganised |
| Closed Y asym `(+1,+1,-1)` (n=24, hw=6) | **`0.001`** | **`2.36`** | **`3.53`** | 82% | seed survives, cores near arcs |
| Trefoil knot (n=48, hw=5) | `0.007` | `4.18` | `1.62` | 1.8% | only viable trefoil state |
| Paper I quoted | n/a | `3.007` | `4.47` | n/a | geometry definition ambiguous |

The asymmetric closed Y-junction is now the first multi-filament configuration
with both a stable seeded geometry and a finite `F^int` (no `log(hw)`
divergence, no anchor-pinning artefact). Its `N_Y / L = 2.36` is in the
neighbourhood of the paper's `N_Y = 3.007` and the trefoil knot's `4.18`.

## Next Pieces

Three plausible follow-ups, in increasing order of cost:

1. **Refinement gate for the asymmetric closed Y** at `(n, hw) in
   {24, 32, 48} x {5, 6, 7}`, reusing the existing refinement harness pattern
   from `trefoil_y_junction_refinement.py`. Quantifies grid + box sensitivity
   of `N_Y / L` and `F^int`, and verifies the predicted `F^int`
   box-convergence of the closed configuration (the open Y's `log(hw)`
   divergence should not appear here).
2. **`(+1, -1, 0)`-equivalent topology** — two filaments cancel, leaving a
   single effective vortex line, as a sanity check that the extractor and
   physics interpretation are consistent.
3. **Validation closure on the asymmetric Y**: if step 1 shows clean
   grid/box convergence, the asymmetric closed Y-junction can be promoted
   from `prototype` to `validation` for `N_Y / L` and `F^int`, the first
   such promotion in the Y-junction track.

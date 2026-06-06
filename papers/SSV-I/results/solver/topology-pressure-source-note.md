# Topology Pressure Source Note

This note records the first carry-through of the medium-pressure topology branch into the existing static source diagnostics.

Artifacts:

- [topology-pressure-source-mechanism-2026-05-17.json](../../papers/SSV-I/data/topology-pressure-source-mechanism-2026-05-17.json)
- [topology-pressure-cumulative-compare-2026-05-17.json](../../papers/SSV-I/data/topology-pressure-cumulative-compare-2026-05-17.json)

States compared:

- baseline branch from the fresh `n = 48`, `half_width = 7` initial state:
  [trefoil-baseline-n48-hw7-steps80.npz](../../papers/SSV-I/data/topology-guard-probe-2026-05-17w50/trefoil-baseline-n48-hw7-steps80.npz)
- medium-pressure branch (`topology_pressure_weight = 50`):
  [trefoil-topology_pressure-n48-hw7-steps80.npz](../../papers/SSV-I/data/topology-guard-probe-2026-05-17w50/trefoil-topology_pressure-n48-hw7-steps80.npz)

## Main Result

The medium-pressure branch does not merely rescale the baseline source. It changes the interior build-up pattern.

Totals:

- baseline:
  - `deficit_volume ~ 253.07`
  - `Q_p^eff ~ 249.93`
  - `projected_residual_norm ~ 0.139`
- topology pressure:
  - `deficit_volume ~ 273.69`
  - `Q_p^eff ~ 271.29`
  - `projected_residual_norm ~ 0.255`

So the topology-pressure branch is still heavier and less relaxed than baseline, but the more important point is how that extra source is distributed.

## Region Split

With the same `core / mid / halo` split at radii `2` and `5`:

- baseline:
  - core deficit fraction `~ 0.066`
  - mid deficit fraction `~ 0.522`
  - halo deficit fraction `~ 0.412`

- topology pressure:
  - core deficit fraction `~ 0.067`
  - mid deficit fraction `~ 0.576`
  - halo deficit fraction `~ 0.358`

The pressure branch shifts weight from halo into the mid region.

That is exactly the kind of movement we hoped to see: the topology pressure is not simply inflating the same long-range halo. It is making the source somewhat more interior.

## Cumulative `Q_p(<r)` Curves

The cumulative comparison shows the same thing.

At shared radii:

- `r = 2`: baseline `16.28`, pressure `17.62`
- `r = 4`: baseline `110.87`, pressure `128.52`
- `r = 5`: baseline `150.95`, pressure `178.25`
- `r = 6`: baseline `179.01`, pressure `199.94`
- `r = 8`: baseline `237.69`, pressure `250.97`

But the normalized fractions tell the more important story:

- `r = 5`: baseline `0.604`, pressure `0.657`
- `r = 6`: baseline `0.716`, pressure `0.737`
- `r = 8`: baseline `0.951`, pressure `0.925`

So the pressure branch accumulates a larger fraction of its total source in the mid-interior, and leaves relatively less in the outer part of the interior support.

## Interpretation

This is not a final fix. The medium-pressure branch still:

- has a higher projected residual than baseline
- still does not recover unit winding
- still remains a prototype branch, not a closure-grade result

But it is the first branch-selection modification that improves the source distribution in the direction we actually want:

- less halo-dominated than the baseline branch
- more of the source built in the mid region
- still interior-settled before the blend layer

## Consequence

The next topology-aware closure step should keep working with the pressure-style branch rather than the hard guard.

The most useful immediate follow-up is:

- tune the medium-pressure strength around the current `50` scale
- track how the mid-vs-halo split and cumulative fractions move
- then decide whether this branch is converging toward a more compact topological source family

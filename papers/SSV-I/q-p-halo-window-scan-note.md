# `Q_p` Halo Window Scan Note

This note records the first direct scan of how the extracted static source splits between inner support and outer halo as the support cutoff radius is moved.

Artifact:

- `papers/SSV-I/data/q-p-halo-window-scan-2026-05-17.json`

Inputs:

- `half_width = 6`, `n = 48`, projected-residual plateau state
- `half_width = 7`, `n = 48`, constrained plateau state
- `half_width = 8`, `n = 64`, constrained plateau state

The scan evaluates hard and smooth windows at cutoff radii

- `r_c = 2, 3, 4, 5, 6, 7, 8, 9, 10`

and reports the inner and outer contributions to `Q_p^eff`.

## Main Result

There is no obvious fixed cutoff radius that makes the inner-support source stable across `half_width = 6, 7, 8`.

For a hard cutoff at `r_c = 5`:

- `half_width = 6`: inner `Q_p^eff ~ 46.21`, outer fraction `~ 0.487`
- `half_width = 7`: inner `Q_p^eff ~ 20.99`, outer fraction `~ 0.654`
- `half_width = 8`: inner `Q_p^eff ~ 58.79`, outer fraction `~ 0.759`

For a hard cutoff at `r_c = 6`:

- `half_width = 6`: inner `Q_p^eff ~ 69.72`, outer fraction `~ 0.226`
- `half_width = 7`: inner `Q_p^eff ~ 34.20`, outer fraction `~ 0.437`
- `half_width = 8`: inner `Q_p^eff ~ 93.90`, outer fraction `~ 0.616`

For a hard cutoff at `r_c = 7`:

- `half_width = 6`: inner `Q_p^eff ~ 84.55`, outer fraction `~ 0.061`
- `half_width = 7`: inner `Q_p^eff ~ 47.48`, outer fraction `~ 0.218`
- `half_width = 8`: inner `Q_p^eff ~ 139.49`, outer fraction `~ 0.429`

So even when the cutoff is pushed well beyond the mid region, the `half_width = 8` state still carries a much larger outer-halo contribution than the `6/7` states.

## What This Means

This is the first clean control statement about the halo.

The previous mechanism probe showed that the large `half_width = 8` source is halo-dominated. This scan adds the stronger point:

- the effect does not disappear under any simple fixed support cutoff in the tested range
- and the inner support extracted at a given cutoff does not line up cleanly across `half_width = 6, 7, 8`

So the problem is not just that the full-domain source includes "too much halo." The problem is that the source is being reorganized across scales in a way that no simple fixed-radius support window resolves automatically.

## Interpretation

This pushes the open question one level deeper.

The repo now needs to decide between two possibilities:

- the proton source functional really is nonlocal enough that the outer halo must be included in a scale-aware way
- or the current constrained static branch is missing a closure condition, so the halo is carrying spurious source weight

At this point, picking a hard cutoff like `r < 5` or `r < 6` would be a modeling choice, not something the current numerics have justified.

## Best Next Probe

The next good step is not another ansatz fit. It is to compare the cumulative inner-source curves directly and look for a plateau in radius:

- does `Q_p(<r)` flatten anywhere before the box edge?
- if it does, is that plateau shared across `half_width = 6, 7, 8`?

If there is no shared plateau region, then the static support definition itself is still open.

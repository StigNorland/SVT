# `Q_p(<r)` Interior Cumulative Curve Comparison

This note records the direct comparison of cumulative source curves

\[
Q_p(<r)
\]

across the plateaued `half_width = 6, 7, 8` static states on shared physical radii.

Artifact:

- `papers/SSV-I/data/q-p-cumulative-curve-compare-2026-05-17.json`

Inputs:

- `half_width = 6`, `n = 48`, projected-residual plateau state
- `half_width = 7`, `n = 48`, constrained plateau state
- `half_width = 8`, `n = 64`, constrained plateau state

Shared sample radii:

- `r = 1, 2, 3, 4, 5, 6, 7, 8`

All of these radii lie inside the blend-start radius for every tested state, so this comparison is entirely interior to the recovery layer.

## Main Result

The interior cumulative curves do **not** line up on any shared radius band.

Representative values:

At `r = 4`:

- `half_width = 6`: `Q_p(<4) ~ 24.73`
- `half_width = 7`: `Q_p(<4) ~ 11.42`
- `half_width = 8`: `Q_p(<4) ~ 33.30`

At `r = 5`:

- `half_width = 6`: `Q_p(<5) ~ 46.15`
- `half_width = 7`: `Q_p(<5) ~ 21.12`
- `half_width = 8`: `Q_p(<5) ~ 58.62`

At `r = 6`:

- `half_width = 6`: `Q_p(<6) ~ 69.70`
- `half_width = 7`: `Q_p(<6) ~ 34.15`
- `half_width = 8`: `Q_p(<6) ~ 94.09`

At `r = 7`:

- `half_width = 6`: `Q_p(<7) ~ 84.58`
- `half_width = 7`: `Q_p(<7) ~ 47.47`
- `half_width = 8`: `Q_p(<7) ~ 139.36`

The relative spread in the raw cumulative source stays large throughout:

- `r = 4`: about `0.657`
- `r = 5`: about `0.640`
- `r = 6`: about `0.637`
- `r = 7`: about `0.659`
- `r = 8`: about `0.698`

The normalized fractions also fail to collapse to a common interior curve. For example:

At `r = 6`:

- `half_width = 6`: about `0.774` of total
- `half_width = 7`: about `0.562` of total
- `half_width = 8`: about `0.385` of total

So even after normalizing by each state's own total source, the interior build-up pattern is still materially different.

## Interpretation

This is the strongest current interior-control result in the repo.

The previous checks showed:

- the large `half_width = 8` source is halo-dominated
- the source is already settled before the blend layer begins

This new comparison adds the key missing point:

- the disagreement is already present throughout the interior cumulative curves themselves

So there is no obvious shared interior radius band where the three branches are all building the same source and only differ in the outer tail.

## Consequence

That means the open problem is not just:

- too much boundary influence
- or too much final halo weight

It is more structural:

- the current constrained static branch is producing different interior source-build-up histories as `half_width` changes

So the next useful moves are the ones that can change branch selection or support definition, not just post-process the same curves:

- test alternative closure conditions or constraints
- test support windows tied to breather geometry rather than fixed radius alone
- examine whether the constrained branch is selecting a large-box halo family rather than a compact proton family

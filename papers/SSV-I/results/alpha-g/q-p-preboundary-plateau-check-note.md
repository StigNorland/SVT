# `Q_p(<r)` Pre-Boundary Plateau Check

This note records the direct check of whether the cumulative source

\[
Q_p(<r)
\]

settles before the boundary blend region begins.

Artifact:

- `papers/SSV-I/data/q-p-preboundary-plateau-check-2026-05-17.json`

Inputs:

- `half_width = 6`, `n = 48`, projected-residual plateau state
- `half_width = 7`, `n = 48`, constrained plateau state
- `half_width = 8`, `n = 64`, constrained plateau state

The current boundary treatment blends back to the background starting at

\[
r_{\rm blend} = (1 - f_{\rm blend}) \sqrt{3}\,\text{half\_width},
\]

with `f_blend = 0.18`.

So the tested blend-start radii are:

- `half_width = 6`: `r_blend ~ 8.52`
- `half_width = 7`: `r_blend ~ 9.94`
- `half_width = 8`: `r_blend ~ 11.36`

The check asks whether `Q_p(<r)` is already flat by `r_blend`, using:

- post-blend remainder fraction threshold `0.02`
- pre-blend tail relative-span threshold `0.01`

## Main Result

All three tested states satisfy the pre-boundary plateau criterion.

`half_width = 6`:

- pre-blend `Q_p^eff ~ 89.92`
- total `Q_p^eff ~ 90.06`
- post-blend remainder fraction `~ 0.00153`
- pre-blend tail relative span `~ 0.00745`

`half_width = 7`:

- pre-blend `Q_p^eff ~ 60.64`
- total `Q_p^eff ~ 60.74`
- post-blend remainder fraction `~ 0.00164`
- pre-blend tail relative span `~ 0.00714`

`half_width = 8`:

- pre-blend `Q_p^eff ~ 243.77`
- total `Q_p^eff ~ 244.24`
- post-blend remainder fraction `~ 0.00192`
- pre-blend tail relative span `~ 0.00853`

So the cumulative source is already essentially settled before the recovery layer begins in all three cases.

## Interpretation

This is an important control result.

The earlier box-size and halo probes showed:

- the integrated source changes dramatically across `half_width = 6, 7, 8`
- the `half_width = 8` state is strongly halo-dominated

This new check shows that those effects are **not** mainly being generated inside the boundary blend layer itself.

In other words:

- the recovery layer is present
- but the large `half_width = 8` source is already built in the interior before the blend starts

So the edge treatment is not the simplest explanation for the source jump.

## Consequence

The current open problem is sharper now.

It is not just:

- "does the boundary layer contaminate the source?"

It is:

- why does the interior halo reorganize so strongly with box size even before the boundary recovery layer starts?

That means the next useful probes should stay focused on the interior halo itself:

- compare `Q_p(<r)` curves directly across `half_width = 6, 7, 8`
- test alternative proton-support windows or closure conditions
- examine whether the constrained branch is selecting a large-box halo family rather than a compact source family

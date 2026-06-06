# `Q_p` Source Mechanism Probe Note

This note records the first focused mechanism probe on the plateaued `half_width = 6, 7, 8` static trefoil states.

Artifact:

- `papers/SSV-I/data/q-p-source-mechanism-probe-2026-05-17.json`

Inputs:

- `half_width = 6`, `n = 48`, projected-residual plateau state
- `half_width = 7`, `n = 48`, constrained plateau state
- `half_width = 8`, `n = 64`, constrained plateau state

The probe computes three families of diagnostics from saved `.npz` states:

- cumulative radial build-up of `delta V_p`, `\int (1-\rho)^2 d^3x`, and the direct static potential at a probe point
- explicit core / mid / halo source splits
- window-sensitive static-potential coefficients

The first run used:

- probe radius `r_* = 12`
- region edges `2, 5`
- smooth-window width `0.5`

## Main Result

The large `half_width = 8` source is overwhelmingly a halo effect.

At `half_width = 6`:

- core deficit fraction: about `3.5%`
- mid-region deficit fraction: about `47.5%`
- halo deficit fraction: about `49.0%`

At `half_width = 7`:

- core deficit fraction: about `2.8%`
- mid-region deficit fraction: about `31.3%`
- halo deficit fraction: about `65.9%`

At `half_width = 8`:

- core deficit fraction: about `2.2%`
- mid-region deficit fraction: about `21.4%`
- halo deficit fraction: about `76.5%`

The potential fractions tell the same story:

- `half_width = 6`: halo contributes about `48.7%`
- `half_width = 7`: halo contributes about `65.4%`
- `half_width = 8`: halo contributes about `75.9%`

So the source growth is not coming from the proton core reorganizing dramatically. It is coming from an increasingly dominant extended halo.

## Window Sensitivity

The window probes make the same point in a different way.

`half_width = 8`:

- full-domain `Q_p^eff`: about `244.24`
- hard `r < 5` window: about `58.79`
- halo-only `r > 5` window: about `185.45`

That means most of the `half_width = 8` source sits outside the `r = 5` region.

For comparison:

`half_width = 7`:

- full-domain `Q_p^eff`: about `60.74`
- hard `r < 5` window: about `20.99`
- halo-only `r > 5` window: about `39.75`

`half_width = 6`:

- full-domain `Q_p^eff`: about `90.06`
- hard `r < 5` window: about `46.21`
- halo-only `r > 5` window: about `43.84`

So the branch evolves from roughly balanced mid-plus-halo support at `half_width = 6` to strongly halo-dominated support by `half_width = 8`.

## Interpretation

This narrows the mechanism question a lot.

The `half_width = 8` jump is not primarily a core effect. It is a large-box halo effect. That means the most relevant follow-up questions are now:

- is that halo physically part of the proton-support source functional?
- should the proton window `W_p` cut it off more aggressively?
- or is the current constrained static branch missing a closure condition that would prevent the halo from carrying most of the integrated source?

So the next probe should stay focused on the halo:

- vary the core / mid / halo edges
- vary the support window definition
- compare cumulative potential build-up curves directly across `half_width = 6, 7, 8`

That is a much sharper target than adding another reduced `Q_p` ansatz.

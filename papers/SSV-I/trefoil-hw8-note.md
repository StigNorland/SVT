# `half_width = 8` Fine-Grid Check

This note records the first constrained `n = 48`, `half_width = 8` static trefoil run and its continuation.

Artifacts:

- `papers/SSV-I/data/trefoil-state-n48-hw8-400steps-2026-05-17.json`
- `papers/SSV-I/data/trefoil-state-n48-hw8-400steps-2026-05-17.npz`
- `papers/SSV-I/data/q-p-static-potential-hw8-400steps-2026-05-17.json`
- `papers/SSV-I/data/trefoil-hw8-projected-residual-2026-05-17.json`

## Why This Was Run

After the constrained-flow and projected-residual fixes, the fine-grid branch had:

- `half_width = 5`: clearly too small
- `half_width = 6`: usable constrained-flow reference state
- `half_width = 7`: usable constrained-flow reference state

The purpose of `half_width = 8` was to test whether `7` already sat in a stable large-box regime or whether the static source still shifts materially when the box is enlarged again.

## Initial `400`-Step State

The first constrained `400`-step state already looked qualitatively different from `half_width = 7`:

- residual norm: `0.0641`
- projected residual norm: `0.0242`
- shell density: `0.9149`
- `delta V_p`: `248.61`
- `Q_p^eff`: `245.97`

So `half_width = 8` is not a mild perturbation of the `6/7` source values. It carries a much larger integrated deficit.

## Plateau Continuation

The projected-residual continuation run reached plateau at `700` total steps:

- `delta V_p`: `248.585 -> 248.559 -> 248.533`
- `Q_p^eff`: `246.018 -> 246.036 -> 246.033`
- projected residual: `0.0170 -> 0.0120 -> 0.00855`
- shell density: `0.914259 -> 0.914077 -> 0.914018`

The plateau criterion is satisfied cleanly:

- source changes are tiny
- shell-density changes are tiny
- projected residual is comfortably below `0.05`

## Interpretation

This is an important result because it falsifies the idea that `half_width = 7` was already safely in the asymptotic large-box regime.

If `7` and `8` were already in the same domain-adequate regime, the static source should not have jumped from roughly

- `delta V_p ~ 61.5`
- `Q_p^eff ~ 61.1`

to roughly

- `delta V_p ~ 248.5`
- `Q_p^eff ~ 246.0`

That is far too large a change to treat as a small boundary correction.

So the current read is:

- `half_width = 8` is numerically well-behaved under the constrained flow
- but it reveals that the earlier `half_width = 6, 7` reference set was not yet in a box-size-stable regime for the integrated proton source
- the domain story is therefore not “`5` bad, `6/7` good”
- it is “`5` too small, `6/7` locally consistent under the constrained flow, but `8` shows the integrated source is still box-sensitive”

## Consequence

The repo should treat this as a serious box-size warning for the gravity branch.

The next comparison should not be another fit. It should be a direct box-size trend note across constrained fine-grid states:

- `half_width = 6`
- `half_width = 7`
- `half_width = 8`

using:

- `delta V_p`
- `Q_p^eff`
- shell density
- projected residual

That will tell us whether `8` is the start of a new stable regime or whether the integrated source is still growing with box size.

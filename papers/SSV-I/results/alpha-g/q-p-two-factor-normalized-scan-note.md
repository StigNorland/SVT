# Normalized Two-Factor `Q_p` Scan Note

This note records the first branch-normalized scan of the additive saturating reduced `Q_p` family.

Artifact:

- `papers/SSV-I/data/q-p-two-factor-normalized-scan-2026-05-06.json`

The normalization used here is intentionally modest: the compactness-style correction is scaled by the branch mean shell deficit, and the free parameter is a dimensionless `\eta`.

## Main Result

This normalization does improve over shell deficit alone, but it does **not** outperform the simpler unnormalized additive saturating family.

Best tested normalized values:

- `n = 24`: relative span `0.726`
- `n = 48`: relative span `0.537`

For comparison:

- shell deficit alone:
  - `n = 24`: `0.860`
  - `n = 48`: `0.785`
- bare additive saturating family at the best tested edge:
  - `n = 24`: `0.466`
  - `n = 48`: `0.402`

So the normalized family is a real improvement over the one-factor baseline, but still weaker than the simpler bare additive correction.

## Interpretation

This is a useful negative result.

It suggests that premature normalization against the branch mean shell deficit is not the right move yet. In practice, it flattens the correction less effectively than the direct additive family.

At the current stage, the repo should therefore treat the normalized scan as a side branch that clarified what **not** to prioritize next.

## Current Read

The better numerical lead remains:

- shell deficit
- plus a bare saturating compactness-style correction

The next sensible step is to widen the bare additive scan further rather than spending more time refining this normalization.

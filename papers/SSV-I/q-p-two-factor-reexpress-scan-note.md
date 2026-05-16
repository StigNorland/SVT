# Re-Expressed Two-Factor `Q_p` Scan Note

This note records the first attempt to re-express the additive saturating reduced `Q_p` family with geometry-tied branch scales rather than a bare correction coefficient.

Artifact:

- `papers/SSV-I/data/q-p-two-factor-reexpress-scan-2026-05-07.json`

The tested family keeps the same additive saturating shape,

\[
\Pi_Q^{\rm re}(\eta)
  = \Pi_{\rm shell}
  + \eta \, S_{\rm branch}
    \frac{r_{\rm eq}}{r_{\rm eff} + r_{\rm eq}},
\]

but replaces the old bare coefficient `\varepsilon` with a branch-derived scale `S_{\rm branch}`. Three simple choices were tested:

- mean shell-deficit-to-saturating ratio
- median shell-deficit-to-saturating ratio
- ratio of branch means

with

\[
\eta \in \{0.25,\,0.5,\,1.0,\,1.5,\,2.0,\,3.0\}.
\]

## Main Result

This re-expression helps relative to shell deficit alone, but it still does **not** outperform the simpler bare additive saturating family.

Best tested values in the re-expressed scan:

- `n = 24`
  - best mean-ratio scale: `0.604`
  - best median-ratio scale: `0.626`
  - best ratio-of-means scale: `0.592`
- `n = 48`
  - best mean-ratio scale: `0.473`
  - best median-ratio scale: `0.492`
  - best ratio-of-means scale: `0.466`

For comparison:

- shell deficit alone
  - `n = 24`: `0.860`
  - `n = 48`: `0.785`
- best bare additive saturating scan so far
  - `n = 24`: `0.456`
  - `n = 48`: `0.313`

So the re-expressed family is a genuine improvement over the one-factor baseline, but still weaker than the simpler additive saturating ansatz with a bare coefficient.

## Interpretation

This is another useful negative result.

It says the current geometry-derived branch scales are not yet capturing the right physical weighting for the compactness correction. They reduce some of the arbitrariness of the naked coefficient, but they also give up too much of the numerical flattening that made the bare additive family attractive in the first place.

## Current Read

The repo should treat this branch as clarifying rather than closing:

- the additive saturating functional shape still looks like the best reduced numerical lead
- the first branch-scale re-expression is not yet good enough to replace the bare parameterization
- any next re-expression should probably use a more local geometric scale than the coarse branch-wide ratios tested here

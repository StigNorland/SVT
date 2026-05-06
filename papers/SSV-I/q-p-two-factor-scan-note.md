# Additive Saturating `Q_p` Scan Note

This note records the first coefficient scan of the additive saturating reduced `Q_p` probe.

Artifact:

- `papers/SSV-I/data/q-p-two-factor-scan-2026-05-06.json`

The scanned family is

\[
\Pi_Q^{\rm sat}(\varepsilon)
  = \Pi_{\rm shell}
  + \varepsilon \,
    \frac{r_{\rm eq}}{r_{\rm eff} + r_{\rm eq}},
\]

with the first exploratory coefficient set

\[
\varepsilon \in \{0.02,\,0.05,\,0.1,\,0.15,\,0.2\}.
\]

## Main Result

The improvement over shell deficit alone is not a one-point accident.

As `\varepsilon` increases across the scanned range, the branch-wise relative span drops monotonically on both branches:

### `n = 24`

- `0.02`: `0.688`
- `0.05`: `0.598`
- `0.10`: `0.542`
- `0.15`: `0.517`
- `0.20`: `0.504`

### `n = 48`

- `0.02`: `0.751`
- `0.05`: `0.708`
- `0.10`: `0.652`
- `0.15`: `0.610`
- `0.20`: `0.577`

For comparison, shell deficit alone gave:

- `n = 24`: `0.860`
- `n = 48`: `0.785`

So the additive saturating family is currently the strongest reduced ansatz family in the repo.

## What This Means

Two things are now true at once:

1. the additive saturating correction is genuinely improving branch-wise stability
2. the currently best tested value sits at the upper edge of the scan range

That means the family has passed a useful first filter, but the coefficient itself is still unresolved.

## Current Read

The repo can now support the following statement:

- the best current reduced `Q_p` probe is not multiplicative
- it is a shell-deficit quantity plus a compactness-style saturating correction
- the correction strength should be treated as an open parameter, not yet a physical constant

The next step is therefore obvious: widen the coefficient scan beyond `0.2` before treating this family as more than a promising numerical lead.

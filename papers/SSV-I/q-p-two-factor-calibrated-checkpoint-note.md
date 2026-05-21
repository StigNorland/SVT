# Calibrated Two-Factor `Q_p` Checkpoint Note

This note records the first checkpoint artifact for the provisionally calibrated additive saturating reduced `Q_p` ansatz.

Artifacts:

- `papers/SSV-I/data/q-p-two-factor-calibrated-checkpoint-2026-05-07.json`
- `papers/SSV-I/data/q-p-two-factor-eta-shape-calibration-2026-05-07.json`

The checkpoint uses the current shape-consistency calibration

\[
\eta = 0.5
\]

in the reduced family

\[
\Pi_Q^{\rm calib}
  = \Pi_{\rm shell}
  + 0.5 \,
    \frac{r_{\rm eq}}{r_{\rm eff} + r_{\rm eq}}.
\]

## Current Calibrated Values

### `n = 24`

- `half_width = 5`: `0.1336`
- `half_width = 6`: `0.0922`
- `half_width = 7`: `0.0700`

### `n = 48`

- `half_width = 5`: `0.3632`
- `half_width = 6`: `0.2611`
- `half_width = 7`: `0.1931`

## Branch-Wise Spread

Relative spans for the calibrated quantity are:

- `n = 24`: `0.476`
- `n = 48`: `0.468`

For comparison, shell deficit alone gave:

- `n = 24`: `0.860`
- `n = 48`: `0.785`

So the calibrated reduced ansatz keeps the same strong stability gain that originally made the additive saturating family worth pursuing.

## Cross-Branch Shape Check

At matched half-width, the normalized branch values are:

- `half_width = 5`
  - `n = 24`: `1.355`
  - `n = 48`: `1.333`
- `half_width = 6`
  - `n = 24`: `0.935`
  - `n = 48`: `0.958`
- `half_width = 7`
  - `n = 24`: `0.710`
  - `n = 48`: `0.709`

The largest normalized shape error in this checkpoint is only about `0.024`, and the smallest is about `0.0016`.

## Current Read

This is the cleanest single reduced `Q_p` checkpoint in the repo so far.

It should still be treated as provisional, but it is now reasonable to refer to

- the additive saturating family as the current reduced ansatz lead
- `\eta = 0.5` as its current shape-calibrated working value

while keeping the absolute monopole normalization explicitly unresolved.

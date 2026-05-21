# Additive Saturating `Q_p` Eta Calibration Note

This note records the first explicit calibration passes for the additive saturating reduced `Q_p` family.

Artifacts:

- `papers/SSV-I/data/q-p-two-factor-eta-calibration-2026-05-07.json`
- `papers/SSV-I/data/q-p-two-factor-eta-shape-calibration-2026-05-07.json`

The calibrated family is

\[
\Pi_Q(\eta)
  = \Pi_{\rm shell}
  + \eta \,
    \frac{r_{\rm eq}}{r_{\rm eff} + r_{\rm eq}}.
\]

## Calibration Passes

Two provisional consistency criteria were tested.

### 1. Absolute coarse-fine consistency

The first pass compared the coarse `n = 24` and fine `n = 48` branches directly at matched `half_width = 5, 6, 7`, using

\[
\text{score}
  = \text{mean relative mismatch}
  + \frac{1}{2}
    \left(
      \text{coarse relative span}
      + \text{fine relative span}
    \right).
\]

This criterion was not very informative. It keeps improving toward the upper scan boundary, with the best tested value at `\eta = 10.0`.

That is a warning sign rather than a satisfying calibration: the objective is still too sensitive to absolute amplitude differences between the two branches.

### 2. Normalized shape consistency

The second pass first normalizes each branch by its own mean over the matched half-width set, then compares the resulting three-point shapes.

This gives a real interior optimum:

- best by mean absolute shape error: `\eta = 0.5`
- best by mean squared shape error: `\eta = 0.5`

At `\eta = 0.5`, the normalized branch values are:

- `n = 24`: `1.355`, `0.935`, `0.710`
- `n = 48`: `1.333`, `0.958`, `0.709`

with mean absolute shape error about `0.0158`.

## Main Read

The first genuinely useful provisional calibration in the repo is therefore:

\[
\eta_{\rm shape} \approx 0.5.
\]

This should not be treated as a physical constant yet. It is only the first value that makes the coarse and fine branches show nearly the same normalized half-width dependence.

## Interpretation

This is a good checkpoint for the gravity branch because it separates two different questions:

- absolute amplitude agreement is still unresolved
- normalized geometric-shape agreement already points to a plausible interior `\eta`

That means the additive saturating family is now calibrated enough to be used as a provisional reduced ansatz, while still keeping its physical normalization explicitly open.

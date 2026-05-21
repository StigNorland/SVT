# Local Additive Two-Factor `Q_p` Scan Note

This note records the first scan of local geometric terms that enter additively without being multiplied back by the shell deficit.

Artifact:

- `papers/SSV-I/data/q-p-two-factor-local-additive-scan-2026-05-07.json`

The tested family was

\[
\Pi_Q^{\rm local+}(\eta)
  = \Pi_{\rm shell}
  + \eta \, G_{\rm local},
\]

with four local geometric choices:

- saturating compactness `r_{\rm eq} / (r_{\rm eff} + r_{\rm eq})`
- compactness `r_{\rm eq} / r_{\rm eff}`
- deficit-volume fraction `V_{\rm def} / (r_{\rm eff}^3 + V_{\rm def})`
- a mixed local average of the saturating and volume-fraction terms

## Main Result

This is the first local re-expression family that actually works numerically.

Among the tested local additive terms, the best performer is again the saturating compactness term. Its best tested branch-wise spreads are:

- `n = 24`: `0.457`
- `n = 48`: `0.325`

For comparison:

- shell deficit alone
  - `n = 24`: `0.860`
  - `n = 48`: `0.785`
- best bare additive saturating family so far
  - `n = 24`: `0.456`
  - `n = 48`: `0.313`

So the local additive saturating form is not quite better than the bare additive family, but it comes very close and is much better than the earlier branch-scale and shell-weighted local re-expressions.

## Interpretation

This is the strongest re-expression attempt so far.

It suggests that two features mattered at once:

- the useful correction really does want the saturating compactness shape
- multiplying that correction back through shell deficit was the wrong move

That is encouraging because it means the local geometry is not the problem by itself. The problem was how the local term was parameterized.

## Current Read

The repo can now support a sharper statement:

- the bare additive saturating family remains the current best reduced numerical lead
- the local additive saturating family is now the best re-expressed alternative
- the gap between them is small enough that future work should focus on improving the local additive parameterization rather than revisiting branch-wide or shell-weighted forms

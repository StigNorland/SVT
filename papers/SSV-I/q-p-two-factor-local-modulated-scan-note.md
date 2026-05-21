# Local Modulated Two-Factor `Q_p` Scan Note

This note records the first scan of locally modulated additive saturating `Q_p` probes.

Artifact:

- `papers/SSV-I/data/q-p-two-factor-local-modulated-scan-2026-05-07.json`

The goal was to keep the best local re-expression found so far,

\[
\Pi_Q^{\rm local+} = \Pi_{\rm shell} + \eta \, S_{\rm sat},
\]

but replace the naked strength by a second local geometric modulation. The tested families were:

\[
\Pi_Q^{\rm mod}(\eta)
  = \Pi_{\rm shell}
  + \eta \, S_{\rm sat} \, H_{\rm local},
\]

with `H_local` taken to be:

- local compactness `r_{\rm eq} / r_{\rm eff}`
- local deficit-volume fraction `V_{\rm def} / (r_{\rm eff}^3 + V_{\rm def})`
- a mixed local average
- a square-root mixed scale

## Main Result

This does **not** help.

All of these modulated variants perform worse than the simpler local additive saturating family, and they are also much weaker than the bare additive saturating family.

Best tested modulated values:

- `n = 24`
  - best modulated candidate: `0.745`
- `n = 48`
  - best modulated candidate: `0.625`

For comparison:

- shell deficit alone
  - `n = 24`: `0.860`
  - `n = 48`: `0.785`
- best local additive saturating family
  - `n = 24`: `0.457`
  - `n = 48`: `0.325`
- best bare additive saturating family
  - `n = 24`: `0.456`
  - `n = 48`: `0.313`

So the extra local modulation is clearly over-structuring the correction rather than improving it.

## Interpretation

This is another useful narrowing result.

The numerically helpful ingredient still appears to be the simple local saturating compactness shape itself. Once the correction strength is multiplied by an additional local factor, the flattening degrades sharply.

That suggests the remaining problem is not "missing a second local factor." It is more likely that the additive strength needs a better single-scale interpretation rather than more multiplicative structure.

## Current Read

The reduced `Q_p` search now has a clearer hierarchy:

- best overall lead: bare additive saturating family
- best re-expressed lead: local additive saturating family
- not promising:
  - branch-scale re-expressions
  - shell-weighted local re-expressions
  - locally modulated additive saturating re-expressions

The next sensible move is to focus on calibrating or interpreting the single local additive saturating strength, not adding more geometric factors on top of it.

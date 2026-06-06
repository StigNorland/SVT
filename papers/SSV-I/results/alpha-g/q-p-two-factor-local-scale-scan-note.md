# Local-Scale Two-Factor `Q_p` Scan Note

This note records the first run-local geometry re-expression scan for the reduced `Q_p` family.

Artifact:

- `papers/SSV-I/data/q-p-two-factor-local-scale-scan-2026-05-07.json`

The goal here was to move past branch-wide ratio scales and test whether a more local geometric weighting could preserve the attractive additive saturating shape without relying on a naked branch coefficient.

The tested families were all shell-weighted additive corrections:

\[
\Pi_Q^{\rm local}(\eta)
  = \Pi_{\rm shell}
  + \eta \, \Pi_{\rm shell} \, G_{\rm local},
\]

where `G_local` was taken in turn to be:

- the local saturating compactness `r_eq / (r_eff + r_eq)`
- the local compactness `r_eq / r_eff`
- a local deficit-volume fraction `V_def / (r_eff^3 + V_def)`
- a mixed local average of the saturating and volume-fraction terms

## Main Result

This family does **not** improve over shell deficit alone.

Best tested branch-wise values all occur at the smallest scanned coefficient, `\eta = 0.1`, and even there they are slightly worse than the shell-deficit baseline.

Best local-scale values:

- `n = 24`
  - shell deficit baseline: `0.860`
  - best local-scale candidate: `0.861`
- `n = 48`
  - shell deficit baseline: `0.785`
  - best local-scale candidate: `0.788`

So the local shell-weighted corrections are not just weaker than the bare additive saturating family; they are effectively no better than doing nothing.

## Interpretation

This is a useful narrowing result.

It suggests that multiplying the correction back through the local shell deficit removes most of the flattening effect that made the bare additive saturating family numerically interesting in the first place.

In other words:

- branch-wide ratio scales were too coarse
- these first shell-weighted local scales are too self-canceling

Neither is yet the right re-expression.

## Current Read

The repo should now treat the reduced `Q_p` search as follows:

- the bare additive saturating family is still the best reduced numerical lead
- branch-scale re-expressions improved over shell deficit, but not enough
- shell-weighted local re-expressions do not help at all

The next promising direction is likely a local geometric scale that enters additively without being multiplied back by the shell deficit itself.

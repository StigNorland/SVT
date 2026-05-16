# Pure Additive Local-Scale `Q_p` Scan Note

This note records the scan of purely additive local-geometry `Q_p` probes, with no `Pi_shell` multiplier on the correction term.

Artifact:

- `papers/SSV-I/data/q-p-two-factor-pure-additive-local-scan-2026-05-16.json`

The tested family is

\[
\Pi_Q^{\rm local}(\eta)
  = \Pi_{\rm shell}
  + \eta \, G_{\rm local},
\]

where `G_local` was taken in turn to be:

- the local saturating compactness `r_eq / (r_eff + r_eq)`
- the local compactness `r_eq / r_eff`
- a local deficit-volume fraction `V_def / (r_eff^3 + V_def)`
- a mixed local average of the saturating and volume-fraction terms

with

\[
\eta \in \{0.1,\,0.25,\,0.5,\,1.0,\,1.5,\,2.0,\,3.0,\,4.0,\,5.0,\,7.5,\,10.0\}.
\]

## Cross-Check

The saturating variant is identical to the bare additive extended scan at the same coefficient values.
The best-by-n results reproduce the known values exactly:

- `n = 24`: `0.456` at `eta = 10.0`
- `n = 48`: `0.313` at `eta = 10.0`

The cross-check passes. Results from the two scripts are consistent.

## Main Result

No new local geometric scale outperforms the bare additive saturating family.

Best tested values at optimal `eta`:

| Variant | `n = 24` (best `eta`) | `n = 48` (best `eta`) |
|---|---|---|
| saturating | `0.456` (η=10) | `0.313` (η=10) |
| compactness | `0.529` (η=10) | `0.455` (η=10) |
| mixed | `0.607` (η=10) | `0.461` (η=10) |
| volume fraction | `0.873` (η=0.1) | `0.554` (η=10) |

For reference, shell deficit alone gave `0.860` (n=24) and `0.785` (n=48).

The saturating variant remains the best by a clear margin on both branches.

## Volume Fraction Anomaly

The volume fraction variant behaves anomalously on the coarse branch.

On `n = 24`, its best value (`0.873` at `eta = 0.1`) is worse than shell deficit alone and gets worse monotonically as `eta` increases. On `n = 48` it eventually matches the other non-saturating variants at large `eta` (`0.554`), but it is always the weakest performer.

This suggests the deficit volume `V_def` is picking up a geometrically inconsistent quantity between the two branches at small correction strength. It is not a useful additive correction at either scale.

## What This Settles

The local additive scan programme is now complete. The full sequence tested:

1. **Probe** — additive saturating beats multiplicative and bare compactness
2. **Scan / Extended** — saturating improves monotonically to `eta = 10`, no turnover
3. **Normalized** — branch-mean normalization does not outperform bare additive
4. **Re-expressed** — branch-wide ratio scales do not outperform bare additive
5. **Shell-weighted local** — multiplying correction through `Pi_shell` is self-canceling
6. **Pure additive local** — removing the shell weight does not produce a new winner

In all cases, the bare additive saturating family is the best reduced form found. No re-expression, normalization, or alternative local scale improves on it.

## Interpretation

The two-factor reduced `Q_p` programme has converged to a dead end as a scan problem.

The additive saturating functional shape is clearly favored. But the coefficient `eta` (or `epsilon`) cannot be fixed from the scan: the best numerical behavior always sits at the upper edge of the tested range with no turnover. This means the scan cannot locate a natural coefficient — it can only push the problem to larger and larger values of a parameter that has no geometric anchor yet.

The path forward is not another scan variant. The coefficient will only become natural once the underlying geometry is fixed, which requires the static 3D breather minimisation (Workstream 2 in `docs/numerical-minimisation-roadmap.md`). Once the relaxed breather geometry is converged, the relevant compactness scales can be read off directly rather than scanned over.

## Current Read

The repo should now treat the `Q_p` two-factor scan programme as closed:

- the additive saturating family `Pi_shell + eta * r_eq / (r_eff + r_eq)` is the best reduced numerical form found
- no scan over local or branch-level geometric scales resolves the coefficient
- further scanning is not the right next step
- the coefficient will only become geometrically grounded after the static breather closes

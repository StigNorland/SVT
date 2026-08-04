# Issue #230 — frozen exploratory protocol

Frozen on 2026-08-04 after reading the issue and primary-source metadata, but
before implementing or running the issue-230 instrument.

## Evidential boundary

This is a retrospective source-discovery audit. The six gas-rich UDG result,
the resolved AGC 114905 result, DDO154, and the issue-225 cored-log outcome were
already known. No row in this audit is held-out confirmation. Leave-one-out
scores are internal predictive diagnostics only.

The words *shared screen* mean a provisional correlated or collective effective
state. They do not mean quantum entanglement. Issue #227 did not derive a
hierarchical composition law, a universal amplitude, or a unique radial kernel.

## Frozen questions and ordered gates

1. **Gate A:** Can the homogeneous UDG and SPARC sources supply comparable
   radial velocities, uncertainties, baryonic components, geometry, and drift
   corrections?
2. **Gate B:** If Gate A passes, can a dimensionally valid, independently
   observed internal-update proxy predict excluded-galaxy response with fewer
   degrees of freedom than galaxy-specific amplitudes?
3. **Gate C:** Only if Gate B is inadequate and true host membership metadata
   exist, can a group-level/shared-state model be fitted.

Failure of a gate is a result. Later gates will not be made to pass by
digitizing an attractive plot, treating correlated rings as independent, or
using the discrepancy itself as a predictor.

## Frozen samples

### Homogeneous gas-rich UDG discovery sample

Use the six objects and the summary quantities printed in Mancera Piña et al.
(2020): AGC 114905, 122966, 219533, 248945, 334315, and 749290. Preserve their
published distances, disc scale lengths, stellar and H I masses, inclinations,
circular-speed intervals, gas dispersions, and outer radii. The primary summary
diagnostic excludes AGC 749290 because its two rings were obtained by a factor
1.7 oversampling and were declared less robust; an all-six sensitivity retains
it.

The higher-resolution AGC 114905 work is a separate inventory row. Its five
nearly independent rings validate that the flat part is reached, but the paper
does not publish a machine-readable numeric radial table; the authors state
that generated/analyzed data are available on request. The present audit will
not silently substitute plot-digitized points for author data.

### SPARC controls

Construct candidates without using fitted screen amplitude or mass discrepancy:

- morphology `T >= 8`;
- rotation-curve quality `Q <= 2`;
- inclination `i >= 30 deg`;
- a reported positive `Vflat`;
- at least eight radial mass-model rows; and
- baryonic mass within 0.25 dex of the full six-UDG baryonic-mass range.

Use `Mbar = 0.5 L[3.6] + 1.33 MHI` in units of solar mass and
`fgas = 1.33 MHI/Mbar`. For each robust UDG, select the two lowest-distance
controls in the fixed observational feature space

```text
[(log10 Mbar)/0.30, (log10 Rdisk)/0.30, fgas/0.20]
```

with deterministic galaxy-name tie breaking. Reuse is allowed because this is
nearest-neighbour coverage, not a randomized case-control study. Include
DDO154 as the named anchor even if it is not selected algorithmically. Do not
use `Vflat` in the matching distance.

## Frozen observables and proxies

The response summary is the dimensionless outer dynamical-to-baryonic mass
ratio

```text
Dout = Vcirc^2 Rout / (G Mbar).
```

It is an outcome, never a matching variable or predictor. It is only a summary
diagnostic: disc geometry means it is not a radial mass decomposition.

The small internal proxy set is

```text
Gamma_dyn = sqrt(G Mbar / Rdisk^3)       [inverse time]
Gamma_gas = fgas Gamma_dyn               [inverse time]
Sigma_bar = Mbar / (2 pi Rdisk^2)        [mass / area].
```

All use baryonic photometry/gas measurements independent of the observed
rotation amplitude. Gas turbulence and SFR surface density are inventory-only:
the UDG dispersions include upper limits and homogeneous SPARC counterparts are
absent; individual homogeneous SFRs are not printed in the source table.

## Frozen diagnostics and model rules

For the summary sample compare weighted linear models for `log10(Dout)`:

- intercept only;
- `log10(Gamma_dyn)`;
- `log10(Gamma_gas)`; and
- `log10(Gamma_dyn) + fgas`.

Report AICc/BIC only when valid, deterministic leave-one-galaxy-out predictions,
coefficient covariance/rank, and robust-five versus all-six sensitivity. A proxy
earns exploratory internal-update support only if it lowers leave-one-out RMSE
by at least 10% relative to the intercept, is full rank with finite covariance,
and the improvement survives both AGC 749290 exclusion and UDG/SPARC class-holdout
extrapolation. Because all samples were viewed, even a pass is discovery, not
confirmation.

Radial fits, where eligible, use the same SPARC velocity residual likelihood,
fixed stellar mass-to-light ratios `(0.5, 0.7)`, and the candidate list:
baryons, NFW, genuine pISO, cored-log, and the issue-225 retained LogSVT
reductions `k2`, `k2_Q`, `k2_L`, `C_L`, and `k2_L_Q`. Light `(0.3, 0.5)` and
heavy `(0.7, 0.9)` baryons are sensitivities. AICc, BIC, covariance rank,
correlations, parameter boundaries, and optimizer status are mandatory.

These SPARC-only radial fits describe controls; they cannot establish a
cross-class kernel preference if the UDG radial input contract fails.

## Decision rules

- **Internal-update support:** all proxy requirements pass and the compared
  classes satisfy the same response-data contract.
- **Shared-screen support:** Gate C has true 3D membership/velocity metadata,
  a group latent predicts excluded members with fewer degrees of freedom, and
  conventional environment controls survive.
- **Unsupported:** the contrast requires outcome-defined predictors,
  per-galaxy amplitudes, incompatible data products, or non-identifiable fits.
- A flat curve or a fitted amplitude that approaches zero is never support.

DF2/DF4 remain outside this audit because they require a Jeans/tracer likelihood.


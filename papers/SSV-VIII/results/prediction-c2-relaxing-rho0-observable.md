# Prediction C2 closure note: relaxing rho_0 cosmology

**Issue:** #51  
**Date:** 2026-06-06  
**Status:** observational-discriminator route identified; numerical Lambda remains
underdetermined by the current SSV papers.

## Question

Prediction C2 in Paper VIII states that late-time acceleration should be read
as slow relaxation of the saturated background rho_0 rather than as an
independent dark-energy sector.  Issue #51 asked for either:

1. a numerical Lambda from the SSV equation of state, or
2. an observational programme that distinguishes LambdaCDM from a
   slowly-relaxing-rho_0 cosmology.

## Numerical Lambda route

The current theory does **not** yet determine a numerical Lambda.

Paper VII-b identifies the cosmological constant with the residual saturation
pressure,

```tex
\Lambda = {8\pi G \over c^2}\,{P_0 \over \rho_0 c^2}.
```

Paper I fixes the LogSE sound-speed slope around the saturated background:

```tex
c_s^2 = {2b\rho_0 \over m_0}, \qquad b={m_0 c^2\over 2\rho_0}.
```

But this fixes the derivative of the equation of state, not the absolute
pressure offset.  The local logarithmic EOS used in the LogSE sector,

```tex
P(\rho)=b\rho\ln(\rho/\bar\rho),
```

gives `P(rho_0)=0` when the linearisation point is chosen as
`rho_0=bar rho`.  The `P_0` that appears in VII-b is therefore an additional
background/saturation pressure offset, not currently computed from the local
LogSE slope.  A numerical Lambda would require one new theoretical input:

```tex
P_0(\rho_0) \quad\hbox{or equivalently}\quad
{P_0\over \rho_0 c^2}.
```

Without that input, computing the observed Lambda would insert a free
normalisation and would not close #51 by the numerical route.

## Minimal relaxing-rho_0 observable

The closure route available now is the observational discriminator.  Define

```tex
\Lambda_{\rm eff}(a)
  = \Lambda_0\,a^\beta,
\qquad
\beta \equiv {d\ln\Lambda_{\rm eff}\over d\ln a}.
```

where `a=1/(1+z)` and `beta=0` is exactly LambdaCDM.  In SSV language,

```tex
\beta
 =
 {d\ln(P_0/\rho_0 c^2)\over d\ln\rho_0}\,
 {d\ln\rho_0\over d\ln a}.
```

Thus C2 is not merely "some evolving dark energy"; it predicts that the dark
sector drift is a single coherent background-relaxation slope.  In the
constant-beta approximation it is equivalent to

```tex
w_{\rm eff} = -1 - {\beta\over 3}.
```

The Friedmann comparison model is

```tex
E^2(z;\beta)
 =
 \Omega_r(1+z)^4
 + \Omega_m(1+z)^3
 + \Omega_\Lambda(1+z)^{-\beta}.
```

## Distinguishing signatures

The observational programme is:

1. Fit the one-parameter C2 slope `beta` to CMB-anchored BAO + SN expansion
   data, with the same high-redshift calibration used for LambdaCDM.
2. Require the same `beta` to describe all three residuals:
   `H(z)`, transverse BAO distance `D_M(z)`, and SN luminosity-distance
   residuals.
3. Interpret any future SSV derivation of `P_0(rho_0)` as a prediction for
   both the **amplitude** and **sign** of `beta`, rather than as a new fit.

For small `|beta|`, the correlated sign pattern is:

| beta | past Lambda_eff | H(z) vs LambdaCDM | D_M(z), D_L(z) vs LambdaCDM | w_eff |
|---:|---|---|---|---:|
| `beta > 0` | smaller | lower | larger | `< -1` |
| `beta < 0` | larger | higher | smaller | `> -1` |

This is the C2 discriminator.  A generic `w0-wa` fit is too broad; the SSV
test is the one-slope relaxation track above.

## Reproducible helper

The helper script is:

```bash
PYTHONPATH=src python -m paper_viii.relaxing_rho0_cosmology \
  --output src/paper_viii/relaxing_rho0_cosmology_results.json
```

It uses a Planck-2018-like flat baseline
`H0=67.4 km/s/Mpc`, `Omega_m=0.315`, `Omega_r=9.2e-5`, and computes example
residuals for `beta = +/-0.1` at `z = 0.3, 0.8, 1.5, 2.5`.

## Observational anchors

This is intentionally framed in the same observable language as current
expansion-history tests:

- Planck 2018 provides the high-redshift LambdaCDM baseline
  (`H0=67.4 km/s/Mpc`, `Omega_m=0.315` in base LambdaCDM):
  <https://arxiv.org/abs/1807.06209>
- DESI DR2 BAO is the natural near-term low-redshift comparison frame for
  evolving-dark-energy tests:
  <https://www.desi.lbl.gov/2025/03/19/desi-dr2-results-march-19-guide/>
  and the associated cosmology-chain/data release:
  <https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/>

## Closure verdict

#51 is solved as far as the current theory allows:

- The numerical Lambda route is explicitly blocked by the missing absolute
  saturation pressure `P_0`.
- The observational route is now identified: fit or constrain the C2
  relaxation slope `beta = d ln Lambda_eff / d ln a`, and test its coherent
  residual pattern across `H(z)`, BAO `D_M(z)`, and SN `D_L(z)`.
- Prediction C2 should be upgraded from "structural with a future observable"
  to "structural with an identified falsifiable cosmological observable."

Promotion beyond that requires a future derivation of `P_0(rho_0)`, which
would turn `beta` from an observational discriminator into a numerical SSV
prediction.

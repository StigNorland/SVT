# Issue #228 — preregistered datasets and likelihoods

Status: **frozen registry; activation vetoed by the analytic C6 result**

## Likelihood registry

1. **Transient clock likelihood.** Use published SN spectral ages and observer
   intervals from Blondin et al. Fit one global exponent `b` in
   `aging_rate=(1+z)^(-b)` with the published uncertainties and object-level
   nuisance structure. The required common value is `b=1`; an energy-only law
   fixes `b=0` and fails.
2. **Supernova distance likelihood.** Use the Pantheon+ distance-modulus vector
   and full statistical-plus-systematic covariance. Marginalize the absolute
   magnitude/calibration parameter. Do not call redshift an independent
   distance.
3. **BAO ruler likelihood.** Use the DESI DR1 consensus vector and covariance
   for transverse/radial/isotropic measurements. Treat `r_d` as a calibrated
   nuisance unless the model supplies recombination and pre-drag dynamics.
4. **Distance-duality likelihood.** Construct
   `eta(z)=D_L/[D_A(1+z)^2]` only from matched, independently calibrated candle
   and ruler information. Propagate lensing, selection, and calibration
   covariance; the metric/photon-conserving target is `eta=1`.
5. **Surface-brightness likelihood.** Use the Lubin--Sandage size/surface-
   brightness relations with explicit band-dependent luminosity-evolution and
   K-correction nuisance parameters. Compare predicted exponents 1, 2, and 4
   for R1, R2, and metric R3 respectively.
6. **CMB spectral likelihood.** Use FIRAS frequencies, intensity residuals, and
   covariance/foreground model. A screen law must propagate a Planck spectrum
   without an unmodeled distortion.
7. **CMB-temperature likelihood.** Use absorber thermometry with collisional
   and radiative excitation nuisance parameters. Test
   `T(z)=T0(1+z)^(1-beta)` jointly with the same total redshift factor.
8. **Redshift-drift likelihood.** Use multi-epoch line centroids with
   instrument-epoch offsets and source peculiar-acceleration nuisances. Do not
   interpret current sensitivity as a detection of the standard signal.

## Joint model and identifiability

For a mixed model define

\[
H_{\rm eff}(t)=H_{\rm geom}(t)+\Gamma_{\rm wake}(t).
\]

The joint likelihood may open only if at least one registered observable has
different, derived response columns for `H_geom` and `Gamma_wake`. If every
electromagnetic prediction depends only on `H_eff`, the Fisher/design matrix
has rank one for two functions and the decomposition is not estimable. Priors
or smoothness penalties do not turn that structural degeneracy into evidence.

## Activation result

R0 fails C1. R1 fails C3. R2 fails reciprocity/surface brightness without a
spatial response. R3 supplies that response but makes all registered ideal
propagation observables functions of a single optical scale `S=BW`; its two
component columns are identical. Consequently no parameter likelihood was
executed. This is the preregistered stopping rule, not missing numerical work.

The post-preregistration R4 information-area hypothesis is also stopped before
a fit: it does not derive `N(t)`, cell area, or area-growth energy, while its
owner-specified pure deceleration has a direct sign conflict with the registered
late-time SN acceleration test under that test's stated assumptions.

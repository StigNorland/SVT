# Issue #228 — primary-literature and systematics map

Status: **complete; no cosmological fit performed**

| gate | primary anchor | observable | required nuisance/systematics treatment |
|---|---|---|---|
| C1/C3 time stretching | [Blondin et al. 2008](https://arxiv.org/abs/0804.3595) | SN Ia spectral age versus observer elapsed time | spectral-template age, phase coverage, object diversity, redshift uncertainty |
| C4 candles | [Pantheon+ cosmology](https://arxiv.org/abs/2202.04077) | standardized SN distance modulus with covariance | calibration, intrinsic scatter, selection, dust, peculiar velocities, absolute-magnitude degeneracy |
| C4/C5 rulers | [DESI 2024 VI](https://arxiv.org/abs/2404.03002) | `D_M/r_d`, `D_H/r_d`, or `D_V/r_d` across tracers | reconstruction, tracer bias, nonlinear damping, fiducial-coordinate mapping, sound-horizon calibration |
| C5 reciprocity | [Bassett & Kunz 2004](https://arxiv.org/abs/astro-ph/0312443) | `eta=D_L/[(1+z)^2D_A]` | photon conservation, unique rays, metric assumption, lensing/selection |
| C5 surface brightness | [Lubin & Sandage 2001](https://arxiv.org/abs/astro-ph/0106566) | Tolman exponent | luminosity/size evolution, K corrections, morphology and selection |
| C5 CMB spectrum | [Fixsen et al. 1996](https://arxiv.org/abs/astro-ph/9605054) | FIRAS monopole spectrum and residuals | Galactic foreground components, calibration, frequency covariance |
| C5 CMB temperature history | [Noterdaeme et al. 2010](https://arxiv.org/abs/1012.3164) | molecular excitation temperature through `z~3` | density, collisions, UV pumping, absorber environment |
| C5 redshift drift | [Darling 2012](https://arxiv.org/abs/1211.4585) and [Loeb 1998](https://arxiv.org/abs/astro-ph/9802122) | repeated-line `dz/dt_o` | frequency calibration, line-profile stability, peculiar acceleration, observer acceleration |
| C5 early universe | [Planck 2018 VI](https://arxiv.org/abs/1807.06209) | CMB anisotropy/lensing likelihoods | foregrounds, calibration, recombination and perturbation model |
| R4 expansion sign | [Seikel & Schwarz 2008](https://arxiv.org/abs/0810.4484) | calibration/dynamics-independent SN acceleration statistic | spatial flatness, statistical homogeneity/isotropy, low-redshift leverage |

## Interpretation boundary

These sources fix observables and likelihood structure; their standard-model
parameter estimates are not imported as screen predictions. BAO is an
independent ruler only after the model states how `r_d` is calibrated. Supernova
redshift is not its own distance. Molecular CMB thermometry is independent of
the distance-redshift conversion but not of local excitation modeling.

The strongest immediate discriminator is not one fitted cosmological number.
It is the joint identity of frequency and transient stretching. A stationary
energy-only loss has duration ratio one and fails before a cosmological fit.
An ideal coherent dilation has the correct duration but lacks the beam-area
factor required by reciprocity; adding that factor makes it an optical metric.

## Current redshift-drift status

Redshift drift is a direct derivative observable, but the cited current radio
constraints are roughly three orders of magnitude above the expected
cosmological signal. It is therefore a preregistered future discriminator, not
a claimed present detection or exclusion of a small wake fraction.

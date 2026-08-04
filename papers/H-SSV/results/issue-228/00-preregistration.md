# Issue #228 — invariant screen-redshift preregistration

Status: **frozen before issue-228 instruments and verdict**

## Question and evidential boundary

Can the C4 global quantum-causal screen produce a nonzero, invariant
cosmological-redshift contribution that is conserved, achromatic, non-blurring,
time-stretching, and independently distinguishable from geometric expansion?

This issue is separate from H-SSV-II. No galaxy-response result, fitted
acceleration scale, or issue-225/227 outcome may select its law. No measured
cosmological rate or density is an H-SSV prediction. Archived SSV cosmology
batteries remain out of scope.

## Frozen foundation

C4 supplies one global quantum state, local no-signaling causal gates, finite
state/update capacities, and a closed global energy-information ledger. It
does not supply a continuum metric, spatial scale factor, photon-screen
Hamiltonian, energy per write, cell area, cosmological update rate, or
background evolution equation.

The post-issue-227 C5 hierarchy of coherent effective screens is recorded but
does not itself select a universal cosmological propagation law.

## Invariant observables

For emitter and observer four-velocities `u_e` and `u_o` and photon wavevector
`k`, the measured endpoint ratio is

\[
1+z={-(u\cdot k)_e\over-(u\cdot k)_o}.
\]

A homogeneous lapse-only metric

\[
ds^2=-A(t)^2c^2dt^2+d\mathbf x^2
\]

is the negative control. With `d tau=A dt` it is Minkowski space, and
equivalent comoving endpoint clocks measure `z=0`.

## Frozen candidate ladder

### R0 — homogeneous lapse only

No spatial response and no photon interaction. Expected result: C1 failure by
coordinate removability.

### R1 — deterministic energy-only path loss

On a physical screen congruence, assume for comparison

\[
{d\ln\nu\over dD}=-\kappa,
\qquad 1+z=e^{\kappa D}.
\]

`kappa` is a phenomenological input, not derived. The fractional law is
achromatic and preserves the ray direction in its ideal limit, but a stationary
path maps successive emission intervals to equal arrival intervals. Expected:
energy redshift `1+z`, duration factor `1`, and failure of C3.

For a static Euclidean baseline with conserved photon number, R1 predicts
`D_L=D sqrt(1+z)`, `D_A=D`, bolometric surface brightness proportional to
`(1+z)^-1`, and therefore violates metric distance duality.

### R2 — coherent wavepacket dilation without spatial response

Let `y=1+z` and apply the normalized ideal channel

\[
\psi_o(t)=y^{-1/2}\psi_e(t/y).
\]

It maps `nu_o=nu_e/y`, `Delta t_o=y Delta t_e`, and preserves photon number
and angular direction. In a static Euclidean baseline it predicts
`D_L=yD`, `D_A=D`, surface brightness proportional to `y^-2`, and still
violates `D_L=y^2D_A`. Exact photon-plus-screen energy conservation requires a
screen reservoir state and Hamiltonian; the ideal dilation alone is not that
derivation.

### R3 — optical/spatial completion

Add exactly the beam-area response needed for metric reciprocity, or introduce

\[
ds^2=-A(t)^2c^2dt^2+B(t)^2d\mathbf x^2.
\]

Writing a putative wake factor as `W(t)`, all ideal electromagnetic propagation
observables depend on the product

\[
S(t)=B(t)W(t),\qquad
1+z={S_o\over S_e},\qquad
H_{\rm eff}=\dot S/S=H_{\rm geom}+\Gamma_{\rm wake}.
\]

R3 recovers redshift, duration, reciprocity, and Tolman scaling in form. But the
transformation `B -> B exp(f)`, `W -> W exp(-f)` leaves `S` and every such
observable invariant. Expected result: a rank-one two-component response and
C6 underdetermination unless C4 supplies an independently measurable
non-electromagnetic screen coupling.

## Gate rules

| gate | frozen pass rule |
|---|---|
| C1 invariant observable | Nonzero endpoint frequency ratio survives coordinate changes and is derived from a physical metric or interaction. |
| C2 conservation/image quality | Photon plus screen energy/information closes; fractional shift is achromatic; no stochastic blur or spectral distortion is added. |
| C3 time stretching | The same `y=1+z` gives `Delta t_o/Delta t_e=y`. |
| C4 independent distances | A distance likelihood uses candles/rulers/chronometers with their calibration assumptions, never redshift as its own distance. |
| C5 joint cosmology | One frozen law addresses distance, reciprocity/surface brightness, time stretching, CMB spectrum and `T(z)`, BAO/rulers, early-universe/growth consistency, and redshift drift. |
| C6 identifiability | The geometric and wake columns have full rank under independently specified observables; a product-only response fails. |
| C7 age/size | Activated only after C1--C6 pass. |

## Primary observational anchors

- Supernova spectral aging must scale as `1/(1+z)`; Blondin et al. find the
  exponent consistent with that relation ([arXiv:0804.3595](https://arxiv.org/abs/0804.3595)).
- The Tolman control is bolometric surface-brightness scaling `(1+z)^-4`, with
  explicit luminosity-evolution nuisance treatment; Lubin and Sandage report a
  result consistent with expansion and reject their tired-light baseline
  ([arXiv:astro-ph/0106566](https://arxiv.org/abs/astro-ph/0106566)).
- Distance duality is `D_L=(1+z)^2D_A` when photon number is conserved and
  photons follow unique null geodesics in a metric theory
  ([arXiv:astro-ph/0312443](https://arxiv.org/abs/astro-ph/0312443)).
- COBE/FIRAS supplies the blackbody-spectrum constraint
  ([arXiv:astro-ph/9605054](https://arxiv.org/abs/astro-ph/9605054)); absorber
  thermometry supplies the independent `T_CMB(z)` relation, with Noterdaeme et
  al. finding `beta=-0.007+/-0.027` in
  `T=T0(1+z)^(1-beta)` ([arXiv:1012.3164](https://arxiv.org/abs/1012.3164)).
- Pantheon+ supplies calibrated supernova likelihood structure and systematics
  ([arXiv:2202.04077](https://arxiv.org/abs/2202.04077)); DESI DR1 supplies
  transverse/radial BAO distances in seven redshift bins
  ([arXiv:2404.03002](https://arxiv.org/abs/2404.03002)).
- Redshift drift is a direct derivative observable. Darling's existing radio
  constraints remain orders above the cosmological signal
  ([arXiv:1211.4585](https://arxiv.org/abs/1211.4585)); the Sandage--Loeb
  strategy is defined in [arXiv:astro-ph/9802122](https://arxiv.org/abs/astro-ph/9802122).

## Dataset and likelihood activation rule

The primary-source datasets and likelihood families above are preregistered in
`02-datasets-and-likelihoods.md`. No cosmological parameter fit is activated
unless one candidate first passes C1--C3 and C6 analytically. This prevents a
flexible non-identifiable decomposition from being fitted and misreported as a
screen detection.

## Decision

- **SURVIVES** only if one C4-derived law passes C1--C6 with independently fixed
  parameters.
- **UNDERDETERMINED** if an admissible optical law exists but wake and geometry
  enter only through one observable product/sum.
- **NEGATIVE** if only removable-lapse or energy-loss candidates remain, or a
  decisive independent gate fails.

No age, lookback, horizon, size, static-universe, or eternal-universe claim is
computed unless the result is `SURVIVES`.

# Issue #228 — final decision and status report

Status: **complete**

Decision: **UNDERDETERMINED — no cosmic age or size revision**

## Outcome

The simplest wake-redshift proposal fails: a homogeneous time-dependent lapse
is removable, and a stationary photon energy-loss law does not stretch
transients. An ideal coherent dilation can stretch a packet by the observed
frequency factor without blur, but it fails distance duality until a spatial
beam response is supplied.

Adding that response yields a metric optical scale. If geometry and wake are
written separately, all ideal electromagnetic observables depend on

\[
S(t)=B(t)W(t),\qquad H_{\rm eff}=H_{\rm geom}+\Gamma_{\rm wake}.
\]

The two component columns are identical. Redshift, time stretching, optical
distances, surface brightness, and redshift drift cannot determine the split.
This is structural underdetermination, not a request for a larger optical
sample.

## Information-area R4 result

The owner-supplied post-preregistration proposal makes screen expansion itself
the geometry: fixed area per persistent record gives

\[
B=\sqrt{N/N_0},\qquad 1+z=\sqrt{N_o/N_e}.
\]

This is invariant and automatically stretches wavepackets. It also produces a
sharp deceleration law:

\[
q_B=1\quad\text{for constant persistent-record production},
\qquad q_B={2\over p}-1\quad\text{for }N\propto t^p.
\]

R4 is not yet derived from C4. Global information is conserved, so `N` must be
reduced-state persistent occupancy or activation of latent sites, not newly
created global entropy. The persistence criterion, cell area, area-growth
energy/stress, `N(t)`, saturation, and perturbations are missing. If pure
late-time deceleration is imposed, its sign is in tension with the registered
calibration-independent SN acceleration test under that test's assumptions.

## Gate result

| gate | strongest result |
|---|---|
| C1 invariant observable | **formal pass** for metric R3/R4; lapse-only fails. |
| C2 conservation/image quality | **fail derivation:** no photon-screen/area-growth Hamiltonian and coherence ledger. |
| C3 time stretching | **formal pass** for coherent dilation and metric R3/R4; energy-only fails. |
| C4 independent distances | **formal likelihood defined, not activated:** analytic stopping rule fired first. |
| C5 joint cosmology | **fail/absent:** no frozen CMB, ruler, early-universe, growth, or drift dynamics. |
| C6 identifiability | **fail:** mixed optical geometry/wake response has rank one. |
| C7 age and size | **blocked by rule.** |

## Completed work

- froze R0--R3, C1--C7, primary observational anchors, dataset registry, and
  likelihood activation rule before implementation;
- proved the lapse no-go and derived energy-only, coherent-dilation, metric,
  reciprocity, surface-brightness, and drift controls;
- proved the exact `BW` redefinition symmetry and rank-one decomposition;
- incorporated R4 after preregistration and derived its record-area redshift and
  acceleration conditions;
- separated global information conservation from reduced persistent records;
- documented primary literature, assumptions, systematics, all inputs and
  negative/underdetermined outcomes;
- generated focused H-SSV instruments, tests, and a hash-pinned receipt without
  opening a cosmological parameter likelihood.

## What could reopen H-SSV-V

C4/R4 would need to derive a persistent-record observable, fixed cell-area and
energy/stress law, `N(t)` including perturbations and saturation, and at least
one independently measurable response that differs from ordinary metric
expansion. Only then should the preregistered joint cosmological likelihood run.

# Issue #129 GW-POL — is SSV's gravitational wave detectable as a tensor wave?

**Status: R2 — the pre-registered clean negative, on two independent counts.
SSV's gravitational wave is the gapless scalar phonon; its acoustic-metric
perturbation is the isotropic γ = 1 weak field (the SAME structure that bends
light correctly), which is helicity-0 scalar (breathing + longitudinal) with
ZERO traceless-transverse part. (1) POLARIZATION: F_SSV carries no helicity-2
(cos 2ψ) content — tensor overlap = 0 — so SSV falls in the LVK-disfavoured
scalar class. (2) AMPLITUDE: the isotropic spatial metric cancels exactly in
the differential interferometer readout (F_breathing = −F_longitudinal); the
residual is an O(fL/c) longitudinal leak, ≈ 2.9×10⁻³ at 100 Hz / 4 km, so a
true SSV wave read under tensor templates is inferred ~339× too distant —
GW170817's 40 Mpc would land at ≈ 13.6 Gpc, grossly inconsistent with its EM
distance. The one clean PASS: SSV emission has no monopole or dipole (mass /
momentum conservation, Lighthill), so it survives the Hulse–Taylor ~0.1%
dipole bound. The longitudinal/scalar identification of gravitational waves is
falsified as a complete account of the LVK observations.**

Pre-registered on issue
[#129](https://github.com/StigNorland/SVT/issues/129) (the GW-POL reframe
comment + the opening pre-registration with decision rules R1/R2, both posted
before this computation). Script: `instruments/paper_iv/gw_polarization.py`;
receipt `gw_pol_receipt.json`; tests
`instruments/test/paper_iv/test_gw_polarization.py` (8: positive control,
helicity content, the cancellation identity, long-wavelength cancellation,
finite-frequency suppression scaling, transfer-function limit, emission
selection rules, verdict).

## The structural spine (why this was expected — see the #129 reframe)

With the holographic γ = 1 (#154/#155) the SSV weak field is the isotropic

> ds² = (1 + 2Φ/c²)c²dt² − (1 − 2Φ/c²) δ_ij dxⁱdxʲ.

The spatial part (1 − 2Φ/c²)δ_ij is **conformally flat in space** — a trace
(scalar) deformation. Light deflection (γ = 1, lensing) comes from the *time
vs space sign difference* (the metric is **not** conformally flat overall, so,
unlike Nordström 1913, deflection ≠ 0). But a LIGO wave is the
**traceless-transverse shear** h_ij^TT, to which a conformal/trace metric
contributes identically zero, and the acoustic (Unruh) metric
g ∝ diag(−(c²−v²), δ_ij) + vector flow has **no TT part at all**. So lensing
success and tensor-GW absence are *one fact*: the emergent metric is
conformal-in-space. The propagating spin-2 graviton would need an induced
Einstein–Hilbert kinetic term, which superfluid/analog gravity does not supply
(the Visser/Volovik kinematics–dynamics wall — the same wall that conceded G's
magnitude); the only gapless propagating mode is the scalar phonon (#138).

## Module A — the polarization modes, antenna patterns, and helicity content

Six Eardley–Lee–Lightman modes built from the wave frame; the L-shaped
interferometer antenna patterns F^A = D : e^A reproduce the published closed
forms to **3.3×10⁻¹⁶** (positive control — the instrument is validated before
its verdict is trusted). ψ-harmonic content (the spin discriminator):

| mode | helicity |n| | ψ-dependence |
|---|---|---|
| plus, cross | **2** | cos 2ψ / sin 2ψ |
| vec_x, vec_y | **1** | cos ψ / sin ψ |
| breathing, longitudinal | **0** | ψ-independent |

## Module B — the SSV mode content and its readout

The isotropic spatial metric is an **equal breathing + longitudinal mix**
(h_ij ∝ δ_ij = e_b + e_L), and for an interferometer **F_b = −F_L exactly**.
Hence the long-wavelength differential response cancels:

> max over sky+ψ of |F_SSV| = |F_b + F_L| = **3.1×10⁻¹⁶** (vs tensor max 1.0).

The residual is purely finite-frequency — the breathing and longitudinal
transfer functions differ at O(fL/c), so a longitudinal scalar mode leaks in.
RMS sky suppression |F_SSV|/|F_tensor| (arm L = 4 km), from the direct
round-trip light-travel integral (which carries both the light-delay and, by
gauge invariance of the long-wavelength tidal response, the mirror-motion half
of the composite):

| f [Hz] | 1 | 10 | 50 | 100 | 300 | 1000 |
|---|---|---|---|---|---|---|
| suppression | 2.9e-5 | 2.9e-4 | 1.5e-3 | **2.9e-3** | 8.8e-3 | 2.9e-2 |

Linear in f (the O(fL/c) leak), confirming the cancellation is exact and the
signal is *suppressed, not absent*. The polarization **class** stays scalar
(helicity-0) at every frequency.

## Module C — the three confrontations

**(i) Polarization / LVK.** F_SSV is built from helicity-0 modes only ⇒ zero
cos 2ψ content ⇒ **tensor overlap = 0**. A detector network reading SSV would
classify it as non-tensor — matching exactly the hypothesis LVK *disfavours*
(pure tensor preferred over scalar/vector at high Bayes factors, GW170814 /
GW170817).

**(ii) Standard-siren amplitude / GW170817.** Inferred amplitude scales with
the response, so a true SSV wave read under tensor templates appears
1/2.9×10⁻³ ≈ **339× weaker → 339× too distant**. GW170817's EM distance
40 Mpc would be inferred at **≈ 13.6 Gpc** — a clean, no-new-data falsifier
(and at face value SSV predicts the loud detections should be near-invisible).

**(iii) Emission / Hulse–Taylor — the one PASS.** With total mass and momentum
conserved, the monopole (d²M/dt²) and dipole (d²P/dt²) radiation moments
vanish identically (**0.0** each in the receipt), leaving the quadrupole
(d³Q/dt³ ≈ 124) as the leading channel — the Lighthill selection rules, the
same as GR's. So SSV carries **no dipole radiation** and survives the
Hulse–Taylor ~0.1% bound. This is genuinely clean: scalar gravity *generically*
radiates a dipole, and SSV is protected from it by momentum conservation.

## Verdict and decision rules

- **R1 (PASS)** required helicity-2 content AND tensor overlap ≥ 0.9. **Not
  met** (overlap 0, helicity set {0}).
- **R2 (clean negative)** — **triggered**, with quantified teeth: tensor
  overlap 0; differential suppression 2.9×10⁻³ at the LIGO band → ×339
  distance bias; emission dipole = 0 (the HT pass).

## Honesty items and contingency (rule 1)

- The result is **contingent on the U(1)-scalar acoustic metric**, not on
  "superfluid vacuum" in general. A richer (multi-component / tensorial) order
  parameter could carry a transverse-traceless Goldstone/collective mode
  (precedent: the fractional-quantum-Hall "chiral graviton", an emergent spin-2
  mode — but gapped and chiral, not the gapless c-mode needed; #138 found no
  second linear mode here). This is the surviving-version requirement, **not** a
  softening of the negative.
- The standard obstruction to an emergent massless spin-2 is the
  **Weinberg–Witten theorem**; SSV's preferred-frame/presentist substrate is a
  recognised loophole — but it owes the same ≲10⁻¹⁷ Lorentz-violation budget as
  #148. Logged as open physics.
- The LVK polarization constraints are strong but **not** at the 10⁻¹⁵ severity
  of the speed test (two-detector events do not test polarization; the teeth are
  GW170814 / GW170817). So this is a standing, sharpening falsifier that the
  growing network (KAGRA, ET, CE, more sirens with EM counterparts) will tighten
  — confrontation (ii) (the amplitude/distance bias) is the more model-independent
  kill of the two.
- Speed c_gw = c passes natively (the phonon propagates at the medium sound
  speed by construction) — that LVK constraint (GW170817, 10⁻¹⁵) is *not* the
  failure point; polarization and amplitude are.

## Net

The bare medium already failed the *static* spatial sector (H-SPATIAL, γ_eff=0);
the holographic γ=1 recovered the static half **in form** (#155). GW-POL shows
that recovery does **not** extend to the radiative sector: the same conformal
metric that lenses light correctly carries no tensor wave and largely cancels in
an interferometer. SSV is, at the level of the present equation, a scalar+vector
theory of gravity — which is exactly why it passes every spin-blind static test
and meets its first genuine spin-2 test, GW polarization, as a clean negative.

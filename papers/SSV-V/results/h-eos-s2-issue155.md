# H-EOS S2 — the LogSE vacuum's cross-horizon entanglement entropy is area-law; the missingness is entirely in the coefficient (issue #155)

**Status: R1 on the *form* (area-law), at the pre-registered bars — but R1 is
the expected, less-valuable side (rule 1). The valuable content is the
*confirmed concession*: the area-law coefficient η overshoots G by
(a_p/l_P)² ≈ 1.69×10³⁸, so the medium generates the area-law *form* of its own
holographic screen but NOT G's magnitude. "Form yes, G no," exactly as
pre-registered (#154 D-b concession; #155 S2 prediction).**

Pre-registered on issue [#155](https://github.com/StigNorland/SVT/issues/155)
(hypothesis + R1/R2/R3 in the body; the S2 instrument design, four
configurations, correlator method, and verdict mapping posted as a comment
*before computing*, rule 6). Script:
`instruments/paper_v/horizon_entanglement_entropy.py`; receipt
`papers/SSV-V/results/heos_s2_receipt.json` (+ `_quick`); figure
`papers/SSV-V/figures/heos_s2_entanglement.png`; tests
`instruments/test/paper_v/test_horizon_entanglement_entropy.py` (10: kernel
closed-form, baseline area-law, volume control, η-universality, dumb-hole
tracking, **negative capability**, chiral silence, verdict shape).

## What was computed

Entanglement entropy is a property of a **quantum** state; the SSV solver
evolves a classical field. S2 therefore quantizes the **Bogoliubov–de Gennes
fluctuations** (phonons) around a background and computes the entanglement
entropy of that Gaussian vacuum by the **correlator method** (Peschel 2003;
Casini–Huerta 2009) — `X=½K^{-1/2}`, `P=½K^{+1/2}`, restrict to a region,
`S=Σ[(ν+½)ln(ν+½)−(ν−½)ln(ν−½)]` from the eigenvalues ν≥½ of `√(X_A P_A)`. The
LogSE phonon dispersion is `ω²(k)=c_s²k²+k⁴/4`, `c_s²=B0` (density-independent,
ξ=1/√(2B0)). Srednicki radial decomposition (`S(R)=Σ_ℓ(2ℓ+1)S_ℓ`) makes the 3D
problem a sum of 1D radial chains. Units ħ=m=B0=ρ₀=1; full run N=240 radial
sites, a=0.4, ℓ_max=110.

## Verdict: R1 (form derived), with the coefficient conceded

| config | what it measures | result | meaning |
|---|---|---|---|
| **A baseline** (flat LogSE vacuum) | S(R) vs region radius, exponent p | **p = 1.830**; area-frac 0.80; S/R³ = 2.93→0.58 ↓0 | **area-law** |
| area calibrator (gapped scalar, *provably* area-law) | same readout | **p = 1.826** | sets "area-law = 1.83 at this grid" |
| **D volume control** (extensive thermal) | S(R) vs radius | **p = 3.000** | volume-law anchor |
| **C dumb-hole** (acoustic-metric inhomogeneity at r_H) | S(r_H) vs horizon radius | **p = 1.834**; c₂(C)/c₂(A)=1.05 | area-law, **η universal** |
| **B chiral-on** (#138 term) | ΔS vs chiral-off | **max-rel-diff = 0 (exact)** | chiral term silent |

The area-law form is **not** decided by a bare slope band — the log-log exponent
sits below 2 because of the subleading perimeter term `S=c₂R²+c₁R+c₀`, and the
*provably* area-law gapped scalar reads the same 1.83 at this finite grid. It is
decided by **bracketing between two calibrated anchors**: the LogSE vacuum (1.830)
and the dumb-hole (1.834) track the area calibrator (1.826) and sit a full 1.17
in exponent below the volume anchor (3.000); S/R³ falls monotonically toward 0
(sub-volume); the dumb-hole reproduces the baseline area coefficient (η universal
to 5%). Each clause is **negative-capable** and was shown to be: the test
`test_area_classifier_rejects_volume_law` confirms the *same* logic scores the
volume-law thermal series **not-area** — so the R1 is reachable-to-R2, not
engineered.

## Why the form is "yes" (and why that is the cheap half) — rule 1

The area-law of the cross-horizon entanglement entropy follows from the LogSE
**Bogoliubov Hamiltonian being local** (`ω²` is a polynomial in k² ⇒ a
finite-order-derivative, short-range operator), which is generic for any local
free field (Srednicki 1993; Bombelli et al. 1986). So S2 does **not** reveal an
SSV-specific dynamical miracle. What it does is **earn** the area law that SSV-V
§6.2 (eq SH) and SSV-VII-b §5.1 Step 3 currently merely *assert* by counting
boundary cells of size ξ²: the area-law is now a derived property of the medium's
quadratic vacuum, with the one candidate non-locality — the #138 chiral-shear
term — shown **exactly silent at quadratic order over irrotational flow**
(curl δj ≡ 0 ⇒ E⊥=O(ε⁴); the Mermin–Ho structure), so the form is
*chiral-protected*. Promotion: **asserted → derived-from-locality.**

## The carried negative (the valuable half): G NO, quantified

The entire missingness is in the **coefficient** η = entanglement-entropy-per-ξ²:
`G_eff = 1/(4ħc η)`, and a natural η~1/ξ² overshoots G_N by
`(a_p/l_P)² = 1/α_G = (m_P/m_p)² = 1.69×10³⁸` (the Susskind–Uglum species problem
= Sakharov, conserved under reformulation). This is the **conceded** sub-grain
input (D-b closed, #154): S2 measures the form and *reports the overshoot at full
strength*; it does **not** derive G's magnitude and does not try to. The
duality's weak-derivation falsifier (the same G must later also fit the a₀
coefficient and the dictionary ratio a_p/l_P) remains promissory, pending the
H-A0-IR battery.

## Honesty flags carried (rule 1)

1. **The dumb-hole is a static spatial inhomogeneity, not a flowing horizon.**
   Config C varies the sound speed on the horizon scale r_H (Visser §8 spirit)
   and confirms that this acoustic-metric inhomogeneity does **not** spoil the
   *vacuum* area-law. The genuine flowing acoustic horizon, its surface gravity,
   and the thermal (Hawking) state are the **S1 analytic battery (deferred)** —
   S2-first delivers the area-law *entanglement-entropy input* to the
   Jacobson/entanglement-equilibrium route, not the full Clausius closure.
2. **R1 is on the form only.** "Form derived" means the area-law premise of the
   Jacobson route is earned; the Unruh-T (S1a) and Clausius-closure (S1c) legs
   are not in this branch.
3. **The chiral residual.** Silence is exact only over *irrotational* flow; the
   chiral term can still act on *rotational* (vortex-sink) backgrounds — flagged
   as bounded residual risk for a future rotational-horizon config.
4. **Finite-size.** The measured exponent rises with lever arm (1.69→1.83 from
   R≤5 to R≤8) and is calibrated against the gapped-scalar anchor rather than
   asserted to be 2; the IR is regulated by the finite radial box (Dirichlet
   wall), the UV by the lattice (a≲ξ) and the k⁴ term.

## Consequences (applied this branch)

- **SSV-V §6.2** (eq SH / Ω_H counting): the area dependence is upgraded from a
  *schematic boundary-cell count* to a **derived** property of the medium's
  Bogoliubov vacuum (cross-horizon entanglement entropy, area-law, η universal),
  with the coefficient gapbox restated as the conceded (a_p/l_P)² overshoot.
- **SSV-V §7** (surface gravity / Hawking): a forward note that the area-law
  *input* to the Jacobson route is now earned (S2), while the surface-gravity /
  Unruh legs remain S1 (deferred).
- **SSV-VII-b §5.1 Step 3**: a cross-reference correction — the area law
  `S=A/4ξ²` is now *tested* (H-EOS S2), not asserted by vortex-core counting.
- **Claim-status (rule 5):** "horizon area law from the medium" moves
  *asserted/coincidence → derived (form)*; "G magnitude from the medium" stays
  *conceded input* (not falsified, not derived).

## Status

#155 S2 resolves: the *form* battery returns **R1 (area-law, η universal)**,
earning the previously-asserted area law from Hamiltonian locality and confirming
the form is chiral-protected (#138). The coefficient→G arm stays **conceded**
(the (a_p/l_P)² overshoot reported at full strength). Deferred to follow-on
branches on #155: **S1** (Unruh-T / surface gravity for a flowing dumb-hole +
Clausius closure) and **H-A0-IR** (the a₀ coefficient + the duality
over-constraint falsifier). See
[project-holographic-screen-bridge] and [ref-visser-acoustic-black-holes].

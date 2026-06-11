# Issue #138 CHIRAL-DISPERSION — what does the αc channel actually do?

**Status: R1 on the operative clause (ω ∝ k², non-radiating, one signal
speed c), with the pre-registered coefficient correction triggered: the
k² coefficient is the quantum-pressure scale ħ/2m₀, NOT an α²-scale
stiffness — the chiral term is silent in the linear spectrum altogether.
Q3 is NEGATIVE (flagged at full strength, rule 1): the n̂ channel is
exactly as non-transactional as sound, so the spatial sector of gravity
is left with no candidate carrier anywhere in the present medium.**

Pre-registered on issue
[#138](https://github.com/StigNorland/SVT/issues/138) (decision rules
R1/R2/R3 in the issue body; Q3 and the sharpened stakes in the
post-H-SPATIAL comment; execution plan with S1 derivation route, S2
battery design and all thresholds posted as a comment before computing).
Script: `instruments/paper_ii/chiral_dispersion.py`; receipt
`chiral_dispersion_receipt.json`; figure
`papers/SSV-II/figures/chiral_dispersion_omega_k.png`; tests
`instruments/test/paper_ii/test_chiral_dispersion.py` (7: stepper
stability, quadratic-not-linear dispersion, Bogoliubov instrument
control, quartic chiral energy + current decoupling, λ-on dynamics
silence, Q3 static flatness, Q3 transit null with validated instrument).

## S1 — analytic (the derivation that predicted the outcome)

Linearize the spinor (CP¹, #83) LogSE + chiral-shear functional

> i∂ₜΨ_a = −½∇²Ψ_a + b ln(Ψ†Ψ)Ψ_a + VΨ_a + δE⊥/δΨ_a\*,
> E⊥ = (λ/2ρ₀²)∫|∇×j|², j = Im(Ψ†∇Ψ)

around the uniform vacuum Ψ₀ = √ρ₀ ζ₀ (units ħ = m₀ = 1, b = c_s² = 1).
Four exact statements:

1. **Chiral silence.** The linear-order current perturbation is
   δj = √ρ₀ ∇Im(δΨ₁) — a *pure gradient* in every channel (the spin
   channel enters j only at O(ε²); this is the Mermin–Ho structure:
   curl-bearing flow is quadratic in spin gradients). Hence
   ∇×δj ≡ 0, E⊥ = O(ε⁴), and the λ-term contributes **exactly zero to
   every linear dispersion around the uniform vacuum**. There is no
   propagating linear mode at c⊥ = αc (nor at √α·c, the SSV-II draft
   variant — the convention difference is moot). λ prices curl-bearing
   flow, which lives only in/near defect cores: statics.
2. **Free magnon.** The transverse-spin perturbation ε = δΨ₂/√ρ₀ obeys
   iε_t = −½∇²ε exactly (the spin-independent log term cancels against
   μ), i.e. **ω(k) = ħk²/2m₀** — gapless, quadratic, precessional
   (first-order in time). The coefficient is the quantum-pressure scale,
   not α²-anything: the α² stiffness lives one nonlinear order down, in
   the defect sector.
3. **Charge decoupling.** The magnon carries no linear-order mass
   current, so charged defects decouple from it at leading order.
   Kinematic honesty note (pre-registered): a gapless quadratic branch
   has zero Landau threshold, so the no-Cherenkov statement rests on the
   measured *coupling* (O(ε²)), not on kinematics.
4. **Q3 (transactionality): NO — exactly.** Over *any* static
   equilibrium background ρ_b(x) in a potential V, substituting the
   exact background equation gives

   > iε_t = με − ½[∇²ε + ∇ln ρ_b · ∇ε]

   — the magnon's effective potential V + b ln ρ_b = μ is a **global
   constant**, the same symmetry-protected cancellation that produced
   the H-SPATIAL γ_eff = 0 (the k → 0 magnon is the exact global spin
   rotation; its frequency cannot read the local background). The drag
   term affects amplitude transport only. The n̂ channel consults the
   local medium state exactly as little as sound does: **it would pay no
   A² tax.**

## S2 — numeric (validated instrument; receipt for exact numbers)

2D split-step spinor LogSE (conventions of `h_spatial_index.py`,
2/3-rule dealiased per the #129 numerics note; the chiral EOM term
−(λ/ρ₀²)(ẑ×∇(∇×j))·∇Ψ derived in the script and integrated by RK2 when
active).

| # | measurement | threshold (pre-registered) | result |
|---|---|---|---|
| B1 | magnon ω(k), 7 modes, k = 0.031–1.571 (1.7 decades below core scale) | R1 trigger p = 2.00 ± 0.05; R2 trigger p = 1.00 ± 0.05 | **p = 2.0000, A = 0.5000** vs ħ/2m₀ = 0.5 ⇒ R1 |
| B2 | Bogoliubov control, same readout on density channel | recover ω = k√(b+k²/4) to ≤ 1% | max dev **0.06%** — instrument distinguishes p=1 from p=2 |
| B3a | E⊥(ε) log-log slope on twist texture | 4.0 ± 0.2 (linear-order stiffness would give 2) | **4.000** |
| B3b | λ = 2000 ACTIVE in dynamics: Δω(ε) = ω_on − ω_off | shift ∝ ε²; ε→0 extrapolation ≤ 10⁻³ rel | shift ratio = ε² ratio; c₂ ≈ first-order PT λq⁴; extrapolated **≤ 7×10⁻⁴** |
| B4 | ‖j‖, ‖∇×j‖ vs ε | slope 2.0 ± 0.1 (slope 1 ⇒ R2 branch) | **2.000 / 2.000** |
| B5a | U_eff = V + b ln ρ_b − μ on relaxed background | ≤ 10⁻³·V₀ (unbalanced channel: ~1) | **~5×10⁻⁴·V₀** (= the tiny quantum-pressure term) |
| B5b | magnon transit vs unbalanced WKB prediction | PC ratio 1 ± 0.2; \|γ_magnon\| ≤ 0.1 ⇒ non-transactional | PC ratio **1.02**; **γ_magnon ≈ −1×10⁻⁵ to −10⁻⁴** ⇒ Q3 NEGATIVE |

(Quick-battery values shown where the full battery confirms them;
`chiral_dispersion_receipt.json` carries the full-scale numbers and the
`_quick` variant the fast ones. Both verdict identically on every rule.)

## Verdict mapping (fixed before the runs)

- **R1 fires on its operative clause**: ω ∝ k² (measured p = 2.0000),
  non-radiating, charge-decoupled; the two-speed problem dissolves; one
  signal speed c for everything that propagates.
- **The R1 parenthetical "(with α²-scale stiffness coefficient)" is
  corrected by the computation**: the coefficient is ħ/2m₀ and the
  chiral term is entirely absent from the uniform-vacuum linear
  spectrum. α is reinterpreted as the *defect-sector static stiffness
  ratio* — sharper than pre-stated: statics need stiffness, not a
  carrier, and the stiffness never enters any propagating dispersion.
- **R2 (Cherenkov falsification branch) does not fire**: no gapless
  linear branch (p = 1 excluded at >100σ of the fit spread), no
  linear-order charge coupling (B4 slope 2). The vacuum-Cherenkov no-go
  is *satisfied*, not triggered.
- **Q3 NEGATIVE** — the clean negative, recorded at full strength:
  the n̂ channel is non-transactional (B5a exact flatness; B5b
  γ_magnon ≈ 0 with the instrument validated at 2% on a real
  spin-channel potential). The bilateral-availability-tax mechanism
  (#129) finds **no carrier in the present medium**: phase channel
  (killed by #129), chiral-shear sector (no propagating mode at all),
  CP¹ channel (non-transactional, this issue). The A² spatial doubling
  demanded by lensing data remains mandatory structure that nothing in
  the present functional supplies.

## Consequences applied (per the pre-registered deliverables)

1. **SSV-II §"Resolved issue: photon propagation speed"** closes the
   EM_open_issue gapbox: one signal speed c; photon = phase-channel
   (Goldstone) wave; polarization = internal CP¹ direction transported
   on the phase channel; the polarization-transport derivation recorded
   as the new obligation (gapbox). Near-field passages re-read with
   c⊥ as a stiffness conversion constant.
2. **SSV-I §2 + claim table**: α = c⊥/c reinterpreted (claim-status row
   updated 2026-06): core-scale stiffness ratio of the defect sector;
   no second signal speed.
3. **SSV-Alpha**: the "what α is not" audit upgraded to a computed
   result; the aspect-ratio derivation target unchanged.
4. **SSV-Goldstone**: channel assignment upgraded from proposal to
   computed result (the Goldstone channel is the *only* propagating
   gapless linear channel); matching programme unchanged.
5. **SSV-II gravity section**: the Q3 negative recorded — the spatial
   sector has no candidate carrier in the present medium. This extends,
   and does not soften, the #129 falsification.

## What would have falsified the verdict (and did not happen)

- A measured p = 1.00 ± 0.05 with finite ω/k as k → 0 (R2): the
  instrument demonstrably resolves linear branches (B2 at 0.06%).
- A linear-order current (B4 slope 1): measured 2.000.
- γ_magnon = 1 ± 0.2 (transactional): measured ~10⁻⁴ with the
  positive control at 1.02 of prediction.

## Numerics note

The #129 lessons carried over (2/3-rule dealiasing mandatory;
peak-window centroids; spin channel needs no baseline subtraction —
component 2 is its own zero-background detector). One new lesson:
**a plane-wave magnon has exactly zero chiral force** (∇×j is constant
for it), so the λ-on dynamics test must use a transversely *modulated*
magnon (cos(q_y y)e^{iq_x x}), for which first-order perturbation theory
predicts the O(ε²) shift λε²q_x²q_y² — confirmed by the measured c₂,
which doubles as a check that the chiral advection term is implemented
with the right sign and magnitude.

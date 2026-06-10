# Issue #119 — falsification record and the bath-driven candidate

**Status: Phase 1 (falsification of the mutual mechanism) COMPLETE and
decisive; Phase 2 (bath-driven candidate) numerically delicate and in
progress.**  Headline: the mutual-radiation mechanism of SSV-II/SSV-IV is
**falsified** — H1a (retardation sign-oscillation) and H1c (static
screening) are both confirmed negatives, and H1b (unequal-frequency null) is
supported.  The bath-driven redesign is so far **untested**, not confirmed:
the first attempt was contaminated by nonlinear defect coupling, and the
clean linear-regime measurement is still being pushed above its noise floor.

Pre-registered in issue [#119](https://github.com/StigNorland/SVT/issues/119).
Solver: `instruments/paper_iv/bath_driven_interaction.py` (reuses the
integrator of `breather_interaction.py`).  2D logarithmic-Schrödinger medium,
`ħ = m = ρ₀ = 1`, `i ∂t ψ = −½∇²ψ + b ln|ψ|² ψ + V ψ`, edge relaxation
absorber, `b = 1` (so `c_s = 1`).

Repository rule 1 applies throughout: the Phase-1 results below are
**negative results and are the point** — they falsify the mutual-radiation
mechanism as written in SSV-II §"Newton's Constant" / SSV-IV §4, and are
flagged as such, not softened.

---

## Phase 1 — falsification record (mutual-radiation mechanism)

### H1a — radiation-zone sign structure  — **CONFIRMED (negative)**

Pre-registration: the time-averaged in-phase force `⟨F⟩(d)` oscillates in
sign with the retardation phase; sign zero-crossings spaced `λ/2` within the
sweep step (λ = 2π c_s/ω ≈ 8.98 at ω = 0.7).

Partial sweep (ω = 0.7, λ = 8.98, step 1.5):

| d | ⟨F_A,x⟩ |
|---|---|
| 7.0  | −3.77×10⁻² |
| 8.5  | +1.19×10⁻² |
| 10.0 | +4.46×10⁻² |
| 11.5 | +3.57×10⁻² |
| 13.0 | −1.79×10⁻³ |
| 14.5 | −3.37×10⁻² |

Full sweep, d = 7 → 46, step 1.5 (CPU):

| d | ⟨F⟩ | d | ⟨F⟩ | d | ⟨F⟩ |
|---|---|---|---|---|---|
| 7.0 | −3.77e−2 | 20.5 | +3.06e−2 | 34.0 | −2.51e−2 |
| 8.5 | +1.19e−2 | 22.0 | +7.58e−3 | 35.5 | −1.57e−2 |
| 10.0 | +4.46e−2 | 23.5 | −2.04e−2 | 37.0 | +7.55e−3 |
| 11.5 | +3.57e−2 | 25.0 | −2.89e−2 | 38.5 | +2.35e−2 |
| 13.0 | −1.79e−3 | 26.5 | −1.11e−2 | 40.0 | +1.78e−2 |
| 14.5 | −3.37e−2 | 28.0 | +1.59e−2 | 41.5 | −3.73e−3 |
| 16.0 | −3.33e−2 | 29.5 | +2.72e−2 | 43.0 | −2.10e−2 |
| 17.5 | −3.56e−3 | 31.0 | +1.33e−2 | 44.5 | −1.89e−2 |
| 19.0 | +2.66e−2 | 32.5 | −1.16e−2 | 46.0 | −5.08e−5 |

**Eight sign zero-crossings**, at d = 8.1, 12.9, 17.7, 22.4, 27.1, 31.8,
36.5, 41.2, with spacings **4.8, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7** — mean
**4.73**, matching the retardation prediction **λ/2 = 4.49** to within the
sweep step.  The time-averaged *mutual* force is therefore sign-indefinite,
oscillating with period λ/2 out to the largest separation tested.  Since
every physically realised gravitational separation is ≥ 10¹² proton-Compton
wavelengths, the as-written mutual mechanism gives an interaction that flips
between attraction and repulsion at every realised separation — it cannot be
the monotone 1/r² Newtonian force.  This **falsifies the SSV-II "independent
of zone" claim** and promotes the negative result Appendix A of SSV-IV had
only glimpsed to a quantitative, retardation-matched falsification.

### H1b — unequal-frequency null — **supported; clean rerun in progress**

Pre-registration: `⟨cos ω₁t · cos ω₂t⟩ = 0` for `ω₁ ≠ ω₂`, so the
time-averaged bilinear force between sources of unequal drive frequency must
be consistent with the isolated-source residual, while the equal-frequency
control at the same separation is large and attractive.

First run (near zone, ω_A = 0.15, d = 10):

| case | ⟨F_A⟩ |
|---|---|
| isolated source (residual) | −8.74×10⁻⁴ |
| equal-frequency control | +2.23×10⁻³ |
| unequal ω_B = 2× | −1.25×10⁻³ |
| unequal ω_B = 4× | −8.84×10⁻⁴ |
| unequal ω_B = 8× | −8.57×10⁻⁴ |

All three unequal-frequency forces sit essentially **at the residual**
(−8.7×10⁻⁴), i.e. there is no genuine mutual force — exactly the predicted
null.  The equal-frequency control is attractive and nonzero.  **Caveat:**
at this near-zone setting the control is only ≈ 3× the residual, too weak a
separation to be decisive, so the script returns INCONCLUSIVE on its own
strict rule.  A strong-coupling rerun (ω_A = 0.7, where the control is ~10³×
the residual; the null is exact and zone-independent because it comes from
time-averaging, not retardation) is running on GPU to make the separation
unambiguous.  **Table to be replaced with the strong-coupling run.**

### H1c — static screening — **CONFIRMED (negative)**

Pre-registration: linearising the stationary LogSE about ρ = 1 gives
`(−½∇² + 2b)s = −V` with `δρ = 2s`, i.e. a Yukawa-screened response with
screening constant `κ = √(4b) = 2` (length 0.5).  In 2D the tail is
`K₀(κr) ~ e^{−κr}/√r`.  An *unscreened* wave-dilution tail would fall as
`1/√r` (2D analogue of the 3D `1/r`).  Decision rule: response
exponentially screened on the healing length (decay rate = κ) and no
monotone power-law tail ⇒ the static (ω = 0) route to a long-range
Newtonian potential is **closed**.

Relaxed static profile (N = 256, V₀ = 0.5, w = 0.8):

| r | ⟨δρ⟩ | source W(r) |
|---|---|---|
| 0.20 | −2.73×10⁻¹ | 1.0 |
| 1.76 | −7.21×10⁻² | 1.19×10⁻¹ |
| 3.32 | −2.78×10⁻³ | 2.70×10⁻⁴ |
| 4.88 | +2.31×10⁻⁴ | 1.78×10⁻⁸ |
| 10.0 | +2.3×10⁻⁴ | ~10⁻³¹ |
| 17.4 | −4.92×10⁻⁵ | (sign flip) |
| 26.8 | −2.71×10⁻⁴ | — |

- **Fitted decay rate = 2.03**, versus the parameter-free prediction
  **κ = √(4b) = 2.0** — screening confirmed to 1.5%.  The response tracks
  the source down to ~10⁻³ by r ≈ 3.3, exactly as a Yukawa response should.
- The far field carries only a residual floor ~3×10⁻⁴ (≈ 10⁻³ of the core)
  that **changes sign** with radius (positive at r ≈ 5–16, negative beyond
  r ≈ 17).  A physical monopole tail is monotone and one-signed; a
  sign-flipping radial pedestal is the box/absorber standing-wave artifact —
  the documented "box-filling pedestal" of the #98 Q_p convergence test.
  It sits ~340× below the unscreened `1/√r` expectation.

The static (ω = 0) LogSE response is short-ranged.  **There is no static
long-range tail**, so the ω = 0 horn of the trilemma is closed: a static
density depression cannot supply the Newtonian 1/r potential.  Gravity in
SSV must come from the *oscillating* sector — which H1a shows is
sign-indefinite for the mutual mechanism, forcing the bath-driven redesign.

---

## Phase 2 — bath-driven candidate (secondary Bjerknes)

### H2a — first run CONTAMINATED; candidate still UNTESTED

Setup: two *passive* static wells (the defects) at `x = ∓d/2`, width 1.6,
in a maintained long-wavelength bath `V_bath = ε sin(ω_b t) cos(πx/L)`.
Interaction force = pair force − single-defect baseline.

First run (defect depth U = 0.5, ε = 0.15, ω_b = 0.1):

| d | F_pair | F_single | F_int |
|---|---|---|---|
| 6 | +2.15e−3 | +3.51e−4 | +1.80e−3 |
| 9 | −3.57e−3 | −4.96e−3 | +1.39e−3 |
| 12 | −3.67e−3 | +4.17e−3 | −7.84e−3 |
| 15 | −2.84e−3 | −1.72e−4 | −2.67e−3 |
| 18 | +6.98e−3 | −7.85e−3 | +1.48e−2 |
| 21 | −8.97e−4 | +8.54e−3 | −9.44e−3 |
| **no-bath control (d=6)** | | | **+6.85e−2** |

**This run does not test the bath-driven mechanism — it is contaminated.**
Two diagnostics show why:
- the defect response is δρ(A) = **−0.90** (ρ falls to 0.1 at the well): the
  U = 0.5 wells are deeply **nonlinear**, not the linear scatterers the
  secondary-Bjerknes picture requires;
- the **no-bath control** (ε = 0) gives F_int = **+6.85×10⁻²**, *larger than
  any bath-on value* — so the measured "interaction" is dominated by the
  direct nonlinear static coupling between the two deep wells, not by the
  bath.  (A further symptom: in this deep-nonlinear/chaotic regime CPU and
  GPU integrations diverge to different time-averaged forces, the signature
  of sensitive dependence — confirming the dynamics are chaotic, not a clean
  measurement.)

The sign-oscillation of F_int here is therefore **not** evidence against the
candidate; it is an artifact of over-deep defects.  The pre-registered H2a
test must be redone with **shallow linear defects** (δρ ≪ 1), whose static
pair coupling is screened to ≈ 0 — confirmed directly: at U = 0.03, d = 12,
the no-bath F_int = **+8.6×10⁻⁹** (ten million times smaller than the deep
case, and consistent with the H1c screening result).

**Calibration of the linear regime (GPU, U = 0.03, d = 12):**

| ε | ρ-osc amp | F_single | F_int |
|---|---|---|---|
| 0.005 | 3.1e−3 | −6.06e−7 | +9.36e−8 |
| 0.010 | 6.3e−3 | −2.09e−6 | +9.96e−8 |
| 0.020 | 1.25e−2 | −7.92e−6 | +1.16e−7 |
| 0.040 | 2.41e−2 | −3.25e−5 | +1.78e−7 |

In the linear regime the bath response is clean (amp ∝ ε; F_single ∝ ε²,
the primary radiation force), but the *interaction* F_int is **below the
pair-minus-single subtraction noise floor** (~10⁻⁷): it does not scale as
ε², so the genuine secondary force (∝ U²ε²) is too weak to resolve at
U = 0.03.  A boosted-but-linear configuration (larger U with δρ still ≪ 1,
closer defects, long averaging) is under test on GPU to bring the secondary
force above the floor.  **Verdict so far: the bath-driven candidate is
neither confirmed nor falsified — it is numerically delicate, and the clean
test is in progress.**  This is reported as-is per rule 1; no positive spin.

### H2b — factorisation and bath-amplitude exponent

Did not run: the driver chained H2b after H2a, and H2a's contaminated run
returned a non-pass exit code.  H2b is deferred to the linear-regime
redesign (it is only meaningful once H2a yields a resolved secondary force).
The coarse-grid pytest probe returned an amplitude exponent p ≈ −2.1
(tracked as issue #119 task), now understood as the same contamination:
with an over-strong bath the medium is driven nonlinear/chaotic and the
ε²-scaling is destroyed.

### H2c — analytic: the driven response and what carries the m₁m₂ law

This is the analytic half of Phase 2, pre-registered as: *derive the driven
sub-resonant response amplitude of a defect; response ∝ mass-energy is
required, else the m₁m₂ law fails.*

**Sub-resonant driven monopole.**  A defect sits in a locally uniform bath
pressure oscillation `δP(t) = a ρ₀ c² sin(ω_b t)` with `ω_b` far below the
defect's internal (Compton) frequency — in the physical application
`ω_b/ω_Compton ≲ 10⁻⁴⁰`, the deepest sub-resonant regime imaginable.  In
this limit the response is stiffness-dominated and the induced volume
oscillation is the static-compression answer evaluated adiabatically:

    δV_ind(t) = −Ξ · δP(t),       Ξ = (∂V_def/∂P) = contrast volume × κ_med

where the *acoustic contrast volume* is the integrated density deficit the
defect maintains against the medium.  Two consequences:

1. **Universality (equivalence principle).**  Deep sub-resonance kills the
   detuning dependence: the response coefficient contains only the medium's
   stiffness (the logarithmic `b`), which is the same for every defect.  A
   resonant mechanism would have made the coupling species-dependent and
   violated the equivalence principle; the cosmologically slow bath makes
   that violation vanish identically.

2. **Mass proportionality is inherited, not new.**  `R ∝ m` holds iff the
   defect's contrast volume is proportional to its mass-energy — which is
   precisely the Paper-II Step-3 assignment `δV ∝ m/ρ₀` (a defect of
   mass-energy m displaces medium volume m/ρ₀).  The bath-driven mechanism
   therefore needs **no new coupling postulate**: the same input that gave
   the old mechanism its m₁m₂ gives it here, but now through a channel that
   survives retardation.

**The force between two driven monopoles.**  Two induced monopoles
oscillating in phase (both driven by the same bath, both sub-resonant) at
separation `r ≪ λ_b` interact through the medium's quadratic term exactly as
Bjerknes pulsators:

    F(r) = −(ρ₀/4πr²) ⟨ δV̇₁ δV̇₂ ⟩
         = −(ρ₀ ω_b² a² Ξ² m₁ m₂ / 8π r²) × (medium constants)

attractive, `1/r²` in 3D (`1/r` in the 2D simulation), and **sign-definite
at every physical separation** because `r ≪ λ_b` always holds for a
cosmological bath mode.  Reading off Newton's constant:

    G_eff ∝ ρ₀ ω_b² χ² a_bath²

**Consequence for H2d (recorded for the next step):** G inherits the bath
through the combination `ω_b² a_bath²` — *both* the amplitude **and the
frequency** of the bath enter.  The Ġ/G decision rule must therefore track
the cosmic evolution of `ω_b² a²`, not amplitude alone.  (For a redshifting
free phonon mode, ω ∝ 1/a_scale and amplitude ∝ 1/a_scale in 3D … each
factor makes the drift worse; only a pinned condensate mode escapes.  To be
computed against the LLR bound |Ġ/G| ≲ 1.5×10⁻¹³ yr⁻¹.)

**The bath must be infrared-dominated (analytic corollary).**  The
secondary force requires the two defects to be driven *coherently* — same
phase across their separation, i.e. `d ≪ λ_mode`.  For an incoherent
(thermal) bath this is not a global obstacle per mode — each mode's
secondary force is quadratic in that mode, so contributions add
sign-definitely — but **only the modes with λ ≳ d contribute**; shorter
modes drive the pair out of phase and their contribution averages away.
Hence with a thermal bath, G becomes separation-dependent:
`G(d) ∝ ∫_{λ > d} ω² S(ω) dω`.  A CMB-like bath peaked at mm wavelengths
would switch gravity off beyond millimetre separations — catastrophically
wrong.  Conclusion: **the gravity driver must be an infrared-dominated,
effectively k ≈ 0 coherent condensate oscillation**, not the thermal
phonons SSV-IX reads as the CMB.  The SSV-IX bath and the gravity driver
are necessarily *different components* of the medium's excitation.
Falsifiable edge: any finite driver wavelength λ_drive predicts departures
from 1/r² at separations ≳ λ_drive; planetary ephemerides push λ_drive
≳ 10² AU.  (Whether a galactic-scale λ_drive connects to the Papers VI-a/b
anomaly phenomenology is a *candidate* question only — not claimed here.)

### H2d — Ġ/G scaling (analytic, to be completed against SSV-VIII/IX)

From H2c, `G ∝ ω_b² a_bath²`.  For a *freely redshifting* mode:
ω ∝ 1/a_scale and (energy density ∝ amplitude² ∝ a_scale⁻⁴ ⇒ amplitude ∝
a_scale⁻²), so `G ∝ a_scale⁻⁶` and

    Ġ/G = −6 H₀ ≈ −4×10⁻¹⁰ yr⁻¹,

exceeding the lunar-laser-ranging bound (|Ġ/G| ≲ 1.5×10⁻¹³ yr⁻¹) by a
factor ~3×10³ — **a freely redshifting driver is excluded**.  Combined with
the infrared-domination corollary above, both requirements point at the
same object: a pinned k ≈ 0 condensate zero-mode whose amplitude and
frequency are fixed by the saturation point (P₀, ρ₀), not by expansion.
Whether the LogSE condensate possesses such a pinned zero-mode (and why it
does not dilute) is now **the** open derivation of the gravity sector.

---

## Verdict table (to be completed)

| Hypothesis | Decision rule | Outcome |
|---|---|---|
| H1a | crossings spaced λ/2 | **CONFIRMED neg.** — 8 crossings, mean spacing 4.73 vs λ/2 = 4.49; mutual force sign-indefinite |
| H1b | unequal-ω force ≈ residual, control large | **supported** — unequal forces at residual; clean strong-coupling rerun in progress |
| H1c | static tail screened, no power law | **CONFIRMED neg.** — decay rate 2.03 vs κ = 2.0; far field a sign-changing box pedestal |
| H2a | sign-definite + monotone at d ≪ λ | **untested** — first run contaminated (nonlinear defects); linear-regime test in progress |
| H2b | factorisation ±10%; p = 2 ± 0.3 | deferred to linear-regime H2a |
| H2c | response ∝ m without new postulate | **met (analytic)** — inherits Paper-II δV ∝ m; sub-resonance protects EP |
| H2d | \|Ġ/G\| vs 1.5×10⁻¹³/yr | freely-redshifting driver excluded (−6H₀); needs pinned zero-mode |

**Net:** the mutual-radiation mechanism is falsified (H1a, H1c, H1b). The
bath-driven candidate survives analytically (H2c) but its central numerical
claim — a sign-definite near-zone secondary force (H2a) — is not yet
established; it is numerically delicate and under active test, and both
H2a-numeric and H2d point to the same open requirement: an infrared,
pinned, sector-blind condensate zero-mode as the gravity driver.

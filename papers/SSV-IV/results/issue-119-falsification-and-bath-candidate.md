# Issue #119 — falsification record and the bath-driven candidate

**Status: Phase 1 (mutual mechanism) FALSIFIED; Phase 2 (bath-driven force)
gives the right sign but the wrong range; Phase 3 (time-dilation field, the
correct observable) reframes the whole problem — the literal SSV-IV potential
is a box artifact, but the robust phase-blind field is the isothermal
(flat-rotation-curve) profile, not the Newtonian one.**

Headline chain:
- **The mechanical force is the wrong observable.** H1a/H1b falsify the
  two-body Bjerknes *force* (it oscillates in sign with retardation and
  vanishes for unequal frequencies).  But gravity in SSV-IV is the gradient
  of the *time-dilation field*, not a pressure force — so the force being
  falsified does not by itself settle gravity.  (Owner's correction,
  recurring; acted on in Phase 3.)
- **The time-dilation field is phase-blind** — it does NOT oscillate in sign
  and does NOT vanish for unequal frequencies, escaping H1a/H1b.  This
  vindicates the time-dilation framing over the force framing.
- **But its range is wrong for Newtonian gravity.**  The literal potential
  Φ ∝ ⟨δρ⟩ is a box-dependent standing-wave artifact (sign flips L=200↔L=400,
  Phase 3).  The robust, box-independent field is the wave **intensity**
  (energy density), ~r⁻¹ in 2D ⇒ **~r⁻² in 3D** by flux conservation.  As a
  *potential* that is too steep (1/r³ force); as a Poisson *source* it is the
  **isothermal ρ ∝ 1/r² halo that gives flat rotation curves** — tying this
  result directly to Paper VI-a.

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

### H1b — unequal-frequency null — **CONFIRMED (negative)**

Pre-registration: `⟨cos ω₁t · cos ω₂t⟩ = 0` for `ω₁ ≠ ω₂`, so the
time-averaged bilinear force between sources of unequal drive frequency must
be consistent with the isolated-source residual, while the equal-frequency
control at the same separation is large and attractive.

Strong-coupling run (ω_A = 0.7, d = 10, GPU):

| case | ⟨F_A⟩ | verdict |
|---|---|---|
| isolated source (residual) | +3.68×10⁻⁵ | — |
| equal-frequency control | +4.46×10⁻² | 1211× residual |
| unequal ω_B = 2× | −6.62×10⁻⁴ | NULL |
| unequal ω_B = 3× | +9.50×10⁻⁵ | NULL |
| unequal ω_B = 4× | +3.75×10⁻⁵ | NULL (= residual) |

The equal-frequency control is **1211× the residual** — a clean separation.
Every unequal-frequency force is below the null threshold; the ω_B = 4× case
lands *exactly* on the isolated-source residual.  There is **no
time-averaged mutual force between sources of unequal Compton frequency**:
the as-written mechanism gives no electron–proton gravity and fails mass
(∝ N) extensivity for composite bodies.  (The earlier near-zone run, ω_A =
0.15, gave the same nulls but with only a 3× control/residual separation —
superseded by this run.)

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
the primary radiation force), but at U = 0.03 the *interaction* F_int is
below the subtraction noise floor (~10⁻⁷).  Boosting to U = 0.12 (still
linear, δρ ≈ −0.10) and applying the double subtraction resolves the
secondary force cleanly.

**Production sweep (GPU, U = 0.12, ε = 0.03, ω_b = 0.1, double subtraction,
all points verified linear):**

| d | F_sec | note |
|---|---|---|
| 5  | +6.41×10⁻⁶ | attractive |
| 6  | +3.50×10⁻⁶ | attractive |
| 7  | +1.84×10⁻⁶ | attractive |
| 8  | +1.02×10⁻⁶ | attractive |
| 10 | +3.58×10⁻⁷ | attractive |
| 12 | −4.8×10⁻⁹  | **at noise floor (≈ 0)** |

Two findings, one encouraging and one likely fatal:

1. **Right sign (encouraging).** The bath-driven secondary force is
   **attractive and monotone** across d = 5→10 — unlike the mutual
   mechanism, it does *not* oscillate in sign.  The lone negative point
   (d = 12, −4.8×10⁻⁹) is two orders below the d = 5 value and consistent
   with zero at the ~10⁻⁷ floor; it is signal decaying into noise, not a
   genuine reversal.

2. **Short range (likely fatal).** The force decays far too fast to be
   gravity.  A fit to d = 5–10 gives **F_sec ∝ exp(−d/1.73)** (RMS residual
   0.045) or equivalently **∝ d⁻⁴·²** (RMS 0.071) — the exponential fits
   better, indicating **evanescent mediation**.  Long-range gravity needs a
   force ∝ 1/r (2D) / 1/r² (3D); this is *vastly* steeper.  The bath-driven
   secondary force is **short-ranged**.

**Interpretation — the trilemma reasserts itself.**  Across the three
regimes now tested, the LogSE medium offers a force that is either
long-range *or* sign-definite, never both:
- ω = 0 (static, H1c): sign-definite but screened (range 1/κ = 0.5);
- ω_b = 0.1 (sub-gap bath, H2a): sign-definite (attractive) but evanescent
  (range ≈ 1.7);
- ω ≳ gap (radiation zone, H1a): long-range but sign-oscillating (period
  λ/2).

The obstruction is the medium's **mass gap** κ = √(4b): bath modes below the
gap are evanescent (short-range), modes above it propagate but carry the
retardation sign-flip.  A long-range, sign-definite force appears to require
operating *at* a regime the gapped LogSE does not provide.  **Verdict: the
bath-driven candidate gives the right sign but the wrong range; on this
evidence it does not deliver long-range gravity any more than the mutual
mechanism did.**  Reported straight, per rule 1 — this is a negative
indication, not a setback to be smoothed over.

**Decisive next test (pre-registered for the next pass):** sweep ω_b from
sub-gap to above-gap and measure the decay length of F_sec versus its
sign-definiteness.  If short-range↔sign-definite and long-range↔oscillating
holds across the sweep, the trilemma is confirmed for the bath-driven case
and the candidate is falsified.  The one escape — a propagating *and*
sign-definite window — would have to appear there; the analytic expectation
(H2c) is that it does not, because the static attractive sign comes
precisely from the evanescent/concave regime.

### H2b — factorisation and bath-amplitude exponent — **factorisation PASSES**

Production run (GPU, d = 6, U ∈ {0.12, 0.24}, ε = 0.03, double subtraction,
all linear):

| case | F_sec |
|---|---|
| F(0.12, 0.12) | +3.4962×10⁻⁶ |
| F(0.24, 0.24) | +1.3060×10⁻⁵ |
| F(0.12, 0.24) | +6.7506×10⁻⁶ |

**Factorisation** F(lo,hi)² / [F(lo,lo)·F(hi,hi)] = **0.998** — the secondary
force obeys the m₁m₂ (bilinear) law to 0.2%.  So *where it is resolved*, the
bath-driven secondary force is a clean bilinear bath-driven interaction; the
defect "charge" is its well depth.  (The coarse pytest p ≈ −2.1 anomaly is
now understood as the over-strong-bath nonlinear contamination, resolved by
the linear regime.)  This does not rescue the candidate: H2a already showed
the force is **short-ranged**, and a factorising short-range force is still
short-range.

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

## Phase 3 — the TIME-DILATION field (the correct observable)

**Motivation (owner's recurring correction).**  Phases 1–2 measure the
two-body *mechanical force*.  But in SSV-IV gravity is the gradient of the
*time-dilation field* Φ(r) = α_g ln(ρ(r)/ρ₀): the "pull" is −∇(time delay),
not a pressure force.  The force is phase-sensitive (hence the H1a/H1b
failures); the time-dilation field is the time-averaged density well around
a *single* source — a one-body quantity, with no phase-correlation between
unlike clocks to spoil it.  Mode `hdil`; `run_dilation` measures the
time-averaged ⟨δρ(r)⟩ and the wave intensity ⟨δρ²_AC⟩(r) around one
oscillating source.

**Result — box-convergence is decisive.**  Two observables, two fates
(GPU, ω = 0.6, λ ≈ 10.5; boxes L = 200/N = 320 and L = 400/N = 640):

| quantity | L = 200 | L = 400 | status |
|---|---|---|---|
| intensity ⟨δρ²_AC⟩ tail | r⁻¹·⁰⁰ | r⁻⁰·⁹⁹⁹ | **box-independent (robust)** |
| DC well ⟨δρ⟩ plateau | +1.1×10⁻⁴ | −8.8×10⁻⁵ | **sign FLIPS → box artifact** |

1. **Phase-blindness CONFIRMED (vindicates the framing).**  Both fields are
   built from time-averaged |ψ|² — they carry no propagation-phase factor, so
   unlike the force they **do not oscillate in sign with r** and **do not
   vanish for unequal frequencies**.  The time-dilation observable genuinely
   escapes the H1a and H1b falsifications.  This is the real content of the
   owner's correction: the *force* was the wrong thing to compute.

2. **The literal potential is a box artifact (negative).**  The rectified DC
   density ⟨δρ⟩ — which is literally Φ/α_g in SSV-IV eq. (phi_rho) — has a
   plateau whose **sign reverses** between the two box sizes (+1.1×10⁻⁴ →
   −8.8×10⁻⁵).  That is a standing-wave/absorber pedestal (cf. the #98 box
   pedestal, the H1c far field), not a converged gravitational well.  The
   first single-box run's "PASS — long-range" was fitting this pedestal and
   is **retracted**.

3. **The robust field is isothermal, not Newtonian (the real result).**  The
   wave **intensity** (energy density) is clean and box-independent at
   **r⁻¹·⁰⁰ in 2D**.  By energy-flux conservation (intensity ∝ 1/r^{D−1})
   this is **1/r² in 3D**.  Two mutually inconsistent SSV-IV readings then
   fork sharply:
   - **(a) density = potential** (Φ = α_g⟨δρ⟩): 3D field ~1/r² ⇒ force ~1/r³
     — far too steep to be Newtonian gravity.
   - **(b) density = Poisson source** (∇²Φ = 4πG ρ_eff, SSV-IV §3 import):
     ρ_eff ∝ 1/r² ⇒ M(r) = ∫ρ_eff 4πr² dr ∝ r ⇒ v² = GM/r = **const ⇒ flat
     rotation curve.**  This is exactly the isothermal-halo profile.

**Verdict.**  The time-dilation framing **defeats the sign and
unequal-frequency objections** (real progress), but on this evidence it does
**not** produce a Newtonian 1/r potential: the literal potential is a box
artifact, and the robust energy-density field is the **isothermal 1/r²
(flat-rotation-curve) profile**, not the 1/r Newtonian one.  Whether that is
a feature (Paper VI-a's flat curves emerge for free) or a fatal bug (the
solar system must be Keplerian, not flat) hinges on the unresolved SSV-IV
ambiguity *(a) vs (b)* — density as potential vs density as source.  **This
ambiguity is now the central open question of the gravity sector**, and it is
the same conflation flagged in the very first SSV-IV review (§7.1 "ρ, c_s
unchanged" vs the acoustic-metric source term).

**Decisive next tests (pre-registered):**
- accumulate ⟨ln ρ⟩ directly (the faithful Φ) instead of ⟨δρ⟩, and re-test
  box convergence — does the −½⟨δρ²⟩ intensity term survive as the dominant,
  sign-definite, box-stable part?
- a 3D run (now affordable on the upgraded GPU) to confirm intensity ~1/r²
  directly rather than by 2D→3D flux argument;
- resolve reading (a) vs (b) at the level of the LogSE Madelung equations:
  is the time-averaged log-density the potential, or the source of the
  potential?  Paper VII-b's metric derivation must answer this.

---

## Phase 4 — the 3D dimensional test (decisive on Newtonian vs isothermal)

The 2D simulation cannot separate "time delay ∝ wave amplitude" (→ 1/r,
Newtonian) from "∝ wave energy/intensity" (→ 1/r², isothermal) because 2D
dilution disguises the powers.  Mode `hdil3d` runs the single oscillating
source in full 3D (FP32 on GPU) and measures both fields, at two box sizes.

**Result (ω = 0.8):**

| box | intensity tail | DC plateau ⟨δρ⟩ |
|---|---|---|
| L = 100, N = 160 | r⁻¹·⁹⁹ | +3.8×10⁻⁶ |
| L = 140, N = 224 | r⁻²·⁰¹ | −6.3×10⁻⁵ |

1. **Intensity = 1/r² in 3D, box-independent** (both boxes within 1% of −2).
   This *confirms by direct 3D simulation* the flux-conservation prediction
   (intensity ∝ 1/r^{D−1}: 1/r in 2D, 1/r² in 3D).  The wave-cloud density —
   the owner's "dense cloud of waves that falls off fast but never null" — is
   the **isothermal ρ ∝ 1/r² profile**.
2. **The DC potential ⟨δρ⟩ is a box artifact in 3D too** (sign flips
   +3.8×10⁻⁶ → −6.3×10⁻⁵ between boxes), exactly as in 2D.  The literal
   Φ ∝ ⟨δρ⟩ reading is not a converged quantity in any dimension tested.

**Conclusion.**  The robust, phase-blind, box-independent time-dilation field
is the wave intensity, and in 3D it is **1/r² — the flat-rotation-curve
(isothermal-halo) profile, NOT the Newtonian 1/r potential.**  The
amplitude-vs-intensity fork is settled on the side of intensity (energy
density), consistent with the update-budget picture ("the condensate is busy
processing wave energy → time slows").  This means SSV gravity, read as
time-delay ∝ wave-cloud density, **natively produces flat rotation curves**
and must *recover* Newtonian 1/r in some limit (e.g. the near field of a
concentrated source, or reading (b) where the 1/r² density is a Poisson
source giving M(r) ∝ r) rather than producing it directly.  Directly ties
the gravity sector to Paper VI-a.

## Phase 5 — the black hole as a frozen-time resonator (`hbh`)

Owner's mechanism: particles do not make standing waves, but **black holes
do** — "time stops at the horizon → friction → the BH oscillates."  Paper V:
BH = acoustic-freezing horizon at A(r_H) = 0.  Owner's sharpening: a "black
*whole*" = an **intact condensate (ρ = ρ₀) with time frozen (A = 0)**, not a
depleted hole.  Modeled (`run_blackhole`) as a frozen-phase, full-density
core clamped each step to ψ = 1, embedded in an exterior whose phase advances
at μ — a Josephson junction whose phase difference winds at the time-shear,
with **no external drive**.

**HBH-a — self-oscillation CONFIRMED** (N = 160, FP32):

| | probe oscillation amplitude |
|---|---|
| control μ = 0 (no time-shear) | **0.000** (exactly) |
| μ = 1.0 (time-shear on) | 0.06–0.11 |

With the time-shear off the core is silent; with it on the boundary
**self-oscillates with no external driver**.  The control is decisive: it is
the *shear* (frozen-vs-flowing time), not the clamp, that pumps the
oscillation — a direct numerical confirmation of the owner's
"time-freeze → friction → oscillation" mechanism, and the physical origin of
the standing wave Paper VI-a posits.

**HBH-b — frequency scaling f ∝ 1/R: NEGATIVE.**  Resolved with a long
window (n_meas = 220, bin width ~0.005):

| R | 5 | 8 | 12 | 18 |
|---|---|---|---|---|
| w | 0.0455 | 0.0455 | 0.0500 | 0.0546 |

The self-oscillation frequency is **~constant (~0.05) and weakly *increasing*
with R — not the 1/R *decrease* required**.  So this simple frozen-core model
**does not reproduce the Paper VI-a eigenfrequency f_BH = f_p·(m_p/M_BH)**.
The oscillation exists and is shear-driven (HBH-a), but its frequency is set
by something other than the core size (a fixed mode of the medium/box, or a
residual of the ramp — the value sits at low FFT bins where slow transients
also live, so even this number is delicate).  Reported straight per rule 1:
the "horizon friction *derives* the galactic standing-wave scale" hypothesis
is **not supported** by this model.  A faithful test would need the Paper-V
acoustic-inflow horizon (supersonic radial flow), not a hard ψ-clamp, and a
frequency cleanly separated from the ramp — both deferred.

---

## Verdict table (to be completed)

| Hypothesis | Decision rule | Outcome |
|---|---|---|
| H1a | crossings spaced λ/2 | **CONFIRMED neg.** — 8 crossings, mean spacing 4.73 vs λ/2 = 4.49; mutual force sign-indefinite |
| H1b | unequal-ω force ≈ residual, control large | **CONFIRMED neg.** — control 1211× residual; all unequal forces NULL (ω_B=4× sits on residual) |
| H1c | static tail screened, no power law | **CONFIRMED neg.** — decay rate 2.03 vs κ = 2.0; far field a sign-changing box pedestal |
| H2a | sign-definite, attractive, AND long-range | **sign OK, RANGE FAILS** — attractive & monotone but short-ranged (∝ e^{−d/1.7} ≈ d⁻⁴·²); cannot be long-range gravity |
| H2b | factorisation ±10%; p = 2 ± 0.3 | **factorisation PASS** (0.998, m₁m₂ law) — but a factorising short-range force is still short-range |
| H2c | response ∝ m without new postulate | **met (analytic)** — inherits Paper-II δV ∝ m; sub-resonance protects EP |
| H2d | \|Ġ/G\| vs 1.5×10⁻¹³/yr | freely-redshifting driver excluded (−6H₀); needs pinned zero-mode |
| H3-dil | time-dilation field long-range & sign-definite | **phase-blind YES; literal Φ a box artifact; robust field ~1/r² (3D) = isothermal, not Newtonian** |
| H4-3D | intensity 1/r²? DC box-stable? | **intensity r⁻²·⁰ (both boxes) = isothermal CONFIRMED in 3D; DC again a box artifact** |
| H5-bh (HBH-a) | frozen-time core self-oscillates from shear | **CONFIRMED** — μ=0 control amplitude exactly 0; μ>0 self-oscillates (no driver) |
| H5-bh (HBH-b) | emission f ∝ 1/R (→ f_BH ~ 1/M) | **NEGATIVE** — w ≈ const (~0.05), weakly increasing with R, not 1/R; does not derive VI-a f_BH in this model |

**Net.**  Three layers, one conclusion:
1. The mutual-radiation **force** is falsified (H1a sign-oscillation, H1b
   unequal-frequency null, H1c static screening).
2. The bath-driven **force** has the right sign and factorises (H2b) but is
   **short-ranged** (H2a) — it cannot be long-range gravity either.
3. The **time-dilation field** (the correct observable, H3-dil) is
   phase-blind and so escapes the sign/frequency objections — genuine
   progress — but the literal potential ⟨δρ⟩ is a **box artifact**, and the
   robust energy-density field scales as **1/r² in 3D**: the
   **isothermal/flat-rotation-curve profile, not the Newtonian 1/r one**.

The gravity sector therefore hinges on one unresolved theoretical fork:
**is the time-averaged log-density the potential, or the Poisson source of
the potential?**  Reading (b) (source) yields flat rotation curves for free
and links to Paper VI-a; reading (a) (potential) gives a force too steep to
be Newtonian.  SSV-IV currently asserts both.  Resolving (a) vs (b) at the
LogSE/Madelung level (Paper VII-b) is now the central open problem.

---

## Phase 6 — "maybe it is both": the two-term Poisson resolution

Owner's resolution of the (a)/(b) fork: under reading (b), gravity is **one
Poisson equation with two source terms** —

    ∇²Φ = 4πG [ρ_core + ρ_cloud]

- **ρ_core** = the defect's own concentrated mass-energy → Φ = −GM/r →
  **Newton 1/r²** (the monopole term; Newton was never absent from (b));
- **ρ_cloud** = the radiated wave cloud.  Measured (hdil3d, 3D):
  **I·r² = 0.0405 ± 2%** over the full range — an *exact* 1/r² Poisson
  source → M_cloud(<r) ∝ r → the **v²/r flat-curve tail**.

Total g(r) = GM/r² + v²/r: Newtonian inside, flat outside, crossover at
r_c = M/(4πC).  BTFR (v⁴ = GM_bar·a₀) forces the cloud coefficient to scale
as **C ∝ √M**, whereupon g_cloud/g_N = √(a₀/g_N) — MOND-like phenomenology
with a₀ emergent from cloud-generation physics, and the solar system
automatically safe (Sun's crossover ≈ 7×10³ AU).

**Dwarf-galaxy cross-check (owner):**
1. *Dwarf DM excess — PASSES automatically.*  √(a₀/g_N) gives ~0.8 for
   MW-class interiors and 10–100 for dwarfs — the observed dwarf
   dark-matter domination is the same √M scaling as BTFR, seen locally.
2. *BH-as-cloud-source — FALSIFIED.*  With f_BH ∝ 1/M_BH (small black
   wholes oscillate faster), the radiated-power scalings give P ∝ M⁰
   (identical v_flat for all galaxies — contradicted) or P ∝ M⁻² (dwarfs
   faster — contradicted).  Decisive independent fact: **BH-less
   bulgeless/LSB galaxies sit exactly on the BTFR**, impossible if the
   central BH generates the halo.  The cloud is **baryon-sourced**; the
   black-whole resonator (Phase 5) is not the halo engine.  *This puts the
   Paper VI-a central-BH standing-wave mechanism for v_flat under direct
   pressure from two independent results* (HBH-b negative + BH-less BTFR);
   what may survive of VI-a is the wiggle/node structure as a secondary
   effect.

**Pre-registered next derivations:**
- *Core term:* show the defect's own energy density enters ρ_eff with the
  same coupling as the cloud (Newton from the monopole) — Paper VII-b.
- *Cloud scaling:* an incoherent particle-cloud sum gives C ∝ M (BTFR slope
  too steep).  Candidate mechanism for the required C ∝ √M: **cloud-
  intensity saturation** (the saturated medium / update-budget ceiling
  making generation self-limiting).  Decision rule: derived exponent
  0.5 ± 0.1 over the observed mass range, else the scaling sector of the
  two-term model is falsified.

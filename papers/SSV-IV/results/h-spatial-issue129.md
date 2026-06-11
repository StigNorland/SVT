# Issue #129 H-SPATIAL — does the medium delay light in a gravity well?

**Status: R2 — the clean negative. The literal LogSE medium supplies the
time half of gravity and NONE of the spatial half: γ_eff ≈ 0, with the
instrument's sensitivity demonstrated by a positive control that detects
a real index at the predicted sign and magnitude. Per the pre-registered
lensing addendum, R2 propagates: a γ_eff = 0 medium predicts light
deflection at half the observed value (Einstein-1911) and lensing masses
at half of dynamical masses — both contradicted by existing data
(1919/1922 eclipse; modern lensing–dynamics agreement). The bare LogSE is
therefore falsified as a complete carrier of gravity; the A² doubling
(the capacity tax co-scaling the grain with the tick) is mandatory
additional structure that the present medium does not contain.**

Pre-registered on issue
[#129](https://github.com/StigNorland/SVT/issues/129) (H-SPATIAL comment;
operational rules R1–R4; lensing-stakes and force-vs-time addendum, all
posted before computing). Script:
`instruments/paper_iv/h_spatial_index.py`; receipt
`h_spatial_receipt.json`; tests
`instruments/test/paper_iv/test_h_spatial_index.py` (4: stepper
stability, estimator synthetic recovery, positive control, the R2
separation).

## S1 — analytic (the derivation that predicted the outcome)

Linearize the Madelung form of the LogSE
(iψ_t = −½∇²ψ + b ln|ψ|²ψ + Vψ; ψ = √ρ e^{iθ}) around a static
background ρ_b(x) (∇θ_b = 0). With u ≡ δρ/ρ_b and φ the phase
perturbation, and dropping quantum-pressure terms (λ ≫ ξ):

> ρ_b u_t = −∇·(ρ_b ∇φ),  φ_t = −b·u
> ⇒ **φ_tt = b [∇²φ + ∇ln ρ_b · ∇φ]**

The eikonal/ray speed is √b **everywhere, independent of ρ_b**: the
logarithmic nonlinearity is the unique equation of state whose sound
speed (c_s² = ρ·∂μ/∂ρ = b) carries no density dependence. The
∇ln ρ_b·∇φ term affects amplitude transport only (no refraction at
eikonal order); the Bogoliubov dispersive correction (ω² = bk² + k⁴/4)
is *also* ρ-independent. The external potential V cancels out of the
linearized dynamics entirely (it is absorbed by the equilibrium
condition). **Phase waves of this medium cannot be index-delayed by a
density depression, at any order of this analysis.**

Matter clocks, by contrast, dilate: a defect's internal rate shifts with
the local chemical potential, δω/ω = δμ = b ln(ρ_b/ρ₀) ≈ −V (the H8b
identification, measured in #119 at the −1/(2b) level). So S1 predicts

> **γ_eff ≡ (index delay)/(clock delay) = 0.**

## S2 — numeric

2D split-step LogSE (b = c_s = 1, dealiased — see *numerics note*),
probe = a genuine collective sound packet (u, φ in the right-mover
eigenrelation), background = Thomas–Fermi depression ρ_b = e^{−V} from a
Gaussian V (σ = 120, ξ ≈ 0.7), baseline-subtracted detection
(packet-run minus no-packet-run on the same background removes startup
transients exactly at linear order), arrival measured by
envelope-centroid + carrier-phase demodulation (the VLBI/Shapiro
method).

**Positive control (the credibility of the null):** a region of
spatially varying coupling b(x) — which *does* change c_s, while uniform
ρ = 1 remains an exact equilibrium — must show its exactly predictable
delay (dispersion-corrected v_p = √(b(x) + k²/4)). PASS condition
±20%.

**Results (full battery; receipt for exact numbers):**

| measurement | result |
|---|---|
| speed calibration (3 λ, uniform medium) | v measured = dispersive v_g prediction to ≤ 0.1% |
| positive control (η = 0.04, real index) | measured 3.90 vs predicted 4.19 (ratio **0.930**) — instrument **VALIDATED** |
| depression λ = 10 (V₀ = 0.1; Δt_clock = 21.3) | index delay −0.034 ⇒ **γ_eff = −0.0016** |
| depression λ = 20 | index delay +0.014 ⇒ **γ_eff = +0.0007** |
| depression λ = 50 | index delay −0.34 ⇒ **γ_eff = −0.0162** |
| depth sweep V₀ = 0.05 (R4) | γ_eff = −0.0017 — null is depth-independent |
| R3 achromaticity | spread 0.017 across the factor-5 sweep (λ = 10→50; the quick-geometry runs at λ = 8, 16 agree, extending the span to ~0.8 decade — the σ ≫ λ ≫ ξ window of this domain; noted against the pre-registered full decade) |
| off-axis deflection (impact parameter σ/√2) | centroid shift −0.30 (null; well σ = 120) |
| **verdict** | **R2: γ_eff = 0 to a few ×10⁻³ of the clock delay, with the instrument's sensitivity to a real index demonstrated at the 7% level. R1 (γ_eff = 1 ± 0.1) decisively failed.** |

## Consequences (pre-stated in the addendum, now triggered)

1. **The bare LogSE is falsified as a complete gravity carrier.** A
   γ_eff = 0 medium gives Einstein-1911 light deflection (0.87″ solar) —
   half the measured 1.75″ (Lick 1922: 1.72 ± 0.11) — and lensing masses
   at half of dynamical masses, against the observed lensing–dynamics
   agreement. The time sector (Pound–Rebka family) is delivered; the
   spatial sector is not present in the equation.
2. **The required extension is now sharply specified:** gravity needs
   the loading to co-scale the effective grain with the tick
   (n = 1 + 2|Φ|/c²). Whatever supplies that — a ρ-dependent stiffness
   beyond the log term, the chiral/CP¹ sector (#138), or A-field
   structure from Paper III's update accounting — it is *mandatory*
   structure, not an optional refinement, and it must be achromatic and
   linear at weak load (the R3/R4 constraints carry over to any
   candidate).
3. **GW-POL inherits γ_eff = 0 for the bare medium:** in the literal
   LogSE the interferometer response to a passing density wave is
   carried by the mirror (matter) term alone; the light-delay term is
   absent. The antenna-pattern computation should be run for this case
   first — if pure mirror response cannot match the LVK tensor
   constraints either, the longitudinal identification fails at both
   ends for the bare medium.

## The surviving candidate: the bilateral availability tax (recorded, not yet derived)

Stated by the owner during the H-SPATIAL session, and recorded here as
the leading candidate for the structure the bare medium lacks. Let the
ambient loading throttle every process's availability to
A = 1 − |Φ|/c². Then:

- a **clock** is a *unilateral* process (a defect's self-oscillation):
  rate ∝ A — the time half, delivered and measured;
- a **propagating interaction** is *bilateral* — every handoff requires
  both parties free simultaneously; for uncorrelated busy-schedules the
  joint availability is the product: rate ∝ **A²** ≈ 1 − 2|Φ|/c² — the
  index, the doubled deflection, Shapiro, γ = 1.

γ = 1 becomes the statement "every interaction has exactly two ends";
the dielectric analogy is exact (light in glass is slow *because* it is
repeatedly processed by atoms). The mechanism explains the H-SPATIAL
null: the LogSE sound wave is not transactional — its restoring force
never consults the local medium state — so it pays no tax; a
transactional carrier would. Whether SSV's photon is transactional is
precisely the #138 (CHIRAL-DISPERSION) question, so the spatial sector
and the photon identification have merged into one problem.

**Derivation obligations (pre-stated falsifiers for any future
H-BILATERAL pre-registration):**
1. **Decorrelation** — the product rule A·A requires the two parties'
   busy-schedules to be uncorrelated; synchronized loading collapses the
   tax to a single factor (half deflection, falsified). The medium's
   loading statistics must be shown to be incoherent.
2. **Achromaticity and weak-load linearity** — inherited from R3/R4: the
   tax must be a rate-proportional levy (every cycle costs one update),
   not per-event latency, or lensing becomes chromatic.
3. **The velocity interpolation** — a massive particle at speed v is
   part monologue (A), part conversation (A²); the mix must reproduce
   GR's (1 + γv²/c²) deflection coefficient as v → c. A step function
   instead of v²/c² kills it.

## Numerics note (recorded for future solver work)

Three instrumentation lessons, each found by a failed run and each now
guarded:
1. **Aliasing instability.** The un-dealiased split-step LogSE has a
   high-k instability seeded by the probe (fp32: field corrupts by
   t ≈ 20; fp64 follows later) — the log nonlinearity is infinite-order
   in the perturbation and aliases into high k. A 2/3-rule spectral
   filter cures it completely (probe amplitude preserved to t = 1400 at
   full scale). Pinned by test.
2. **Record truncation.** Whole-record envelope centroids are dragged
   early when the packet's tail is clipped by t_end, corrupting the
   cycle-skip correction (the first full battery measured "delays" of
   ~100–200 that were identical for both well depths — the tell that
   they came from the instrument, not the well). Cure: peak-windowed
   centroids + carrier phase in the window overlap.
3. **Carrier-cycle minimum.** A packet with < 3 carrier wavelengths in
   its envelope is a broadband pulse; its "phase delay" is meaningless
   (the λ = 50, w = 100 run produced γ_eff ≈ +51 garbage). Cure:
   per-wavelength envelope widths w ≥ 3λ.
All earlier H-SPATIAL numbers predating these fixes are invalid and
superseded by this record; the positive control validated the final
instrument at both quick (ratio 0.910) and full scale before the
depression verdicts were read.

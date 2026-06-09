# #115 first pass: CP¹ Hopf-charge generations — Gate 1 PASS, Gate 3 (baseline) FAIL

**Issue:** [#115](https://github.com/StigNorland/SVT/issues/115) — generations as
CP¹ Hopf-charge sectors (π₃(S²) = ℤ) with a dynamical burst-threshold cutoff.

**Script:** `instruments/paper_i/hopf_generation_audit.py`
**Test:** `instruments/test/paper_i/test_hopf_generation_audit.py` (3 cases, pass)

This is the pre-registered cheap-gate-first opening pass. It does **not** build a
3D solver — that is gated behind these results. Hopfion textures are the analytic
Hietarinta–Salo A_{n,m} ansätze (Hopf charge Q = n·m); all derivatives are
spectral on a periodic box with the texture → south pole at the boundary.

---

## Gate 1 — quantum-number preservation: **PASS**

### G1a — three distinct, correctly quantised Hopf sectors

| (n,m) | Q | Hopf invariant H | H / H₁ |
|---|---|---|---|
| (1,1) | 1 | −1.000 | 1.000 |
| (2,1) | 2 | −1.999 | 2.000 |
| (3,1) | 3 | −2.998 | 2.999 |

The Whitehead integral H = (1/4π)² ∫ a·b returns clean integers with ratios
1 : 2 : 3. (The sign is the orientation of the ansatz — it → south pole; only the
magnitude/ratios bear the claim.) So the construction genuinely realises the three
sectors the hypothesis needs.

### G1b — electric charge is orthogonal to Hopf charge

Electric charge is the winding of the overall U(1) phase θ in Ψ = A e^{iθ} z (a
π₁(U(1)) invariant). The Hopf charge lives in n̂ = z†σz, which is invariant under
z ↦ e^{iθ}z. Built explicitly and multiplied by a genuine vortex-line phase
(electric charge 1), the texture is unchanged: **max|Δn̂| = 1.1 × 10⁻¹⁵**. So
stacking Hopf charge cannot disturb electric charge — the two are independent
additive sectors, exactly as a generation label must be.

> Not yet done (the decisive remaining part of G1): the **spin-statistics**
> (Finkelstein–Rubinstein / Hopf-term) check — whether a Q = 2, 3 hopfion is still
> spin-½ or whether spin tracks Q. Deliberately deferred (see verdict).

---

## Gate 3 — energetic hierarchy (baseline): **FAIL**

The observed mass steps demand E(Q) climb like ~Q⁷. The canonical
hopfion-stabilising (Faddeev–Niemi) energy on the same ansätze gives:

| step | computed E ratio | required (mass ratio) | shortfall |
|---|---|---|---|
| Q1 → Q2 (e → μ) | **1.30** | 206.8 | ~160× too flat |
| Q2 → Q3 (μ → τ) | **1.34** | 16.8 | ~13× too flat |

And this is an **unrelaxed ansatz** — an *upper* bound on the energy. The true
minima are flatter still: the Vakulenko–Kapitanskii theorem gives E ≳ Q^{3/4}
(sublinear), and Battye–Sutcliffe minimal energies run ≈ 1 : 1.5 : 1.9. Every way
of measuring it, the standard topological-soliton energy is one-to-two orders of
magnitude too flat to be a generation mass ladder.

This also kills, quantitatively, the volume/area (holographic) reading of the
×207 / ×17 spacing floated in #115: an area-law (Q^{2/3}) or volume-law (Q¹) is
*even flatter* than what we measured, not steeper.

### The chiral-shear escape hatch is closed too

The hatch left open in the first commit was: *SSV is not Faddeev–Niemi, maybe the
chiral-shear term (λ_⊥/2)|∇×j|² scales far steeper.* It does not. For a pure
texture (θ = 0, ρ = ρ₀ — no electric charge, saturated amplitude) the SSV current
is j ∝ a, the CP¹ Berry connection, so |∇×j|² = |∇×a|². Computing ∫|∇×a|²
directly from the spinor:

| step | chiral-shear ∫|∇×a|² ratio | required | shortfall |
|---|---|---|---|
| Q1 → Q2 | **2.33** | 206.8 | ~89× too flat |
| Q2 → Q3 | **1.96** | 16.8 | ~9× too flat |

And ∫|∇×a|² / E₄ = 0.253, 0.251, 0.253 — **Q-independent** (the Mermin–Ho factor
¼). So the chiral-shear term *is* the Skyrme structure up to a constant; it scales
exactly as flatly. The huge coupling λ_⊥ = α⁻² ≈ 1.9×10⁴ multiplies every Q
equally — it sets the overall mass *scale* but leaves the Q-*scaling* at ~Q^{1.2}.
It cannot manufacture a ×207 step.

So all three energy structures that act on a bare texture — gradient (E₂),
Skyrme (E₄), chiral-shear (∫|∇×a|²) — are 1–2 orders of magnitude too flat. The
texture-energy route to the generation hierarchy is closed.

---

## Verdict and re-prioritisation

- **The geometry/quantum-number side works** (G1a, G1b clean). The CP¹ Hopf sector
  really does supply discrete, electric-charge-preserving, EM-unradiatable labels —
  the qualitative profile the idea was reaching for.
- **The energetics side fails hard at baseline** (G3). No standard soliton
  functional makes states whose energies span ×207 in one step.

Every **texture-energy** structure (gradient, Skyrme, chiral-shear) is closed:
none scales steeper than ~Q^{1.6}, against the ~Q⁷ the masses demand. The
"SSV ≠ Faddeev–Niemi" hatch is shut — the chiral-shear term is the Skyrme
structure up to the constant ¼.

### Gate 3′ — the saturation / log-potential sector: **FAIL**

This was the last surviving route and the original physical picture ("load
energy into a confined core; the saturated vacuum resists"). Test
(`hopf_saturation_relax.py`): write Ψ = A·z, hold the Hopf texture z fixed, and
**relax the amplitude** A by imaginary-time flow under the full LogSE energy
½[(∇A)² + A²|∂z|²] + ½(A² ln A² − A² + 1). The texture forces a core notch and
the log-potential pays for it.

| Q | A_min (core depth) | E_pot (saturation) | E_total |
|---|---|---|---|
| 1 | 0.223 | 46.0 | 303.9 |
| 2 | 0.090 | 115.6 | 462.3 |
| 3 | 0.042 | 190.0 | 585.2 |

The mechanism is genuinely engaged — the core depletes deeper at higher Q
(A_min 0.22 → 0.09 → 0.04). But the energy step is **E(Q2)/E(Q1) = 1.52**
(grid-stable: 1.63 at N=64, 1.52 at N=96, drifting *away* from the target with
refinement) — ~136× too flat. Even the saturation-only piece (E_pot) steps just
×2.5. Decision rule (step stays O(1)) → **the energetic hierarchy is
unreachable.**

### Combined test — were the sectors only tested separately?

A fair objection: Gates 3 evaluated E₂/E₄/chiral-shear on *fixed* ansätze, and
G3′ relaxed only the amplitude with the chiral-shear term *outside* the
minimised functional. Could combining them — in particular the dominant
λ_⊥ = α⁻² chiral-shear term *with* a varying amplitude — produce a steep step
that the separate tests miss?

No. Evaluating the chiral-shear current with the relaxed amplitude, j = ρ·a
(ρ = A²):

| step | chiral-shear, ρ varies (combined) | chiral-shear, ρ = 1 (separate) | required |
|---|---|---|---|
| Q1 → Q2 | **1.39** | 2.33 | 206.8 |
| Q2 → Q3 | **1.20** | 1.96 | 16.8 |

Coupling makes it **flatter**, not steeper: where the core depletes, the current
ρ·a is suppressed, so the combined step (×1.39) is *below* the separate one
(×2.33). This is the general rule — energies are additive, so a fixed-config
total ratio is bounded by the steepest term's ratio (≈ 2.3 even with λ_⊥
weighting all of it), and relaxing more degrees of freedom only lowers energies
toward the rigorously *sublinear* Faddeev minimum (Vakulenko–Kapitanskii
E ≳ Q^{3/4}). The combined, fully-relaxed result is therefore squeezed between a
flat ansatz ceiling and a sublinear floor — it cannot be Q⁷. Separate testing
was conservative.

**Root cause (why all four sectors fail together).** In a *static* topological
texture every energy term — gradient, Skyrme, chiral-shear, and the
log-potential's depletion response — is ultimately sourced by the texture
gradient |∂z|², which scales sublinearly (~Q^{0.1–0.75}). The log potential can
only *respond* by depleting ρ, and depletion is **bounded** (ρ ≥ 0 caps the
density at ½ per unit volume — the "saturation"). A bounded response cannot
amplify a ~Q^{0.7} source into a ~Q⁷ step. The unbounded branch (ρ ≫ ρ₀, the
balloon *overfilling*) is never reached by a static texture; accessing it needs
active driving, i.e. a non-stationary state — which is not a stable particle
(and the lifetime/quasiparticle cutoff that would govern such a state does not
naturally terminate at 3 either).

---

### Fully-coupled end-to-end relaxation — nailing it down

The combined checks above still relaxed at most one sector at a time. The
definitive test (`hopf_full_relax.py`) relaxes the **full complex spinor**
Ψ = (ψ₁, ψ₂) under the **complete** functional at once — gradient + chiral-shear
(λ_⊥/2)|∇×j|² + log-potential — by backtracking imaginary-time descent
(every accepted step strictly lowers E, so no spurious spikes), with the Hopf
charge **monitored, not constrained**, for Q = 1, 2, 3.

| Q | Q (initial) | Q (relaxed) | E (relaxed), λ_⊥=1 |
|---|---|---|---|
| 1 | −0.999 | −0.996 | 197.6 |
| 2 | −1.991 | −1.866 | 437.0 |
| 3 | −2.964 | −2.661 | 766.2 |

Two findings:

1. **The hopfion is stable.** Under true monotone descent the Hopf charge is
   preserved (it does *not* unwind to 0) — the chiral-shear quartic term plays
   the Skyrme role and Derrick-stabilises the texture, exactly as expected. (The
   apparent "collapse" in a naive explicit run was a numerical energy spike from
   the stiff quartic term, removed by backtracking.) So these are genuine stable
   topological objects, not transients.

2. **The coupled energy is flat.** E(Q2)/E(Q1) = **2.21**, E(Q3)/E(Q2) = 1.75 —
   ~94× too flat for the muon step. λ-invariance confirmed: the ratio is 2.21,
   2.11, 2.03 at λ_⊥ = 1, 2, 4, so the physical λ_⊥ = α⁻² (which only rescales
   size → ~α⁻¹ξ = R*, and overall scale) leaves the ratio ~2. The descent stalls
   partially (stiff term), but full convergence only *flattens* it further
   (Vakulenko–Kapitanskii forces the true minimum to ~Q^{3/4} = ×1.68), so 2.2 is
   an upper bound on the steepness.

This is the end-to-end confirmation: no separation artifact, no fixed-ansatz
crutch, Hopf charge dynamically preserved — and the hierarchy is still ~2 orders
of magnitude out of reach.

## Overall verdict: #115 closes **NEGATIVE** (directly confirmed)

**Gate 1 PASS / Gate 3 (all four energy sectors) FAIL.** CP¹ Hopf charge supplies
valid, discrete, electric-charge-preserving, EM-unradiatable topological *labels*
(exactly the profile the hypothesis wanted), **but it cannot source the lepton
mass hierarchy in any static sector.** No static CP¹ configuration makes Q = 1, 2,
3 differ by ×207, ×17 — the texture-gradient source is too flat and the
saturation response is bounded.

Because G3/G3′ are the binding constraint and fail, the texture-only gates parked
behind them — spin-statistics (rest of G1), selection-rule G2, neutrino G4 — are
**moot** (per the pre-registration). The 3D burst-threshold solver is **not**
built: it was gated behind a PASS here.

This is a clean negative that *strengthens* #99: not only is there no derived
generation mass, the most natural topological candidate (Hopf charge) is
**excluded as the mass mechanism** by a root-cause argument, not merely unproven.
Generations remain recorded coincidences. Reopening would now require structure
beyond *both* CP¹ and a static energy functional — e.g. a genuinely dynamical
(driven, non-stationary) state, which then faces the lifetime/quasiparticle
problem documented in the issue thread.

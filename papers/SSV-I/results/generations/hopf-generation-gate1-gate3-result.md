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

**The one surviving route is the amplitude / log-potential (saturation) sector —
which is exactly the original physical picture** ("load energy into a confined
core; the saturated vacuum resists"). That sector is *not* tested here: every
energy above holds ρ = ρ₀ fixed. The mass of a loaded core could instead live in
the LogSE saturation term b(ρ ln ρ − ρ + 1) when the amplitude is driven away
from ρ₀ at the core, with the Hopf charge acting only as the discrete, pinning
*label* (not the energy source). The next gate is therefore:

> **G3′ (saturation):** relax ρ (not just the texture) for the Q = 1, 2, 3
> hopfions under the full LogSE + chiral-shear functional. Does the log-potential
> energy of a Hopf-pinned core scale steeply enough to span ×207? Decision rule:
> step ≳ ×50 and grid-stable → the saturation route is viable; step stays O(1) →
> the energetic hierarchy is unreachable and #115 closes negative.

The texture-only gates (spin-statistics part of G1, selection-rule G2, neutrino
G4) stay **behind** G3′: if the saturation sector cannot carry the hierarchy,
they are moot.

Status of the generation claim is **unchanged** by this pass: generations remain
recorded coincidences (#99). #115 stays open on the saturation-sector energetics
(G3′) only.

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

---

## Verdict and re-prioritisation

- **The geometry/quantum-number side works** (G1a, G1b clean). The CP¹ Hopf sector
  really does supply discrete, electric-charge-preserving, EM-unradiatable labels —
  the qualitative profile the idea was reaching for.
- **The energetics side fails hard at baseline** (G3). No standard soliton
  functional makes states whose energies span ×207 in one step.

The hypothesis is **not dead outright**, because SSV's action is *not*
Faddeev–Niemi — its chiral-shear term (λ_⊥/2)|∇×j|², λ_⊥ = α⁻², is a different
operator. But the burden is now sharply located and heavy: **the SSV chiral-shear
energy would have to scale like ~Q⁷**, which is unlike any known soliton. Per
rule 1, that is a strong negative signal, recorded as such.

**Re-ordering of the remaining gates:** because G3 is the binding constraint and
is failing, the next step is **not** the harder spin-statistics computation (G1)
nor a 3D burst-threshold solver. It is the cheap analytic question: *can the
chiral-shear functional |∇×j|² on a Hopf texture scale steeply enough at all?* If
it cannot approach ~Q⁷, #115 closes negative and the spin-statistics, selection-rule
(G2), and neutrino (G4) gates are moot. If it can, they come back into play.

Status of the generation claim is **unchanged** by this pass: generations remain
recorded coincidences (#99). #115 stays open on the chiral-shear energetics
question only.

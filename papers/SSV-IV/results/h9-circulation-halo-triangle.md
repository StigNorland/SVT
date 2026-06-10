# Issue #119 H9 — the circulation-halo G triangle vs the BTFR

**Status: FALSIFIED on both pre-registered decision rules.** The route to
Newton's constant through the intrinsic circulation halo with the *natural
chain* (medium circulation locked to the baryons' angular momentum via the
Fall relation) fails by ~35 orders of magnitude on rule (a) and predicts
BTFR slope 3/2 instead of 4 on rule (b). Per repository rule 1 this negative
is the result; it is reported without softening.

Pre-registered in issue
[#119](https://github.com/StigNorland/SVT/issues/119) (owner's H9 comment;
operational execution plan posted before computing). Script:
`instruments/paper_iv/h9_circulation_halo_triangle.py`; receipt:
`papers/SSV-IV/results/h9_triangle_receipt.json`; tests:
`instruments/test/paper_iv/test_h9_circulation_halo_triangle.py` (7 tests,
incl. a numerical pin of the Poisson factor and robustness of the verdicts
to ±50% Fall / ±30% BTFR normalisation).

## Setup

- Halo energy density (H7a/H8 measured form): e(r) = ρ₀Γ²/(8π²r²).
- Poisson source (reading b): ∇²Φ = 4πG e/c² ⇒ **v_flat² = Gρ₀Γ²/(2πc²)**
  (factor verified by direct numerical integration in the test).
- Natural chain: Γ(M) = 2π·j_b(M), Fall form J ∝ M^{5/3}
  (j(10¹¹ M_sun) = 2.0×10³ kpc km/s).
- Anchors: BTFR M_b = 47·v⁴ M_sun (McGaugh 2012; free-fit slope 3.98±0.06);
  reference point M_b = 6×10¹⁰ M_sun ⇒ v = 189 km/s.
- Primary saturation dials: ρ₀ = m_p/a_p³ = 1.80×10²⁰ kg/m³ (grain Compton
  packing), m₀ = m_p.

## Rule (a) — magnitude: **FAIL**

Solving the triangle for G at the reference point:

| ρ₀ dial | G solved (m³ kg⁻¹ s⁻²) | α_G solved | orders off target |
|---|---|---|---|
| grain m_p/a_p³ (primary) | 1.48×10⁻⁴⁵ | 1.30×10⁻⁷³ | **−34.7** |
| Planck (Sakharov corner) | 5.1×10⁻¹²² | 4.6×10⁻¹⁵⁰ | −111 |
| nuclear saturation (reference) | 1.15×10⁻⁴² | 1.02×10⁻⁷⁰ | −31.8 |

The pre-registered window was 10^±2 around α_G = 5.9×10⁻³⁹. Every
saturation dial misses by ≥ 30 orders, in the **opposite direction from the
Sakharov overshoot**: the baryon-locked circulation in a saturation-density
medium is so energetic that observed rotation curves require G to be ~35
orders *weaker* than Newton's. Equivalently, with the real G the natural
chain overshoots observed v_flat by ~17 orders (in Γ). The verdict is
robust: it survives ±50% in the Fall normalisation and ±30% in the BTFR
normalisation simultaneously (tested), and no choice of m₀ rescues it (Γ is
set by j, not by the quantum).

## Rule (b) — slope: **FAIL**

v² ∝ Γ² ∝ M^{2β} ⇒ M_b ∝ v^{1/β}:

| chain | β = d ln j/d ln M | implied BTFR slope | observed |
|---|---|---|---|
| pre-registered J ∝ M^{5/3} | 2/3 | **1.50** | 3.98 ± 0.06 |
| empirical Fall j ∝ M^{0.55} | 0.55 | 1.82 | 3.98 ± 0.06 |

Inverse requirement: BTFR slope 4 forces Γ ∝ M^{1/4}, i.e. **J ∝ M^{5/4}**
— an exponent gap of 5/3 − 5/4 = 0.42 from the Fall relation. No
normalisation freedom can absorb an exponent.

## Inversions (what a surviving mechanism would have to deliver)

With real G and grain ρ₀, matching the reference point needs
Γ_req = 1.30×10⁹ m²/s — a factor **2.1×10¹⁷ smaller** than the baryon
circulation 2πj. That corresponds to N_req ≈ 3.3×10¹⁵ quanta of h/m_p
(1.8×10¹² of h/m_e), a medium flow velocity of ~7×10⁻¹³ m/s at 10 kpc, and
a halo mass-equivalent density there of ~4.5×10⁻²² kg/m³ (the right DM-halo
order, by construction). Alternatively, keeping the Fall chain requires
ρ₀ = 4.0×10⁻¹⁵ kg/m³ — no SSV saturation scale sits there.

## Standing of the surrounding results

- **Unaffected:** H7a/H8 (the intrinsic two-term source — core + ℓ²ρ/2r²
  circulation halo + Bernoulli time-dilation tail — measured in the LogSE
  medium). That is a property of defects in the medium and stands.
- **Falsified:** the *G-from-the-triangle* route on the natural
  baryon-locked chain, including its BTFR corollary. With #98 closed
  (Q_p route divergent) and the Phase-1/2 mutual-radiation G derivation
  dead, **SSV currently has no live derivation of G's magnitude**; α_G
  remains an input and the 39-order hierarchy problem is fully exposed.
- **Sharpened discriminator:** any future entrainment law must produce
  Γ ∝ M^{1/4} with the ~10⁻¹⁷ suppression above — and must still address
  dispersion-supported dSphs (barely rotating, DM-dominated), which remain
  the standing falsification exposure of any circulation-sourced halo
  phenomenology.

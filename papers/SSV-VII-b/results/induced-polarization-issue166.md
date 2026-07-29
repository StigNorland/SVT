# Issue #166 sub-calculation 3 — the induced gravitational polarisation

> **CORRECTION — sub-calculations 5–6.** The identification `m=1/xi` is invalid
> for corrected SSV, whose quadratic branch is gapless. The positive
> `dc2/dm²` lattice fit below survives as a massive-scalar control, but it is not
> a derivation of `1/G ∝ 1/xi²`; the seagull, covariant regulator and explicit
> screen-to-metric map are also absent. The “screen scale sets G” interpretation
> is retracted.

**Original status (superseded): the fix HOLDS (positive, honestly scoped).** Reading the screen as
*matter one integrates out* (Sakharov induced gravity — the correct reading for
a superfluid whose metric is induced, not fundamental), the short-range screen
stress **induces a positive-sign, local Einstein term whose Newton constant is
set by the screen scale**: `1/16πG ∝ +1/ξ²`. The graviton stays **massless by
diffeomorphism invariance** (a symmetry theorem, whose precondition — a conserved
screen stress — is already verified). So sub-calc 2's short-range finding is a
**feature** (it makes the induced action *local*), not the death-knell it was
first read as. This **overturns the "R2-leaning / massive graviton" reading** of
sub-calc 2 and re-opens R1.

Pre-registered (and amended) on
[#166](https://github.com/StigNorland/SVT/issues/166) before the computation.
Script `instruments/model_screen/induced_polarization.py`; tests
`instruments/test/model_screen/test_induced_polarization.py` (7); receipt
`induced_polarization_receipt.json`.

## The correction that motivated this (rule 1 cuts both ways)

Sub-calc 2 measured the screen's *own* stress correlator `⟨τ τ⟩`, found it
Yukawa (range ξ), and inferred "→ massive/short-range **bulk** mode." That step
silently used the **membrane-paradigm** reading (screen stress = graviton
boundary value, so its range is the graviton's range). For an *induced* metric
the logic reverses:

- the screen is integrated out; `⟨τ τ⟩(k)` is the **polarisation** generating
  the metric kinetic term `Γ[g] = ∫√g (Λ + R/16πG + …)`;
- the induced graviton is **massless** because `Γ[g]` is diff-invariant — an
  `m²h²` term is not, so it cannot be generated. **ξ sets G, not the range.**
- a **gap** (short-range `⟨τ τ⟩`) is exactly what makes the derivative expansion
  `Λ + R/16πG + …` *local*. Short-range stress ⇒ **local** gravity.

## What is and is not claimed (amended pre-registration)

`⟨TT⟩` alone omits the **seagull/contact** term `⟨δT/δg⟩` (2nd metric
variation), so the raw intercept `Π₂(0)` is **not** the graviton mass — even a
*massless* screen has `Σₓ⟨T₁₂T₁₂⟩ ≠ 0`. Masslessness is therefore a **symmetry
theorem**, not a number read off the lattice. The contact/seagull pieces are
**analytic** in `k`; the contact-robust content is the *non-analytic* structure
and the *mass-scaling* of the form factor. So this note claims only the
**existence, sign, locality, and ξ-scaling** of the induced Einstein term — not
its absolute `1/G` (which needs the physical cutoff `= 1/ξ` and the seagull;
deferred).

## Method

Free scalar, `D = 4` Euclidean lattice, minimal `T₁₂ = ∂₁φ ∂₂φ`. With momentum
along axis 0, `k = (k₀,0,0,0)`, the `{1,2}` plane is transverse to `k` and `h₁₂`
is a pure transverse-traceless graviton polarisation (θ₁₂ = 0 on these grid
points → **no spin-0 contamination**). The spin-2 form factor is

    Π₂(k₀) = 2·FFT[C₁₂₁₂](k₀,0,0,0),   C₁₂₁₂(x) = W₁₁W₂₂ + W₁₂²,
    W_ab(x) = ⟨∂_aφ(x)∂_bφ(0)⟩ = IFFT[sin k_a sin k_b · G(k)],
    G(k) = 1/(m² + Σ 4 sin²(k/2)).

Fit `Π₂(k) = c₀ + c₂k² + c₄k⁴` at small `k`, then isolate the physical part:
the raw `c₂(m)` is dominated by an `m`-independent lattice-cutoff contact piece
(`~1/a²`), so fit `c₂(m) = A + B m²`. `A` is the (unphysical, `a`-scale) cutoff;
`B = dc₂/dm²` drops the `m`-independent `A` and is the **cutoff-independent,
sign-robust** physical response — the induced `1/16πG` per unit `1/ξ²`.

## Positive controls (all pass)

| control | result | meaning |
|---|---|---|
| **C1** Ward (precondition) | `∂·τ/τ = 7.1×10⁻⁷` | separated `⟨TT⟩` transverse → masslessness-by-symmetry has its precondition |
| **C3** slope recovery | `ĉ₂ = 0.5000` (true `0.5`) | the polynomial fit recovers a **known** `k²` slope → a nonzero `c₂` is trusted |
| locality | massive `⟨TT⟩(x)` tail rate `= 1.30 > 0` | the massive stress is **exponentially short-range** → the induced action is *local* |

## Result

Raw `c₂(m)` is nearly flat in `m` (the `m²` part is only ~8 % of the cutoff
piece) — cutoff-dominated, so its raw (negative) value is **not** physical.
Isolating the screen-scale part:

| quantity | value | reading |
|---|---|---|
| `A` (lattice-cutoff contact) | `−0.00608` | unphysical (`a`-scale); subtracted |
| `B = dc₂/dm²` (physical) | **`+0.00253`** | **positive** induced `1/16πG` per `1/ξ²` |
| `R²` (linear in `m²`) | **`0.99906`** | `c₂` **∝ m²** → `1/G ∝ 1/ξ²` |
| `B` at `L = 40 / 48 / 56` | `+0.00253` (identical) | **L-converged** → physical, not finite-size |

So the induced Einstein coefficient's screen-scale part is **positive** (healthy
sign, no ghost) and scales as **`m² = 1/ξ²`** — Newton's constant is *set by the
screen scale ξ*, cleanly (`R² = 0.999`) and stably across lattice size.

## Verdict (against the amended #166 rule)

- **T1′ (locality): PASS.** The massive screen's `⟨TT⟩` is exponentially
  short-range and `Π₂(k)` is analytic (polynomial, residual `~10⁻⁶`) → the
  induced gravitational action is **local**. Short-range stress ⇒ local gravity.
- **T2 (Einstein term induced): PASS, positive.** `B = dc₂/dm² > 0`, `∝ m²`,
  L-stable → a genuine, healthy-sign `∫R` term is induced, with `1/G ∝ 1/ξ²`.
- **Masslessness:** by diff-invariance (theorem); precondition (conserved stress)
  verified. **Not** read off the contaminated intercept.

**Net:** short-range screen stress → **long-range** (massless-by-symmetry),
**local**, **positive-G** induced gravity, with G *set by ξ*. The programme is
still in the race — sub-calc 2's pessimistic reading is corrected.

## Honesty items and scope (rule 1)

- **Absolute `1/G` is deferred.** I isolate only the ξ-scaling coefficient `B`
  (sign + `m²` law). The absolute `1/16πG` mixes in the lattice-cutoff piece `A`
  and the seagull; getting it needs the physical cutoff `= 1/ξ` and the second
  metric variation. So "ξ *sets* G" is shown at the level of the **scaling and
  sign**, not a pinned number — consistent with the programme's standing pattern
  (forms/scalings are cheap; the absolute constant is the hard, deferred part).
- **Masslessness is symmetry, not measured.** The lattice intercept `Π₂(0)` is a
  seagull-cancelled contact term; I explicitly do **not** claim a numerical
  `m_graviton = 0`. The claim rests on diff-invariance + the verified conserved
  stress.
- **Sign robustness.** `B = dc₂/dm²` is a derivative of the polarisation w.r.t.
  the physical mass, so the `m`-independent cutoff `A` drops out and `B`'s sign
  is scheme-robust — but the *total* graviton kinetic coefficient (`A + Bm²`) is
  negative on this lattice because `A` (unphysical, `a`-scale) dominates; the
  physical statement is only about the ξ-response `B`, evaluated with cutoff
  `= 1/ξ` in the real theory.
- **Remaining R1 item.** "Does the bulk TT response *follow from the screen
  state* (not imposed as in #162)" is still untouched. This note shows the screen
  *induces* the right structure; the reconstruction direction is the next probe.

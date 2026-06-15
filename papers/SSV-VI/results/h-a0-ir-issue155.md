# H-A0-IR — the IR acceleration scale a₀ = cH₀/2π and the duality over-constraint, as a coefficient-consistency test (issue #155)

**Status: R1 — the cosmological a₀ is consistent with cH₀/2π using the *same*
Gibbons–Hawking/Unruh 2π that S1/S2 fixed for local horizons, and the c²√Λ
holographic branch is excluded (8×). So the local and cosmological screens share
one thermodynamics: the duality **survives its falsifier**, and the weak
G-derivation's promissory falsifier (b) is **discharged from promissory to
survived (not confirmed)**. Honest bars, all at full strength (rule 1): the a₀
*magnitude* is a conceded input (P₀→Λ→H₀, SSV-VIII), only the coefficient is
derived; 1/2π vs 1/6 is **not** decisively separable from SPARC (0.065σ); the
decisive cH-vs-√Λ separation is the z-evolution falsifier, which needs high-z
data; the cored amplitude is post-hoc (#146 A4). With S1+S2+H-A0-IR the *form*
half of Option D is complete and internally consistent, with every magnitude
(G, Λ/H₀) an honest conceded input.**

Pre-registered on issue [#155](https://github.com/StigNorland/SVT/issues/155)
(the coefficient-consistency framing, the candidate table, the discrimination-
power and z-falsifier designs, and the R1/R2 rules posted as a comment *before
computing*, rule 6). Owner's framing call: coefficient-consistency, not a literal
three-G-magnitude match. Script `instruments/paper_vi/a0_overconstraint.py`;
receipt `papers/SSV-VI/results/a0_overconstraint_receipt.json`; figure
`papers/SSV-VI/figures/a0_overconstraint.png`; tests
`instruments/test/paper_vi/test_a0_overconstraint.py` (6, incl. negative
capability). Builds on the #146 measurement (`a0_from_vh.py`,
[a0-target-issue146](a0-target-issue146.md)).

## Why coefficient-consistency, not three G's (non-circularity, recorded)

The over-constraint was pre-registered as "the same G must fit η, a₀=cH₀/2π, and
a_p/ℓ_P." But (i) `a_p/ℓ_P` is the **#122 circular identity**
(`(a_p/ℓ_P)²=1/α_G`, guarded, not a derivation), and (ii) SSV-VIII concedes the
a₀ **magnitude**: `Λ=(8πG/c²)(P₀/ρ₀c²)` with the absolute saturation pressure
`P₀(ρ₀)` an **undetermined input** ("a numerical Λ would require one new
theoretical input"), exactly as G's magnitude is conceded (D-b, #154). With two
conceded magnitudes plus a circular identity, a literal three-G match has no
teeth. The teeth are in the **dimensionless coefficient** `a₀/(cH₀)`, which must
equal the de Sitter Gibbons–Hawking `1/2π` — the *same* 2π S1 used in
`kT_H = ħg_H/(2πc)`.

## The derivation

`a₀ = c·f_dS`, with `f_dS = H₀/2π` the de Sitter (Hubble) horizon's
Gibbons–Hawking thermal frequency — the cosmological-horizon instance of S1's
local `kT_H = ħg_H/(2πc)` (identical Unruh/GH 2π; Visser's acoustic-metric
construction applied to the de Sitter horizon). So **`a₀ = cH₀/2π`**. The
magnitude (`H₀`, via `P₀→Λ`) is conceded; only the coefficient `1/2π` is derived.

## The over-constraint (vs the #146 measured cored a₀ = 1.13×10⁻¹⁰, σ≈0.31 dex)

| candidate | a₀ form | ratio measured/pred (H₀=73 / 67.4) | reading |
|---|---|---|---|
| **GH-2π (SSV)** | `cH₀/2π` | **0.999 / 1.082** | consistent, same 2π as S1/S2 |
| Verlinde | `cH₀/6` | 0.954 / 1.034 | within the scatter — not separable |
| equipartition | `cH₀` | 0.159 / 0.172 | off by ~2π (excluded) |
| de Sitter √Λ | `c²√Λ` | **0.120** | **off by 8.4× (excluded)** |

- **GH-2π consistent** across the H₀ tension (ratio in [0.85, 1.15]).
- **c²√Λ excluded** (8.4× too large) — a clean negative killing the
  cosmological-constant holographic branch.
- **1/2π vs 1/6 not decisively separated:** the two cH coefficients differ by
  `6/2π = 0.955` (0.020 dex), far below the measurement scatter (~0.31 dex);
  the σ-separation is **0.065σ**, and the H₀ tension alone shifts the cH anchor
  by 0.035 dex (> the 1/2π-vs-1/6 gap). SPARC cannot choose between them.
- **The decisive separator is the z-evolution falsifier** (re-pinned from #146
  A4): the cH branch predicts a BTFR normalization shift
  `Δlog M = log[H(z)/H₀]` = **0.121 / 0.253 / 0.482 dex** at z = 0.5 / 1 / 2
  (flat ΛCDM, Ω_m=0.315); the √Λ branch predicts **0**. This is what
  distinguishes the branches — and it needs high-z rotation-curve data not yet
  in hand.

## Verdict: R1 (the duality survives its falsifier) — read honestly

The over-constraint **could** have falsified the whole duality: had the measured
a₀ landed on the √Λ form, or far from any cH-form, the local screens (S1/S2,
GH-2π) and the cosmological screen would have carried inconsistent
thermodynamics. It did not — a₀ sits on `cH₀/2π` with the same 2π. So:

- the **c²√Λ branch is a clean negative** (excluded);
- the weak G-derivation's falsifier (b) — "the same thermodynamics must fit the
  local η and the cosmological a₀" — is **discharged from promissory to
  survived**;
- but **survived, not confirmed**: 1/2π vs 1/6 is undecidable from SPARC, the
  magnitude is conceded input, and the decisive test (cH vs √Λ) awaits high-z
  data. Per rule 1, a surviving consistency check is suggestive, not proof.

The instrument's R1 is shown reachable-to-R2: `test_negative_capability_…`
confirms that an a₀ equal to the √Λ prediction would fall outside the
consistency band → R2.

## Consequences (applied this branch)

- **SSV-VI §SPARC**: a new resultbox — the deep-MOND a₀ (the constant-v_h halo,
  #146) is read as `a₀ = cH₀/2π` from the de Sitter Gibbons–Hawking frequency
  (the same 2π as SSV-V S1/S2), with the over-constraint verdict (√Λ excluded;
  1/2π-vs-1/6 not separable; z-falsifier re-pinned) and the conceded magnitude.
- **Claim-status (rule 5):** "a₀ = cH₀/2π coefficient from the cosmological
  horizon" → **derived (coefficient, consistency-survived)**; "a₀ magnitude
  (H₀/Λ via P₀)" → **conceded input** (SSV-VIII gapbox); "c²√Λ form" →
  **falsified**.
- **Open problems**: the decisive cH-vs-√Λ z-evolution test (high-z BTFR) and
  the P₀(ρ₀) saturation-pressure derivation (the a₀/Λ magnitude) are the live
  handles.

## Status

#155 H-A0-IR resolves the cosmological/IR half: **R1**, the duality survives its
coefficient-consistency falsifier; √Λ excluded; magnitude conceded; decisive test
pinned to high-z. **With S1 + S2 + H-A0-IR the form half of Option D (#154) is
complete** — local-horizon area-law and surface gravity, and the cosmological a₀,
all governed by one holographic thermodynamics (area-law 1/4, Unruh/GH 2π), with
every magnitude (G, Λ/H₀) an honest conceded input. See
[h-eos-s2-issue155](../../SSV-V/results/h-eos-s2-issue155.md),
[h-eos-s1-issue155](../../SSV-V/results/h-eos-s1-issue155.md),
[a0-target-issue146](a0-target-issue146.md), and
[project-holographic-screen-bridge].

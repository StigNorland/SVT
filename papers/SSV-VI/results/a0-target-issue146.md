# H-A0 S0 — the measured acceleration scale (issue #146)

**Date:** 2026-06-12 · **Branch:** `issue-146-a0-target` · **Instrument:**
`instruments/paper_vi/a0_from_vh.py` · **Receipt:**
`papers/SSV-VI/results/a0_target_receipt.json` · **Pre-registration:** issue
#146 (rules A1–A4 fixed before computing).

Measurement side of the #129 item-1 reframe: convert the frozen #133/#136
per-galaxy halo amplitudes into the acceleration-scale form and pin the
target any future H-A0 derivation must hit. No new fitting against rotation
curves; inputs are `sparc_per_galaxy_results.csv` only.

## The deep-limit identity (S0-analytic)

The SSV halo model fits v² = v_bar² + v_h² with constant v_h. MOND with the
simple/RAR interpolation has g = g_N + √(g_N·a₀); the extra term contributes
v_extra²(r) = √(g_N a₀)·r = √(G M_bar a₀) — constant in r. So the
constant-v_h form *is* the deep-MOND tail with

> a₀,h ≡ v_h⁴ / (G·M_bar),

the same a₀ as the RAR convention. The per-galaxy a₀,h therefore maps
convention-free onto the literature scale, with one recorded bias: v_h is
fitted over *all* radii, so a shape that misfits the inner curve (the
falsified no-core form, #133 rules a/b) drags the amplitude away from the
true outer tail. Both amplitudes are reported side by side per rule A4.

## Results

| tier × amplitude | n used / in tier | log₁₀ a₀ median [16%, 84%] | a₀ (m/s²) | slope log a₀ vs log M | equiv. BTFR slope |
|---|---|---|---|---|---|
| primary, no-core | 83/83 | −10.435 [−11.100, −10.027] | 3.67×10⁻¹¹ | +0.024 [−0.117, +0.175] | 3.90 |
| **primary, cored** | **81/83** | **−9.948 [−10.229, −9.611]** | **1.13×10⁻¹⁰** | **−0.095 [−0.185, −0.004]** | **4.42** |
| Q≤2, no-core | 161/163 | −10.487 | 3.26×10⁻¹¹ | +0.125 | 3.55 |
| Q≤2, cored | 157/163 | −9.942 | 1.14×10⁻¹⁰ | −0.116 | 4.53 |
| all, no-core | 170/175 | −10.530 | 2.95×10⁻¹¹ | +0.172 | 3.41 |
| all, cored | 166/175 | −9.949 | 1.12×10⁻¹⁰ | −0.038 | 4.16 |

Exclusions (all 175, cored): 2 with v_h = 0, 4 with r_c at the 50 kpc fit
bound, 3 with v_h at the 500 km/s bound — degenerate fits, counted, never
silent. Tier note: "Q≤2" here is the plain quality cut (163 galaxies), not
#136's 115-galaxy middle tier (which also kept the i/N cuts); the decisive
tier (primary, 83) is identical to #133's.

## Rules

- **A1 (constancy): PASS on the decisive tier, both amplitudes** (no-core
  +0.024, cored −0.095; both |slope| ≤ 0.10). Honesty items: the cored
  bootstrap CI [−0.185, −0.004] *marginally excludes zero* — a weak
  anti-trend (more massive galaxies prefer slightly smaller a₀), recorded,
  to be watched at the looser tiers where it reappears (−0.116 at Q≤2)
  alongside the *opposite*-signed no-core trends (+0.125, +0.172). Signs
  disagreeing between amplitudes across tiers reads as shape-systematics,
  not a coherent mass trend; it is not hidden either way.
- **A2 (the target):** the no-core/cored medians differ by **0.487 dex**
  > 0.3, so per rule A4 the wide window applies:
  > **log₁₀ a₀ ∈ [−11.100, −9.611]** (window covering both amplitudes'
  > 68% intervals), headline (cored, post-hoc-flagged) median
  > **a₀ = 1.13×10⁻¹⁰ m/s²**.
  Any future H-A0 derivation passes only inside this window (supersedes
  "order-unity of 1.2×10⁻¹⁰"). The cored form's post-hoc flag propagates to
  the target's status until the #133 r_c promotion condition is met.
- **A3 (anchors — none declared hit, per the guard):**

  | anchor | value (m/s²) | cored median / anchor | no-core median / anchor |
  |---|---|---|---|
  | cH₀/2π, H₀ = 67.4 | 1.042×10⁻¹⁰ | 1.082 | 0.352 |
  | cH₀/2π, H₀ = 73.0 | 1.129×10⁻¹⁰ | 0.999 | 0.325 |
  | c²√Λ | 9.427×10⁻¹⁰ | 0.120 | 0.039 |
  | RAR (literature) | 1.200×10⁻¹⁰ | 0.940 | 0.306 |

  Recorded without declaration: the cored amplitude sits within 8% of
  cH₀/2π and within 6% of the RAR scale; c²√Λ overshoots it by ~8×. A
  derivation must declare its anchor *in advance* against this table.
- **A4:** wide window applied (see A2); the 0.49 dex no-core/cored spread is
  the headline systematic of this measurement.

## Redshift falsifiers (pinned; flat ΛCDM, Ω_m = 0.315)

| z | H(z)/H₀ | cH-anchor Δlog₁₀M | √Λ-anchor Δlog₁₀M |
|---|---|---|---|
| 0.5 | 1.32 | +0.121 | 0 |
| 1.0 | 1.79 | +0.253 | 0 |
| 2.0 | 3.03 | +0.482 | 0 |

A cH-anchored derivation predicts the BTFR normalization rises ~0.5 dex by
z = 2; a √Λ-anchored one predicts no evolution. Anchors cannot be swapped
after a high-z measurement.

## Status

Constraint-pricing run: no claim changes status. The open #129 item 1 now
has a measured target window instead of a literature value. The result and
this note are cross-posted on #146 and #129.

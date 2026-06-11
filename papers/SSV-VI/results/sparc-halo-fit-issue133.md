# Issue #133 — SPARC multi-galaxy test of the SSV circulation halo

**Status: the pre-registered pure (no-core) constant-v_h² form is
FALSIFIED on rules (a) and (b); the BTFR-equivalent amplitude scaling of
rule (c) PASSES with a parameter-free exponent match (v_h ∝
M_bar^0.256±0.019 vs the predicted 0.25, scatter 0.14 dex). A flagged
post-hoc exploration shows the entire (a)/(b) failure is the core
extrapolation: rolling the halo off below a core radius (median r_c ≈
4.3 kpc) gives median reduced χ² = 0.89 and beats NFW by BIC in 76% of
galaxies at equal parameter count. Per rule 1 the falsification of the
pure form is the headline; the rule-(c) pass and the post-hoc repair are
suggestive and flagged respectively.**

Pre-registered in issue
[#133](https://github.com/StigNorland/SVT/issues/133) (protocol posted
before computing). Script: `instruments/paper_vi/sparc_halo_fit.py`;
receipt `sparc_halo_fit_receipt.json`; tests
`instruments/test/paper_vi/test_sparc_halo_fit.py` (6, incl. headline
pins); figures `fig_sparc_montage.png`, `fig_sparc_vh_mbar.png`,
`fig_sparc_residual_quintiles.png`.

## Data and sample

SPARC (Lelli, McGaugh & Schombert 2016, AJ 152, 157): 175 galaxies, 3391
rotation-curve points with the baryonic decomposition (V_gas with helium,
V_disk and V_bul at M/L = 1 [3.6 µm]). Official MRT files cached under
`papers/SSV-VI/data/SPARC/`. Provenance: the battery first ran on a
public vendored copy (astroweb.cwru.edu was unreachable from the
analysis machine), validated against the byte-by-byte headers,
galaxy/point counts, and spot values; the author subsequently downloaded
the official files directly (2026-06-11) and they are
**content-identical line by line** (3416 + 273 data/header lines) to the
copy used — the repo now carries the official downloads, and every
number in this note is unchanged.
**Primary sample (pre-registered): Q = 1, i ≥ 30°, ≥ 10 points → 83
galaxies.** Robustness: Q ≤ 2 → 115 galaxies (same verdicts; rule-(c)
slope 0.268).

## Models (identical fixed baryons: Υ_d = 0.5, Υ_b = 0.7)

| model | free params/galaxy | median reduced χ² (Q=1) |
|---|---|---|
| **SSV pure: v² = v_bar² + v_h²** | 1 | **14.47** |
| NFW halo | 2 | 1.64 |
| MOND/RAR (a₀ = 1.2×10⁻¹⁰ m/s² global) | 0 | 12.21 |
| Flynn & Cannaliato ω (arXiv:2601.00522) | 0 (endpoint-anchored) | **93.68** |
| *post hoc, flagged:* SSV cored, v_h²·r²/(r²+r_c²) | 2 | **0.89** |

## Rule (a) — competitiveness: **FAIL**

Median reduced χ² ratio SSV/NFW = 8.80 against the pre-registered
threshold 1.5; SSV wins by BIC in only 4% of galaxies. The pure form is
not competitive point-by-point.

## Rule (b) — residual structure: **FAIL, with a clean physical signature**

Median fractional residual (V_obs − V_model)/V_obs per quintile of
r/R_max: **−0.212**, −0.015, +0.040, +0.077, **+0.113** (threshold
±0.05). The model overshoots by 21% in the innermost quintile and
undershoots by 11% in the outermost: one constant v_h², applied at all
radii, is too strong where the measured halo's validity window never
reached (inside the core) and consequently fits too weak a value for the
outskirts. This is precisely the pre-flagged risk: H7a/H8 measured the
1/r² circulation-energy density *outside* the defect core; the pure form
extrapolated it to r → 0.

## Rule (c) — the v_h(M_bar) scaling: **PASS**

Over all 83 galaxies (every fit has v_h constrained away from zero):

> **log₁₀ v_h = (0.256 ± 0.019)·log₁₀ M_bar − 0.665, scatter 0.14 dex**

against the parameter-free BTFR-equivalent prediction slope **0.25**
(v_h ∝ M^{1/4} ⟺ M ∝ v⁴). At M_bar = 10¹⁰ M_sun this gives v_h ≈ 79
km/s. Robust at Q ≤ 2 (slope 0.268, 115 galaxies). **This is the
empirical curve the #129 entrainment law must produce** — measured, not
assumed. Per rule 1 this positive is suggestive, not proof; its sharpest
use is as the falsification target for any derived Γ(M).

## Post-hoc exploration (FLAGGED — not pre-registered)

Rolling the halo off below a core radius, v_h²·r²/(r² + r_c²)
(pseudo-isothermal form), with (v_h, r_c) free: median reduced χ² =
**0.89**; **BIC-beats NFW in 76% of galaxies at the same parameter
count**; r_c quartiles 2.5 / 4.3 / 7.0 kpc. The entire pre-registered
failure is therefore localised in the core region. This is recorded as
an exploration only. The pre-registerable follow-up it motivates: derive
the galactic defect's core scale from the medium (is r_c set by the
defect core, the baryon distribution, or neither?), pre-register an
r_c(galaxy) relation, and only then promote the cored form.

## Standing

- The **pure** constant-v_h² halo (the H7a/H8 measurement extrapolated
  through the core) is falsified on SPARC — recorded in Paper VI's
  claim-status table.
- The **asymptotic** content survives and sharpens: a constant outer
  v_h² with amplitude scaling as M_bar^{0.256±0.019} describes the
  population with 0.14 dex scatter.
- The Flynn ω velocity-addition model, whose paper motivated this run,
  is an order of magnitude worse than every dynamical model on
  error-weighted statistics (median reduced χ² ≈ 94).
- dSphs remain outside SPARC (rotation-supported sample) and remain the
  standing discriminator.

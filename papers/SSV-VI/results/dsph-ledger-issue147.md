# DSPH-LEDGER — the dwarf-spheroidal discriminator, run as a ledger (issue #147)

**Date:** 2026-06-12 · **Branch:** `issue-147-dsph-ledger` · **Instrument:**
`instruments/paper_vi/dsph_ledger.py` · **Receipt:**
`papers/SSV-VI/results/dsph_ledger_receipt.json` · **Figure:**
`papers/SSV-VI/figures/fig_dsph_ledger.png` · **Pre-registration:** issue
#147 (rules B1–B3 and all sweeps fixed before computing).

#129 item 3: dispersion-supported dwarfs barely rotate yet are DM-dominated
— the standing falsifier for circulation-sourced halo phenomenology,
inherited from H7a's corollary. Pinned data: the eight classical MW dSphs
(McConnachie 2012), Wolf estimator v_c(r₁/₂) = √3·σ_los, M_*/L_V = 1.6
(swept ×/÷2), v_rot ≤ 3 km/s (swept 1–10).

## The ledger (baseline settings)

| dwarf | M_* (M_☉) | v_h,obs | model A (mass law) | Δ_A | model B ≤ (rotation law) | Δ_B | σ_pred (universal core) | σ_obs |
|---|---|---|---|---|---|---|---|---|
| Fornax | 3.2×10⁷ | 18.4 | 18.0 | +0.01 | 0.080 | +2.36 | 6.2 | 11.7 |
| Leo I | 8.8×10⁶ | 14.1 | 13.0 | +0.03 | 0.028 | +2.70 | 4.5 | 9.2 |
| Sculptor | 3.7×10⁶ | 15.3 | 10.4 | +0.17 | 0.032 | +2.68 | 2.8 | 9.2 |
| Leo II | 1.2×10⁶ | 11.0 | 7.8 | +0.15 | 0.020 | +2.74 | 2.0 | 6.6 |
| Sextans | 7.0×10⁵ | 13.6 | 6.8 | +0.30 | 0.078 | +2.24 | 1.6 | 7.9 |
| Carina | 6.1×10⁵ | 11.3 | 6.5 | +0.24 | 0.028 | +2.60 | 1.3 | 6.6 |
| Ursa Minor | 4.6×10⁵ | 16.3 | 6.1 | +0.43 | 0.020 | +2.90 | 1.2 | 9.5 |
| Draco | 4.6×10⁵ | 15.7 | 6.1 | +0.41 | 0.025 | +2.80 | 1.1 | 9.1 |

(velocities in km/s; Δ in dex = log₁₀ v_h,obs/v_h,model)

## Verdicts (rules evaluated verbatim; all sweep-stable over 27 combinations)

- **B1 — rotation-proportional entrainment FALSIFIED.** Median Δ_B = +2.69
  dex ≥ 1.5 (the rotation law's *upper limits* miss by a factor ~500) while
  median Δ_A = +0.20 dex ≤ 0.5 (the dwarfs sit ON the mass law,
  extrapolated three decades below the SPARC sample). The halo amplitude
  reads baryonic **mass**, not baryonic **rotation**. Stable across M_*/L
  ×/÷2, v_rot limits 1–10 km/s, ±30% anisotropy.
- **B2 — the budget does NOT bind (recorded as demanded).** Even at
  v_rot = 1 km/s the dwarfs carry ≥ 10¹⁵ × the H9-inverted circulation
  requirement Γ_req(M). The naive "no rotation ⇒ no circulation budget"
  version of the dSph killer is wrong; the discriminator is B1's
  *correlation*, not the budget. (Exactly as pre-stated: the H9 inversion
  had already put Γ_req 17 orders below MW baryon circulation.)
- **B3 — a universal kpc-scale core FALSIFIED at dSph scales.** With
  r_c = 2.5 kpc (the SPARC lower quartile, most dwarf-favorable), 7/8
  dwarfs predict σ below half the observed value (threshold ≥ 6/8). The
  #133 promotion condition sharpens: any r_c(galaxy) relation must deliver
  r_c ≲ r₁/₂ ~ 0.2–0.9 kpc at dwarf scale — a single medium-set core
  length is dead; only a baryon-set core scale survives.

## Honesty items

1. The dwarfs sit systematically **above** the mass law (+0.20 dex median,
   +0.43 worst). They are MW satellites; the tidal confound was pre-stated.
   At face value: slightly *more* halo than the mass law predicts — the
   offset direction is *against* tidal stripping of the halo and within
   ~1.5× the relation's 0.14-dex scatter. Recorded, not interpreted.
2. Model B was normalized at the H9 MW reference (R = 15 kpc, v = 220 km/s).
   Any alternative normalization moves Δ_B by the same constant for all
   dwarfs; the 2.7-dex gap cannot be normalized away without breaking the
   SPARC spirals by the inverse factor.
3. These are satellite dwarfs; field dIrrs at the same M_bar (which rotate)
   would complete the rotation-independence argument from the other side —
   they are in SPARC's low-mass tail, which is exactly where the mass law
   was measured. The two-sided version is implicit in B1's construction.

## Consequence for the programme

What survives of "circulation sourcing" after #147 is only the variant in
which the galactic medium circulates *without* tracking the baryons'
rotation — entrainment as a collective property coupled to mass-energy.
Combined with the #129 solar-system scope limit (no per-star halo), the
mechanism space is pinched from both sides. The complementary medium-side
question — whether the bare medium's static far field can read mass-energy
at all — is the pre-registered extensivity battery #149.

Paper edits in this pass (rule 5): SSV-VI gains §"The dwarf-spheroidal
ledger" (two falsboxes + figure), three claim-status rows, the updated
gapbox sentence, and the resolved falsifiable-statement item.

# UV-GAUNTLET — the update ceiling and the grain vs the measured ultraviolet sky (issue #148)

**Date:** 2026-06-12 · **Branch:** `issue-148-uv-gauntlet` · **Instrument:**
`instruments/paper_iv/uv_gauntlet.py` · **Receipt:**
`papers/SSV-IV/results/uv_gauntlet_receipt.json` · **Pre-registration:**
issue #148 (formulas, bounds, and the ≥ 2-order rule fixed before
computing).

#129 items 5 and 6 — the two SSV-IV gapboxes from the Phase-3 rewrite —
converted from flags into numbers. Constraint-pricing run in the TOKEN-TAX
mold; per rule 1 these correctly-negative results are the success mode and
are recorded at full strength.

Pinned medium scales: a_p = ħ/(m_p c) = 2.103×10⁻¹⁶ m, E_grain = m_p c² =
0.938 GeV, N₀ = 1.4255×10²⁴ s⁻¹.

## Results

| confrontation | SSV (naive reading) | pinned bound / observation | margin | verdict |
|---|---|---|---|---|
| C1 ceiling vs photon frequency | E_max = ħN₀ = 0.94 GeV | LHAASO J2032+4127 1.42 PeV (Nature 594, 33); Crab 1.1 PeV (Science 373, 425); GRB 221009A 13 TeV (Science 380, 1390) | **+6.2 / +6.1 / +4.1 orders** | falsified-as-written |
| C2 Bogoliubov grain dispersion vs GRB TOF | effective E_QG,2 = 2·E_grain = 1.88 GeV (superluminal quadratic, δv/c = (3/8)(k·a_p)²) | E_QG,2 > 1.3×10¹¹ GeV (Vasileiou+ 2013, GRB 090510, 95% CL) | **+10.8 orders**; δv/c(31 GeV) = 409 — perturbative collapse | falsified-as-written |
| C3 superluminal photon decay | δ(1.42 PeV) = 8.6×10¹¹, k·a_p = 1.5×10⁶ | γ→e⁺e⁻ threshold δ_thr = 2.6×10⁻¹⁹; LHAASO E_LV ≥ 1.42×10²⁴ GeV (PRL 128, 051102) | **+30.5 orders above decay threshold** | falsified-as-written |
| C4 grain as scattering structure | 0.94 GeV / 2.1×10⁻¹⁶ m | LEP/LHC contact Λ ≳ 10 TeV; r_e ≲ 2×10⁻¹⁹ m (Bourilkov 2001) | **+4.0 (energy) / +3.0 (length) orders** | falsified-as-written |
| C5 lab Lorentz tests | predicted anisotropy 3.7×10⁻²¹ at optical k with CMB boost | Δc/c ≲ 10⁻¹⁸ (Nagel+ 2015) | **2.4 orders BELOW the bound** | **NOT excluded** — recorded plainly |

## What this means, precisely

1. **The single-mode-frequency reading of the ceiling N₀ is dead by ~6
   orders.** Survivor requirement S2: N₀, if retained, must move off the
   single-mode frequency axis (per-grain bandwidth shared across a
   delocalized mode), with a derivation that permits above-ceiling
   collective modes while still forbidding sub-grain wakes.
2. **The bare-medium photon (the #138 phase-channel Bogoliubov mode)
   cannot be the astrophysical photon without protection.** The
   quantum-pressure k⁴ term — *measured real* in the #138 magnon channel,
   present on the Bogoliubov branch by the same algebra — predicts
   superluminal dispersion excluded by 11 orders (TOF) and 30 orders
   (photon survival). Survivor requirement S1: the propagating phase
   channel must be exactly linear to ≲ 10⁻¹⁷ fractional dispersion out to
   ≥ 10⁶·E_grain. A Fermi-point/emergent-LI-class protection (Volovik) is
   now a **quantified derivation obligation on the #138 photon
   identification**, not a free pass. This makes #148 load-bearing for
   #138.
3. **The grain must not scatter** (S3): no form factor at GeV; the grain
   may appear only in defect statics (where #138 put α) and in update
   accounting.
4. **Honesty (pre-registered):** C2 and C3 price the same object at
   different energies — one kill stated twice, not two independent kills.
   And the laboratory does *not* exclude the grain (C5): resonator
   anisotropy at optical k is 2.4 orders too soft; the kill lives at
   TeV–PeV. A gauntlet that only recorded kills would be spin.

## Paper edits in this pass (rule 5)

Both SSV-IV gapboxes upgraded from qualitative flags to quantified
falsifiers with the survivor requirements verbatim ("Quantified (#148)"
boxes in §ceiling and §universal); the status-summary paragraph updated
accordingly. PDF rebuilt, provenance regenerated.

Not affected: the gravity-sector items (1–4) of #129 — this battery
touches only the UV/kinematics gapboxes. The deepest consequence is the
new quantified obligation on the photon identification (#138), which was
already flagged as the heaviest domino.

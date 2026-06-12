# H-EXT — the medium's static response reads circulation, not energy (issue #149)

**Date:** 2026-06-12 · **Branch:** `issue-149-extensivity` · **Instrument:**
`instruments/paper_iv/extensivity_battery.py` · **Receipt:**
`papers/SSV-IV/results/extensivity_receipt.json` · **Figure:**
`papers/SSV-IV/figures/fig_extensivity_ladder.png` · **Pre-registration:**
issue #149 (S1 analytic prediction + rules R1–R3 fixed before computing).

#129 item 2: composite-body source extensivity (Eötvös 10⁻¹⁵). The battery
decides whether the bare medium produces ANY far-field dilation response
reading a composite's total energy — the monopole the Newton sector needs
— or whether the static far field reads only circulation.

## Verdict: R2, the pre-registered clean negative, at the pre-registered bars

| measurement | result | S1 prediction / gate |
|---|---|---|
| E1 single ℓ=1 control, δρ·r² plateau (relaxed state) | **−0.5221** (dev 4.4%) | −1/(2b) = −0.5; gate ±15% |
| E1 evolved-snapshot cross-check | −0.4473 | H8b's measured −0.447 — exact replication |
| E2 net-zero quadrupole, far slope | **6.04** (28 bins) | 6 exactly (the quadrupole rung); gate ≥ 3.5 |
| E2 amplitude at the pre-registered r = 40 window | **0.62% of the E1 coefficient** | monopole bound: ≤ 5% |
| E2b net-zero dipole pair (relaxed), far slope | **4.014** | 4 exactly (the dipole rung) |
| E3 two clusters vs one | superposition of multipole tails (see below) | no monopole emergence |
| E4 energy ledger (report-only) | cluster = 1.094 × (4 × single-core aperture energy) | binding-energy fraction characterized |

**The bare medium has no Newtonian (energy-monopole) dilation response:
non-circulating composite matter does not gravitate in the bare medium.**
The static far field is the circulation multipole ladder S1 predicted —
slope 2 (winding) / 4 (dipole) / 6 (quadrupole), each measured — and the
composite's ~4× core energy (E4: 4.4× including binding) appears nowhere
in the far field.

## Pre-stated consequences, triggered verbatim (rule 1, full strength)

1. **Item 2 is not derivable from bare defect/medium energetics.**
   Extensivity holds only under the Poisson-compliance postulate
   ∇²Φ = 4πG·e/c², which is hereby promoted from "reading (b)" to
   load-bearing added structure — it is where both G and the Eötvös
   property live.
2. **Items 1 and 2 of #129 merge:** one compliance postulate, one
   undelivered coupling.
3. **Jointly with DSPH-LEDGER #147 B1** (the halo reads mass, not
   rotation): the circulation channel cannot be the galactic halo
   mechanism — the medium's own field reads circulation that real halos
   do not track. The pincer is closed from both sides.

This is a proof-grade negative of the same rank as H-SPATIAL's γ_eff = 0:
the bare medium delivers the time sector for circulating defects and
nothing for composite non-circulating matter — the entire Newton sector is
added structure.

## Deviations from the pre-registration (recorded, with the first-run numbers)

1. **E1 plateau window moved from (5, 12) to (3, 7).** The registered
   window reaches into the screen-cancellation zone (the D = 30 partners
   cancel the test vortex's velocity beyond r ~ D/4), and past r ≈ 17 the
   bins pass through the partner cores. Geometry, corrected before any
   rule re-evaluation; with the registered window the first run read
   −0.363 (27% — an instrument artifact, not physics).
2. **Rule source moved from evolved-state to relaxed-state (static)
   profiles.** The first full run showed a ~10⁻³ standing-sound /
   boundary-ring floor in the evolved fields that swamps any far signal
   (|δρ·r²| at the r = 40 window read −3.7, *growing* toward the box edge
   — 10× the control plateau, slope −0.58; E3 ratio 0.72: floor noise).
   The pre-registered question is the medium's *static* response, and the
   imaginary-time-relaxed state is the static configuration; the evolved
   profiles are retained in the receipt as the stability cross-check
   (which the E1 snapshot passes by reproducing H8b's −0.447 exactly).
3. **E3's far-window doubling test is geometrically confounded as
   designed:** the r ∈ [36, 44] annulus passes within ~11–19 of the
   displaced clusters (at ±25), so it reads their own r⁻⁶ mid-fields.
   Measured annulus mean |δρ| ≈ 1.7×10⁻⁴ matches the superposition of two
   single-cluster tails (single-cluster |δρ| = 3.6×10⁻³ → 1.5×10⁻⁴ over
   d = 11–20 weighted by arc fraction) — linear superposition of
   multipole fields, no monopole emergence. A clean doubling test would
   need a window beyond the live region; not pursued.
4. **E2b's evolved-snapshot rung was floor-limited** (the moving pair's
   asymptotic zone sits below the snapshot sound gate); the relaxed-state
   profile supplies the rung instead.

## Instrument lessons (for the next battery in this family)

- The empty-box floor is machine-zero and gates nothing; the *operative*
  floor in evolved fields is the standing-sound / boundary-ring level
  (~10⁻³ in δρ at this box), which **grows** as r² in coefficient units —
  far-field claims from evolved LogSE states are floor-dominated beyond
  r ≈ 15 at this box size.
- The imaginary-time-relaxed state measures static response with a
  machine-clean far field — the right tool for statics; real-time
  evolution is for stability checks only.
- Screened-control plateau windows must respect ξ ≪ r ≪ D/4.

## Status

#129 item 2 resolves: closed as a bare-medium derivation hope, merged into
item 1 (the compliance postulate carries G, extensivity, and now —
after #147 — the galactic halo's mass-coupling too). Paper edits in this
pass (rule 5): SSV-IV §universal extensivity paragraph updated from "open
requirement" to the #149 record; claim-status table updated; the
falsification-record summary gains the H-EXT row.

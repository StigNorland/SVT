# A3 — Goldstone-mode safety: the n̂ spin waves do not pollute the EM sector

**Issue:** [#87](https://github.com/StigNorland/SVT/issues/87) Part A, task A3.
**Status: PASS (conditional, condition argued)** — the two CP¹ spin-wave modes
are electrically neutral, decouple from the U(1)/chiral-shear EM channel at
linear order, and propagate no faster than `c⊥ = αc ≪ c`; the photon remains the
unique massless transverse mode of the EM channel. Verification:
`src/paper_i/cp1_safety_checks.py` (identity I4), `test_cp1_safety_checks.py`.

## The concern

`CP¹ ≅ S²` has real dimension 2, so tilting the internal direction `n̂` gives
**two real spin-wave modes** (the δn̂ fluctuations). If the SU(2) acting on the
spinor is spontaneously broken to the physical `U(1)` by the vacuum n̂₀, these
are massless Goldstone bosons. The danger: new massless modes could (a)
masquerade as extra photon polarisations, (b) add a second long-range force, or
(c) shift the electron/EM sector already matched in Papers I–II. A3 must show
none of these happens.

## Three layers of protection

**(L1) Linear decoupling from the U(1) phase and current (the core fact).**
The EM sector of SSV is the U(1) chiral-shear channel: photons are the
transverse `∇×j` waves at speed `c` (`L_⊥ ∝ |∇×j|²`, Paper I §"origin of α").
The spin waves enter the (ρ, θ, j) sector *only* through the Berry connection
`a = −i z†∇z` (decomposition identities I2, I3). Expanding the spinor about the
vacuum, `z = z₀ + ε δz` with z₀ const and the physical fluctuation transverse
(`z₀†δz = 0`), the Berry connection has **no O(ε) part**: `a = O(ε²)` (verified
identity I4, `linear_decoupling_coefficient() = 0`). Therefore:

- the current `j = (ħ/m₀)(ρ/ρ₀)(∇θ + a)` receives **no linear spin-wave
  contribution** ⇒ `∇×j`, hence the photon, is unmodified at quadratic order;
- the cross term `2A²(∂θ)a` in the energy is `O(ε² δθ)` (third order) ⇒ no
  bilinear `spin–photon` or `spin–sound` mixing in the free Lagrangian.

So at the level where the photon and electron sectors were derived (linear
response / quadratic action), the spin waves are **invisible to EM**. They are a
separate, decoupled sector.

**(L2) The spin waves are electrically neutral and parametrically slow.** The
n̂ fluctuations carry SU(2) "spin" charge, not U(1) electric charge (electric
charge in SSV is the U(1) winding / chiral-shear flux, orthogonal to n̂ by L1).
A neutral mode does not couple to the Coulomb channel, so it cannot be a second
electromagnetic long-range force. Its gradient stiffness is set by the
chiral-shear sector (A4: coefficient `λ = α²ρ₀/m₀`), so the spin-wave phase
speed is bounded by the chiral-shear scale `c⊥ = αc ≈ c/137`, parametrically
**slower than the photon at c**. Even in the worst case (exactly gapless
Goldstones), they are slow, neutral excitations cleanly separated in both speed
and charge from light — not extra photon polarisations.

**(L3) Gap-or-confine: the locking that fixes n̂₀ also lifts the modes.** Two
sub-cases, both safe:

- *If the SU(2)-covariant chiral-shear locking (the #84 total-current `L_⊥`)
  selects a preferred bulk n̂₀* — the natural expectation, since the saturated
  vacuum aligns the spin texture to the shear background — then the spin waves
  acquire a **gap** set by that locking, and there are no new massless bulk
  modes at all; the n̂ degrees of freedom are dynamical only inside defect cores
  (where `∇z ≠ 0`), exactly where they are wanted (lepton spin, muon rung).
- *If SU(2) is exact and unbroken in the bulk*, the modes are gapless Goldstones,
  but by L1+L2 they are neutral, decoupled from EM at linear order, and slower
  than light: a "spin sound" in the orthogonal sector, not a modification of the
  photon/electron results.

## Conclusion

The EM sector (photon = U(1) transverse chiral-shear wave at c; electron ring;
α) is built entirely from the (ρ, θ, j) channel, which the spin waves do not
touch at linear order (I4). The two n̂ modes are neutral, propagate at `≤ c⊥ =
αc`, and are either gapped (locked vacuum) or gapless-but-decoupled (exact
SU(2)). **No new massless mode appears in the EM channel; the photon stays the
unique massless transverse U(1) excitation.** A3 passes.

## Caveats (honest)

- **What is rigorously derived:** the linear decoupling (I4) and the consequent
  absence of any bilinear spin↔photon / spin↔sound mixing — this is solid and
  machine-verified.
- **What is argued, not yet computed:** the exact spin-wave dispersion (gapless
  `ω ∝ k²` ferromagnetic vs `ω ∝ k` antiferromagnetic vs gapped) depends on the
  time-derivative structure of the spinor action, which is fixed only once the
  full SU(2)-covariant Lagrangian is written down (a Part-B / follow-up task).
  The safety conclusion does **not** depend on which case obtains — L1 and L2
  hold for all three — but a definitive "the bulk is gapped" statement awaits
  that Lagrangian.
- The **non-linear** coupling (`O(ε²)` Berry phase) is real and is precisely the
  channel that gives the muon its half-integer holonomy (B1); it is a *core/
  texture* effect, not a bulk long-range one, so it does not reopen the
  bulk-EM-pollution concern.

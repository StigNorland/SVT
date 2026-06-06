# B1 winding-regime gate — result: CLEAN NO for the IQV electron

**Issue:** [#91](https://github.com/StigNorland/SVT/issues/91). Resolves the one
open conditional from [#87 B1](b1-muon-berry-phase.md): does the physical
electron-torus eigenbundle sit in the winding regime (`|m| < 1`)?
**Verdict: NO — the spin–orbit coupling |V| = 0 exactly for the IQV electron.
Muon reverts to NUMERICAL COINCIDENCE.** Verification: `src/paper_i/
spinor_bdg_coupling_audit.py`, `test_spinor_bdg_coupling_audit.py` (7 tests).

## Pre-registered decision rule (#91)

| condition | verdict |
|---|---|
| `|m| < 1` (lock dominates) | muon → **DERIVED** |
| **`|m| > 1`** (anisotropy dominates) | **TOPOLOGICAL-SECTOR conditional fails → NUMERICAL COINCIDENCE** |
| `|m| = 1` (gap-closing) | fine-tuning concern, estimate sensitivity |

**This audit returns: |m| → ∞. Verdict: CLEAN NO.**

## The spin–orbit coupling vanishes exactly for the IQV

The coupling amplitude `|V|` in the B1 model is the matrix element of the SU(2)-covariant `L_⊥` between `K_{+}(m_φ=+1)` and `Φ_{+}(m_φ=0)`. For this to be nonzero, `L_⊥` must carry a Fourier `e^{iφ}` component so that the azimuthal integral

    V = ∫₀^{2π} e^{−iφ} · kernel(φ) · dφ ≠ 0.

For the IQV (integer quantum vortex) with uniform spin direction z₀ = const, three independent facts show `|V| = 0`:

**Fact 1 — the current on the IQV background is scalar.** By Part A identity I3',
`j_total = (ρ/ρ₀)(∇θ + a)` with `a = −i z₀†∇z₀ = 0` for constant z₀. The
current is φ-independent and identical to the scalar result.

**Fact 2 — the z₀_⊥ channel contributes zero to δj.** For a perturbation `δΨ = w z₀_⊥`:

    δj = Im(δΨ†∇Ψ₀) + Im(Ψ₀†∇δΨ)
       = Im(w* z₀_⊥†∇(Ae^{iθ}z₀)) + Im(Ae^{-iθ}z₀†∇(wz₀_⊥))
       = 0 + 0   (killed by z₀†z₀_⊥ = 0 in both terms).

(Verified symbolically: `current_variation_from_perp_channel() = 0`.)

The second-order correction `δ²j = Im(δΨ†∇δΨ)` also separates — cross terms between the z₀ and z₀_⊥ channels carry `z₀†z₀_⊥ = 0`.

**Fact 3 — Fourier orthogonality.** The `L_⊥` operator on a φ-symmetric, uniform-n̂ background has no `e^{iφ}` Fourier component. Therefore:

    V = ∫₀^{2π} e^{−iφ} × (φ-independent kernel) dφ = 0   [exact].

(Verified symbolically and numerically: `fourier_bridge_integral_iqv() = 0`.)

**Consequence.** The `L_⊥` BdG matrix is block-diagonal in the (z₀, z₀_⊥) spin channels. This is the **same selection rule** already encoded in `kelvin_augmented_bdg.py` (line 476: `same_m = (bra.m_phi == ket.m_phi)`): it applies to both the scalar operator and the spinor L_⊥ on the uniform-n̂ background. The z₀ channel reduces to the scalar BdG; the z₀_⊥ channel is a decoupled free sector.

**Therefore: |V| = 0, |m| = |Δε|/(2·0) → ∞, regime = UNLOCKED, γ_B = 0.** The scalar #76 null is reproduced exactly. The B1 conditional is not met.

## What B1 got right vs what needed checking

B1 Half 1 (selection rule) was **correct**: the coupling is *allowed* by total-J
conservation (`ΔJ_φ = 0` satisfied by `Δm_φ=+1, Δs_z=−1`). The scalar `Δm_φ=0`
obstruction is genuinely lifted.

B1 Half 2 (the lock model) was **correct as a model**: if the lock amplitude were
nonzero, the ℤ₂-quantised Berry phase would give γ_B = π. The model H(φ) = d·σ
correctly represents the structure of the azimuthal eigenbundle.

What the B1 caveat correctly flagged as the open step: **whether the physical
background supplies a nonzero lock**. This audit answers: NO for the IQV.

Allowed ≠ nonzero. The lock requires the background to have azimuthal spin
texture (an `e^{iφ}` component in the operator), which the cylindrically symmetric
IQV does not have.

## The HQV control (confirmed nonzero, but a different foundational decision)

For a half-quantum vortex (HQV) with `z₀(φ) = (cos(φ/2), sin(φ/2))`:
- An `e^{iφ}` coupling kernel is sourced by the background texture
- The bridge integral gives `∫e^{−iφ}·e^{iφ} dφ = 2π` ≠ 0 (verified)
- BUT: the HQV mechanism is different from the spin-orbit lock — it works because
  modes on the HQV background have **half-integer effective azimuthal quantum
  numbers** (the background z₀(φ) contributes ½ to the total), so γ_B = π follows
  directly from the half-integer ladder without any matrix element needed

HQV gives γ_B = π, but: (a) it has ½ quantum of circulation, changing all mass
formulas; (b) the A1 pion = 2μ₀ result assumed IQV and must be re-examined for
HQV; (c) this is a further foundational decision not yet made. → Issue #94.

## Muon claim-status change

`m_μ = (3/2)μ₀`: **TOPOLOGICAL-SECTOR (conditional, #87 B1) → NUMERICAL
COINCIDENCE** (B1 IQV conditional not met; HQV route open but requires new
foundational decision). Claim-status table updated in Paper I.

## Gapboxes updated

Both stale muon gapboxes in Paper I (§"Empirical Ladder" ~line 813,
§"The Muon" ~line 933) updated to reflect the current state.

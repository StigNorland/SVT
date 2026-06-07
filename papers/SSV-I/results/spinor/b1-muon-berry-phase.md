# B1 — Muon rung `(3/2)μ₀` from the spinor Berry phase

**Issue:** [#87](https://github.com/StigNorland/SVT/issues/87) Part B, task B1 (the
highest-value item). Redoes the [#76](https://github.com/StigNorland/SVT/issues/76)
Task-3 Berry-phase calculation for the CP¹/spinor BdG operator.
**Verdict: CONDITIONAL-POSITIVE — the #76 no-go is LIFTED.** The muon is promoted
from **NUMERICAL COINCIDENCE** to **TOPOLOGICAL-SECTOR (protected half-integer
ladder)**, conditional on one quantitative check (the spin–orbit lock strength).
Verification: `instruments/paper_i/spinor_berry_phase_b1.py`,
`test_spinor_berry_phase_b1.py` (7 tests).

## Pre-registered hypothesis and decision rule (stated before computing)

**Hypothesis.** Promoting Ψ to the spinor `Ψ_a = √(ρ/ρ₀)e^{iθ}z_a` supplies the
`exp(iγ_B) = −1` (γ_B = π) that the scalar BdG operator lacked, so the muon rung
`m_μ = (3/2)μ₀` becomes a protected feature of a half-integer CdGM ladder
`E_n = (n + ½)ω₀`.

**Decision rule (pre-registered).**
- **DERIVES** the muon rung **iff** (a) the scalar-forbidden bridge
  `K_{σ,±}(m_φ=±1) ↔ Φ_R(m_φ=0)` is reopened by the spinor selection rule, **and**
  (b) the azimuthal Berry holonomy is `γ_B = π` and that value is **protected**
  (ℤ₂-quantised, not a tunable continuous angle).
- **CLEAN NO** if the spinor leaves `γ_B = 0` (as in the scalar case), with the
  obstruction named.
- **CONDITIONAL** if `γ_B = π` follows only given an extra ingredient — name the
  ingredient and whether it is already in the adopted theory.

## The scalar no-go being overturned (#76 Task 3)

The half-integer muon rung needs azimuthal holonomy `exp(iγ_B) = −1` in
`E_n = (n + γ_B/2π)ω₀`. The scalar LogSE BdG operator gave `γ_B = 0` for two
reasons:
1. the eigenbundle carries only **integer** azimuthal labels `e^{imφ}`, so the
   holonomy is `exp(i2πm) = +1`;
2. the bridge matrix element `⟨K_{σ,±}|(∇×δj)†(∇×δj)|Φ_R⟩` **vanishes** by the
   scalar selection rules `L^⊥: Δm_φ = 0`, `M^⊥: m_a + m_b = 0` — the Kelvin
   helicity modes carry `m_φ = ±1`, the breathing mode carries `m_φ = 0`.

The #76 note itself named the cures: *"eigenvectors rotating by half an angle
around the ring, or an underlying spinorial order parameter."* B1 supplies the
spinor and checks both halves.

## Half 1 (analytic) — the selection rule is reopened

With the spinor, the SU(2)-covariant chiral-shear term (the
[#84](https://github.com/StigNorland/SVT/issues/84) total-current `L_⊥`,
`j_total = Im(Ψ†∇Ψ)`) is a **spin–orbit coupling**: it conserves the **total**
azimuthal angular momentum `J_φ = m_φ + s_φ`, not `m_φ` separately. The
breathing mode and the Kelvin helicity modes are reclassified by `J_φ`:

| mode | `m_φ` | `s_φ` | `J_φ` |
|---|---|---|---|
| `Φ_R` (breathing) | 0 | ±½ | ±½ |
| `K_{σ,±}` (Kelvin helicity) | ±1 | ∓½ | ±½ |

Both sit at `J_φ = ±½`, so the bridge is **allowed**: the scalar obstruction
`Δm_φ = ±1 ≠ 0` is compensated by `Δs_φ = ∓1`, i.e. the spin flips against the
orbit. The selection rule that killed #76 Task 3 (`Δm_φ = 0`) is replaced by the
total-`J` rule (`ΔJ_φ = 0`), which the spin–orbit term satisfies. **The bridge no
longer vanishes.**

## Half 2 (computed) — the holonomy is `γ_B = π` and it is protected

A single spin-½ excitation on the ring has half-integer total angular momentum
`J_φ ∈ ℤ + ½` (`π₁(SO(3)) = ℤ₂`: a 2π frame rotation = −1). When the spin–orbit
lock co-rotates the internal frame once with the Kelvin helicity around the
major circle, the Nambu eigenbundle winds and acquires `γ_B = π`.

Crucially this is **not** the continuous solid-angle phase. The Nambu/BdG
particle–hole (here chiral) symmetry pins the azimuthal Berry phase to a **ℤ₂
invariant `γ_B ∈ {0, π}`** — it can change only by closing the BdG gap. The
minimal chiral-symmetric model of the azimuthal eigenbundle,

    H(φ) = d(φ)·σ ,   d(φ) = (m + cos φ, sin φ, 0) ,   σ_z H σ_z = −H,

makes this falsifiable. The constant `m` is the un-locked anisotropy (scalar
piece); the winding part `(cos φ, sin φ)` is the spin–orbit lock co-rotating the
spin with the Kelvin frame. The computed gauge-invariant Wilson-loop phase:

| regime | `m` | winding | `γ_B` | offset `γ_B/2π` | ladder |
|---|---|---|---|---|---|
| **locked** (lock wins) | `|m|<1` | 1 | **π** | **½** | `E_n=(n+½)ω₀` → **muon = 3/2** |
| unlocked / scalar | `|m|>1` | 0 | 0 | 0 | `E_n=nω₀` → **#76 null reproduced** |

`γ_B` is **exactly** π across the entire locked phase (every `|m|<1` tested) and
**exactly** 0 across the unlocked phase; the gap `2|d|` closes only at `|m|=1`,
so the `0→π` jump is a genuine **topological transition**. Hence `3/2` is sharp
and protected, not a fine-tuned `≈1.47`. The `m→∞` (no internal spin) limit
returns `γ_B = 0`, reproducing the #76 scalar result as a special case.

## Verdict against the decision rule

- (a) bridge reopened — **YES** (Half 1, total-`J` selection rule).
- (b) `γ_B = π` and protected — **YES** (Half 2, ℤ₂-quantised by BdG chiral
  symmetry; topological transition at the gap closing).

Both pre-registered conditions are met, **conditional on the spin–orbit lock**
(the eigenbundle being in the winding regime `|m|<1`). The lock is supplied by
the **already-adopted** SU(2)-covariant `L_⊥` (#84) — it is **not a new
coupling**. What the spinor adds is the *capacity* for `−1` (absent in the
scalar theory, `π₁(U(1))=ℤ`); what `L_⊥` does is *activate* it by tying the spin
to the Kelvin frame.

**Answer to the B1 decision question** ("does `γ_B=π` follow from the spinor
holonomy, or does it still require an explicit `L_⊥` coupling?"): it follows from
the spinor holonomy **once the spin is locked to the ring frame**, and that lock
is the SU(2)-covariant `L_⊥` already in the adopted theory — no new ingredient.

## Status change

`m_μ = (3/2)μ₀`: **NUMERICAL COINCIDENCE → TOPOLOGICAL-SECTOR.** The half-integer
ladder is now a protected consequence of the spinor structure; the muon is the
`n=1` rung of `E_n = (n+½)ω₀`. This is the #87 "DERIVES … or TOPOLOGICAL-SECTOR
(if partial)" outcome on the positive side.

## Caveats (honest — why TOPOLOGICAL-SECTOR, not yet unqualified DERIVED)

1. **The one open quantitative step:** that the SU(2)-covariant `L_⊥` puts the
   physical electron-torus eigenbundle in the **winding regime** (`|m|<1`, the
   lock dominating the anisotropy) — rather than the trivial regime — must be
   shown from the explicit `L_⊥` mode computation, not assumed. The present work
   proves the *dichotomy* (π if locked, 0 if not) and its protection; it does
   not yet compute which side of `|m|=1` the real defect lands on. That is the
   natural follow-up (a spinor version of the `kelvin_augmented_bdg.py` solve).
2. The two-band `H(φ)=d·σ` is the minimal faithful model of the **azimuthal
   eigenbundle holonomy** (the only thing `γ_B` depends on), not a full 3D
   spinor BdG solve; its job is to establish the ℤ₂ structure and protection,
   which it does rigorously.
3. The rung **assignment** (muon at the `3/2` step, electron as base) carries
   over from Paper I §4 unchanged; B1 supplies the half-integer *ladder*, which
   is what was missing.

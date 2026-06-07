# A2 + A4 — `α = c⊥/c`, `R_e = ξ/α`, Madelung survive; n̂ stiffness adds no free parameter

**Issue:** [#87](https://github.com/StigNorland/SVT/issues/87) Part A, tasks A2 and
A4. **Status: PASS** — all three foundational results are inert under the CP¹
extension to leading order; the spin stiffness is fixed by couplings already in
the theory. Verification: `instruments/paper_i/cp1_safety_checks.py`,
`test_cp1_safety_checks.py` (identities I2, I2′, I3, I3′, I4).

## What must survive (scalar derivations, `papers/SSV-I/main.tex`)

1. **Madelung structure** (§"Madelung representation", Eqs. continuity/euler):
   writing `Ψ = √(ρ/ρ₀) e^{iθ}`, `v = (ħ/m₀)∇θ`, the LogSE splits into the exact
   continuity equation and an Euler equation with log EOS `P = bρ ln(ρ/ρ̄)`.
2. **Sound speed / healing length** (Eqs. `cs`, `xi`): `c_s = √(2bρ₀/m₀)`;
   setting `c_s = c` gives `ξ = ħ/(m₀c)`.
3. **Origin of α** (Eq. `alpha-origin`): the chiral-shear term
   `L_⊥ = −(λħ²/2m₀ρ₀²)|∇×j|²` gives a transverse mode with `c⊥/c = √(λm₀/ρ₀) ≡ α`,
   fixing `λ = α²ρ₀/m₀`.
4. **Electron radius** (Eq. `Re-star`): minimising the ring energy (Lamb kinetic
   + core + chiral-shear) gives `R_e* = ξ/α = ħ/(α m₀ c)`.

## A2 — why all four are inert under the spinor extension

**These are all functionals of the (ρ, θ) sector only.** The spinor adds the
internal direction z (n̂ ∈ S²). The decomposition (identity I2, verified)

    |∇Ψ|² = (∂A)² + A²(∂θ)² + A²|∂z|² + 2A²(∂θ)·a ,   a = −i z†∇z ,  A = √(ρ/ρ₀)

and the current (Mermin–Ho, identity I3)

    j = (ħ/m₀)(ρ/ρ₀)(∇θ + a)

show that z enters *only* through `∂z` (the stiffness term `A²|∂z|²` and the
Berry connection a). Three consequences pin each result:

**(2.1) The vacuum is uniform-n̂.** The saturated vacuum is `ρ = ρ₀`, `θ` flat,
`n̂ = n̂₀ const` ⇒ `∂z = 0 ⇒ a = 0`. On this background the energy density and
current reduce *exactly* to the scalar ones (identities I2′, I3′, machine-zero
residuals). So `ρ = Ψ†Ψ` still obeys the same LogSE amplitude/phase dynamics,
the Madelung split is unchanged, and `c_s = √(2bρ₀/m₀)`, `ξ = ħ/(m₀c)` are
untouched. The log potential depends on `ρ = A²` only — also untouched.

**(2.2) The sound channel does not mix with spin waves at linear order
(identity I4).** Linearising about the vacuum, write `z = z₀ + ε δz` with z₀
constant and the *physical* fluctuation transverse, `z₀†δz = 0`. Then the Berry
connection has **no O(ε) part**: `a = O(ε²)` (verified, `linear_decoupling_
coefficient() = 0`). Since a is the only route by which z enters j and the
phase channel, the cross term `2A²(∂θ)a` is `O(ε² · δθ)` — third order. Hence
the quadratic (linear-wave) Lagrangian of the (δρ, δθ) sound channel receives
**no contribution from the spin fluctuations**: `c_s` is exactly the scalar
value. (This is the load-bearing fact for A3 as well.)

**(2.3) α and the chiral-shear coefficient are unchanged.** `α = √(λm₀/ρ₀)` is
a statement about the *coefficient* λ of `|∇×j|²` together with the background
`ρ₀, m₀`. The spinor extension does not introduce a new value of λ, ρ₀, m₀, and
on the vacuum (a = 0) `j` is the scalar current, so `∇×j` and `c⊥` are computed
from the same expression. Therefore `c⊥/c = α` and `λ = α²ρ₀/m₀` are preserved.

**(2.4) `R_e = ξ/α` is preserved to leading order.** The electron ring energy
`E(R,a)` (Lamb kinetic `∝ ln(8R/a)`, core self-energy, chiral-shear) is built
from ξ, α and the (ρ, θ) current — all inert by (2.1)–(2.3). The electron's
spin-½ is, in the spinor picture, the global framing/holonomy of n̂ around the
ring (a 2π rotation sends Ψ → −Ψ), a **π Berry phase carried by a flat (zero-
curvature) connection** in the thin-ring limit: it costs no gradient energy
`A²|∂z|²` at leading order (a flat connection has `∇×a = 0` and the holonomy is
topological, not energetic). Any stiffness correction is `O(λ_spin/R²)`,
subleading to the `ln(8R/ξ)` Lamb term that fixes the minimiser. So the
stationarity condition collapses to `ln 8r* = ln(8/α)` exactly as in the scalar
case ⇒ `R_e* = ξ/α`.

## A4 — the n̂ stiffness introduces no new free parameter

The spin sector's gradient energy is `A²|∂z|²` (identity I2). Its coefficient is
**the principal kinetic coefficient `ħ²/2m₀` already in the LogSE** — `|∇z|²`
rides on the same `(ħ²/2m₀)|∇Ψ|²` term, with prefactor `ρ/ρ₀`. No new constant
appears.

The coupling that locks the spin texture to the existing chiral-shear sector is
likewise fixed: by the connected-symmetry result of
[#84](https://github.com/StigNorland/SVT/issues/84), the SU(2)-covariant
generalisation of `L_⊥` is built from the *total* current
`j_total = Im(Ψ†∇Ψ)`, which is invariant under the full internal group
(`lie_closure = 15` for SU(4); the same argument gives the SU(2) spinor sector).
Its coefficient is the same `λ = α²ρ₀/m₀` already fixed by `c⊥/c = α`. So the
spin-texture stiffness and its locking are both set by `{ħ²/2m₀, ρ₀, λ=α²ρ₀/m₀}`
— **no tunable input is added.**

## Conclusion

`α = c⊥/c`, `R_e = ξ/α`, and the Madelung/sound structure are all functionals of
the (ρ, θ) sector, which is inert under the spinor extension on the vacuum and
decouples from the spin waves at linear order (I4). The n̂ stiffness and its
chiral-shear locking are fixed by couplings already present. **All four results
keep status DERIVED (re-confirmed under spinor); A4 introduces no new free
parameter.**

## Caveat (honest)

The one genuinely new freedom the extension *could* introduce is an explicit
vacuum-anisotropy potential `V(n̂)` selecting n̂₀. That is a **gap term**, not a
stiffness, and is addressed in the A3 note (it would *help* Goldstone safety by
gapping the spin waves, not hurt the results above, which live in the orthogonal
(ρ,θ) sector). If `V(n̂) = 0` (the maximally symmetric saturated vacuum), the
spin waves are gapless Goldstones — see A3 for why they still do not pollute EM.

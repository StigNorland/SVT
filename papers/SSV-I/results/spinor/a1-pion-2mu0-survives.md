# A1 — `pion = 2μ₀` survives the CP¹/spinor extension

**Issue:** [#87](https://github.com/StigNorland/SVT/issues/87) Part A, task A1 (the
gate). **Status: PASS — `m_{π±} = 2μ₀` is unchanged; claim stays DERIVED.**
Verification: `src/paper_i/cp1_safety_checks.py` (identities I2′, I3′),
`src/paper_i/test_cp1_safety_checks.py`.

## The claim under test

Paper I §"The Charged Pion" (`papers/SSV-I/main.tex`, Eq. `pion-mass`) derives

    m_{π±} ≈ 2 μ₀ = 2 m_e/α ≈ 140.05 MeV   (observed 139.57, 0.34%)

from a single fact: the charged pion is the minimal closed vortex–antivortex
loop carrying **two units of U(1) winding**, and each unit of winding costs the
flux-tube quantum μ₀. The "2" is topological (`π₁(U(1)) = ℤ`); μ₀ = m_e c²/α is
the per-winding string energy. The question for #87: does promoting the scalar
Ψ to the spinor `Ψ_a = √(ρ/ρ₀) e^{iθ} z_a` (z†z = 1, z ∈ CP¹) change this?

## Argument

**1. The pion is a uniform-n̂ configuration.** The charged pion is spin-0. In
the spinor picture spin is carried by the internal direction `n̂ = z†σz`; a
spin-0 object carries no spin texture, i.e. `z = const` (n̂ = n̂₀ everywhere).
The pion's winding lives entirely in the overall phase θ (the U(1) factor),
which is exactly the field that carried it in the scalar theory. The two
topological indices are independent: the U(1) winding (`π₁(U(1)) = ℤ`) and the
CP¹ skyrmion charge (`π₂(S²) = ℤ`) are distinct, so a pure 2-winding object can
— and for a spin-0 meson does — have trivial n̂ (skyrmion number 0).

**2. On uniform-n̂ configurations the energy is term-by-term the scalar energy.**
The decomposition (verified symbolically, identity I2 in `cp1_safety_checks.py`)
is

    |∇Ψ|² = (∂A)² + A²(∂θ)² + A²|∂z|² + 2A²(∂θ)·a ,   a ≡ −i z†∇z ,  A = √(ρ/ρ₀).

The first two terms are the scalar LogSE gradient energy; `A²|∂z|²` and
`2A²(∂θ)a` are the only new pieces, and **both carry a factor of a spatial
derivative of z**. For `z = const`: `∂z = 0 ⇒ a = 0 ⇒` both new terms vanish, and

    |∇Ψ|²  →  (∂A)² + A²(∂θ)²   (exactly scalar; identity I2′, machine-zero residual).

The LogSE potential `p(ρ ln ρ − ρ + 1)` depends only on `ρ = Ψ†Ψ = A²`,
unchanged. So the **entire energy functional restricted to uniform-n̂
configurations is identical to the scalar functional.**

**3. The current — hence the chiral-shear sector — is also unchanged.** By the
Mermin–Ho identity (I3, verified),

    j = (ħ/m₀)(ρ/ρ₀)(∇θ + a),

so at `a = 0` the current is exactly the scalar `j = (ħ/m₀)(ρ/ρ₀)∇θ` (identity
I3′, machine-zero). Therefore `∇×j` and the chiral-shear term
`L_⊥ ∝ |∇×j|²` — the part of the energy that, with the Lamb kinetic term, fixes
the per-winding cost μ₀ — take their scalar values on the pion.

**4. Uniform n̂ is a genuine solution, and the minimum, in the spin sector.**
The new spin-stiffness contribution `A²|∂z|² ≥ 0` is non-negative and zero only
for `∂z = 0`. A 2-winding loop with no skyrmion/Hopf charge and no enforced n̂
twist therefore *minimises* the spin sector at uniform n̂ (zero spin cost): the
pion cannot lower its energy by developing texture, and uniform n̂ solves the
n̂ Euler–Lagrange equation trivially. The spin sector contributes exactly 0.

## Conclusion

For the spin-0, 2-winding pion the spinor energy functional collapses to the
scalar one with zero spin-sector contribution. Hence

    E[π±] = 2 μ₀   exactly as in the scalar theory,

with the factor 2 still the U(1) winding number (untouched by the CP¹ factor)
and μ₀ still the scalar flux-tube quantum. **`m_{π±} = 2μ₀` survives; its claim
status remains DERIVED (re-confirmed under the spinor extension).** The gate is
open: nothing in the adoption forces a revision of the one clean mass
derivation.

## Caveats (honest)

- This is the leading-order statement for the idealised spin-0 loop. A
  *sub-leading* spin-orbit-type coupling between the chiral-shear sector and n̂
  (the same coupling that gives the muon its handle in B1) could shift the pion
  at `O(stiffness)`; but such a term is built from `∇z` and so vanishes on the
  uniform-n̂ pion at leading order — it cannot move the topological factor 2.
- The original Paper I claim already labels the *coefficient* (not the factor 2)
  as motivated rather than fully solved (the two-winding soliton profile is
  deferred to Paper II). A1 does not strengthen that; it only shows the spinor
  extension does **not weaken** it — the scalar derivation transfers verbatim.

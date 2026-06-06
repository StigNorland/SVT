# #95 — μ₀ and the SSV mass-sector parameter count

**Issue:** [#95](https://github.com/StigNorland/SVT/issues/95). **Verdict: μ₀ =
m_e/α is NOT independently predicted — it *is* m_e/α. The SSV mass sector has
exactly TWO irreducible inputs: α (dimensionless structure, = c⊥/c) and one mass
scale (m_e). Given those, the entire mass *spectrum* follows parameter-free; α =
1/137 is irreducible (identified, not predicted).** Verification:
`src/paper_i/mass_sector_parameter_count.py`, `test_mass_sector_parameter_count.py`
(6 tests).

## The question, sharpened

"Derive μ₀" has two readings: (1) *predict its value* from dimensionless vacuum
numbers; (2) *establish the irreducible input count* and show μ₀ and the whole
spectrum follow from it. Reading (1) is not achievable (it would require
predicting α and a mass scale from nothing). Reading (2) is the real, publishable
result — and Paper I already asserts it (eq `rho0-value`, "two empirical inputs
m_e, α, no free parameters"). This note makes it rigorous.

## The rigorous core

Every SSV particle mass is a pure topological number times μ₀:

| particle | `N_X` | basis | `m_X` | `m_X / m_e` |
|---|---|---|---|---|
| pion | 2 | two-winding (#87 A1) | `2μ₀` | **2/α** |
| muon | 3/2 | coincidence (#91/#94) | `(3/2)μ₀` | **3/(2α)** |
| proton | `N_Y·F = 3F` | trefoil crossing number (#92) | `3F·μ₀` | **3F/α** |

with `μ₀ = m_e/α`. Therefore the **mass ratios**

    m_X / m_e = N_X / α   (× F for the proton)

are functions of **α and topology only** — verified symbolically to be free of
every vacuum parameter {ρ₀, m₀, b, λ, ξ}. Consequences:

- the mass **spectrum** (all ratios) is fixed by **α + topology** alone;
- the overall **scale** is one mass unit, m_e;
- the order-parameter mass **m₀ cancels from every particle-mass ratio** (the
  Lamb formula `m_e c² = 2π²ρ₀ħ³Λ/(αm₀³c)` ties m_e to the same vacuum factor
  that scales every other mass) — m₀ is a decoupled graininess/UV scale
  (≈ ℓ_grain), not part of the mass sector;
- `ρ₀, b, λ` are fixed by {`c_s=c`, `c⊥/c=α`} and the m_e normalisation.

⇒ **The SSV mass sector has exactly TWO irreducible inputs: α and m_e.**

## Is α itself predicted? No.

The only candidate is the R_e-minimisation relation (Paper I eq `gammadef`):

    2π γ α² = ln(8/α) − 3/4 .

If γ were an independent pure number, this transcendental equation would *predict*
α. But γ is **defined via** α — `γ(α) = (ln(8/α) − 3/4)/(2πα²)` — i.e. the
chiral-shear coefficient is tuned to give `R_e = ξ/α`. So the relation is a
**consistency condition, not a prediction**. **α = 1/137 is irreducible**: SSV
identifies it as the stiffness ratio `c⊥/c`, but does not predict its value.

## Verdict and significance

- **μ₀ is not derivable** from more fundamental numbers; it **is** m_e/α.
- **Two irreducible inputs** (m_e, α); every mass **ratio** is parameter-free
  (α + topology); m₀, ρ₀, b, λ do not enter the spectrum.
- **α is irreducible** (the one free dimensionless number).

The honest headline: SSV's mass spectrum is a **2-parameter** system — one scale
(m_e) and one dimensionless constant (α) — versus the Standard Model's ~19 free
parameters, with the *content* carried by the topological integers (pion = 2,
proton crossing number `N_Y = 3`). This is a clarification of what SSV does and
does not claim, not a prediction of μ₀'s value.

## Claim-status

μ₀ row: **irreducible input** (= m_e/α). New framing: the SSV mass sector has
2 parameters (m_e, α); all mass ratios are parameter-free derived numbers.

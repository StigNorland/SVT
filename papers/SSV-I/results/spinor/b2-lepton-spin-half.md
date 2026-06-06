# B2 — Lepton spin-½ from the CP¹ order parameter (no longer assumed)

**Issue:** [#87](https://github.com/StigNorland/SVT/issues/87) Part B, task B2.
**Status: DONE — spin-½ promoted from ASSUMED to DERIVED.** Paper I updated
(`papers/SSV-I/main.tex`, §"The Electron (The Torus)" spin item, and the
gyromagnetic-ratio paragraph).

## The change

Before, Paper I asserted spin-½ via a scalar Finkelstein–Rubinstein argument
deferred to Paper II ("π₁ of the configuration space is ℤ₂, … will be given in
Paper II"). Issue [#29](https://github.com/StigNorland/SVT/issues/29)
(strand-model import, PARTIAL) showed that route does **not** work for a scalar
field: `π₁(U(1)) = ℤ` carries no ℤ₂, so the half-integer label does not fall out
for free. This was one of the reasons the CP¹/spinor order parameter was adopted
([#83](https://github.com/StigNorland/SVT/issues/83)).

With the spinor `Ψ_a = √(ρ/ρ₀) e^{iθ} z_a` (z†z = 1), spin-½ is **intrinsic**:

- the internal direction `n̂ = z†σz ∈ S²` is a genuine spin-1 vector built from
  a spin-½ amplitude z;
- a `2π` rotation of the frame acts on z by the spinor double cover and returns
  `Ψ → −Ψ` — `π₁(SO(3)) = ℤ₂`, the defining spinor property;
- the toroidal defect therefore lies in the **fermionic sector by construction**,
  not by an added topological assumption.

This is the field-theoretic home for the framing parity that #29 identified as a
required *extra label* on a scalar defect: the spinor supplies it natively.

## Consistency

- The gyromagnetic-ratio derivation (`g ≈ 2`) used `S_topo = ħ/2`; that input is
  now the intrinsic spinor spin rather than a deferred claim. The numerical
  `g ≈ 2` argument is unchanged.
- The half-integer **mass** ladder (muon = 3/2·μ₀) is the *dynamical* companion
  of the same spinor structure — see [B1](b1-muon-berry-phase.md): the same
  `π₁(SO(3)) = ℤ₂` that gives spin-½ gives the protected `γ_B = π` Berry phase.
- Spin-statistics composition for composites (e.g. the proton's
  ½⊕½⊕… build-up, Paper I §"baryons") is unaffected: it now rests on a genuine
  spinor, strengthening the earlier surface-framing argument.

## Claim-status change

`lepton spin-½`: **ASSUMED → DERIVED** (intrinsic to the CP¹ order parameter).

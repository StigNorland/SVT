# B3 — Chirality ℤ₂ from the CP¹ spin framing (postulate → consequence)

**Issue:** [#87](https://github.com/StigNorland/SVT/issues/87) Part B, task B3.
**Status: DONE — chirality ℤ₂ promoted from POSTULATE to DERIVED FROM SPIN
FRAMING.** Verification: `src/paper_ii/chirality_spin_framing_b3.py`,
`test_chirality_spin_framing_b3.py` (5 tests). Builds on
[#81](https://github.com/StigNorland/SVT/issues/81)
(`lr-su4-cp-parity-verdict.md`).

## What #81 established

The chirality ℤ₂ (selecting the chiral **16** over its mirror **16̄**) is **not**
forced by any CP-even chiral-shear energy. The SU(4) third colour bit makes `P_c`
CP-odd, so the **16** and **16̄** are exact CP conjugates; CPT pins them
degenerate. Forcing chirality **requires a parity-odd coupling** — the canonical
example `∫ j_c·ω_w` (`C=+1, P=−1, CP=−1`). In the **scalar** theory no such term
arises for free: a scalar U(1) order parameter has **no intrinsic handedness**,
so there is no P-odd object to build the lock from. Chirality therefore had to be
**postulated** ("chirality = the spin framing", written by hand).

## What the spinor supplies

With `Ψ_a = √(ρ/ρ₀) e^{iθ} z_a` the CP¹ field has a **spin Berry connection**

    a_i = −i z†∂_i z      (real — Part A identity I1).

Under the discrete symmetries `a` transforms **exactly like the probability
current** `j = Im(ψ*∇ψ)`:

| object | C | P | role |
|---|---|---|---|
| `j` (current) | −1 | −1 | #81 polar vector |
| `a` (spin Berry connection) | −1 | −1 | spinor analogue |
| `ω = ∇×j` | −1 | +1 | #81 pseudovector |
| `b = ∇×a` (spin Berry curvature) | −1 | +1 | spinor analogue |

(`a` is C-odd because charge conjugation sends `z → z*` and `a` is real; P-odd
because it transforms like `∂_i`.) Hence the spinor provides, **intrinsically**:

- the **spin-framing helicity** `a·b = a·(∇×a)` — a **P-odd pseudoscalar** (the
  Chern–Simons / Hopf term of the CP¹ field), whose **sign is the ℤ₂ handedness**
  of the framing;
- the **chirality lock** `j_c·b_spin`, with `(C,P,CP) = (+1,−1,−1)` — **the same
  slot as #81's `j_c·ω_w`**, the parity-odd coupling #81 proved is required, and
  it **can force chirality** (verified, `lock_matches_issue81_slot() = True`).

And the framing ℤ₂ acts on it: flipping the handedness sends `a → −a ⇒ b → −b`,
so the lock flips sign and the two handedness classes **select opposite sectors**
(`16 ↔ 16̄`). The chirality is locked to the framing handedness.

## Why this is a derivation, not a relabelled postulate

The decisive contrast (verified, `scalar_theory_has_no_carrier() = True`):

- **Scalar theory:** the only operands are `(j, ω)`; the single CP-even energy
  `|∇×j|²` yields only `ω·ω` (P-even). There is **no P-odd carrier at all** — the
  chirality label has no field-theoretic home, so it is an external postulate.
- **Spinor theory:** the P-odd carrier `a·b` **exists**, and the field
  configurations come in two genuinely distinct handedness classes (the
  `π₁(SO(3)) = ℤ₂`). The locking coupling `j_c·b_spin` is the **same spin–orbit
  term** that B1 uses to lock the spin to the Kelvin frame and that B2 uses for
  spin-½ — not a new ingredient.

So chirality is the **spin-framing handedness** of the CP¹ field — the same ℤ₂
that delivers spin-½ ([B2](../../../SSV-I/results/spinor/b2-lepton-spin-half.md))
and the muon Berry phase
([B1](../../../SSV-I/results/spinor/b1-muon-berry-phase.md)). The three Part-B
results are **one structure** (`π₁(SO(3)) = ℤ₂`) viewed three ways: as a spin
label (B2), as a dynamical holonomy (B1), and as a parity-odd handedness (B3).

## Claim-status change

`chirality ℤ₂`: **POSTULATE → DERIVED FROM SPIN FRAMING.**

## Caveat (honest)

What remains is a single **global** choice of framing orientation — the
definition of "left-handed" — one ℤ₂ convention for the entire theory (fixing
which of `16`/`16̄` is the physical generation). This is **not** a free parameter
per generation or per sector; it is the one irreducible handedness convention any
chiral theory carries. The mechanism (P-odd carrier + spin-framing sign) is
derived; only this universal orientation is conventional. A fully quantitative
step — that the spinor action's natural spin–orbit term generates `j_c·b_spin`
with a definite coefficient (rather than merely permitting it) — is the same open
computation flagged in B1 (the explicit SU(2)-covariant `L_⊥` mode solve).

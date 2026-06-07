# The sign is moot — a CPT degeneracy answers #81: chirality is NOT dynamically forced (2026-06-05)

**Issue:** [#81](https://github.com/StigNorland/SVT/issues/81), the decision. **Verdict:
NOT-FORCED — by a CPT degeneracy, not a vanishing matrix element.** A CP-conserving
SSV chiral-shear term cannot make the chiral **16** the lowest single-defect sector,
because the 16 and its vector-like mirror **16̄** are exact CP conjugates. The
chirality ℤ₂ ("chirality = the spin framing") remains SSV's one irreducible
fermion-sector postulate — and we now know *why no parity-conserving dynamics can
derive it.*

**Script:** `instruments/paper_ii/lr_su4_cp_parity_audit.py` · **tests:**
`test_lr_su4_cp_parity_audit.py` (9 pass). **Builds on:** `lr-su4-cross-term-audit.md`
(which it corrects), `lr-su4-logse-spec.md`, and the #80 Pass 5/6 bit structure.

## The question this settles

The spec (§3) reduced the entire chirality verdict to one term — the generalised
chiral-shear cross coupling `λ_cw ∫ ω_c·ω_w` — and the cheap route showed that term
is nonzero and leading-order. That left the **sign of `λ_cw`**: `λ_cw<0` would make
the chiral 16 the ground state (a genuine prediction); `λ_cw>0` would favour the
anti-diagonal (the pre-registered WRONG-SIGN branch). This note settles it: **the
sign is moot**, because a symmetry obstruction forbids *any* CP-even term from
selecting either sector.

## Layer 1 — CP maps the chiral 16 onto its mirror 16̄ (tested bit structure)

Antiparticle / CP conjugation reverses all charges, i.e. flips all five bits
`(c1,c2,c3,w1,w2) → (−…)`. Colour has **three** bits and weak has **two**, so

```
P_c = c1c2c3  → (−1)^3 P_c = −P_c     (CP-odd)
P_w = w1w2    → (−1)^2 P_w = +P_w     (CP-even)
```

Hence **CP: (P_c,P_w) → (−P_c, +P_w)** — it maps the **diagonal** sector (`P_c=P_w`,
the chiral 16) onto the **anti-diagonal** (`P_c≠P_w`, the 16̄), bijectively. Verified
on the tested `cp1_logse_16_assembly` weights: CP sends the 16 (even parity) onto the
16̄ (odd parity), flips `P_c`, preserves `P_w`, and swaps the two sectors, for every
state.

> It is precisely the **SU(4) enlargement** — the third colour bit `c3 = B−L = 4th
> colour` that #80 Pass 5/6 forced — that makes `P_c` CP-odd. With only SU(3)'s two
> colour bits `P_c` would be CP-even and this protection would not arise. The very
> structure that pins the target to Pati–Salam is what protects the chirality ℤ₂.

## Layer 2 — the canonical chiral-shear term is CP-even

The SSV chiral-shear term is `E_perp = (λ⊥/2)∫|∇×j|²` (Paper II §3–4: the Coulomb-like
`nn′/r²` interaction, like-sign repulsion, `λ⊥ ~ α^{-2} > 0`). The currents
`j = Im(ψ*∇ψ)` are C-odd polar vectors; `ω = ∇×j` are C-odd pseudovectors:

| coupling | C | P | CP | can force χ? |
|---|---|---|---|---|
| `ω_c·ω_w` (the `\|∇×j_total\|²` cross term) | + | + | **+** | no (P-even) |
| `j_c·j_w` | + | + | + | no (P-even) |
| `j_c·ω_w` | + | **−** | **−** | **yes (P-odd)** |
| `j·ω` (single-sector helicity) | + | − | − | yes (P-odd) |

The canonical term and its multi-component lift produce only the **CP-even** cross
term `ω_c·ω_w`.

## The verdict

A CP-even Hamiltonian commutes with CP, so CP-conjugate states are degenerate:
`E(16) = E(16̄)`. Combined with Layer 1 (CP *is* the diagonal↔anti-diagonal map),
the four `(P_c,P_w)` sectors are **forced degenerate** under any CP-even chiral-shear
energy. Therefore:

- **The sign of `λ_cw` is moot.** A parity-even `ω_c·ω_w` coupling yields *zero* net
  16-vs-16̄ selection, whatever its sign. **NOT-FORCED** — by a CPT degeneracy, not a
  #76-style vanishing.
- **Forcing chirality requires a parity-ODD coupling** (`∫ j_c·ω_w`). This is just
  *"you cannot derive parity violation from a parity-conserving Lagrangian."* A P-odd
  chiral-shear term **is** the postulate "chirality = the spin framing" in
  field-theory form — it does not come for free.

This **corrects the cheap-route toy** (`lr-su4-cross-term-audit.md`): its single
colour winding (1 bit) made CP flip `P_c` and `P_w` together, so it mis-saw a
CPT-violating "split." With colour properly SU(4) (3 bits), CP flips only `P_c`, the
would-be-split sectors are CP partners, and the split is forbidden. The cross
*integral* (`I_cross = 5.02`) is still nonzero — it simply cannot produce a net
chirality selection once CP is implemented correctly.

## Where #81 lands

The closes the dynamical question #80 left open, in the strongest available form:

- **#80 said:** chirality = one ℤ₂ postulate; topology *permits but does not force*
  the diagonal.
- **#81 adds:** no CP-conserving SSV *dynamics* can force it either — the chiral 16
  and the vector-like 16̄ are CP-conjugate (a consequence of SU(4) colour), so CPT
  protects their degeneracy against any CP-even chiral-shear energy. The postulate is
  exactly a **parity-odd** insertion, and SSV must make it by hand, as every chiral
  theory does.

So "one generation = one defect + one ℤ₂ postulate" is now sharpened: that ℤ₂ is
provably **not** obtainable from parity-conserving defect dynamics. The full
`C^4×C^2×C^2` 3D relaxer (spec Milestones 3–4) would only re-confirm a degeneracy
that this symmetry argument already guarantees — it is **not needed** to decide #81.
(It would still be the tool if one ever introduces an explicit P-odd term and wants
its quantitative consequences — a separate, much larger programme.)

## Caveats (honest)

1. The argument assumes the chiral-shear sector is **CP-conserving** (the canonical
   `|∇×j|²`, the EM-analog of Paper II). If SSV's master equation secretly contains a
   P-odd helicity term `j·ω`, chirality *could* be forced — but that term is itself
   parity-violating and would be the postulate, not a derivation of it. Either way the
   conclusion holds: chirality is an input, not an output, of CP-even SSV.
2. CPT here is used at the level of degeneracy of CP-conjugate static-defect
   configurations under a CP-invariant energy functional — an elementary
   `[H,CP]=0 ⇒` degeneracy argument, not the full relativistic CPT theorem.

## Reproducer

```bash
.venv/bin/python instruments/paper_ii/lr_su4_cp_parity_audit.py
.venv/bin/python -m pytest instruments/paper_ii/test_lr_su4_cp_parity_audit.py -q
```

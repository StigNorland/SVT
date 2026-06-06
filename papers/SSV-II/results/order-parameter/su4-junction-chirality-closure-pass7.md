# Chapter close — the 4-valent junction delivers SU(4); chirality is one postulate — Pass 7 (2026-06-05)

**Issue:** [#80](https://github.com/StigNorland/SVT/issues/80) Pass 7.
**Verdict: requirement (i) DELIVERED, requirement (ii) is ONE irreducible postulate.**
Reverse-engineering reaches its honest end: an entire Standard-Model generation
follows from a single SSV defect once *one* identification — "chirality = the spin
framing" — is adopted. Everything else (SU(4) colour, B−L, weak doublets,
multiplicities, anomaly) falls out.

**Script:** `src/paper_ii/su4_junction_chirality_closure.py` · **tests:**
`test_su4_junction_chirality_closure.py` (8); 40 pass across the #80/#79 suite.

## The two requirements Pass 6 left

Pass 6 forced the target to left–right-symmetric Pati–Salam SU(4)×SU(2)_L×SU(2)_R
and left exactly two requirements — both about realising it as a *connected*
symmetry: **(i)** a 4-fold junction giving SU(4), and **(ii)** the chirality ℤ₂
(16 vs 32) being the spacetime spin-½ / half-quantum-vortex ℤ₂ of #78. Both are
decidable at the structural level *before* any 3D field build.

## Part A — the 4-valent junction delivers SU(4) (requirement i)

Repeating the #79 computation for **four** legs with balance `θ₁+θ₂+θ₃+θ₄ = 0`:

- balanced phase space has **dimension 3 = rank SU(4)**;
- the continuous balanced moves generate an **abelian Cartan u(1)³** (not su(4),
  dim 15 — off-diagonal generators absent, exactly as #79);
- leg permutations form **S₄ = Weyl(SU(4))** (order 24);
- the **B−L direction `diag(1/3,1/3,1/3,−1)` lies inside that Cartan** (verified).

So the 4-valent junction supplies the SU(4) maximal torus *including B−L* for free,
at precisely the level #79 supplied SU(3). "Lepton = 4th colour" is structurally
present. **Requirement (i) is met** (same honest PARTIAL — Cartan + Weyl, no
off-diagonal generators).

## Part B — the chirality ℤ₂ is a postulate, not forced (requirement ii)

The order parameter carries **two independent ℤ₂ sector-parities**: colour
`P_c = c₁c₂c₃` (4 vs 4̄) and weak/spin `P_w = w₁w₂` (L vs R). Together they form
ℤ₂×ℤ₂ acting on the 32, splitting it into four sectors of 8. The chiral 16 is the
**diagonal** sector `P_c = P_w`.

Enumerating the three index-2 ℤ₂ quotients of ℤ₂×ℤ₂:

| conserve | content | is one generation? |
|---|---|---|
| P_c only (by colour) | mixed colour sectors | no |
| P_w only (by weak/spin) | mixed weak sectors | no |
| **P_c·P_w (diagonal = chirality)** | **Q6, u^c3, d^c3, L2, e^c1, ν^c1** | **YES — the 16** |

Only the diagonal quotient yields the Standard-Model generation, and **nothing in
the homotopy forces it** — topology equally permits the full product (the
vector-like 32) and the two other quotients. Selecting the diagonal is exactly the
statement *"the spinor's spacetime framing sign IS its internal chirality"* — the
chiral nature of the weak force, which no framework derives.

## Verdict — where the chapter honestly ends

- **(i) 4-valent junction = delivered.** SU(4) Cartan + Weyl + B−L, for free.
- **(ii) chirality ℤ₂ = one postulate.** Not forced by topology; it is the single
  identification chirality = spin framing.

The whole structure of one generation — SU(4) colour, B−L = 4th colour, the weak
doublets, the multiplicities 6,3,3,2,1,1, anomaly cancellation — follows from an
SSV defect **once that one ℤ₂ identification is adopted**. SSV does not derive it
(no framework does), but it **reduces all of a generation to it**. That is the
maximal over-constrained outcome reverse-engineering could reach short of the full
dynamical field theory.

## The precise brief left for the field theory

Build a **left–right-symmetric SU(4) LogSE** and test the one open dynamical
question: do its defect dynamics **force the diagonal ℤ₂** (chirality = spin) — or
leave it a choice? If forced, it is a genuine prediction (the origin of chirality).
If not, the postulate stands as SSV's one irreducible input for the fermion sector.
Either way, the group-theoretic skeleton of a generation is now fully accounted for.

## Reproducer

```bash
.venv/bin/python src/paper_ii/su4_junction_chirality_closure.py
.venv/bin/python -m pytest src/paper_ii/test_su4_junction_chirality_closure.py -q
```

# The 16 is forced to be Pati–Salam — the two Pass-5 demands are one structure — Pass 6 (2026-06-05)

**Issue:** [#80](https://github.com/StigNorland/SVT/issues/80) Pass 6.
**Verdict: the two Pass-5 impositions collapse into ONE connected group.** The
minimal LogSE that can carry one generation is forced into a sharp, falsifiable
shape — left–right-symmetric **Pati–Salam SU(4)_c × SU(2)_L × SU(2)_R** — with
B−L *inside* colour and chirality = a single ℤ₂. Nothing tuned per fermion.

**Script:** `src/paper_ii/pati_salam_16_unification.py` · **tests:**
`test_pati_salam_16_unification.py` (6); 32 pass across the #80/#79 suite.

## The question Pass 5 left

Pass 5 showed the 16 does not drop out of (scalar phase × CP¹ × SU(3) Y-junction);
it needs two impositions — **(a)** colour SU(3)→SU(4) with B−L as the 4th colour,
and **(b)** a parity lock `c₁c₂c₃ = w₁w₂` to pick the 16 over the 32. The open
question: are (a) and (b) two free knobs, or one structure? If two, it's fitting;
if one, it's a real target.

## Three rigorous facts (reconstructing the 16 from the Pati–Salam side)

Using the **same five bits** as Pass 5, cross-checked to give the identical 16,
B−L and Y:

1. **B−L is a Cartan *generator* of SU(4):** `diag(1/3, 1/3, 1/3, −1)`, traceless
   ⇒ a genuine SU(4) element. The 4 = 3_{+1/3}(quarks) + 1_{−1}(lepton), so
   **"lepton = the 4th colour" is exact.** B−L is not a U(1) *beside* colour; it
   lives *inside* the enlarged colour. Pass-5 demand (a) = "colour is SU(4)."

2. **16 = (4,2,1) + (4̄,1,2)**, with `T₃_L = (w₁−w₂)/4`, `T₃_R = (w₁+w₂)/4`. The
   left fields (Q, L) sit in the **4** and an SU(2)_L doublet; the right fields
   (u^c, d^c, e^c, ν^c) sit in the **4̄** and an SU(2)_R doublet. Computed
   explicitly: the even-parity constraint `c₁c₂c₃ = w₁w₂` is **exactly**
   "4 ↔ left, 4̄ ↔ right." So Pass-5 demand (b)'s parity lock *is* the left–right
   chirality correlation — **one ℤ₂.**

3. **Product → 32, connected → 16.** The full 32 = the four LR combos
   (4,2,1)+(4̄,1,2)+(4,1,2)+(4̄,2,1). A product of *independent* colour and weak
   sectors keeps all four (vector-like). The chirality ℤ₂ drops exactly
   (4,1,2) and (4̄,2,1), leaving the chiral 16.

| field | irrep | B−L | T₃_L | T₃_R | Y |
|---|---|---|---|---|---|
| Q | (4,2,1) | +1/3 | ±½ | 0 | +1/6 |
| L | (4,2,1) | −1 | ±½ | 0 | −1/2 |
| u^c | (4̄,1,2) | −1/3 | 0 | +½ | −2/3 |
| d^c | (4̄,1,2) | −1/3 | 0 | −½ | +1/3 |
| ν^c | (4̄,1,2) | +1 | 0 | +½ | 0 |
| e^c | (4̄,1,2) | +1 | 0 | −½ | +1 |

## Verdict — the demands are one group, and the target is now pinned

(a) and (b) are **not** two knobs: they are one connected left–right-symmetric
group, **Pati–Salam SU(4)_c × SU(2)_L × SU(2)_R** (the maximal subgroup of SO(10)
the 16 lands in). B−L is an SU(4) generator; the parity lock is the LR-chirality
ℤ₂. The minimal carrier of one generation is therefore forced to be:

- **left–right symmetric**, with an **automatic right-handed neutrino** (which SSV
  independently wants);
- **SU(4) colour with the lepton as the 4th colour**;
- selected to the chiral 16 by a **single chirality ℤ₂**.

This is a strong, falsifiable shape — not a per-fermion fit.

## What remains, and it is purely dynamical

Does an SSV order parameter realise G_PS as a **connected** internal symmetry,
not a product? Two concrete dynamical requirements:
1. a **4-fold junction** (the lepton loop as the 4th strand-type) giving SU(4),
   rather than the 3-valent SU(3) Y-junction of #79;
2. the **chirality ℤ₂ to *be* the spacetime spin-½ / half-quantum-vortex**
   structure #78 already demands — locking internal chirality to spacetime
   handedness, as any chiral theory requires.

So the field-theory target is no longer "a CP¹ LogSE" but precisely **"a
left–right-symmetric SU(4) order parameter whose chirality ℤ₂ is its spin
structure."** If a minimal such LogSE forces (i)+(ii) for free, it is the first
over-constrained SSV hit; if it cannot, the scalar core needs replacing, not
patching. The curiosity is answered at the group-theory level: **the 16 is
reachable, but only as one left–right-symmetric SU(4) object.**

## Reproducer

```bash
.venv/bin/python src/paper_ii/pati_salam_16_unification.py
.venv/bin/python -m pytest src/paper_ii/test_pati_salam_16_unification.py -q
```

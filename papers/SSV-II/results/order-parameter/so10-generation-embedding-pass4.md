# Does a single SSV defect carry the SO(10) 16? — Pass 4 (2026-06-05)

**Issue:** [#80](https://github.com/StigNorland/SVT/issues/80) Pass 4.
**Verdict: CONDITIONAL-POSITIVE.** The over-constraint is real and airtight on the
group-theory side (one generation = one anomaly-free irrep, verified). On the SSV
side the embedding is *consistent under the spinor extension that #78/#79 already
demand* — and three of the five Cartan charges have genuine homes SSV did not have
to invent. This is embedding-consistency, **not** a derivation; the derivation is
the falsifiable Pass 5.

**Script:** `src/paper_ii/so10_generation_embedding.py` · **tests:**
`test_so10_generation_embedding.py` (8) + `test_su3_y_junction.py` (8), all pass.

## Rigorous layer — the 16 is one anomaly-free generation (no SSV input)

The 16 spinor weights are the 5-tuples of ±½ with **even** parity (16 of them);
the odd-parity 16̄ is the anti-generation (16+16 = 2⁵ = 32). The standard
branching gives one SM generation:

| field | colour | weak | Y | B−L | states |
|---|---|---|---|---|---|
| Q (u_L,d_L) | 3 | 2 | +1/6 | +1/3 | 6 |
| u^c | 3̄ | 1 | −2/3 | −1/3 | 3 |
| d^c | 3̄ | 1 | +1/3 | −1/3 | 3 |
| L (ν_L,e_L) | 1 | 2 | −1/2 | −1 | 2 |
| e^c | 1 | 1 | +1 | +1 | 1 |
| ν^c | 1 | 1 | 0 | +1 | 1 |

**All anomaly coefficients vanish, computed directly:**

| anomaly | value |
|---|---|
| grav–U(1) (Σ Y) | 0 |
| [U(1)]³ (Σ Y³) | 0 |
| [SU(2)]² U(1) | 0 |
| [SU(3)]² U(1) | 0 |
| Σ electric charge | 0 |

So "one generation = one anomaly-free irrep" is not asserted, it is checked. This
is the over-constraint #80 identified — and it lives entirely in the 16.

## Interpretive layer — can an SSV defect realise the 5 Cartan charges?

Honest per-charge audit (5 Cartan charges + the chirality ℤ₂):

| Cartan charge | SSV realisation | status |
|---|---|---|
| colour I₃ | Y-junction phase-balance colour class (#79) | **PRESENT** |
| colour I₈ | second Y-junction Cartan direction (#79) | **PRESENT** |
| weak T₃ | spinor/CP¹ internal up–down (#78) | conditional-spinor |
| hypercharge Y | winding ⊕ spinor-framing combination | conditional-spinor |
| **B − L** | **Y-junction present (baryon) vs simple loop (lepton)** | **topological-candidate** |
| chirality (16 vs 16̄) | the spinor's defining ℤ₂ (2π-rotation sign) | conditional-spinor |

Tally: **PRESENT 2, CONDITIONAL-SPINOR 3, TOPOLOGICAL-CANDIDATE 1, ABSENT 0.**

### The three genuine homes (not invented for this purpose)

1. **Colour (2 Cartan charges) ← the Y-junction maximal torus.** #79 already
   established that the trivalent phase-balance gives exactly the SU(3) maximal
   torus (the three colour classes). Those are precisely the two colour Cartan
   charges the 16 needs.
2. **Chirality / even-parity ℤ₂ ← the spinor's defining ℤ₂.** The 16-vs-16̄ split
   *is* a chirality ℤ₂, and a spinor order parameter is the natural carrier of a
   chirality ℤ₂ (the Dirac belt / 2π-rotation sign). The **same** spinor that #78
   independently requires for lepton spin-½ is the right structure to supply the
   even-parity that selects *one* generation rather than a vector-like pair. This
   is a genuine two-for-one, not a new knob.
3. **B − L ← knot/graph type.** In SSV, baryons carry a trivalent Y-junction /
   trefoil skeleton while leptons are simple closed loops. "Has a Y-junction" vs
   "is an unknot" is a real topological distinction that could realise the
   baryon-minus-lepton charge *intrinsically*, rather than as an added U(1). This
   is novel and deserves its own derivation.

The two conditional charges (weak T₃, Y) need the explicit spinor-LogSE defect
spectrum and its winding↔framing map, which is not yet constructed.

## Why this is the strongest possible outcome short of building the spinor-LogSE

The question "does an SSV defect carry the 16?" comes back **plausibly yes**, and —
importantly — the pieces that fall into place are exactly the ones the *other*
fronts independently forced (colour from #79, spinor from #78), plus a genuinely
new topological reading of B−L. Nothing was tuned per fermion; the anomaly
cancellation is automatic for the 16. That is the signature of an over-constrained
embedding rather than a fit.

It is **not** a derivation. No SSV defect has been *shown* to fill the 16 weight
diagram; the spinor-LogSE whose defects would do so does not yet exist. The honest
status is: the target is consistent, over-constrained, and has real SSV homes for
3 of 5 charges + chirality.

## Pass 5 — the falsifiable derivation step

Construct the minimal spinor (CP¹) LogSE — scalar amplitude/phase × 2-component
internal direction — and compute its topological defect spectrum. Then test:

1. Does a single defect's label set (winding `n`, Y-junction colour, spinor
   framing parity, knot type) fill the **16** weight diagram with the **correct
   multiplicities** (6+3+3+2+1+1)?
2. Is **B − L** exactly the Y-junction / knot-type invariant?
3. Does the chirality ℤ₂ of the spinor reproduce the even-parity selection (one
   generation, not a vector-like 16+16̄)?

**If yes:** the first genuinely over-constrained SSV prediction — one generation,
anomaly-free, from one defect. **If the labels cannot be packed into a 16:** the
scalar core needs replacing, not patching, and the reverse-engineering has failed
its bar honestly. Either way it is decidable.

## Reproducer

```bash
.venv/bin/python src/paper_ii/so10_generation_embedding.py
.venv/bin/python -m pytest src/paper_ii/test_so10_generation_embedding.py -q
```

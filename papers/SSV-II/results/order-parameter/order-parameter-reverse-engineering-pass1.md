# Reverse-engineering the SSV order parameter from the SM targets — Pass 1–3 (2026-06-05)

**Issue:** [#80](https://github.com/StigNorland/SVT/issues/80).
**Script:** `instruments/paper_ii/order_parameter_manifold_scan.py`.
**Verdict: the order-parameter *manifold* alone cannot over-constrain the answer.
The genuine over-constraint is anomaly cancellation, a representation-theory fact
of a unifying group — not a homotopy fact.** This sets the bar that separates a
derivation from "the Standard Model relabelled in superfluid notation."

## Why this exercise is legitimate (and where it can go wrong)

Two independent fronts converge on the same missing ingredient — a non-abelian /
multi-component order parameter: the muon (#78, needs ℤ₂/spinor for half-integer
Berry phase + spin-½) and colour (#79, needs ℂ³ for the off-diagonal SU(3)
generators). When independent constraints land on one structure, reverse-engineering
is sound. The trap is over-fitting: if we add one component per front, we have
explained nothing. The test is **over-constraint** — one choice hitting many
targets, with anomaly cancellation falling out, plus an out-of-sample prediction.

## Pass 1 — homotopy / symmetry triage

| manifold | π₁ | π₂ | π₃ | symmetry | #choices | targets hit |
|---|---|---|---|---|---|---|
| S¹ = U(1) (current scalar SSV) | ℤ | 0 | 0 | U(1) | 1 | 2/7 |
| S² = CP¹ | 0 | ℤ | ℤ | SU(2) | 1 | 3/7 |
| SO(3) = ℝP³ | ℤ₂ | 0 | ℤ | SU(2) | 1 | 3/7 |
| CP² = SU(3)/U(2) | 0 | ℤ | 0 | SU(3) | 1 | 2/7 |
| SU(3) | 0 | 0 | ℤ | SU(3) | 1 | 2/7 |
| S¹ × CP¹ | ℤ | ℤ | ℤ | U(1)×SU(2) | 2 | 5/7 |
| **S¹ × CP¹ × CP²** | ℤ | ℤ⊕ℤ | ℤ | U(1)×SU(2)×SU(3) | **3** | **6/7** |
| SO(3) × CP² | ℤ₂ | ℤ | ℤ | SU(2)×SU(3) | 2 | 5/7 |

### Two structural findings

1. **The winding tension forces a product.** Integer winding (leptons, pion) needs
   π₁ = ℤ; spin-½ and half-quantum vortices (muon) need π₁ = ℤ₂. No connected
   *irreducible* manifold has both. So the order parameter must factor as
   **overall U(1) phase × internal (SO(3)/spinor) × colour**, e.g. S¹ × SO(3) × CP².
   This is a genuine deduction, and it matches the #78/#79 conclusions exactly.

2. **The full gauge group costs one factor per group.** U(1)×SU(2)×SU(3) appears
   only for product manifolds with #choices = 3 — one manifold factor per gauge
   group. That is **not over-constrained**: it is the SM gauge group inserted by
   hand and then relabelled as a superfluid order-parameter space.

## Pass 2 — where the real over-constraint lives (rep theory)

The discriminator between derivation and fit is whether **one irrep of a unifying
group gives one anomaly-free SM generation**. Explicit cubic-anomaly arithmetic
(`su_n_anomaly`, normalised A(N)=+1):

| group | one generation | anomaly sum | status |
|---|---|---|---|
| **SU(5)** | 5̄ + 10 | A(5̄)+A(10) = −1+1 = **0** | **OVER-CONSTRAINED** — fixed irrep set, anomaly cancels |
| **SO(10)** | **16** (spinor) | 0 (SO(N≠6) has no cubic anomaly) | **OVER-CONSTRAINED** — one irrep = one generation + ν_R, automatic |
| U(1)×SU(2)×SU(3) | SM fields, hypercharges by hand | 0 only after tuning | fitted / by-hand (the over-fitting baseline) |

SO(10) is the maximal over-constraint: a **single** 16-dimensional spinor irrep
*is* exactly one Standard Model generation (15 Weyl fermions + right-handed
neutrino), and anomaly cancellation is automatic. Nothing is tuned per fermion.

## Pass 3 — verdict and the bar this sets

- **Topology is necessary but not sufficient.** It fixes which *defects* exist
  (winding, HQV, skyrmion, baryon) and which symmetry can act, and it forces the
  "phase × internal" product structure — but the gauge group itself comes one
  factor at a time, which is fitting, not derivation.
- **The over-constraint is anomaly cancellation**, which is a fact about the
  *representation content* of a unifying group (SU(5)/SO(10)-type), invisible to
  the manifold's homotopy.
- **Consequence for SSV.** "Find a function that fits all fronts" will *always*
  succeed cheaply — you can relabel the SM as a multi-component order parameter —
  but it is predictive only if it clears the anomaly bar. The honest target is
  therefore sharp:

  > Show that a single SSV defect/texture sector transforms as one irrep of a
  > unifying group (the SO(10) **16** is the canonical candidate) per generation,
  > with anomaly cancellation falling out rather than inserted.

  Until that is demonstrated, a multi-component SSV order parameter is a **fit**
  (SM in superfluid notation), not a derivation.

## The decidable next test (Pass 4, future)

Take the forced product structure S¹ × (internal). Ask whether the SSV defect
that must carry spin-½ + colour can be assigned to the SO(10) **16** — i.e.
whether the vortex/texture quantum numbers (winding, framing parity, Y-junction
colour, chirality crossings) reproduce the 16's weight diagram. If they do *and*
the anomaly is automatic (SO(10) guarantees it), that is the first genuine
over-constrained hit. If the SSV defect labels cannot be packed into a 16, the
reverse-engineering fails the bar and SSV needs a different core, not a patch.

This converts the "one field that fits everything" intuition into a single
falsifiable question: **does an SSV defect carry the SO(10) 16?**

## Reproducer

```bash
.venv/bin/python instruments/paper_ii/order_parameter_manifold_scan.py
```

# Task B (scoping): could the muon be a half-winding / half-quantum-vortex?

**Issue:** [#78](https://github.com/StigNorland/SVT/issues/78) Task B — feasibility
memo only, no new infrastructure. Reached because Routes C and D both came back
negative.

## The idea

A half-quantum vortex (HQV) carries half the circulation quantum, `∮∇θ·dl = π`
instead of `2π`. Its hallmark is a **π Berry phase** — exactly the missing
ingredient the muon no-go (`muon-bdg-nogo-summary.md`) identified. Volovik §14.3.3
shows the ³He double-core vortex *is* a pair of HQVs joined by a non-topological
soliton wall, and that mapping already underlies the SSV baryon (trefoil /
double-core, see `notes/volovik-mapping.md` §2). So the π phase is not exotic — it
is present in the **paired** baryon sector. The question: can a **single**
half-winding object be the muon?

## Feasibility verdict: blocked in scalar SSV, needs the Task A structure

1. **An isolated HQV is forbidden for a single scalar Ψ.** The U(1) order
   parameter `Ψ = |Ψ|e^{iθ}` must be single-valued; a π phase winding leaves
   `Ψ → −Ψ` on encircling the core, which is a discontinuity. Only integer
   winding is admissible. This is the same `π₁(U(1)) = ℤ` fact that blocks the
   half-integer Berry phase in the first place.

2. **HQVs become admissible only with a compensating ℤ₂ / internal sector.** In
   every physical system that hosts HQVs (³He-A, spinor BECs, nematics), the π
   phase jump is cancelled by a simultaneous π rotation in an *internal* degree
   of freedom (spin, or the `d`/`l` vector), so the *combined* order parameter is
   single-valued. That internal sector is precisely the two-component / spinor
   extension scoped in **Task A**. There is no HQV without it.

3. **Why the baryon escapes and the lepton does not.** The baryon is a *pair* of
   half-windings (`π + π = 2π`, integer) tied by a soliton wall — globally
   single-valued, so it lives happily in scalar SSV. A lepton-as-single-HQV would
   need an *open* half-winding terminated by a wall whose far side supplies the
   missing π. In scalar SSV there is no field to carry that wall; the
   construction collapses back to requirement (2).

## What it would take (and what it buys)

- **Minimal addition:** a ℤ₂-valued (or S² / `CP¹`) internal label on Ψ so that a
  π phase winding can be screened by a π internal rotation. This is structurally
  identical to Task A's spinor order parameter — Tasks A and B are **the same
  extra structure** viewed from the winding vs the spectral side.
- **Payoff if added:** the muon becomes a genuinely distinct topological sector
  (half-winding) rather than an excited breathing mode, naturally carrying the
  π Berry phase and a `(3/2)`-type half-integer rung; the baryon HQV-pair mapping
  becomes literal rather than analogical.
- **Cost:** identical to Task A (see that memo) — it breaks the "one scalar Ψ"
  commitment of Papers I–II.

## Recommendation

Do **not** pursue a stand-alone half-winding muon construction: it is not a
separate route, it is Task A wearing a topological hat. Fold this into the Task A
decision. If a spinor order parameter is ever adopted, the half-winding muon and
the HQV-pair baryon should be re-derived together as the two simplest defects of
the enlarged manifold.

# Reconnection cap observable: grid convergence, and why the φ-ansatz test is blocked (#97)

**Issue:** #97 · **Date:** 2026-06-07 · **Branch:** `issue-97-cap-scaling`
**Script:** `instruments/paper_ii/cap_observable_convergence.py`
**Test:** `instruments/test/paper_ii/test_cap_observable_convergence.py`
**Touches:** `instruments/paper_ii/reconnection_supplement.py` (new `cap_method="moment"`)
**Context:** #105 (the W-mass resolution this would numerically cross-check), #15.

## Pre-registration

#97 asks whether the dynamic reconnection harness can give a **grid-converged**
cap radius, sufficient to test the golden-ratio cap-geometry ansatz
`R_cap = φ R*` (the route-C cross-check of the #105 resolution). The stated
blocker is that `cap_radius` drifts **17–62%** under grid/box refinement.

**Decision rule:** (1) a cap-radius observable is "grid-stable" if its spread
across `n` is `< 5%` at fixed physical evolved time `T` and coupling `λ_⊥`;
(2) the φ-ansatz is testable only if the harness produces a **well-posed cap** —
a transient depletion that forms and closes, giving a definite radius to measure.
Honest negatives are reported as such (rule 1).

## Result 1 — POSITIVE: a threshold-free observable is grid-convergent

The legacy `cap_radius` is built from a **hard threshold**: count cells with
`|ψ| < 0.25`, then `R = √(count·dx³/πξ)` (`volume`) or take the max radial extent
of a deep-depleted slice (`radial-slice`). Hard counts of a smooth field are
grid-sensitive — hence the drift.

New `cap_method="moment"`: the **depletion-weighted transverse second moment**
`R_cap = √(2⟨ρ²⟩_w)`, `w = (1−|ψ|²)₊`, taken in the slice of maximum depletion
(rings lie in (x,y), separated along z). Being an integral of the smooth field,
it converges. At `λ_⊥ = 1`, fixed `T = 0.045`, c=1 convention (`log_pressure=0.5`):

| n | moment | volume | radial-slice |
|---|---|---|---|
| 24 | 9.760 | 2.539 | 3.558 |
| 32 | 9.717 | 2.020 | 3.580 |
| 40 | 9.764 | 2.725 | 3.558 |
| 48 | 9.835 | 2.259 | 3.607 |
| **spread** | **1.2%** | **29.6%** | 1.4% |

**The moment radius is grid-stable to 1.2%**, vs 29.6% for the legacy default.
The #97 grid-convergence blocker is removed.

## Result 2 — NEGATIVE: the 2-ring harness produces no transient cap

A grid-stable *number* is not yet a cap. Time-resolving the canonical
opposite-circulation pair (n=40, λ_⊥=1, c=1) over the evolution:

- the on-axis `|ψ|` at the geometric centre **rises** `0.99 → 1.64` — the centre
  **never depletes**, so no central cap opens;
- the total depletion `Σw` (3.9k → 9.1k) and the moment `R_cap` (5.5 → 10.0)
  **grow monotonically**, with **no interior peak or plateau**.

There is therefore **no well-posed "cap radius" instant** in this harness: the
depletion just spreads. The earlier "cap forms at ~6 ξ" was an early-time sample
of this monotonic growth, read off at the (unstable, jittering) energy-saddle
index — not a transient cap. Consequently the φ cap-geometry ansatz
**cannot be tested with this configuration, independently of grid resolution.**

Two confounds that any future attempt must also fix (found en route): with
`auto_dt` the evolved time scales as `λ_⊥^{-1}·dx^4` for fixed step count (so a
naive `λ_⊥` sweep compares different physical durations), and the cap is set by
the **imposed** `ring_radius`, which is not tied to `R* = ξ/α = √λ_⊥ ξ` — so the
ansatz `R_cap ∝ √λ_⊥` is not even represented unless the initial ring radius is
made to track the coupling.

## Verdict (#97 stays OPEN)

The observable is fixed (1.2% grid stability); the φ-ansatz test is **blocked not
by grid noise but by the absence of a transient cap** in the 2-ring merger. The
remaining work is re-posing the harness so it realises the actual W-tube end-cap
geometry (a tube that pinches, giving a cap that forms and closes), with the
initial ring radius tied to `√λ_⊥` — then the `R_cap ∝ √λ_⊥` / φ test becomes
meaningful. This is a redesign, not a refinement, and it does not affect the
#105 resolution (which is analytic: the cap *scale* is the inherited ring scale;
`φ` remains an O(1) coincidence).

## Claim-status note (rule 5)

| Claim | Before | After |
|---|---|---|
| `cap_radius` grid stability | 17–62% drift (blocker) | **fixed** to 1.2% via threshold-free `moment` |
| φ cap-geometry ansatz, numerical test | "needs grid-converged cap_radius" | **blocked** — no transient cap in the 2-ring harness; needs a redesigned (pinch/tube) harness |
| #105 W-mass resolution | analytic (scale derived, φ coincidence) | unaffected; numerical cross-check remains open under #97 |

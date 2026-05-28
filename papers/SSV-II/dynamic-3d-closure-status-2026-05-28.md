# Dynamic 3D Reconnection Closure — Status (2026-05-28)

**Status:** closure memo for issue
[#15](https://github.com/StigNorland/SVT/issues/15).
**Scope:** dynamic branch only. Static breather closure is #13.

Same shape as `static-3d-closure-status-2026-05-28.md` (issue #13) and
`alpha-g-extraction-closure-status-2026-05-28.md` (issue #14): map each
of the seven issue tasks onto repo artifacts, identify which are
addressed and which are blocked, and state what would unblock the
blocked items.

## Task-by-task status

| # | Task | Status | Where |
|---|---|---|---|
| 1 | Define incoming defect geometry and event setup clearly enough to reproduce | **addressed** | `src/paper_ii/reconnection_supplement.py`'s `Config` dataclass + `initial_state()` exposes ring_radius, core_radius, separation, ring circulations (opposite/same), phase kick, and box length. Reproducible from CLI flags; CSV row format documented in `SCRIPT_METADATA.observables`. |
| 2 | Choose the first production-grade time-evolution scheme | **partial / prototype-grade** | Split-step Strang integrator in `evolve_path()` (Fourier kinetic step, real-space nonlinear potential, chiral-shear added spectrally as `λ_perp · k⁴`). Production-grade means: convergence verified at the target precision. The #16 dt-sweep (commit `a375acb`) shows the integrator is ~4% converged in dt for the opposite-circulation case at the current grid; the grid itself is far from converged (see task 5). The integrator choice is appropriate; the production-grade status is gated by the grid. |
| 3 | Define event diagnostics: energy drift, norm drift, onset/completion markers | **partial** | `energy()` and `potential_u()` exist; `analyse()` extracts saddle_index from the discrete time axis. Energy-drift and norm-drift telemetry are **not currently recorded** in the CSV outputs — they need to be added to the `analyse()` return path or to a dedicated diagnostics dataclass. Onset/completion markers are implicit in `saddle_index` (the peak of the excess curve) but not separately tracked. `shared_numerics.DynamicDiagnostics` (added under #12) gives the standard slot for advertising these. |
| 4 | Define observables: barrier height, cap radius, cap volume, emitted mode content | **partial** | Barrier height = `saddle_excess` (in `analyse()`); cap radius via volume or radial-slice extraction in `cap_radius()`; **cap volume** is computed inside `cap_radius()` but not separately returned; **emitted mode content** is not extracted — the projected-Hessian `cos_phi` is a related but distinct quantity (amplitude vs phase channel measure at the saddle, not a radiated-mode spectrum). `shared_numerics.DynamicObservables` (added under #12) is currently `(saddle_index, saddle_excess, cap_radius, cos_phi)` — extending it to include cap volume and a radiated-mode spectrum is the next observable-side work. |
| 5 | Timestep, resolution, initial-condition sensitivity checks | **addressed for timestep + resolution; blocked for IC** | `papers/SSV-II/validation-refinement-sweeps-reconnection-2026-05-28.md` (commit `a375acb`) reports the dt + grid + length sweeps with the headline result that **grid is the dominant non-convergence axis**: `saddle_excess` drifts 91.7% (opposite) / 45.3% (same) across n=16..48; `cap_radius` 44.6% / 17.3%; `cos_phi` 12.0% / 4.93%. Only `cos_phi` (same-circulation) marginally passes the 5% gate. dt is well-resolved (3.7-4.2% for the opposite case). Initial-condition sensitivity is **blocked** until cross-grid stability is achieved; with 91.7% spread on `saddle_excess` at fixed IC, recovering "the same event" from a different IC is not well-posed. |
| 6 | Compare measured cap geometry with the golden-ratio ansatz instead of back-solving from observed W mass | **blocked-by-design** | The φ ansatz says the reconnection cap geometry sits at `r_cap = φ · ξ` (or a related geometric constant) determined by the relaxed event itself, *not* by tuning to reproduce `m_W`. The current pipeline cannot test this: `cap_radius` swings 17-62% under grid + box refinement (per task 5), which is far larger than the precision needed to distinguish `r_cap = φξ` from neighbouring rational values like `1.5ξ` or `2ξ`. The ansatz test requires cross-grid stability at the few-percent level first. |
| 7 | Summarize Paper II claims that remain structural after the first reconnection run | **addressed below** | See §3. |

**Three of seven tasks fully addressed; three partial; one
blocked-by-design.**

## Implications for Paper II

Paper II §"Reconnection / W mass" already labels the cap-radius and
φ-ansatz content as **"Candidate geometry only"** in its abstract.
This labelling is consistent with the present #15 status: the
reconnection content remains *structural*, with `m_W ∼ φ · m_(scale)`
asserted on geometric grounds and not back-solved into agreement
with observed `m_W`. The #16 dynamic-side validation sweep (commit
`a375acb`) confirms the labelling: a pipeline that produces a
saddle_excess varying by 91.7% across n=16..48 cannot at this point
support a derived `m_W` prediction even if the φ ansatz held exactly.

**No Paper II main.tex edits are required** to reflect the current
#15 status. The honest framing is already in place.

What changes for Paper II once #15 reaches closure-grade:

- "Candidate geometry only" → "Candidate geometry, verified against
  measured cap radius at \[tolerance\]" once cap geometry is grid-stable.
- "φ-ansatz cap radius" → either confirmed against the relaxed event
  (promoting the W-mass content from candidate to derived) or
  falsified (which would itself be a clean result, since the ansatz
  is geometrically motivated and not free-parameter-fitted).
- The neutrino-sector and CP-observable claims, which Paper II
  currently inherits from the reconnection event via mode-spectrum
  extraction, become **conditional** on `task 4` (emitted mode
  content) being implemented and verified. Without that observable,
  those claims remain structural regardless of how well the cap
  geometry converges.

## What would close #15

Three concrete next-step work items, none of which are this-session
work:

1. **Refine the grid to n=64 and n=96 at length ≥ 24.** The current
   sweep stops at n=48; the cross-grid spread is still 45-92% on the
   primary observables. A coarse-fine pair at n=64 vs n=96 with
   identical (length, dt) would establish whether the saddle-excess
   and cap-radius observables plateau at a converged value. This is
   the dynamic-side parallel to the static refinement work tracked
   under #13.

2. **Add energy-drift, norm-drift, cap-volume, and a radiated-mode
   diagnostic to the analyser.** Three of the seven issue-task
   observables (cap volume, energy drift, norm drift, emitted mode
   content) are currently not recorded in the CSV outputs. Adding
   them to `analyse()` is cheap — the integrator already evolves the
   full state and `energy()` is already implemented — and is required
   before the φ-ansatz test can be done in a falsifiable way.

3. **Reconcile the c_eff convention mismatch.** The reconnection
   supplement uses `c_eff = sqrt(2 · log_pressure)` (default ≈ 4),
   not the canonical static-branch `c = 1`. The mismatch is flagged
   in `SCRIPT_METADATA.limitations` (commit `a5bb374` under #12).
   Closure-grade dynamic numbers should use a unit system compatible
   with the static branch so the cap-radius / breather-radius
   comparisons can be done without unit-conversion factors. This is a
   one-line `Config` change but propagates through every test.

These three are the dynamic-side counterpart of the #13 static
closure work. The natural follow-up issue would close all three
before promoting any reconnection observable from candidate to
derived, and before testing the φ-ansatz against measured cap
geometry.

## Honest status

The reconnection_supplement at its present reference configuration is
a **structural harness**, not a closure-grade event simulator. It
correctly identifies a reconnection saddle, distinguishes the
opposite-circulation channel from the same-circulation control, and
gives reasonable order-of-magnitude cap geometry; it cannot at this
point produce a falsifiable test of the φ-ansatz or a derived
`m_W` prediction. The Paper II "Candidate geometry only" labelling
remains the correct stance. Closure of the dynamic 3D reconnection
numbers — true closure, in the sense of converged cap geometry
under refinement — is open work; the immediate path forward is grid
refinement at the existing pipeline, not a redesign.

## Cross-references

- `src/paper_ii/reconnection_supplement.py` (the prototype harness)
- `src/paper_ii/validation_sweep_reconnection_supplement.py` (#16 sweep harness)
- `papers/SSV-II/validation-refinement-sweeps-reconnection-2026-05-28.md` (sweep findings)
- `src/shared_numerics/dynamic_branch.py` (shared dataclasses, #12)
- `docs/numerical-minimisation-roadmap.md` Workstream 4 (dynamic reconnection closure)
- `papers/SSV-I/static-3d-closure-status-2026-05-28.md` (static-side parallel for #13)
- `papers/SSV-I/alpha-g-extraction-closure-status-2026-05-28.md` (the α_G branch, blocked on both #13 and #15)

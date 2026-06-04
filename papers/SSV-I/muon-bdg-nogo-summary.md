# Muon BdG no-go: consolidated summary (2026-06-05)

**Issue:** [#78](https://github.com/StigNorland/SVT/issues/78) Task 0.
**Status:** the BdG-breathing-mode muon programme is retired. This note states
the single structural no-go that five independent probes converged on, and
records why the program cannot be rescued by further tuning of the current
scalar `L + L_perp` operator.

## The no-go statement

> A single scalar order parameter Ψ has a U(1) order-parameter manifold. Its
> first homotopy group π₁(U(1)) = ℤ gives integer winding but **no ℤ₂/spinor
> structure**, hence no half-integer Berry holonomy. The only term in the
> action that could bridge the m=0 breathing mode to the m=±1 helicity sector —
> the chiral-shear `L_perp` current-curl block — is **forbidden by the U(1)
> azimuthal selection rules** (`m_a = m_b` for the normal block, `m_a + m_b = 0`
> for the anomalous block). Therefore the muon cannot arise as a Bogoliubov
> breathing eigenmode with a half-integer `(3/2)μ₀` rung in the present scalar
> SSV operator.

Volovik's CdGM equal-level-spacing — the mechanism that *does* produce
half-integer-shifted bound-state ladders in vortex cores — does not transfer,
because it is a **fermionic** (Fermi-point) phenomenon. Scalar SSV has no Fermi
surface and no fermionic pairing, so the geometric Berry phase that drives the
CdGM shift is structurally absent.

## The five convergent probes

| Probe | Finding | Rules out |
|---|---|---|
| Draft App. B | `V_eff = 4(1−f₀²) ≥ 0`, purely repulsive | a bound *planar* breathing mode of the ring |
| Bare-ring estimate | `ω/ω_c ~ 0.016` vs target `0.207` | the uncoupled ring is ~13× too soft to be the muon |
| Two-mode model | needs a large ring↔chiral coupling `G` | locates the entire gap in one overlap integral `G` |
| #76 Task 3 (Berry phase) | `G = 0` by selection rule; `γ_Berry = 0` for scalar LogSE | the m=0 breathing mode cannot couple to the m=±1 helicity sector — no half-integer holonomy |
| #73 direct φ-BdG | lowest branch `~0.50–0.59`, robust to grid / window / current-curl model | the `0.207` hit is a basis-truncation artifact, not a real eigenvalue |

### Probe detail

1. **Effective potential (Draft App. B).** Linearising the LogSE about the
   vortex profile `f₀`, the radial breathing fluctuation sees
   `V_eff = 4(1 − f₀²) ≥ 0`. A non-negative potential has no bound state below
   the continuum, so there is no localized planar breathing eigenmode to host a
   sub-gap muon rung.

2. **Bare-ring softness.** A free toroidal ring's lowest breathing frequency
   estimates to `ω/ω_c ≈ 0.016`, an order of magnitude below the muon target
   `ω/ω_c = 0.207`. The ring alone is far too soft; any muon-scale stiffness
   must come from coupling to another sector.

3. **Two-mode reduction** (`papers/SSV-I/notes/muon-two-mode-symbolic-reduction.md`).
   Collapsing the dynamics onto {breathing `q`, chiral fluctuation `χ`} shows
   the entire muon gap would have to be supplied by a single ring↔chiral
   overlap integral `G`. The muon mass becomes a statement about `G`.

4. **Berry-phase audit, #76 Task 3**
   (`papers/SSV-I/volovik-berry-phase-issue76-tasks1-4.md`).
   The bridge matrix element
   `⟨K_{σ,±}|(∇×δj)†(∇×δj)|Φ_R⟩` is exactly the `G` above. It **vanishes**:
   `Φ_R` carries `m_φ = 0`, `K_{σ,±}` carries `m_φ = ±1`; the normal `L_perp`
   block requires `m_a = m_b` and the anomalous `M_perp` block requires
   `m_a + m_b = 0`, neither of which a 0→±1 bridge satisfies. So `G = 0` and the
   azimuthal holonomy stays trivial (`γ_B = 0`, integer rungs only).

5. **Direct φ-discretized BdG, #73**
   (`papers/SSV-I/muon-issue73-phi-bdg-result.md`).
   Representing the `m_φ = ±1` sector directly (no hand-picked Kelvin seeds) at
   the matched `hw=8, r_w=4, λ_perp=π/4` point gives lowest branches
   `0.502 (n=9)`, `0.591 (n=11)`, `0.539 (n=13)`, `0.553 (n=15)` — all far above
   `0.207` and stable under resolution / window / current-curl-model variation.
   The earlier `0.207` reduced-basis hit was therefore a truncation artifact.

## Consequence for the mass ladder

`m_{μ±} = (3/2)μ₀` is **demoted** from "candidate rung" to **numerical
coincidence pending Route C** (generations as distinct static minima). The
`(3/2)` assignment matches the PDG muon mass to `0.59%`, but the present scalar
operator provides no mechanism that selects `3/2`; the agreement is at the level
of the `Δ = 0.096` ladder coincidence (Path A), not a derivation.

The pion rung (`n = 2`, integer) is **not** affected — it lives in the integer
sector that the pure-LogSE holonomy *does* support, and is consistent with #76
Task 2.

## What a revival would require (not in scope here)

A positive muon derivation needs *new microscopic structure*, not another pass
through the reduced basis:

- a **spinorial / CP¹ order parameter** that restores the fermionic Fermi-point
  Berry phase wholesale (Task A scoping — collides with the "one field Ψ"
  commitment), or
- a **derived half-winding (half-quantum-vortex) configuration** carrying a
  genuine π holonomy (Task B scoping — the π phase already lives in the baryon
  double-core = HQV-pair mapping, Volovik §14.3.3).

Both are scoped, not committed, in issue #78. The constructive replacement
programme is **Route C** (generations as distinct static minima) and **Route D**
(Kelvin-mode degeneracy / closed-shell 8ⁿ rule), both reusing the #77 static
minimiser.

## References

- `papers/SSV-I/path-b-eigenvalue-result.md` — Path B BdG null
- `papers/SSV-I/muon-issue72-drift-diagnostic-result.md` — Kelvin drift diagnostic
- `papers/SSV-I/muon-issue72-lperp-second-variation-audit.md` — L_perp audit
- `papers/SSV-I/muon-issue73-phi-bdg-result.md` — direct φ-BdG null
- `papers/SSV-I/volovik-berry-phase-issue76-tasks1-4.md` — Berry-phase no-go
- `papers/SSV-I/notes/muon-two-mode-symbolic-reduction.md` — the `G` overlap integral
- `notes/volovik-mapping.md` — lepton ladder, closed-shell hypothesis, fermionic/scalar divergence

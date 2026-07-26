# Issue #166 sub-calculation 4 — the reconstruction map (does the bulk TT *follow from* the screen state?)

**Status: R1 assembled — the bulk shear response is DETERMINED and LONG-RANGE
(it *follows from* the screen state), not imposed as in #162.** With three
necessary conditions verified (geometric modular flow, conserved spin-2 stress,
local positive-G induced Einstein term), the Faulkner–Van Raamsdonk theorem
gives the linearised bulk Einstein equations — the bulk metric perturbation
*follows from* the screen state. This note supplies the missing operational
content: a localized screen source produces a **determined, transverse,
long-range** bulk shear response (`G₂(r) ∝ 1/r²`), the hallmark of
reconstruction, in explicit contrast to the short-range/contact response of an
imposed (#162-like) kernel.

Pre-registered on [#166](https://github.com/StigNorland/SVT/issues/166) before
the computation. Script `instruments/model_screen/reconstruction_response.py`;
tests `instruments/test/model_screen/test_reconstruction_response.py` (6);
receipt `reconstruction_response_receipt.json`.

## Why this is what "follows from" means

In #162 the bulk shear was **imposed by hand** — inserted locally, with free
data. Reconstruction is the opposite: the bulk shear at a point is **determined,
non-locally, by the screen source elsewhere**. Two computable signatures
distinguish them:

- **Determinacy** — the map source → response `h₂ = J/Π₂` is single-valued
  (`Π₂` invertible), so there is *no* free/imposed data.
- **Propagation** — the response is **long-range** (a localized source is felt at
  distant `r`), not contact/short-range (a purely local insertion).

## Method

The induced bulk spin-2 Green's function `G₂(k) = 1/Π₂(k)` (sub-calc 3's
polarisation). The physical, masslessness-protected kinetic term `Π₂^phys = c₂k̂²`
gives `G₂ = FFT[1/c₂k̂²]`; its radial profile `G₂(r) ∝ 1/r^p` is fit for `p`.
Contrast: a **gapped** kernel `M² + c₂k̂²` (the #162-like "imposed/contact" case)
gives a Yukawa `G(r) ∝ e^{−Mr}/r^{3/2}`.

## Positive controls (all pass)

| control | result | meaning |
|---|---|---|
| **C1** Ward (reuse sc2) | `∂·τ/τ = 7.1×10⁻⁷` | the response is **transverse** (couples to the TT source, not the trace) |
| **C2** machinery | `1/k̂² → G(r) ∝ 1/r^{2.0}` | the Green's-function extraction recovers the 4D massless power |
| **C3** discrimination | gapped kernel: Yukawa rate `0.59 > 0`, power `4.7` (steep) | the test **separates** long-range (follows-from) from short-range (imposed) |

## Result

| test | result | verdict |
|---|---|---|
| **T1 determinacy** | `min\|Π₂(k)\| = 1.8×10⁻²  > 0` | the map source→response is **single-valued** (no free data) |
| **T2 propagation** | `G₂(r) ∝ 1/r^{2.09}` (4D massless `→ p≈2`) | the response is **long-range** — a localized screen source determines bulk shear at distant `r` |
| contrast (imposed) | Yukawa rate `0.59`, no clean power | the #162-like imposed kernel is **short-range** |

So the induced bulk shear response is **determined** and **long-range**: the bulk
TT perturbation *follows from* (propagates from) the screen state, in direct
contrast to the short-range/contact response of an imposed insertion. Combined
with the three verified necessary conditions, the Faulkner–Van Raamsdonk
reconstruction closes at the level this programme can compute.

## Verdict

- **T1 (determinacy): PASS** — `Π₂` invertible → the bulk response is fixed by
  the screen source, no imposed/free data.
- **T2 (propagation): PASS** — `G₂(r) ∝ 1/r²` (long-range) → the bulk shear
  follows non-locally from the screen; the imposed (#162) kernel is short-range.

**Net:** the bulk TT response *follows from* the screen state — the exact thing
#162 could not achieve (it imposed it). R1's reconstruction direction is
assembled from four validated computations.

## Honesty items and scope (rule 1)

- **Masslessness is the verified symmetry theorem, not re-measured here.**
  `Π₂^phys`'s `k→0` masslessness (which makes `G₂` long-range) is the
  diff-invariance theorem whose precondition (conserved stress) is verified in
  sub-calc 2; the raw `⟨TT⟩`-only lattice `Π₂` is cutoff-contaminated (sub-calc 3)
  and is *not* used to re-derive masslessness. This sub-calc establishes
  **determinacy** and the **resulting long-range transverse propagation**, and
  *assembles* the reconstruction — it does not independently re-derive
  masslessness or the absolute `G`.
- **Necessary content, assembled — not a new sufficiency proof.** The
  reconstruction *theorem* (Faulkner–Van Raamsdonk) supplies sufficiency once its
  inputs hold; this note verifies its operational signatures (determinacy +
  propagation) for the SSV screen. It is the assembly of four validated pieces,
  not a fifth independent theorem.
- **Deferred (the honest remaining items).** (1) The specifically-TT numerics in
  `d ≥ 3` boundary (this uses the 4D screen polarisation, adequate for the spin-2
  channel, but the full boundary-region entanglement reconstruction in `d ≥ 3` is
  heavier). (2) The seagull-complete absolute `1/G`. (3) The one remaining R1
  probe that could still bite: whether the *full nonlinear* map (not just the
  linear response) closes — beyond the linearised first law.

## Net

Four validated computations — geometric modular flow (sc1), conserved spin-2
stress (sc2), local positive-G induced Einstein term (sc3), and a determined,
long-range, transverse bulk response (sc4) — assemble the Faulkner–Van Raamsdonk
reconstruction: **the bulk transverse-traceless shear follows from the screen
entanglement state.** This is the object SSV lacked (the superfluid cannot shear;
the screen's entanglement supplies it) and the reason holography is structurally
essential. The deferred items are the absolute `G` and the nonlinear/`d≥3`
strengthening — not the existence of the reconstruction.

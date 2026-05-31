# Muon Stage 3 pre-registration: first-principles audit of L_perp BdG implementation

**Date:** 2026-05-30. Written BEFORE doing the derivation, so its conclusion
cannot be tuned to the result. Follows Stages 1 and 2 which together
established that the L+L_perp toroidal-breather BdG operator at
$\lambda_\perp = \pi/4$, as currently implemented, does not predict a muon
(neither as a core-Kelvin hybrid nor as a basis-converged pure-Kelvin Nambu
mode; the hw-drift of the Kelvin sector is structural and survives the
selection-rule fix).

## What Stage 3 is NOT doing

Explicitly excluded by methodological commitment:

- **No term-hunting.** Stage 3 does not propose new Lagrangian terms,
  candidate corrections, or phenomenological additions. The only operator
  changes allowed are those that follow uniquely from a careful derivation
  of the existing $\mathcal{L}_\perp$ on the torus.

- **No coefficient tuning.** If the derivation produces a missing term,
  that term's coefficient is whatever the derivation says it is. We do
  not adjust to match the muon, the pion, or any other target. If the
  derivation has free coefficients, we report the operator is
  under-determined and stop.

- **No phenomenological additions in the name of "completing the
  physics".** A claim like "we should also add a boundary term because
  it's natural" is not allowed unless it falls out of the variational
  principle directly.

## What Stage 3 IS doing

A careful symbolic re-derivation of the second variation of
$\mathcal{L}_\perp = -(\lambda \hbar^2 / 2 m_0 \rho_0)\,(\nabla \times j)^2$
on the toroidal background $\Psi_0(r, z)$, comparing each derived term
to what the code in `kelvin_augmented_bdg.py` and
`current_curl_component_overlap` actually computes.

The derivation proceeds in three steps:

**Step 1 — Linearise.** Write $\Psi = \Psi_0 + \delta\Psi$, expand
$\nabla \times j$ to first order in $\delta\Psi$:
$\nabla \times j = (\nabla \times j_0) + (\nabla \times \delta j_1) + O(\delta\Psi^2)$.

**Step 2 — Square.** Compute
$(\nabla \times j)^2 = |\nabla \times j_0|^2 + 2 (\nabla \times j_0) \cdot (\nabla \times \delta j_1)
+ |\nabla \times \delta j_1|^2 + 2 (\nabla \times j_0) \cdot (\nabla \times \delta j_2)
+ O(\delta\Psi^3)$
where $\delta j_2$ is the bilinear-in-$\delta\Psi$ part of $j$.

**Step 3 — Integrate.** The action $\int d^3 x\,\mathcal{L}_\perp$, expanded
to second order in $\delta\Psi$, must equal $\sum_{ab} \delta\bar\psi_a M_{ab} \delta\psi_b$
where $M_{ab}$ are the L and M block matrix elements. Any integration-by-parts
step that produces surface terms gets tracked explicitly.

The output of Step 3 is the exact L and M block matrix elements that the
$\mathcal{L}_\perp$ variation produces. Each is compared term-by-term against:

- `current_curl_component_overlap(bg, a, "u", b, "u", cfg)` and the "v" variant
  (these are the `|∇×δj_1|^2` terms in the linear current-curl model)
- `background_second_current_curl_overlap(bg, a, b, cfg, pair_type=...)`
  (these are the `(∇×j_0)·(∇×δ²j)` terms in the "full" current-curl model)
- Any surface terms produced by integration-by-parts in the derivation.

## Pre-registered decision rule

After comparing the derived BdG operator to the code:

**CASE A — they match exactly.** The operator is implemented correctly.
The Stage 2 finding (no basis-converged muon eigenmode) is then the
operator's actual prediction. Output: "the L+L_perp operator at
$\lambda_\perp = \pi/4$ does not predict a muon; the §The Muon rewrite
proceeds with this as the final word from the variational principle."

**CASE B — surface terms exist that the code drops.** Implement the surface
terms exactly as derived. Re-run Stages 1 and 2 on the corrected operator.
If the corrected operator now produces a basis-converged eigenmode in the
muon window, that is a genuine derivation; the muon ladder is rescued and
the §Muon mechanism is the surface-term-corrected one (which we'll then
have to interpret physically). If the corrected operator still produces
no basis-converged muon, escalate to CASE C.

**CASE C — bulk terms exist that the code drops, with uniquely determined
coefficients.** Same as Case B, but for bulk rather than surface terms.

**CASE D — the derivation produces a term with a free coefficient (or with a
coefficient that depends on a choice not present in the Lagrangian).** Report
the operator as under-determined; do NOT pick a coefficient. The Stage 2
result (no muon) stands; the §Muon rewrite proceeds.

**CASE E — the derivation reveals a term in the code that doesn't follow
from the Lagrangian** (a spurious addition). Remove it, re-run Stages 1
and 2.

## Output commitment

Whatever the comparison reveals goes into the Stage 3 result note verbatim,
with the derivation shown in full so a reader can check each step. The
result note's conclusion follows the decision rule above; nothing is
adjusted post-hoc.

## Honest probability estimate (also pre-registered)

Based on the prior author's diagnosis that the hw-drift looks like a
missing outer-region term, my honest prior estimate before doing the
derivation:

- CASE A (operator matches exactly): ~50%. The most likely outcome; the
  code is carefully written, and the prior author's "needs a term that
  provides the correct hw-independent Kelvin shift" was a hypothesis, not
  a demonstration of a missing derivation step.
- CASE B (missing surface term): ~25%. Surface terms are notoriously
  dropped in numerical implementations and the hw-drift behaviour is
  exactly the symptom of one.
- CASE C (missing bulk term): ~10%. Less likely because bulk terms are
  more obvious in the derivation.
- CASE D (under-determined): ~10%. Possible if the
  $\delta^2 j$ projection requires a choice of reference frame or basis.
- CASE E (spurious term): ~5%. Unlikely but worth checking.

If CASE A holds, the §Muon rewrite proceeds with definitive language.
If CASE B/C produces a non-tuned operator change that rescues the muon,
the SSV physics has been actually advanced.

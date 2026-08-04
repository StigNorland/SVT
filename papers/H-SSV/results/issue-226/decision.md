# Issue #226 — final decision and status report

Status: **complete**

Decision: **PROCEED — C4 passes all six foundation gates**

## Outcome

H-SSV-I now has one minimal causal, conserved, observer-consistent and bounded
screen theory. H-SSV-II may open, but must inherit this foundation unchanged
and may not use rotation residuals to replace it.

The decisive correction was to separate global state from global signaling:

\[
\boxed{\text{one entangled global state}\;\not\Rightarrow\;
\text{superluminal local influence}.}
\]

C3 represented the screen as a classical membrane and failed F3 because it
needed an undefined preferred rest flow. C4 instead represents it as a quantum
causal network. Spacelike gates commute, the encoding is independent of their
linear order, and a local operation leaves a remote reduced state unchanged.
The screen can carry shared host/satellite/cluster correlations without
violating local causality.

## Physical foundation fixed by C4

- A topological screen site has finite state capacity `ln d_e` and finite
  update capacity `nu_e_max`.
- A moving particle has the same two kinds of capacity.
- A relocation is one bilateral causal gate using one particle slot and one
  addressed screen-site slot.
- Static content is encoded occupation/correlation; active load is gate demand;
  retained memory is reduced-state mutual information/correlation.
- Site load and universal remaining update availability are

  \[
  q_e=j_e/\nu_e^{\max},\qquad A_e=1-q_e.
  \]

- Every gate is unitary/isometric and conserves additive local four-momentum;
  reduced entropy may grow while global information remains conserved.
- Positive gate counts and record projectors add below capacity and saturate at
  capacity; coherent phase cannot turn them negative.

## Six-gate result for C4

| gate | result | reason |
|---|---|---|
| F1 dimensions / causality | **PASS** | Proper-time gate rates have `s^-1`; all graph edges are causal; spacelike algebras commute. |
| F2 conservation | **PASS** | Local unitary gates commute with additive four-momentum and preserve global information. |
| F3 observer consistency | **PASS** | Spacelike gate order is foliation-independent; remote marginals obey no signaling; no `u_S` exists. |
| F4 bounded memory | **PASS** | Finite `ln d` bounds stored entropy and finite `nu_max` bounds active load for sites and particles. |
| F5 universality / sign | **PASS** | Positive bilateral gate demand cannot phase-cancel; every local clock sees `A=1-q`. |
| F6 independent prediction | **PASS** | Shared patches may correlate without remote marginal change; particles sharing a site have one collectively saturating service budget. |

## Completed work

- froze the C0--C3 classical candidate ladder and all six gates;
- defined and tested dimensions, causal propagation, damping, reservoir energy,
  bounded classical memory and coordinate-speed controls;
- retained C3's preferred-frame failure as a negative result;
- separately preregistered C4 after the owner identified global state plus
  local causality as a distinct ontology;
- defined the global screen, effective subalgebras and causal bulk encoding;
- separated state capacity, update capacity, content, write rate and memory;
- assigned the same state/update capacities to topological sites and moving
  particles and closed the bilateral write ledger;
- reconciled every relocation write with Paper III: reversible writes need not
  produce global entropy, while entangling writes raise reduced entropy;
- added executable microcausality, no-signaling, foliation, four-momentum,
  phase, capacity and bounded-drive controls;
- generated a hash-pinned machine receipt without galaxy, lensing, cluster or
  cosmology inputs.

## Independent predictions carried into H-SSV-II

1. Shared effective patches may have connected screen correlations, but a
   unilateral perturbation cannot change the remote marginal before causal
   contact.
2. Particles mapped to one topological site share its finite update service;
   their availability is correlated and collectively saturating.
3. Below capacity positive demands add; at capacity response is subadditive by
   saturation, not destructive interference.

## Scope boundary

This is a foundation pass, not a gravity pass. C4 does not yet derive a
continuum response/Green function, the magnitude of any coupling, Newtonian or
cored-logarithmic limits, a spatial metric, lensing, a galaxy relation or
cosmology. Those claims remain prohibited until their later gates are met.

Verification is intentionally scoped to `instruments/test/model_hssv`. The
archived full-series numerical batteries are on hold and are not part of this
independent H-SSV audit.

# Proton closure gate (iii) pre-registration:
# recovery from non-trefoil-parameterised seeds

**Date:** 2026-05-30. Written BEFORE running any relaxation, so the
decision rule cannot be tuned to the result. Picks up the third gate
listed in `papers/SSV-I/static-3d-closure-status-2026-05-28.md`:

> "Recovered from multiple nearby initial conditions | not yet |
> Topology-penalty pipeline preserves the seeded trefoil but has not been
> seeded from non-trefoil initial conditions."

This pre-registration tests two distinct things the closure memo's gate
(iii) language conflates:

  (iii-a) **Same-topology basin of attraction.** Does the relaxer
  converge to the same final state (same energy, F, $N_Y$) when seeded
  from different parameterisations or perturbations of the trefoil knot?

  (iii-b) **Trefoil-vs-other-torus-knot comparison.** With the topology
  penalty enabled, do other torus knots ((2,5), (3,2), etc.) produce
  comparable observables under the same relaxer, or is the trefoil
  specifically picked out as energetically favourable in some sense?

(iii-a) is the literal "recovery" test in the closure memo. (iii-b) is
a strictly stronger test of trefoil specialness.

## States and seeds

The standard seed (used by all existing saved states) is a (2,3) torus
knot via `trefoil_curve(...)`:

  x(t) = (R_M + r_m cos(3t)) cos(2t)
  y(t) = (R_M + r_m cos(3t)) sin(2t)
  z(t) = r_m sin(3t)

with R_M = 2.8 xi (major), r_m = 0.85 xi (minor). The general (p, q)
torus knot replaces (2, 3) with (p, q):

  x(t) = (R_M + r_m cos(q t)) cos(p t)
  y(t) = (R_M + r_m cos(q t)) sin(p t)
  z(t) = r_m sin(q t)

Five seeds tested:

| label | (p, q) | R_M | r_m | topology | purpose |
|-------|--------|-----|-----|----------|---------|
| REF       | (2, 3) | 2.8 | 0.85 | (2,3) trefoil | reference (matches existing state) |
| REPARAM   | (3, 2) | 2.8 | 0.85 | (3,2)=(2,3) trefoil topologically | (iii-a): same knot, alternate parameterisation |
| PERTURB   | (2, 3) | 3.0 | 0.70 | (2,3) trefoil | (iii-a): same knot, perturbed geometry |
| FIVEKNOT  | (2, 5) | 2.8 | 0.85 | (2,5) torus knot (cinquefoil) | (iii-b): different topology, same scale |
| SEVENKNOT | (2, 7) | 2.8 | 0.85 | (2,7) torus knot | (iii-b): more crossings, same scale |

All five seeds run at n=24, hw=6, lambda_perp=2000, penalty_mu=400,
max_steps=800. These are the same parameters as the reference saved
state `penalty-mu400-rho0p01-n24-hw6-1600steps-2026-05-18.npz`, except
the step count is halved (800 vs 1600) to control compute -- if the
800-step result is already well-converged on the reference seed, that
validates the 800-step budget; if not, we report this as a limitation.

## What we extract per relaxation

For each final state:
- Total energy (final_energy_full)
- F at the canonical R = 1.18 xi (f_factor_straight_int)
- mu_0_str(R=1.18)
- n_y_straight (the dimensionful line integral, NOT the topological N_Y)
- effective_radius, deficit_volume (geometric checks)
- final_vortex_links (topology-preservation check)
- stop_reason (did the run hit max_steps or converge?)

## Pre-registered decision rules

For (iii-a) -- same-topology basin of attraction:

**PASS-A** iff REF, REPARAM, PERTURB all give:
- final_energy_full within 5% of each other
- F(R=1.18) within 5% of each other
- All three preserve the seeded trefoil topology (final_vortex_links
  stays close to initial_vortex_links throughout the run, or at minimum
  ends with a count consistent with a single closed knot)

**FAIL-A** iff any of these spreads exceed 10%, or any of the three
runs catastrophically loses topology (final_vortex_links drops to <5).

**AMBIGUOUS-A** for spreads in 5-10%.

For (iii-b) -- knot comparison:

This is NOT a pass/fail test (different knots are expected to give
different observables). Instead, we report:

- The ratio E(FIVEKNOT) / E(REF) and E(SEVENKNOT) / E(REF). For pure
  vortex-tension knots, energy scales with curve length; the (2,5) has
  ~longer curve than (2,3), so E(FIVEKNOT) > E(REF) is expected.
- Whether F(R=1.18) is comparable across knot types. The form factor F
  is a function of the breather's interior energy density and is not
  obviously topology-dependent at leading order; substantial F variation
  across knot types would argue against the "F is geometric" framing of
  the proton mass formula.
- Whether N_Y_str scales with the topological crossing count
  (3, 5, 7 for (2,3), (2,5), (2,7)). If yes, the line-integral N_Y is
  tracking topology; if no, the relation is more complex.

## What this does NOT settle

- The N_Y_topological = 3.007 value used in the proton mass formula
  (different observable from n_y_straight).
- Whether the trefoil is the absolute ground state across all topologies
  (the penalty enforces a topology floor; without the penalty, the
  relaxer would just unwind everything to vacuum).
- Cross-grid convergence (this is at n=24 only -- the smaller cost
  pre-registers; if results are interesting, n=48 could follow as a
  separate test).
- The cutoff R = 1.18 xi question (already addressed by the
  proton-geometric-r diagnostic on this branch).

## Compute budget

Estimated 5-10 minutes per relaxation at n=24, 800 steps; ~30-60 min
total for all 5 seeds. Acceptable.

## Outcome commitment

Whatever the relaxations produce goes into the result note verbatim,
with the per-state table of observables and the PASS-A / FAIL-A /
AMBIGUOUS-A verdict applied without adjustment. The (iii-b)
descriptive observations are reported but do not trigger a binary
verdict.

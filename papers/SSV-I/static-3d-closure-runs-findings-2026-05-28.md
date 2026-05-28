# Static 3D Closure Runs — Results and Honest Conclusions (2026-05-28)

**Status:** results memo for the three closure runs identified in
`static-3d-closure-status-2026-05-28.md` §5 (issue
[#13](https://github.com/StigNorland/SVT/issues/13) follow-up).

This note records what the closure runs actually produced today. The
headline result is **closure-negative**: the cutoff-invariance route
for promoting `N_Y` and `F` from candidate to derived is empirically
falsified at the current pipeline configuration. The Paper I
candidate-grade status is reaffirmed and the path to closure is
narrowed by the result.

## Run executed: cutoff-invariance + cross-grid sweep

**Script:** `src/paper_i/static_closure_cutoff_invariance_sweep.py`
(committed today).
**Data:** `papers/SSV-I/data/static-closure-cutoff-sweep-2026-05-28.csv`
(42 rows: 6 topology-preserving NPZ states × 7 cutoff values
`R ∈ {0.5, 0.8, 1.0, 1.18, 1.5, 2.0, 3.0} ξ`).
**Compute cost:** 307 s on the existing topology-penalty NPZ states; no
fresh 3D relaxation needed.

The sweep simultaneously addresses **Run 2** (cutoff-invariance of
`N_Y·F`) and **Run 1** (cross-grid `N_Y` sweep) by computing the
straight-vortex calibrated observables at each `(state, R)`.

## States used

All six are topology-preserving NPZ saved states from the May 18–19
penalty-mechanism campaign:

| Label | n³ | half-width | μ_penalty | ρ_target | min_density |
|---|---:|---:|---:|---:|---:|
| n24_mu1000          | 24³ | 6 | 1000 | (default) | 1.01e-4 |
| n24_mu400_rho001    | 24³ | 6 |  400 | 0.01      | 1.05e-4 |
| n48_best            | 48³ | 6 |  (best of penalty-expansion sweep) | | 1.19e-7 |
| n48_mu1000          | 48³ | 6 | 1000 | (default) | 2.20e-5 |
| n48_mu2500_rho005   | 48³ | 6 | 2500 | 0.05      | 3.83e-5 |
| n72_mu2000_rho005   | 72³ | 6 | 2000 | 0.05      | 1.18e-4 |

## Result A: N_Y · F is NOT cutoff-invariant

For every state, sweeping `R` from `0.5 ξ` to `3.0 ξ`, the product
`N_Y · F` decreases monotonically and smoothly with `R`. The
`max/min` ratio across the swept range is **identical to 31.5× in every
state** (a clean scaling signature — `N_Y` and `F` both scale uniformly
with the straight-vortex calibration over the same R range, so the
product's R-dependence is fixed by the calibration, not by the
breather physics).

This rules out the cutoff-invariance route for promoting
`N_Y · F` from candidate to derived:

- **There is no R at which `N_Y · F` is stationary in R.** The
  derivative `d(N_Y·F)/dR` is everywhere negative in the swept range.
- **The R-dependence is not a small correction.** A factor of 31.5×
  across R = 0.5..3 is structural; no choice of cutoff makes
  `N_Y · F` independent of the cutoff.

The original hypothesis -- that `N_Y` and `F` might each depend on `R`
but their product would be cutoff-invariant -- is empirically falsified.

## Result B: cross-grid spread at fixed R = 1.18 is large

At the canonical paper cutoff `R = 1.18 ξ`, the six topology-preserving
states give:

| Label | N_Y | F | N_Y·F |
|---|---:|---:|---:|
| n24_mu1000          | 46.6 |  3.08 |   143.5 |
| n24_mu400_rho001    | 47.8 |  5.61 |   268.1 |
| n48_best            | 72.4 | 10.65 |   770.8 |
| n48_mu1000          | 57.0 | 10.12 |   577.2 |
| n48_mu2500_rho005   | 68.1 | 10.48 |   713.9 |
| n72_mu2000_rho005   | 70.4 | 14.90 |  1048.7 |

Cross-state spread at R = 1.18:

- `N_Y`     spans 46.6 .. 72.4    (**35.6%** spread)
- `F`       spans  3.08 .. 14.90  (**79.3%** spread)
- `N_Y · F` spans 143.5 .. 1048.7 (**7.31×** spread)

No tolerance band in the
`trefoil-breather-minimisation-plan.md` validation gates is satisfied.
The penalty configuration (`μ_penalty`, `ρ_target`) materially changes
the converged observable values, even at the *same* grid: `n=48 best`
vs `n=48 mu=1000` differ by 25% in `N_Y · F` (770.8 vs 577.2).

## Result C: Run 3 is moot at the current configuration

The closure-status memo's Run 3 was "recovery of the same converged
`N_Y` and `F` from an independent initial condition". With cross-grid
spread of 35–79% on the *same* initial condition family across
different penalty configurations and grid resolutions, recovering "the
same converged values" from a different IC is not a well-posed test
yet -- there is no single converged value to test against. Run 3 is
shelved until either cross-grid stability is achieved at fixed IC
(Run 1 closure), or the geometric-cutoff path is replaced with a
different observable definition.

## Result D: the no-penalty / penalty discrepancy

The earlier `f-factor-grid-converged-checkpoint.md` finding that
"n=48 and n=72 agree to within 6% at every R" referred to
**no-penalty** Krylov-implicit runs -- the same runs that
`topology-penalty-checkpoint.md` later proved have **zero vortex
links** (the apparent vortex structure was a density inhomogeneity
without phase winding, fooling the `min_rho` proxy).

The penalty-preserving states used in today's sweep -- the only ones
with verified non-trivial topology (50 vortex links at n=24/μ=1000
per topology-penalty-checkpoint.md) -- give substantially **larger**
`F` than the no-penalty states at the same cutoff. At `R = 1.0 ξ`:

- no-penalty (per `f-factor-grid-converged-checkpoint.md`):
  `n=48` F = 4.897, `n=72` F = 5.210
- penalty-preserving (this sweep):
  `n48_best` F = 12.56, `n72_mu2000_rho005` F = 17.57

This is a factor of ~3 difference in `F` between topologically trivial
states and topologically valid states. The Paper I headline
`F ≈ 4.47 at R = 1.18 ξ` was extracted from no-penalty states; the
honest value at topologically valid states under the present pipeline
is in the 10–17 range and is not yet grid-converged.

This sharpens the Paper I claim status: the
`F ≈ 4.47` candidate value is conditional on a relaxation that does
not in fact preserve the trefoil topology. A topologically valid
candidate value exists but is currently far from cross-grid stable.

## Implications for Paper I claim status

The Paper I §"Claim Status" entries (commit `eb40440` under issue
#17) remain at **candidate**. Two refinements to the supporting prose
are warranted by today's findings, but the labels do not change:

1. The cutoff-invariance route is no longer a live promotion path.
   `static-3d-closure-status-2026-05-28.md` §5 lists three runs that
   *would* close #13. Run 2 (cutoff-invariance) has now been
   tested and shown not to hold; it should be removed from the
   promotion plan. Runs 1 and 3 remain but are not pursued because
   the underlying convergence question is not yet answered.

2. The relationship between the no-penalty `F ≈ 4.47` cited in Paper I
   and the penalty-preserving `F ≈ 10–17` measured today is not
   currently established. The Paper I number depends on a relaxation
   that lost the trefoil topology by step 100; the topology-valid
   number is not yet grid-converged. Honest framing: the proton-mass
   prediction `m_p ~ N_Y · F · μ_0 ~ 930-954 MeV` (commit `eb40440`
   abstract / §4.5) inherits both uncertainties and should be
   understood as the prediction at the no-penalty configuration with
   a separately open question about what the topology-valid
   configuration would give.

## What unblocks the static closure now

The blocking question is: **does the topology-penalty mechanism
produce a unique converged breather geometry under refinement, or
does the penalty itself fix part of the geometry?** The 35-79%
cross-state spread at fixed R = 1.18 is consistent with the latter --
the penalty parameters (`μ`, `ρ_target`) are influencing the
converged state, not just gating away topology-trivial relaxation
paths.

Three candidate paths forward, ranked by what they would establish:

1. **Refine within a single penalty configuration.** Pick one
   `(μ, ρ_target)` and run at n³ = 96³, 120³ with the same penalty
   parameters, then measure cross-grid spread. If the spread drops
   to <5% as the grid is refined, the penalty configuration is a
   convergence parameter (not a physical-state parameter) and the
   closure-grade pipeline is "the n→∞ limit at a fixed penalty
   recipe". If the spread stays at the 30-79% level, the penalty
   itself is fixing physics and a different topology constraint is
   needed.

2. **Replace the penalty with a winding-number projection.** The
   `refinement-gate-checkpoint.md` listed three topology-preservation
   strategies; the penalty was the first to work, but the
   winding-number projection (option 1) does not introduce a
   `(μ, ρ_target)` dependence and might give a topology-valid state
   whose convergence is governed by grid resolution alone.

3. **Drop the cutoff-invariance route entirely.** Pick a single
   geometric cutoff (e.g. `R = the radius at which |ψ|² = 0.5` of the
   relaxed breather) and report `N_Y · F` at that radius. This makes
   `R` a derived quantity of each grid's relaxed state, and asks the
   different question "does `N_Y · F` at the self-consistent cutoff
   converge under refinement?".

None of these are this-session work. They are the next concrete
items for whoever picks up the static-branch closure next.

## Honest status update

The candidate-grade label on `N_Y`, `F`, and the proton-mass
prediction was already correct in Paper I. Today's runs reaffirm
that label and remove one of the proposed promotion paths
(cutoff-invariance) from contention. The Paper I claim-status
language does not need re-editing; the Paper-I-side picture is
unchanged at the claim-label level. What changes is the **honest
expectation** of what closure-grade work would actually look like:
it is not a sweep at the existing penalty configuration but either a
refinement-in-grid study of one penalty recipe, or a topology
constraint that does not introduce extra free parameters.

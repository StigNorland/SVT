# Issue #13: n=96 cross-grid result — FAIL-A (2026-06-02)

**Status:** FAIL-A (pre-registered decision rule triggered).
**Script:** `src/paper_i/static_closure_n96_result.py`
**Data:** `papers/SSV-I/data/static-closure-n96-result-2026-06-02.json`
**NPZ:** `papers/SSV-I/data/penalty-n96-mu2000-rho0p05-400steps-2026-06-02.npz` (12 MB)

## Raw observables

| n | R (ξ) | N_Y | F | N_Y·F | min_ρ |
|---|---:|---:|---:|---:|---:|
| 72 | 1.18 | 70.404 | 14.896 | 1048.7 | 1.18e-04 |
| 96 | 1.18 | 103.073 | 22.149 | 2283.0 | 1.39e-04 |
| 72 | 0.923 | 90.519 | 19.152 | 1733.6 | 1.18e-04 |
| 96 | 0.923 | 132.522 | 28.478 | 3773.9 | 1.39e-04 |

## Decision rule outcome

Pre-registered gate: spread < 5% on N_Y and F at R = 1.18 → PASS.

| observable | n=72 | n=96 | spread | verdict |
|---|---:|---:|---:|---|
| N_Y at R=1.18 | 70.404 | 103.073 | **46.4%** | FAIL-A |
| F at R=1.18 | 14.896 | 22.149 | **48.7%** | FAIL-A |
| N_Y·F at R=1.18 | 1048.7 | 2283.0 | **117.7%** | FAIL-A |

## Scaling analysis

Both N_Y and F grow as n^α where α ≈ 1.35:

```
N_Y: 103.073 / 70.404 = 1.464  =>  α = log(1.464)/log(96/72) = 1.33
F:    22.149 / 14.896 = 1.487  =>  α = log(1.487)/log(96/72) = 1.38
```

Power-law growth with α > 1 (rather than convergence toward a limit) means
the observables reflect the number of grid points in the vortex core, not a
converged geometric quantity. The penalty solver preserves vortex topology
(links intact at both resolutions) but does not constrain the relaxed geometry
to a grid-independent fixed point.

## Root cause

Same as Runs 2 and 3: the soft-penalty Krylov relaxer defines a family of
topology-preserving states parameterised by both the penalty config (μ,
ρ_target) **and the grid spacing**. Neither is a convergence parameter in
isolation. Grid refinement at fixed (μ, ρ_target) traces a trajectory through
state space that does not converge — N_Y and F grow roughly linearly with
resolution.

## Summary: all three runs exhausted

| Run | Description | Result |
|---|---|---|
| Run 2 | Cutoff-invariance: sweep R = 0.5..3 ξ | FAIL: 31.5× spread, no stationary point |
| Run 3 | Self-consistent R_sc = 0.923 ξ | FAIL: 60.6% spread, same root cause |
| Run 1 | Cross-grid at fixed (μ=2000, ρ=0.05), n=72→96 | FAIL-A: 46–48% spread, n^1.35 scaling |

All three pre-registered routes for issue #13 have now been exhausted.
The proton N_Y·F product is not accessible via the current penalty-Krylov
static solver. A topology-preserving solver with geometric invariance under
grid refinement is needed before closure-grade proton observables are possible.

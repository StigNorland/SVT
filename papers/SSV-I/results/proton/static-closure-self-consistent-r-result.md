# Issue #13 Run 3: Self-Consistent R — Results (2026-06-02)

**Status:** result note for
[issue #13](https://github.com/StigNorland/SVT/issues/13), Run 3 (self-consistent R).
Reproducer: `python instruments/paper_i/static_closure_self_consistent_r.py`
Data: `papers/SSV-I/data/static-closure-self-consistent-r-2026-06-02.json`

## Design

The empirical cutoff R = 1.18 ξ used to calibrate the straight-vortex tension
`mu_0_straight` was shown by the May 2026 sweep to produce N_Y·F values that
vary by 35–79% across penalty configurations.  This run tests whether replacing
R = 1.18 ξ with the self-consistent vortex-profile cutoff R_sc — the radius at
which the LogSE straight-vortex profile crosses |ψ|² = 0.5 — reduces the spread.

## R_sc derivation

From `VortexProfile.solve()` at log_pressure = 0.5 (the static-branch canonical
value):

```
R_sc = 0.92314 ξ   (first-principles, no free parameter)
```

This is the half-density radius of the LogSE vortex.  It is the natural scale
beyond which a neighbour vortex's contribution to the local density exceeds the
local vortex's contribution, so the straight-vortex calibration integral should
not extend further without double-counting.

## Results at R_sc = 0.923 ξ

| Label | n | mu_penalty | rho_target | N_Y | F | N_Y·F | min_rho |
|---|---:|---:|---:|---:|---:|---:|---:|
| n24_mu400_rho001 | 24 | 400 | 0.01 | 61.5 | 7.21 | 443 | 1.04e-4 |
| n48_best | 48 | — | — | 93.1 | 13.69 | 1274 | 1.19e-7 |
| n48_mu1000 | 48 | 1000 | — | 73.3 | 13.01 | 954 | 2.20e-5 |
| n48_mu2500_rho005 | 48 | 2500 | 0.05 | 87.5 | 13.48 | 1180 | 3.83e-5 |
| n72_mu2000_rho005 | 72 | 2000 | 0.05 | 90.5 | 19.15 | 1734 | 1.18e-4 |

**Cross-grid spread at R_sc (n ≥ 48): 60.6%**
Closure gate (< 5%): **FAIL**

## Interpretation

Changing from the empirical R = 1.18 ξ to the self-consistent R_sc = 0.923 ξ
does not materially reduce the cross-state spread.  At R = 1.18, the spread was
79% on F and 35% on N_Y; at R_sc = 0.923, the spread remains ~60% on N_Y·F.

This confirms the conclusion of the May 2026 cutoff-invariance sweep:

> The dominant source of N_Y·F variation is not the choice of cutoff radius.
> It is the penalty configuration (μ, ρ_target) influencing the converged
> 3D state geometry.

**Path 3 (self-consistent R) does not unblock the static closure.**  The
blocking question remains: does the topology-penalty mechanism produce a unique
converged breather geometry under grid refinement, or does the penalty itself
fix part of the geometry?

## Consistent finding across all three closure runs (issue #13)

| Run | Approach | Result |
|---|---|---|
| Run 2 (May 2026) | Cutoff-invariance: test if N_Y·F(R) is stationary | **FAIL** — N_Y·F varies by 31.5× across R = 0.5..3 ξ; never stationary |
| Run 1 (May 2026) | Cross-grid at fixed penalty: n=24..72 at R=1.18 | **FAIL** — 35–79% spread across penalty configs at same grid |
| Run 3 (this note) | Self-consistent R_sc = 0.923 ξ | **FAIL** — 60.6% spread; same root cause as Run 1 |

## What remains to unblock #13

The path forward is **Path 1 from static-3d-closure-runs-findings-2026-05-28.md**:

> Refine within a single penalty configuration.  Pick one (μ, ρ_target) and
> run at n³ = 96³, 120³ with the same penalty parameters, then measure
> cross-grid spread.  If the spread drops to <5% as the grid is refined, the
> penalty configuration is a convergence parameter (not a physical-state
> parameter) and the closure-grade pipeline is "the n→∞ limit at a fixed
> penalty recipe".

A n=96, mu=2000, rho=0.05 run was started (alongside this note) to provide the
first data point for Path 1.  See `static-closure-n96-result.md` when that run
completes.

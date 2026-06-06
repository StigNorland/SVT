# Pre-registration: n=96 cross-grid refinement for issue #13 (2026-06-02)

**Type:** pre-registered run.
**Status:** running (started 2026-06-02 ~15:29 CEST).
**Script:** `trefoil_breather_lperp_krylov_static.py`

## Run parameters

```
--n 96 --half-width 6
--penalty-mu 2000 --penalty-rho-target 0.05
--max-steps 400
--save-state papers/SSV-I/data/penalty-n96-mu2000-rho0p05-400steps-2026-06-02.npz
--output    papers/SSV-I/data/penalty-n96-mu2000-rho0p05-400steps-2026-06-02.json
```

Penalty config matches the existing n=72 state
(`penalty-n72-mu2000-rho0p05-2026-05-19.npz`), enabling a direct matched
cross-grid comparison at one fixed (mu, rho_target).

## Pre-registered decision rule

**PASS (closure-gate met):** |N_Y(n=96) - N_Y(n=72)| / N_Y(n=72) < 5%
AND |F(n=96) - F(n=72)| / F(n=72) < 5% at R = 1.18 ξ.

If both conditions hold, the penalty config is a convergence parameter
and the n→∞ limit at (mu=2000, rho=0.05) is a candidate closure-grade
pipeline.

**FAIL-A:** Spread ≥ 5% — penalty parameters still influence the
converged geometry; not closure-grade.

**FAIL-B:** Topology collapses (final vortex links < 5) — the penalty
is insufficient at n=96; need stronger penalty or topology-preserving
solver.

## Context

The three closure runs to date have all failed at different levels:
- Run 2: cutoff-invariance falsified (31.5× spread across R = 0.5..3)
- Run 1: cross-grid spread 35–79% across *different* penalty configs
- Run 3: self-consistent R_sc = 0.923 ξ shows 60.6% spread (same root cause)

This run is the first matched cross-grid test (same mu, rho_target) and
is the decisive test for whether the penalty mechanism converges under
grid refinement.

## Expected compute time

~2 hours wall time at 7–8 cores on the development machine.
Results to be recorded in `static-closure-n96-result.md`.

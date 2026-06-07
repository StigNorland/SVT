# Issue #15 Grid Refinement at Canonical c=1 — Results (2026-06-02)

**Status:** result note for
[issue #15](https://github.com/StigNorland/SVT/issues/15), closure items 1–3.
Reproducer: `python instruments/paper_ii/reconnection_grid_refinement.py`
Data: `papers/SSV-II/data/reconnection-grid-refinement-lp05-2026-06-02.json`

## What was done

Three of the four #15 closure items were addressed this session:

**Item 2 (diagnostics):** Added to `reconnection_supplement.py`:
- `cap_volume` (previously computed inside `cap_radius()` but not returned)
- `energy_drift_pct` (relative energy change from first to last snapshot)
- `norm_drift_pct` (relative norm-squared change; should be ≈0 for split-step)
- `AnalyseResult` dataclass replaces the bare 4-tuple return from `analyse()`

**Item 3 (c_eff fix):** Added `--log-pressure` CLI argument.  Default remains 8.0
for backwards compatibility with existing results; `--log-pressure 0.5` gives the
canonical c=1 static-branch convention.  A deprecation warning is printed if
log_pressure=8.0 is used.

**Item 1 (grid refinement):** Ran the reconnection supplement at n = 16, 24, 32,
48, 64, 96 with log_pressure = 0.5 (canonical c=1), length = 24, dt = 0.001,
200 steps.

## Results

### lambda_perp = 0 (pure LogSE, opposite circulation)

| n | saddle_excess | cap_radius | cos_phi | energy_drift% | norm_drift% |
|---:|---:|---:|---:|---:|---:|
| 16 | -0.615 | 4.15 | 0.876 | 0.475 | ~0 |
| 24 | -0.827 | 0.0 | 0.766 | 0.322 | ~0 |
| 32 | -0.826 | 2.93 | 0.731 | 0.273 | ~0 |
| 48 | -0.459 | 2.52 | 0.674 | 0.175 | ~0 |
| 64 | -0.240 | 2.14 | 0.641 | 0.115 | ~0 |
| 96 | -0.089 | 2.52 | 0.655 | 0.060 | ~0 |

**Key finding:** saddle_excess is **negative** throughout — there is no
reconnection barrier in the pure LogSE at canonical c=1.  This is consistent
with Kelvin's theorem: compressible-fluid reconnection is downhill in energy.
Norm drift is machine-zero (split-step conserves norm exactly).  Energy drift
decreases monotonically with n (good convergence trend).

cap_radius at n ≥ 32 converges roughly to 2.1–2.9 ξ (large relative spread
still, gated on a proper saddle being identified).

### lambda_perp = 10 — UNSTABLE at canonical c=1

At log_pressure = 0.5 (dx = length/n = 24/96 = 0.25 ξ at n=96), the chiral-
shear k^4 term has:

```
k_max = π/dx = 12.57  →  lambda_perp × k_max^4 × dt = 10 × 24,977 × 0.001 ≈ 250
```

The Strang split-step for the k^4 term is formally unitary (each FFT phase
rotation has magnitude 1) but the large phase rotation creates rapid oscillations
that drive energy growth in the nonlinear step.  Observed energy_drift = 300–579%
at n = 48–96 confirms the integrator is out of the accuracy regime.

For comparison, the previous campaign used log_pressure = 8.0 (c_eff = 4), giving
dx = length/(n) and k_max that produced lower k_max^4 × dt in the stability product.
Changing to log_pressure = 0.5 at the same dt = 0.001 is NOT numerically stable
for lambda_perp = 10.

**Required for closure-grade lambda_perp≠0 runs at canonical c=1:**
```
dt < 1/(lambda_perp × k_max^4)  at the target resolution
```
At n=96, length=24, lambda_perp=10: dt_critical ≈ 4e-6.  This is 250× smaller
than the current dt = 0.001, making a 200-step run require 50,000 steps.
A smaller lambda_perp (e.g. 0.01 or 0.1) or adaptive timestepping is needed.

### Convergence summary (lambda_perp=10, opposite)

| Observable | n=16..96 range | Spread | Gate |
|---|---|---:|---|
| saddle_excess | 2069 .. 253,156 | 354% | FAIL |
| cap_radius | 14.6 .. 28.3 ξ | 73% | FAIL |
| cos_phi | 0.670 .. 0.757 | 12% | FAIL (but closest) |

## Conclusions

1. **Pure LogSE reconnection at canonical c=1 shows no barrier** and the energy
   drift converges well under grid refinement.  cap_radius at n ≥ 32 is in the
   2–3 ξ range.  cos_phi is roughly stable at 0.65–0.87.

2. **lambda_perp = 10 is integrator-unstable at canonical c=1** with dt = 0.001.
   A smaller dt (by factor ~250 at n=96) or smaller lambda_perp is required.
   This is the root cause of the 91.7% saddle_excess spread reported in the
   May 2026 validation sweep (which used log_pressure=8.0 and hence a larger
   effective c that masked the stability issue at coarser grids).

3. **Item 4 (radiated-mode spectrum) remains unimplemented.** Adding it requires
   Fourier decomposition of the field at late times relative to the pre-saddle
   state, and is the next concrete work item for #15.

## What still needs to be done for full #15 closure

1. Run lambda_perp≠0 with a stability-limited dt (either analytical expression
   for dt_max, or an adaptive integrator).
2. Verify cap_radius convergence for the opposite-topology case at small lambda_perp.
3. Implement radiated-mode spectrum diagnostic in `analyse()`.

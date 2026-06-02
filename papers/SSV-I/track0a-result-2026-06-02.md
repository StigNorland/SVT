# #77 Track 0a result: cutoff sweep — FAIL (2026-06-02)

**Pre-registered gate:** spread < 5% on `n_y_straight` (n=72 vs n=96) at any R_cutoff.
**Verdict:** FAIL at all R_cutoff values tested.

## Summary table

| R_cutoff | n_y_straight spread | n_y_per_curve spread | n_y_phys spread | N_Y×F spread |
|---|---|---|---|---|
| 1.18 (baseline) | 37.7% | 6.2% | 37.7% | 64.1% |
| 1.50 | 37.7% | 6.2% | 37.7% | 64.1% |
| 2.00 | 37.7% | 6.2% | 37.7% | 64.1% |
| 2.50 | 37.7% | 6.2% | 37.7% | 64.1% |
| 3.00 | 37.7% | 6.2% | 37.7% | 64.1% |

## Why the spread is R_cutoff-independent

`n_y_straight = (e_line + e_cavity) / mu_0_straight(R_cutoff)`.
With r_tube = 1.5 fixed, the numerator `e_line + e_cavity` does not change with
R_cutoff — only the denominator does. The relative spread |N_Y(96) - N_Y(72)| /
mean(N_Y) is therefore calibration-invariant: any overall rescaling of mu_0 cancels.

Track 0b (physics-based mu_0 from ring formula with C_LogSE = 1.880) has the same
invariance: mu_0_phys(R_ring) = pi*(ln(8*R_ring) - 1.880) is the same constant for
both states (major_radius = 2.800 in both), so the spread is unchanged.

## Root cause (confirmed)

The n=72 and n=96 states are **genuinely different physical configurations**, not
the same trefoil at two grid resolutions. The penalty-Krylov relaxation converges to
a resolution-dependent geometry. No post-hoc calibration change can fix this.

## One informative result

`n_y_per_curve_length` (arc-length normalised) gives 6.2% spread vs 37.7% for
`n_y_straight` — a 6× improvement. This observable eliminates the arc-length
growth from the tube volume and uses the cal-slab mu_0_grid instead of the
straight-vortex calibration. If a solver could produce the **same geometry** at
both resolutions, `n_y_per_curve_length` would likely pass the 5% gate.

## Next step: Track 2 (imaginary-time gradient flow)

Track 0 and Track 1 are both exhausted on existing states. The fix must come from
the solver: produce geometrically-converged states before extracting observables.
See issue #77 for the Track 2 plan.

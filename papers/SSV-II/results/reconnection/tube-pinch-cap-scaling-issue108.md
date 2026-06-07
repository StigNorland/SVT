# Tube-pinch cap lambda-scaling diagnostic (#108)

**Issue:** #108, linked from #97.
**Script:** `instruments/paper_ii/tube_pinch_cap_harness.py --scaling`.

## Method

Each `(lambda_perp, n)` trajectory uses the short-cap ansatz and is evolved
to a common physical duration `T = 0.10` with `65` saved frames. The
measured event is the first prefix that passes the pre-registered cap-event
gate. This preserves a fixed-duration evolution while allowing the cap
opening/closing time to drift with `lambda_perp`.

The scaling test fits the event-gated maximum cap radius against
`sqrt(lambda_perp)`. The through-origin fit is the literal
`R_cap = A sqrt(lambda_perp) xi` test; a free-intercept line is recorded
only as a diagnostic.

## Event Windows

| n | lambda_perp | event t | R0 | max R | R/R0 | closing | localization |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 24 | 0.5 | 0.0250 | 2.121 | 5.648 | 2.663 | 0.173 | 0.155 |
| 24 | 1 | 0.0484 | 3.000 | 8.029 | 2.676 | 0.198 | 0.134 |
| 24 | 1.4 | 0.0438 | 3.550 | 7.877 | 2.219 | 0.038 | 0.124 |
| 24 | 2 | 0.0250 | 4.243 | 8.381 | 1.976 | 0.037 | 0.173 |
| 24 | 2.8 | 0.0250 | 5.020 | 9.532 | 1.899 | 0.059 | 0.187 |
| 24 | 4 | 0.0203 | 6.000 | 10.261 | 1.710 | 0.088 | 0.184 |
| 32 | 0.5 | 0.0406 | 2.121 | 8.068 | 3.803 | 0.269 | 0.149 |
| 32 | 1 | 0.0312 | 3.000 | 7.173 | 2.391 | 0.045 | 0.123 |
| 32 | 1.4 | 0.0453 | 3.550 | 7.868 | 2.216 | 0.058 | 0.121 |
| 32 | 2 | 0.0188 | 4.243 | 8.660 | 2.041 | 0.064 | 0.171 |
| 32 | 2.8 | 0.0188 | 5.020 | 9.687 | 1.930 | 0.052 | 0.175 |
| 32 | 4 | 0.0203 | 6.000 | 10.228 | 1.705 | 0.074 | 0.166 |
| 40 | 0.5 | 0.0375 | 2.121 | 7.992 | 3.767 | 0.109 | 0.147 |
| 40 | 1 | 0.0328 | 3.000 | 7.352 | 2.451 | 0.221 | 0.134 |
| 40 | 1.4 | 0.0406 | 3.550 | 7.797 | 2.197 | 0.235 | 0.137 |
| 40 | 2 | 0.0234 | 4.243 | 8.336 | 1.965 | 0.168 | 0.173 |
| 40 | 2.8 | 0.0141 | 5.020 | 9.498 | 1.892 | 0.032 | 0.177 |
| 40 | 4 | 0.0203 | 6.000 | 10.199 | 1.700 | 0.066 | 0.163 |

## Fits

| grid | pass count | origin slope | origin RMS % | free slope | free intercept | free RMS % |
|---|---:|---:|---:|---:|---:|---:|
| n=24 | 6 | 5.955 | 16.86 | 3.248 | 3.970 | 6.23 |
| n=32 | 6 | 6.077 | 21.88 | 2.178 | 5.718 | 6.43 |
| n=40 | 6 | 6.009 | 22.21 | 2.075 | 5.770 | 5.75 |
| combined | 18 | 6.014 | 20.46 | 2.500 | 5.153 | 7.68 |

## Verdict

The event-gated cap radius does **not** support the literal through-origin
`R_cap = A sqrt(lambda_perp) xi` scaling in this desktop harness. The
through-origin RMS residual is `16.9%`, `21.9%`, and `22.2%` on
`n=24,32,40`, respectively; the combined residual is `20.4%`. The ratio
`R/R0` decreases from about `3.8` at small `lambda_perp` to about `1.7` at
`lambda_perp=4`.

A free-intercept line fits much better, which means the measured radius
contains a large additive/core/box-scale component rather than being a
pure inherited-throat scaling. This falsifies the desktop route-C scaling
cross-check for the current tube-pinch ansatz; it does not alter the
analytic W-scale argument in #105.

## Box-contamination diagnostic (takeover, 2026-06-07)

The free-intercept floor `B ≈ 5 ξ` above is **not** a core scale — it is the
**box**. Holding the physics fixed (`lambda_perp=2`, `kappa=3`, throat
`R0 = 4.243 ξ` constant) and the resolution fixed (`dx = 0.75`), and enlarging
*only* the box (`length/n` constant), the measured cap radius grows with the box
while its localization collapses and the cap-event gate fails
(`box_contamination_sweep`, `test_tube_pinch_box_contamination.py`):

| length | n | box/2 | max R_cap | localization | cap-event |
|---|---|---|---|---|---|
| 18 | 24 | 9.0  | 8.38 ξ  | 0.177 | pass |
| 27 | 36 | 13.5 | 10.93 ξ | 0.112 | fail |
| 36 | 48 | 18.0 | 15.91 ξ | 0.080 | fail |

`R_cap` tracks the **box** (≈ box/2), not the fixed throat `R0 = 4.24 ξ`. So the
depletion in this ansatz is a box-confined structure, not a localized cap: the
moment `sqrt(2<rho^2>_w)` picks up the box scale, and the "cap event" only passes
in the small box where the structure fills enough of the domain to look
localized. The `~20%` through-origin scaling residual is therefore a
**box-contamination artefact**, and even the cap-existence "pass" at `length=18`
is box-dependent.

## Refined verdict

The desktop route-C cross-check is **not a physical falsification of
inherited-ring scaling** — it is structurally unable to test it. A meaningful
test needs `core << R0 << R_cap << box` simultaneously; here `R0`, `R_cap`, and
`box/2` are all within a factor of ~2 of each other, so throat, cap, core, and
box are not separated. Achieving the separation (e.g. `R0 ~ 10-100 xi` in a box
several times larger, at `dx <~ xi`) is the same petascale requirement that
blocks the direct physical-`alpha` simulation (`n >~ 10^3` per side). Increasing
the grid `n` at fixed box does not help (it refines a fixed, contaminated domain;
the optional `n=64` point moved the convergence spread by `0.01%`).

**Status for #97/#108:** the dynamic route-C cross-check is **closed as
desktop-infeasible** (box-contaminated, not falsified). The #105 analytic result
— `W` mass *scale* derived from the inherited ring scale `R* = xi/alpha`, `phi` an
O(1) coincidence — stands unaffected; it never depended on this cross-check.

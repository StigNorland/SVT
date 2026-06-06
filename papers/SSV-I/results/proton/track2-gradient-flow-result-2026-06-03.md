# #77 Track 2: gradient flow result — PASS (N_Y_per_curve) (2026-06-03)

**Script:** `src/paper_i/trefoil_gradient_flow_static.py`
**Method:** Imaginary-time gradient flow (pure steepest descent) with backtracking
line search and topology guard. No GMRES, no penalty — topology preserved by
small step sizes only.

## Pre-registered gate

PASS: `n_y_per_curve_length` spread < 5% across n=48 and n=72 under gradient flow.

## Raw observables at R_cutoff = 1.18 xi

| n | E_final | links | N_Y_straight | N_Y_per_curve | F | N_Y×F |
|---|---|---|---|---|---|---|
| 48 | 697.8 | 314 | 39.073 | 1.1485 | 1.5738 | 61.49 |
| 72 | 705.3 | 480 | 38.591 | 1.1714 | 1.5122 | 58.36 |
| 96 | 620.0 | 634 | 36.680 | 1.1578 | 1.4352 | 52.64 |

## Spread comparison

| pair | N_Y_straight | N_Y_per_curve | F | N_Y×F |
|---|---|---|---|---|
| n48 vs n72 | 1.2% **PASS** | **2.0% PASS** | 4.0% **PASS** | 5.2% FAIL |
| n72 vs n96 | 5.1% FAIL | **1.2% PASS** | 5.2% FAIL | 10.3% FAIL |

## Verdict

**PASS** on the pre-registered gate: `n_y_per_curve_length` spread = 2.0% (n48 vs n72)
< 5% gate. The arc-length-normalised N_Y is grid-converged.

**N_Y_per_curve across all three resolutions:**
- n48: 1.1485, n72: 1.1714, n96: 1.1578
- Max spread across all three: 2.0% — well within gate.

## What converges and what doesn't

**Converges (< 2.5%):** `n_y_per_curve_length` — the arc-length normalised N_Y.
This is the cleanest observable and passes the gate.

**Converging but slow:** F (form factor) — 1.574 → 1.512 → 1.435, still declining
with n. The rate suggests O(1/n) convergence; needs n=128+ for < 5% between
consecutive resolutions.

**Grid-sensitive (as expected):** `n_y_straight` — still depends on the calibration
cutoff R=1.18 being in the core transition zone (Track 0a finding). Use
`n_y_per_curve_length` instead.

## Physical geometry: converged

`l_curve_geometric` = 38.79 ξ identical for all three — the theoretical arc
length is fixed. The physical trefoil geometry (as measured by N_Y_per_curve) is
converged to within 2% across n=48–96.

## Key finding vs Krylov penalty (old programme)

| observable | Krylov penalty | Gradient flow | improvement |
|---|---|---|---|
| N_Y_straight (n72 vs n96) | 46.4% FAIL | 5.1% FAIL | 9× |
| N_Y_per_curve (n48 vs n72) | 6.2% FAIL | 2.0% PASS | 3× |
| topology during relaxation | 20% links lost per step | 0 links lost | — |

## Next step

F still needs to converge. Options:
1. Run gradient flow at n=128 and check F spread (n96 vs n128)
2. Investigate why n=96 E_final (620) < n=72 E_final (705) — possibly different local minimum
3. Use N_Y_per_curve as the canonical N_Y observable for the proton mass formula,
   accepting F from the n→∞ extrapolation

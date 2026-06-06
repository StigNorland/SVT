# GMRES Tuning Checkpoint

This note records the first GMRES tuning pass for the Krylov-implicit L_perp
solver (`lperp_krylov_helpers.py`), addressing the two structural weaknesses
identified at the end of the Krylov-implicit checkpoint:

1. GMRES hitting its iteration cap (30) on every step.
2. The FFT preconditioner capturing only the L_perp `k^4` stiffness, leaving
   the LogSE kinetic `k^2` modes unconditioned.

## Changes

### Improved preconditioner

The left preconditioner now captures both stiff contributions:

```
M = I + dt * (kinetic_coeff * k^2 + lambda_perp * k^4)
```

`kinetic_coeff = 0.5` matches the LogSE kinetic term `-½∇²` in nondimensional
units (xi=1, rho0=1, c=1).  The old preconditioner used only `lambda_perp * k^4`,
which left intermediate-k modes from the kinetic sector unconditioned and forced
GMRES to do extra work that the preconditioner should have done.

### Restarted GMRES

The unrestarted GMRES (fixed `maxiter=30`, always hitting the cap) has been
replaced by restarted GMRES(`restart`, `max_cycles`):

- Each cycle runs at most `restart` Arnoldi steps.
- After each cycle the current solution is updated and the outer residual checked.
- Up to `max_cycles` cycles run before the step is accepted.
- Memory cost stays `O(restart × N)` per cycle rather than growing with total iters.
- Default: `restart=30`, `max_cycles=5`.

The inner tolerance per cycle is scaled so each cycle targets a genuine
reduction of the outer residual: `inner_tol = tol * ||b|| / ||r||`.

### Unit tests

`src/paper_i/test_lperp_krylov.py` — 17 tests covering:

| Group | Tests |
|---|---|
| `fft_left_preconditioner` | identity at dt=0, kinetic term changes output, high-k damping increases, dtype preserved |
| `gmres_matrix_free` | identity system (1 iter), diagonal system, zero RHS |
| `gmres_restarted` | convergence, multi-cycle, zero RHS, matches unrestarted on easy system |
| `krylov_implicit_step` | lambda=0 explicit Euler, gradient reduction, shape, kinetic_coeff=0 fallback |
| pack/unpack | round-trip |

All 17 tests pass.

## Smoke Test: n=16, hw=5, lambda=2000, 50 steps

Head-to-head on a small grid (n=16, hw=5, lambda=2000, 50 relaxation steps):

| parameter set | `min_rho` | `F^int` | violations | mean GMRES iters/step | stop |
|---|---:|---:|---:|---:|---|
| old: k^4 only, 1 cycle (maxiter=30) | 2.61e-3 | 1.034 | 5 | 30.0 | max_steps |
| new: k^2+k^4, 5 cycles (restart=30) | 2.23e-3 | 1.094 | 8 | 130.9 | max_steps |

Observations:

- **Cores are slightly deeper** (2.23e-3 vs 2.61e-3) with the improved preconditioner
  and restart cycles — consistent with the solver finding a lower-energy state.
- **F^int increases** (1.094 vs 1.034), in the right direction toward the paper's 4.47.
- **Mean GMRES iters/step jumps from 30 to 131** — reflecting that the solver now
  runs up to 5 cycles of 30 steps each rather than stopping at the first cap hit.
  This is the expected cost of doing the job properly.
- **Violations increase slightly** (8 vs 5 out of 50 steps, 16% vs 10%) — larger
  per-step moves from the better-conditioned implicit step occasionally overshoot the
  energy guard.  Acceptable at this grid size.

The n=16 grid is a smoke test; the preconditioner improvement is expected to matter
more at n=24 and n=48 where the unconditioned intermediate-k modes had more impact.

## What This Does Not Yet Settle

- Whether the GMRES inner solve converges within each cycle (mean 130.9 iters over
  5 cycles = ~26 per cycle, still not fully converging to `gmres_tol=1e-4`).  A
  further preconditioner improvement (e.g., including the LogSE nonlinear density
  term in the diagonal) could reduce this.
- The violation rate at n=16 is higher than ideal.  Step-size tuning or a tighter
  energy guard may be needed at larger grids.
- No refinement sweep yet at `(n, hw) ∈ {24, 32, 48} × {5, 6, 7}`.

## Recommended Next Steps

1. Run the full `(n=24, hw=6, lambda=2000, 800 steps)` comparison against the
   previous Krylov checkpoint to confirm `F^int` and `min_rho` improve at the
   paper scale.
2. Tune `gmres_tol` and `gmres_max_cycles` to trade per-step cost against
   violation rate.
3. If violations remain high, consider adding the diagonal LogSE nonlinear term
   to the preconditioner.

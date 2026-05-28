# Validation refinement and sensitivity sweeps — dynamic branch (2026-05-28)

**Status:** validation result for issue [#16] (dynamic side).
**Branch:** dynamic (Paper II / reconnection supplement).
**Baseline:** `src/paper_ii/reconnection_supplement.py` — the
prototype split-step LogSE/GPE harness for the W/Z reconnection-barrier
checks.
**Sweep harness:** `src/paper_ii/validation_sweep_reconnection_supplement.py`.
**Raw data:** `papers/SSV-II/data/validation-refinement-reconnection-2026-05-28.csv`.

This completes the dynamic side of issue [#16]; the static side
(restricted 2-mode BdG diagnostic) landed earlier in
[`papers/SSV-I/validation-refinement-sweeps-2026-05-27.md`].

## What was tested

For the reconnection_supplement at the reference configuration
`(n=32, length=18, dt=0.001, steps=200, log_pressure=8, lambda_perp=10)`,
the script varies one axis at a time and records the analyser outputs
`saddle_excess`, `cap_radius`, `cos_phi` for both topology classes
(opposite-circulation ring pair, same-circulation ring pair). An
observable is **stable** if the relative spread across the swept axis is
under 5%, otherwise **drifts materially**. The 5% threshold is set
deliberately looser than the static-side 1% gate because reconnection
analyses sit on a moving target (the time-dependent saddle); the goal
here is to surface gross non-convergence, not to gate paper-level
precision.

Sweep axes:

| Axis | Range | Points |
|---|---|---:|
| grid `n` | 16, 24, 32, 48 | 4 |
| `length` (box) | 12, 15, 18, 24 | 4 |
| `dt` (with `steps` adjusted to preserve total integration time) | 0.0005, 0.001, 0.002 | 3 |

Each axis runs both topologies; total 22 single-topology integrations,
total compute ~55 seconds.

## Headline findings

### 1. Grid is the dominant non-convergence axis

Relative spreads across `n = 16..48` at fixed `length=18, dt=0.001`:

| Observable | opposite | same |
|---|---:|---:|
| `saddle_excess` | **91.7%** drifts | 45.3% drifts |
| `cap_radius` | 44.6% drifts | 17.3% drifts |
| `cos_phi` | 12.0% drifts | **4.93% stable** |

`saddle_excess` swings by nearly a factor of 12 across the swept grids
for the opposite topology (1.08e4 → 1.29e5); `cap_radius` doubles
between n=16 and n=24 then plateaus. The only observable that meets
the 5% gate is `cos_phi` on the same-circulation topology, and even
that sits just barely under threshold.

### 2. Box-size sensitivity is comparable

Relative spreads across `length = 12..24` at fixed `n=32, dt=0.001`:

| Observable | opposite | same |
|---|---:|---:|
| `saddle_excess` | 76.3% drifts | 27.9% drifts |
| `cap_radius` | 42.5% drifts | 62.5% drifts |
| `cos_phi` | 32.5% drifts | 11.5% drifts |

No `length` value gives a stable read on any of the three observables
in either topology. The `cap_radius` swings show the rings interacting
with their periodic image at small `length` (the box is comparable to
the ring radius for `length=12`), so this drift is partly a
boundary-condition signature rather than an internal physics signal.

### 3. Time integration is closer to converged

Relative spreads across `dt = 0.0005..0.002` with `steps` adjusted to
preserve total integration time (`steps × dt = 0.2`):

| Observable | opposite | same |
|---|---:|---:|
| `saddle_excess` | **4.17% stable** | 5.72% drifts |
| `cap_radius` | **3.69% stable** | 11.4% drifts |
| `cos_phi` | 5.52% drifts | 7.03% drifts |

For the opposite-circulation case `saddle_excess` and `cap_radius`
both pass the 5% gate. The same-circulation case sits just above 5%
on all three observables. The split-step Strang integrator is doing
its job: at this resolution `dt` is not the limiting factor, the
grid is.

### 4. Topology behaves differently in different axes

Opposite-circulation (the physical reconnection-event channel) has
**larger** grid drift and **smaller** dt drift than same-circulation
(the kinematic-control channel). The cleanest single observable
across the entire sweep is `cos_phi` on the same-circulation case at
4.93% grid drift — within threshold but only just. The opposite case
benefits from the dt convergence cleanly, but its absolute values
move with grid by factors that exceed any honest tolerance band.

## What this means for the paper-text status

The reconnection_supplement at its existing reference configuration is
a **prototype**, not derived. Quantitative numbers it prints (saddle
heights, cap radii, channel cosines) at any single `(n, length)` are
not converged. This matches the script's own
`SCRIPT_METADATA.status = OutputStatus.PROTOTYPE` declaration (added
under issue #12) and is consistent with the docstring's framing as a
"compact reproduction harness for structural tests rather than a
physical-scale production calculation".

**No paper-text edits are required** by this finding. Paper II §
"Reconnection / W mass" already labels the cap-radius / `φ`-ansatz
content as "Candidate geometry only" in its abstract (commit history
predating issue #17). The dynamic-side numbers are not cited as
derived in the body. This memo confirms the labelling is honest.

## What would close the dynamic-side convergence gap

The sweep identifies three concrete next steps, in order of expected
payoff:

1. **Refine to `n = 64, 96` at `length = 24..30`** and rerun. The
   grid sweep above plateaus only weakly between `n=32` and `n=48`;
   the necessary cross-grid stability hasn't been reached. A
   coarse-fine ratio of ≥4 with a wide box would establish whether the
   reconnection observables converge under refinement.

2. **Run the dt sweep at the converged grid**, not at the prototype
   one. The current dt-stable region (4–6% on opposite) is the
   *integrator's* convergence rate on a *non-converged spatial
   discretisation*. Once the grid is converged, the dt sensitivity
   should tighten.

3. **Adopt the canonical `c = 1` nondimensionalisation** when the
   above are pursued. The known mismatch
   `c_eff = sqrt(2*log_pressure) ≈ 4` (flagged in
   `SCRIPT_METADATA.limitations` since #12 closure) is harmless for
   prototype work but should be reconciled before any quantitative
   comparison with the static-branch numbers.

None of the three is this-session work. The honest framing for now is:
the reconnection_supplement reproduces structural reconnection
signatures (clean topology distinction, dt-convergent saddle in the
opposite-circulation case, sensible cap geometry) but is far from
producing closure-grade numbers for the W-mass programme of
Paper II. Closure of those numbers is tracked under issue #15.

## Falsifiability check

If any quantitative number from `reconnection_supplement.py` at the
existing reference configuration were cited as a derived prediction
in Paper II, the grid-sweep results above would falsify that claim
for two of three observables, and at the 5% gate for the third.
The current Paper II framing ("candidate geometry only") is
consistent with the data; the dynamic-branch refinement work is the
upgrade path.

## Out of scope for this memo

- The dynamic 3D reconnection closure (full physical-scale
  calculation) is issue #15.
- The cap-extraction-method dependence (`volume` vs `radial-slice`)
  is not swept here; the default `volume` method is used throughout.
- The `lambda_perp` sensitivity is itself a physical question (not a
  numerics question) and is sampled by the existing
  `runA`/`runB` data files under `papers/SSV-II/data/`.

[#16]: https://github.com/StigNorland/SVT/issues/16
[`papers/SSV-I/validation-refinement-sweeps-2026-05-27.md`]: ../SSV-I/validation-refinement-sweeps-2026-05-27.md

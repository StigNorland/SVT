# Trefoil Continuation Sweep Note

This checkpoint records the first use of saved-state continuation for the static `n = 48` trefoil branch.

Artifacts:

- `papers/SSV-I/data/trefoil-continuation-sweep-n48-plus100-2026-05-17.json`
- `papers/SSV-I/data/trefoil-continuation-sweep-n48-plus200-2026-05-17.json`
- `papers/SSV-I/data/trefoil-plateau-driven-n48-2026-05-17.json`
- `papers/SSV-I/data/trefoil-continuation-sweep-n48-constrained-plus100-2026-05-17.json`
- `papers/SSV-I/data/trefoil-plateau-driven-n48-constrained-2026-05-17.json`
- `papers/SSV-I/data/trefoil-hw6-constrained-plateau-extension-2026-05-17.json`
- `papers/SSV-I/data/trefoil-hw6-constrained-plateau-extension-2-2026-05-17.json`
- `papers/SSV-I/data/trefoil-hw6-projected-residual-2026-05-17.json`
- `papers/SSV-I/data/continuations-2026-05-17/`
- `papers/SSV-I/data/continuations-plateau-2026-05-17/`
- `papers/SSV-I/data/continuations-constrained-2026-05-17/`
- `papers/SSV-I/data/continuations-constrained-plateau-2026-05-17/`

Tooling:

- `instruments/paper_i/trefoil_breather_static.py` now supports `--load-state`
- `instruments/paper_i/trefoil_state_continuation_sweep.py` continues saved states in step chunks, or in plateau mode, and tracks `delta V_p`, shell density, residual norm, and the asymptotic static `Q_p` coefficient

## Relaxer improvement

The relaxer was then upgraded to use an interior `L2`-norm-constrained flow.

This is a practical stand-in for preserving a proton-scale conserved source measure instead of letting the defect simply dissolve while the unconstrained energy keeps dropping.

The constrained flow now reports:

- `initial_l2_norm`
- `final_l2_norm`
- `l2_norm_relative_drift`

and continuation runs keep that drift at the `10^-6` level.

## Constrained `+100` continuation

The first constrained continuation checkpoint is:

- `papers/SSV-I/data/trefoil-continuation-sweep-n48-constrained-plus100-2026-05-17.json`

This changes the static branch substantially.

Under the old unconstrained flow, the first `+100` chunk caused large source leakage:

- `half_width = 5`: `delta V_p` `115.713 -> 80.275`
- `half_width = 6`: `delta V_p` `90.709 -> 50.663`
- `half_width = 7`: `delta V_p` `61.521 -> 32.970`

Under the constrained flow, the same `+100` continuation keeps the source almost fixed:

- `half_width = 5`: `delta V_p = 115.711`, `Q_p^eff = 115.475`
- `half_width = 6`: `delta V_p = 90.707`, `Q_p^eff = 90.345`
- `half_width = 7`: `delta V_p = 61.519`, `Q_p^eff = 61.043`

So the main failure mode of the original relaxer really was source leakage.

## Main result

The continuation path works cleanly, but it also shows that the saved `n = 48` proton states are still not close to convergence.

From the original `400`-step states to `500` total steps:

- `half_width = 5`: `delta V_p` drops from `115.713` to `80.275`, `Q_p^eff` drops from `115.477` to `80.101`, shell density rises from `0.8744` to `0.9159`, residual drops from `0.1817` to `0.1529`
- `half_width = 6`: `delta V_p` drops from `90.709` to `50.663`, `Q_p^eff` drops from `90.376` to `50.441`, shell density rises from `0.9446` to `0.9665`, residual drops from `0.1151` to `0.0874`
- `half_width = 7`: `delta V_p` drops from `61.521` to `32.970`, `Q_p^eff` drops from `61.019` to `32.673`, shell density rises from `0.9731` to `0.9846`, residual drops from `0.0728` to `0.0554`

From `500` to `600` total steps, the same trend continues:

- `half_width = 5`: `delta V_p` drops again to `48.757`, `Q_p^eff` to `48.638`, shell density rises to `0.9469`, residual drops to `0.1168`
- `half_width = 6`: `delta V_p` drops to `27.029`, `Q_p^eff` to `26.893`, shell density rises to `0.9809`, residual drops to `0.0666`
- `half_width = 7`: `delta V_p` drops to `17.750`, `Q_p^eff` to `17.582`, shell density rises to `0.9915`, residual drops to `0.0420`

## Interpretation

Two things are now clear.

1. The large-`r` static-potential extraction is not the bottleneck.
   Within each continued state, the fitted tail coefficient stays very tight, with tail-span relative widths still around `0.18%` to `1.00%`.

2. The underlying proton states are still evolving strongly.
   The fact that `delta V_p` and `Q_p^eff` keep falling this much between `400 -> 500 -> 600` total steps means the current saved `n = 48` states are still far from plateau in the quantities that matter most for the gravity branch.

This continuation result strengthens the convergence audit conclusion:

- the correct next task is still solver/state convergence
- direct static `Q_p` extraction is the right observable
- any gravity normalization based on the pre-continuation saved states should be treated as provisional

## Plateau-driven continuation

The next pass promoted the same driver into a plateau-based stopping rule using:

- `100` extra steps per chunk
- `2%` relative-change thresholds for both `delta V_p` and `Q_p^eff`
- `0.005` absolute shell-density threshold
- residual threshold `0.05`
- `2` consecutive plateau hits required

None of the three saved `n = 48` states reached plateau within four `100`-step chunks.
All three stopped by `max_chunks_reached`.

The key signal is that the proton-source observables are still moving by order `45%` per chunk:

- `half_width = 5`: `delta V_p` relative changes `0.393`, `0.441`, `0.462`
- `half_width = 6`: `delta V_p` relative changes `0.466`, `0.470`, `0.467`
- `half_width = 7`: `delta V_p` relative changes `0.462`, `0.458`, `0.455`

The extracted `Q_p^eff` moves almost identically, which confirms again that the outer-potential fit is not the limiting issue.

By contrast, shell-density changes do shrink:

- `half_width = 5`: `0.0309`, `0.0216`, `0.0137`
- `half_width = 6`: `0.0143`, `0.0085`, `0.0048`
- `half_width = 7`: `0.0068`, `0.0038`, `0.0021`

So the outer shell is flattening faster than the integrated proton source itself.
That is exactly why shell-density-only convergence is not enough for the gravity branch.

## Plateau-driven continuation after the relaxer fix

With the constrained relaxer, the same plateau driver behaves much better.

Checkpoint:

- `papers/SSV-I/data/trefoil-plateau-driven-n48-constrained-2026-05-17.json`

Results:

- `half_width = 7` reaches plateau at `700` total steps
- `half_width = 6` does not reach plateau within `800` total steps, but `delta V_p` and `Q_p^eff` are already nearly flat
- `half_width = 5` does not reach plateau and still has a large residual

Final constrained plateau-driven states:

- `half_width = 5`: stop `max_chunks_reached`, `delta V_p = 115.693`, `Q_p^eff = 115.497`, shell density `0.8361`, residual `0.1462`
- `half_width = 6`: stop `max_chunks_reached`, `delta V_p = 90.690`, `Q_p^eff = 90.380`, shell density `0.9252`, residual `0.0624`
- `half_width = 7`: stop `plateau_reached`, `delta V_p = 61.511`, `Q_p^eff = 61.108`, shell density `0.9683`, residual `0.0360`

The most important new conclusion is that the improved relaxer converts the branch picture from "all saved fine-grid states are still collapsing" to:

- `half_width = 7` looks genuinely settleable
- `half_width = 6` looks close, but not yet under the current residual threshold
- `half_width = 5` is still the clearly problematic box

## Next step

Continue the `n = 48` branch further, but keep the plateau criteria tied to the real source observables:

- fractional change in `delta V_p`
- fractional change in `Q_p^eff`
- residual norm
- shell-density recovery

The right stopping rule is no longer "run another nice round number of steps." It is "stop when these proton-source observables flatten enough to be trusted."

With the constrained relaxer in place, the next practical move is:

- focus continuation effort on `half_width = 6`
- treat `half_width = 7` as the first usable fine-grid reference state
- stop spending time on `half_width = 5` until the solver or domain treatment is improved further

## Focused `half_width = 6` follow-up

The next follow-up did exactly that:

- `papers/SSV-I/data/trefoil-hw6-constrained-plateau-extension-2026-05-17.json`

Starting from the constrained `800`-step `half_width = 6` state, the solver was advanced in four more `100`-step chunks to `1200` total steps.

This clarifies the remaining issue.

The proton-source observables are already essentially flat:

- `delta V_p`: `90.6830 -> 90.6763 -> 90.6696 -> 90.6628`
- `Q_p^eff`: `90.3828 -> 90.3813 -> 90.3774 -> 90.3722`
- shell-density changes: `1.15e-4`, `5.11e-5`, `2.26e-5`

The per-chunk relative changes in `delta V_p` and `Q_p^eff` are only of order `10^-4`, far below the current `2%` plateau tolerances.

But the residual remains just above the current threshold:

- residuals: `0.0584`, `0.0560`, `0.0547`, `0.0539`

So the present status of `half_width = 6` is:

- source-flat by the gravity-facing observables
- not yet plateaued by the current residual criterion

That makes it the main borderline case in the branch.

## Deeper `half_width = 6` push

The next continuation pushed the same constrained `half_width = 6` state beyond `1200` total steps:

- `papers/SSV-I/data/trefoil-hw6-constrained-plateau-extension-2-2026-05-17.json`

This makes the next bottleneck explicit.

The source observables remain extremely flat:

- `delta V_p`: `90.6560 -> 90.6502 -> 90.6457 -> 90.6421`
- `Q_p^eff`: `90.3662 -> 90.3607 -> 90.3565 -> 90.3530`
- shell-density changes fall to `10^-6` to `10^-4` scale

But the residual no longer improves materially:

- residuals: `0.05344`, `0.05344`, `0.05345`, `0.05346`

And the controller starts hitting the step-size floor:

- the first extra chunk reaches `1300` total steps normally
- the next three chunks each accept only `1` step and reject `10`, then stop at `step_size_floor`

So the updated status of `half_width = 6` is:

- source-converged for the gravity-facing extraction
- not residual-converged under the current `0.05` threshold
- now limited by controller behavior rather than by obvious physical drift of the static source

## Projected residual for the constrained flow

The next correction was conceptual rather than geometric:

- `papers/SSV-I/data/trefoil-hw6-projected-residual-2026-05-17.json`

For the constrained `L2` flow, the right residual is the gradient projected onto the tangent space of the fixed-`L2` manifold on the freely updated interior cells.

With that projected residual in place, the same `half_width = 6` continuation reaches plateau.

Key numbers:

- raw residual at `1300` total steps: `0.05344`
- projected residual at `1300` total steps: `0.00463`
- projected residual at `1302` total steps: `0.00498`
- projected residual at `1304` total steps: `0.00527`

The source observables remain flat at the same time:

- `delta V_p`: `90.6560 -> 90.6502 -> 90.6457`
- `Q_p^eff`: `90.3662 -> 90.3607 -> 90.3565`

So the correct reading is now:

- the unconstrained residual was over-penalizing directions the constrained flow is not allowed to take
- the projected residual respects the actual constrained dynamics
- under that corrected residual, `half_width = 6` joins `half_width = 7` as a usable fine-grid reference state

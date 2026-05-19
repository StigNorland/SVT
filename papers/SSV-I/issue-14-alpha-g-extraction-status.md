# Issue #14 `\alpha_G` Extraction Status

Issue `#14` is not ready for a first-principles `\alpha_G` value yet. The useful progress is that the pipeline now has a reproducible separation between:

- the far-field suppression estimator tracked by [alpha-g-proxy-note.md](alpha-g-proxy-note.md)
- the direct long-wavelength `Q_p` kernel checkpoint tracked by [q-p-kernel-integral-note.md](q-p-kernel-integral-note.md)
- the unresolved calibration/operator step that still prevents an `\alpha_G` claim

## Current Tracked Checkpoint

Artifacts:

- [data/alpha-g-proxy-checkpoint-2026-05-06.json](data/alpha-g-proxy-checkpoint-2026-05-06.json)
- [data/q-p-convergence-audit-2026-05-07.json](data/q-p-convergence-audit-2026-05-07.json)
- [data/q-p-kernel-integral-2026-05-07.json](data/q-p-kernel-integral-2026-05-07.json)

The direct long-wavelength kernel currently computed by `q_p_kernel_integral.py` is

\[
Q_p^{LW} = \delta V_p \left(\frac{a_p}{\xi}\right)^3,
\]

with `a_p / xi = m_e / m_p`. This is a direct `Q_p` object, not an `\alpha_G` estimate.

The tracked May 7 checkpoint gives:

- `n = 24`: `Q_p^{LW}` runs from `3.12e-10` to `9.34e-10` across `half_width = 5, 6, 7`
- `n = 48`: `Q_p^{LW}` runs from `9.94e-9` to `1.87e-8` across `half_width = 5, 6, 7`
- fixed-`half_width` coarse-fine `Q_p^{LW}` drift is about `0.950`, `0.967`, and `0.969`

The convergence audit gives a more forgiving shell-density read:

- best fixed-`half_width` shell-density drift: about `2.6%`
- worst fixed-`half_width` shell-density drift: about `12.0%`

That split is the key diagnostic: the outer suppression scalar is much more stable than the integrated source, but the gravity-facing kernel is still dominated by static-state drift.

## Closure Gate

The current status is:

- `suppression_estimator`: candidate
- `Q_p_kernel`: candidate long-wavelength checkpoint
- `C_Q` or explicit carrier operator: unresolved
- `alpha_G_prediction`: blocked

Do not identify `1 - shell_mean_density`, `delta V_p`, or `Q_p^{LW}` directly with `\alpha_G`.

## Next Practical Task

The next useful issue `#14` step is not another reduced two-factor fit. It is to tighten the static branch until the direct `Q_p` kernel is stable enough that a calibration or carrier-operator test is meaningful.

Concrete next checks:

- rerun the convergence audit on the constrained continuation states once those artifacts are promoted
- keep `Q_p^{LW}` and `\Pi_{\rm mono}` side by side in every gravity-facing checkpoint
- add the first explicit nontrivial carrier operator only after the long-wavelength kernel stops moving at the current level

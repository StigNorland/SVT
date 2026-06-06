# `Q_p` Convergence And Kernel Note

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `src/_fitted_quarantine/`. Tracking: issue #66.

This note pauses the reduced-ansatz fitting track and asks two prior questions:

1. is the current static trefoil minimum converged in `n` and `half_width` independently?
2. what analytic kernel is the static pipeline supposed to compute for `Q_p`?

Artifacts:

- `papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-geom-2026-05-06.json`
- `papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-geom-2026-05-06.json`
- `papers/SSV-I/data/q-p-convergence-audit-2026-05-07.json`
- `papers/SSV-I/data/trefoil-plateau-driven-n48-constrained-2026-05-17.json`
- `papers/SSV-I/data/trefoil-hw6-projected-residual-2026-05-17.json`
- `papers/SSV-I/data/trefoil-hw8-n64-projected-residual-2026-05-17.json`
- `papers/SSV-I/data/trefoil-boxsize-trend-6-7-8-2026-05-17.json`
- `papers/SSV-I/data/q-p-convergence-audit-2026-05-17.json`

## 1. Convergence First

The current saved static states are **not** independently converged in `n` and `half_width`.

### Within-Branch `half_width` Drift

For the coarse branch (`n = 24`, `200` steps):

- `shell_mean_density` relative drift across `half_width = 5, 6, 7`: about `0.0059`
- `shell_mean_deficit` relative drift: about `0.860`
- `deficit_volume` relative drift: about `0.666`
- `equivalent_deficit_radius` relative drift: about `0.306`

For the original unconstrained fine branch (`n = 48`, `400` steps):

- `shell_mean_density` relative drift across `half_width = 5, 6, 7`: about `0.101`
- `shell_mean_deficit` relative drift: about `0.785`
- `deficit_volume` relative drift: about `0.468`
- `equivalent_deficit_radius` relative drift: about `0.190`

So even before comparing resolutions, the static minimum is still moving materially with box size, especially on the fine branch.

### Updated Fine-Grid Read

The constrained continuation branch changes the stationarity story but does **not** close the box-size story.

At the level of constrained-flow plateauing:

- `half_width = 7` reaches plateau under the constrained-flow criterion
- `half_width = 6` reaches plateau once the residual is projected onto the tangent space of the constrained `L2` manifold
- `half_width = 8` also reaches plateau cleanly
- `half_width = 5` remains the outlier

But the direct constrained box-size comparison across `half_width = 6, 7, 8` shows that the integrated source is still moving dramatically:

- `6 -> 7`: `delta V_p` and `Q_p^eff` change by about `32%`
- `7 -> 8`: `delta V_p` and `Q_p^eff` change by about `75%`

So the fine-grid branch is no longer uniformly unconverged in the solver sense, but it is still strongly unconverged in the domain-size sense for the gravity-facing source.

### Cross-Resolution Drift At Fixed `half_width`

Using the updated constrained fine-grid references, the coarse-to-fine shell-density drift is:

- `half_width = 5`: about `0.158`
- `half_width = 6`: about `0.073`
- `half_width = 7`: about `0.031`

This is the most optimistic convergence-facing quantity currently available, because shell density is much better behaved than shell deficit.

But the shell-deficit drift itself is still enormous:

- `half_width = 5`: about `0.945`
- `half_width = 6`: about `0.960`
- `half_width = 7`: about `0.964`

The same is true for the interior geometry:

- `deficit_volume` cross-resolution drift: about `0.950` to `0.969`
- `equivalent_deficit_radius` cross-resolution drift: about `0.632` to `0.684`

## Convergence Read

The static trefoil branch is not yet converged well enough to support detailed `Q_p` ansatz fitting as if the extracted states were settled.

The practical shell-density ceiling is now:

- best-case shell-density cross-resolution drift: about `3.1%`
- worst-case shell-density cross-resolution drift: about `15.8%`

So even on the optimistic outer-shell metric, any `Q_p` inferred from these states already carries at least a few-percent numerical uncertainty before any modeling uncertainty is introduced. On the quantities currently used for reduced fitting (`shell_deficit`, deficit-volume-style geometry), the uncertainty is much larger.

That means additional `q_p_two_factor_*` fitting is still below the current solver noise floor unless convergence improves first.

### Residual Criterion Update

For constrained continuation states, the relevant stationarity measure is the projected residual, not the raw unconstrained residual.

This matters especially for `half_width = 6`:

- raw residual remains about `0.053`
- projected residual is about `0.005`

The raw residual counts off-manifold directions that the constrained flow is not allowed to follow. The projected residual measures the actual remaining tangent-space force on the constrained branch.

So the correct convergence reading for the updated fine-grid references is:

- `half_width = 5`: still not acceptable
- `half_width = 6, 7, 8`: individually usable constrained-flow stationary states
- but `half_width = 6, 7, 8` do **not** yet define a box-size-stable gravity reference set

## 2. The `Q_p` Kernel

The static branch should not be judged by whether it produces a convenient scalar fit. It should be judged by whether it computes the right monopole kernel.

The correct object to target is a coarse-grained proton monopole functional of the static deficit profile:

\[
Q_p[\rho]
  =
  \left(\frac{a_p}{\xi}\right)^3
  \int_{\mathbb{R}^3}
    W_p(\mathbf{x})
    \,\mathcal{S}_{\xi}\!\left[1-\rho(\mathbf{x})\right]
  \, d^3x.
\]

Here:

- `\rho = |\Psi|^2 / \rho_0` is the dimensionless static density profile
- `W_p(\mathbf{x})` is the proton-support window for the resolved breather geometry
- `\mathcal{S}_{\xi}` is the carrier-medium coupling operator set by the healing length of the surrounding medium
- the prefactor `\left(a_p/\xi\right)^3` is the cross-defect suppression identified in the units audit

The critical scale split is:

- `\xi = \hbar/(m_e c)` is the electron healing length of the surrounding medium
- `a_p = \hbar/(m_p c)` is the proton grain scale

The proton radiates into the surrounding medium, so `\xi`, not `a_p`, sets the carrier-scale part of the kernel. The `a_p` dependence enters through the explicit cubic suppression factor.

This is the kernel-level statement the pipeline should satisfy.

### Long-Wavelength Test

In the long-wavelength limit, where the deficit profile varies slowly on the carrier healing-length scale relevant to the emitted mode, the smoothing operator should reduce to the identity:

\[
\mathcal{S}_{\xi}[1-\rho] \to 1-\rho.
\]

If the proton window resolves the full static breather support, then

\[
\int W_p(\mathbf{x}) \, (1-\rho(\mathbf{x}))\, d^3x
  \equiv \delta V_p,
\]

and the kernel must reduce to

\[
Q_p \to \delta V_p \left(\frac{a_p}{\xi}\right)^3.
\]

That is the basic correctness test for the numerical pipeline.

## What The Current Pipeline Actually Computes

The current prototype branch computes pieces of this kernel, not the kernel itself:

- `deficit_volume` is the resolved `\delta V_p` candidate
- `shell_mean_density` and `shell_mean_deficit` are outer-region proxies for how much of that deficit leaks into the far field
- the reduced additive ansatzes are only surrogate maps between those pieces

What it does **not** yet compute explicitly is:

- the proton-support window `W_p`
- the carrier operator `\mathcal{S}_{\xi}` beyond its long-wavelength identity limit
- a first-principles map from the static profile to the true monopole source moment

## Current Implemented Limit

The present repository can honestly compute only the long-wavelength kernel limit

\[
Q_p^{\rm LW}
  =
  \delta V_p \left(\frac{a_p}{\xi}\right)^3,
\]

because the current grids do not resolve any additional carrier operator beyond the identity limit.

That quantity should be treated as the direct kernel object the current static branch can support, with convergence diagnostics carried separately from any reduced fitting.

## Current Read

The gravity branch should therefore prioritize, in this order:

1. treat `half_width = 5` as dropped from the reference set unless a specific rescue path is found
2. understand why the integrated source reorganizes so strongly between `half_width = 7` and `8`
3. define and implement the explicit kernel operator for `Q_p`
4. only then resume reduced ansatz fitting if a surrogate is still needed

That is a cleaner stopping rule than continuing to add fitted `q_p_two_factor_*` variants on top of unconverged static states.

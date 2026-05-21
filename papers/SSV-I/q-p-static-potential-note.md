# Direct Static Potential Note

This note records the first direct static-potential calculation from saved proton trefoil states.

Artifact:

- `papers/SSV-I/data/q-p-static-potential-2026-05-07.json`
- `papers/SSV-I/data/trefoil-plateau-driven-n48-constrained-2026-05-17.json`
- `papers/SSV-I/data/trefoil-hw6-projected-residual-2026-05-17.json`
- `papers/SSV-I/data/trefoil-hw8-n64-projected-residual-2026-05-17.json`
- `papers/SSV-I/data/trefoil-boxsize-trend-6-7-8-2026-05-17.json`

The script evaluates three definite integrals on each saved state:

\[
\int (\rho_0 - \rho)\,d^3x,
\]

\[
\int (\rho_0 - \rho)^2\,d^3x,
\]

and

\[
\Phi(\mathbf{x}_*)
  =
  \int (\rho_0 - \rho(\mathbf{x}))
    G_{\rm static}(|\mathbf{x}-\mathbf{x}_*|)
  \,d^3x,
\]

using the linearised static LogSE Green's function

\[
G_{\rm static}(r)
  =
  \frac{1 - e^{-2r/\xi}}{4\pi c^2 r}.
\]

The probe points were taken on the positive `x` axis at radii

- `r = 8, 10, 12, 16, 20`

in the current `\xi = 1` nondimensionalisation.

## Main Result

The actual static potential behaves exactly as hoped in one sense and badly in another.

### Good

For each saved state, the large-`r` coefficient

\[
Q_p^{\rm eff}(r) \equiv 4\pi c^2 r \,\Phi(r)
\]

stabilizes very cleanly across the outer probe set.

Representative tail spans:

- `n = 24`, `half_width = 5`: about `0.22%`
- `n = 24`, `half_width = 6`: about `0.47%`
- `n = 24`, `half_width = 7`: about `0.82%`
- `n = 48`, `half_width = 5`: about `0.16%`
- `n = 48`, `half_width = 6`: about `0.36%`
- `n = 48`, `half_width = 7`: about `0.84%`

So the asymptotic `1/r` coefficient is numerically well-defined for each fixed saved state.

### Bad

Across resolution, the extracted asymptotic coefficient still drifts almost exactly as badly as the deficit volume itself.

Cross-resolution drift in the asymptotic coefficient:

- `half_width = 5`: about `0.950`
- `half_width = 6`: about `0.968`
- `half_width = 7`: about `0.969`

So the physical static-source coefficient can be read off unambiguously from a given state, but the state itself is still not converged.

## Current Values

### Asymptotic coefficient from the direct potential

`n = 24`:

- `half_width = 5`: `5.77`
- `half_width = 6`: `2.94`
- `half_width = 7`: `1.92`

`n = 48`:

- `half_width = 5`: `115.48`
- `half_width = 6`: `90.38`
- `half_width = 7`: `61.02`

### Auxiliary integrals

Bare deficit volume:

- `n = 24`: `5.78`, `2.95`, `1.93`
- `n = 48`: `115.71`, `90.71`, `61.52`

Squared-deficit integral:

- `n = 24`: `9.75e-2`, `1.38e-2`, `3.65e-3`
- `n = 48`: `4.02e1`, `1.59e1`, `3.74`

## Interpretation

This is a stronger result than another reduced ansatz fit.

The direct potential route shows:

1. the static Green's function extraction is internally clean for each saved state
2. the outer `1/r` coefficient is easy to read off
3. the dominant uncertainty is still the unresolved static profile itself, not the fitting method

## Updated Fine-Grid Read

The direct potential route is still the right diagnostic object, but the interpretation of the fine-grid branch has changed again after the `half_width = 8` check.

The constrained-flow continuation now shows:

- `half_width = 6` is plateaued once the residual is measured on the constrained `L2` tangent space
- `half_width = 7` is plateaued under the same constrained-flow logic
- `half_width = 8` is also plateaued, and the `n = 64` rerun shows that its large source is not a coarse-grid artifact
- `half_width = 5` remains the bad box

That is good news for solver stationarity, but bad news for domain adequacy. The direct fine-grid box-size comparison gives:

- `half_width = 6`: `Q_p^eff ~ 90.36`
- `half_width = 7`: `Q_p^eff ~ 61.11`
- `half_width = 8`: `Q_p^eff ~ 246.77`

So the static-potential track should **not** treat `half_width = 6, 7` as an adequate large-box reference set. The asymptotic coefficient is easy to read off from each fixed state, but the underlying state is still box-sensitive enough to dominate the gravity-facing uncertainty.

So the repo now has the right diagnostic object:

- not another reduced `Q_p` surrogate
- but the actual static potential and its asymptotic coefficient

The remaining bottleneck is no longer "can we read off the asymptotic coefficient?" It is:

- dropping `half_width = 5` from the gravity-facing reference set
- and understanding the large `half_width = 7 -> 8` source reorganization before treating any extracted `Q_p` as box-size-stable

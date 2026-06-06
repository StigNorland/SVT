# Direct `Q_p` Kernel Integral Note

This note records the first direct `Q_p` kernel artifact built from saved static proton states.

Artifacts:

- `papers/SSV-I/data/q-p-kernel-integral-2026-05-07.json`
- `papers/SSV-I/data/q-p-convergence-audit-2026-05-07.json`

The current script computes the long-wavelength kernel limit

\[
Q_p^{\rm LW}
  =
  \delta V_p \left(\frac{a_p}{\xi}\right)^3,
\]

with

- `\xi = \hbar/(m_e c)` the electron healing length of the surrounding medium
- `a_p = \hbar/(m_p c)` the proton grain scale

so that

\[
\left(\frac{a_p}{\xi}\right)^3
  =
  \left(\frac{m_e}{m_p}\right)^3
  \approx 1.615 \times 10^{-10}.
\]

## Current Values

### `n = 24`

- `half_width = 5`: `9.34e-10`
- `half_width = 6`: `4.77e-10`
- `half_width = 7`: `3.12e-10`

### `n = 48`

- `half_width = 5`: `1.87e-8`
- `half_width = 6`: `1.47e-8`
- `half_width = 7`: `9.94e-9`

## What This Means

This is a direct kernel computation, not another reduced fitting ansatz.

But it also shows immediately why further ansatz fitting should pause: the current direct kernel values are still dominated by the unresolved static-state drift.

Cross-resolution drift of the direct long-wavelength kernel is:

- `half_width = 5`: about `0.950`
- `half_width = 6`: about `0.967`
- `half_width = 7`: about `0.969`

That is exactly the deficit-volume drift, as it should be, because the present long-wavelength kernel is just the deficit-volume integral times the fixed suppression factor.

## Current Read

This is a useful checkpoint for two reasons.

First, it confirms the scale logic:

- the carrier medium scale is `\xi = \hbar/(m_e c)`
- the proton scale enters only through the cubic suppression factor
- the resulting prefactor is of the right rough order for the gravity branch

Second, it confirms the numerical bottleneck:

- the current uncertainty in direct `Q_p` is not coming from the reduced ansatz choice
- it is coming from the unconverged static deficit volume itself

So the next upgrade path is now cleaner:

1. improve static convergence of `\delta V_p`
2. only then add any nontrivial carrier operator beyond the long-wavelength identity limit
3. only after that revisit downstream gravity normalization

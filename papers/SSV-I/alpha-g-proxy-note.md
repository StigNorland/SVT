# First `alpha_G` Proxy Note

This note defines the first conservative bridge from the static trefoil branch (`#13`) to the gravity-extraction branch (`#14`).

The key discipline is simple:

- do **not** claim an `alpha_G` prediction yet
- do extract the simplest dimensionless far-field suppression quantity that the current static sweeps measure reproducibly

## Working Choice

The present primary proxy is

\[
\Pi_G^{(1)} \equiv 1 - \rho_{\rm shell},
\]

where `rho_shell` is the shell-averaged density in the outer region currently reported by the static sweeps as `shell_mean_density`.

The reason for this choice is empirical, not theoretical elegance:

- among the current outer-region scalars, `shell_mean_density` is the most stable quantity under the longer box-size and multiresolution checks
- its complement, the shell deficit, is the most direct dimensionless measure of how much the outer medium still differs from the saturated background

This makes `\Pi_G^{(1)}` the safest first suppression proxy to carry forward into the gravity branch.

## Secondary Cross-Check

The current secondary proxy is

\[
\Pi_G^{(2)} \equiv \frac{M_{\rm far}}{L_{\rm box}},
\]

where `M_far` is the existing `far_field_moment` diagnostic and `L_box` is represented in the current prototype by `half_width`.

This quantity is kept only as a geometric cross-check. At the present stage it is less stable than the shell-deficit proxy and should not be treated as the leading gravity-facing scalar.

## What This Is Not

This note does **not** define

\[
\alpha_G = \frac{G m_p^2}{\hbar c}
\]

from first principles.

Instead it defines the quantity that the future extraction pipeline will have to map into the structural Paper II gravity formula. In other words:

- `#13` gives a relaxed static breather plus far-field diagnostics
- this note identifies which diagnostic currently deserves to be the first bridge quantity
- `#14` will still need to turn that bridge quantity into a true `alpha_G` prediction

## Current Read

The static branch now supports a clean provisional statement:

- `shell_mean_density` is the most stable simple outer-region observable currently in hand
- therefore `1 - shell_mean_density` is the most honest first `alpha_G` proxy
- any stronger claim should wait until the proxy is extracted from a more converged static branch and connected explicitly to the Paper II gravity formula

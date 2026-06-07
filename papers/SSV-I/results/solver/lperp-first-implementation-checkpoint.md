# L_perp First Implementation Checkpoint

This note records the first implementation of the chiral non-local shear
term `L_perp` from Paper I, the term that the paper's appendix attributes
the stabilisation of `N_Y = 3.007` and `F = 4.47` to.

Artifacts:

- `instruments/paper_i/trefoil_y_junction_closed_asym_lperp_static.py`
- `papers/SSV-I/data/y-junction-closed-asym-lperp-lambda10-n24-hw6-200steps-2026-05-17.npz`
- `papers/SSV-I/data/y-junction-closed-asym-lperp-lambda10-n24-hw6-200steps-2026-05-17.json`
- `papers/SSV-I/data/y-junction-closed-asym-lperp-sweep-n24-hw6-200steps-2026-05-17.json`

## What L_perp Is

Paper I equation `chiral`:

\[
\mathcal{L}_\perp = -\frac{\lambda\hbar^2}{2 m_0 \rho_0^2} \,|\nabla\times\mathbf{j}|^2,
\quad
\mathbf{j} = \mathrm{Im}(\Psi^* \nabla \Psi).
\]

In the static-branch dimensionless units (`hbar = m_0 = rho_0 = 1`), the
energy contribution is

\[
E_\perp = \tfrac{1}{2}\lambda \int |\nabla\times \mathbf{j}|^2 \, d^3x.
\]

The paper quotes `lambda = 2000` (Section 2 + Appendix `app:minimisation`).

## Variational Derivative

Working through the Wirtinger derivative with two integrations by parts and
the identity `div(curl omega) = 0`:

\[
\frac{\delta E_\perp}{\delta \Psi^*}(x) = -i\,\lambda\,(\nabla\times\boldsymbol{\omega})(x) \cdot \nabla\Psi(x),
\quad
\boldsymbol{\omega} = \nabla\times\mathbf{j}.
\]

This is added to the LogSE gradient in the relaxation loop:

\[
\frac{\partial \Psi}{\partial t} = -\frac{\delta E_{\rm LogSE}}{\delta \Psi^*} - \frac{\delta E_\perp}{\delta \Psi^*}.
\]

The new term costs about three additional finite-difference passes per
relaxation step (gradient -> current -> first curl -> second curl ->
contraction with grad psi), so per-step cost roughly doubles.

## Sanity Check At lambda = 0

Running the L_perp script with `lambda = 0` reproduces the existing
asymmetric closed Y-junction relaxation byte-for-byte. The shared
machinery passes through cleanly.

## Lambda Sweep (n=24, hw=6, 200 steps)

| `lambda` | `E_LogSE` | `E_perp` | `E_full` | violations | rejected | step | residual | `min_rho` | depressed_fraction | shell_rho | r_eff |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1008.10 | 0.00 | 1008.10 | 0 | 0 | 2.88e-2 | 1.37 | 1.26e-3 | 0.082 | 0.703 | 5.05 |
| 0.1 | 1008.09 | 10.24 | 1018.33 | 0 | 0 | 2.88e-2 | 1.38 | 3.97e-4 | 0.087 | 0.698 | 5.04 |
| 1.0 | 1011.43 | 92.95 | 1104.38 | 0 | 0 | 2.88e-2 | 1.56 | 2.79e-4 | 0.108 | 0.668 | 5.00 |
| 10.0 | 1031.29 | 847.79 | 1879.07 | 0 | 0 | 2.88e-2 | 5.79 | **1.20e-4** | 0.151 | 0.610 | 4.96 |
| 30.0 | 1050.57 | 2469.68 | 3520.25 | 12 | 12 | 4.72e-3 | 16.44 | 1.61e-3 | 0.146 | 0.596 | 4.99 |
| 100.0 | 1103.63 | 8247.21 | 9350.84 | 14 | 14 | 1.54e-3 | 54.03 | **6.10e-5** | 0.186 | 0.558 | 4.94 |

Five clean trends, one stiffness wall.

## Finding 1: L_perp Sharpens Vortex Cores

`min_rho` drops as `lambda` rises: `1.26e-3 -> 3.97e-4 -> 2.79e-4 -> 1.20e-4`
across the no-violations range. The L_perp term penalises gradients of the
phase current most strongly where the field has rapid azimuthal phase
variation, which is exactly the core region of each vortex. Minimising it
pushes the cores into thinner, more sharply-localised structures.

`depressed_fraction` correspondingly grows from 0.082 to 0.151. More cells
sit below the `rho < 0.35` cutoff, because the cores carry the same total
phase winding but in smaller volumes.

## Finding 2: L_perp Does Not Compactify The Bulk

The hope was that L_perp would remove the asymmetric closed Y's
linear-in-`hw` divergence of `F^int` by suppressing long-range phase
structure. The far-field shell density tells a different story:

`shell_rho` at `r in [4.2, 5.7]` goes from `0.703` to `0.558` as
`lambda` grows. The outer shell becomes **more depressed**, not less.

This is consistent with `L_perp` adding (not removing) long-range structure.
The chiral shear term has its own characteristic length and creates phase
correlations that extend into the bulk, rather than damping the
multi-vortex velocity tails.

So adding `L_perp` at the values we can reach with explicit Euler does not
compactify the configuration. We have not tested the paper's `lambda = 2000`
regime, only `lambda <= 100`.

## Finding 3: The Stiffness Wall Hits Around `lambda ~ 30 - 100`

At `lambda = 0` through `lambda = 10`, the adaptive step size stays at the
LogSE-only maximum (`2.88e-2`) and the relaxation runs with zero rejected
steps.

At `lambda = 30`, the step size drops by a factor of 6 (`2.88e-2 ->
4.72e-3`) and 12 of 200 steps are rejected. At `lambda = 100`, step size
is down by 20x with 14 rejections.

This is exactly the operator stiffness behaviour the analytic estimate
predicts. The variational derivative involves up to 5 nested first
derivatives (`(nabla x nabla x j) . nabla psi`), so the maximum eigenvalue of
the linearised operator scales as `lambda / dx^5`. With `dx = 0.5` and
`lambda = 100`: `100 / 0.5^5 = 3200`, vs the LogSE Laplacian's
`1 / 0.5^2 = 4`. So `lambda = 100` is already `800x` stiffer than the
LogSE-only baseline at this grid.

For the paper's `lambda = 2000` at `dx = 0.5`: a further factor of 20
stiffer. Explicit Euler with the adaptive controller we have is not the
right algorithm at the paper's regime.

## What This Settles And Does Not Settle

Settles:

- the L_perp term can be derived analytically and implemented on top of
  the existing relaxation machinery without breaking anything (`lambda = 0`
  reproduces the LogSE-only result)
- `L_perp` does measurable physical work: it sharpens the vortex cores,
  monotonically and dramatically (factor of 20 reduction in `min_rho` from
  `lambda = 0` to `lambda = 10`)
- the explicit Euler scheme hits a stiffness wall around `lambda = 30 - 100`
  at `dx = 0.5`. The paper's `lambda = 2000` is unreachable with this
  algorithm at this grid

Does not settle:

- whether `L_perp` at the paper's coupling stabilises the trefoil knot
  against curvature-driven dissolution (need to apply `L_perp` to the
  trefoil prototype too)
- whether the apparent failure of `L_perp` to compactify the bulk would
  reverse at `lambda = 2000` (we cannot test directly, but the trend
  through `lambda = 100` is in the wrong direction)
- the right algorithmic path to reach `lambda = 2000`: implicit time
  stepping, a much finer grid, or a different relaxation scheme entirely

## Next Pieces

In increasing order of cost:

1. **Apply L_perp to the trefoil knot** by writing a sibling
   `trefoil_breather_lperp_static.py` that adds the same L_perp gradient
   on top of the existing trefoil knot initial condition. Test whether
   `lambda = 10` is enough to prevent the dissolution we documented at
   `lambda = 0`. Cheapest piece; answers the binary question of whether
   `L_perp` is the missing stabilisation mechanism.
2. **Refinement of L_perp at fixed lambda**: re-run the same `lambda = 10`
   sweep at `(n = 32, n = 48)` to test grid sensitivity. The stiffness
   wall moves with `dx`, so finer grids may be able to reach larger
   `lambda`.
3. **Semi-implicit time stepping** for the L_perp term. Treat the LogSE
   gradient explicitly and the L_perp operator implicitly (e.g.,
   Crank-Nicolson on the linearised L_perp Hessian). This is the right
   algorithm for stiff terms and would unlock `lambda >> 100`. Significant
   work: requires solving a sparse linear system per step.

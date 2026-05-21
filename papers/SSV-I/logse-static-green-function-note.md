# Static Green's Function Of The Linearised LogSE Around Saturation

This note addresses the specific gravity-branch question:

What is the static long-range Green's function of the linearised LogSE around saturation, with the chiral-shear sector turned off?

This is the right place to look before adding more reduced `Q_p` fitting structure.

## Starting Point

Take the saturated background in the scalar LogSE sector, with

\[
\rho = \rho_0 + \delta \rho,
\qquad
|\delta \rho| \ll \rho_0,
\]

and no chiral-shear coupling.

The linearised density-mode equation already quoted in the audit is

\[
\partial_t^2 \delta \rho
  =
  c^2 \nabla^2 \delta \rho
  -
  \frac{\hbar^2}{4 m_e^2} \nabla^4 \delta \rho,
\]

where the carrier scale is set by the surrounding medium's lightest stable defect, so the relevant healing length is

\[
\xi = \frac{\hbar}{m_e c}.
\]

This is the gapless Bogoliubov-type density branch of the scalar LogSE medium.

## Static Source Equation

Now couple in a static source `J(\mathbf{x})` and set `\partial_t = 0`. The static response solves

\[
-c^2 \nabla^2 \delta \rho
  +
  \frac{\hbar^2}{4 m_e^2} \nabla^4 \delta \rho
  =
  J(\mathbf{x}).
\]

Factor the operator:

\[
-\nabla^2
\left(
  c^2
  -
  \frac{\hbar^2}{4 m_e^2}\nabla^2
\right)\delta \rho
  =
  J(\mathbf{x}).
\]

So the static Green's function is not the Green's function of a single Helmholtz operator. It is the Green's function of a Laplacian times a Helmholtz operator.

## Fourier-Space Green's Function

For a point source, the Fourier-space Green's function is

\[
\widetilde{G}(\mathbf{k})
  =
  \frac{1}{
    c^2 k^2 + \dfrac{\hbar^2}{4 m_e^2} k^4
  }.
\]

Write

\[
\beta \equiv \frac{\hbar^2}{4 m_e^2 c^2}
       = \frac{\xi^2}{4}.
\]

Then

\[
\widetilde{G}(\mathbf{k})
  =
  \frac{1}{c^2}
  \frac{1}{k^2(1+\beta k^2)}.
\]

Partial fractions give

\[
\frac{1}{k^2(1+\beta k^2)}
  =
  \frac{1}{k^2}
  -
  \frac{\beta}{1+\beta k^2}
  =
  \frac{1}{k^2}
  -
  \frac{1}{k^2 + 1/\beta}.
\]

Since

\[
\frac{1}{\beta} = \frac{4}{\xi^2},
\]

the second term has Yukawa mass

\[
\mu = \frac{2}{\xi}.
\]

## Real-Space Green's Function

Using the standard transforms

\[
\mathcal{F}^{-1}\!\left[\frac{1}{k^2}\right]
  = \frac{1}{4\pi r},
\qquad
\mathcal{F}^{-1}\!\left[\frac{1}{k^2+\mu^2}\right]
  = \frac{e^{-\mu r}}{4\pi r},
\]

the static Green's function is

\[
G(r)
  =
  \frac{1}{4\pi c^2 r}
  \left(
    1 - e^{-2r/\xi}
  \right).
\]

This is the main result.

## Interpretation

The scalar LogSE density sector is **not** giving a pure Yukawa law at long range.

It gives:

- a massless `1/r` Coulomb-like tail
- minus a short-range Yukawa piece with range `\xi/2`

So the linearised static response is:

- Newtonian-like at large `r`
- regularized at small `r`

At large distance,

\[
G(r) \sim \frac{1}{4\pi c^2 r}
\qquad
(r \gg \xi),
\]

while near the source,

\[
G(r)
  \to
  \frac{1}{2\pi c^2 \xi}
\qquad
(r \to 0),
\]

so the Yukawa subtraction removes the short-distance singularity.

## What This Rules Out

This result rules out the simplest "gravity dies because the scalar LogSE is gapped" reading.

If one keeps the full linearised static operator, the scalar density response does carry a massless long-range component.

So the empirical objection

- "if the static mode were pure Yukawa with range `\xi \sim 4\times 10^{-13}` m, SSV would be dead macroscopically"

does **not** follow from the linearised static LogSE calculation itself.

## What Remains Open

The real open problem is now sharper:

The issue is not whether a massless static Green's function exists. It does.

The issue is:

- what source functional of the proton breather couples into that massless branch,
- how the resolved static deficit profile projects onto that source,
- and how that static source picture matches the radiation-zone Bjerknes picture in Paper II.

In other words, the unresolved step is not the existence of the long-range kernel. It is the correct proton coupling to that kernel.

## Consequence For The Current Gravity Track

This changes the priority ordering.

Before more reduced `Q_p` ansatz fitting, the repo should treat the following as the actual open tasks:

1. derive the proton source functional for the massless static branch,
2. identify which part of the static trefoil profile feeds that source,
3. reconcile that static source with the Paper II radiation-zone argument.

That is a more fundamental question than fitting another suppression ansatz on top of the current prototype states.

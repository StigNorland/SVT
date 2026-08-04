# Conditional screen-response theory

This note records the strongest response that follows from the C4 foundation
when a compact saturated screen patch and a capacity-limited boundary are added.
It is a conditional construction, not a completed gravitational theory.

## Local control

Let an invariant source demand be `D_M=eta M`. Conserved isotropic flux in
three spatial dimensions gives

\[
4\pi r^2F_3=\eta M,
\qquad g_N=\kappa_3F_3={GM\over r^2},
\qquad G={\kappa_3\eta\over4\pi}.
\]

The inverse-square form and composition independence follow if all mass-energy
has the same charge. The magnitude does not: `G` remains measured input unless
the microscopic factors are independently determined.

## Saturated patch and min-cut

On a two-dimensional spatial antichain, add global constants: site spacing
`ell_*`, encoded mass per filled site `m_*`, edge update capacity `nu_*`, and
response time `tau_R`. If mass `M` fills a minimum compact patch,

\[
{M\over m_*}\ell_*^2=\pi r_c^2,
\qquad r_c=\ell_*\sqrt{M\over\pi m_*}.
\]

The patch boundary contains `2 pi r_c/ell_*` cut edges. Saturating that positive
causal cut gives a throughput proportional to `sqrt(M)`. Conserved exterior
two-dimensional flux therefore has

\[
V_\infty^2=a_s r_c,
\qquad a_s={c^2\tau_R\nu_*\over\ell_*}.
\]

The Newtonian acceleration at the same radius is

\[
a_c={GM\over r_c^2}={\pi Gm_*\over\ell_*^2}.
\]

Imposing a continuous one-scale closure, `a_s=a_c=a_*`, yields

\[
\boxed{r_c=\sqrt{GM/a_*}},\qquad
\boxed{V_\infty^4=GMa_*}.
\]

Thus the baryonic Tully--Fisher exponent four can arise from a positive
max-flow/min-cut rather than phase cancellation. C4 alone does not establish
compact filling, cut saturation, or the equality `a_s=a_c`, and it does not
calculate `a_*`.

## Response-shape ambiguity

The integrated cut and core scale do not select a radial regulator. For
example, both positive normalized kernels

\[
K_{\rm CL}={r_c^2\over\pi(r^2+r_c^2)^2},\qquad
K_G={e^{-r^2/r_c^2}\over\pi r_c^2}
\]

are compatible with the same total charge, central regularity, and exterior
`1/r` acceleration. Their accelerations,

\[
g_{\rm CL}={V_\infty^2r\over r^2+r_c^2},\qquad
g_G={V_\infty^2\over r}(1-e^{-r^2/r_c^2}),
\]

differ by about 26% at `r=r_c`. The issue-225 cored-log law is consequently a
representative phenomenology, not a unique C4 derivation.

For a finite reference radius `R`, that representative does have an exact C4
availability map:

\[
\Phi_s={V_\infty^2\over2}\ln{r^2+r_c^2\over R^2+r_c^2}\le0,
\qquad A_s=e^{\Phi_s/c^2},\qquad q_s=1-A_s.
\]

An outer reference is necessary; an unbounded positive logarithmic potential
cannot be interpreted as a globally valid availability.

## Boundary of the result

The static representatives are conservative and bounded on a finite domain,
but no C4 response action currently fixes retardation, radiation, binary
orbital loss, polarization, or a host/satellite external-field marginal. The
statement `c_screen <= c` also does not derive equality with the measured
gravitational-wave speed. These omissions prevent promotion to H-SSV-III or a
frozen H-SSV-IV population test.

## Hierarchical coherence-screen extension

After this audit was frozen, C5 was proposed: every sufficiently coherent
system has a common effective screen, so subsystem screens may range across
many scales and be nested or overlapping. This is compatible with C4 when each
screen is an effective causal cut or subsystem algebra within the one global
state. It is not compatible with counting the same fundamental gate capacity
once for every enclosing screen.

C5 could describe shared host/satellite and galaxy/cluster states, but it needs
an objective coherence criterion, a one-count capacity ledger, and a response
composition law. Until those are derived it is an ontology for the hierarchy,
not a force-law closure. The full requirements are recorded in
`results/issue-227/06-hierarchical-screen-addendum.md`.

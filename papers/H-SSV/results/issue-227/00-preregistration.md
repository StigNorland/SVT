# Issue #227 — H-SSV-II response preregistration

Status: **frozen before issue-227 instruments and verdict**

## Question

Does the C4 quantum-causal screen fix a Newtonian-to-galactic gravitational
response—including transition scale and baryonic amplitude—without choosing a
constitutive law from galaxy residuals?

## Evidential boundary

The issue-225 cored-logarithmic comparison is known, so this is not blind with
respect to the candidate shape. No issue-225 per-galaxy parameter, likelihood,
residual or winner may enter this derivation.

The observational scaling gate is fixed independently by the 153-galaxy SPARC
BTFR analysis of Lelli et al. (2019): for flat velocity, the reported best-fit
`M_bar`--`V_f` slope is `3.85 +/- 0.09`, with systematic choices spanning
approximately `3.5--4.0` ([arXiv:1901.05966](https://arxiv.org/abs/1901.05966)).
A predicted slope `2` is therefore a failure; the target foundation exponent
is `4`.

The standard measured `G` may be imported and must then be labelled input. No
acceleration scale is imported into the derivation. The often-used
`1.2e-10 m s^-2` value may be used only as a post-derivation conditional scale
check, never to select a law or coefficient.

## Frozen C4 inputs

- one global quantum causal screen with two-dimensional spatial antichain
  connectivity;
- local causal gates and no signaling;
- one topological site state capacity `ln d_e` and update capacity `nu_*`;
- one moving-particle state and update capacity;
- positive bilateral gate demand;
- `q=j/nu_max`, `A=1-q`, `Phi=c^2 ln A`;
- finite state/update capacity and a closed global energy-information ledger.

C4 did **not** fix a spatial source map, graph metric, continuum constitutive
law, site length, mass encoded per site, response time, or dynamical radiation
sector. H-SSV-II must expose every such addition.

## Candidate ladder

### T0 — local three-dimensional conserved flux

For an invariant maintenance demand `D_M=eta M`, isotropic local conservation
gives

\[
4\pi r^2F_3=\eta M,
\qquad g_N=\kappa_3F_3={GM\over r^2},
\qquad G\equiv{\kappa_3\eta\over4\pi}.
\]

This is the local control. Unless `kappa_3 eta` is independently known, `G` is
calibrated/imported, not derived.

### T1 — linear two-dimensional screen flux

For the same additive demand,

\[
2\pi rF_2=\eta M
\quad\Longrightarrow\quad
V_\infty^2\propto M,
\quad V_\infty^4\propto M^2.
\]

It is the expected G3 negative control and also lacks the local inverse-square
limit.

### T2 — linear 3D-to-2D crossover

T2 uses T0 locally and T1 outside a transition radius. Changing dimension
changes radial shape, but a linear source still gives `V_inf^2 proportional
to M`. A crossover alone cannot repair the BTFR exponent.

### T3 — saturated compact patch and causal min-cut

Introduce only global continuum constants:

| symbol | units | meaning |
|---|---:|---|
| `ell_*` | m | screen-site spacing on a spatial antichain |
| `m_*` | kg | invariant baryonic mass-energy encoded per filled site |
| `nu_*` | s^-1 | maximum update rate per cut edge/site |
| `tau_R` | s | response time converting boundary throughput to load |

A source of invariant baryonic mass `M` occupies the minimum compact saturated
patch of `N=M/m_*` sites. Its area and core radius are

\[
N\ell_*^2=\pi r_c^2,
\qquad
r_c=\ell_*\sqrt{M\over\pi m_*}.
\]

Every causal update from the filled patch to the exterior crosses its graph
cut. In two dimensions the compact-patch cut has

\[
|\partial P|={2\pi r_c\over\ell_*}\propto\sqrt M,
\qquad
J_\partial=\nu_*|\partial P|.
\]

If that cut is the bottleneck, exterior two-dimensional flux conservation
gives

\[
V_\infty^2
= {c^2\tau_RJ_\partial\over2\pi}
=a_s r_c,
\qquad
a_s\equiv{c^2\tau_R\nu_*\over\ell_*}.
\]

The Newtonian acceleration at the capacity radius is

\[
a_c={GM\over r_c^2}={\pi Gm_*\over\ell_*^2}.
\]

A continuous one-scale crossover requires the **closure condition**
`a_s=a_c=a_*`. If it holds,

\[
r_c=\sqrt{GM\over a_*},
\qquad
V_\infty^2=\sqrt{GMa_*},
\qquad
\boxed{V_\infty^4=GMa_*}.
\]

The square-root amplitude is a max-flow/min-cut result from positive local
gate capacities; it is not coherent amplitude cancellation.

The audit must distinguish a consequence from an added closure: C4 supplies
finite capacities and local gates, but it did not prove compact filling,
two-dimensional isoperimetry, cut saturation, or `a_s=a_c`.

## Core regulator non-uniqueness control

The same T3 total cut charge and core scale admit at least two positive,
normalized two-dimensional source kernels:

\[
K_{\rm CL}(r)={r_c^2\over\pi(r^2+r_c^2)^2},
\qquad
K_G(r)={e^{-r^2/r_c^2}\over\pi r_c^2}.
\]

They yield, respectively,

\[
g_{\rm CL}={V_\infty^2r\over r^2+r_c^2},
\qquad
g_G={V_\infty^2\over r}\left(1-e^{-r^2/r_c^2}\right).
\]

Both are linear at the origin, asymptote to `V_inf^2/r`, have the same
positive charge and scale, and obey C4 capacity bounds. If C4/T3 cannot select
between them before data, the exact cored-logarithmic regulator is not derived.

## Exact C4 availability map

For a finite exterior reference radius `R>r`, the cored-log representative is

\[
\Phi_s(r)={V_\infty^2\over2}
\ln{r^2+r_c^2\over R^2+r_c^2}\le0,
\qquad
A_s=e^{\Phi_s/c^2},
\qquad q_s=1-A_s.
\]

This is required because C4 fixes `A=1-q`; using only the weak-field linear
map is not an exact pass. An infinite positive logarithmic potential is
inadmissible without an outer boundary/reference.

## Gates and decision rules

| gate | frozen rule |
|---|---|
| G1 | T0 must recover `GM/r^2` with universal mass-energy charge. `G` is input unless microconstants independently reproduce it. |
| G2 | A transition and `r_c(M)` must follow from frozen global constants. If more than one positive kernel survives without a selection principle, exact cored-log status is phenomenology only. |
| G3 | The predicted BTFR `M`--`V` exponent must lie in `3.5--4.0`; T3 must return exactly `4`, while linear 2D must return `2`. |
| G4 | The static response must be conservative and bounded. A dynamic gate/action must bound orbital energy loss; absence of a radiation calculation is not a pass. |
| G5 | `V_inf(M, observables)` and `r_c(M, observables)` must contain no galaxy-specific halo parameters. Every global constant, especially `a_*` and the regulator, must be fixed independently before H-SSV-IV. |
| G6 | The response must address the current Cassini external-field/tidal constraint, binary radiation, preferred-frame effects, and the GW170817 propagation-speed interval. “Signal speed <=c” alone is insufficient. |

For G6 the fixed external references are:

- Cassini/DE440: `Q2=(1.6 +/- 1.8)e-27 s^-2` (Park et al. 2026,
  [arXiv:2602.17884](https://arxiv.org/abs/2602.17884));
- GW170817/GRB 170817A:
  `-3e-15 <= (c_g-c)/c <= 7e-16` (LIGO/Virgo/Fermi/INTEGRAL 2017,
  [arXiv:1710.05834](https://arxiv.org/abs/1710.05834)).

The decision is:

- **PROCEED** only if one candidate passes G1--G6 and freezes a population law;
- **PHENOMENOLOGY ONLY** if the capacity construction reproduces shape/scaling
  but a kernel, scale, or dynamic/local closure remains selected or unfixed;
- **NEGATIVE** if the scaling, sign, stability or tested local limit is wrong.

No galaxy outcome is opened in this issue.

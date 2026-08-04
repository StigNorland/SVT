# Issue #227 — derivation and dimensional checks

Status: **complete**

The tested candidate ladder is T0 local 3D flux, T1 linear 2D flux, T2 a
linear dimensional crossover, and T3 a saturated compact patch with a causal
min-cut. No issue-225 galaxy fit or residual entered the calculation.

## Analytic result

T0 recovers `g=GM/r^2`, conditionally on a universal mass-energy charge, with
`G` explicitly imported. T1 and T2 retain a linear two-dimensional source:
`V_inf^2 proportional M`, hence `V_inf^4 proportional M^2`; their predicted
`M`--`V` slope is 2 and fails the frozen 3.5--4.0 BTFR interval.

T3 adds `ell_*`, `m_*`, `nu_*`, and `tau_R`. Compact area filling gives
`r_c proportional sqrt(M)`, while the saturated boundary min-cut gives a
positive throughput proportional to `sqrt(M)`. If the service and crossover
accelerations are identified,

\[
a_s={c^2\tau_R\nu_*\over\ell_*}
=a_c={\pi Gm_*\over\ell_*^2}=a_*,
\]

then `r_c=sqrt(GM/a_*)` and `V_inf^4=G M a_*`. The executable log-log audit
returns slopes 2.0000000000000004 for T1 and 4.000000000000001 for T3.

## Dimensional receipt

| quantity | derived dimension |
|---|---|
| `r_c` | length |
| `a_s=c^2 tau_R nu_*/ell_*` | acceleration |
| `a_c=pi G m_*/ell_*^2` | acceleration |
| `V_inf^2=a_* r_c` | velocity squared |

Both candidate regulators integrate to unit positive charge within numerical
integration error. They share the central and asymptotic limits but differ by
0.264241 at the core radius. This is a constructive non-uniqueness result.

The exact finite-domain cored-log map satisfies `0<A<=1`, `0<=q<1`, and
`A=1-q`; the result is not restricted to the weak-load linearization.

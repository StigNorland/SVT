# Series-wide N-gate report (#182)

Gate: **N-GATE PASS for the whole series — no recomputation required**

## The decisive fact

Every instrument family in the repository implements the logarithmic potential
with the **adopted (stable-vacuum) sign**:

| file | implementation |
|---|---|
| `paper_i/trefoil_observables.py:25` | `log_pressure * (rho*log(rho) - rho + 1.0)` |
| `paper_i/trefoil_breather_observables.py:66` | same form |
| `paper_i/hopf_full_relax.py:106`, `hopf_saturation_relax.py:102` | same form |
| `paper_i/gradient_flow_numba.py:159` | same form |
| `paper_ii/reconnection_supplement.py:304,326` | same form |

Searches for a negative coupling (`-log_pressure`, `log_pressure = -…`) return
**zero hits** across the entire repository. Defaults are `0.5` (17 occurrences)
or `1`, always positive.

With $\bar\rho=1$, $b(\rho\ln\rho-\rho+1)\equiv +b\rho[\ln(\rho/\bar\rho)-1]+b$,
which is exactly the corrected potential adopted on 2026-07-27 — verified
symbolically, with $\mu=+b\ln\rho$, $\rho\mu'=+b>0$, $P=b(\rho-1)$ and $V$
bounded below with minimum zero at the background.

**The entire numerical corpus of the series has always been on the stable
branch.** The sign defect is confined to printed prose.

## Second reason: everything is dimensionless

46 of 78 `paper_i` scripts declare $\xi=1$, $\rho_0=1$, $c=1$; **all 66**
hard-coded `rho0` values are `1`; exactly one result note quotes a dimensionful
$\rho_0$, and it is the audit's own report. So D1's $\sqrt2$ and E5's factor
$2.7\times10^4$ move only paper-side conversions.

## Third reason: the mass chain is independent

$m_pc^2=N_Y\!\cdot\!F\!\cdot\!\mu_0$ with $\mu_0=m_ec^2/\alpha$ empirical and
$N_Y$, $F$ dimensionless. None of $\xi$, $b$, $\rho_0$ enters.

## The one exception

**SSV-VII-b `main.tex:315,362`** use $\xi$ in horizon-area and entropy counting.
Quantities scaling as $A_H/\xi^2$ move by a factor **2**, and $1/\xi$ by
$\sqrt2$. This is the only place in the series where the D1 correction reaches a
stated numerical result rather than a definition, and it is a paper-side
computation, not an instrument output.

## Verdict

**N-GATE PASS.** Zero result notes require recomputation across all twelve
papers. One paper-side recomputation is owed (SSV-VII-b horizon counting).

## Flagged for the solver track

The kinetic term `0.5 * grad_sq` fixes $\hbar=m=1$, so the implied sound speed is
$c_s=\sqrt{\texttt{log\_pressure}}$: at the canonical `0.5` that is $1/\sqrt2$,
while 46 scripts declare "longitudinal speed $c=1$". Changes no result (all
observables are in $\xi$-units) but should be reconciled — and it is the same
$\sqrt2$ that appears in $\xi=\hbar/(\sqrt2 m_0c)$, which may not be coincidence.

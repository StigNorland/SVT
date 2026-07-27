# SSV-I N-gate — numerical corpus

Status: **closure-grade**

Gate: **N-GATE PASS — no recomputation required**

The N-gate asked whether the D1 (sign, $b$, $\xi$) and E5 ($\rho_0$) corrections
invalidate SSV-I's 138 result notes and 78 instrument scripts. They do not, for
three independent reasons, each verified below.

## 1. The solvers already use the adopted sign

`instruments/paper_i/trefoil_observables.py:25` implements the potential as

```python
potential = log_pressure * (rho * np.log(rho) - rho + 1.0)
```

with `log_pressure` **positive** (0.5 canonical). Symbolically, with
$b=$ `log_pressure` and $\bar\rho=1$:

$$V(\rho)=b\left(\rho\ln\rho-\rho+1\right) \;\equiv\; +b\,\rho\left[\ln(\rho/\bar\rho)-1\right]+b$$

verified identical to the **adopted corrected form** (sympy, exact). Its
properties:

| | |
|---|---|
| $\mu=dV/d\rho$ | $+b\ln\rho$ |
| $\rho\mu'(\rho)$ | $+b>0\;\Rightarrow\;c_s^2>0$, **stable** |
| $P=\rho\mu-V$ | $b(\rho-1)$, $dP/d\rho=+b>0$ |
| $V(\bar\rho=1)$ | $0$ — minimum, bounded below |

**The numerical corpus has been on the stable-vacuum branch all along.** The
sign defect is confined to the printed paper; no solver, no state file and no
result note carries the unstable sign. Nothing needs re-running.

This is the third instance of the same pattern in this audit: the **code was
right and the prose was wrong** — as with the trefoil (D2) and with SSV-VII-b's
gravitational potential.

## 2. Every result is dimensionless

| probe | result |
|---|---|
| scripts declaring $\xi=1$, $\rho_0=1$, $c=1$ | 46 of 78 |
| distinct hard-coded `rho0 =` values across `paper_i` | **all 66 are `1`** |
| scripts hard-coding a physical $\xi$ | 2 |
| result notes quoting a dimensionful $\rho_0$ | **1 — this audit's own E-gate report** |

Since $\xi$, $\rho_0$ and $c$ are set to unity throughout, changing their
*physical* values cannot change any computed dimensionless output. D1's $\sqrt2$
in $\xi$ and E5's factor $2.7\times10^4$ in $\rho_0$ move only the
paper-side conversions, which are prose and already covered by the E-gate.

## 3. The mass chain does not touch the corrected quantities

$$m_pc^2 = N_Y\cdot F\cdot\mu_0,\qquad \mu_0=m_ec^2/\alpha$$

$\mu_0$ is **empirical** (inputs $m_e$, $\alpha$); $N_Y$ and $F$ are
**dimensionless** lattice observables. None of $\xi$, $b$, $\rho_0$ enters. The
proton prediction is therefore untouched by D1 and E5 — it stands or falls on
its own grounds, which `proton-mass-final-checkpoint.md` already records
honestly (fine-grid product $\approx10$–$13$ rather than $13.44$; the $0.3\%$
figure was a coarse-grid artefact).

## Verdict

**N-GATE PASS.** No result note requires recomputation. SSV-I's numerical corpus
is invariant under both corrections.

## One item flagged for the solver track

With the kinetic term written `0.5 * grad_sq` the code fixes $\hbar=m=1$, so the
implied sound speed is $c_s=\sqrt{b}=\sqrt{\texttt{log\_pressure}}$:

| `log_pressure` | $c_s$ (code units) |
|---|---|
| 0.5 (canonical) | 0.707107 |
| 1.0 | 1.000000 |

But 46 scripts declare the nondimensionalisation *"$\xi=1$, background density
$\rho_0=1$, longitudinal speed $c=1$"*. At the canonical `log_pressure = 0.5`
the model's own sound speed is $1/\sqrt2$, not 1.

This may be a deliberate convention (the $c_{\rm eff}$ calibration recorded for
the Paper-II reconnection work fixed `log_pressure = 0.5`) rather than a
mismatch — the two could differ by how $c$ is defined relative to the healing
length. **Not verdicted here**: it changes no result in this gate, since every
observable is expressed in $\xi$-units. Flagged so the solver track can confirm
that the declared $c=1$ and the implied $c_s=1/\sqrt2$ are reconciled, and note
that this is the same $\sqrt2$ that appears in D1's $\xi=\hbar/(\sqrt2 m_0c)$ —
which may not be a coincidence and is worth checking directly.

## Machine-checked

The identity between the implemented potential and the adopted corrected form is
reproduced in `instruments/paper_i/ssv_i_audit_2026.py`, tested in
`instruments/test/paper_i/test_ssv_i_audit_2026.py`.

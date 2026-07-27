# SSV-V — E-gate report

Gate: **E-GATE FAIL — a load-bearing argument inverts under the adopted branch** · #187

## E1 — "Argument 1: the LogSE chemical-potential floor" **inverts**

`main.tex:629` uses a **third** printed variant of the potential,
$V(\rho)=-b\rho\ln(\rho/\rho_0)$ (no $-1$), giving
$\mu=-b[\ln(\rho/\rho_0)+1]$ — internally correct for that $V$.

The stable-Planck-remnant argument then turns on:

> which diverges to $+\infty$ as $\rho\to0$. Any region whose density tries to
> fall below $\rho_0$ pays a logarithmic chemical-potential cost; the surrounding
> saturated medium … therefore exerts an inward pressure on any sub-saturated
> region.

Symbolic check of all three printed variants:

| variant | $\rho\mu'$ | $c_s^2$ | $\mu$ as $\rho\to0$ |
|---|---|---|---|
| SSV-I `eq:pot` / SSV-III L1169 | $-b$ | $<0$ **unstable** | $+\infty$ |
| SSV-V L629 | $-b$ | $<0$ **unstable** | $+\infty$ |
| **ADOPTED (D1)** | $+b$ | $>0$ **stable** | $-\boldsymbol\infty$ |

**Under the adopted branch $\mu\to-\infty$ as $\rho\to0$.** There is no
chemical-potential floor and no confining inward pressure — the argument does not
merely weaken, it **reverses sign**.

**Verdict `MISDERIVED` under the adopted theory.** SSV-V's Argument 1 for a
stable Planck-scale remnant depends on the *rejected* sign. It must be withdrawn
or replaced. Whether the remnant survives on other grounds (Arguments 2+) is not
settled here.

This is the clearest example in the series of why the D1 branch decision was not
cosmetic: an argument built on the unstable sign can look perfectly sound and
still be load-bearing for a headline conclusion.

## E2 — the symbol $b$ is overloaded across papers

`main.tex:142` writes the nonlinear potential as $b\hbar\ln(\rho/\rho_0)$ with
$c_s=\sqrt{b\hbar/m}$. With Paper I's $b$ (an energy) this is dimensionally
wrong: $[b\hbar/m]=\mathrm{J^2\,s\,kg^{-1}}$, not a velocity squared. It is
consistent **only** if SSV-V's $b$ is a *frequency*, in which case
$[b\hbar/m]=\mathrm{J/kg}=\mathrm{m^2s^{-2}}$ ✓.

**Verdict:** not an error inside SSV-V, but the same symbol denotes different
quantities in Paper I and Paper V with no statement of the change. Must be
disambiguated at reconciliation.

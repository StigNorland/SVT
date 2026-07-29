# SSV-VII-b — change record

The paper states **current status only**. Its history lives here.

Entries link the issue that drove each change. Git history carries the rest.

---

## 2026-07-29 — [#213](https://github.com/StigNorland/SVT/issues/213) · the cosmological-constant relation was dimensionally inhomogeneous

Found by the new programme-wide symbol census (`instruments/tools/conventions.py`),
which flagged `\Lambda` as carrying **three** dimensions across the series —
dimensionless in SSV-I and SSV-III, a wavenumber `\xi^{-1}` in SSV-III, and a
curvature in SSV-VI, SSV-VII-b and SSV-IX. Checking the relation that defines
the cosmological one showed the printed expression did not have the dimension
the paper's own text quotes for it.

As printed:

> `\Lambda = \frac{8\pi G}{c^2}\,\frac{P_0}{\rho_0 c^2}`

`[G/c^2] = L M^{-1}` and `P_0/(\rho_0 c^2)` is dimensionless, so the expression
has dimension **L M⁻¹** — while SSV-VII-b's own text quotes
`\Lambda \sim 10^{-52}\,\mathrm{m}^{-2}`, i.e. **L⁻²**. The prefactor is
missing `\rho_0`. Corrected:

> `\Lambda = \frac{8\pi G \rho_0}{c^2}\,\frac{P_0}{\rho_0 c^2} = \frac{8\pi G P_0}{c^4}`

The **value** was never wrong — `8\pi G P_0/c^4` is what the surrounding
argument uses, and no downstream number moves. What was wrong was the printed
expression, for an unknown length of time, in two papers.

Both forms are now in `instruments/tools/dimensions.py` as
`eq:Lambda-as-printed-pre-213` (recorded `inhomogeneous`, `printed=False`) and
`eq:Lambda`, so the checker is demonstrated to catch the class rather than
merely to agree with corrected algebra. SSV-VII-b's `FREE` set is empty, which
makes the defect *unrepairable* by any assignment rather than merely unresolved.

**Why no gate caught it:** `dimensions.py` covered SSV-I, II, V and VII-a only.
Neither SSV-VI nor SSV-VII-b had ever been checked.


## 2026-07-29 — [#210](https://github.com/StigNorland/SVT/issues/210) · conditional-gravity repair

The conversion from healing length to Newton's constant is corrected to
\(G=c^3\xi^2/\hbar=c^2\xi/(\sqrt2m_0)\), consistently carrying
\(m_0=m_P/\sqrt2\).  Jacobson's argument, Kerr/no-hair imports and the
strong-field numerical checks are now labelled conditional on their GR and
entropy-density inputs.  Evaluating observables in an inserted Schwarzschild
metric verifies that metric; it does not derive the metric from SSV.

Load-bearing wording removed or replaced (verbatim):

> “The full Einstein equations are recovered nonlinearly.”

> “These are direct consequences of the Jacobson route once the SSV picture
> is accepted.”

> “Numerical verification of three strong-field observables at the
> SSV-identified metric reproduces the exact GR results.”

## 2026-07 — [#198](https://github.com/StigNorland/SVT/issues/198) · Planck length printed two ways

The paper printed `ell_P` as both `1.6` and `1.616e-35` m. Both are now the
generated macro `\ssvEllP` (rule 14), with four claim guards (rule 16).

## 2026-07 — [#190](https://github.com/StigNorland/SVT/issues/190) · C- and E-gate audit

Reports in [`results/audit-2026/`](results/audit-2026/).

## 2026-07 — [#183](https://github.com/StigNorland/SVT/issues/183) · the D1 `sqrt2` correction

`xi = ell_P` is **unchanged** by the correction; what moves is the mass,
`m_0 = m_P/sqrt2`. At fixed `m_0` and horizon area the entropy would double —
a factor 2, not `sqrt2`, because entropy counts one degree of freedom per
`xi^2`.

# SSV-VII-b — change record

The paper states **current status only**. Its history lives here.

Entries link the issue that drove each change. Git history carries the rest.

---

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

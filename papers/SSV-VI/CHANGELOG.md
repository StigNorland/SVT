# SSV-VI — change record

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


## 2026-07-29 — [#203](https://github.com/StigNorland/SVT/issues/203) · dSph model-B normalisation

Four defects in `instruments/paper_vi/dsph_ledger.py`. Two constants were
labelled as coming from H9's receipt and did not: H9 records a BTFR velocity of
**189.02 km/s**, not 220, and contains **no MW circulation radius at all**.
Model B also used `R_e` where the rest of the ledger uses `r_1/2`. The
constants are now read from the H9 receipt rather than retyped.

- median model-B shortfall **2.687 → 2.320 dex** (factor ~500 → **209**)
- **B1 is now reported sweep-fragile**, not sweep-stable: adding the MW
  normalisation radius as a sweep axis took the grid 27 → 81 points, and 6
  points return *inconclusive*. All six sit at `v_rot = 10 km/s`, above the
  `≤ 3 km/s` observational limit. Within that limit the verdict holds at all 54
  points with 0.174 dex of margin.

The earlier text read "the verdict is stable across the entire pre-registered
robustness sweep … 27 combinations". That was true of the grid it was computed
on; the grid was missing the axis the conclusion turns on.

SSV-VI's load-bearing numbers are now generated macros (rule 14) with claim
guards (rule 16), so the shortfall is no longer typed in three places.

## 2026-07 — [#182](https://github.com/StigNorland/SVT/issues/182) · C- and E-gate audit

Reports in [`results/audit-2026/`](results/audit-2026/). Retired mechanisms —
the CBH standing wave ([#122](https://github.com/StigNorland/SVT/issues/122))
and CBH overtones ([#124](https://github.com/StigNorland/SVT/issues/124)) — are
retained in the paper's own falsification-record appendix.

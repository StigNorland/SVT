# SSV-VI — change record

The paper states **current status only**. Its history lives here.

Entries link the issue that drove each change. Git history carries the rest.

---

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

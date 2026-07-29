# Issue #213 Parts B/C — shared-value registry result

**Date:** 2026-07-29  
**Pre-registration:** [issue #213](https://github.com/StigNorland/SVT/issues/213)  
**Comparison commit:** `a85023c` (the last Part-A commit, before value migration)

## Result

Nine observed quantities now have one programme-level numerical source in
`instruments/series_values.py`, one series receipt in
`papers/shared_values_receipt.json`, and one generated `\ssv*` macro in every
paper that declares the quantity.  The declared consumers are SSV-Alpha,
SSV-I, SSV-II and SSV-IV.

This is prospective prevention with one present-day finding.  It is not a
complete inventory of load-bearing numbers.

## D1 — did cross-paper drift exist?

**Yes: one registered physical quantity disagreed.**

The proton reduced Compton wavelength \(\bar{\lambda}_p=\hbar/(m_pc)\) appeared as both
\(2.0\times10^{-16}\,\mathrm{m}\) and
\(2.1\times10^{-16}\,\mathrm{m}\):

| pre-migration site at `a85023c` | printed value |
|---|---:|
| `papers/SSV-I/main.tex:406` | \(2.10\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-II/main.tex:90` | \(2.0\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-II/main.tex:293` | \(2.10\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-II/main.tex:295` | \(2.10\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-II/main.tex:1251` | \(2.10\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-II/main.tex:3215` | \(2.0\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-IV/main.tex:175` | \(2.1\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-IV/main.tex:968` | \(2.10\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-IV/main.tex:998` | \(2.0\times10^{-16}\,\mathrm{m}\) |
| `papers/SSV-IV/main.tex:1311` | \(2.0\times10^{-16}\,\mathrm{m}\) |

The common source computes \(2.103\ldots\times10^{-16}\,\mathrm{m}\), rendered
at the papers' two-significant-figure precision as
\(2.1\times10^{-16}\,\mathrm{m}\).  All ten sites now use
`\ssvProtonReducedComptonWavelength`.

Two further differences were precision-only, not physical disagreements:

- \(m_p/m_e\) appeared as `1836` and `1836.15`; the shared rendering is
  `1836.15`.
- \(m_\tau c^2\) appeared as `1776.860` and `1776.86` MeV; both denote the same
  central value and the shared rendering is `1776.86`.

The charged-pion sites agreed at their common rounded precision, but SSV-I's
single high-precision line still carried the older
\(139.57018\pm0.00035\) MeV pair.  The shared source now uses the
[PDG 2024 summary](https://pdg.lbl.gov/2024/tables/rpp2024-sum-mesons.pdf)
\(139.57039\pm0.00018\) MeV value, so both the rounded and precise sites come
from the same central value.  This is a source update rather than a
cross-paper disagreement.

The other five registered quantities agreed at their declared printed
precision.  Thus the pre-registered prediction “low but non-zero” is met by
**one physical drift**, with two notation/precision differences and one
outdated high-precision observation corrected.

## D2 — build cost

Measured with:

```text
/usr/bin/time -f 'ELAPSED_SECONDS=%e' \
  python instruments/tools/build_paper.py --all --gate-only
```

| state | elapsed |
|---|---:|
| before Parts B/C | 17.88 s |
| after Parts B/C | 18.27 s |
| increment | **0.39 s** |
| pre-registered budget | +30 s |

The increment is below budget by 29.61 s.  The stronger guarantee therefore
remains active: each participating paper's gate re-runs the shared source and
checks the receipt, rather than trusting only the last recorded run.

## D3 — coverage, stated without implying completeness

“Shared” below means a value declared in at least two papers.  “Local” is the
older rule-14 per-paper registry.  The last column is deliberately not a count
unless a semantic inventory has actually been performed.

| paper | local generated | shared registered | known unregistered load-bearing surface |
|---|---:|---:|---|
| SSV-Alpha | 0 | 1 | not enumerated; no completeness claim |
| SSV-Goldstone | 0 | 0 | not enumerated; no completeness claim |
| SSV-I | 3 | 8 | \(N_Y=3.007\), \(F\approx4.47\), and the \(N_YF=13.28\text{--}13.62\) bracket remain unregistered |
| SSV-II | 0 | 9 | \(N_YF\approx13.44\), \(6.72\), \(\alpha_G\), and derived comparison values remain unregistered |
| SSV-III | 0 | 0 | not enumerated; no completeness claim |
| SSV-IV | 0 | 3 | observational bounds and instrument verdict numbers remain unregistered |
| SSV-IX | 0 | 0 | not enumerated; no completeness claim |
| SSV-V | 0 | 0 | \((\bar{\lambda}_p/\ell_P)^2\approx1.69\times10^{38}\) remains unregistered |
| SSV-VI | 10 | 0 | non-dSph load-bearing numbers are not enumerated |
| SSV-VII-a | 0 | 0 | not enumerated; no completeness claim |
| SSV-VII-b | 4 | 0 | non-Planck-scale load-bearing numbers are not enumerated |
| SSV-VIII | 0 | 0 | not enumerated; no completeness claim |

The candidate \(N_YF\) values are intentionally not promoted: their
cutoff-dependent source is not a stable instrument output.  Registering
`13.44` now would turn a candidate calibration into a programme-wide
authoritative number, exactly the “propagate one wrong value everywhere”
failure called out in the issue.

## Part C guard

`test_no_shared_literal_survives` scans each declared consumer for the exact
old spellings recorded in `gen_values.SHARED`.  The same check runs in
`build_paper.py::gate_values`, so it applies inside tables as well as prose.
The receipt/source check and the old-literal check are separate: a current
receipt does not pass if a paper retypes the value beside its macro.

## Negative result retained

This does **not** close FM21 in general.  The mismatched SSV-I form-factor table
that motivated #213 is still outside the registry because its 23-second
calculation has not been wired into a stable receipt.  An unregistered table
cell remains invisible.  Parts B/C make drift impossible only on the declared
surface and report that limited coverage explicitly.

## Part A follow-up — standard notation is enforced, not merely inventoried

The first Part-A implementation found that `\mu_0` carried three dimensions:
vacuum permeability, the SSV mass/energy scale, and a line tension.  It then
whitelisted that state as a known collision.  That was a useful census but a
**negative infrastructure result**: documenting a reader-facing ambiguity did
not remove it.

The paper surface now uses:

- \(m_\star=m_e/\alpha\) for the SSV mass scale;
- \(E_\star=m_\star c^2\) for its corresponding rest-energy scale;
- \(\varepsilon_{\rm line}\) for the cutoff-dependent line tension;
- \(\mu_0\) only for vacuum permeability; and
- \(\bar{\lambda}_p=\hbar/(m_pc)\) for the reduced proton Compton wavelength,
  replacing the project-specific \(a_p\).

The census distinguishes \(\bar{\lambda}_p\) from the ordinary
\(\lambda_p\).  The build gate rejects legacy `a_p`, the retired generated
macro name, and every non-Maxwell `\mu_0` in a paper.  This is deliberately a
small, high-confidence reserved-symbol surface; it does not certify the 100+
shared tokens that remain undeclared.

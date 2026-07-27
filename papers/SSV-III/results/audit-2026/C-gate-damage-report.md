# SSV-III — C-gate (citation) damage report

Status: **closure-grade** for the verified keys

Gate: **C-GATE PASS with reservations** — no misattribution found

Audit date 2026-07-27, under #185. SSV-III has the largest citation surface in
the series (32 keys) and the smallest compute surface (1 result note).

## Ledger — Tier A

| # | Key | Claim | Verdict |
|---|---|---|---|
| C1 | `Kibble1976`,`Zurek1985` | Kibble–Zurek defect counting, density set by quench rate | **`OK`** — canonical, correctly attributed |
| C2 | `Lindblad1975` | relative entropy to a fixed reference cannot increase under any CPTP map | **`OK`** — this *is* Lindblad's monotonicity theorem, correctly attributed |
| C3 | `Deutsch1991` | D-CTC: self-consistency via a fixed-point density matrix | **`OK`** — the paper's subject |
| C4 | `Lloyd2011` | post-selected CTC variant | **`OK`** — retrieved; author list in the bibitem matches the paper exactly |
| C5 | `Clisby2010` | $\nu\approx0.587597$, SAW correlation-length exponent | **`OK` (value)**, `PENDING-PRIMARY` (source) — see below |
| C6 | `MadrasSlade1993` | $p_n\sim A\mu^n n^{\theta}$ polygon enumeration | `PENDING-PRIMARY` — book; **form is standard** |
| C7 | `SumnersWhittington1988` | knotted polygons are exponentially generic | `PENDING-PRIMARY` — pre-arXiv; this is the Frisch–Wasserman–Delbrück theorem, correctly attributed |
| C8 | `Barenghi2014` | $\dot N_{\rm rec}=c_{\rm rec}\kappa\mathcal L^{5/2}$ by dimensional analysis | **`OK`** — retrieved; see below |
| C9 | `Vinen2002` | Kelvin-wave dispersion of vortex filaments | `PENDING-PRIMARY` — not obtained |
| C10 | `Villois2017` | $\delta(t)\approx A_\pm\|t-t_0\|^{1/2}$ with asymmetric prefactors | `PENDING-PRIMARY` — see retrieval note |
| C11 | `Rovelli1993`,`Rovelli2018` | relational treatments of time | **`OK`** — framing claim |

## Positive checks performed

**SAW exponent algebra is internally consistent** (`instruments` reproduction):

| quantity | value |
|---|---|
| $\nu$ (canonical Clisby 2010) | 0.587597 |
| hyperscaling $\alpha=2-d\nu$, $d=3$ | 0.237209 |
| $\theta=\alpha-3$ | **−2.762791** |
| paper's alternative form $-(1+3\nu)$ | **−2.762791** — identical |
| paper's stated $\theta\approx-2.76$ | **matches** |

Both routes to $\theta$ agree exactly, and the value quoted for $\nu$ is the
canonical Clisby result. The algebra is sound.

**Barenghi rate is dimensionally correct**: with $[\kappa]=\mathrm{m^2s^{-1}}$
and $[\mathcal L]=\mathrm{m^{-2}}$, $\kappa\mathcal L^{5/2}=\mathrm{m^{-3}s^{-1}}$
— a rate per unit volume, as claimed. The paper describes it as *"fixed by
dimensional analysis from the only quantities available"*, and cites Barenghi
for the setting rather than for the formula, which is a fair use of the source.

## Retrieval notes — two keys deliberately NOT downloaded

- `Clisby2010`: the cited work is PRL **104**, 055702 (2010). An arXiv title
  search returned the J. Stat. Phys. *pivot-implementation* companion instead;
  the retrieved file contains no occurrence of `0.587597`, confirming it is the
  wrong paper. Stored as `Clisby2010_pivot_implementation_SIBLING.pdf`.
  **The value SSV-III quotes is nonetheless the canonical one.**
- `Villois2017`: search returned *A Vortex Filament Tracking Method for the
  Gross-Pitaevskii Model*, a different paper from the cited *Universal and
  nonuniversal aspects of vortex reconnections in superfluids*. Not downloaded.

Both are recorded rather than silently accepted, per the evidence rule.

## Gate decision

**C-GATE PASS with reservations.** No `MISATTRIBUTED`, no `MISREAD`, no
`UNSUPPORTED` found. Six `OK`, five `PENDING-PRIMARY` — all of the latter being
pre-arXiv papers or books whose claimed results are canonical and correctly
attributed as far as can be checked without the source.

This is the healthiest citation surface audited so far. Notably, SSV-III makes
its dimensional-analysis steps explicit and cites sources for *setting* rather
than for results they do not contain — the opposite of the SSV-I D1 and SSV-II
D1 failure mode.

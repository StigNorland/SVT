# SSV-VI — C-gate damage report

Status: **closure-grade** for retrieved keys · Gate: **C-GATE PASS** (#188)

The only paper in the series resting on **observational data**, so the risk
profile differs: the failure mode is a mis-quoted number, not a mis-attributed
equation.

| # | Key | Claim | Verdict |
|---|---|---|---|
| C1 | `chemin2009` | M31 H I rotation curve, $r=1.14$–$38$ kpc, $n=98$ | **`OK`** — source states "measured out to **38 kpc**"; 1.14 present |
| C2 | `lelli2016` | SPARC: 175 galaxies with rotation curve + baryonic model | **`OK`** — title states "Mass Models for **175** Disk Galaxies" |
| C3 | `mcgaugh2012` | BTFR $M\propto v^4$ (slope $1/4$ in $v$–$M$) | **`OK`** — retrieved, *Baryonic Tully-Fisher Relation of Gas Rich Galaxies* |
| C4 | `mcgaugh2016` | radial acceleration relation | **`OK`** — retrieved |
| C5 | `ibata2013` | vast thin plane of corotating dwarfs around M31 | **`OK`** — retrieved |
| C6 | `gebhardt2001` | M33 has no supermassive black hole | **`OK`** — retrieved, title matches exactly |
| C7 | `flynn2026` | arXiv:2601.00522, empirical rotation-curve fit | **`OK`** — **exists as cited**, title verified |
| C8 | `toomre1964`,`toomre1981`,`linshu1964`,`mestel1963`,`ostrikerpeebles1973`,`hockneyeastwood1988` | Toomre $Q$, swing amplification, Lin–Shu pitch, Mestel profile, bar instability, PM solver | `PENDING-PRIMARY` — pre-arXiv papers and a book; all are canonical and correctly attributed as far as checkable |

All seven retrieved keys verified by title/content against their bibitems. No
misattribution found. `flynn2026` was checked specifically because a
2026 preprint ID is the kind of citation most likely to be wrong; it is correct.

Remaining check for the E-gate: the Lin–Shu pitch relation $\tan\alpha_m=mQ/4$
as used at L370 — the *form* of a marginal-stability pitch relation should be
re-derived rather than taken on trust, since `linshu1964` is not obtainable.

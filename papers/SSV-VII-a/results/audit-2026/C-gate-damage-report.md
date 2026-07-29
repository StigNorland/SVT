# SSV-VII-a — C-gate damage report

Status: **closure-grade** · Gate: **C-GATE PASS** · #189 · updated 2026-07-29

Six cited keys: `bbm1976`, `Madelung1927`, and the self-citations `SSV-I`,
`SSV-II`, `SSV-III`, `SSV-IV`, `SSV-V`.

| # | Key | Claim | Verdict |
|---|---|---|---|
| C1 | `bbm1976` | the LogSE admits an exact Gaussian stationary solution of width `sigma^2 = hbar^2/(2mb)`, shape-preserving | **`OK`** |
| C2 | `SSV-I` | `alpha = c_perp/c` fixes the chiral-shear coupling | **`OK`** |
| C3 | `SSV-I` | *the Coulomb reduction of the chiral-shear field* | **`MISATTRIBUTED`** — it is Paper II's; see E3 |
| C4 | `Madelung1927`, `SSV-III`, `SSV-IV`, `SSV-V` | lineage and cross-references | **`OK`** |

## C1 — resolved, and no longer on trust

The 2026-07-27 version of this report recorded C1 as `OK` "as attribution —
pre-arXiv, not retrieved, but this is unambiguously the BBM paper's result".
That is a weaker standard than rule 12 allows, and it has since been met
properly: `papers/cited/notes/bbm1976.md` carries verbatim paragraph evidence
from the printed article, registered `access: open`,
`evidence_mode: quotation`, `paragraph_required: true`.

The note quotes BBM's Eq. (3.3) nonlinear term `-b psi ln(|psi|^2 a^3)` with its
restriction to `b > 0`, and Eq. (6.1) defining `ell = hbar/sqrt(2mb)`.

**Two independent confirmations of E1 now agree.** BBM's published width
`ell^2 = hbar^2/(2mb)` is exactly what symbolic substitution returns for VII-a's
sign convention (`instruments/paper_vii_a/logse_gaussian.py`), and neither was
fitted to the other. The note's own verdict already draws the consequence: the
source supports the Gausson **for its `b>0` attractive convention** and does not
support using it on SSV's adopted branch.

Retrieval caveat, carried from `papers/cited/INDEX.md`: the host's anti-bot
layer prevented a reproducible local download, so this is one of the three notes
whose quotations were checked by a human but are not re-fetchable by script.
The verdict stands; what is weaker than rule 12's wording is *reproducibility*,
not correctness. Recorded under FM5.

## C3 — a self-citation pointing at the wrong paper

`eq:Veff-coulomb` was justified as "the content of Paper I's electromagnetism
sector". Paper I does not contain it. `SSV-I/main.tex:374` states the chiral
stiffness acts "in the statics of charged defects (**Paper II's Coulomb
sector**)", and the Bernoulli-pressure derivation of `F_C = alpha hbar c/r^2`
is at `SSV-II/main.tex:490` ff.

VII-a did not cite `SSV-II` at all. A paper's central effective potential was
sourced to a companion that routes it elsewhere — the same defect shape as a
misattributed external citation, inside the series where it is easier to miss
because both papers are the same author's.

**Repaired:** `SSV-II` added to the citation list and the attribution corrected
in place. Full analysis in the E-gate report, E3.

## The section is voided by the D1 branch decision

Unchanged from the earlier report and now machine-checked: under SSV-I's D1
decision the BBM Gausson does not exist, so `eq:gausson` has no solution under
the adopted theory. Per the owner's decision of 2026-07-28,
§"Saturation by the Gausson" is **retained as an explicitly labelled
rejected-branch record** rather than deleted — the same treatment Paper I gives
its own rejected sign.

## Uncited bibitems

None. All six keys resolve to citations in the text, and the shared
`papers/cited/references.bib` carries no VII-a-only entries. Checked by
`instruments/tools/bibliography.py` at every gated build.

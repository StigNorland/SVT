# SSV-II — E-gate report

Gate: **E-GATE FAIL (one defect, already known to the paper)** · #184

## E1 — `eq:maxwell` contradicts the paper's own #138 computation

`main.tex:508` states the vacuum Maxwell equations as a derived result. The
paper's own record, two paragraphs below, says the #138 linearization found the
transverse wave equation does **not** arise from the LogSE + chiral-shear + CP¹
functional around the uniform vacuum, and that **the chiral term is silent at
linear order**.

Independently, #180 P4 (S route) established that one scalar Goldstone cannot
furnish two transverse photon helicities. Three independent routes agree.

**Verdict `MISDERIVED`.** `eq:maxwell` must carry the #138 status at the point of
statement or move into the historical-record subsection. Citations to `Barcelo`
(and `Volovik` for a one-component Madelung system) withdraw with it.

## E2 — inherited from D1

`main.tex:303` uses $\xi=\hbar/(m_0c)$; under the adopted branch this becomes
$\hbar/(\sqrt2 m_0c)$. Textual only — SSV-II's numerics are in $\xi$-units
(see the series N-gate report).

# SSV-VII-b — C-gate damage report

Status: **closure-grade** · Gate: **C-GATE PASS with one inherited defect** (#190)

| # | Key | Claim | Verdict |
|---|---|---|---|
| C1 | `Unruh1976` (L301) | accelerating observer sees a thermal phonon bath at the Unruh temperature | **`OK`** |
| C2 | `Jacobson1995` (L349) | requiring the Clausius relation on every local Rindler horizon yields the Einstein equations | **`OK`** — retrieved, gr-qc/9504004, *Thermodynamics of Spacetime: The Einstein Equation of State*; "local Rindler horizon" and the Clausius argument confirmed present |
| C3 | `Bjerknes1906` (L202) | attractive Bjerknes acoustic force between oscillating density perturbations | **`OK`** as a citation; **falsified as a mechanism** — see D1 |

## D1 — inherited: same falsified Bjerknes mechanism

L202 states that two oscillating density perturbations *"experience an
attractive Bjerknes acoustic force"* and builds on it. Per #119 the
mutual-radiation Bjerknes force is falsified: the radiation-zone cross-term
oscillates in sign with separation and vanishes for unequal frequencies.

Third paper in the series to present it without the falsification (after SSV-I
L1245 and SSV-IV L565). SSV-II is the only one that flags it.

## Credit where due — the sign

`main.tex:144` uses $\Phi=+b\ln(\rho/\rho_0)$, the sign required for
$\Phi\approx-GM/r$, which is **opposite to SSV-I as printed** and **agrees with
the corrected D1 branch**. SSV-VII-b was right and SSV-I was wrong. No change
needed here.

The $\sqrt2$ in $\xi=\hbar/(\sqrt2 m_0c)$ still propagates into the
horizon-area/entropy counting at L315 and L362 — an E-gate item, not a citation
one.

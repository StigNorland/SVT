# Issue #182 — series-wide audit: final decision

Status: **complete** · 2026-07-27

Twelve papers audited through three gates (C: citations verified against
retrieved primary sources; E: equations re-derived; N: numbers re-run).

## Headline

**The computations were sound. The write-up was not.**

Every substantive defect found is in printed prose, in a citation, or in an
algebraic step in the text. **Not one defect was found in the numerical corpus.**
The solvers have always implemented the corrected potential; the papers printed
the wrong sign for it.

That pattern repeated four times, independently:

| # | the code / record said | the prose said |
|---|---|---|
| 1 | solvers use $+b(\rho\ln\rho-\rho+1)$ — stable branch | SSV-I `eq:pot` prints the unstable sign |
| 2 | trefoil extractor: "a single continuous closed curve **with no Y-junctions**" | SSV-I:618 "a Y-junction of three quantized vortex filaments" |
| 3 | SSV-VII-b uses $\Phi=+b\ln(\rho/\rho_0)$ — the correct sign | SSV-I prints the opposite |
| 4 | `issue-119` note headlines "Phase 1 (mutual mechanism) **FALSIFIED**" | SSV-I, SSV-IV and SSV-VII-b all present it as the gravity mechanism |

## Root cause

A single misreading, in SSV-I `main.tex:205`: Zloshchastiev's
$F(\rho)=b\ln(\rho/\bar\rho)$ — a nonlinear **chemical-potential** term — was
read as a **pressure**, and attributed to Volovik, who has no logarithmic
equation of state at all ("equation of state" occurs **0 times** in 71,425 words
of Phys. Rept. **351**, 195).

Because the equation was credited to a source that does not contain it, the real
source's constraint $\rho|F'(\rho)|=mc_0^2/\hbar$ — an **absolute value**, silent
on stability — was never applied. Since $c_s^2=\rho\mu'(\rho)/m$ for a chemical
potential but $P'(\rho)/m$ for a pressure, that one substitution produced the
wrong sign, a spurious factor 2, and a fabricated
thermodynamic-vs-Bogoliubov discrepancy complete with a fabricated resolution.

The sibling Zloshchastiev paper shows the confusion was *invited*: it gives
$c_s\propto\sqrt{p'(\rho)}$ while never writing $p(\rho)$ anywhere, with
$F(\rho)$ a few lines above. That explains the error without excusing it.

## Gate results

| Paper | C | E | N |
|---|---|---|---|
| SSV-I (#183) | **FAIL** | **FAIL** (D1,D2,E1,E3,E4,E5) | PASS |
| SSV-II (#184) | **FAIL** | **FAIL** (`eq:maxwell`, AB sector) | PASS |
| SSV-III (#185) | PASS | PASS | PASS |
| SSV-IV (#186) | PASS | **FAIL** (inherited) | PASS |
| SSV-V (#187) | PASS | **FAIL** (Argument 1 inverts) | PASS |
| SSV-VI (#188) | PASS | PASS | PASS |
| SSV-VII-a (#189) | PASS | **FAIL** (Gausson + circular $\hbar/2$) | n/a |
| SSV-VII-b (#190) | PASS | PASS (2 inherited) | PASS* |
| SSV-VIII (#191) | PASS (hygiene) | n/a | n/a |
| SSV-IX (#192) | PASS (hygiene) | n/a | n/a |
| SSV-Alpha (#193) | PASS (hygiene) | n/a | n/a |
| SSV-Goldstone (#194) | PASS (superseded) | n/a | n/a |

\* one paper-side recomputation owed: horizon counting at `main.tex:315,362`.

## Substantive defects, ranked

1. **D1 — the logarithmic sign** (SSV-I, propagating to II, III, V). Resolved:
   author adopted the stable-vacuum branch. Repairs #180 at P0/P1/P3.
2. **SSV-V Argument 1 inverts.** Its stable-Planck-remnant argument needs
   $\mu\to+\infty$ as $\rho\to0$; the adopted branch gives $\mu\to-\infty$. Not a
   weakening — a sign reversal. Must be withdrawn or replaced.
3. **E5 — $\rho_0$ too large by $2.7\times10^4$.** Three mutually inconsistent
   statements; route 1 adopted, $\rho_0=\alpha m_e^4c^3/(2\pi^2\Lambda\hbar^3)$.
4. **E4 — $\xi/\alpha$ is the Bohr radius**, not the classical electron radius
   ($\alpha^2$ out). The paper advertises recovering one known constant and
   recovers a different one.
5. **SSV-II `eq:maxwell` is unsupported** and contradicted by the paper's own
   #138 result and by #180 P4.
5b. **SSV-II's Aharonov–Bohm derivation fails** (added 2026-07-27, once the
   paywalled Haldane–Wu was settled by proxy). Haldane–Wu counts enclosed
   *atoms*, not circulation quanta, and is extensive where an AB phase must be
   topological — so no prefactor can repair it. Independently, `eq:AB_SSV` needs
   the symbol $e$ to be a mass while using it as a charge, which makes step
   $(\star)$ circular, and `eq:flux_quantisation` is dimensionally inconsistent
   by $\mathsf{L^{-2}T^{-1}}$. The qualitative claim ($\mathbf A=\mathbf v_s$ is a
   physical flow) survives and re-cites to Volovik §XII A; the quantised
   $2\pi n$ does not.
6. **SSV-VII-a's $\hbar/2$ is imported, not derived** — circular on either branch.
7. **E3 — spurious $\alpha^2$** in `eq:Etotal`: as printed the functional
   stationarises at $r^*=0.57$, not $1/\alpha$. Presentation-fatal, physics intact.
8. **Falsification suppression** — the #119-falsified Bjerknes mechanism is
   presented as current in three papers.

## What survives

- The **proton mass chain** $m_pc^2=N_YF\mu_0$: untouched. $N_Y=3$ is the trefoil
  crossing number, a genuine knot invariant, and the computations always used the
  single-curve knot.
- **$R^*_e=\xi/\alpha$** as a relation (only its *name* was wrong).
- **SSV-III** entirely — the healthiest paper in the series; it cites sources for
  *setting* rather than for results they do not contain.
- **SSV-VI** entirely — rests on data, not on the LogSE.
- The **whole numerical corpus**.

## Convergence worth keeping

Two independent no-gos now point at the same repair. #178 found bare SSV has no
fermionic solitons ($\pi_3(S^1)=0$); the D2 audit found a symmetric Y-junction is
forbidden by quantized circulation in a one-component condensate. Same root
cause, same indicated fix: **multi-component structure is not a patch, it is the
missing content.**

## Durable fix

`papers/cited/` now holds every retrieved source, hash-pinned and re-fetchable via
`instruments/tools/fetch_cited.py`. The **evidence rule** — no verdict without a
verbatim quotation, enforced by `missing_evidence()` — means no future reader has
to re-download anything to check a verdict, and no load-bearing citation can go
unchecked again. That rule caught two of my own errors during this audit.

## Remaining open

- `zloshchastiev2023` (*Universe* **9**, 234) — publisher blocks retrieval;
  `MISATTRIBUTED` expected but not verdicted.
- ~~`HaldaneWu1985`~~ — **closed 2026-07-27.** Settled `MISREAD` without
  obtaining the paywalled PRL, via an open-access secondary source that quotes,
  re-derives and numerically verifies it (`notes/polkinghorne2021.md`). The
  method generalises: for a pre-arXiv result, find a modern open-access paper
  that *reproduces* it rather than one that merely cites it.
- Pre-arXiv/book sources still open: `Landau_Fluid`, `Vinen2002`, `linshu1964`
  and others. None is presently known to be load-bearing.
- `Villois2017` and `Clisby2010` were deliberately **not** downloaded after title
  verification showed the search had returned different papers.

## Next phase — not part of #182

Rewriting the papers. Every defect above is textual, so this is an editing pass,
not a research pass. It should be one pass per paper, and the D1 sign, the E5
$\rho_0$ and the E4 label all touch the same passages in SSV-I — they must be
applied together, not sequentially.

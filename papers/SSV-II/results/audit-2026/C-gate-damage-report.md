# SSV-II — C-gate (citation) damage report

Status: **closure-grade** for the verified keys

Gate: **C-GATE FAIL**

Audit date 2026-07-27, under \#184 (child of \#182). Verdict vocabulary and the
evidence rule are defined in `papers/cited/INDEX.md`.

## Ledger — Tier A (load-bearing)

| # | Key | Where | Claim in SSV-II | Verdict |
|---|---|---|---|---|
| C1 | `Volovik`,`Barcelo` | **508** | "the linearised Madelung equations around a single chiral vortex background reduce … to the **vacuum Maxwell equations**" | **`MISATTRIBUTED`** (see D1) |
| C2 | `Schwinger` | 585 | Schwinger term $g-2=\alpha/\pi$ | **`OK`** — standard: $a_e=(g-2)/2=\alpha/2\pi\Rightarrow g-2=\alpha/\pi$ |
| C3 | `AharonovBohm1959` | 785 | AB effect: phase shift on a path with $\mathbf B=0$ | **`OK`** — the paper's subject |
| C4 | `HaldaneWu1985` | 832 | "a vortex transported around a closed path accumulates a Berry phase **proportional to the number of circulation quanta it encloses**" | `PENDING-PRIMARY` — **flagged**, see D3 |
| C5 | `Villois` | 1091 | vortex reconnection when filaments approach within a core radius | `PENDING-PRIMARY` — arXiv resolution ambiguous (see below) |
| C6 | `Bjerknes1906` | 2384 | time-averaged force between two bodies pulsating in a compressible medium | **`OK`** as a citation — but see D2 |
| C7 | `Landau_Fluid` §74 | 2419 | pressure field of a pulsating sphere | `PENDING-PRIMARY` — book |

`Villois` and `Villois2017` are **duplicate keys** for the same paper (Villois,
Proment & Krstulovic, *Universal and nonuniversal aspects of vortex
reconnections in superfluids*), used in SSV-II and SSV-III respectively.
Bibliography hygiene, no correctness impact.

## D1 — the Maxwell claim is unsupported, and conflicts with SSV-II's own \#138 result

`main.tex:508` asserts that linearised Madelung reduces to **vacuum Maxwell
equations**, citing `Volovik` and `Barcelo`.

**Barceló, Liberati & Visser do not say this.** Their Theorem 1 (gr-qc/0505065
p.13, quoted verbatim in `papers/cited/notes/barcelo2011.md`) yields

> the d'Alembertian equation of motion for a **minimally-coupled massless
> scalar field** propagating in a (3+1)-dimensional Lorentzian geometry

— a **scalar**, not a vector field. Of the four occurrences of "Maxwell" in the
99,381-word review, none concerns acoustic perturbations of a condensate: they
are the history of analogue models, a *dielectric* analogue, macroscopic Maxwell
inside a dielectric, and conformal invariance. Volovik's ³He-A does support
emergent gauge fields, but from the **multi-component** $\hat l$-vector order
parameter, not from Madelung of a one-component condensate.

**SSV-II already knows this.** Two paragraphs below, the paper states:

> the \#138 linearization has since computed the actual spectrum: the
> second-order transverse wave equation below does **not** arise from the LogSE
> + chiral-shear + CP¹ functional around the uniform vacuum — the chiral term is
> **silent at linear order** …

So `eq:maxwell` is presented **without caveat** at 508, while the paper's own
computation two paragraphs later says the mechanism that would produce it does
not exist at linear order. This also reproduces \#180's P4 finding: *one scalar
Goldstone does not furnish two transverse photon helicities* (S route FAIL).

**Consequence:** `eq:maxwell` must either carry the \#138 caveat at the point of
statement, or be moved into the historical-record subsection with the rest of
the provisional identification. The citations to `Barcelo` (and to `Volovik` for
a one-component Madelung system) must be withdrawn.

## D2 — SSV-I states as current a mechanism SSV-II records as falsified

**This is a cross-paper defect and its locus is SSV-I.**

SSV-II is honest about its own status. `main.tex:92`:

> **Falsified as written (issue \#119, 2026-06):** The gravity section's
> mutual-radiation Bjerknes mechanism — pulsating breathers gravitating through
> the time-averaged interference of the waves they radiate at one another — is
> **falsified by pre-registered computation**: the radiation-zone cross-term
> oscillates in sign with separation … and it vanishes between breathers of
> unequal [frequency]

and `main.tex:227` repeats it in the claim-status list ("Falsified as written;
retained as record").

But **SSV-I `main.tex:1245`** says, with no caveat whatsoever:

> Gravity is the acoustic Bjerknes force — mutual attraction between vibrating
> breathers via secondary flow fields in the plenum — **derived in Paper II and
> shown there to reproduce Newtonian gravity** with $G$ expressed in terms of
> $\hbar$, $c$, $m_e$, and $\alpha$

SSV-I presents as an established result what SSV-II records as **falsified by
pre-registered computation**. Under standing rule 1 this is the one failure mode
the programme most needs to avoid: a negative result that is explicit in one
paper and invisible in another.

This compounds SSV-I's `C11`, whose `zloshchastiev2023` citation is attached to
the same sentence and is independently expected `MISATTRIBUTED`
(`papers/cited/notes/zloshchastiev2023_pramana_rotcurves.md`).

**Action:** SSV-I:1245 must carry the \#119 falsification, or be rewritten. Filed
back to \#183.

## D3 — Haldane–Wu: phase proportional to *what*?

SSV-II says the Berry phase is *"proportional to the number of **circulation
quanta** it encloses"*. The standard Haldane–Wu result is that a vortex
transported around a closed loop in a 2D superfluid acquires a Berry phase
proportional to the **number of particles enclosed** by the loop (the
Magnus/Berry phase, $2\pi\times$ enclosed particle number) — a different
quantity, and the one that carries the superfluid density.

Not verdicted: PRL 54, 1985 is pre-arXiv and was not obtained. Flagged as the
highest-value remaining check in this paper, because the AB-effect
identification in §"The Aharonov–Bohm Effect as Mechanical Berry Phase" rests
on which quantity the phase counts.

## Retrieval notes

`Villois` could not be pinned: an arXiv title search returned *A Vortex Filament
Tracking Method for the Gross-Pitaevskii Model* (1604.03595), which is a
**different paper** from the cited *Universal and nonuniversal aspects of vortex
reconnections in superfluids*. Not downloaded rather than downloaded wrongly.

`Clisby2010` (cited by SSV-III) was similarly mis-resolved during bulk fetch —
the retrieved file is the J. Stat. Phys. companion, not the cited PRL 104,
055702. It is stored as `Clisby2010_pivot_implementation_SIBLING.pdf` so it
cannot masquerade as the cited work.

## Gate decision

**C-GATE FAIL.** One `MISATTRIBUTED` with a live conflict against the paper's own
computation (D1); one cross-paper falsification-suppression defect whose locus
is SSV-I (D2); one flagged claim awaiting a pre-arXiv source (D3); three `OK`;
three `PENDING-PRIMARY`.

E-gate for SSV-II opens for claims not depending on C4, C5, C7.

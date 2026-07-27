# polkinghorne2021 — evidence

R. E. S. Polkinghorne, A. J. Groszek and T. P. Simula,
*Geometric phases of a vortex in a superfluid*,
Phys. Rev. A **104**, L041305 (2021) · arXiv:2101.07438 · sha256 `bb9eb1c160557019`

**Role in the audit:** open-access **secondary source** admitted to settle
`HaldaneWu1985` (Phys. Rev. Lett. **55**, 2887), which is pre-arXiv and paywalled.
It is a suitable proxy because it (i) quotes the Haldane–Wu result in the
abstract, (ii) re-derives it, and (iii) *verifies it numerically* — so it is not
merely repeating a claim second-hand.

Used for: **SSV-II C4 / D3** — does the vortex Berry phase count *particles* or
*circulation quanta*?

---

## Q1. What quantity does the Haldane–Wu Berry phase count?

**Abstract** (p. 1):

> We consider geometric phases of mobile quantum vortices in superfluid
> Bose–Einstein condensates. Haldane and Wu [Phys. Rev. Lett. 55, 2887 (1985)]
> showed that the geometric phase, $\gamma_C = 2\pi N_C$, of such a vortex is
> determined by the **number of condensate atoms $N_C$ enclosed by the vortex
> trajectory**.

**Introduction** (p. 1):

> Soon after Berry's seminal result [3], Haldane and Wu [14] considered a quantum
> vortex being adiabatically transported along a closed path $C$ in a
> two-dimensional superfluid and conjectured that as a consequence the system
> acquires a geometric phase $\gamma_C = 2\pi N_C$, where $N_C$ is the **number of
> atoms enclosed by the path of the vortex**.

**Derivation** (p. 2, Eq. S1):

> When the vortex phase singularity $R$ is transported along a closed path $C$
> that encircles $N_C$ **atoms** of the superfluid, the geometric phase
> $$\gamma_C = i\oint\langle n;R|\nabla_R|n;R\rangle\,dR = 2\pi N_C$$

**Numerical confirmation** (p. 8):

> Our numerical results have verified that the prediction by Haldane and Wu,
> under the assumptions made in [14], is correct.

**Citation as given** (ref. [14], p. 9):

> [14] F. D. M. Haldane and Y.-S. Wu, Phys. Rev. Lett. **55**, 2887 (1985).

— which matches SSV-II's bibitem exactly (`main.tex:3276–3279`). The bibliographic
entry is `OK`; only the *content* attributed to it is not.

## Q2. Verdict

**`MISREAD`.** SSV-II `main.tex:832–834` states the phase is

> proportional to the number of **circulation quanta** it encloses.

Haldane–Wu give **enclosed particle number**. These are not the same quantity and
not even the same *kind* of quantity:

| | Haldane–Wu $\gamma_C = 2\pi N_C$ | what SSV-II needs |
|---|---|---|
| counts | condensate atoms | circulation/flux quanta $n$ |
| scales with | enclosed **area × density** | nothing — depends only on $n$ |
| under deformation of $C$ at fixed enclosed defect | **changes** | invariant |
| character | extensive, non-topological | topological |

The Haldane–Wu phase grows without bound as the loop is enlarged in a uniform
condensate. An Aharonov–Bohm phase must not. So Haldane–Wu cannot supply the
loop-independent $\gamma_{\rm AB} = 2\pi n$ that SSV-II
`eq:AB_SSV` asserts, and the phrase "This is precisely the Haldane-Wu mechanism"
is false as written.

Two independent notes in this paper make the same point from the other side: the
Haldane–Wu phase is exactly the one whose *boundary* subtleties the paper spends
its length resolving, because in a finite condensate it is **not** determined by
the enclosed defect alone (p. 8):

> the way those assumptions apply to the boundary conditions of a realistic
> superfluid order parameter is quite subtle, and is obscured by the common but
> unphysical assumption of an infinite condensate of uniform density.

## Q3. Is there a literature result of the form SSV-II wants?

Yes, and **SSV-II already cites the source for other purposes** — see
`volovik2001.md` §XII A. It is the *acoustic/gravitational* Aharonov–Bohm effect,
not the Haldane–Wu vortex Berry phase. But it does **not** deliver a universal
$2\pi n$ either: the mapping replaces the electric charge by the quasiparticle's
$E/c^2$, so the analogue AB phase is **energy-dependent**. Detail in the SSV-II
E-gate report, `E3`.

## Retrieval

    curl -L https://arxiv.org/pdf/2101.07438 -o polkinghorne2021.pdf

Not tracked by git (public repo; arXiv licence). Hash pinned in
`instruments/tools/fetch_cited.py`.

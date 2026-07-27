# SSV-IV — C-gate damage report

Status: **closure-grade** · Gate: **C-GATE PASS with one inherited defect** (#186)

| # | Key | Claim | Verdict |
|---|---|---|---|
| C1 | `Volovik`,`Barcelo` (L1046) | "The curved-spacetime formulation of gravity emerges from the Madelung equations in the hydrodynamic limit … The acoustic metric" | **`OK`** |
| C2 | `Bjerknes1906` (L565) | time-averaged force between pulsating bodies | **`OK`** as a citation; see D1 |

## C1 is correct — and instructive by contrast with SSV-II

SSV-IV claims only an **acoustic metric** for a scalar mode. That is exactly
Barceló–Liberati–Visser Theorem 1 (`papers/cited/notes/barcelo2011.md`), which
gives a minimally-coupled massless **scalar** in a Lorentzian acoustic metric.

Compare SSV-II:508, which cites the *same two sources* for the **vacuum Maxwell
equations** — a vector theory the sources do not support (SSV-II D1). SSV-IV
uses the citation correctly; SSV-II over-reaches it. The two papers cite the same
pair for different strength claims, and only one is supported.

## D1 — inherited: the Bjerknes mechanism is falsified

SSV-IV L565 presents the Bjerknes time-averaged force as the gravity mechanism.
That mechanism is **falsified by pre-registered computation** (#119), as SSV-II
records at its `main.tex:92`, and as SSV-IV's own result note
`results/issue-119-falsification-and-bath-candidate.md` states in its headline:
*"Phase 1 (mutual mechanism) FALSIFIED"*.

The result note is exemplary — it separates the falsified *force* from the
surviving *time-dilation field* and records that the literal SSV-IV potential is
a box artefact. **The main text must carry that status at the point of use.**
Same defect class as SSV-I D2, but here the honest record already exists
in-repo; it simply has not reached the prose.

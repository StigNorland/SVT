# Working rules for the SSV repository

This is the Saturated Superfluid Vacuum (SSV) theoretical-physics programme:
a multi-paper series (`papers/SSV-*`) with supporting computation (`instruments/`,
with tests under `instruments/test/<paper>/`; env setup via `instruments/setup_env.{sh,ps1}`) and
result notes (`papers/*/results/`). Work is organised around GitHub issues
(StigNorland/SVT). Background and current status live in the auto-memory
(`MEMORY.md` and the `project-*` notes).

## Standing rules (from the user)

1. **Only (correctly) negative results are proof; positive results are merely
   suggestive.** Negative results are important — flag them explicitly, never
   bury or soften them. Do not pressure findings toward the positive.
2. **Plan before executing a multi-step task.** Produce a detailed,
   pre-registered plan (and post it where relevant) before doing the work.
3. **Move and rename successfully compiled PDFs into `papers/pdf/`** (the
   human-readable names, e.g. `SSV I.pdf`). Keep the tracked PDFs in step with
   their `.tex` source.
4. **One feature branch at a time.** Before creating a new branch, make sure the
   previous branch has completed its pull-request workflow (merged) and delete
   it (local and remote).

## Additional conventions (proposed by Claude — under review)

5. **Claim-status discipline.** Track every quantitative claim as *derived*
   (e.g. topological), *coincidence*, or *falsified*. When a claim's status
   changes, update the paper's claim-status table, the relevant prose, and the
   auto-memory in the same pass. (Extends rule 1.)
6. **Issue-driven, pre-registered workflow.** Pre-register the hypothesis and the
   decision rule in the issue *before* computing; post the result as a comment;
   close the issue with links to the commits. (Extends rule 2.)
7. **Back analytic claims with a tested computation** where feasible — a script
   in `instruments/` plus a `pytest` test under `instruments/test/<paper>/` plus
   a result note in `papers/*/results/`.
8. **LaTeX hygiene.** Escape `#` as `\#` in prose (a raw `#` is a macro-parameter
   character and breaks the build). Before committing a paper, confirm a clean
   2-pass `pdflatex` build: 0 errors and no *new* undefined references. Then
   apply rule 3.
9. **Git/PR.** Feature branch per issue → PR → merge to `main`; do not push to
   `main` directly. Commit messages end with the `Co-Authored-By` trailer.
10. **Don't reintroduce retired framing.** Some concepts have been demoted (e.g.
    the "α-harmonic mass ladder" is a numerical coincidence, not a derived
    spectrum; the muon/tau as derived breather modes are closed no-gos). Check
    the auto-memory before reusing old terminology.
11. **Provenance is generated, not hand-written.** Every paper's "Code and Issue
    References" appendix is produced by `instruments/tools/gen_provenance.py` (it pins
    each `\#NN` issue to its URL and each `\texttt{instruments/...py}` script and
    result-note report to a GitHub permalink at the commit that last modified it;
    in-text `\#NN` is rewritten to `\ssvissue{NN}`, and inline script/report
    refs to `\ssvfile{stem}` — both hyperlink to their appendix entry; the
    generator resolves a bare `stem` to its repo file by glob). Regenerate before building a
    paper: `python instruments/tools/gen_provenance.py <PAPER>` (or `--all`); the result
    is `papers/<PAPER>/provenance.tex`, `\input` in an appendix. The test
    `instruments/test/tools/test_gen_provenance.py` enforces that every cited script path
    exists, so a reference can never silently break.
12. **The evidence rule: no verdict without a verbatim quotation.** *(User's
    idea, 2026-07-27: "we could include the paragraph we cite?" — adopted as a
    rule after it caught two of Claude's own errors during the \#182 audit.)*
    Every load-bearing citation must be checked against the retrieved primary
    source, and the **paragraph actually relied on** stored verbatim in
    `papers/cited/notes/<key>.md` — not a paraphrase, not a page number. Give
    each note the claim being made, the quotation, and a verdict from the fixed
    vocabulary: `OK` / `MISATTRIBUTED` / `MISREAD` / `MISDERIVED` /
    `UNSUPPORTED` / `PENDING-PRIMARY` / `UNCITED`. Sources are hash-pinned and
    re-fetchable via `instruments/tools/fetch_cited.py`; `missing_evidence()`
    must stay empty, so a verdict can never exist without its evidence. The
    retrieved PDFs are **gitignored** — this repo is public and arXiv's licence
    does not permit redistribution — so the notes are what make a verdict
    checkable without re-downloading anything.
    - **Paywalls are never circumvented.** A source that cannot be obtained is
      recorded `PENDING-PRIMARY` and every dependent claim stays flagged.
    - **Proxies are allowed when they do more than cite.** A secondary source is
      admissible if it quotes the result and preferably re-derives or
      independently verifies it; look for a modern open-access paper that
      *reproduces* the old one. Record the verdict against the *original* key
      and name the proxy (e.g. `HaldaneWu1985` → `polkinghorne2021`).
    - **Pin identifiers, not titles.** Papers are often retitled on publication,
      so a title check produces false negatives as well as the false positives
      it exists to catch. Pin the arXiv ID, then verify author list and content.
    - **Never read equations off degraded OCR.**
    *Why:* the defect that triggered \#182 survived for years because an
    equation was credited to a source that does not contain it, so the real
    source's constraint was never applied. A quotation makes that
    unsustainable. (Extends rule 1.)
13. **State the search behind an absence claim.** "X does not appear" and "there
    are no others" are only as strong as the query that backs them, so give the
    pattern, the corpus and the count. *"`equation of state` occurs 0 times in
    71,425 words"* is re-runnable and falsifiable; *"no others"* has to be
    trusted. Where practical, widen the query until it over-matches and inspect
    the excess, rather than trusting the query that returned the expected
    answer. (Extends rules 1 and 6; see \#198 Part C.)

# Working rules for the SSV repository

This is the Saturated Superfluid Vacuum (SSV) theoretical-physics programme:
a multi-paper series (`papers/SSV-*`) with supporting computation (`src/`) and
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
   in `src/` plus a `pytest` test plus a result note in `papers/*/results/`.
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

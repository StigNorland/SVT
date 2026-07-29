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
   `pdflatex → BibTeX → pdflatex → pdflatex` build: 0 errors and no undefined
   references or citations. Then apply rule 3.
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
12. **The evidence rule: paragraph evidence by default; every exception is
    explicit.** *(User's
    idea, 2026-07-27: "we could include the paragraph we cite?" — adopted as a
    rule after it caught two of Claude's own errors during the \#182 audit.)*
    Every load-bearing citation must be checked against the retrieved primary
    source, and the **paragraph actually relied on** stored verbatim in the
    quote directory `papers/cited/notes/<key>.md` — not a paraphrase and not
    merely a page number. Each evidence record identifies the exact SSV
    sentence/equation being checked, gives a page/section/equation locator,
    quotes the complete source paragraph (including assumptions and
    qualifications), and explains whether SSV uses it correctly with a verdict
    from the fixed vocabulary: `OK` / `MISATTRIBUTED` / `MISREAD` /
    `MISDERIVED` / `UNSUPPORTED` / `PENDING-PRIMARY`.

    Sources are hash-pinned and re-fetchable via
    `instruments/tools/fetch_cited.py`. The retrieved PDFs are **gitignored** —
    this repo is public and arXiv's licence does not permit redistribution — so
    the notes are what make a verdict checkable without re-downloading anything.
    The canonical status and identifier registry is
    `papers/cited/verification.json`. Every entry has a source URL, access
    status, verification status and paragraph requirement. A DOI is mandatory
    when the work has one; every arXiv work records its arXiv ID; explicit
    checked statuses replace blank identifiers when neither is available.
    `instruments/tools/citation_evidence.py` validates the registry and tracked
    evidence on every gated build; `missing_evidence()` must stay empty.
    Every cited work, including SSV self-citations, has a catalog entry and
    `papers/cited/notes/<key>.md`. A note marked `NOT-REVIEWED` is an explicit
    inventory gap, never evidence and never a verdict. Evidence-bearing notes
    form the stricter `sources` subset of `verification.json`.
    Bibliographic identity is canonical in `papers/cited/references.bib`;
    all papers use that one database and BibTeX selects only their cited keys.
    `instruments/tools/bibliography.py` rejects inline bibliographies, undefined
    keys, duplicate/legacy aliases, and quote-registry sources missing from the
    shared database. Every quote note must have a JSON registry entry, and every
    registry entry must have its note.
    - **Owner-supplied or image-only scans require an accessible Markdown
      transcript.** Store audit-relevant pages, in reading order with page
      boundaries and uncertainty markers, under
      `papers/cited/transcripts/<key>.md`; link the evidence note and transcript
      both ways. Never silently repair an unreadable word or equation.
    - **A quote is contextual evidence, not decoration.** Include the complete
      paragraph and any immediately governing paragraph that supplies scope,
      definitions, assumptions or qualifications. Equations include their
      introducing/interpreting prose.
    - **Paywalls are never circumvented.** A source that cannot be obtained may
      omit the primary paragraph only through a reasoned
      `paragraph_exception` in `verification.json`; no missing paragraph passes
      implicitly. The source is recorded `PENDING-PRIMARY` and every unresolved
      dependent claim stays flagged.
    - **Proxies are allowed when they do more than cite.** A secondary source is
      admissible if it quotes the result and preferably re-derives or
      independently verifies it; look for a modern open-access paper that
      *reproduces* the old one. Record the verdict against the *original* key
      and name the proxy (e.g. `HaldaneWu1985` → `polkinghorne2021`).
    - **Pin identifiers, not titles.** Papers are often retitled on publication,
      so a title check produces false negatives as well as the false positives
      it exists to catch. Pin the arXiv ID, then verify author list and content.
    - **Remove uncited bibitems.** They are not granted an `UNCITED` evidence
      waiver; keeping an unused or mismatched source in the bibliography creates
      false provenance.
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
14. **Derived numbers are generated, not typed — and the computation is separate
    from the rendering.** A load-bearing number must not exist twice, once in an
    instrument and once in the `.tex`. Register it in
    `instruments/tools/gen_values.py`. The chain is *(user's design call,
    2026-07-28)*:

        instrument --(--compute)--> results/values_receipt.json --> values.tex --> PDF

    - `gen_values.py --compute <PAPER>` runs the instruments and writes the
      **receipt** — the recorded result of the last run, following the series'
      existing `results/*_receipt.json` convention. Run it when the *physics*
      changes.
    - `gen_values.py <PAPER>` reads the receipt and writes `values.tex`. It
      imports nothing, so **a document build never re-runs the physics** — run it
      before every build, exactly as for provenance.
    - `gen_values.py <PAPER> --check` re-runs the instruments and compares
      against the receipt, so the recorded result is *checkable*, not merely
      trusted.

    The paper `\input`s `values.tex` and prints `\ssvRhoZero` rather than a
    literal (macro namespace `\ssv<CamelCase>`). `test_gen_values.py` tests each
    hop separately; the one that actually prevents re-typing is
    `test_replaced_literal_is_gone`. Cross-paper values are declared in
    `gen_values.SHARED`, computed once into
    `papers/shared_values_receipt.json`, and emitted into every declaring
    paper's `values.tex`; `test_no_shared_literal_survives` and the build gate
    reject every registered old spelling anywhere in `main.tex`, including
    tables. This is declared coverage, not a scanner: an unregistered number is
    still invisible. **The receipt is itself a drift surface** —
    if `test_receipt_matches_instruments` is ever skipped for cost, the guarantee
    weakens from "the paper matches the instrument" to "the paper matches what
    the instrument last said". Say which one you mean. Paper-local receipts
    currently cover SSV-I, SSV-VI and SSV-VII-b; the shared receipt has
    consumers in SSV-Alpha, SSV-I, SSV-II and SSV-IV. Extend opportunistically,
    and do not assume a number is generated because others are. (Extends rule
    11; see \#198 Part A and \#213 Parts B/C.)
15. **Ask what a symbol means throughout, not just whether an equation
    balances, and use established domain-standard notation.** Three of the
    \#182 defects were one error class — a symbol
    carrying two dimensions in one paper (`b` in SSV-I, `e` in SSV-II) or across
    papers undeclared (`b` in SSV-V) — and the C/E/N gates missed all three
    because they checked equations and products, never symbols. Encode a paper's
    symbol table and relations in `instruments/tools/dimensions.py`, splitting
    symbols into *anchored* (dimension fixed by definition) and *free*, and ask
    whether **any** assignment to the free symbols makes the printed relations
    simultaneously homogeneous. Covers SSV-I, SSV-II and SSV-V only. It checks
    the relations *as transcribed*, not the `.tex` — state that limit whenever
    citing it.

    `instruments/tools/conventions.py` supplies the programme-wide complement:
    preserve established subfield notation; where fields conventionally reuse
    a letter, disambiguate by context or subscript; and rename project-specific
    quantities that occupy a reserved spelling. In particular, `\mu_0` means
    vacuum permeability, `m_\star=m_e/\alpha` is the SSV mass scale,
    `E_\star=m_\star c^2` its rest-energy scale, and
    `\bar{\lambda}_p=\hbar/(m_pc)` the reduced proton Compton wavelength.
    The build gate rejects the retired `a_p` and non-permeability `\mu_0`
    spellings. The wider symbol census remains partial: an undeclared symbol is
    not certified merely because these reserved cases pass. (Extends rule 7;
    see \#198 Part B and \#213 Part A.)
16. **Build through the gate, and freeze reviewed conclusions against number
    drift.**
    *(User's instruction, 2026-07-28: "we need to record our failure mode and
    test at every compile.")* Compile with
    `python instruments/tools/build_paper.py <PAPER>` (or `--all`, or
    `--gate-only`), which runs rules 12, 11, 14 and 8 and rule 3 in order — and,
    before `pdflatex`, checks that citation evidence is structurally complete
    and every registered numerical relationship still holds.

    Rule 14 stops a number drifting from its instrument. It does not stop the
    number *moving legitimately* after an intentional recomputation and leaving
    a previously reviewed result false. Each registered relationship therefore
    records a stable LaTeX anchor, the generated macros it depends on, a
    predicate, and a tolerance. If the statement changes or its predicate stops
    holding after the inputs move, the paper **does not compile**.

    This is a **drift guard, not a semantic referee**. It cannot establish that a
    conclusion was supported when the author or model first wrote it; that must
    be checked during review. A predicate that ignores its inputs also guards
    nothing, so `test_claims_are_not_tautologies` perturbs them and requires the
    predicate to notice. Every claim must state its tolerance — "approximately"
    cannot be falsified.

    **Future improvement:** when a +2-agent harness is available, send every new
    or materially changed conclusion and its predicate to independent "third
    eye" review before registration. The build gate then preserves that reviewed
    relationship; it does not substitute for the review.

    **The failure-mode register is `docs/failure-modes.md`.** Every entry is a
    mode observed in this repository, with its guard and what the guard does not
    cover. When a new failure mode is found, add it there in the same pass —
    including when the guard is embarrassing. (See \#198 Part D.)

17. **A paper states its current status; it does not narrate its own edit
    history.** *(User's instruction, 2026-07-29: "we keep a change record in the
    papers themselves, we need to stop that — it increases the size of each
    paper and doesn't add comprehension and clarity.")* Every paper has
    `papers/<PAPER>/CHANGELOG.md`; corrections, withdrawals and re-framings go
    there, linked once from the generated provenance appendix, and never into
    the prose.

    The line is **tense, not topic**:
    - *"the $\hbar/2$ prefactor is imported, not derived"* — status. **Stays.**
    - *"this replaces the result this section originally claimed"* — history.
      **Moves.**

    **Rule 1 outranks this rule.** A falsification stated in the present tense
    is not a change record. The deny-list in
    `build_paper.py::CHANGE_RECORD_PHRASES` therefore contains no verdict word —
    not `withdrawn`, `falsified`, `retracted` or `rejected` — and
    `test_present_tense_verdicts_are_never_banned` keeps it that way. Removing a
    change record must leave a present-tense statement of the same finding
    behind; if a passage has no such residue, report it rather than treating the
    rule as licence to delete a negative result. Removed text is reproduced
    verbatim in the changelog, so the migration relocates and never destroys.

    A claim guard whose statement moves to the changelog **moves with it** —
    `claims.py` anchors to whatever file `site` names, so the guarantee follows
    the sentence instead of being dropped (see `rho0-smaller-by-2e4`).

    The gate catches *phrasing*, not intent: history written in fresh words will
    pass. Drift guard, not referee. (Extends rules 1 and 5; see \#207, FM15.)

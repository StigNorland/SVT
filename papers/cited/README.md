# Shared citation infrastructure

The SSV series has three citation layers with different jobs:

1. `references.bib` is the canonical bibliographic database. Every paper uses
   the same keys and BibTeX selects only the works cited by that paper.
2. `verification.json` is the local citation-note and evidence registry. Its
   catalog covers every cited work; its evidence subset records URLs, DOI and
   arXiv status, evidence mode, verdict, and any explicit paragraph exception.
3. `notes/<key>.md` exists for every cited work. Notes visibly distinguish
   `NOT-REVIEWED`, `LOCAL-SOURCE`, and evidence-recorded states. Image-only
   evidence additionally has an accessible `transcripts/<key>.md`.

The invariants are enforced by `instruments/tools/bibliography.py` and
`instruments/tools/citation_evidence.py`:

- no inline `thebibliography` blocks;
- every cited key exists in `references.bib`;
- legacy aliases cannot return;
- every citation-note and evidence source exists in `references.bib`;
- every cited work has a catalog entry and note;
- every note has a registry entry and every registry entry has its note;
- paragraph evidence is required unless the registry contains a validated,
reasoned exception.

`NOTES.md` is the generated navigation and coverage index.

Each paper ends with:

```tex
\bibliographystyle{unsrt}
\bibliography{../cited/references}
```

Build through `python instruments/tools/build_paper.py <PAPER>`, which runs
`pdflatex`, BibTeX, and the two resolving `pdflatex` passes.

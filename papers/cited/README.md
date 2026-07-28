# Shared citation infrastructure

The SSV series has three citation layers with different jobs:

1. `references.bib` is the canonical bibliographic database. Every paper uses
   the same keys and BibTeX selects only the works cited by that paper.
2. `verification.json` is the local source/access/verification registry. It
   records URLs, DOI and arXiv status, evidence mode, verdict, and any explicit
   paragraph exception.
3. `notes/<key>.md` contains the human-checkable quotation, locator and use
   assessment. Image-only source material additionally has an accessible
   `transcripts/<key>.md`.

The invariants are enforced by `instruments/tools/bibliography.py` and
`instruments/tools/citation_evidence.py`:

- no inline `thebibliography` blocks;
- every cited key exists in `references.bib`;
- legacy aliases cannot return;
- every quote-registry source exists in `references.bib`;
- every quote note has a registry entry and every registry entry has its note;
- paragraph evidence is required unless the registry contains a validated,
  reasoned exception.

Each paper ends with:

```tex
\bibliographystyle{unsrt}
\bibliography{../cited/references}
```

Build through `python instruments/tools/build_paper.py <PAPER>`, which runs
`pdflatex`, BibTeX, and the two resolving `pdflatex` passes.

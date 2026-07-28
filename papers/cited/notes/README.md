# Citation evidence notes

This is the repository's **quote directory**. One file per bibliography key
records enough context to answer two separate questions:

1. Does the cited source really say this?
2. Does the SSV paper use what it says correctly?

A bare quotation answers only the first question. Every load-bearing citation
record must include all of the following:

The canonical machine-readable inventory is
[`../verification.json`](../verification.json). It records the source URL,
DOI/arXiv status, access state, verification verdict, evidence mode and whether
paragraph evidence is required. A note without a registry record is not
registered evidence and fails the citation gate; a registry record without its
note fails as well.

The corresponding bibliographic identity must also exist under the same key in
[`../references.bib`](../references.bib). The `.bib` file controls what papers
print; the JSON file controls what the audit knows about source access and
verification.

## Required record

```markdown
# <bibkey> — citation evidence

## Claim being checked

**SSV site:** `papers/SSV-X/main.tex:<line>`

> The exact SSV sentence or equation that relies on the citation.

## Source and locator

Author, title, stable identifier, pinned SHA-256, page/section/equation.

## Verbatim context

> The complete source paragraph containing the relied-on statement, not only
> the convenient sentence. Include the immediately governing paragraph when it
> supplies assumptions, scope, definitions, or qualifications.

## Use assessment

**Verdict: `OK` / `MISATTRIBUTED` / `MISREAD` / `MISDERIVED` /
`UNSUPPORTED` / `PENDING-PRIMARY`.**

Explain what follows from the quotation, what does not, and whether the SSV
sentence preserves the source's assumptions and scope.
```

Use one `## Evidence <n> — ...` subsection for each materially different use of
the same source. Equations must include the paragraph that introduces or
interprets them. Mark omissions as `[…]`; never silently repair wording or
mathematics in a purportedly verbatim block.

## Honest exceptions

- An absence verdict uses a reproducible search record: corpus, patterns and
  counts, followed by the use assessment.
- A paywalled or unobtainable primary may pass the structural gate without a
  primary-source paragraph only when `verification.json` sets
  `paragraph_required` to `false` and supplies an allowed
  `paragraph_exception` with a reason. A proxy
  record must name the primary work, identify the proxy, quote the proxy's full
  relevant paragraph, and explain why the proxy is probative.
- Image-only or owner-supplied scans link to an accessible Markdown
  transcription under `papers/cited/transcripts/`. The evidence note still
  quotes the specific paragraph used.

Every registry record has a stable `source_url`. A DOI is mandatory when the
work has one, and every arXiv work records its arXiv ID. When an identifier does
not exist or could not be found, the corresponding checked status is explicit;
an empty field is not accepted.

Uncited bibliography entries should be removed, not given a paragraph waiver.

These files are evidence, not scratch notes. Background investigation can stay
in a result report; this directory holds the shortest complete verification
record.

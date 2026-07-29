"""Validate the tracked evidence behind citation-use verdicts.

``papers/cited/verification.json`` is the canonical source and status registry.
The Markdown notes contain the human-checkable quotation and interpretation.
This validator checks identifiers, access states, explicit paragraph waivers,
and note structure.  It cannot decide whether an interpretation is
intellectually correct; that remains a review task.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import bibliography
import fetch_cited

ROOT = Path(__file__).resolve().parents[2]
CITED = ROOT / "papers" / "cited"
NOTES = CITED / "notes"
TRANSCRIPTS = CITED / "transcripts"
REGISTRY = CITED / "verification.json"
NOTE_INDEX = CITED / "NOTES.md"

VERDICTS = {
    "OK", "MISATTRIBUTED", "MISREAD", "MISDERIVED", "UNSUPPORTED",
    "PENDING-PRIMARY",
}
EVIDENCE_MODES = {"quotation", "mixed", "search", "proxy", "transcript"}
ACCESS_STATES = {"open", "paywalled", "owner-supplied-scan", "unavailable"}
DOI_STATES = {"present", "none-known"}
ARXIV_STATES = {"present", "none-found", "pre-arxiv", "not-applicable"}
PARAGRAPH_EXCEPTIONS = {
    "paywalled-primary", "unavailable-primary",
    "reproducible-absence-search",
}
NOTE_STATUSES = {"evidence-recorded", "not-reviewed", "local-source"}

# Locally retained files that are deliberately not citation sources.  The
# Liberati file is a false arXiv match discovered during this audit.
LOCAL_AUXILIARY = {
    "Clisby2010_pivot_implementation_SIBLING",
    "liberati2006",
}


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def registered_keys(registry: dict[str, Any] | None = None) -> set[str]:
    data = load_registry() if registry is None else registry
    sources = data.get("sources", {})
    return set(sources) if isinstance(sources, dict) else set()


def citation_note_keys(registry: dict[str, Any] | None = None) -> set[str]:
    data = load_registry() if registry is None else registry
    notes = data.get("citation_notes", {})
    return set(notes) if isinstance(notes, dict) else set()


def retrieval_keys() -> set[str]:
    return {s.key for s in fetch_cited.SOURCES} | {
        s.key for s in fetch_cited.UNAVAILABLE
    }


def _blockquote_word_count(text: str) -> int:
    """Word count of the longest contiguous Markdown quotation block."""
    longest = current = 0
    for line in text.splitlines():
        if line.startswith(">"):
            current += len(re.findall(
                r"\b[\w'-]+\b", line.removeprefix(">").strip()))
            longest = max(longest, current)
        else:
            current = 0
    return longest


def _has_source_locator(text: str) -> bool:
    return bool(re.search(
        r"(?:\bp{1,2}\.\s*\d|\bpage\s+\d|§\s*\w|\bart\.\s*\d|"
        r"\babstract\b|eq(?:uation)?\.?\s*\(?\d)",
        text,
        flags=re.IGNORECASE,
    ))


def _has_reproducible_search(text: str) -> bool:
    corpus = bool(re.search(r"\d[\d,]*\s+words", text, flags=re.IGNORECASE))
    zero = bool(re.search(
        r"(?:\|\s*(?:\*\*)?0(?:\*\*)?\s*\||\b0\s+"
        r"(?:hits?|occurrences?|matches?)\b)",
        text,
        flags=re.IGNORECASE,
    ))
    return corpus and zero


def registry_issues(
    registry: dict[str, Any] | None = None,
    source_keys: set[str] | None = None,
    catalog_keys: set[str] | None = None,
) -> list[str]:
    """Return schema/policy defects in the JSON verification registry."""
    issues: list[str] = []
    data = load_registry() if registry is None else registry
    sources = data.get("sources")
    if data.get("schema_version") != 1:
        issues.append("verification.json: unsupported schema_version")
    policy = data.get("policy", {})
    if policy.get("paragraph_default") != "required":
        issues.append("verification.json: paragraph_default must be required")
    if set(policy.get("allowed_paragraph_exceptions", [])) != PARAGRAPH_EXCEPTIONS:
        issues.append(
            "verification.json: allowed paragraph exceptions do not match validator")
    if not isinstance(sources, dict):
        return issues + ["verification.json: sources must be an object"]

    catalog = data.get("citation_notes")
    if not isinstance(catalog, dict):
        return issues + ["verification.json: citation_notes must be an object"]

    expected_keys = retrieval_keys() if source_keys is None else source_keys
    missing = expected_keys - set(sources)
    extra = set(sources) - expected_keys
    if missing:
        issues.append(f"verification.json missing sources: {sorted(missing)}")
    if extra:
        issues.append(f"verification.json has unregistered sources: {sorted(extra)}")

    if catalog_keys is None:
        expected_catalog = (
            bibliography.series_citation_keys() | set(sources)
            if source_keys is None else set(sources)
        )
    else:
        expected_catalog = catalog_keys
    missing_notes = expected_catalog - set(catalog)
    extra_notes = set(catalog) - expected_catalog
    if missing_notes:
        issues.append(
            f"verification.json missing citation notes: {sorted(missing_notes)}")
    if extra_notes:
        issues.append(
            f"verification.json has uncatalogued citation notes: "
            f"{sorted(extra_notes)}")

    for key, record in sorted(catalog.items()):
        if not isinstance(record, dict):
            issues.append(f"{key}: citation-note record must be an object")
            continue
        if record.get("note") != f"notes/{key}.md":
            issues.append(f"{key}: citation note must be notes/{key}.md")
        status = record.get("review_status")
        if status not in NOTE_STATUSES:
            issues.append(f"{key}: invalid or missing citation-note review status")
        if key in sources and status != "evidence-recorded":
            issues.append(
                f"{key}: evidence source must be marked evidence-recorded")
        if status == "evidence-recorded" and key not in sources:
            issues.append(
                f"{key}: evidence-recorded note has no source-verification record")
        if status == "local-source":
            local = record.get("local_source")
            if not isinstance(local, str) or not (CITED / local).is_file():
                issues.append(f"{key}: local-source note has no valid local_source")
        expected_cited_by = bibliography.cited_by(key)
        if record.get("cited_by") != expected_cited_by:
            issues.append(
                f"{key}: cited_by drift; expected {expected_cited_by}")

    for key, record in sorted(sources.items()):
        if not isinstance(record, dict):
            issues.append(f"{key}: registry record must be an object")
            continue

        source_url = record.get("source_url")
        if not isinstance(source_url, str) or not re.match(r"https?://", source_url):
            issues.append(f"{key}: missing valid source_url")

        identifiers = record.get("identifiers", {})
        doi = identifiers.get("doi")
        doi_status = identifiers.get("doi_status")
        if doi_status not in DOI_STATES:
            issues.append(f"{key}: invalid or missing doi_status")
        if doi_status == "present":
            if not isinstance(doi, str) or not re.fullmatch(
                    r"10\.\d{4,9}/\S+", doi, flags=re.IGNORECASE):
                issues.append(f"{key}: DOI status is present but DOI is invalid")
        elif doi is not None:
            issues.append(f"{key}: DOI must be null when doi_status is not present")

        arxiv = identifiers.get("arxiv")
        arxiv_status = identifiers.get("arxiv_status")
        if arxiv_status not in ARXIV_STATES:
            issues.append(f"{key}: invalid or missing arxiv_status")
        if arxiv_status == "present":
            if not isinstance(arxiv, str) or not re.fullmatch(
                    r"(?:[a-z-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5})"
                    r"(?:v\d+)?",
                    arxiv,
                    flags=re.IGNORECASE):
                issues.append(
                    f"{key}: arXiv status is present but arXiv ID is invalid")
        elif arxiv is not None:
            issues.append(
                f"{key}: arXiv ID must be null when arxiv_status is not present")

        access = record.get("access", {})
        access_status = access.get("status")
        if access_status not in ACCESS_STATES:
            issues.append(f"{key}: invalid or missing access status")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(access.get("checked", ""))):
            issues.append(f"{key}: access check date must be YYYY-MM-DD")

        verification = record.get("verification", {})
        verdict = verification.get("status")
        mode = verification.get("evidence_mode")
        required = verification.get("paragraph_required")
        exception = verification.get("paragraph_exception")
        if verdict not in VERDICTS:
            issues.append(f"{key}: invalid or missing verification status")
        if mode not in EVIDENCE_MODES:
            issues.append(f"{key}: invalid or missing evidence mode")
        if not isinstance(required, bool):
            issues.append(f"{key}: paragraph_required must be boolean")
        elif required:
            if exception is not None:
                issues.append(
                    f"{key}: paragraph exception supplied although paragraph is required")
            if mode not in {"quotation", "mixed", "transcript"}:
                issues.append(
                    f"{key}: paragraph-required record cannot use {mode!r} mode")
            # Mirror of the open-source rule below.  Without this the asymmetry
            # lets an inaccessible source assert the *stronger* evidence state:
            # `paragraph_required` says the complete relied-on paragraph is
            # present, which a source nobody could obtain cannot honour.  Only a
            # transcript (rule 12's owner-supplied-scan route) makes the full
            # text available without retrieval.  Found 2026-07-28: `toomre1981`
            # was registered unavailable + paragraph_required + no waiver while
            # its own note said the chapter "was not openly obtainable".
            if access_status in {"paywalled", "unavailable"} and mode != "transcript":
                issues.append(
                    f"{key}: {access_status} source asserts a complete relied-on "
                    f"paragraph without a waiver or a transcript")
        else:
            if not isinstance(exception, dict):
                issues.append(
                    f"{key}: paragraph waiver requires an explicit exception")
            else:
                kind = exception.get("kind")
                if kind not in PARAGRAPH_EXCEPTIONS:
                    issues.append(f"{key}: invalid paragraph exception {kind!r}")
                if not str(exception.get("reason", "")).strip():
                    issues.append(f"{key}: paragraph exception has no reason")
                if access_status == "open" and kind != "reproducible-absence-search":
                    issues.append(
                        f"{key}: open source cannot waive paragraph as {kind!r}")

        note = verification.get("note")
        if note != f"notes/{key}.md":
            issues.append(f"{key}: note must be notes/{key}.md")
        if mode == "proxy" and not verification.get("proxy"):
            issues.append(f"{key}: proxy mode does not identify its proxy source")
        if mode == "transcript" and not verification.get("transcript"):
            issues.append(f"{key}: transcript mode does not identify a transcript")

    return issues


def evidence_issues(
    registry: dict[str, Any] | None = None,
    source_keys: set[str] | None = None,
    catalog_keys: set[str] | None = None,
) -> list[str]:
    """Return human-readable defects in tracked citation evidence."""
    data = load_registry() if registry is None else registry
    issues = registry_issues(data, source_keys, catalog_keys)
    sources = data.get("sources", {})
    if not isinstance(sources, dict):
        return issues
    catalog = data.get("citation_notes", {})
    if not isinstance(catalog, dict):
        return issues

    note_keys = {
        path.stem for path in NOTES.glob("*.md")
        if path.name != "README.md"
    } if NOTES.is_dir() else set()
    orphan_notes = note_keys - set(catalog)
    if orphan_notes:
        issues.append(
            "citation notes have no verification.json entry: "
            f"{sorted(orphan_notes)}"
        )
    missing_note_files = set(catalog) - note_keys
    if missing_note_files:
        issues.append(
            f"citation-note registry entries have no note file: "
            f"{sorted(missing_note_files)}")

    for key, record in sorted(catalog.items()):
        note = NOTES / f"{key}.md"
        if not note.is_file():
            continue
        text = note.read_text(encoding="utf-8")
        first = text.splitlines()[0] if text.splitlines() else ""
        if key.lower() not in first.lower():
            issues.append(
                f"{key}: first heading does not identify the citation key")
        status = record.get("review_status")
        if status == "not-reviewed":
            if "NOT-REVIEWED" not in text:
                issues.append(
                    f"{key}: unreviewed citation note is not visibly marked")
            if "not quotation evidence" not in text.lower():
                issues.append(
                    f"{key}: unreviewed note lacks evidence disclaimer")
        elif status == "local-source" and "LOCAL-SOURCE" not in text:
            issues.append(f"{key}: local citation note is not visibly marked")

    for key, record in sorted(sources.items()):
        verification = record.get("verification", {})
        note_name = verification.get("note", f"notes/{key}.md")
        note = NOTES / f"{key}.md"
        if not note.is_file():
            issues.append(f"{key}: missing {note_name}")
            continue
        text = note.read_text(encoding="utf-8")
        if key.lower() not in text.splitlines()[0].lower():
            issues.append(f"{key}: first heading does not identify the citation key")
        if "SSV-" not in text:
            issues.append(f"{key}: note does not identify the SSV use being checked")

        expected = verification.get("status")
        if expected and expected not in text:
            issues.append(f"{key}: note does not record use verdict {expected}")

        required = verification.get("paragraph_required")
        mode = verification.get("evidence_mode")
        if required:
            if _blockquote_word_count(text) < 20:
                issues.append(
                    f"{key}: no paragraph-sized verbatim context (minimum 20 words)")
            if not _has_source_locator(text):
                issues.append(
                    f"{key}: quoted context has no page/section/equation locator")

        if mode in {"search", "mixed"} and not _has_reproducible_search(text):
            issues.append(
                f"{key}: absence evidence lacks corpus size and a zero-count search")

        if mode == "proxy":
            proxy = verification.get("proxy")
            if proxy not in sources or not (NOTES / f"{proxy}.md").is_file():
                issues.append(
                    f"{key}: proxy evidence does not resolve to notes/{proxy}.md")

        if mode == "transcript":
            transcript_name = verification.get("transcript")
            transcript = (
                TRANSCRIPTS / Path(transcript_name).name
                if transcript_name else None
            )
            if not transcript or not transcript.is_file():
                issues.append(f"{key}: owner-supplied scan has no Markdown transcript")
            else:
                body = transcript.read_text(encoding="utf-8")
                if _blockquote_word_count(body) < 50:
                    issues.append(f"{key}: transcript contains too little source prose")
                if f"notes/{key}.md" not in body:
                    issues.append(
                        f"{key}: transcript does not link back to its evidence note")
                if transcript_name not in text:
                    issues.append(
                        f"{key}: evidence note does not link to its transcript")

    return issues


def unregistered_local_sources() -> list[str]:
    """Downloaded PDF keys not yet entered in the tracked source registry."""
    pdf_dir = CITED / "pdf"
    if not pdf_dir.is_dir():
        return []
    return sorted(
        p.stem for p in pdf_dir.glob("*.pdf")
        if p.stem not in registered_keys() and p.stem not in LOCAL_AUXILIARY
    )


def render_note_index(registry: dict[str, Any] | None = None) -> str:
    """Render the navigable index of all citation notes."""
    data = load_registry() if registry is None else registry
    catalog = data.get("citation_notes", {})
    counts = {
        status: sum(
            record.get("review_status") == status
            for record in catalog.values()
        )
        for status in NOTE_STATUSES
    }
    lines = [
        "# Citation-note coverage",
        "",
        "Generated from `verification.json` — do not edit by hand.",
        "",
        (
            f"{len(catalog)} notes: "
            f"{counts['evidence-recorded']} evidence-recorded, "
            f"{counts['not-reviewed']} not reviewed, "
            f"{counts['local-source']} local SSV sources."
        ),
        "",
        "`NOT-REVIEWED` is a visible coverage gap, not a verification verdict.",
        "",
        "| key | review status | cited by | note |",
        "|---|---|---|---|",
    ]
    for key, record in sorted(catalog.items(), key=lambda item: item[0].lower()):
        cited_by = ", ".join(record.get("cited_by", [])) or "audit evidence only"
        status = record.get("review_status", "missing")
        lines.append(
            f"| `{key}` | `{status}` | {cited_by} | "
            f"[note](notes/{key}.md) |"
        )
    lines.append("")
    return "\n".join(lines)


def write_note_index(registry: dict[str, Any] | None = None) -> None:
    NOTE_INDEX.write_text(render_note_index(registry), encoding="utf-8")


def report() -> str:
    issues = evidence_issues()
    lines = [
        f"{len(citation_note_keys())} citation notes",
        f"{len(registered_keys())} evidence-recorded sources",
        f"{len(issues)} evidence issue(s)",
    ]
    lines.extend(f"  FAIL {issue}" for issue in issues)
    local = unregistered_local_sources()
    if local:
        lines.append(
            f"{len(local)} downloaded PDF(s) await registration: {', '.join(local)}")
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover
    print(report())
    raise SystemExit(1 if evidence_issues() else 0)

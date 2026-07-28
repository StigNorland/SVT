"""Tests for citation metadata, paragraph evidence, and explicit waivers."""

import copy
import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import citation_evidence as E  # noqa: E402
import fetch_cited as F  # noqa: E402


def one_source(key):
    data = copy.deepcopy(E.load_registry())
    data["sources"] = {key: data["sources"][key]}
    return data


def test_every_registered_source_has_complete_evidence():
    assert E.evidence_issues() == []
    assert F.missing_evidence() == []


def test_json_registry_exactly_covers_retrieval_registry():
    assert E.registered_keys() == E.retrieval_keys()


def test_every_source_has_url_and_checked_identifier_status():
    for record in E.load_registry()["sources"].values():
        assert record["source_url"].startswith(("https://", "http://"))
        ids = record["identifiers"]
        assert ids["doi_status"] in E.DOI_STATES
        assert ids["arxiv_status"] in E.ARXIV_STATES


def test_missing_source_url_is_rejected():
    data = one_source("barcelo2011")
    data["sources"]["barcelo2011"]["source_url"] = ""
    issues = E.registry_issues(data, {"barcelo2011"})
    assert any("missing valid source_url" in issue for issue in issues)


def test_quote_note_without_registry_entry_is_rejected(tmp_path, monkeypatch):
    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "orphan.md").write_text(
        "# orphan — citation evidence\n\nSSV-I main.tex:1\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(E, "NOTES", notes)
    data = one_source("barcelo2011")

    issues = E.evidence_issues(data, {"barcelo2011"})
    assert any(
        "quote notes have no verification.json entry" in issue
        and "orphan" in issue
        for issue in issues
    )


def test_inaccessible_primary_can_explicitly_waive_paragraph():
    data = one_source("HaldaneWu1985")
    assert E.registry_issues(data, {"HaldaneWu1985"}) == []


def test_paragraph_waiver_requires_allowed_kind_and_reason():
    data = one_source("HaldaneWu1985")
    data["sources"]["HaldaneWu1985"]["verification"][
        "paragraph_exception"] = None
    issues = E.registry_issues(data, {"HaldaneWu1985"})
    assert any("requires an explicit exception" in issue for issue in issues)


def test_open_source_cannot_use_inaccessible_source_waiver():
    data = one_source("barcelo2011")
    verification = data["sources"]["barcelo2011"]["verification"]
    verification["paragraph_required"] = False
    verification["paragraph_exception"] = {
        "kind": "unavailable-primary",
        "reason": "Pretend it was unavailable.",
    }
    issues = E.registry_issues(data, {"barcelo2011"})
    assert any("open source cannot waive paragraph" in issue for issue in issues)


def test_present_doi_must_contain_valid_doi():
    data = one_source("barcelo2011")
    data["sources"]["barcelo2011"]["identifiers"]["doi"] = None
    issues = E.registry_issues(data, {"barcelo2011"})
    assert any("DOI status is present but DOI is invalid" in issue
               for issue in issues)


def test_present_arxiv_must_contain_valid_arxiv_id():
    data = one_source("barcelo2011")
    data["sources"]["barcelo2011"]["identifiers"]["arxiv"] = "not-an-id"
    issues = E.registry_issues(data, {"barcelo2011"})
    assert any("arXiv status is present but arXiv ID is invalid" in issue
               for issue in issues)


def test_a_short_excerpt_is_not_paragraph_context(tmp_path, monkeypatch):
    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "barcelo2011.md").write_text(
        "# barcelo2011\n\nSSV-I main.tex:1\n\n"
        "## Abstract, p. 1\n\n> Too short.\n\n**Verdict: `OK`.**\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(E, "NOTES", notes)
    data = one_source("barcelo2011")

    assert any(
        "paragraph-sized verbatim context" in issue
        for issue in E.evidence_issues(data, {"barcelo2011"})
    )


def test_absence_claim_requires_corpus_and_zero_count(tmp_path, monkeypatch):
    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "faddeev1997.md").write_text(
        "# faddeev1997\n\nSSV-I main.tex:1\n\n"
        "We searched for junction-like language.\n\n"
        "**Verdict: `MISATTRIBUTED`.**\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(E, "NOTES", notes)
    data = one_source("faddeev1997")

    assert any(
        "corpus size and a zero-count search" in issue
        for issue in E.evidence_issues(data, {"faddeev1997"})
    )


def test_owner_supplied_scan_requires_accessible_transcript(
        tmp_path, monkeypatch):
    notes = tmp_path / "notes"
    notes.mkdir()
    quoted = "> " + " ".join(["source"] * 30)
    (notes / "lamb1932.md").write_text(
        "# lamb1932\n\nSSV-I main.tex:1\n\n"
        "Art. 163, p. 241\n\n"
        f"{quoted}\n\n**Verdict: `OK`.**\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(E, "NOTES", notes)
    monkeypatch.setattr(E, "TRANSCRIPTS", tmp_path / "transcripts")
    data = one_source("lamb1932")

    assert any(
        "has no Markdown transcript" in issue
        for issue in E.evidence_issues(data, {"lamb1932"})
    )

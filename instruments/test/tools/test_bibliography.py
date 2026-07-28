"""Tests for the shared BibTeX database and canonical citation keys."""

import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import bibliography as B  # noqa: E402


def write_fixture(tmp_path, *, main, database, registry='{"sources": {}}'):
    papers = tmp_path / "papers"
    paper = papers / "SSV-Test"
    cited = papers / "cited"
    paper.mkdir(parents=True)
    cited.mkdir()
    (paper / "main.tex").write_text(main, encoding="utf-8")
    bib = cited / "references.bib"
    bib.write_text(database, encoding="utf-8")
    verification = cited / "verification.json"
    verification.write_text(registry, encoding="utf-8")
    return papers, bib, verification


def test_every_series_paper_uses_the_shared_database_cleanly():
    papers = sorted(path.parent.name for path in B.PAPERS.glob("SSV-*/main.tex"))
    assert papers
    assert B.shared_issues() == []
    for paper in papers:
        assert B.issues_for(paper) == []


def test_undefined_citation_key_is_rejected(tmp_path):
    papers, database, verification = write_fixture(
        tmp_path,
        main=(
            r"\cite{missing}" "\n"
            r"\bibliographystyle{unsrt}" "\n"
            r"\bibliography{../cited/references}" "\n"
        ),
        database="@misc{known, note={{Known.}}}\n",
    )
    issues = B.issues_for(
        "SSV-Test", papers=papers, database=database,
        verification=verification,
    )
    assert any("undefined shared citation keys: ['missing']" in issue
               for issue in issues)


def test_inline_bibliography_is_rejected(tmp_path):
    papers, database, verification = write_fixture(
        tmp_path,
        main=(
            r"\begin{thebibliography}{9}\bibitem{known} Known."
            r"\end{thebibliography}" "\n"
        ),
        database="@misc{known, note={{Known.}}}\n",
    )
    issues = B.issues_for(
        "SSV-Test", papers=papers, database=database,
        verification=verification,
    )
    assert any("inline bibliography is forbidden" in issue for issue in issues)


def test_duplicate_database_key_is_rejected(tmp_path):
    papers, database, verification = write_fixture(
        tmp_path,
        main=(
            r"\bibliographystyle{unsrt}" "\n"
            r"\bibliography{../cited/references}" "\n"
        ),
        database=(
            "@misc{same, note={{First.}}}\n"
            "@misc{same, note={{Second.}}}\n"
        ),
    )
    issues = B.issues_for(
        "SSV-Test", papers=papers, database=database,
        verification=verification,
    )
    assert any("duplicate BibTeX keys: ['same']" in issue for issue in issues)


def test_every_quote_registry_source_must_exist_in_database(tmp_path):
    papers, database, verification = write_fixture(
        tmp_path,
        main=(
            r"\bibliographystyle{unsrt}" "\n"
            r"\bibliography{../cited/references}" "\n"
        ),
        database="@misc{known, note={{Known.}}}\n",
        registry='{"sources": {"quoted": {}}}',
    )
    issues = B.issues_for(
        "SSV-Test", papers=papers, database=database,
        verification=verification,
    )
    assert any("quote-registry sources absent" in issue and "quoted" in issue
               for issue in issues)

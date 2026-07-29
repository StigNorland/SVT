"""Tests for the read-only SSV verification audit."""

import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import ssv_verify as V  # noqa: E402


def test_numeric_inventory_distinguishes_generated_lines():
    tex = "\n".join([
        r"\usepackage[margin=2.5cm]{geometry}",
        r"\begin{document}",
        r"The measured value is $3.74\times10^{-11}$ m.",
        r"The generated value is $\ssvReStar$ and differs by 0.7\%.",
        r"% The obsolete value was 1.9.",
    ])

    got = V.extract_numeric_candidates(tex, {"ssvReStar"}, "paper.tex")

    assert [item["location"] for item in got] == [
        "paper.tex:3", "paper.tex:4"]
    assert [item["tokens"] for item in got] == [
        [r"3.74\times10^{-11}"], [r"0.7\%"]]
    assert got[0]["classification"] == "MANUAL_NUMERIC_CANDIDATE"
    assert got[1]["classification"] == "MIXED_WITH_GENERATED_VALUE"
    assert got[1]["review_id"] == "NUM-4"


def test_numeric_inventory_groups_tokens_by_line_and_prioritizes_claims():
    tex = "\n".join([
        r"\begin{document}",
        r"\begin{resultbox}[Closure]",
        r"The prediction matches at 0.3\% and differs by 1.2\%.",
        r"\end{resultbox}",
        r"\begin{equation}",
        r"x = 3.14",
        r"\end{equation}",
    ])

    got = V.extract_numeric_candidates(tex, set(), "paper.tex")

    assert got[0]["tokens"] == [r"0.3\%", r"1.2\%"]
    assert got[0]["priority"] == "HIGH"
    assert "resultbox" in got[0]["environments"]
    assert got[1]["priority"] == "LOW"
    assert got[1]["priority_reasons"] == ["display-math"]


def test_abstraction_section_is_not_mistaken_for_abstract():
    priority, reasons = V._numeric_priority(
        "A background estimate is 95\\%.",
        {"section": "Introduction: The Crisis of Abstraction",
         "environments": ("document",)},
    )

    assert priority == "LOW"
    assert reasons == ("background-or-unclassified",)


def test_numeric_inventory_omits_layout_only_table_dimensions():
    tex = "\n".join([
        r"\begin{document}",
        r"\section{Claim Status}",
        r"\renewcommand{\arraystretch}{1.2}",
        r"\begin{longtable}{p{0.32\linewidth} p{0.15\linewidth} "
        r"p{0.49\linewidth}}",
        r"A real claim remains within 1.5\% of the reference.",
    ])

    got = V.extract_numeric_candidates(tex, set(), "paper.tex")

    assert [item["review_id"] for item in got] == ["NUM-5"]
    assert got[0]["tokens"] == [r"1.5\%"]
    assert got[0]["priority"] == "HIGH"


def test_citation_uses_include_context_and_ignore_comments():
    tex = "\n".join([
        r"\section{Results}",
        "The setup sentence.",
        r"Supported here~\cite{alpha,beta}.",
        "The consequence follows.",
        r"% Retired use~\cite{beta}.",
        r"Also here~\citep{beta}.",
    ])

    got = V.citation_uses(tex, "beta", "main.tex")

    assert [item["location"] for item in got] == [
        "main.tex:3", "main.tex:6"]
    assert got[0]["review_id"] == "CITE-beta-3"
    assert got[0]["section"] == "Results"
    assert "The setup sentence." in got[0]["snippet"]
    assert "The consequence follows." in got[0]["snippet"]


def test_claim_anchor_resolves_current_line_not_registered_line(
    tmp_path, monkeypatch
):
    source = tmp_path / "papers" / "SSV-Test" / "main.tex"
    source.parent.mkdir(parents=True)
    source.write_text(
        "first line\nmoved text with\nan exact anchor here\n",
        encoding="utf-8",
    )
    claim = V.claims.Claim(
        "SSV-Test", "moved", "papers/SSV-Test/main.tex:999",
        "the statement", (), lambda: True,
        source_anchor="moved text with an exact anchor here",
    )
    monkeypatch.setattr(V, "REPO_ROOT", tmp_path)

    location, snippet = V.current_claim_location(claim)

    assert location == "papers/SSV-Test/main.tex:2"
    assert "exact anchor" in snippet


def test_verdict_never_claims_semantic_pass_from_green_checks():
    audit = V.Audit(
        paper="SSV-Test",
        generated_utc="2026-07-29T00:00:00Z",
        recomputed_instruments=False,
        findings=[
            V.Finding("X", "artifact-integrity", "PASS", "INFO", "green")
        ],
        include_all_numbers=False,
    )

    assert audit.verdict == "DETERMINISTIC_PASS_SEMANTIC_REVIEW_PENDING"
    assert audit.to_dict()["schema"] == "ssv-verify/v2"


def test_provenance_without_references_needs_no_generated_file(
    tmp_path, monkeypatch
):
    paper_dir = tmp_path / "papers" / "SSV-Test"
    paper_dir.mkdir(parents=True)
    monkeypatch.setattr(V, "PAPERS", tmp_path / "papers")
    monkeypatch.setattr(V.gen_provenance, "repo_slug", lambda: "owner/repo")
    audit = V.Audit(
        paper="SSV-Test",
        generated_utc="2026-07-29T00:00:00Z",
        recomputed_instruments=False,
    )

    V._audit_provenance(
        audit,
        "SSV-Test",
        r"\documentclass{article}\begin{document}No refs.\end{document}",
    )

    finding = next(
        item for item in audit.findings
        if item.check_id == "S1-PROVENANCE-RENDER"
    )
    assert finding.status == "PASS"
    assert "No provenance references" in finding.message


def test_deterministic_failure_controls_exit_verdict():
    audit = V.Audit(
        paper="SSV-Test",
        generated_utc="2026-07-29T00:00:00Z",
        recomputed_instruments=False,
        findings=[
            V.Finding(
                "X", "artifact-integrity", "FAIL", "CRITICAL", "drift")
        ],
    )

    assert audit.verdict == "DETERMINISTIC_FAIL"
    assert audit.to_dict()["summary"]["deterministic_failures"] == 1


def test_report_writer_refuses_to_overwrite(tmp_path):
    report = tmp_path / "report.md"
    report.write_text("existing", encoding="utf-8")

    try:
        V._write_new(report, "replacement")
    except FileExistsError:
        pass
    else:
        raise AssertionError("existing report was overwritten")

    assert report.read_text(encoding="utf-8") == "existing"

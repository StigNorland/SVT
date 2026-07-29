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
    assert [item["token"] for item in got] == [
        r"3.74\times10^{-11}", r"0.7\%"]
    assert got[0]["classification"] == "MANUAL_NUMERIC_CANDIDATE"
    assert got[1]["classification"] == "MIXED_WITH_GENERATED_VALUE"


def test_citation_locations_handle_multi_key_commands_and_comments():
    tex = "\n".join([
        r"Supported here~\cite{alpha,beta}.",
        r"% Retired use~\cite{beta}.",
        r"Also here~\citep{beta}.",
    ])

    assert V.citation_locations(tex, "beta", "main.tex") == [
        "main.tex:1", "main.tex:3"]


def test_verdict_never_claims_semantic_pass_from_green_checks():
    audit = V.Audit(
        paper="SSV-Test",
        generated_utc="2026-07-29T00:00:00Z",
        recomputed_instruments=False,
        findings=[
            V.Finding("X", "artifact-integrity", "PASS", "INFO", "green")
        ],
    )

    assert audit.verdict == "DETERMINISTIC_PASS_SEMANTIC_REVIEW_PENDING"


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

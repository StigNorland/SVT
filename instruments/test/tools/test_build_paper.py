"""Regression tests for the build gate's publication boundary."""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import build_paper as B  # noqa: E402


def paper_dir(tmp_path, *, log="", pdf=True):
    d = tmp_path / "SSV-Test"
    d.mkdir()
    if log is not None:
        (d / "main.log").write_text(log, encoding="utf-8")
    if pdf:
        (d / "main.pdf").write_bytes(b"%PDF-1.4 stale-or-current")
    return d


def completed(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def test_citation_evidence_defect_fails_the_build_gate(monkeypatch):
    monkeypatch.setattr(
        B.citation_evidence, "evidence_issues",
        lambda: ["source: missing paragraph context"],
    )

    with pytest.raises(B.GateFailure, match="missing paragraph context"):
        B.gate_citations("SSV-I")


def test_bibliography_defect_fails_the_build_gate(monkeypatch):
    monkeypatch.setattr(
        B.bibliography, "issues_for",
        lambda paper: [f"{paper}: undefined shared citation key"],
    )

    with pytest.raises(B.GateFailure, match="undefined shared citation key"):
        B.gate_bibliography("SSV-I")


def test_nonzero_pdflatex_exit_rejects_an_existing_pdf(tmp_path, monkeypatch):
    """A stale PDF must not turn a failed compile into a successful build."""
    paper_dir(tmp_path)
    monkeypatch.setattr(B, "PAPERS", tmp_path)
    monkeypatch.setattr(
        B.subprocess, "run",
        lambda *a, **k: completed(returncode=1, stdout="fatal compile failure"),
    )

    with pytest.raises(B.GateFailure, match=r"pass 1 exited 1"):
        B.run_pdflatex("SSV-Test")


def test_second_pdflatex_pass_must_also_succeed(tmp_path, monkeypatch):
    paper_dir(tmp_path)
    monkeypatch.setattr(B, "PAPERS", tmp_path)
    results = iter([
        completed(),  # pdflatex 1
        completed(),  # BibTeX
        completed(returncode=2, stderr="second pass failed"),
    ])
    monkeypatch.setattr(B.subprocess, "run", lambda *a, **k: next(results))

    with pytest.raises(B.GateFailure, match=r"pass 2 exited 2"):
        B.run_pdflatex("SSV-Test")


def test_bibtex_failure_rejects_the_build(tmp_path, monkeypatch):
    paper_dir(tmp_path)
    monkeypatch.setattr(B, "PAPERS", tmp_path)
    results = iter([
        completed(),
        completed(returncode=2, stderr="bad bibliography database"),
    ])
    monkeypatch.setattr(B.subprocess, "run", lambda *a, **k: next(results))

    with pytest.raises(B.GateFailure, match=r"BibTeX exited 2"):
        B.run_pdflatex("SSV-Test")


def test_undefined_reference_blocks_publication(tmp_path, monkeypatch):
    paper_dir(
        tmp_path,
        log="LaTeX Warning: Reference `missing' on page 1 undefined on input line 3.\n",
    )
    monkeypatch.setattr(B, "PAPERS", tmp_path)
    monkeypatch.setattr(B.subprocess, "run", lambda *a, **k: completed())

    with pytest.raises(B.GateFailure, match="undefined references or citations"):
        B.run_pdflatex("SSV-Test")


def test_clean_bibtex_build_succeeds(tmp_path, monkeypatch):
    paper_dir(tmp_path, log="Output written on main.pdf (1 page).\n")
    monkeypatch.setattr(B, "PAPERS", tmp_path)

    calls = []
    call_options = []

    def run(command, **kwargs):
        calls.append(command)
        call_options.append(kwargs)
        return completed()

    monkeypatch.setattr(B.subprocess, "run", run)

    assert B.run_pdflatex("SSV-Test") == (
        "BibTeX + 3 pdflatex passes, 0 errors, 0 undefined references")
    assert [command[0] for command in calls] == [
        "pdflatex", "bibtex", "pdflatex", "pdflatex"]
    assert all(options["errors"] == "replace" for options in call_options)


# --------------------------------------------------------------------------
# rule 17 — papers state current status, not their own edit history (#207)
# --------------------------------------------------------------------------

def change_record_paper(tmp_path, monkeypatch, tex, *, changelog=True):
    d = tmp_path / "SSV-Test"
    d.mkdir()
    (d / "main.tex").write_text(tex, encoding="utf-8")
    if changelog:
        (d / "CHANGELOG.md").write_text("# SSV-Test\n", encoding="utf-8")
    monkeypatch.setattr(B, "PAPERS", tmp_path)
    return d


def test_change_record_prose_fails_the_gate(tmp_path, monkeypatch):
    """The guard on the guard: a checker that passes everything guards nothing."""
    change_record_paper(
        tmp_path, monkeypatch,
        r"Earlier versions of this paper printed the opposite sign.")
    with pytest.raises(B.GateFailure, match="narrates its own edit history"):
        B.gate_change_records("SSV-Test")


def test_a_missing_changelog_fails_the_gate(tmp_path, monkeypatch):
    change_record_paper(tmp_path, monkeypatch, "Clean prose.", changelog=False)
    with pytest.raises(B.GateFailure, match="no CHANGELOG.md"):
        B.gate_change_records("SSV-Test")


def test_current_status_prose_passes(tmp_path, monkeypatch):
    change_record_paper(
        tmp_path, monkeypatch,
        r"The $\hbar/2$ prefactor is imported, not derived.")
    assert "current-status only" in B.gate_change_records("SSV-Test")


@pytest.mark.parametrize(
    "verdict", ["withdrawn", "falsified", "retracted", "rejected"])
def test_present_tense_verdicts_are_never_banned(tmp_path, monkeypatch, verdict):
    """Rule 1 outranks rule 17.

    Banning verdict words would turn this gate into a tool for deleting
    negative results — the exact defect #182 existed to find. A falsification
    stated in the present tense is not a change record, and must pass.
    """
    change_record_paper(
        tmp_path, monkeypatch,
        f"The symmetric Y-junction is {verdict}: it is forbidden in a "
        f"one-component condensate.")
    assert "current-status only" in B.gate_change_records("SSV-Test")
    assert verdict not in B.CHANGE_RECORD_PHRASES


def test_the_deny_list_is_matched_case_insensitively(tmp_path, monkeypatch):
    change_record_paper(tmp_path, monkeypatch, "EARLIER VERSIONS said so.")
    with pytest.raises(B.GateFailure):
        B.gate_change_records("SSV-Test")

"""Tests for the provenance-appendix generator.

The load-bearing guarantee: every Python-script path cited in any paper exists as
a tracked file in the repo, so the generated permalinks cannot 404. Plus parser
correctness for the LaTeX reference forms actually used in the papers."""

import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import gen_provenance as gp  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
PAPERS = sorted(p.parent.name for p in (REPO / "papers").glob("SSV-*/main.tex"))


def test_extract_issue_numbers_both_forms():
    # raw \#NN and the cross-ref macro \ssvissue{NN} both count
    issues, _, _ = gp.extract_refs(
        r"see \#92 and issues~\#76, \#91; also \ssvissue{34} and \#92 again.")
    assert issues == [34, 76, 91, 92]            # sorted + de-duped, both forms


def test_extract_script_paths_only_instruments_py():
    tex = (r"\texttt{instruments/paper\_i/foo.py} and \texttt{instruments/paper\_i/bar.py}, "
           r"but not \texttt{instruments/\_q/dir/}.")
    _, paths, _ = gp.extract_refs(tex)
    assert paths == ["instruments/paper_i/bar.py", "instruments/paper_i/foo.py"]


def test_extract_reports_resolves_real_note():
    # a real result note, cited paper-relative (resolved against papers/SSV-I/)
    tex = r"see \texttt{results/proton/ny-trefoil-derivation-result.md}."
    _, _, reports = gp.extract_refs(tex, paper="SSV-I")
    assert reports == ["papers/SSV-I/results/proton/ny-trefoil-derivation-result.md"]


def test_normalise_path_joins_line_wraps_and_unescapes():
    raw = "instruments/paper\\_i/trefoil\\_ny\\_\n        derivation.py"
    assert gp._normalise_path(raw) == "instruments/paper_i/trefoil_ny_derivation.py"


def test_render_has_permalink_issue_url_and_label():
    out = gp.render("SSV-I", [92], ["instruments/paper_i/trefoil_ny_derivation.py"],
                    ["papers/SSV-I/results/proton/ny-trefoil-derivation-result.md"],
                    "StigNorland/SVT")
    assert "https://github.com/StigNorland/SVT/issues/92" in out
    assert r"\label{issue:92}" in out            # hyperlink target for \ssvissue{92}
    assert "/blob/" in out                       # pinned permalink (script + report)
    assert "Reports" in out


def test_render_empty_paper_is_graceful():
    out = gp.render("SSV-X", [], [], [], "StigNorland/SVT")
    assert "no external code or issue references" in out


def test_no_broken_script_refs_in_any_paper():
    """THE guarantee: every cited instruments/*.py path exists in the repo."""
    broken = {}
    for paper in PAPERS:
        tex = (REPO / "papers" / paper / "main.tex").read_text(encoding="utf-8")
        _, paths, _ = gp.extract_refs(tex, paper)
        miss = gp.missing_code_paths(paths)
        if miss:
            broken[paper] = miss
    assert not broken, f"cited scripts not found in repo: {broken}"

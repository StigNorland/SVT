"""Tests for the provenance-appendix generator.

The load-bearing guarantee: every Python-script path cited in any paper exists as
a tracked file in the repo, so the generated permalinks cannot 404. Plus parser
correctness for the LaTeX reference forms actually used in the papers."""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
TOOLS = str(SRC_ROOT / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import gen_provenance as gp  # noqa: E402

PAPERS = sorted(p.parent.name for p in (SRC_ROOT.parent / "papers").glob("SSV-*/main.tex"))


def test_extract_issue_numbers():
    issues, _ = gp.extract_refs(r"see issue~\#92 and issues~\#76, \#91; also \#92 again.")
    assert issues == [76, 91, 92]            # sorted + de-duped


def test_extract_script_paths_only_src_py():
    tex = (r"\texttt{instruments/paper\_i/foo.py} and \texttt{instruments/paper\_i/bar.py}, but not "
           r"\texttt{papers/SSV-I/results/note.md} nor \texttt{instruments/\_q/dir/}.")
    _, paths = gp.extract_refs(tex)
    assert paths == ["instruments/paper_i/bar.py", "instruments/paper_i/foo.py"]


def test_normalise_path_joins_line_wraps_and_unescapes():
    # a \texttt path split across a LaTeX line break, with escaped underscores
    raw = "instruments/paper\\_i/trefoil\\_ny\\_\n        derivation.py"
    assert gp._normalise_path(raw) == "instruments/paper_i/trefoil_ny_derivation.py"


def test_render_contains_permalink_and_issue_url():
    # use a real tracked script so it resolves to a pinned commit
    out = gp.render("SSV-I", [92], ["instruments/paper_i/trefoil_ny_derivation.py"],
                    "StigNorland/SVT")
    assert "https://github.com/StigNorland/SVT/issues/92" in out
    assert r"\section{Code and Issue References}" in out
    assert "/blob/" in out                   # a pinned permalink was emitted


def test_render_empty_paper_is_graceful():
    out = gp.render("SSV-X", [], [], "StigNorland/SVT")
    assert "no external code or issue references" in out


def test_no_broken_script_refs_in_any_paper():
    """THE guarantee: every cited src/*.py path exists in the repo."""
    broken = {}
    for paper in PAPERS:
        tex = (SRC_ROOT.parent / "papers" / paper / "main.tex").read_text(encoding="utf-8")
        _, paths = gp.extract_refs(tex)
        miss = gp.missing_code_paths(paths)
        if miss:
            broken[paper] = miss
    assert not broken, f"cited scripts not found in repo: {broken}"

"""Tests for the provenance-appendix generator.

The load-bearing guarantee: every code/report reference cited in any paper —
whether a `\\texttt{...}` path or an in-text `\\ssvfile{stem}` / `\\ssvissue{N}`
cross-ref — resolves to a real repo file (or a real issue number), so the
generated permalinks/links cannot dangle."""

import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import gen_provenance as gp  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
PAPERS = sorted(p.parent.name for p in (REPO / "papers").glob("SSV-*/main.tex"))


def test_extract_issue_numbers_both_forms():
    issues, *_ = gp.extract_refs(
        r"see \#92 and issues~\#76, \#91; also \ssvissue{34} and \#92 again.")
    assert issues == [34, 76, 91, 92]


def test_extract_code_paths():
    tex = (r"\texttt{instruments/paper\_i/trefoil\_ny\_derivation.py} and "
           r"\texttt{instruments/paper\_i/cp1\_safety\_checks.py}.")
    _, code, _, broken = gp.extract_refs(tex)
    assert "instruments/paper_i/trefoil_ny_derivation.py" in code
    assert "instruments/paper_i/cp1_safety_checks.py" in code
    assert broken == []


def test_resolve_ref_bare_stem_and_paths():
    # bare stem (code) resolves by glob
    assert gp.resolve_ref("trefoil_ny_derivation", None) == \
        "instruments/paper_i/trefoil_ny_derivation.py"
    # bare stem (report) resolves by glob
    assert gp.resolve_ref("b2-lepton-spin-half", None) == \
        "papers/SSV-I/results/spinor/b2-lepton-spin-half.md"
    # paper-relative report path resolves
    assert gp.resolve_ref("results/spinor/b2-lepton-spin-half.md", "SSV-I") == \
        "papers/SSV-I/results/spinor/b2-lepton-spin-half.md"
    # nonsense resolves to None
    assert gp.resolve_ref("definitely_not_a_file_xyz", None) is None


def test_ssvfile_macro_is_scanned():
    _, code, reports, broken = gp.extract_refs(
        r"see \ssvfile{trefoil_ny_derivation} and \ssvfile{b2-lepton-spin-half}.", "SSV-I")
    assert code == ["instruments/paper_i/trefoil_ny_derivation.py"]
    assert reports == ["papers/SSV-I/results/spinor/b2-lepton-spin-half.md"]
    assert broken == []


def test_normalise_path_joins_line_wraps_and_unescapes():
    raw = "instruments/paper\\_i/trefoil\\_ny\\_\n        derivation.py"
    assert gp._normalise_path(raw) == "instruments/paper_i/trefoil_ny_derivation.py"


def test_render_has_links_and_file_labels():
    out = gp.render("SSV-I", [92], ["instruments/paper_i/trefoil_ny_derivation.py"],
                    ["papers/SSV-I/results/proton/ny-trefoil-derivation-result.md"],
                    "StigNorland/SVT")
    assert "https://github.com/StigNorland/SVT/issues/92" in out
    assert r"\label{issue:92}" in out
    assert r"\label{file:trefoil_ny_derivation}" in out      # code cross-ref target
    assert r"\label{file:ny-trefoil-derivation-result}" in out  # report cross-ref target
    assert "/blob/" in out


def test_render_empty_paper_is_graceful():
    out = gp.render("SSV-X", [], [], [], "StigNorland/SVT")
    assert "no external code or issue references" in out


def test_no_broken_refs_in_any_paper():
    """THE guarantee: every cited code/report ref resolves to a real repo file."""
    broken = {}
    for paper in PAPERS:
        tex = (REPO / "papers" / paper / "main.tex").read_text(encoding="utf-8")
        _, _, _, b = gp.extract_refs(tex, paper)
        if b:
            broken[paper] = b
    assert not broken, f"unresolved code/report references: {broken}"

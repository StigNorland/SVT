"""Tests for the generated-values mechanism (#198 Part A).

The load-bearing guarantee: a number printed in a paper and the instrument that
derives it cannot drift apart, because there is only one of them.

Four of these tests are hygiene.  The one that actually prevents the #182 defect
class is :func:`test_replaced_literal_is_gone` — without it, nothing stops a
value being re-typed into the prose next to its own macro, which is exactly how
``rho_0`` came to be printed as ``1.9`` beside a formula yielding ``0.0078``.
"""

import re
import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import gen_values as gv  # noqa: E402
import pytest  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
PAPERS = sorted(gv.REGISTRY)

# \ssv<CamelCase> — the generated-value namespace.  Deliberately excludes the
# cross-ref macros \ssvissue and \ssvfile, which are lower-case after "ssv".
VALUE_MACRO_RE = re.compile(r"\\(ssv[A-Z][A-Za-z]*)")


def _main_tex(paper: str) -> str:
    return (REPO / "papers" / paper / "main.tex").read_text(encoding="utf-8")


def _declared(paper: str) -> set[str]:
    text = gv.values_path(paper).read_text(encoding="utf-8")
    return set(re.findall(r"\\newcommand\{\\(ssv[A-Z][A-Za-z]*)\}", text))


def _used(paper: str) -> set[str]:
    return set(VALUE_MACRO_RE.findall(_main_tex(paper)))


# --------------------------------------------------------------------------
# formatting
# --------------------------------------------------------------------------

@pytest.mark.parametrize("x, sig, want", [
    (5.2496852, 3, "5.25"),
    (9.9590365e-5, 3, r"9.96\times10^{-5}"),
    (1.616255024e-35, 4, r"1.616\times10^{-35}"),
    (2.176434342e-8, 4, r"2.176\times10^{-8}"),
    (6.6743e-11, 3, r"6.67\times10^{-11}"),
    (5.20, 3, "5.20"),          # trailing zero is a significant figure, not noise
    (9.996e-5, 3, r"1.00\times10^{-4}"),   # rounding carry renormalises
])
def test_fmt(x, sig, want):
    assert gv.fmt(x, sig) == want


# --------------------------------------------------------------------------
# the registry is honest about where its numbers come from
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_every_source_resolves(paper):
    """`source` must name a real file and a real attribute in it — so the
    macro -> function -> test path a reader follows cannot dangle."""
    for v in gv.values_for(paper):
        path_part, _, attr = v.source.partition("::")
        assert (REPO / path_part).is_file(), f"{v.macro}: no such file {path_part}"
        mod = __import__(Path(path_part).stem)
        assert hasattr(mod, attr), f"{v.macro}: {path_part} has no {attr}"


# --------------------------------------------------------------------------
# no drift
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_values_tex_is_not_stale(paper):
    """The tracked values.tex equals a fresh generation.  This is `--check`."""
    assert gv.values_path(paper).is_file(), f"{paper}/values.tex not generated"
    fresh = gv.render(paper, gv.values_for(paper))
    assert gv.values_path(paper).read_text(encoding="utf-8") == fresh, (
        f"{paper}/values.tex is out of date — run "
        f"`python instruments/tools/gen_values.py {paper}`")


@pytest.mark.parametrize("paper", PAPERS)
def test_paper_inputs_values_tex(paper):
    assert r"\input{values.tex}" in _main_tex(paper), (
        f"{paper}/main.tex does not \\input its generated values")


# --------------------------------------------------------------------------
# declared <-> used
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_no_dead_macro(paper):
    dead = _declared(paper) - _used(paper)
    assert not dead, f"{paper}: declared but never used: {sorted(dead)}"


@pytest.mark.parametrize("paper", PAPERS)
def test_no_undeclared_macro(paper):
    """Catches a macro left in the prose after its registry entry was removed —
    which would otherwise fail only at build time, or silently print nothing."""
    undeclared = _used(paper) - _declared(paper)
    assert not undeclared, f"{paper}: used but not declared: {sorted(undeclared)}"


# --------------------------------------------------------------------------
# THE test
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_replaced_literal_is_gone(paper):
    """No generated value may also appear as a typed literal in the paper.

    This is the test that closes #198 Part A.  Everything above keeps
    values.tex correct; only this one stops a second, hand-typed copy of the
    same number from reappearing in the prose and drifting.
    """
    tex = _main_tex(paper)
    offenders = {v.macro: v.was for v in gv.values_for(paper)
                 if v.was and v.was in tex}
    assert not offenders, (
        f"{paper}: these values are printed as literals as well as macros — "
        f"use the macro: {offenders}")


@pytest.mark.parametrize("paper", PAPERS)
def test_generated_value_matches_its_instrument(paper):
    """The rendered string round-trips to the instrument value at the printed
    precision — so a formatting bug cannot silently misreport the computation."""
    for v in gv.values_for(paper):
        rendered = gv.fmt(v.compute(), v.sig)
        as_float = float(rendered.replace(r"\times10^{", "e").replace("}", ""))
        exact = float(v.compute())
        assert abs(as_float - exact) <= abs(exact) * 10.0 ** -(v.sig - 1), (
            f"{v.macro}: printed {rendered} but instrument gives {exact}")

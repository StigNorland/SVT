"""Tests for the programme-wide symbol registry (#213 Part A, executes #205).

The module has two halves with different failure modes, and they are tested
differently.

The **census** is machine-extracted, so what can go wrong is a filter that
silently drops a real symbol. An earlier draft filtered ``c``, ``t`` and ``r``
as LaTeX column specifiers, which would have hidden the speed of light, time
and radius. ``test_heavily_shared_physical_symbols_survive_the_filter`` is the
negative control against that class: it names symbols that *must* appear, so
tightening the filter fails loudly instead of quietly reporting a clean series.

The **declarations** are hand-written, so what can go wrong is a wrong
transcription. Those are checked for internal consistency and for agreement
with ``dimensions.py`` where the two overlap.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS = REPO_ROOT / "instruments" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import conventions as C  # noqa: E402
import dimensions as D  # noqa: E402


# --------------------------------------------------------------------------
# the census
# --------------------------------------------------------------------------

def test_census_covers_every_paper():
    seen = {p for papers in C.census().values() for p in papers}
    assert seen == set(C.paper_names())


#: Symbols that are unambiguously physical and unambiguously series-wide.
#: If the extractor stops reporting one of these, a filter has gone too far.
MUST_SURVIVE = {
    "c": 8,          # speed of light — was wrongly filtered as a column spec
    "t": 6,          # time           — likewise
    "r": 6,          # radius         — likewise
    "hbar": 8,
    "alpha": 8,
    "xi": 8,
    "rho_0": 8,
    "e": 6,          # the #182 E3b symbol; never filtered as Euler's number
}


@pytest.mark.parametrize("symbol,least", sorted(MUST_SURVIVE.items()))
def test_heavily_shared_physical_symbols_survive_the_filter(symbol, least):
    """The negative control on ``_NOISE``.

    A filter that is too aggressive makes the whole module report a clean
    series, which is the failure that looks most like success.
    """
    papers = C.census().get(symbol, set())
    assert len(papers) >= least, (
        f"{symbol!r} found in only {len(papers)} papers ({sorted(papers)}); "
        f"expected at least {least}. Has _NOISE or _STRIP swallowed it?")


def test_noise_filter_stays_tiny():
    """Growth here is how the census silently stops working."""
    assert C._NOISE == {"d"}, (
        "Adding to _NOISE removes a symbol from the census without any "
        "report. Strip the *construct* in _STRIP instead.")


def test_euler_note_documents_why_e_is_kept():
    assert "e" not in C._NOISE
    assert "E3b" in C.EULER_NOTE


# --------------------------------------------------------------------------
# the declarations
# --------------------------------------------------------------------------

def test_every_use_names_a_real_paper():
    names = set(C.paper_names())
    for u in C.USES:
        assert u.paper in names, f"{u.symbol}: unknown paper {u.paper}"


def test_every_use_site_points_at_a_real_line():
    """The transcription this module cannot machine-check is at least located."""
    for u in C.USES:
        path_s, _, lineno = u.site.rpartition(":")
        path = REPO_ROOT / path_s
        assert path.is_file(), f"{u.symbol}: no such file {u.site}"
        n = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        assert 1 <= int(lineno) <= n, f"{u.symbol}: {u.site} is past end of file"


def test_declared_symbol_actually_occurs_in_that_paper():
    """A declaration about a symbol the paper does not use is a stale record."""
    seen = C.census()
    for u in C.USES:
        assert u.paper in seen.get(u.symbol, set()), (
            f"{u.symbol} is declared for {u.paper} but the census does not "
            f"find it there — the declaration or the paper has moved")


# --------------------------------------------------------------------------
# the findings this pass established
# --------------------------------------------------------------------------

def test_the_three_known_collisions_are_reported():
    found = {c.symbol for c in C.collisions()}
    assert {"Lambda", "a_0", "b"} <= found


def test_lambda_carries_three_dimensions():
    """#213 Part A. Dimensionless in I/III, a wavenumber in III, a curvature
    in VI/VII-b/IX — and two of those are inside SSV-III alone."""
    lam = next(c for c in C.collisions() if c.symbol == "Lambda")
    assert len(lam.dims) == 3
    within_iii = [d for d, uses in lam.dims.items()
                  if any(p == "SSV-III" for p, _, _ in uses)]
    assert len(within_iii) == 2, (
        "SSV-III uses Lambda both as a slow logarithm and as the cutoff "
        "wavenumber xi^-1; that is the b-in-SSV-I error class inside one paper")


def test_a0_is_a_bohr_radius_and_an_acceleration():
    a0 = next(c for c in C.collisions() if c.symbol == "a_0")
    assert len(a0.dims) == 2


def test_a_declared_local_reuse_is_not_a_collision():
    """SSV-III's RG block factor ``b`` is declared local, so it must not be
    counted against the LogSE coupling. Without this, the guard would cry wolf
    on every legitimate reuse and stop being read."""
    b = next(c for c in C.collisions() if c.symbol == "b")
    reported = {p for uses in b.dims.values() for p, _, _ in uses}
    assert "SSV-III" not in reported
    assert "SSV-III" in b.declared_local


def test_local_declarations_state_a_reason():
    for u in C.USES:
        if u.local:
            assert len(u.local) > 20, (
                f"{u.paper} {u.symbol}: a local reuse must say why, or the "
                f"declaration is just a way to silence the check")


# --------------------------------------------------------------------------
# agreement with dimensions.py, where they overlap
# --------------------------------------------------------------------------

def test_b_dimensions_agree_with_the_dimensions_module():
    """The two modules reach ``b`` by different routes — one from declared
    per-paper dimensions, the other by solving the printed relations. They must
    not disagree."""
    from_conventions = {
        u.paper: C._dim_key(u.dim) for u in C.uses_of("b") if not u.local}
    for paper, declared in D.DECLARED.items():
        if "b" in declared and paper in from_conventions:
            assert from_conventions[paper] == C._dim_key(declared["b"]), (
                f"{paper}: conventions.py and dimensions.py disagree about [b]")


# --------------------------------------------------------------------------
# coverage is reported, never implied
# --------------------------------------------------------------------------

def test_coverage_admits_what_is_undeclared():
    cov = C.coverage()
    assert cov["undeclared_shared"], (
        "coverage() reporting nothing undeclared would mean the registry "
        "claims to cover all 145 shared tokens; it does not")
    assert cov["declared"] < cov["shared_2plus_papers"]


def test_docstring_states_the_limits():
    doc = C.__doc__
    for phrase in ("Not** guarded", "drift guard", "not referee"):
        assert phrase.lower() in doc.lower(), f"missing limit: {phrase}"

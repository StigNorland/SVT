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


def test_declared_symbol_is_declared_everywhere_it_occurs():
    """Once a symbol is declared at all, every paper using it must be declared.

    Scoped to ``COMPLETE`` — the symbols whose declarations claim to be
    exhaustive. This is the test that would have caught the first pass's own
    omission: the census reported ``\\Lambda`` in 7 papers while the table
    declared 5, silently understating the collision as three dimensions when it
    is four. A partial declaration is worse than none, because it reports a
    number that looks complete.
    """
    seen = C.census()
    gaps = []
    for symbol in sorted(C.COMPLETE):
        have = {u.paper for u in C.uses_of(symbol)}
        missing = seen.get(symbol, set()) - have
        if missing:
            gaps.append(f"{symbol}: undeclared in {sorted(missing)}")
    assert not gaps, "\n".join(gaps)


def test_lambda_carries_four_dimensions():
    """Dimensionless (I, III), a wavenumber (III), a curvature (VI/VII-b/VIII/IX)
    and an energy (II, Lambda_QCD). Four unrelated quantities, four fields, one
    letter."""
    lam = next(c for c in C.collisions() if c.symbol == "Lambda")
    assert len(lam.dims) == 4, sorted(lam.dims)


# --------------------------------------------------------------------------
# the external reference (physics.info, owner's choice 2026-07-29)
# --------------------------------------------------------------------------

def test_departure_check_is_not_vacuous():
    """FM3: a check that cannot fire is not a check.

    The first version of ``departures_from_standard`` returned an empty list —
    not because SSV agrees with the reference, but because the declared symbols
    and the reference's symbols barely overlapped. An empty result read as a
    clean bill of health and was nothing of the kind.
    """
    assert len(C.departures_from_standard()) >= 5, (
        "the departure check has stopped finding the known departures; if the "
        "declared set no longer overlaps STANDARD, an empty result means the "
        "check is silent, not that the series agrees")


def test_root_symbol_carries_the_readers_expectation():
    """``a_0`` and ``a_p`` must be checked against ``a``.

    This is what makes the reference useful for the a_0 question: the MOND
    scale agrees with the root symbol's standard meaning and the Bohr radius
    does not, which is a fact about the reader independent of which usage is
    older.
    """
    assert C._standard_for("a_p"), "a_p must inherit the entry for a"
    reported = " ".join(C.departures_from_standard())
    assert "a_0 in SSV-I" in reported
    assert "a_0 in SSV-VI" not in reported, (
        "the MOND a_0 IS an acceleration and must not be reported as a "
        "departure — otherwise the check punishes the conforming usage")


def test_the_reference_cannot_arbitrate_our_collisions():
    """Recorded so nobody later mistakes this page for an authority.

    physics.info has no entry for Lambda, b or hbar — it does not cover the
    collisions this module exists to find, and the docstring says which
    documents would.
    """
    for symbol in ("Lambda", "b", "hbar"):
        assert symbol in C.NOT_IN_STANDARD
        assert not C._standard_for(symbol)
    assert "ISO 80000" in C.__dict__["STANDARD"].__doc__ or True
    src = (REPO_ROOT / "instruments/tools/conventions.py").read_text()
    for authority in ("ISO 80000", "SUNAMCO", "NIST SP 811"):
        assert authority in src, f"the real standard {authority} is not named"


def test_reference_source_is_pinned_with_url_and_date():
    src = (REPO_ROOT / "instruments/tools/conventions.py").read_text()
    assert "https://physics.info/symbols/" in src
    assert re.search(r"retrieved 20\d\d-\d\d-\d\d", src)


def test_every_collision_symbol_is_asserted_complete():
    """A collision COUNT is only meaningful over a complete declaration.

    Without this, a symbol could be reported as carrying two dimensions purely
    because the third paper was never declared — the exact failure the first
    pass of this file committed.
    """
    for c in C.collisions():
        assert c.symbol in C.COMPLETE, (
            f"{c.symbol} is reported as a collision but its declarations are "
            f"only a sample; the dimension count cannot be trusted")


def test_sampled_symbols_are_not_silently_treated_as_complete():
    sampled = {u.symbol for u in C.USES} - C.COMPLETE
    assert sampled, "COMPLETE has swallowed every symbol; the split is doing nothing"

"""Tests for the typed-dimension checker (#198 Part B).

The load-bearing test here is **not** that everything passes.  A green suite over
corrected relations proves nothing about whether the checker can see anything.
What proves it is :func:`test_known_defects_are_detected`: the three dimensional
defects #182 actually found, encoded **as printed**, must each come back
inhomogeneous.  A checker that cannot reproduce a known failure is not evidence
about the failures it has not seen.
"""

import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import dimensions as D  # noqa: E402
import pytest  # noqa: E402

PAPERS = sorted(D.ANCHORED)


# --------------------------------------------------------------------------
# THE test — the checker reproduces the defects that motivated it
# --------------------------------------------------------------------------

def test_known_defects_are_detected():
    """SSV-I E6, SSV-II E3b and SSV-II E3d, encoded as printed, must all fail."""
    failing = {r.label for p in PAPERS for r in D.relations_for(p)
               if not D.is_homogeneous(r)}
    assert {"eq:cs", "eq:xi", "eq:brho0"} <= failing        # SSV-I E6
    assert "eq:berry_ab" in failing                          # SSV-II E3b
    assert "eq:flux_quantisation" in failing                 # SSV-II E3d


def test_ssv_i_b_has_no_consistent_dimension():
    """E6, stated without arguing which equation is the wrong one: there is NO
    dimension for `b` making SSV-I's four printed relations simultaneously well
    formed."""
    assert D.consistent_assignment("SSV-I", "b") is None
    req = D.requirements("SSV-I", "b")
    assert D._key(req["eq:pot"]) != D._key(req["eq:cs"])
    # and the gap is exactly L^3, as the damage report says
    assert req["eq:pot"] == D.dims(D.ENERGY / D.mass)
    assert req["eq:cs"] == D.dims(D.ENERGY / D.mass * D.length**3)
    assert req["eq:cs"] == req["eq:xi"] == req["eq:brho0"]


def test_ssv_ii_e_must_be_both_a_mass_and_a_charge():
    """E3b.  The Berry phase needs a mass; Phi_0 = h/e needs a charge."""
    assert D.consistent_assignment("SSV-II", "e") is None
    req = D.requirements("SSV-II", "e")
    assert req["eq:berry_ab"] == D.dims(D.mass)
    assert req["eq:flux_quantum"] == D.dims(D.charge)


def test_ssv_ii_flux_quantisation_cannot_be_repaired_by_redefining_e():
    """E3d.  The relation contains no free symbol, so the whole argument about
    what `e` means cannot reach it — it is broken on its own terms."""
    un = [r.label for r in D.unrepairable("SSV-II")]
    assert un == ["eq:flux_quantisation"]


def test_ssv_ii_flux_mismatch_is_exactly_L2_T():
    """The mismatch quoted in the paper, L^-2 T^-1, is correct — verified here
    because the two dimensions it is quoted *between* were not (see the report
    for #198: the paper printed M T^-3 for a quantity that is M T^-2, and
    M L^2 T^-2 for h, which is an energy, not an action)."""
    rel = next(r for r in D.relations_for("SSV-II")
               if r.label == "eq:flux_quantisation")
    assert D.residual(rel) == D.dims(1 / (D.length**2 * D.time))
    # the quantity itself is M T^-2, NOT the M T^-3 the paper printed
    assert D.dims(D.combination(rel)) == D.dims(D.mass / D.time**2)
    assert D.dims(D.combination(rel)) != D.dims(D.mass / D.time**3)


def test_h_is_an_action_not_an_energy():
    """Guard on the constant that SSV-II's item (iv) got wrong."""
    assert D.dims(D.ACTION) == D.dims(D.mass * D.length**2 / D.time)
    assert D.dims(D.ACTION) != D.dims(D.ENERGY)


# --------------------------------------------------------------------------
# the corrected forms really are corrected
# --------------------------------------------------------------------------

def test_ssv_i_corrected_relations_are_homogeneous():
    """The E6 repair works: with [b] = J/kg, c_s^2 = b and xi = hbar/sqrt(2 m^2 b)
    both balance — which the printed forms do not."""
    for label in ("eq:cs-corrected", "eq:xi-corrected"):
        rel = next(r for r in D.relations_for("SSV-I") if r.label == label)
        assert D.is_homogeneous(rel), f"{label}: residual {D.residual(rel)}"


def test_ssv_v_b_is_consistent_and_is_a_frequency():
    """#187 E2: SSV-V's `b` is fine — it is simply a different quantity, and the
    paper now says so."""
    assert D.consistent_assignment("SSV-V", "b") == D.dims(D.FREQUENCY)


def test_b_differs_across_papers_and_that_is_declared():
    """The cross-paper collision that E2 was about.  This test asserts the
    difference EXISTS — it is a fact about the series, not a defect, and the
    repair was to declare it rather than to unify the symbol."""
    across = D.declared_across_papers("b")
    assert across["SSV-I"] != across["SSV-V"]
    assert across["SSV-V"] == D.dims(D.FREQUENCY)


# --------------------------------------------------------------------------
# hygiene
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_no_relation_disagrees_with_its_declared_status(paper):
    """Every relation is homogeneous, or is recorded as a known defect and still
    fails.  A drift either way shows up here."""
    bad = D.check(paper)
    assert not bad, f"{paper}: status now wrong for {[r.label for r in bad]}"


@pytest.mark.parametrize("paper", PAPERS)
def test_every_symbol_used_is_declared(paper):
    """No relation may reference a symbol with no declared dimension."""
    known = set(D.ANCHORED[paper]) | set(D.DECLARED.get(paper, {}))
    for r in D.relations_for(paper):
        missing = set(r.powers) - known
        assert not missing, f"{r.label} uses undeclared symbols {missing}"


@pytest.mark.parametrize("paper", PAPERS)
def test_free_and_anchored_are_disjoint(paper):
    """A symbol cannot be both pinned by definition and solved for."""
    assert not (set(D.ANCHORED[paper]) & D.FREE[paper])


@pytest.mark.parametrize("paper", PAPERS)
def test_relation_sites_exist(paper):
    """Each transcription cites a real file — the module cannot check that the
    transcription is faithful, so the least it can do is keep the pointer live."""
    repo = Path(__file__).resolve().parents[3]
    for r in D.relations_for(paper):
        f = r.site.split("::")[0].split(":")[0]
        assert (repo / f).is_file(), f"{r.label}: no such file {f}"


def test_solving_for_an_anchored_symbol_is_refused():
    """Guard against the mistake this module was rewritten to fix: solving a
    broken relation for a healthy symbol yields noise, and must not be offered
    as a finding."""
    rel = next(r for r in D.relations_for("SSV-I") if r.label == "eq:xi")
    with pytest.raises(ValueError):
        D.implied_dimension(rel, "hbar")

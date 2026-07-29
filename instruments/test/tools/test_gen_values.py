"""Tests for the generated-values mechanism (#198 Part A).

The load-bearing guarantee: a number printed in a paper and the instrument that
derives it cannot drift apart.

Since the compute and render phases are separated by a receipt, that guarantee
now spans three artifacts, and each hop needs its own test:

    instrument  --[test_receipt_matches_instruments]-->  values_receipt.json
                --[test_values_tex_matches_receipt]-->   values.tex
                --[test_replaced_literal_is_gone]-->     main.tex

Only the first of the three has to run any physics.  If it is ever skipped
because a computation has become too expensive, the guarantee weakens to "the
paper matches what the instrument said when it was last run" — still far better
than a hand-typed literal, but a different claim, and one that must be stated
rather than assumed.
"""

import json
import re
import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import gen_values as gv  # noqa: E402
import pytest  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
LOCAL_PAPERS = sorted(gv.REGISTRY)
PAPERS = gv.registered_papers()

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
# hop 1 — instrument -> receipt   (the only test that runs physics)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_receipt_exists_and_is_wellformed(paper):
    r = gv.read_receipt(paper)
    assert r["paper"] == paper and r["issue"] == 198
    assert r["values"], f"{paper}: receipt records no values"
    for macro, e in r["values"].items():
        assert set(e) == {"value", "sig", "rendered", "describes", "source",
                          "source_sha256_16", "was"}, f"{macro}: bad fields"


@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_receipt_matches_instruments(paper):
    """Re-run the physics and compare against the recorded last run.

    This is what makes the receipt *checkable* rather than merely trusted, and
    it is the hop that closes the drift surface the receipt introduces.
    """
    drift = gv.receipt_drift(paper)
    summary = {k: (v["receipt"] and v["receipt"].get("rendered"),
                   v["now"] and v["now"].get("rendered"))
               for k, v in drift.items()}
    assert not drift, (
        f"{paper}: receipt no longer describes what the instruments produce: "
        f"{summary} — run `gen_values.py --compute {paper}`")


@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_recorded_fingerprints_match_the_instruments_on_disk(paper):
    """Cheap staleness signal, independent of re-running: the instrument file
    backing each value is byte-for-byte what it was when the receipt was written."""
    for macro, e in gv.read_receipt(paper)["values"].items():
        assert e["source_sha256_16"] == gv.source_fingerprint(e["source"]), (
            f"{macro}: {e['source'].split('::')[0]} has changed since the "
            f"receipt was computed")


@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_every_source_resolves(paper):
    """`source` must name a real file and a real attribute in it — so the
    macro -> receipt -> function -> test path a reader follows cannot dangle."""
    for macro, e in gv.read_receipt(paper)["values"].items():
        path_part, _, attr = e["source"].partition("::")
        assert (REPO / path_part).is_file(), f"{macro}: no such file {path_part}"
        mod = __import__(Path(path_part).stem)
        assert hasattr(mod, attr), f"{macro}: {path_part} has no {attr}"


@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_registry_and_receipt_declare_the_same_macros(paper):
    """A value added to the registry but never computed would otherwise be
    invisible until someone noticed the paper was missing a number."""
    assert {v.macro for v in gv.values_for(paper)} == set(
        gv.read_receipt(paper)["values"])


# --------------------------------------------------------------------------
# series receipt — one computation, multiple declaring papers (#213 Part B)
# --------------------------------------------------------------------------

def test_shared_receipt_exists_and_is_wellformed():
    receipt = gv.read_shared_receipt()
    assert receipt["issue"] == 213 and receipt["scope"] == "SSV series"
    assert receipt["values"]
    for macro, entry in receipt["values"].items():
        assert set(entry) == {
            "value", "sig", "rendered", "describes", "source",
            "source_sha256_16", "papers", "was",
        }, f"{macro}: bad shared fields"
        assert len(entry["papers"]) >= 2, (
            f"{macro}: shared values must be printed in at least two papers")


def test_shared_receipt_matches_instruments():
    drift = gv.shared_receipt_drift()
    assert not drift, (
        f"shared receipt no longer describes its sources: {sorted(drift)} — "
        f"run `gen_values.py --shared --compute`")


def test_shared_registry_and_receipt_declare_the_same_surface():
    receipt = gv.read_shared_receipt()["values"]
    assert {value.macro for value in gv.SHARED} == set(receipt)
    for value in gv.SHARED:
        entry = receipt[value.macro]
        assert entry["papers"] == list(value.papers)
        assert entry["was"] == {
            paper: list(literals) for paper, literals in value.was.items()
        }
        assert set(value.was) == set(value.papers)


def test_every_shared_source_resolves_and_is_fingerprint_current():
    for macro, entry in gv.read_shared_receipt()["values"].items():
        path_part, _, attr = entry["source"].partition("::")
        assert (REPO / path_part).is_file(), f"{macro}: no such file {path_part}"
        module = __import__(Path(path_part).stem)
        assert hasattr(module, attr), f"{macro}: {path_part} has no {attr}"
        assert entry["source_sha256_16"] == gv.source_fingerprint(entry["source"])


def test_shared_receipt_is_deterministic_apart_from_timestamp():
    first = gv.compute_shared_receipt()
    second = gv.compute_shared_receipt()
    first.pop("computed_utc"), second.pop("computed_utc")
    assert first == second


def test_shared_macros_are_unique_and_do_not_collide_with_local_macros():
    shared = [value.macro for value in gv.SHARED]
    assert len(shared) == len(set(shared))
    for paper in PAPERS:
        local = (
            {value.macro for value in gv.values_for(paper)}
            if paper in gv.REGISTRY else set()
        )
        assert local.isdisjoint(value.macro for value in gv.shared_values_for(paper))


def test_numeric_literal_matching_uses_token_boundaries():
    assert gv.literal_occurs("x=139.570 MeV", "139.570")
    assert not gv.literal_occurs("x=139.57018 MeV", "139.570")
    assert gv.literal_occurs(r"x=1.3\times10^{-15}", r"1.3\times10^{-15}")
    assert gv.literal_occurs(
        "x=2.10\\times\n  10^{-16}", r"2.10\times10^{-16}")


# --------------------------------------------------------------------------
# hop 2 — receipt -> values.tex   (imports nothing)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_values_tex_matches_receipt(paper):
    assert gv.values_path(paper).is_file(), f"{paper}/values.tex not generated"
    local = gv.read_receipt(paper) if paper in gv.REGISTRY else None
    shared = gv.read_shared_receipt() if gv.shared_values_for(paper) else None
    fresh = gv.render(paper, local, shared)
    assert gv.values_path(paper).read_text(encoding="utf-8") == fresh, (
        f"{paper}/values.tex is out of date with its receipt — run "
        f"`python instruments/tools/gen_values.py {paper}`")


def test_rendering_does_not_import_instruments():
    """The point of the split: a document build must not run the physics.

    Rendering from an in-memory receipt must work with the paper's instrument
    modules absent from sys.modules and unimportable.
    """
    receipt = {"values": {"ssvFake": {
        "rendered": r"1.23\times10^{-4}", "describes": "x", "source": "y::z"}}}
    saved = dict(sys.modules)
    for name in ("ssv_i_audit_2026", "planck_scale_values", "series_values"):
        sys.modules.pop(name, None)
    saved_path = list(sys.path)
    try:
        sys.path[:] = [p for p in sys.path if "instruments" not in p]
        out = gv.render("SSV-I", receipt)
    finally:
        sys.path[:] = saved_path
        sys.modules.update(saved)
    assert r"\newcommand{\ssvFake}{1.23\times10^{-4}}" in out


@pytest.mark.parametrize("paper", PAPERS)
def test_paper_inputs_values_tex(paper):
    assert r"\input{values.tex}" in _main_tex(paper), (
        f"{paper}/main.tex does not \\input its generated values")


# --------------------------------------------------------------------------
# hop 3 — values.tex -> main.tex
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


@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_replaced_literal_is_gone(paper):
    """No generated value may also appear as a typed literal in the paper.

    This is the test that closes #198 Part A.  Everything above keeps the chain
    internally consistent; only this one stops a second, hand-typed copy of the
    same number from reappearing in the prose and drifting.
    """
    tex = _main_tex(paper)
    offenders = {macro: e["was"]
                 for macro, e in gv.read_receipt(paper)["values"].items()
                 if e["was"] and e["was"] in tex}
    assert not offenders, (
        f"{paper}: these values are printed as literals as well as macros — "
        f"use the macro: {offenders}")


@pytest.mark.parametrize("paper", PAPERS)
def test_no_shared_literal_survives(paper):
    """#213 Part C: every declared cross-paper copy was replaced by its macro."""
    offenders = gv.surviving_shared_literals(paper)
    assert not offenders, (
        f"{paper}: registered shared values remain typed beside their macros: "
        f"{offenders}")


@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_rendered_value_round_trips(paper):
    """The rendered string round-trips to the recorded value at the printed
    precision — so a formatting bug cannot silently misreport the computation."""
    for macro, e in gv.read_receipt(paper)["values"].items():
        as_float = float(e["rendered"].replace(r"\times10^{", "e").replace("}", ""))
        exact = float(e["value"])
        assert abs(as_float - exact) <= abs(exact) * 10.0 ** -(e["sig"] - 1), (
            f"{macro}: printed {e['rendered']} but recorded {exact}")


def test_shared_rendered_values_round_trip():
    for macro, entry in gv.read_shared_receipt()["values"].items():
        as_float = float(
            entry["rendered"].replace(r"\times10^{", "e").replace("}", "")
        )
        exact = float(entry["value"])
        assert abs(as_float - exact) <= abs(exact) * 10.0 ** -(entry["sig"] - 1), (
            f"{macro}: printed {entry['rendered']} but recorded {exact}")


# --------------------------------------------------------------------------
# the receipt is a tracked, readable record
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_receipt_is_deterministic_apart_from_its_timestamp(paper):
    """Two computes must differ only in `computed_utc`.  If anything else moves,
    the receipt is not a stable record and its git history is not the history of
    the number."""
    a = gv.compute_receipt(paper)
    b = gv.compute_receipt(paper)
    a.pop("computed_utc"), b.pop("computed_utc")
    assert a == b


@pytest.mark.parametrize("paper", LOCAL_PAPERS)
def test_receipt_is_valid_json_on_disk(paper):
    json.loads(gv.receipt_path(paper).read_text(encoding="utf-8"))

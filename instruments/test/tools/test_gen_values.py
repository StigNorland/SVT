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
# hop 1 — instrument -> receipt   (the only test that runs physics)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_receipt_exists_and_is_wellformed(paper):
    r = gv.read_receipt(paper)
    assert r["paper"] == paper and r["issue"] == 198
    assert r["values"], f"{paper}: receipt records no values"
    for macro, e in r["values"].items():
        assert set(e) == {"value", "sig", "rendered", "describes", "source",
                          "source_sha256_16", "was"}, f"{macro}: bad fields"


@pytest.mark.parametrize("paper", PAPERS)
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


@pytest.mark.parametrize("paper", PAPERS)
def test_recorded_fingerprints_match_the_instruments_on_disk(paper):
    """Cheap staleness signal, independent of re-running: the instrument file
    backing each value is byte-for-byte what it was when the receipt was written."""
    for macro, e in gv.read_receipt(paper)["values"].items():
        assert e["source_sha256_16"] == gv.source_fingerprint(e["source"]), (
            f"{macro}: {e['source'].split('::')[0]} has changed since the "
            f"receipt was computed")


@pytest.mark.parametrize("paper", PAPERS)
def test_every_source_resolves(paper):
    """`source` must name a real file and a real attribute in it — so the
    macro -> receipt -> function -> test path a reader follows cannot dangle."""
    for macro, e in gv.read_receipt(paper)["values"].items():
        path_part, _, attr = e["source"].partition("::")
        assert (REPO / path_part).is_file(), f"{macro}: no such file {path_part}"
        mod = __import__(Path(path_part).stem)
        assert hasattr(mod, attr), f"{macro}: {path_part} has no {attr}"


@pytest.mark.parametrize("paper", PAPERS)
def test_registry_and_receipt_declare_the_same_macros(paper):
    """A value added to the registry but never computed would otherwise be
    invisible until someone noticed the paper was missing a number."""
    assert {v.macro for v in gv.values_for(paper)} == set(
        gv.read_receipt(paper)["values"])


# --------------------------------------------------------------------------
# hop 2 — receipt -> values.tex   (imports nothing)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_values_tex_matches_receipt(paper):
    assert gv.values_path(paper).is_file(), f"{paper}/values.tex not generated"
    fresh = gv.render(paper, gv.read_receipt(paper))
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
    for name in ("ssv_i_audit_2026", "planck_scale_values"):
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


@pytest.mark.parametrize("paper", PAPERS)
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
def test_rendered_value_round_trips(paper):
    """The rendered string round-trips to the recorded value at the printed
    precision — so a formatting bug cannot silently misreport the computation."""
    for macro, e in gv.read_receipt(paper)["values"].items():
        as_float = float(e["rendered"].replace(r"\times10^{", "e").replace("}", ""))
        exact = float(e["value"])
        assert abs(as_float - exact) <= abs(exact) * 10.0 ** -(e["sig"] - 1), (
            f"{macro}: printed {e['rendered']} but recorded {exact}")


# --------------------------------------------------------------------------
# the receipt is a tracked, readable record
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_receipt_is_deterministic_apart_from_its_timestamp(paper):
    """Two computes must differ only in `computed_utc`.  If anything else moves,
    the receipt is not a stable record and its git history is not the history of
    the number."""
    a = gv.compute_receipt(paper)
    b = gv.compute_receipt(paper)
    a.pop("computed_utc"), b.pop("computed_utc")
    assert a == b


@pytest.mark.parametrize("paper", PAPERS)
def test_receipt_is_valid_json_on_disk(paper):
    json.loads(gv.receipt_path(paper).read_text(encoding="utf-8"))

"""Generate the printed-value macros for SSV papers (#198 Part A).

The problem this closes: a number printed in a paper and the instrument that
derives it were two independent objects.  ``eq:rho0-value``'s
:math:`9.96\\times10^{-5}` was typed into the ``.tex`` by hand, and the only
thing keeping it equal to what ``instruments/paper_i/ssv_i_audit_2026.py``
produces was care at the time of writing.  Nothing detected drift — which is how
the original defect survived: ``rho_0`` was printed as :math:`1.9` alongside a
formula yielding :math:`0.0078`, and the two disagreed in print for years.

Three artifacts, two phases
---------------------------
The computation and the rendering are **separated**, so a document build never
re-runs the physics (owner's design call, 2026-07-28)::

    instrument  --(--compute)-->  results/values_receipt.json  --()-->  values.tex  --> PDF
       slow, run when                the result of the             cheap, run
       the physics changes              LAST run                  before every build

* ``--compute`` runs the instruments and writes the receipt.  This is the only
  phase that imports a paper's instruments.
* the default phase reads the **receipt** and writes ``values.tex``.  It imports
  nothing, so rendering costs nothing however expensive the physics becomes.
* ``--check`` re-runs the instruments and compares against the receipt, so the
  recorded result of the last run is *checkable* rather than merely trusted.

The receipt follows the series' existing ``results/*_receipt.json`` convention:
it is a tracked record of what a run produced, and its git history is the history
of the number.

What this buys, and what it costs
----------------------------------
Buys: rendering is cheap and cannot fail on a numerical dependency; the value's
provenance is a tracked file; the history of a printed number is inspectable.

Costs: the receipt is a **new intermediate artifact, and therefore a new place to
drift** — the exact failure mode this issue exists to close, moved one level up.
It is closed by ``--check`` and by ``test_receipt_matches_instruments``.  If that
test is ever skipped because a computation has become too expensive to re-run,
the guarantee weakens from "the paper matches the instrument" to "the paper
matches what the instrument said when it was last run" — which is still far
better than a hand-typed literal, but it is a different claim and must be stated
as one, not assumed.

Macro namespace: ``\\ssv<CamelCase>``.  Deliberately disjoint from the existing
``\\ssvissue`` / ``\\ssvfile`` cross-ref macros (lower-case after ``ssv``), so
the regex ``\\\\ssv[A-Z][A-Za-z]*`` matches generated values and nothing else.

Scope is deliberately narrow — the load-bearing numbers touched by #182 — not
every number in the series.  The goal is that *derived* numbers are generated,
not that prose becomes unwritable.

Usage:
    python instruments/tools/gen_values.py --compute SSV-I   # run physics -> receipt
    python instruments/tools/gen_values.py SSV-I             # receipt -> values.tex
    python instruments/tools/gen_values.py --all             # every registered paper
    python instruments/tools/gen_values.py --all --check     # re-run + compare, write nothing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS = REPO_ROOT / "papers"
INSTRUMENTS = REPO_ROOT / "instruments"

# Run as a CLI there is no pytest conftest to set up sys.path, so do it here.
for _d in [INSTRUMENTS, *sorted(INSTRUMENTS.glob("paper_*"))]:
    if _d.is_dir() and str(_d) not in sys.path:
        sys.path.insert(0, str(_d))


# --------------------------------------------------------------------------
# Registry — the declaration.  The receipt is the result.
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Value:
    """One generated macro.

    ``macro``     name without the backslash, e.g. ``ssvRhoZero``
    ``compute``   zero-argument callable returning the number
    ``sig``       significant figures, as the paper prints it
    ``describes`` short human note, rendered as a comment in ``values.tex``
    ``source``    ``<repo-relative .py>::<function>`` — checked by the test suite
    ``was``       the literal this macro replaced.  The test asserts this string
                  no longer occurs in the paper, which is what stops a value
                  from being re-typed alongside its own macro.
    """

    macro: str
    compute: Callable[[], float]
    sig: int
    describes: str
    source: str
    was: str


def _ssv_i() -> list[Value]:
    import ssv_i_audit_2026 as A
    return [
        Value("ssvLambda", lambda: A.lambda_param(), 3,
              r"\Lambda = \ln(8/\alpha) - 7/4",
              "instruments/paper_i/ssv_i_audit_2026.py::lambda_param",
              "5.25"),
        Value("ssvRhoZero", lambda: A.rho0_natural_units(sqrt2_corrected=True), 3,
              r"\rho_0 in units of m_e^4 c^3/\hbar^3 (E5 route 1, \sqrt2-corrected)",
              "instruments/paper_i/ssv_i_audit_2026.py::rho0_natural_units",
              r"9.96\times10^{-5}"),
        Value("ssvReStar", lambda: A.xi_over_alpha(sqrt2_corrected=True), 3,
              r"R_e^* = \xi/\alpha = a_0/\sqrt2, in metres",
              "instruments/paper_i/ssv_i_audit_2026.py::xi_over_alpha",
              ""),   # newly printed by this pass; replaced no literal
    ]


def _ssv_vii_b() -> list[Value]:
    import planck_scale_values as P
    return [
        Value("ssvEllP", lambda: P.planck_length(), 4,
              r"\ell_P = \sqrt{\hbar G/c^3}, in metres",
              "instruments/paper_vii_b/planck_scale_values.py::planck_length",
              r"1.616\times10^{-35}"),
        Value("ssvMZero", lambda: P.fundamental_mass(), 4,
              r"m_0 = m_P/\sqrt2, in kg (the D1 \sqrt2 correction)",
              "instruments/paper_vii_b/planck_scale_values.py::fundamental_mass",
              r"1.539\times10^{-8}"),
        Value("ssvMPlanck", lambda: P.planck_mass(), 4,
              r"m_P = \sqrt{\hbar c/G}, in kg",
              "instruments/paper_vii_b/planck_scale_values.py::planck_mass",
              r"2.176\times10^{-8}"),
        Value("ssvGNewton", lambda: P.G_NEWTON, 3,
              r"G (CODATA-2018), in m^3 kg^-1 s^-2 — a conceded input, not derived",
              "instruments/paper_vii_b/planck_scale_values.py::G_NEWTON",
              r"6.67\times10^{-11}"),
    ]


def _ssv_vi() -> list[Value]:
    """#203.  The B1 falsbox printed its shortfall three times -- falsbox,
    figure caption, claim-status table -- none of them generated, so a
    recomputation moved the instrument and left all three false.  That is how
    #203 was found: by eye, off the figure, not by any gate."""
    import dsph_ledger as D
    S = "instruments/paper_vi/dsph_ledger.py::summary"

    # Uncached, like the SSV-VI claims: summary() costs 2.3 ms, and a shared
    # cache would let a --check run compare the receipt against one stale
    # snapshot instead of against the instruments.
    def get(key):
        return lambda: D.summary()[key]

    return [
        Value("ssvDsphMedianDeltaB", get("median_delta_B_dex"), 3,
              r"median $\log_{10}(v_h^{\rm obs}/v_h^{\rm B})$ over the 8 dSphs",
              S, "2.7"),
        Value("ssvDsphShortfallFactor", get("shortfall_factor"), 2,
              r"model-B shortfall as a factor, $10^{\rm median\ dB}$",
              S, r"\sim 500"),
        Value("ssvDsphMedianDeltaA", get("median_delta_A_dex"), 2,
              r"median offset of the dwarfs from the mass law, dex",
              S, ""),      # 0.20 recurs in unrelated prose; not literal-checked
        # The per-dwarf minimum (~8e-3 dex) is deliberately NOT a macro: a
        # sig-fig formatter renders it 8\times10^{-3}, which reads badly inside
        # a printed range, and it carries no weight of its own.  The claim
        # predicate still bounds it, so it stays honest without being printed.
        Value("ssvDsphDeltaAMax", get("delta_A_max_dex"), 2,
              r"largest per-dwarf offset from the mass law, dex", S, ""),
        Value("ssvDsphSweepPoints", get("n_sweep_points"), 2,
              r"pre-registered robustness sweep grid size",
              # "27" alone would match any 27 anywhere in the prose; the
              # literal that mattered is the phrase it appeared in.
              S, "27 combinations"),
        Value("ssvDsphSweepDisagreeing", get("n_sweep_disagreeing"), 1,
              r"sweep points where B1 is not falsified (fragility, \#203)",
              S, ""),
        Value("ssvDsphMarginDex", get("within_limit_margin_dex"), 2,
              r"margin above the 1.5 dex B1 threshold within $v_{\rm rot} "
              r"\leq 3$ km/s", S, ""),
        Value("ssvDsphBudgetRatio", get("min_budget_ratio"), 2,
              r"smallest $\Gamma_{\rm bar}/\Gamma_{\rm req}$ over the dwarfs",
              S, ""),
        Value("ssvDsphVrotNeededMin", get("vrot_needed_min_kms"), 2,
              r"least rotation any dwarf would need for model B to reach its "
              r"observed $v_h$, km/s", S, ""),
        Value("ssvDsphVrotNeededMax", get("vrot_needed_max_kms"), 2,
              r"most rotation any dwarf would need, km/s", S, ""),
    ]


# Lazy: the loaders import instrument modules, so nothing is imported unless a
# paper is actually computed or checked.  Rendering never triggers them.
REGISTRY: dict[str, Callable[[], list[Value]]] = {
    "SSV-I": _ssv_i,
    "SSV-VI": _ssv_vi,
    "SSV-VII-b": _ssv_vii_b,
}


def values_for(paper: str) -> list[Value]:
    if paper not in REGISTRY:
        raise KeyError(f"{paper} has no registered values")
    return REGISTRY[paper]()


# --------------------------------------------------------------------------
# Formatting
# --------------------------------------------------------------------------

def fmt(x, sig: int) -> str:
    """Render ``x`` to ``sig`` significant figures as LaTeX maths.

    Plain decimal for exponents in [-2, 3]; ``m\\times10^{e}`` otherwise.  The
    mantissa keeps exactly ``sig`` significant figures — no trailing-zero
    stripping, which would silently drop a figure (``5.20`` -> ``5.2``).
    """
    x = float(x)
    if x == 0:
        return "0"
    exp = math.floor(math.log10(abs(x)))
    mant = round(x / 10.0**exp, sig - 1)
    if abs(mant) >= 10:            # rounding carried, e.g. 9.996 -> 10.0
        mant /= 10.0
        exp += 1
    if -2 <= exp <= 3:
        return f"{x:.{max(0, sig - 1 - exp)}f}"
    return f"{mant:.{sig - 1}f}" + r"\times10^{" + str(exp) + "}"


# --------------------------------------------------------------------------
# Receipt — the result of the last run
# --------------------------------------------------------------------------

def receipt_path(paper: str) -> Path:
    return PAPERS / paper / "results" / "values_receipt.json"


def values_path(paper: str) -> Path:
    return PAPERS / paper / "values.tex"


def source_fingerprint(source: str) -> str:
    """First 16 hex of the SHA-256 of the instrument file backing a value.

    Provenance, and a cheap staleness signal: if this no longer matches the file
    on disk, the instrument has changed since the receipt was written and the
    receipt should be recomputed.  It is deliberately whole-file, so it is
    *over*-sensitive — a docstring edit trips it.  That is the safe direction:
    re-blessing is one command, and a missed change is a wrong number in print.
    """
    path = REPO_ROOT / source.split("::")[0]
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def compute_receipt(paper: str) -> dict:
    """Run the paper's instruments and build the receipt body."""
    entries = {}
    for v in values_for(paper):
        value = float(v.compute())
        entries[v.macro] = {
            "value": value,
            "sig": v.sig,
            "rendered": fmt(value, v.sig),
            "describes": v.describes,
            "source": v.source,
            "source_sha256_16": source_fingerprint(v.source),
            "was": v.was,
        }
    return {
        "issue": 198,
        "paper": paper,
        "hypothesis": "every load-bearing number this paper prints is computed "
                      "by a named instrument, not typed by hand (#198 Part A)",
        "generator": "instruments/tools/gen_values.py",
        "computed_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "values": entries,
    }


def read_receipt(paper: str) -> dict:
    path = receipt_path(paper)
    if not path.is_file():
        raise FileNotFoundError(
            f"{path.relative_to(REPO_ROOT).as_posix()} missing — run "
            f"`python instruments/tools/gen_values.py --compute {paper}`")
    return json.loads(path.read_text(encoding="utf-8"))


def write_receipt(paper: str, receipt: dict) -> None:
    path = receipt_path(paper)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


def receipt_drift(paper: str) -> dict[str, dict]:
    """Re-run the instruments and compare against the recorded last run.

    Returns ``{macro: {"receipt": ..., "now": ...}}`` for every value that
    moved — empty when the receipt still describes what the code produces.
    This is what makes the recorded result checkable rather than merely trusted.
    """
    old = read_receipt(paper)["values"]
    new = compute_receipt(paper)["values"]
    drift = {}
    for macro in sorted(set(old) | set(new)):
        a, b = old.get(macro), new.get(macro)
        if a is None or b is None:
            drift[macro] = {"receipt": a, "now": b}
            continue
        # the rendered string is what reaches the paper, so it is the sharp test;
        # the fingerprint catches an instrument edit that has not moved a value
        if (a["rendered"] != b["rendered"]
                or a["source_sha256_16"] != b["source_sha256_16"]):
            drift[macro] = {"receipt": a, "now": b}
    return drift


# --------------------------------------------------------------------------
# Rendering — reads the receipt only, imports nothing
# --------------------------------------------------------------------------

def render(paper: str, receipt: dict) -> str:
    lines = [
        "% Auto-generated by instruments/tools/gen_values.py — do not edit by hand.",
        f"% Regenerate: python instruments/tools/gen_values.py {paper}",
        "%",
        "% Every macro below is COMPUTED by the named instrument, not typed.  A",
        "% number printed in this paper cannot drift from the code that derives it,",
        "% because there is only one of it.  (#198 Part A)",
        "%",
        f"% Rendered from results/values_receipt.json — the recorded result of the",
        f"% last instrument run.  Re-run the physics with --compute; verify the",
        f"% recorded result against the instruments with --check.",
        "",
    ]
    for macro, e in receipt["values"].items():
        lines += [
            f"% {e['describes']}",
            f"%   {e['source']}",
            f"\\newcommand{{\\{macro}}}{{{e['rendered']}}}",
            "",
        ]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def generate(paper: str) -> dict:
    """Write ``papers/<PAPER>/values.tex`` from the receipt."""
    receipt = read_receipt(paper)
    fresh = render(paper, receipt)
    path = values_path(paper)
    current = path.read_text(encoding="utf-8") if path.is_file() else None
    path.write_text(fresh, encoding="utf-8")
    return {"paper": paper, "path": path, "changed": current != fresh,
            "n": len(receipt["values"])}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paper", nargs="?", help="paper dir name, e.g. SSV-I")
    ap.add_argument("--all", action="store_true", help="every registered paper")
    ap.add_argument("--compute", action="store_true",
                    help="run the instruments and rewrite the receipt")
    ap.add_argument("--check", action="store_true",
                    help="re-run the instruments and compare against the receipt, "
                         "and confirm values.tex matches it; write nothing "
                         "(exit 1 on any drift)")
    args = ap.parse_args()

    if args.all:
        papers = sorted(REGISTRY)
    elif args.paper:
        papers = [args.paper]
    else:
        ap.error("give a paper name or --all")

    bad = False
    for paper in papers:
        if args.check:
            drift = receipt_drift(paper)
            stale_tex = (values_path(paper).read_text(encoding="utf-8")
                         if values_path(paper).is_file() else None
                         ) != render(paper, read_receipt(paper))
            tag = "STALE" if (drift or stale_tex) else "ok   "
            print(f"{tag} {paper}: receipt drift {sorted(drift) or 'none'}; "
                  f"values.tex {'STALE' if stale_tex else 'current'}")
            bad |= bool(drift) or stale_tex
        elif args.compute:
            r = compute_receipt(paper)
            write_receipt(paper, r)
            print(f"computed {paper}: {len(r['values'])} values -> "
                  f"{receipt_path(paper).relative_to(REPO_ROOT).as_posix()}")
        else:
            r = generate(paper)
            print(f"wrote {paper}: {r['n']} values -> "
                  f"{r['path'].relative_to(REPO_ROOT).as_posix()}"
                  f"{'' if r['changed'] else ' (unchanged)'}")
    if bad:
        print("\nERROR: recompute with --compute, then regenerate values.tex.")
        sys.exit(1)


if __name__ == "__main__":
    main()

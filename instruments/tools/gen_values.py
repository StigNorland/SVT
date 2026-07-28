"""Generate the printed-value macros for SSV papers (#198 Part A).

The problem this closes: a number printed in a paper and the instrument that
derives it were two independent objects.  ``eq:rho0-value``'s
:math:`9.96\\times10^{-5}` was typed into the ``.tex`` by hand, and the only
thing keeping it equal to what ``instruments/paper_i/ssv_i_audit_2026.py``
produces was care at the time of writing.  Nothing detected drift — which is how
the original defect survived: ``rho_0`` was printed as :math:`1.9` alongside a
formula yielding :math:`0.0078`, and the two disagreed in print for years.

The fix reuses the pattern rule 11 already establishes for citations.
``gen_provenance.py`` generates ``provenance.tex``, the paper ``\\input``\\ s it,
and a test validates it.  This does the same for values:

  * the registry below names, for each macro, the instrument function that
    computes it — so a reader goes macro -> function -> test in two hops;
  * ``papers/<PAPER>/values.tex`` is written from that registry;
  * the paper writes ``\\ssvRhoZero`` rather than a literal;
  * ``instruments/test/tools/test_gen_values.py`` asserts there is no drift,
    no dead macro, no undeclared macro, and — the test that actually bites —
    that the old literal no longer appears in the ``.tex``.

Then a printed number *cannot* drift from its instrument, because there is only
one of it.

Macro namespace: ``\\ssv<CamelCase>``.  Deliberately disjoint from the existing
``\\ssvissue`` / ``\\ssvfile`` cross-ref macros (lower-case after ``ssv``), so
the regex ``\\\\ssv[A-Z][A-Za-z]*`` matches generated values and nothing else.

Scope is deliberately narrow — the load-bearing numbers touched by #182 — not
every number in the series.  The goal is that *derived* numbers are generated,
not that prose becomes unwritable.

Usage:
    python instruments/tools/gen_values.py SSV-I         # one paper
    python instruments/tools/gen_values.py --all         # every registered paper
    python instruments/tools/gen_values.py --all --check # report drift, write nothing
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
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
# Registry
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


# Lazy: the loaders import instrument modules, so nothing is imported until a
# paper is actually generated or tested.
REGISTRY: dict[str, Callable[[], list[Value]]] = {
    "SSV-I": _ssv_i,
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
# Rendering
# --------------------------------------------------------------------------

def render(paper: str, values: list[Value]) -> str:
    lines = [
        "% Auto-generated by instruments/tools/gen_values.py — do not edit by hand.",
        f"% Regenerate: python instruments/tools/gen_values.py {paper}",
        "%",
        "% Every macro below is COMPUTED by the named instrument, not typed.  A",
        "% number printed in this paper cannot drift from the code that derives it,",
        "% because there is only one of it.  (#198 Part A)",
        "",
    ]
    for v in values:
        lines += [
            f"% {v.describes}",
            f"%   {v.source}",
            f"\\newcommand{{\\{v.macro}}}{{{fmt(v.compute(), v.sig)}}}",
            "",
        ]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def values_path(paper: str) -> Path:
    return PAPERS / paper / "values.tex"


def generate(paper: str, check: bool) -> dict:
    """Write (or, with ``check``, only compare) ``papers/<PAPER>/values.tex``."""
    fresh = render(paper, values_for(paper))
    path = values_path(paper)
    current = path.read_text(encoding="utf-8") if path.is_file() else None
    drifted = current != fresh
    if not check:
        path.write_text(fresh, encoding="utf-8")
    return {"paper": paper, "path": path, "drifted": drifted,
            "existed": current is not None, "n": len(values_for(paper))}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paper", nargs="?", help="paper dir name, e.g. SSV-I")
    ap.add_argument("--all", action="store_true", help="every registered paper")
    ap.add_argument("--check", action="store_true",
                    help="report drift, write nothing (exit 1 if any file is stale)")
    args = ap.parse_args()

    if args.all:
        papers = sorted(REGISTRY)
    elif args.paper:
        papers = [args.paper]
    else:
        ap.error("give a paper name or --all")

    stale = False
    for paper in papers:
        r = generate(paper, args.check)
        if args.check:
            tag = "STALE" if r["drifted"] else "ok   "
        else:
            tag = "wrote"
        print(f"{tag} {paper}: {r['n']} values -> "
              f"{r['path'].relative_to(REPO_ROOT).as_posix()}")
        stale |= args.check and r["drifted"]
    if stale:
        print("\nERROR: values.tex is out of date with its instruments — regenerate.")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""Drift guards for statements that ride on a generated number (#198 Part D).

A generated number closes half the defect. The other half is the prose around it.

    "This is *not* the classical electron radius, which is smaller by a factor
     alpha^2"                                       -- SSV-I main.tex:537
    "smaller by ~2x10^4"                            -- SSV-I main.tex:1639
    "the entropy would double"                      -- SSV-VII-b main.tex:401

Each is a relationship that was reviewed when written. Under #198 Part A the
value can no longer drift from its instrument — but the instrument and receipt
can move legitimately later, leaving that previously reviewed relationship
false. Without this gate the paper would rebuild cleanly and the number would
agree with the code.

The gap was not hypothetical. When this module was written, SSV-I printed
``R_e^* = a_0/sqrt2 ~ 3.74e-11`` while the test that appeared to guard it,
``test_e4_xi_over_alpha_is_the_bohr_radius``, asserted the *uncorrected*
``xi/alpha = a_0 = 5.29e-11``. The printed claim was true and guarded by nothing;
the guard that looked like its guard checked a different quantity.

So each claim is registered here with a stable LaTeX anchor, its site, the
macros it depends on, and a predicate. When a value moves and the registered
relationship stops holding, a named test fails and quotes the affected sentence.
If the sentence itself changes, the anchor requires its guard to be reviewed and
updated rather than silently becoming detached.

Registered under ``instruments/test/tools/test_claims.py`` and enforced at build
time by ``instruments/tools/build_paper.py`` — a paper whose claims do not hold
does not compile.

Limits, stated because they matter:
  * this is a drift detector, not an authoring-time semantic review. It cannot
    decide whether the conclusion and predicate were correct when first written;
    independent "third eye" review is a future +2-agent-harness improvement;
  * a claim is only as good as its predicate. A predicate that restates the
    computation instead of the *conclusion* guards nothing — see
    ``test_claims_are_not_tautologies``;
  * this registry is hand-built, so a sentence nobody registered is unguarded.
    ``test_every_generated_value_is_claimed`` catches the subset that hangs off a
    generated number; the rest of the prose is not covered and is not pretended
    to be.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTRUMENTS = REPO_ROOT / "instruments"

for _d in [INSTRUMENTS, *sorted(INSTRUMENTS.glob("paper_*"))]:
    if _d.is_dir() and str(_d) not in sys.path:
        sys.path.insert(0, str(_d))


@dataclass(frozen=True)
class Claim:
    """One conclusion the paper draws from a value.

    ``site``        ``papers/<PAPER>/main.tex:<line>`` — where the sentence is
    ``asserts``     the sentence, close enough to find it by search
    ``depends_on``  generated macros the conclusion rests on
    ``check``       predicate returning True while the conclusion holds
    ``tolerance``   how the predicate treats "approximately", in words
    ``source_anchor`` exact LaTeX fragment that binds this guard to the paper
    """

    paper: str
    key: str
    site: str
    asserts: str
    depends_on: tuple[str, ...]
    check: Callable[[], bool]
    tolerance: str = ""
    note: str = ""
    source_anchor: str = ""


def _rel(a, b) -> float:
    return abs(float(a) / float(b) - 1)


# --------------------------------------------------------------------------
# SSV-I
# --------------------------------------------------------------------------

def _ssv_i() -> list[Claim]:
    import mpmath as mp
    import ssv_i_audit_2026 as A

    # the paper prints the sqrt2-CORRECTED value; every claim below is stated
    # about that quantity, not about the uncorrected one
    Re = lambda: A.xi_over_alpha(sqrt2_corrected=True)

    return [
        Claim(
            "SSV-I", "Re-is-bohr-over-root2", "papers/SSV-I/main.tex:541",
            "R_e^* = a_0/sqrt2  (the combination hbar/(alpha m_e c) is the Bohr radius)",
            ("ssvReStar",),
            lambda: _rel(Re(), A.A_BOHR / mp.sqrt(2)) < 1e-9,
            tolerance="relative 1e-9",
            note="THE claim that was unguarded when this module was written: the "
                 "existing E4 test asserts the UNCORRECTED xi/alpha = a_0, which "
                 "is a different number from the one the paper prints.",
            source_anchor=(
                r"corrected healing length $R_e^* = a_0/\sqrt2 "
                r"\approx \ssvReStar$~m."
            ),
        ),
        Claim(
            "SSV-I", "Re-is-not-classical-electron-radius", "papers/SSV-I/main.tex:537",
            "R_e^* is NOT the classical electron radius r_e, which is smaller by alpha^2",
            ("ssvReStar",),
            lambda: _rel(Re() / A.R_E_CLASSICAL, 1 / (A.ALPHA**2 * mp.sqrt(2))) < 1e-6,
            tolerance="relative 1e-6 on the ratio",
            note="the sqrt2 enters because the printed R_e^* is the corrected one; "
                 "the paper's 'factor alpha^2' is the uncorrected statement.",
            source_anchor=(
                r"$r_e = \alpha\hbar/(m_ec)$, which is smaller by a factor "
                r"$\alpha^2$;"
            ),
        ),
        Claim(
            "SSV-I", "rho0-smaller-by-2e4", "papers/SSV-I/main.tex:1647",
            "the corrected rho_0 is smaller than the retired 1.9 by ~2x10^4",
            ("ssvRhoZero",),
            lambda: 1.5e4 < float(A.rho0_asserted_value()
                                  / A.rho0_natural_units(sqrt2_corrected=True)) < 2.5e4,
            tolerance="the printed '~2x10^4' read as one significant figure",
            note="guards the claim-status table entry, which is the paper's own "
                 "record of the #183 correction.",
            source_anchor=(
                r"$\approx\ssvRhoZero\,m_e^4c^3/\hbar^3$, smaller by "
                r"$\sim2\times10^4$."
            ),
        ),
        Claim(
            "SSV-I", "lambda-enters-denominator", "papers/SSV-I/main.tex:562",
            "Lambda appears in the DENOMINATOR of rho_0 (the retired form had it on top)",
            ("ssvLambda", "ssvRhoZero"),
            # retired: 2 alpha Lambda/pi^2      correct: sqrt2 alpha/(2 pi^2 Lambda)
            # so correct/retired = sqrt2/(4 Lambda^2).  The Lambda EXPONENT differs
            # by 2, which is exactly the "numerator -> denominator" move; a
            # predicate that only compared magnitudes would not distinguish it
            # from any other factor.
            lambda: _rel(A.rho0_natural_units(sqrt2_corrected=True)
                         / A.rho0_as_printed(),
                         mp.sqrt(2) / (4 * A.lambda_param()**2)) < 1e-9,
            tolerance="relative 1e-9",
            note="first draft of this predicate was a tautology that restated the "
                 "computation instead of the conclusion; it passed while guarding "
                 "nothing. Replaced, and test_claims_are_not_tautologies now "
                 "checks every predicate actually depends on its inputs.",
            source_anchor=(
                r"\rho_0 = \frac{\sqrt{2}\,\alpha\,m_e^4c^3}"
                r"{2\pi^2\Lambda\,\hbar^3}"
            ),
        ),
        Claim(
            "SSV-I", "r-star-is-one-over-alpha", "papers/SSV-I/main.tex:530",
            "the stationary point sits at r* = 1/alpha, i.e. 1/alpha healing lengths",
            ("ssvLambda",),
            lambda: _rel(A.stationary_radius(A.lambda_param() + 1), 1 / A.ALPHA) < 1e-3,
            tolerance="relative 1e-3; the neglected 2C/r*^2 term is O(alpha^2)",
            source_anchor=r"an equilibrium radius $1/\alpha$ healing lengths across",
        ),
    ]


# --------------------------------------------------------------------------
# SSV-VII-b
# --------------------------------------------------------------------------

def _ssv_vii_b() -> list[Claim]:
    import mpmath as mp
    import planck_scale_values as P

    return [
        Claim(
            "SSV-VII-b", "xi-is-ell-P-unchanged", "papers/SSV-VII-b/main.tex:391",
            "xi = ell_P is UNCHANGED by the D1 sqrt2 correction",
            ("ssvEllP",),
            P.xi_equals_planck_length,
            tolerance="relative 1e-25",
            source_anchor=r"\xi = \ell_P = \ssvEllP\ \text{m}",
        ),
        Claim(
            "SSV-VII-b", "m0-is-mP-over-root2", "papers/SSV-VII-b/main.tex:396",
            "what moves is the mass: m_0 = m_P/sqrt2, not m_0 = m_P",
            ("ssvMZero", "ssvMPlanck"),
            lambda: _rel(P.correction_factor(), mp.sqrt(2)) < 1e-20,
            tolerance="relative 1e-20 — the claim is exactness, not approximation",
            source_anchor=r"\frac{m_P}{\sqrt2} \;\approx\; \ssvMZero\ \text{kg}",
        ),
        Claim(
            "SSV-VII-b", "entropy-would-double", "papers/SSV-VII-b/main.tex:401",
            "at fixed m_0 and horizon area the entropy would DOUBLE (factor 2, not sqrt2)",
            ("ssvEllP", "ssvMZero"),
            lambda: _rel(P.healing_length(P.fundamental_mass(),
                                          sqrt2_corrected=False)**2
                         / P.planck_length()**2, 2) < 1e-20,
            tolerance="relative 1e-20",
            note="entropy counts one dof per xi^2, so the sqrt2 in xi becomes a "
                 "factor 2 in the count. This is the arithmetic the sentence "
                 "asserts, and it is not the same statement as m_P/m_0 = sqrt2.",
            source_anchor=(
                r"entropy~\eqref{eq:BH_entropy} would \emph{double};"
            ),
        ),
        Claim(
            "SSV-VII-b", "G-reproduced-from-ell-P", "papers/SSV-VII-b/main.tex:381",
            "inserting xi = ell_P into G = c^3 xi^2/hbar reproduces G ~ 6.67e-11",
            ("ssvEllP", "ssvGNewton"),
            lambda: _rel(P.C**3 * P.planck_length()**2 / P.HBAR, P.G_NEWTON) < 1e-20,
            tolerance="relative 1e-20 — an identity, since ell_P is defined from G",
            note="deliberately labelled: this is a CONSISTENCY identity, not a "
                 "derivation of G. G is a conceded input (#155).",
            source_anchor=r"$G\approx \ssvGNewton$~m$^3$\,kg$^{-1}$\,s$^{-2}$.",
        ),
    ]


REGISTRY: dict[str, Callable[[], list[Claim]]] = {
    "SSV-I": _ssv_i,
    "SSV-VII-b": _ssv_vii_b,
}


def claims_for(paper: str) -> list[Claim]:
    return REGISTRY[paper]() if paper in REGISTRY else []


def _normalise_source(text: str) -> str:
    """Ignore LaTeX line wrapping while keeping the registered wording exact."""
    return re.sub(r"\s+", " ", text).strip()


def source_drift(paper: str) -> list[Claim]:
    """Claims whose registered LaTeX statement moved or changed.

    This binds a predicate to the statement it was written to guard. It does not
    certify that the statement was correct when authored; that remains a review
    responsibility.
    """
    out = []
    for c in claims_for(paper):
        source_path = REPO_ROOT / c.site.rsplit(":", 1)[0]
        try:
            source = _normalise_source(source_path.read_text(encoding="utf-8"))
        except OSError:
            out.append(c)
            continue
        if not c.source_anchor or _normalise_source(c.source_anchor) not in source:
            out.append(c)
    return out


def failing(paper: str) -> list[Claim]:
    """Claims whose predicate no longer holds. Empty is the healthy result."""
    out = []
    for c in claims_for(paper):
        try:
            ok = bool(c.check())
        except Exception:
            ok = False
        if not ok:
            out.append(c)
    return out


def report(paper: str) -> str:
    lines = [f"{paper}: {len(claims_for(paper))} registered claims"]
    for c in claims_for(paper):
        try:
            ok = bool(c.check())
        except Exception as exc:      # a predicate that blows up is a failure
            ok, extra = False, f"  ({type(exc).__name__})"
        else:
            extra = ""
        lines.append(f"  {'ok  ' if ok else 'FAIL'} {c.key:34s} {c.site}{extra}")
        if not ok:
            lines.append(f"       asserts: {c.asserts}")
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover
    bad = 0
    for paper in sorted(REGISTRY):
        print(report(paper))
        bad += len(failing(paper))
    if bad:
        print(f"\n{bad} claim(s) no longer follow from their values.")
        sys.exit(1)

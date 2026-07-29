"""Typed symbol tables and dimensional homogeneity for the SSV series (#198 Part B).

Three defects found in a single #182 pass were the same kind of error, and none
was caught by the C/E/N gates:

    SSV-I  (E6)   ``b``  eq:pot needed [V]/[rho]; eq:cs and eq:xi needed an extra L^3
    SSV-II (E3b)  ``e``  a dimensionless Berry phase requires a MASS;
                         Phi_0 = h/e uses a CHARGE
    SSV-V  (E2)   ``b``  a FREQUENCY here; an energy-per-mass in Paper I

The gates checked equations, and even checked *products*, but never asked
**"does this symbol mean one thing throughout?"**  Two of the three surfaced
during the rewrite rather than the audit, so a clean gate report would have
shipped with them intact.  Issue #216 repairs SSV-I in print; the retired
relations remain as explicit negative controls.

The question this module asks
-----------------------------
Symbols come in two kinds.  **Anchored** symbols have a dimension fixed by
definition outside the relation under test — ``hbar`` is an action, ``c`` a
velocity, ``rho`` a mass density.  **Free** symbols are the ones a paper
introduces without pinning independently: SSV-I's ``b``, SSV-II's ``e``.

    Is there ANY dimension for the free symbols that makes all of the paper's
    printed relations simultaneously homogeneous?

When there is not, the defect is established without having to argue about which
equation is "the wrong one" — and because the free symbol is the only unknown,
attribution is automatic rather than a judgement call.  This matters: an earlier
draft of this module reported ``hbar``, ``m_0`` and ``kappa_0`` as overloaded
too, purely because they appear inside relations broken by a *different* symbol.
Solving a broken relation for a healthy symbol yields nonsense, and reporting
that nonsense as a finding would have been false.

What this module does NOT do
----------------------------
It does not parse LaTeX.  It checks the relations **as transcribed here**, so it
proves the intended dimensions are consistent, not that ``main.tex`` matches
them.  A relation mis-transcribed into this file is invisible to it.  That is the
honest limit of the "80% version", and it is why each relation carries the
``site`` it came from: the transcription is checkable by hand even though it is
not checked by machine.

Scope is SSV-I, SSV-II, SSV-V and SSV-VII-a — the papers where a dimensional
defect was actually found, plus VII-a which #189 brought in.  Transcribing all
twelve by hand would be a large manual operation with a real chance of
introducing the very error class this exists to catch; that trade is not worth
taking, and #205 is the proposal to do it properly rather than by hand.

Adding VII-a produced a finding no per-paper check could reach: ``b`` is
declared J/kg in SSV-I, a frequency in SSV-V, and required to be an energy in
SSV-VII-a — three dimensions for one letter, each self-consistent inside its
own paper.  See ``declared_across_papers``.

Mirrored by ``instruments/test/tools/test_dimensions.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from sympy import Rational
from sympy.physics.units import Dimension
from sympy.physics.units.definitions.dimension_definitions import (
    charge, length, mass, time)
from sympy.physics.units.systems.si import dimsys_SI

# --------------------------------------------------------------------------
# base dimensions
# --------------------------------------------------------------------------

ONE = Dimension(1)
VELOCITY = length / time
ACTION = mass * length**2 / time                 # [h] = [hbar];  NOT an energy
ENERGY = mass * length**2 / time**2
ENERGY_DENSITY = ENERGY / length**3
MASS_DENSITY = mass / length**3
FREQUENCY = 1 / time
MAGNETIC_FLUX = ENERGY * time / charge           # Wb = J s / C


def dims(expr) -> dict:
    """Dimensional dependencies under the SI system's own normalisation."""
    return dict(dimsys_SI.get_dimensional_dependencies(expr))


def is_dimensionless(expr) -> bool:
    return dims(expr) == {}


def _key(d: dict) -> tuple:
    """Hashable, comparable form of a dimension-dependency dict."""
    return tuple(sorted((str(k), v) for k, v in d.items()))


# --------------------------------------------------------------------------
# symbol tables
# --------------------------------------------------------------------------
# ANCHORED: dimension fixed by definition, independently of the relations below.
# FREE:     dimension the paper never pins independently — the unknowns.

ANCHORED: dict[str, dict[str, Dimension]] = {
    "SSV-I": {
        # rho and rho_0 are ONE symbol here: rho_0 is the value of rho at
        # saturation, so they cannot carry different dimensions.  Splitting them
        # would let the system absorb the E6 mismatch and hide the defect.
        "rho": MASS_DENSITY,
        "m_0": mass,
        "hbar": ACTION,
        "c": VELOCITY,
        "xi": length,
        "kappa_0": ACTION / mass,                # kappa_0 = h/m_0, circulation
    },
    "SSV-II": {
        "hbar": ACTION,
        "kappa_0": ACTION / mass,
        "m_0": mass,
        "c_perp": VELOCITY,
        "rho_perp": MASS_DENSITY,                # rho_perp = alpha rho_0
        "Phi_B": MAGNETIC_FLUX,
    },
    "SSV-V": {
        "hbar": ACTION,
        "m": mass,
        "rho": MASS_DENSITY,
    },
    # Added by #213 Part A: the cross-paper symbol census flagged Lambda as
    # carrying three dimensions across the series, which sent the checker at
    # this paper's cosmological-constant relation for the first time.
    "SSV-VII-b": {
        "hbar": ACTION,
        "c": VELOCITY,
        "G": length**3 / (mass * time**2),
        "rho": MASS_DENSITY,                     # rho_0, the saturation density
        "P": mass / (length * time**2),          # P_0, the saturation pressure
    },
    "SSV-VII-a": {
        "hbar": ACTION,
        "m": mass,
        "m_e": mass,
        "c": VELOCITY,
        "S": ACTION,                             # Psi = sqrt(rho) exp(iS/hbar)
        # rho is anchored to what eq:polar DECLARES it to be -- "the mass
        # density".  The Gausson section then uses it as a normalised
        # probability density, and that clash is the E5 defect: anchoring it
        # here is what lets the checker see the clash rather than absorb it.
        "rho": MASS_DENSITY,
    },
}

FREE: dict[str, set[str]] = {
    # SSV-VII-b introduces no unpinned symbol: every symbol in its Lambda
    # relation is fixed by definition elsewhere.  The empty set is a
    # declaration, not an omission — with nothing free, an inhomogeneous
    # relation cannot be repaired by any assignment, which is what makes the
    # #213-A1 defect unrepairable rather than merely unresolved.
    "SSV-VII-b": set(),
    "SSV-I": {"b"},
    "SSV-II": {"e"},
    "SSV-V": {"b"},
    "SSV-VII-a": {"b"},
}

# What each paper *declares* its free symbols to be, for comparison against what
# the relations actually require.  SSV-V's declaration is the #187 E2 repair.
DECLARED: dict[str, dict[str, Dimension]] = {
    "SSV-I": {"b": ENERGY / mass},               # J/kg, after the E6 correction
    "SSV-II": {"e": charge},                     # as used by Phi_0 = h/e
    "SSV-V": {"b": FREQUENCY},                   # declared at main.tex:146
    # VII-a never declares [b]; the LogSE fixes it, since b Psi ln(...) must
    # match i hbar d_t Psi.  Recorded as the requirement, not as a declaration.
    "SSV-VII-a": {"b": ENERGY},
}


# --------------------------------------------------------------------------
# relations
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Relation:
    """One relation a paper asserts, as a monomial in its symbols.

    ``powers``  symbol -> exponent, with the relation rearranged so the monomial
                equals ``target``.  E.g. ``c_s = sqrt(2 b rho_0/m_0)`` becomes
                ``{b: 1, rho: 1, m_0: -1}`` against ``VELOCITY**2``.
    ``status``  ``"homogeneous"``, or ``"inhomogeneous"`` for a relation recorded
                as a known defect or negative control.
    ``site``    where it was transcribed from, so the transcription this module
                cannot machine-check is at least checkable by hand.
    """

    paper: str
    label: str
    site: str
    powers: Mapping[str, int]
    target: Dimension
    note: str
    status: str = "homogeneous"
    defect: str = ""
    printed: bool = True     # False for historical negative controls


RELATIONS: list[Relation] = [
    # ---------------- SSV-I, corrected in print by #216 ----------------
    Relation("SSV-I", "eq:Lag-normalisation", "papers/SSV-I/main.tex",
             {"hbar": 1, "rho": 1, "m_0": -1}, ACTION / length**3,
             "n_0 hbar with n_0=rho_0/m_0 is an action density"),
    Relation("SSV-I", "eq:pot", "papers/SSV-I/main.tex:251",
             {"b": 1, "rho": 1}, ENERGY_DENSITY,
             "V(rho) = b rho [ln(rho/rhobar) - 1] + V_0 must be an energy density"),
    Relation("SSV-I", "eq:LogSE", "papers/SSV-I/main.tex",
             {"m_0": 1, "b": 1}, ENERGY,
             "the logarithmic wave-equation coefficient is m_0 b"),
    Relation("SSV-I", "eq:cs", "papers/SSV-I/main.tex",
             {"b": 1}, VELOCITY**2,
             "c_s^2 = dP/drho = rho dmu/drho = b exactly; no rho_0"),
    Relation("SSV-I", "eq:xi", "papers/SSV-I/main.tex",
             {"hbar": 2, "m_0": -2, "b": -1}, length**2,
             "xi = hbar/sqrt(2 m_0^2 b); the energy is m_0 b, not b rho_0"),
    # Historical negative controls: deliberately not printed.
    Relation("SSV-I", "control:retired-cs",
             "instruments/paper_i/ssv_i_audit_2026.py::b_dimension_from",
             {"b": 1, "rho": 1, "m_0": -1}, VELOCITY**2,
             "retired c_s^2=b rho_0/m_0 must remain inhomogeneous",
             status="inhomogeneous", defect="E6-control", printed=False),
    Relation("SSV-I", "control:retired-xi",
             "instruments/paper_i/ssv_i_audit_2026.py::b_dimension_from",
             {"hbar": 2, "m_0": -1, "b": -1, "rho": -1}, length**2,
             "retired xi^2=hbar^2/(2 m_0 b rho_0) must remain inhomogeneous",
             status="inhomogeneous", defect="E6-control", printed=False),

    # ---------------- SSV-II ----------------
    Relation("SSV-II", "eq:berry_ab", "papers/SSV-II/main.tex:823",
             {"e": 1, "hbar": -1, "kappa_0": 1}, ONE,
             "gamma = (e/hbar) n kappa_0 must be dimensionless",
             status="inhomogeneous", defect="E3b"),
    Relation("SSV-II", "eq:flux_quantum", "papers/SSV-II/main.tex:870",
             {"hbar": 1, "e": -1}, MAGNETIC_FLUX,
             "Phi_0 = h/e — standard, and homogeneous only if e is a CHARGE"),
    Relation("SSV-II", "eq:flux_quantisation", "papers/SSV-II/main.tex:870",
             {"c_perp": 1, "rho_perp": 1, "kappa_0": 1}, ACTION,
             "c_perp rho_perp kappa_0 was asserted to equal h — contains no free "
             "symbol, so no choice of [e] can repair it",
             status="inhomogeneous", defect="E3d"),

    # ---------------- SSV-V ----------------
    Relation("SSV-V", "eq:cs", "papers/SSV-V/main.tex:145",
             {"b": 1, "hbar": 1, "m": -1}, VELOCITY**2,
             "c_s = sqrt(b hbar/m) with b a frequency — declared at main.tex:146"),

    # ---------------- SSV-VII-a (#189) ----------------
    Relation("SSV-VII-a", "eq:velocity", "papers/SSV-VII-a/main.tex:140",
             {"S": 1, "m": -1}, length**2 / time,
             "v = grad S / m; the gradient's length is folded into the target"),
    Relation("SSV-VII-a", "eq:hamilton_jacobi", "papers/SSV-VII-a/main.tex:163",
             {"S": 2, "m": -1}, ENERGY * length**2,
             "(grad S)^2 / 2m must be an energy"),
    Relation("SSV-VII-a", "eq:Q", "papers/SSV-VII-a/main.tex:168",
             {"hbar": 2, "m": -1}, ENERGY * length**2,
             "Q = -hbar^2/(2m) lap(sqrt rho)/sqrt rho is an energy; rho cancels, "
             "which is why Q is blind to the E5 normalisation clash"),
    Relation("SSV-VII-a", "eq:phase_quantisation",
             "papers/SSV-VII-a/main.tex:282",
             {"S": 1}, ACTION,
             "contour integral of grad S equals 2 pi n hbar"),
    Relation("SSV-VII-a", "eq:circulation", "papers/SSV-VII-a/main.tex:287",
             {"hbar": 1, "m": -1}, length**2 / time,
             "quantum of circulation h/m"),
    Relation("SSV-VII-a", "eq:LogSE-VIIa", "papers/SSV-VII-a/main.tex:388",
             {"b": 1}, ENERGY,
             "b Psi ln(|Psi|^2/rho_0) must match i hbar d_t Psi — this is what "
             "fixes [b] = energy in THIS paper"),
    Relation("SSV-VII-a", "eq:gausson", "papers/SSV-VII-a/main.tex:399",
             {"hbar": 2, "m": -1, "b": -1}, length**2,
             "sigma^2 = hbar^2/(2 m b); homogeneous exactly when b is an energy"),
    Relation("SSV-VII-a", "eq:rydberg", "papers/SSV-VII-a/main.tex:258",
             {"m_e": 1, "c": 2}, ENERGY,
             "E_n = -m_e c^2 alpha^2 / 2n^2, with alpha dimensionless"),
    # The E5 defect, encoded AS PRINTED.
    Relation("SSV-VII-a", "eq:gausson-Dx", "papers/SSV-VII-a/main.tex:413",
             {"rho": 1}, 1 / length,
             "(Dx)^2 = int x^2 |Psi|^2 dx = sigma^2/2 requires |Psi|^2 to be a "
             "1D probability density, but eq:polar declares rho the MASS "
             "density — one symbol, two dimensions",
             status="inhomogeneous", defect="E5"),

    # ---------------- SSV-VII-b (#213 Part A) ----------------
    # Both forms are kept.  Recording the defective one as printed is what makes
    # this checker demonstrably able to catch the class, rather than merely
    # agreeing with corrected algebra — the same convention as SSV-I eq:cs.
    Relation("SSV-VII-b", "eq:Lambda-as-printed-pre-213",
             "papers/SSV-VII-b/main.tex:526",
             {"G": 1, "c": -4, "P": 1, "rho": -1}, 1 / length**2,
             "Lambda = (8 pi G/c^2)(P_0/rho_0 c^2) as printed before #213: the "
             "prefactor is missing rho_0, so the expression is L/M while the "
             "paper's own text quotes Lambda ~ 1e-52 m^-2",
             status="inhomogeneous", defect="#213-A1", printed=False),
    Relation("SSV-VII-b", "eq:Lambda", "papers/SSV-VII-b/main.tex:526",
             {"G": 1, "rho": 1, "c": -2}, 1 / length**2,
             "Lambda = (8 pi G rho_0/c^2)(P_0/rho_0 c^2) = 8 pi G P_0/c^4, the "
             "corrected form: a curvature, matching the quoted 1e-52 m^-2"),
]


def relations_for(paper: str, printed_only: bool = False) -> list[Relation]:
    return [r for r in RELATIONS
            if r.paper == paper and (r.printed or not printed_only)]


def _dimension_of(paper: str, symbol: str) -> Dimension:
    if symbol in ANCHORED[paper]:
        return ANCHORED[paper][symbol]
    return DECLARED[paper][symbol]


# --------------------------------------------------------------------------
# the checks
# --------------------------------------------------------------------------

def combination(rel: Relation) -> Dimension:
    """The monomial, evaluated with anchored + declared symbol dimensions."""
    out = ONE
    for sym, p in rel.powers.items():
        out *= _dimension_of(rel.paper, sym) ** p
    return out


def residual(rel: Relation) -> dict:
    """Dimensions of (monomial / target).  Empty exactly when homogeneous."""
    return dims(combination(rel) / rel.target)


def is_homogeneous(rel: Relation) -> bool:
    return residual(rel) == {}


def free_symbols_in(rel: Relation) -> set[str]:
    return set(rel.powers) & FREE[rel.paper]


def implied_dimension(rel: Relation, symbol: str) -> dict:
    """Solve the relation for one FREE symbol: the dimension it must carry for
    this relation to balance.

    Only meaningful when ``symbol`` is the relation's sole free symbol —
    otherwise the anchored values used for the rest are not all trustworthy and
    the result is noise.  Enforced, because reporting that noise as a finding is
    exactly the mistake this module was rewritten to avoid.
    """
    if symbol not in FREE[rel.paper]:
        raise ValueError(f"{symbol} is anchored in {rel.paper}; solving for it "
                         f"would report noise, not a defect")
    if free_symbols_in(rel) != {symbol}:
        raise ValueError(f"{rel.label} has free symbols {free_symbols_in(rel)}; "
                         f"cannot attribute to {symbol} alone")
    p = rel.powers[symbol]
    rest = ONE
    for sym, q in rel.powers.items():
        if sym != symbol:
            rest *= _dimension_of(rel.paper, sym) ** q
    return dims((rel.target / rest) ** Rational(1, p))


def requirements(paper: str, symbol: str, printed_only: bool = True
                 ) -> dict[str, dict]:
    """``{relation label: dimension this relation requires of ``symbol``}``."""
    return {r.label: implied_dimension(r, symbol)
            for r in relations_for(paper, printed_only)
            if symbol in r.powers}


def consistent_assignment(paper: str, symbol: str, printed_only: bool = True
                          ) -> dict | None:
    """The dimension satisfying every printed relation containing ``symbol``,
    or ``None`` when the relations demand two different things.

    ``None`` is the machine-checked form of "this symbol is overloaded": no
    choice of dimension makes the paper's printed equations simultaneously well
    formed.  It settles the defect without arguing which equation is wrong.
    """
    req = requirements(paper, symbol, printed_only)
    if not req:
        return None
    distinct = {_key(d) for d in req.values()}
    return next(iter(req.values())) if len(distinct) == 1 else None


def unrepairable(paper: str) -> list[Relation]:
    """Printed relations that are inhomogeneous and contain NO free symbol.

    No redefinition can rescue these — the defect is in the relation itself.
    SSV-II's eq:flux_quantisation is the example: it never mentions ``e``, so
    the argument about what ``e`` means cannot touch it.
    """
    return [r for r in relations_for(paper, printed_only=True)
            if not is_homogeneous(r) and not free_symbols_in(r)]


def check(paper: str) -> list[Relation]:
    """Relations whose actual homogeneity disagrees with their declared status.

    Empty is the healthy result.  A relation recorded as a known defect and still
    inhomogeneous does *not* appear here — it is doing its job.
    """
    return [r for r in relations_for(paper)
            if is_homogeneous(r) != (r.status == "homogeneous")]


def declared_across_papers(symbol: str) -> dict[str, dict]:
    """Papers declaring ``symbol``, and with what dimension.

    A difference is not automatically a defect — SSV-V's ``b`` legitimately
    differs from Paper I's — but it must be *declared*, which is #187 E2.
    """
    return {paper: dims(table[symbol])
            for paper, table in DECLARED.items() if symbol in table}


if __name__ == "__main__":  # pragma: no cover
    for paper in ANCHORED:
        print(f"\n=== {paper} ===")
        for r in relations_for(paper):
            mark = "ok  " if is_homogeneous(r) else "FAIL"
            tag = f"  [{r.defect} known]" if r.defect else ""
            src = "" if r.printed else "  (not in print)"
            print(f"  {mark} {r.label:22s} residual={residual(r) or '-'}{tag}{src}")
        for sym in sorted(FREE[paper]):
            req = requirements(paper, sym)
            print(f"  free '{sym}' must be:")
            for lab, d in req.items():
                print(f"      {lab:22s} -> {d}")
            ok = consistent_assignment(paper, sym)
            print(f"    consistent assignment: {ok if ok else 'NONE — overloaded'}")
        un = unrepairable(paper)
        if un:
            print(f"  unrepairable (no free symbol): {[r.label for r in un]}")
        print(f"  check() disagreements: {[r.label for r in check(paper)]}")
    print("\n'b' across papers:", declared_across_papers("b"))

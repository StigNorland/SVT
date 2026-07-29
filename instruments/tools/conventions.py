"""Programme-wide symbol conventions: one meaning, one dimension (#213 Part A, executes #205).

``dimensions.py`` asks whether a *paper's* printed relations can be
simultaneously homogeneous.  It covers four papers, and by construction it
cannot see the failure that matters most here: a symbol that is perfectly
consistent inside every paper it appears in, and means something different in
each.  ``b`` is the worked example — J/kg in SSV-I, a frequency in SSV-V, an
energy in SSV-VII-a, each self-consistent locally.

This module asks the other question:

    Does this letter mean one thing across the programme, and if a paper reuses
    it for something else, did the paper *say so*?

Two halves, deliberately separated
----------------------------------
**The census is machine-extracted.**  ``census()`` reads the maths out of every
``main.tex`` and reports which symbols occur where.  Nothing is transcribed by
hand, so the census cannot carry a transcription error.  It over-matches on
purpose (rule 13) — it will report ``d`` from ``\\mathrm{d}x`` and letters that
are really free indices — because the intended direction is to inspect the
excess rather than to trust a query that returned the expected answer.

**The declarations are hand-written.**  ``GLOBAL`` and ``LOCAL`` are the human
half, and they are where a mistake could hide.  ``dimensions.py`` warns that
transcribing twelve papers by hand risks introducing the very error class the
tool exists to catch; that warning applies here too, and the response is the
same one: every declaration carries the ``site`` it came from, so what cannot be
machine-checked is at least checkable by hand.

What is guarded, and what is not
--------------------------------
Guarded: a symbol carrying two declared meanings, or two declared dimensions,
across papers without a local declaration saying so.

**Not** guarded:
- A symbol nobody declared.  ``coverage()`` reports those rather than implying
  they are fine — a paper is not covered because some of its symbols are.
- Whether the paper's prose actually uses the symbol the way its declaration
  says.  Same limit rule 15 states: this checks the declarations, not the
  ``.tex``.
- Which of two conflicting uses is *correct*.  Drift guard, not referee.

Mirrored by ``instruments/test/tools/test_conventions.py``.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS = REPO_ROOT / "papers"


def paper_names() -> list[str]:
    return sorted(p.parent.name for p in PAPERS.glob("SSV-*/main.tex"))


# --------------------------------------------------------------------------
# The census — machine-extracted, over-matching on purpose
# --------------------------------------------------------------------------

#: Spans we treat as maths.  Display environments plus inline ``$...$``.
_MATH = re.compile(
    r"\$\$(.+?)\$\$"
    r"|\$(.+?)\$"
    r"|\\begin\{(?:equation|align|gather|eqnarray|multline)\*?\}(.+?)"
    r"\\end\{(?:equation|align|gather|eqnarray|multline)\*?\}",
    re.DOTALL)

#: A symbol: a Greek macro or a single Latin letter, with an optional subscript.
_SYMBOL = re.compile(
    r"\\(?P<greek>alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|"
    r"vartheta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|varphi|"
    r"chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega|"
    r"hbar|ell)(?![A-Za-z])"
    r"|(?<![A-Za-z\\])(?P<latin>[A-Za-z])(?![A-Za-z])")

#: Subscript immediately following a symbol: ``_e``, ``_{\rm grain}``, ``_{0}``.
_SUB = re.compile(r"\A_(?:\{(?P<braced>[^{}]*)\}|(?P<bare>[A-Za-z0-9]))")

#: Extraction noise we never want to report as a symbol.
#:
#: This list is deliberately *tiny*.  An over-eager filter here is the dangerous
#: kind of mistake: it removes a symbol from the census silently, so a genuine
#: collision is never reported and the tool looks clean.  An earlier draft
#: filtered ``c``, ``t`` and ``r`` as LaTeX column specifiers — which would have
#: hidden the speed of light, time and radius, three of the most heavily shared
#: symbols in the series.  ``_STRIP`` removes the constructs those letters
#: actually leak from, so the filter does not have to.
#:
#: ``d`` survives only as a differential once ``\mathrm{d}`` is stripped, and is
#: never a physical symbol in this series.
_NOISE = {"d"}

#: ``e`` is genuinely ambiguous between Euler's number and a physical symbol, and
#: SSV-II's #182 E3b defect was exactly an ``e`` carrying both a charge and a
#: dimensionless Berry phase.  It is therefore NOT filtered.
EULER_NOTE = ("e is not filtered: SSV-II's #182 E3b defect was an `e` carrying "
              "both a charge and a dimensionless Berry phase")

#: Column specifiers, macro fragments and TikZ keys share letters with symbols.
#: Rather than guess, strip the constructs before scanning.
_STRIP = (
    re.compile(r"\\(?:left|right|big|Big|bigg|Bigg)\b"),
    re.compile(r"\\(?:mathrm|mathbf|mathcal|mathbb|text|textrm|operatorname)"
               r"\s*\{[^{}]*\}"),
    re.compile(r"\\begin\{(?:tabular|array)\}\{[^{}]*\}"),
    re.compile(r"\\(?:label|ref|eqref|cite|ssvissue|ssvfile)\s*\{[^{}]*\}"),
    re.compile(r"\\[A-Za-z]+"),      # every remaining macro name
)


def _math_spans(text: str) -> list[str]:
    spans = []
    for m in _MATH.finditer(text):
        spans.append(next(g for g in m.groups() if g is not None))
    return spans


def _symbols_in(span: str) -> set[str]:
    """Symbol tokens in one maths span, subscripts kept."""
    found = set()
    # Find symbols BEFORE stripping macros, so Greek survives; then rescan the
    # stripped text for bare Latin letters, so macro names do not contribute.
    for m in _SYMBOL.finditer(span):
        name = m.group("greek")
        if not name:
            continue
        sub = _SUB.match(span[m.end():])
        found.add(_join(name, sub))
    bare = span
    for pat in _STRIP:
        bare = pat.sub(" ", bare)
    for m in _SYMBOL.finditer(bare):
        name = m.group("latin")
        if not name or name in _NOISE:
            continue
        sub = _SUB.match(bare[m.end():])
        found.add(_join(name, sub))
    return found


def _join(name: str, sub) -> str:
    if not sub:
        return name
    tail = sub.group("braced") if sub.group("braced") is not None else sub.group("bare")
    tail = re.sub(r"\\(?:rm|mathrm|text)\s*", "", tail or "").strip()
    return f"{name}_{tail}" if tail else name


def census() -> dict[str, set[str]]:
    """symbol -> set of papers it occurs in.  Machine-extracted, over-matching."""
    out: dict[str, set[str]] = defaultdict(set)
    for name in paper_names():
        text = (PAPERS / name / "main.tex").read_text(encoding="utf-8", errors="replace")
        for span in _math_spans(text):
            for sym in _symbols_in(span):
                out[sym].add(name)
    return dict(out)


def shared_symbols(min_papers: int = 2) -> dict[str, set[str]]:
    return {s: p for s, p in census().items() if len(p) >= min_papers}


# --------------------------------------------------------------------------
# The declarations — the hand-written half
# --------------------------------------------------------------------------
# Everything below is transcribed by a human and is therefore the part that can
# be wrong.  Each ``Use`` carries the ``site`` it came from so the transcription
# is checkable by hand, exactly as ``dimensions.py`` does.
#
# Scope is deliberately partial: the symbols verified against the papers in the
# #213 Part A pass, not all 145 shared tokens the census reports.  ``coverage()``
# reports the gap rather than letting silence imply completeness.

from sympy.physics.units import Dimension                       # noqa: E402
from sympy.physics.units.definitions.dimension_definitions import (  # noqa: E402
    charge, current, length, mass, temperature, time)
from sympy.physics.units.systems.si import dimsys_SI            # noqa: E402

ONE = Dimension(1)
VELOCITY = length / time
ACCELERATION = length / time**2
ACTION = mass * length**2 / time
ENERGY = mass * length**2 / time**2
PRESSURE = mass / (length * time**2)
MASS_DENSITY = mass / length**3
FREQUENCY = 1 / time
WAVENUMBER = 1 / length
CURVATURE = 1 / length**2
NEWTON_G = length**3 / (mass * time**2)
#: Entropy is an energy PER TEMPERATURE, not an energy.  Boltzmann fixes it:
#: S = k_B ln(Omega) with Omega a dimensionless microstate count, so [S] = [k_B]
#: exactly.  Writing this out because an earlier version of STANDARD below used
#: ``Dimension(1)`` as a placeholder for "a dimension I did not encode", which
#: renders as *dimensionless* and made this table assert that entropy is an
#: energy — a dimensional error inside the tool built to catch dimensional
#: errors.  ``test_no_placeholder_dimensions`` now forbids the shortcut.
BOLTZMANN = ENERGY / temperature
ENTROPY = BOLTZMANN
TEMPERATURE = temperature
SPECIFIC_HEAT = ENERGY / (mass * temperature)
ELECTRIC_POTENTIAL = ENERGY / charge
CONDUCTANCE = current**2 * time**3 / (mass * length**2)


@dataclass(frozen=True)
class Use:
    """What one paper means by one symbol.

    ``local`` non-empty declares a deliberate paper-local reuse, with the
    reason.  An undeclared disagreement is a finding; a declared one is a
    convention.  The distinction is the whole point: the programme cannot
    forbid reuse, it can only forbid *silent* reuse.
    """

    paper: str
    symbol: str
    means: str
    dim: Dimension | None      # None = notational, not a dimensioned quantity
    site: str
    local: str = ""
    notational: str = ""       # why this occurrence carries no dimension


#: The canonical programme-wide meaning, where one exists.
GLOBAL: dict[str, tuple[str, Dimension]] = {
    "hbar":    ("reduced Planck constant", ACTION),
    "c":       ("signal speed of the medium", VELOCITY),
    "alpha":   ("fine-structure constant", ONE),
    "xi":      ("healing length of the electron-scale defect", length),
    "rho_0":   ("saturation mass density of the vacuum", MASS_DENSITY),
    "m_e":     ("electron mass", mass),
    "m_p":     ("proton mass", mass),
    "m_0":     ("defect mass scale", mass),
    "G":       ("Newton's constant", NEWTON_G),
    "P_0":     ("saturation pressure", PRESSURE),
    "kappa_0": ("quantum of circulation, h/m_0", ACTION / mass),
    "H_0":     ("Hubble parameter", FREQUENCY),
}

#: Per-paper uses, transcribed and checked in the #213 Part A pass.
USES: list[Use] = [
    # ---- Lambda: three dimensions across the series, two inside SSV-III ----
    Use("SSV-I", "Lambda", r"\ln(8/\alpha) - 7/4, a pure number", ONE,
        "papers/SSV-I/main.tex:472"),
    Use("SSV-III", "Lambda", r"\Lambda(k\xi) = \ln(1/k\xi), a slow logarithm", ONE,
        "papers/SSV-III/main.tex:621"),
    Use("SSV-III", "Lambda", r"UV cutoff wavenumber, \Lambda = \xi^{-1}", WAVENUMBER,
        "papers/SSV-III/main.tex:997"),
    Use("SSV-VI", "Lambda", "cosmological constant", CURVATURE,
        "papers/SSV-VI/main.tex:570"),
    Use("SSV-VII-b", "Lambda", "cosmological constant", CURVATURE,
        "papers/SSV-VII-b/main.tex:526"),
    Use("SSV-VIII", "Lambda", "cosmological constant", CURVATURE,
        "papers/SSV-VIII/main.tex:242"),
    Use("SSV-IX", "Lambda", "cosmological constant", CURVATURE,
        "papers/SSV-IX/main.tex:226"),
    # The fourth meaning, and the one the first pass of this table MISSED:
    # bare \Lambda in the running-coupling form \ln(Q/\Lambda) is Lambda_QCD,
    # an energy.  The census reported \Lambda in 7 papers while the hand-written
    # half declared only 5 — the machine half caught the human half's omission,
    # which is why test_declared_symbol_is_declared_everywhere_it_occurs exists.
    Use("SSV-II", "Lambda", r"\Lambda_{\rm QCD} \approx 200 MeV, an energy scale",
        ENERGY, "papers/SSV-II/main.tex:1057"),

    # ---- a_0: Bohr radius vs the MOND acceleration scale ----
    Use("SSV-I", "a_0", "Bohr radius", length,
        "papers/SSV-I/main.tex:507"),
    Use("SSV-VI", "a_0", "MOND/RAR acceleration scale", ACCELERATION,
        "papers/SSV-VI/main.tex:553"),
    Use("SSV-IX", "a_0", "MOND/RAR acceleration scale", ACCELERATION,
        "papers/SSV-IX/main.tex:226"),

    # ---- b: the #189 finding, three dimensions, recorded here across papers ----
    Use("SSV-I", "b", "LogSE coupling, energy per unit mass", ENERGY / mass,
        "papers/SSV-I/main.tex:251"),
    Use("SSV-V", "b", "LogSE coupling, declared a frequency", FREQUENCY,
        "papers/SSV-V/main.tex:146"),
    Use("SSV-VII-a", "b", "LogSE coupling, required to be an energy", ENERGY,
        "papers/SSV-VII-a/main.tex:120"),
    Use("SSV-III", "b", "RG block-scaling factor, a pure number", ONE,
        "papers/SSV-III/main.tex:995",
        local="the renormalisation block factor of \\mathcal{R}_b; unrelated to "
              "the LogSE coupling and never appears beside it"),
    # The completeness test found four more papers using b that the first pass
    # had not declared.  IV and VII-b agree with SSV-I; VI is a local
    # dimensionless fit parameter; II restates SSV-I's E6 relation.
    Use("SSV-IV", "b", r"LogSE coupling, \mu_{\rm nl} = dV/d\rho = b\ln(\rho/\rho_0)",
        ENERGY / mass, "papers/SSV-IV/main.tex:495"),
    Use("SSV-VII-b", "b", r"LogSE coupling, \Phi = b\ln(\rho/\rho_0)",
        ENERGY / mass, "papers/SSV-VII-b/main.tex:46"),
    Use("SSV-II", "b", r"LogSE stiffness, via b\rho_0 = m_0c^2 — inherits SSV-I's "
        r"recorded E6 mismatch, see dimensions.py",
        ENERGY / mass, "papers/SSV-II/main.tex:253"),
    # Departures from what a physicist reader expects (physics.info). Declared
    # so the departure is on the record, not so it is forbidden.
    Use("SSV-I", "F", "form factor of the trefoil breather, a pure number", ONE,
        "papers/SSV-I/main.tex:738"),
    # ---- departures the Wikipedia reference newly exposes ----
    # mu_0 is the vacuum permeability to essentially every physicist.  SSV uses
    # it for a MASS, m_e/alpha ~ 70 MeV, in four papers.  Not a defect — the
    # series is internally consistent — but the most expensive departure here,
    # because mu_0 is among the least ambiguous symbols in physics.
    Use("SSV-I", "mu_0", r"base mass scale m_e/\alpha \approx 70.025 MeV", mass,
        "papers/SSV-I/main.tex:937"),
    Use("SSV-I", "xi", "healing length of the defect core", length,
        "papers/SSV-I/main.tex:403"),
    Use("SSV-III", "Omega", "number of microstates, dimensionless", ONE,
        "papers/SSV-III/main.tex:308"),

    # ---- S: an action in Goldstone/VII-a, an entropy in III/V ----
    # Prompted by the owner noting S = k_B ln(Omega): entropy is an energy per
    # temperature, so the two uses differ in two base dimensions.
    Use("SSV-VII-a", "S", "phase action of the polar decomposition", ACTION,
        "papers/SSV-VII-a/main.tex:119"),
    Use("SSV-Goldstone", "S", r"action functional S[\Psi] = \int dt\,d^3x\,\mathcal{L}",
        ACTION, "papers/SSV-Goldstone/main.tex:312"),
    Use("SSV-III", "S", r"entropy, S = k_B\ln\Omega", ENTROPY,
        "papers/SSV-III/main.tex:308"),
    Use("SSV-V", "S", r"wake/horizon entropy, S_H = k_B\ln\Omega_H", ENTROPY,
        "papers/SSV-V/main.tex:430"),
    # Not dimensioned quantities: a manifold label, an integration surface, a
    # propagator.  Typing these would be inventing a dimension to satisfy a
    # completeness rule, which is worse than admitting the category.
    Use("SSV-I", "S", r"the spheres S^1, S^2 in homotopy statements", None,
        "papers/SSV-I/main.tex:672",
        notational="a manifold label in \\pi_3(S^1), \\hat n \\in S^2 — topology, "
                   "not a physical quantity"),
    Use("SSV-II", "S", "fermion propagator S(p); also the integration surface "
        r"in \Phi_B = \int_S B\cdot dA", None,
        "papers/SSV-II/main.tex:595",
        notational="a propagator and a surface of integration; neither is a "
                   "quantity this registry types"),
    Use("SSV-VII-b", "S", "subscript of the Schwarzschild radius r_S", None,
        "papers/SSV-VII-b/main.tex:263",
        notational="occurs only as the subscript in r_S = 2GM/c^2, never as a "
                   "standalone symbol"),
    Use("SSV-VII-b", "G", "Newton's constant", NEWTON_G,
        "papers/SSV-VII-b/main.tex:526"),
    Use("SSV-I", "a_p", r"proton Compton radius \hbar/(m_p c)", length,
        "papers/SSV-I/main.tex:406"),

    Use("SSV-VI", "b", "dimensionless halo-profile fit parameter (b = 0.5, 1)",
        ONE, "papers/SSV-VI/main.tex:218",
        local="a fit exponent in the rotation-curve profile; the LogSE coupling "
              "does not appear anywhere in this paper"),
]


#: Symbols whose USES are asserted COMPLETE across the series — every paper the
#: census finds them in is declared.  Everything else in ``USES`` is a *sample*:
#: enough to record a departure or a meaning, not a claim of full coverage.
#:
#: The distinction is not a weakening.  It is the difference between "b carries
#: four dimensions" (a countable claim, only true if the declaration is
#: complete) and "SSV-I uses F for a form factor" (a fact about one site).
#: Reporting the first from a partial table is how the first pass of this file
#: said "three dimensions" about a symbol carrying four.
COMPLETE: frozenset = frozenset({"b", "Lambda", "a_0", "S"})


def uses_of(symbol: str) -> list[Use]:
    return [u for u in USES if u.symbol == symbol]


def _dim_key(d: Dimension) -> tuple:
    return tuple(sorted((str(k), v)
                        for k, v in dimsys_SI.get_dimensional_dependencies(d).items()))


@dataclass(frozen=True)
class Collision:
    symbol: str
    dims: dict            # rendered dimension -> [(paper, site, means)]
    declared_local: tuple = field(default_factory=tuple)

    def describe(self) -> str:
        parts = []
        for d, uses in sorted(self.dims.items()):
            where = ", ".join(f"{p} ({s.rsplit('/', 1)[-1]})" for p, s, _ in uses)
            parts.append(f"{d} in {where}")
        return f"{self.symbol}: " + "; ".join(parts)


def collisions() -> list[Collision]:
    """Symbols carrying more than one dimension without a local declaration.

    A ``Use`` with a non-empty ``local`` is excluded from the comparison: the
    paper said it was reusing the letter, and said why.  Everything else that
    disagrees is reported.
    """
    out = []
    for symbol in sorted({u.symbol for u in USES}):
        uses = uses_of(symbol)
        globals_only = [u for u in uses
                        if not u.local and u.dim is not None]
        buckets: dict[str, list] = defaultdict(list)
        for u in globals_only:
            buckets[str(u.dim)].append((u.paper, u.site, u.means))
        if len(buckets) > 1:
            out.append(Collision(symbol, dict(buckets),
                                 tuple(u.paper for u in uses if u.local)))
    return out


def undeclared_global(symbol: str) -> bool:
    """A symbol used in 2+ papers with no GLOBAL entry and no Use record."""
    return symbol not in GLOBAL and not uses_of(symbol)


def coverage() -> dict:
    """What this module actually checks, and what it does not.

    Reported, never implied: a paper is not covered because some of its symbols
    are declared.  Rule 14's warning about generated values applies verbatim to
    declared symbols.
    """
    shared = shared_symbols()
    declared = set(GLOBAL) | {u.symbol for u in USES}
    return {
        "symbols_extracted": len(census()),
        "shared_2plus_papers": len(shared),
        "declared": len(declared),
        "undeclared_shared": sorted(s for s in shared if s not in declared),
        "papers": len(paper_names()),
    }


# --------------------------------------------------------------------------
# The gate
# --------------------------------------------------------------------------

#: Collisions established by the #213 Part A pass and recorded as open findings.
#:
#: The gate fails on anything NOT in this set.  Recording rather than fixing is
#: deliberate: ``Lambda`` and ``a_0`` are standard notation in their own
#: literatures — the cosmological constant and the MOND scale are not going to
#: be renamed to suit this repository — so the resolution is a declaration, not
#: a rename, and that is a judgement for the author.
#:
#: What the gate does guarantee is that **no fourth collision arrives quietly**.
#: This is the same shape as ``claims.py``: known state is pinned, and drift
#: from it stops the build.
KNOWN_COLLISIONS: frozenset = frozenset({"Lambda", "a_0", "b", "S"})


def new_collisions() -> list[Collision]:
    return [c for c in collisions() if c.symbol not in KNOWN_COLLISIONS]


def gate_report(paper: str) -> tuple[list[Collision], str]:
    """Collisions this paper participates in, split into new and known."""
    mine = [c for c in collisions()
            if any(p == paper for uses in c.dims.values() for p, _, _ in uses)]
    fresh = [c for c in mine if c.symbol not in KNOWN_COLLISIONS]
    known = sorted(c.symbol for c in mine if c.symbol in KNOWN_COLLISIONS)
    note = f"{len(known)} known collision(s): {', '.join(known)}" if known \
        else "no declared collisions"
    return fresh, note


# --------------------------------------------------------------------------
# External reference: the standard assignments a physicist reader expects
# --------------------------------------------------------------------------
#: Source: The Physics Hypertextbook, "Symbols" (Glenn Elert),
#: https://physics.info/symbols/ — retrieved 2026-07-29 (owner's choice).
#:
#: WHAT THIS IS FOR.  ``collisions()`` finds symbols the *series* uses two ways.
#: This table finds something different and equally worth knowing: where SSV
#: uses a symbol for something other than what a physicist reader will assume
#: it means.  A departure is not an error — ``F`` for a form factor is fine —
#: but an *undeclared* departure costs the reader every time.
#:
#: WHAT THIS IS NOT.  physics.info is a teaching reference, not a standard.  It
#: has no entry at all for ``\Lambda``, ``a_0``, ``b``, ``\hbar`` or ``\Gamma``
#: — which is to say, it does not cover a single one of the four collisions this
#: module found, and cannot arbitrate them.  The documents that could are
#: ISO 80000 (Quantities and units), the IUPAP SUNAMCO red book, and NIST SP 811.
#: If a symbol convention ever becomes load-bearing in a paper, cite one of
#: those under rule 12, not this.
STANDARD: dict[str, tuple[tuple[str, Dimension], ...]] = {
    "a":     (("acceleration", ACCELERATION),),
    "c":     (("wave speed", VELOCITY), ("specific heat capacity", SPECIFIC_HEAT)),
    "E":     (("energy", ENERGY),),
    "F":     (("force", mass * length / time**2),),
    "f":     (("frequency", FREQUENCY),),
    "G":     (("shear modulus", PRESSURE), ("conductance", CONDUCTANCE)),
    "g":     (("gravitational field", ACCELERATION),),
    "k":     (("spring constant", mass / time**2),),
    "L":     (("length", length), ("angular momentum", ACTION)),
    "m":     (("mass", mass),),
    "P":     (("power", ENERGY / time), ("pressure", PRESSURE)),
    "p":     (("momentum", mass * length / time),),
    "r":     (("position, separation, radius", length),),
    "S":     (("entropy", ENTROPY),),
    "s":     (("displacement, distance", length),),
    "T":     (("period", time), ("temperature", TEMPERATURE)),
    "t":     (("time, duration", time),),
    "V":     (("volume", length**3), ("electric potential", ELECTRIC_POTENTIAL)),
    "v":     (("velocity, speed", VELOCITY),),
    "lambda": (("wavelength", length), ("linear mass density", mass / length)),
    "rho":   (("density, volume mass density", MASS_DENSITY),),
    "omega": (("angular frequency", FREQUENCY),),
    "tau":   (("time constant", time), ("torque", ENERGY),
              ("shear stress", PRESSURE)),
    "sigma": (("normal stress", PRESSURE), ("area mass density", mass / length**2)),
    "k_B":   (("boltzmann constant", BOLTZMANN),),
    "xi":    (),      # no entry — see NOT_IN_STANDARD
}

#: Second reference, added at the owner's suggestion 2026-07-29:
#: Wikipedia, "List of common physics notations",
#: https://en.wikipedia.org/wiki/List_of_common_physics_notations — retrieved
#: 2026-07-29.  It covers most of what physics.info omits, and consulting it
#: CORRECTED one of the departures the first reference produced: physics.info
#: has no entry for Newton's constant, so ``G`` was reported as departing from
#: "shear modulus, conductance".  Wikipedia lists "universal gravitational
#: constant" outright, and the departure was an artefact of the first
#: reference's gap, not a fact about SSV.  Two references disagreeing is the
#: cheapest available check on a single reference's silence.
WIKI: dict[str, tuple[tuple[str, Dimension], ...]] = {
    "a":      (("acceleration", ACCELERATION),),
    "c":      (("speed of light in vacuum", VELOCITY), ("speed of sound", VELOCITY),
               ("specific heat capacity", SPECIFIC_HEAT)),
    "e":      (("eccentricity", ONE), ("Euler's number", ONE),
               ("elementary charge", charge)),
    "F":      (("force", mass * length / time**2),),
    "G":      (("universal gravitational constant", NEWTON_G),
               ("electrical conductance", CONDUCTANCE), ("shear modulus", PRESSURE)),
    "k":      (("Boltzmann constant", BOLTZMANN), ("wavenumber", WAVENUMBER),
               ("stiffness", mass / time**2)),
    "P":      (("power", ENERGY / time),),
    "S":      (("surface area", length**2), ("entropy", ENTROPY),
               ("action", ACTION)),
    "T":      (("period", time), ("temperature", TEMPERATURE)),
    "V":      (("voltage", ELECTRIC_POTENTIAL), ("volume", length**3)),
    "hbar":   (("reduced Planck constant", ACTION),),
    "lambda": (("wavelength", length), ("linear charge density", charge / length)),
    "rho":    (("mass density", MASS_DENSITY), ("volume charge density", charge / length**3)),
    "xi":     (("electromotive force", ELECTRIC_POTENTIAL),),
    "mu_0":   (("vacuum permeability / magnetic constant",
                mass * length / (time**2 * current**2)),),
    "Omega":  (("electric resistance", ELECTRIC_POTENTIAL / current),),
    # Wikipedia gives the cosmological constant in s^-2 (the Friedmann/dynamical
    # convention, Lambda/3 = H^2).  SSV prints 1e-52 m^-2, the Einstein-equation
    # convention.  BOTH are standard; they differ by c^2.  Recorded as the two
    # entries rather than picking one, so a paper matching either is not
    # reported as departing.
    "Lambda": (("cosmological constant (Einstein convention)", CURVATURE),
               ("cosmological constant (Friedmann convention)", 1 / time**2)),
}

#: Symbols the series leans on that the reference simply does not cover.  Listed
#: explicitly so the silence is a recorded fact rather than an inference.
#: Still unlisted by EITHER reference. ``b`` in particular is unclaimed, so
#: SSV is free to use it — but only consistently, which is what makes its
#: three dimensions a defect rather than a clash of conventions.
NOT_IN_STANDARD = ("b", "Gamma", "kappa_0", "alpha_G", "P_0")


def departures_from_standard() -> list[str]:
    """Where SSV's declared meaning is not one the reference lists.

    Reported, never gated.  A departure is a fact about the reader's
    expectations, not a defect — and the reference is a teaching page, so
    treating it as an authority would be worse than not consulting it.
    """
    out = []
    for u in USES:
        if u.dim is None:
            continue
        entries = _standard_for(u.symbol)
        if not entries:
            continue
        keys = {_dim_key(d) for _, d in entries}
        if _dim_key(u.dim) not in keys:
            seen, uniq = set(), []
            for q, d in entries:
                if (q, str(d)) not in seen:
                    seen.add((q, str(d)))
                    uniq.append(f"{q} [{d}]")
            expect = "; ".join(uniq)
            out.append(f"{u.symbol} in {u.paper}: SSV means {u.means!r} "
                       f"[{u.dim}]; reference lists {expect}")
    return out


def _standard_for(symbol: str):
    """Reference entries for a symbol, falling back to its ROOT.

    ``a_0`` and ``a_p`` inherit what the reader expects of ``a``.  This is the
    whole reason the root matters: it is why ``a_0`` as the MOND acceleration
    reads naturally and ``a_0`` as the Bohr radius does not, even though the
    Bohr radius is the older and more universal usage.
    """
    merged = tuple(STANDARD.get(symbol, ())) + tuple(WIKI.get(symbol, ()))
    if merged:
        return merged
    root = symbol.split("_", 1)[0]
    if root in NOT_IN_STANDARD or symbol in NOT_IN_STANDARD:
        return ()
    return tuple(STANDARD.get(root, ())) + tuple(WIKI.get(root, ()))

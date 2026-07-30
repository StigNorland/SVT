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

Scope is deliberately declared rather than inferred.  The paper-local registry
covers load-bearing numbers touched by #182; ``SHARED`` adds the observed
constants selected by #213 Part B.  Neither is every number in the series, and
coverage is reported rather than implied.

Usage:
    python instruments/tools/gen_values.py --compute SSV-I   # run physics -> receipt
    python instruments/tools/gen_values.py --shared --compute # series sources -> receipt
    python instruments/tools/gen_values.py SSV-I             # receipt -> values.tex
    python instruments/tools/gen_values.py --all             # every registered paper
    python instruments/tools/gen_values.py --all --check     # re-run + compare, write nothing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
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


@dataclass(frozen=True)
class SharedValue:
    """One value computed once and emitted into every declaring paper.

    ``papers`` is the explicit coverage surface.  ``was`` records the literal
    spellings replaced in each paper; it is deliberately declared rather than
    discovered by scanning, because #213 showed that scanning numeric literals
    has poor recall and poor precision in opposite directions.
    """

    macro: str
    compute: Callable[[], float]
    sig: int
    describes: str
    source: str
    papers: tuple[str, ...]
    was: dict[str, tuple[str, ...]]


def _lazy_call(module: str, attr: str) -> Callable[[], float]:
    """Return a callable that imports its instrument only when computed.

    Rendering reads receipts and must never import the physics.
    """
    return lambda: float(getattr(__import__(module), attr)())


def _shared(
    macro: str,
    attr: str,
    sig: int,
    describes: str,
    papers: tuple[str, ...],
    was: dict[str, tuple[str, ...]],
) -> SharedValue:
    source = f"instruments/series_values.py::{attr}"
    return SharedValue(
        macro, _lazy_call("series_values", attr), sig, describes, source,
        papers, was,
    )


# Programme-level values.  This is the declared surface; it is intentionally
# not inferred from main.tex.  All are observed inputs, not SSV derivations.
SHARED: tuple[SharedValue, ...] = (
    _shared(
        "ssvAlphaInverse", "inverse_fine_structure", 6,
        r"\alpha^{-1}, CODATA observed input",
        ("SSV-Alpha", "SSV-I", "SSV-II"),
        {
            "SSV-Alpha": ("137.036",),
            "SSV-I": ("137.036",),
            "SSV-II": ("137.036",),
        },
    ),
    _shared(
        "ssvProtonElectronMassRatio", "proton_electron_mass_ratio", 6,
        r"m_p/m_e, CODATA observed input",
        ("SSV-II", "SSV-IV"),
        {
            "SSV-II": ("1836", "1836.15"),
            "SSV-IV": ("1836",),
        },
    ),
    _shared(
        "ssvElectronMassMeV", "electron_mass_mev", 3,
        r"m_e c^2 in MeV, observed input",
        ("SSV-I", "SSV-II"),
        {"SSV-I": ("0.511",), "SSV-II": ("0.511",)},
    ),
    _shared(
        "ssvMuonMassMeV", "muon_mass_mev", 6,
        r"m_\mu c^2 in MeV, observed input",
        ("SSV-I", "SSV-II"),
        {"SSV-I": ("105.658",), "SSV-II": ("105.658",)},
    ),
    _shared(
        "ssvChargedPionMassMeV", "charged_pion_mass_mev", 8,
        r"m_{\pi^\pm} c^2 in MeV, observed input",
        ("SSV-I", "SSV-II"),
        {
            "SSV-I": ("139.570", "139.57018"),
            "SSV-II": ("139.570",),
        },
    ),
    _shared(
        "ssvProtonMassMeV", "proton_mass_mev", 6,
        r"m_p c^2 in MeV, observed input",
        ("SSV-I", "SSV-II"),
        {"SSV-I": ("938.272",), "SSV-II": ("938.272",)},
    ),
    _shared(
        "ssvTauMassMeV", "tau_mass_mev", 6,
        r"m_\tau c^2 in MeV, observed input",
        ("SSV-I", "SSV-II"),
        {"SSV-I": ("1776.860",), "SSV-II": ("1776.86",)},
    ),
    _shared(
        "ssvProtonReducedComptonWavelength", "proton_reduced_compton_wavelength", 2,
        r"\bar{\lambda}_p=\hbar/(m_p c) in metres, CODATA observed inputs",
        ("SSV-I", "SSV-II", "SSV-IV"),
        {
            "SSV-I": (
                r"2.10\times10^{-16}", r"2.10\times 10^{-16}",
            ),
            "SSV-II": (
                r"2\times10^{-16}", r"2\times 10^{-16}",
                r"2.10\times10^{-16}", r"2.10\times 10^{-16}",
            ),
            "SSV-IV": (
                r"2\times10^{-16}", r"2\times 10^{-16}",
                r"2.1\times10^{-16}", r"2.1\times 10^{-16}",
                r"2.10\times10^{-16}", r"2.10\times 10^{-16}",
            ),
        },
    ),
    _shared(
        "ssvProtonComptonWavelength", "proton_compton_wavelength", 2,
        r"\lambda_p=2\pi\hbar/(m_p c) in metres, CODATA observed inputs",
        ("SSV-II", "SSV-IV"),
        {
            "SSV-II": (
                r"1.3\times10^{-15}", r"1.3\times 10^{-15}",
            ),
            "SSV-IV": (
                r"1.3\times10^{-15}", r"1.3\times 10^{-15}",
            ),
        },
    ),
)


def _ssv_i() -> list[Value]:
    import ssv_i_audit_2026 as A
    import issue_218_values as I218

    values = [
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
        Value("ssvCandidateNY", I218.candidate_n_y, 4,
              r"candidate finite-thickness trefoil factor N_Y",
              "instruments/paper_i/issue_218_values.py::candidate_n_y",
              "3.007"),
        Value("ssvEnergyStarMeV", I218.energy_star_mev, 6,
              r"E_\star=(m_e/\alpha)c^2 in MeV",
              "instruments/paper_i/issue_218_values.py::energy_star_mev",
              "70.025"),
        Value("ssvProtonFormFactorLow", I218.fine_grid_form_factor_low, 4,
              r"corrected n=72 proton form factor at R=1.18 xi",
              "instruments/paper_i/issue_218_values.py::fine_grid_form_factor_low",
              "5.168"),
        Value("ssvProtonFormFactorHigh", I218.fine_grid_form_factor_high, 4,
              r"corrected n=48 proton form factor at R=1.18 xi",
              "instruments/paper_i/issue_218_values.py::fine_grid_form_factor_high",
              "5.298"),
        Value("ssvProtonFormFactorMean", I218.fine_grid_form_factor_mean, 3,
              r"mean corrected fine-grid proton form factor at R=1.18 xi",
              "instruments/paper_i/issue_218_values.py::fine_grid_form_factor_mean",
              "5.23"),
        Value("ssvProtonCandidateProductLow", I218.candidate_product_low, 4,
              r"low endpoint of candidate N_Y F product",
              "instruments/paper_i/issue_218_values.py::candidate_product_low",
              "15.54"),
        Value("ssvProtonCandidateProductHigh", I218.candidate_product_high, 4,
              r"high endpoint of candidate N_Y F product",
              "instruments/paper_i/issue_218_values.py::candidate_product_high",
              "15.93"),
        Value("ssvProtonCandidateMassLowMeV", I218.candidate_mass_low_mev, 4,
              r"low endpoint of corrected candidate proton band in MeV",
              "instruments/paper_i/issue_218_values.py::candidate_mass_low_mev",
              "1088"),
        Value("ssvProtonCandidateMassHighMeV", I218.candidate_mass_high_mev, 4,
              r"high endpoint of corrected candidate proton band in MeV",
              "instruments/paper_i/issue_218_values.py::candidate_mass_high_mev",
              "1116"),
        Value("ssvProtonCandidateDeviationLowPct",
              I218.candidate_mass_low_deviation_pct, 3,
              r"low endpoint deviation of candidate proton band, percent",
              "instruments/paper_i/issue_218_values.py::candidate_mass_low_deviation_pct",
              "16.0"),
        Value("ssvProtonCandidateDeviationHighPct",
              I218.candidate_mass_high_deviation_pct, 3,
              r"high endpoint deviation of candidate proton band, percent",
              "instruments/paper_i/issue_218_values.py::candidate_mass_high_deviation_pct",
              "18.9"),
        Value("ssvProtonCutoffLogSlope", I218.cutoff_log_slope, 3,
              r"d ln F / d ln R from R=1.18 to 1.5 xi on the n=72 state",
              "instruments/paper_i/issue_218_values.py::cutoff_log_slope",
              "-1.04"),
        Value("ssvProtonCutoffDropPct", I218.cutoff_drop_pct, 2,
              r"drop in F from R=1.18 to 1.5 xi on the n=72 state, percent",
              "instruments/paper_i/issue_218_values.py::cutoff_drop_pct",
              ""),
        Value("ssvProtonCombinedNYF", I218.corrected_combined_n_y_f, 2,
              r"issue-77 combined N_Y F anchor after corrected calibration",
              "instruments/paper_i/issue_218_values.py::corrected_combined_n_y_f",
              ""),
    ]

    table_specs = (
        ("ssvFTableCoarseROne", I218.form_factor_n24_r100, "7.98"),
        ("ssvFTableCoarseRPaper", I218.form_factor_n24_r118, "6.56"),
        ("ssvFTableCoarseROneHalf", I218.form_factor_n24_r150, "5.11"),
        ("ssvFTableCoarseRTwo", I218.form_factor_n24_r200, "3.99"),
        ("ssvFTableCoarseRThree", I218.form_factor_n24_r300, "3.03"),
        ("ssvFTableMidROne", I218.form_factor_n48_r100, "6.45"),
        ("ssvFTableMidRPaper", I218.form_factor_n48_r118, "5.30"),
        ("ssvFTableMidROneHalf", I218.form_factor_n48_r150, "4.13"),
        ("ssvFTableMidRTwo", I218.form_factor_n48_r200, "3.22"),
        ("ssvFTableMidRThree", I218.form_factor_n48_r300, "2.45"),
        ("ssvFTableFineROne", I218.form_factor_n72_r100, "6.29"),
        ("ssvFTableFineRPaper", I218.form_factor_n72_r118, "5.17"),
        ("ssvFTableFineROneHalf", I218.form_factor_n72_r150, "4.03"),
        ("ssvFTableFineRTwo", I218.form_factor_n72_r200, "3.14"),
        ("ssvFTableFineRThree", I218.form_factor_n72_r300, "2.39"),
    )
    for macro, compute, was in table_specs:
        values.append(Value(
            macro,
            compute,
            3,
            r"corrected saved-state form factor in Table Fstraight",
            f"instruments/paper_i/issue_218_values.py::{compute.__name__}",
            was,
        ))
    return values


def _ssv_ii() -> list[Value]:
    import issue_218_values as I218
    import issue_220_values as I220

    return [
        Value("ssvIIVortexSlope", I220.profile_slope, 6,
              r"corrected coefficient-one vortex origin slope",
              "instruments/paper_ii/issue_220_values.py::profile_slope", ""),
        Value("ssvIIIcurl", I220.i_curl, 5,
              r"corrected straight-core curl integral",
              "instruments/paper_ii/issue_220_values.py::i_curl", "5.02"),
        Value("ssvIIJBend", I220.j_bend, 5,
              r"corrected local curvature integral",
              "instruments/paper_ii/issue_220_values.py::j_bend", "7.81"),
        Value("ssvIIKBend", I220.k_bend, 5,
              r"corrected metric-Jacobian integral",
              "instruments/paper_ii/issue_220_values.py::k_bend", ""),
        Value("ssvIIJKOverFour", I220.jk_over_four, 5,
              r"corrected local bending coefficient (J+K)/4",
              "instruments/paper_ii/issue_220_values.py::jk_over_four", "2.50"),
        Value("ssvIIVortexTau", I220.tau, 5,
              r"corrected vortex line tension at Rcap=phi/alpha",
              "instruments/paper_ii/issue_220_values.py::tau", "17.0"),
        Value("ssvIILambdaBendLocal", I220.lambda_bend_local, 4,
              r"corrected local bending stiffness for lambda_perp=alpha^-2",
              "instruments/paper_ii/issue_220_values.py::lambda_bend_local", ""),
        Value("ssvIILambdaBendGap", I220.lambda_bend_gap, 4,
              r"corrected required/local bending-stiffness ratio",
              "instruments/paper_ii/issue_220_values.py::lambda_bend_gap", "232"),
        Value("ssvIILinearRunningShortfallPct",
              I220.linear_running_shortfall_pct, 3,
              r"shortfall of the p=1 running candidate, percent",
              "instruments/paper_ii/issue_220_values.py::linear_running_shortfall_pct",
              ""),
        Value("ssvIILocalCapRadius", I220.local_equilibrium_radius, 3,
              r"cap radius from the corrected local-equilibrium sub-model",
              "instruments/paper_ii/issue_220_values.py::local_equilibrium_radius",
              ""),
        Value("ssvIILocalCapMassGeV", I220.local_equilibrium_mass_gev, 3,
              r"cap-formula mass at the corrected local-equilibrium radius",
              "instruments/paper_ii/issue_220_values.py::local_equilibrium_mass_gev",
              ""),
        Value("ssvIICandidateProductLow", I218.candidate_product_low, 4,
              r"corrected low endpoint of the Paper I candidate N_Y F product",
              "instruments/paper_i/issue_218_values.py::candidate_product_low",
              "13.28"),
        Value("ssvIICandidateProductHigh", I218.candidate_product_high, 4,
              r"corrected high endpoint of the Paper I candidate N_Y F product",
              "instruments/paper_i/issue_218_values.py::candidate_product_high",
              "13.62"),
        Value("ssvIIProtonPionRatioLow",
              I220.candidate_proton_pion_ratio_low, 4,
              r"corrected low endpoint of candidate m_p/m_pi",
              "instruments/paper_ii/issue_220_values.py::candidate_proton_pion_ratio_low",
              ""),
        Value("ssvIIProtonPionRatioHigh",
              I220.candidate_proton_pion_ratio_high, 4,
              r"corrected high endpoint of candidate m_p/m_pi",
              "instruments/paper_ii/issue_220_values.py::candidate_proton_pion_ratio_high",
              ""),
        Value("ssvIIProtonPionDeviationLowPct",
              I220.candidate_proton_pion_deviation_low_pct, 3,
              r"low corrected candidate m_p/m_pi deviation, percent",
              "instruments/paper_ii/issue_220_values.py::candidate_proton_pion_deviation_low_pct",
              ""),
        Value("ssvIIProtonPionDeviationHighPct",
              I220.candidate_proton_pion_deviation_high_pct, 3,
              r"high corrected candidate m_p/m_pi deviation, percent",
              "instruments/paper_ii/issue_220_values.py::candidate_proton_pion_deviation_high_pct",
              ""),
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
    "SSV-II": _ssv_ii,
    "SSV-VI": _ssv_vi,
    "SSV-VII-b": _ssv_vii_b,
}


def values_for(paper: str) -> list[Value]:
    if paper not in REGISTRY:
        raise KeyError(f"{paper} has no registered values")
    return REGISTRY[paper]()


def shared_values_for(paper: str) -> list[SharedValue]:
    return [value for value in SHARED if paper in value.papers]


def registered_papers() -> list[str]:
    return sorted(set(REGISTRY) | {paper for value in SHARED for paper in value.papers})


def has_values(paper: str) -> bool:
    return paper in REGISTRY or bool(shared_values_for(paper))


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


def shared_receipt_path() -> Path:
    return PAPERS / "shared_values_receipt.json"


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


def compute_shared_receipt() -> dict:
    """Run each series-level source once and build the shared receipt."""
    entries = {}
    for value in SHARED:
        number = float(value.compute())
        entries[value.macro] = {
            "value": number,
            "sig": value.sig,
            "rendered": fmt(number, value.sig),
            "describes": value.describes,
            "source": value.source,
            "source_sha256_16": source_fingerprint(value.source),
            "papers": list(value.papers),
            "was": {paper: list(literals)
                    for paper, literals in value.was.items()},
        }
    return {
        "issue": 213,
        "scope": "SSV series",
        "hypothesis": "every declared load-bearing value printed in two or "
                      "more papers has one computed source (#213 Part B)",
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


def read_shared_receipt() -> dict:
    path = shared_receipt_path()
    if not path.is_file():
        raise FileNotFoundError(
            f"{path.relative_to(REPO_ROOT).as_posix()} missing — run "
            f"`python instruments/tools/gen_values.py --shared --compute`")
    return json.loads(path.read_text(encoding="utf-8"))


def write_shared_receipt(receipt: dict) -> None:
    shared_receipt_path().write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


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


def shared_receipt_drift() -> dict[str, dict]:
    """Compare the one series receipt against the shared-value sources."""
    old = read_shared_receipt()["values"]
    new = compute_shared_receipt()["values"]
    drift = {}
    for macro in sorted(set(old) | set(new)):
        before, after = old.get(macro), new.get(macro)
        if before is None or after is None:
            drift[macro] = {"receipt": before, "now": after}
            continue
        if (before["rendered"] != after["rendered"]
                or before["source_sha256_16"] != after["source_sha256_16"]
                or before["papers"] != after["papers"]
                or before["was"] != after["was"]):
            drift[macro] = {"receipt": before, "now": after}
    return drift


def literal_occurs(text: str, literal: str) -> bool:
    """Whether a declared old literal survives as a complete numeric token."""
    if re.fullmatch(r"\d+(?:\.\d+)?", literal):
        return re.search(
            rf"(?<![\d.]){re.escape(literal)}(?![\d.])", text
        ) is not None
    if r"\times" in literal:
        # LaTeX authors wrap long scientific notation across lines.  Whitespace
        # is not semantic here, so a line break must not evade the guard.
        return re.sub(r"\s+", "", literal) in re.sub(r"\s+", "", text)
    return literal in text


def surviving_shared_literals(paper: str) -> dict[str, list[str]]:
    """Registered old spellings still typed in one paper (#213 Part C)."""
    text = (PAPERS / paper / "main.tex").read_text(encoding="utf-8")
    offenders = {}
    for value in shared_values_for(paper):
        found = [literal for literal in value.was.get(paper, ())
                 if literal_occurs(text, literal)]
        if found:
            offenders[value.macro] = found
    return offenders


# --------------------------------------------------------------------------
# Rendering — reads the receipt only, imports nothing
# --------------------------------------------------------------------------

def _entries_for_render(
    paper: str,
    receipt: dict | None,
    shared_receipt: dict | None,
) -> dict:
    entries = dict((receipt or {"values": {}})["values"])
    if shared_receipt is not None:
        for macro, entry in shared_receipt["values"].items():
            if paper in entry["papers"]:
                if macro in entries:
                    raise ValueError(
                        f"{paper}: {macro} is both paper-local and shared")
                entries[macro] = entry
    return entries


def render(
    paper: str,
    receipt: dict | None,
    shared_receipt: dict | None = None,
) -> str:
    entries = _entries_for_render(paper, receipt, shared_receipt)
    receipt_sources = []
    if receipt is not None:
        receipt_sources.append("results/values_receipt.json")
    if shared_receipt is not None:
        receipt_sources.append("../shared_values_receipt.json")
    source_note = " and ".join(receipt_sources)
    lines = [
        "% Auto-generated by instruments/tools/gen_values.py — do not edit by hand.",
        f"% Regenerate: python instruments/tools/gen_values.py {paper}",
        "%",
        "% Every macro below is COMPUTED by the named instrument, not typed.  A",
        "% number printed in this paper cannot drift from the code that derives it,",
        "% because there is only one of it.  (#198 Part A)",
        "%",
        f"% Rendered from {source_note} — the recorded result of the",
        f"% last instrument run.  Re-run the physics with --compute; verify the",
        f"% recorded result against the instruments with --check.",
        "",
    ]
    for macro, e in entries.items():
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
    """Write one paper's ``values.tex`` from local and shared receipts."""
    if not has_values(paper):
        raise KeyError(f"{paper} has no registered local or shared values")
    receipt = read_receipt(paper) if paper in REGISTRY else None
    shared = read_shared_receipt() if shared_values_for(paper) else None
    fresh = render(paper, receipt, shared)
    path = values_path(paper)
    current = path.read_text(encoding="utf-8") if path.is_file() else None
    path.write_text(fresh, encoding="utf-8")
    return {"paper": paper, "path": path, "changed": current != fresh,
            "n": len(_entries_for_render(paper, receipt, shared))}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paper", nargs="?", help="paper dir name, e.g. SSV-I")
    ap.add_argument("--all", action="store_true", help="every registered paper")
    ap.add_argument("--shared", action="store_true",
                    help="the series-level shared receipt and all its papers")
    ap.add_argument("--compute", action="store_true",
                    help="run the instruments and rewrite the receipt")
    ap.add_argument("--check", action="store_true",
                    help="re-run the instruments and compare against the receipt, "
                         "and confirm values.tex matches it; write nothing "
                         "(exit 1 on any drift)")
    args = ap.parse_args()

    if sum(bool(x) for x in (args.all, args.shared, args.paper)) != 1:
        ap.error("give one paper name, --all, or --shared")

    if args.shared:
        papers = sorted({paper for value in SHARED for paper in value.papers})
    elif args.all:
        papers = registered_papers()
    elif args.paper:
        papers = [args.paper]

    include_shared = (
        args.shared or args.all or any(shared_values_for(paper) for paper in papers)
    )

    bad = False
    if args.check:
        shared_drift = shared_receipt_drift() if include_shared else {}
        if include_shared:
            tag = "STALE" if shared_drift else "ok   "
            print(f"{tag} shared: receipt drift "
                  f"{sorted(shared_drift) or 'none'}")
            bad |= bool(shared_drift)
        for paper in papers:
            local_drift = receipt_drift(paper) if paper in REGISTRY else {}
            local = read_receipt(paper) if paper in REGISTRY else None
            shared = read_shared_receipt() if shared_values_for(paper) else None
            stale_tex = (
                values_path(paper).read_text(encoding="utf-8")
                if values_path(paper).is_file() else None
            ) != render(paper, local, shared)
            literals = surviving_shared_literals(paper)
            tag = "STALE" if (local_drift or stale_tex or literals) else "ok   "
            print(f"{tag} {paper}: local receipt drift "
                  f"{sorted(local_drift) or 'none'}; values.tex "
                  f"{'STALE' if stale_tex else 'current'}; shared literals "
                  f"{literals or 'none'}")
            bad |= bool(local_drift) or stale_tex or bool(literals)
    elif args.compute:
        if include_shared:
            shared = compute_shared_receipt()
            write_shared_receipt(shared)
            print(f"computed shared: {len(shared['values'])} values -> "
                  f"{shared_receipt_path().relative_to(REPO_ROOT).as_posix()}")
        for paper in papers:
            if args.shared or paper not in REGISTRY:
                continue
            r = compute_receipt(paper)
            write_receipt(paper, r)
            print(f"computed {paper}: {len(r['values'])} values -> "
                  f"{receipt_path(paper).relative_to(REPO_ROOT).as_posix()}")
    else:
        for paper in papers:
            r = generate(paper)
            print(f"wrote {paper}: {r['n']} values -> "
                  f"{r['path'].relative_to(REPO_ROOT).as_posix()}"
                  f"{'' if r['changed'] else ' (unchanged)'}")
    if bad:
        print("\nERROR: recompute with --compute, then regenerate values.tex.")
        sys.exit(1)


if __name__ == "__main__":
    main()

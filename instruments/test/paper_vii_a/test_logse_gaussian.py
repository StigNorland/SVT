"""Tests for #189 E1/E2 -- the Gausson under both LogSE sign conventions.

The verdict these guard is NEGATIVE: SSV-VII-a's "Saturation by the Gausson"
is `MISDERIVED`, on either branch. The tests exist so that verdict is
machine-checked rather than trusted, and so a later edit cannot quietly
re-upgrade it (standing rule 1).
"""

import os
import re
import sys

import pytest
import sympy as sp

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_vii_a")
sys.path.insert(0, os.path.abspath(SRC))

import logse_gaussian as L  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", ".."))


# --------------------------------------------------------------------------
# E1 -- the Gausson exists only on the branch #183 rejected
# --------------------------------------------------------------------------

def test_vii_a_convention_reproduces_the_printed_gausson_width():
    """VII-a's eq:gausson is algebraically correct IN ITS OWN CONVENTION."""
    w = L.gausson_width_squared_unconstrained("vii_a_minus")
    assert sp.simplify(w - L.hbar**2 / (2 * L.m * L.b)) == 0


def test_adopted_convention_admits_no_normalisable_gaussian():
    """E1, the load-bearing negative result.

    Under the `+b ln` convention SSV-I adopted (#183) with b > 0, the x^2
    balance forces sigma^2 < 0. There is no normalisable Gaussian, so
    section "Saturation by the Gausson" has no solution to stand on.
    """
    w = L.gausson_width_squared_unconstrained("adopted_plus")
    assert sp.simplify(w + L.hbar**2 / (2 * L.m * L.b)) == 0
    assert L.gaussian_exists("adopted_plus", b_positive=True) is False
    assert L.gaussian_exists("vii_a_minus", b_positive=True) is True


def test_the_two_conventions_differ_only_by_the_sign_of_sigma_squared():
    """Neither branch is 'wrong arithmetic' -- they are different theories.
    Stating this keeps the finding accurate: VII-a did not miscalculate."""
    a = L.gausson_width_squared_unconstrained("vii_a_minus")
    p = L.gausson_width_squared_unconstrained("adopted_plus")
    assert sp.simplify(a + p) == 0


def test_positivity_assumption_does_not_manufacture_the_result():
    """Guard on the guard: `sigma` is declared positive in the module, which
    could in principle let sympy discard a negative root before it is seen.
    The unconstrained solve must agree with the constrained one where a
    solution legitimately exists."""
    assert sp.simplify(L.gausson_width_squared("vii_a_minus")
                       - L.gausson_width_squared_unconstrained(
                           "vii_a_minus")) == 0


def test_single_length_scale_matches_zloshchastiev(  # checkbox 2 of #189
):
    """|sigma^2| = hbar^2/(2m|b|) = Zloshchastiev's a^2 exactly, so the LogSE
    has ONE length scale: the bright-soliton width for one sign, the healing
    length xi for the other."""
    for name in L.CONVENTIONS:
        w = L.gausson_width_squared_unconstrained(name)
        assert sp.simplify(sp.Abs(w) - L.zloshchastiev_length_squared()) == 0


# --------------------------------------------------------------------------
# E2 -- hbar/2 is a property of Gaussians, not of the LogSE
# --------------------------------------------------------------------------

def test_any_gaussian_saturates_regardless_of_width():
    """E2. Note what is NOT in this calculation: b, rho_0, the LogSE."""
    assert sp.simplify(L.uncertainty_product() - L.hbar / 2) == 0


@pytest.mark.parametrize("width", [sp.Rational(1, 7), sp.sqrt(3), 42])
def test_saturation_is_width_independent_for_concrete_widths(width):
    """VII-a offered width-independence as evidence the result was robust.
    It is reproduced here as evidence of the opposite: nothing about the
    LogSE can enter a number that does not depend on the width it fixes."""
    assert sp.simplify(L.uncertainty_product(width) - L.hbar / 2) == 0


def test_a_non_gaussian_state_does_not_saturate():
    """The negative control, and the reason E2 says anything at all.

    If every normalisable state gave hbar/2, "the Gaussian is what does the
    work" would be an empty claim and this whole module would be measuring
    nothing (FM3). A Laplace state gives sqrt(2)/2 hbar > hbar/2.
    """
    product = L.laplace_uncertainty_product()
    assert sp.simplify(product - L.hbar / 2) != 0
    assert bool(sp.simplify(product / L.hbar) > sp.Rational(1, 2))


def test_no_dependence_on_the_logse_coupling_anywhere_in_e2():
    """The claim VII-a made was that hbar/2 comes 'directly from the LogSE'.
    The symbol b does not occur in the E2 result at all."""
    assert L.b not in L.uncertainty_product().free_symbols
    assert L.b not in L.laplace_uncertainty_product().free_symbols


# --------------------------------------------------------------------------
# The cross-paper sign convention -- pilot slice of #205
# --------------------------------------------------------------------------

#: Where each paper prints the logarithmic term, and with which sign.
#: Found by grepping all 12 main.tex; SSV-VII-a is the only outlier, and that
#: single grep is the whole of #189.
PRINTED_SIGN = {
    "SSV-I": "+", "SSV-II": "+", "SSV-IV": "+", "SSV-V": "+",
    "SSV-VII-a": "-",
}

LOG_TERM = re.compile(r"([-+])\s*b\s*\\*,?\s*(?:\\Psi\s*\\,\s*)?\\ln")


def test_the_series_sign_conventions_are_still_what_189_found():
    """Freeze the measurement behind #189 so it cannot silently change.

    This is a DRIFT guard, not a referee: it records that SSV-VII-a prints the
    opposite sign to the other four, which is the defect. It cannot say which
    convention is right -- #183 decided that. If VII-a is later brought onto
    the adopted convention, this test must be updated deliberately, which is
    the point.
    """
    found = {}
    for paper in PRINTED_SIGN:
        tex = os.path.join(REPO, "papers", paper, "main.tex")
        with open(tex, encoding="utf-8") as fh:
            signs = set(LOG_TERM.findall(fh.read()))
        assert signs, f"{paper}: the logarithmic term is no longer found"
        found[paper] = signs

    for paper, expected in PRINTED_SIGN.items():
        assert found[paper] == {expected}, (
            f"{paper} prints {found[paper]}, expected {{'{expected}'}} -- "
            f"the #189 sign finding has moved")

    outliers = [p for p, s in found.items() if s != {"+"}]
    assert outliers == ["SSV-VII-a"], (
        f"the set of papers disagreeing with the adopted +b ln convention "
        f"changed: {outliers}")

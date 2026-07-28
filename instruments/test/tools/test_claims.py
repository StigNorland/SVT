"""Tests for the claim guards (#198 Part D).

The claim guards exist because #198 Part A closed only half the drift path. A
number that cannot diverge from its instrument can still move *legitimately*
after an intentional receipt update and invalidate a relationship reviewed
against its old value.

The tests here fall in two groups, and the second matters more:

  1. the registered claims currently hold;
  2. the registered claims are capable of *not* holding.

A predicate that ignores its changing inputs passes forever and guards nothing.
The first draft of `lambda-enters-denominator` was exactly that: it passed, and
it tested nothing.
`test_claims_are_not_tautologies` exists so that cannot recur silently.

These tests preserve registered relationships after review. They do not decide
whether an author or model wrote a sound conclusion in the first place.
"""

import sys
from pathlib import Path

TOOLS = str(Path(__file__).resolve().parents[2] / "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import claims as C  # noqa: E402
import gen_values as gv  # noqa: E402
import pytest  # noqa: E402

PAPERS = sorted(C.REGISTRY)


# --------------------------------------------------------------------------
# 1 — the claims hold
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_registered_claims_hold(paper):
    bad = C.failing(paper)
    assert not bad, "conclusions that no longer follow from their values:\n" + "\n".join(
        f"  {c.site}  {c.key}\n    asserts: {c.asserts}" for c in bad)


@pytest.mark.parametrize("paper", PAPERS)
def test_registered_statements_have_not_moved_or_changed(paper):
    """A numeric guard must remain bound to the LaTeX statement it protects."""
    moved = C.source_drift(paper)
    assert not moved, (
        f"{paper}: registered LaTeX statements moved or changed: "
        f"{[c.key for c in moved]}")


def claims_of(paper):
    return C.claims_for(paper)


# --------------------------------------------------------------------------
# 2 — the claims could fail   (the group that matters)
# --------------------------------------------------------------------------

def claims_ignoring_perturbations(registered, targets):
    """Keys of predicates that do not notice any registered input changing."""
    unguarded = []
    for claim in registered:
        noticed = False
        for mod, attr in targets:
            original = getattr(mod, attr)
            if callable(original):
                setattr(mod, attr, lambda *a, _o=original, **k: _o(*a, **k) * 1.5)
            else:
                setattr(mod, attr, original * 1.5)
            try:
                if not claim.check():
                    noticed = True
            except Exception:
                noticed = True          # blowing up counts as noticing
            finally:
                setattr(mod, attr, original)
            if noticed:
                break
        if not noticed:
            unguarded.append(claim.key)
    return unguarded


@pytest.mark.parametrize("paper", PAPERS)
def test_claims_are_not_tautologies(paper):
    """Every predicate must actually depend on the numbers it reads.

    Perturb the instrument function each claim rests on and require the claim to
    notice. A predicate that survives an arbitrary perturbation of its own inputs
    is not guarding anything — which is precisely the bug this test was written
    after finding by hand.
    """
    import ssv_i_audit_2026 as A
    import planck_scale_values as P

    # (module, attribute) pairs the claims read, and a way to break each
    targets = {
        "SSV-I": [(A, "lambda_param"), (A, "xi_over_alpha"),
                  (A, "rho0_natural_units"), (A, "rho0_as_printed"),
                  (A, "stationary_radius"), (A, "A_BOHR"), (A, "R_E_CLASSICAL")],
        "SSV-VII-b": [(P, "planck_length"), (P, "planck_mass"),
                      (P, "fundamental_mass"), (P, "healing_length"),
                      (P, "G_NEWTON")],
    }[paper]

    unguarded = claims_ignoring_perturbations(claims_of(paper), targets)

    assert not unguarded, (
        f"{paper}: these predicates survive a 1.5x perturbation of every input "
        f"they read — they restate the computation rather than guard the "
        f"conclusion: {unguarded}")


def test_the_tautology_detector_detects_a_tautology():
    """Guard on the guard: a predicate that ignores its inputs must be caught."""
    always = C.Claim("SSV-I", "always-true", "papers/SSV-I/main.tex:1",
                     "2 + 2 = 4", ("ssvLambda",), lambda: True)
    import ssv_i_audit_2026 as A
    assert claims_ignoring_perturbations(
        [always], [(A, "lambda_param")]
    ) == ["always-true"]


# --------------------------------------------------------------------------
# 3 — coverage: a generated number with no guarded conclusion
# --------------------------------------------------------------------------

@pytest.mark.parametrize("paper", PAPERS)
def test_every_generated_value_is_claimed(paper):
    """A number printed with no conclusion attached is either decoration or an
    unguarded claim. Either way someone should look at it."""
    generated = {v.macro for v in gv.values_for(paper)}
    claimed = {m for c in claims_of(paper) for m in c.depends_on}
    orphans = generated - claimed
    assert not orphans, (
        f"{paper}: generated but no registered conclusion depends on them: "
        f"{sorted(orphans)}")


@pytest.mark.parametrize("paper", PAPERS)
def test_claims_only_reference_real_macros(paper):
    generated = {v.macro for v in gv.values_for(paper)}
    for c in claims_of(paper):
        unknown = set(c.depends_on) - generated
        assert not unknown, f"{c.key} depends on unregistered macros {unknown}"


@pytest.mark.parametrize("paper", PAPERS)
def test_every_claim_states_its_tolerance(paper):
    """'Approximately' is not a specification. A claim that does not say how
    close is close enough cannot be falsified."""
    vague = [c.key for c in claims_of(paper) if not c.tolerance.strip()]
    assert not vague, f"{paper}: claims with no stated tolerance: {vague}"

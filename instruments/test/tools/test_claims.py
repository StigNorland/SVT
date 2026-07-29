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

#: Perturbation factors tried, in order, before a predicate is called unguarded.
#:
#: A single fixed factor conflates two different things: a predicate that
#: ignores its inputs, and a claim that is simply robust.  SSV-VI's B1 clears
#: its threshold by 0.8 dex, so a 1.5x (0.18 dex) nudge legitimately does not
#: flip it — reporting that as a tautology would be a false positive, and the
#: register warns that an inflated defect is still a defect (FM8).  Escalating
#: separates the two: a real tautology survives every factor, a margin does not.
PERTURBATIONS = (1.5, 10.0, 1.0e3, 1.0e6)


def claims_ignoring_perturbations(registered, targets):
    """Keys of predicates that no perturbation of their inputs can disturb."""
    unguarded = []
    for claim in registered:
        noticed = False
        for factor in PERTURBATIONS:
            for mod, attr in targets:
                original = getattr(mod, attr)
                if callable(original):
                    setattr(mod, attr,
                            lambda *a, _o=original, _f=factor, **k:
                            _o(*a, **k) * _f)
                else:
                    setattr(mod, attr, original * factor)
                try:
                    if not claim.check():
                        noticed = True
                except Exception:
                    noticed = True      # blowing up counts as noticing
                finally:
                    setattr(mod, attr, original)
                if noticed:
                    break
            if noticed:
                break
        if not noticed:
            unguarded.append(claim.key)
    return unguarded


#: Papers whose registered claims are about a SIGN or a STRUCTURE rather than
#: a magnitude. Multiplying an input by a positive factor cannot falsify
#: "sigma^2 < 0" or "b does not appear in this expression", so the magnitude
#: harness would report them unguarded — FM8, over-reporting, again. They get
#: the control below, which perturbs the thing they actually depend on.
SIGN_CONTROLLED = {"SSV-VII-a"}


def claims_ignoring_a_flipped_convention(registered):
    """Keys of predicates that do not notice the LogSE sign convention flipping.

    The right perturbation for SSV-VII-a: its findings turn entirely on which
    sign the logarithmic term carries, which is the whole of #189.
    """
    import logse_gaussian as G

    unguarded = []
    original = dict(G.CONVENTIONS)
    for claim in registered:
        G.CONVENTIONS.update({k: -v for k, v in original.items()})
        try:
            noticed = not claim.check()
        except Exception:
            noticed = True
        finally:
            G.CONVENTIONS.update(original)
        if not noticed:
            unguarded.append(claim.key)
    return unguarded


def test_the_sign_control_detects_a_sign_blind_predicate():
    """Guard on the guard: a predicate ignoring the convention must be caught."""
    always = C.Claim("SSV-VII-a", "always-true",
                     "papers/SSV-VII-a/main.tex:1", "2 + 2 = 4", (),
                     lambda: True)
    assert claims_ignoring_a_flipped_convention([always]) == ["always-true"]


@pytest.mark.parametrize("paper", PAPERS)
def test_claims_are_not_tautologies(paper):
    """Every predicate must actually depend on the inputs it reads.

    Perturb what each claim rests on and require the claim to notice. A
    predicate that survives an arbitrary perturbation of its own inputs is not
    guarding anything — which is precisely the bug this test was written after
    finding by hand.
    """
    if paper in SIGN_CONTROLLED:
        import logse_gaussian as G

        # Two controls, and a claim needs only ONE of them to catch it.
        # E1 is about the sign of sigma^2 and is invisible to a positive
        # rescaling; E2 ("hbar/2 is a property of Gaussians") holds on BOTH
        # branches by construction, so it is invisible to a sign flip -- that
        # is its content, not a weakness. Demanding both would fail a correct
        # claim for being correct.
        blind_to_sign = set(claims_ignoring_a_flipped_convention(
            claims_of(paper)))
        blind_to_magnitude = set(claims_ignoring_perturbations(
            claims_of(paper),
            [(G, "uncertainty_product"), (G, "laplace_uncertainty_product"),
             (G, "gausson_width_squared_unconstrained")]))
        unguarded = sorted(blind_to_sign & blind_to_magnitude)
        assert not unguarded, (
            f"{paper}: these predicates survive both a flipped LogSE sign "
            f"convention and a rescaling of every quantity they read: "
            f"{unguarded}")
        return

    import dsph_ledger as D
    import ssv_i_audit_2026 as A
    import planck_scale_values as P

    # (module, attribute) pairs the claims read, and a way to break each
    targets = {
        "SSV-I": [(A, "lambda_param"), (A, "xi_over_alpha"),
                  (A, "rho0_natural_units"), (A, "rho0_as_printed"),
                  (A, "stationary_radius"), (A, "A_BOHR"), (A, "R_E_CLASSICAL")],
        "SSV-VI": [(D, "model_a_vh"), (D, "model_b_vh"), (D, "gamma_req"),
                   (D, "V_MW"), (D, "GAMMA_REQ_MW")],
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

def generated_macros(paper):
    """Macros rule 14 generates for this paper, empty if it registers none.

    A paper may legitimately guard conclusions without printing any generated
    number: SSV-VII-a's #189 findings are symbolic identities, so there is no
    number to generate and nothing to drift. `gv.values_for` raises for such a
    paper, which is right for the generator and wrong for a coverage check.
    """
    try:
        return {v.macro for v in gv.values_for(paper)}
    except KeyError:
        return set()


@pytest.mark.parametrize("paper", PAPERS)
def test_every_generated_value_is_claimed(paper):
    """A number printed with no conclusion attached is either decoration or an
    unguarded claim. Either way someone should look at it."""
    generated = generated_macros(paper)
    claimed = {m for c in claims_of(paper) for m in c.depends_on}
    orphans = generated - claimed
    assert not orphans, (
        f"{paper}: generated but no registered conclusion depends on them: "
        f"{sorted(orphans)}")


@pytest.mark.parametrize("paper", PAPERS)
def test_claims_only_reference_real_macros(paper):
    generated = generated_macros(paper)
    for c in claims_of(paper):
        unknown = set(c.depends_on) - generated
        assert not unknown, f"{c.key} depends on unregistered macros {unknown}"


@pytest.mark.parametrize("paper", PAPERS)
def test_every_claim_states_its_tolerance(paper):
    """'Approximately' is not a specification. A claim that does not say how
    close is close enough cannot be falsified."""
    vague = [c.key for c in claims_of(paper) if not c.tolerance.strip()]
    assert not vague, f"{paper}: claims with no stated tolerance: {vague}"

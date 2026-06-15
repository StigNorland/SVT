"""Tests for #155 H-A0-IR -- the a0 = cH0/2pi coefficient-consistency
over-constraint.

Covers: (1) the GH-2pi derivation reproduces the measured cored a0 to ~0.1% at
H0=73 (parameter-free); (2) c^2 sqrt(Lambda) is excluded (~8x); (3) the
1/2pi-vs-1/6 separation is NOT decisive given the scatter (the honest negative);
(4) the z-evolution falsifier matches the pinned #146 A4 numbers; (5) NEGATIVE
CAPABILITY -- had a0 matched the sqrt(Lambda) prediction the verdict would be R2;
(6) the overall R1 verdict.
"""

import math

import a0_overconstraint as a0


def test_gh_2pi_reproduces_measured_a0():
    out = a0.battery()
    r73 = out["verdicts"]["GH_2pi_ratios"]["73.0"]
    # parameter-free: the cored a0 sits within 1% of cH0/2pi at H0=73
    assert abs(r73 - 1.0) < 0.02
    # and within the consistency band across the H0 tension
    assert all(0.85 <= r <= 1.15
               for r in out["verdicts"]["GH_2pi_ratios"].values())


def test_sqrt_lambda_excluded_both_estimators():
    out = a0.battery()
    r = out["verdicts"]["sqrtLambda_ratio_H73"]
    assert r < 1.0 / 3.0          # off by >3x (measured ~8.4x)
    assert out["verdicts"]["sqrtLambda_excluded_both_estimators"]
    # and excluded under the independent RAR a0 too
    assert out["rar_cross_check"]["rar_sqrtLambda_ratio_H73"] < 1.0 / 3.0


def test_estimators_straddle_2pi_vs_6():
    """The honest tension: the SSV-halo a0 favours 1/2pi, the tighter RAR a0
    favours 1/6 -- so 1/2pi is consistent but not singled out."""
    out = a0.battery()
    rc = out["rar_cross_check"]
    assert rc["ssv_halo_prefers"]["73.0"]["prefers"] == "1/2pi"
    assert rc["rar_prefers"]["73.0"]["prefers"] == "1/6"
    assert rc["estimators_disagree_on_2pi_vs_6"]


def test_desitter_via_S1_machinery():
    """The same Visser eq-70 finite-difference surface gravity as the S1
    dumb-hole, applied to the Hubble flow, gives g_dS = cH0 and a0 = cH0/2pi --
    'same thermodynamics' as a computation, not an assertion."""
    for h0 in (67.4, 73.0):
        g_num, g_an, a0_ds = a0.desitter_surface_gravity(h0)
        assert abs(g_num - g_an) / g_an < 1e-3          # g_dS = cH0
        gh = a0.candidate_a0(h0)["GH_2pi (cH0/2pi, SSV)"]
        assert abs(a0_ds - gh) / gh < 1e-9              # a0 = g_dS/2pi = cH0/2pi
    assert a0.battery()["verdicts"]["deSitter_machinery_reproduces_cH0_2pi"]


def test_1over2pi_vs_1over6_not_decisive():
    # the honest negative: the two cH coefficients differ by 6/2pi = 0.955
    # (0.020 dex), far below the ~0.31 dex measurement scatter
    out = a0.battery()
    d = out["discrimination"]
    assert d["sep_2pi_vs_6_sigma"] < 1.0
    assert not out["verdicts"]["1over2pi_vs_1over6_decisively_separated"]
    # and the H0 tension alone exceeds the 1/2pi-vs-1/6 gap
    assert d["H0_tension_dex"] > d["sep_2pi_vs_6_dex"]


def test_z_falsifier_matches_pinned_146_values():
    out = a0.battery()
    zf = out["z_falsifier"]
    assert abs(zf["z=0.5"]["cH_branch_dex"] - 0.121) < 2e-3
    assert abs(zf["z=1.0"]["cH_branch_dex"] - 0.253) < 2e-3
    assert abs(zf["z=2.0"]["cH_branch_dex"] - 0.482) < 2e-3
    # sqrt(Lambda) branch predicts no evolution -- the decisive separator
    assert all(v["sqrtLambda_branch_dex"] == 0.0 for v in zf.values())


def test_negative_capability_sqrtLambda_would_give_R2():
    """If the measured a0 equalled the sqrt(Lambda) prediction, the GH-2pi
    ratio would fall far outside the consistency band -> R2. Proves the R1
    verdict is reachable-to-R2, not rigged."""
    h0 = 73.0
    preds = a0.candidate_a0(h0)
    a0_if_sqrtL = preds["deSitter (c^2 sqrt(Lambda))"]
    gh = preds["GH_2pi (cH0/2pi, SSV)"]
    ratio_if_sqrtL = a0_if_sqrtL / gh
    assert not (0.85 <= ratio_if_sqrtL <= 1.15)     # would be ~8x -> R2


def test_verdict_R1():
    out = a0.battery()
    v = out["verdicts"]
    assert v["VERDICT"] == "R1"
    assert v["GH_2pi_consistent"]
    assert v["sqrtLambda_excluded_both_estimators"]
    assert v["deSitter_machinery_reproduces_cH0_2pi"]
    assert v["form_yes_magnitude_conceded"]

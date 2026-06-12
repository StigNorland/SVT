"""Tests for #146 H-A0 S0 -- the measured acceleration scale.

Fast CPU checks:
  (i)   the deep-limit identity round-trips (synthetic galaxy built with
        v_h = (G M a0)^{1/4} recovers a0);
  (ii)  the pinned z-falsifier table matches the pre-registered values
        (0.121 / 0.253 / 0.482 dex at z = 0.5 / 1 / 2);
  (iii) anchor arithmetic (cH0/2pi, c^2 sqrt(Lambda)) is correct;
  (iv)  rule A1/A4 logic behaves on synthetic stats;
  (v)   the real CSV runs: tier counts (83 primary / 175 all),
        exclusions accounted, receipt fields present.
"""

import math
import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_vi")
sys.path.insert(0, os.path.abspath(SRC))

import a0_from_vh as a0mod  # noqa: E402


def test_deep_limit_identity_round_trip():
    a0_true = 1.2e-10
    for m in (1e8, 1e10, 1e12):
        v4 = a0mod.G_SI * m * a0mod.M_SUN * a0_true
        vh_kms = v4 ** 0.25 / 1.0e3
        got = a0mod.a0_from(vh_kms, m)
        assert abs(got / a0_true - 1.0) < 1e-12


def test_z_falsifier_table_pinned_values():
    tab = a0mod.z_falsifier_table()
    assert abs(tab["z_0.5"]["cH_anchor_dlog10_M"] - 0.121) < 0.002
    assert abs(tab["z_1.0"]["cH_anchor_dlog10_M"] - 0.253) < 0.002
    assert abs(tab["z_2.0"]["cH_anchor_dlog10_M"] - 0.482) < 0.002
    for z in a0mod.Z_GRID:
        assert tab[f"z_{z}"]["sqrtLambda_anchor_dlog10_M"] == 0.0


def test_anchor_arithmetic():
    anch = a0mod.anchors()
    # cH0/2pi at H0 = 67.4: H0 = 2.184e-18 s^-1 -> 1.042e-10 m/s^2
    assert abs(anch["cH0_over_2pi_H0_67.4"] / 1.042e-10 - 1.0) < 0.01
    # c^2 sqrt(Lambda) = 8.988e16 * 1.0488e-26 = 9.43e-10
    assert abs(anch["c2_sqrt_Lambda"] / 9.43e-10 - 1.0) < 0.01
    assert anch["RAR_literature"] == 1.2e-10


def _stats_stub(slope_nc, slope_c, med_nc, med_c):
    def block(slope, med):
        return {"slope_log_a0_vs_log_M": slope, "slope_ci95": [0, 0],
                "log10_a0_median": med, "log10_a0_p16": med - 0.3,
                "log10_a0_p84": med + 0.3, "a0_median_m_s2": 10.0 ** med}
    return {"primary_nocore": block(slope_nc, med_nc),
            "primary_cored": block(slope_c, med_c)}


def test_rule_a1_pass_fail_logic():
    r = a0mod.evaluate_rules(_stats_stub(0.05, -0.09, -10.0, -10.0))
    assert r["A1_constancy"]["nocore"]["pass_abs_slope_le_0p10"]
    assert r["A1_constancy"]["cored"]["pass_abs_slope_le_0p10"]
    r = a0mod.evaluate_rules(_stats_stub(0.2, 0.0, -10.0, -10.0))
    assert not r["A1_constancy"]["nocore"]["pass_abs_slope_le_0p10"]


def test_rule_a4_wide_window_logic():
    # spread 0.5 dex > 0.3 -> window must cover both amplitudes
    r = a0mod.evaluate_rules(_stats_stub(0.0, 0.0, -10.5, -10.0))
    assert r["A4_wide_window_applied"]
    lo, hi = r["A2_target"]["target_log10_a0_window"]
    assert lo <= -10.8 + 1e-9 and hi >= -9.7 - 1e-9
    # spread 0.1 dex -> cored interval alone
    r = a0mod.evaluate_rules(_stats_stub(0.0, 0.0, -10.1, -10.0))
    assert not r["A4_wide_window_applied"]
    assert r["A2_target"]["target_log10_a0_window"] == [-10.3, -9.7]


def test_real_csv_runs_and_counts():
    rows = a0mod.load_rows()
    assert len(rows) == 175
    assert sum(a0mod.tier_mask(rows, "primary")) == 83
    stats = a0mod.analyse(rows, n_boot=50)
    s = stats["primary_nocore"]
    assert s["n_tier"] == 83
    assert s["n_used"] + s["n_excluded"] == 83
    assert np.isfinite(s["log10_a0_median"])
    # the cored tier excludes only bound-hitters/zeros, never silently
    c = stats["primary_cored"]
    assert c["n_used"] + c["n_excluded"] == 83
    rules = a0mod.evaluate_rules(stats)
    assert "A2_target" in rules and "A3_anchor_table_no_anchor_declared_hit" \
        in rules

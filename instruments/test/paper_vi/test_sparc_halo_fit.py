"""Tests for #133 -- the SPARC multi-galaxy SSV halo battery.

Pins (i) the SPARC parsers against the vendored official files (counts and
spot values), (ii) the model algebra, (iii) synthetic-recovery of the SSV
fit, and (iv) the headline pre-registered outcomes from the cheap side
(no NFW refits): the rule-(c) slope 0.256 +- 0.05 and the rule-(b)
inner-quintile overshoot that falsifies the pure (no-core) form.
"""

import math
import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_vi")
sys.path.insert(0, os.path.abspath(SRC))

import sparc_halo_fit as s  # noqa: E402


def _curves():
    return s.parse_mass_models(s.SPARC_DIR / "MassModels_Lelli2016c.mrt")


def _table():
    return s.parse_galaxy_table(s.SPARC_DIR / "SPARC_Lelli2016c.mrt")


def test_parsers_match_official_counts_and_spot_values():
    curves, table = _curves(), _table()
    assert len(curves) == 175 and len(table) == 175
    assert sum(len(g["R"]) for g in curves.values()) == 3391
    g = curves["NGC3198"]
    assert len(g["R"]) == 43 and abs(g["R"].max() - 44.08) < 1e-9
    t = table["NGC3198"]
    assert t["Q"] == 1 and abs(t["L36"] - 38.279) < 1e-9
    assert table["CamB"]["T"] == 10 and abs(table["CamB"]["D"] - 3.36) < 1e-9


def test_vbar_sq_signed_gas():
    g = {"Vgas": np.array([-10.0, 10.0]), "Vdisk": np.array([20.0, 20.0]),
         "Vbul": np.array([0.0, 30.0])}
    vb2 = s.v_bar_sq(g)
    assert vb2[0] == -100.0 + 0.5 * 400.0
    assert vb2[1] == 100.0 + 0.5 * 400.0 + 0.7 * 900.0


def test_fit_ssv_recovers_synthetic_vh():
    rng = np.random.default_rng(1)
    r = np.linspace(0.5, 20, 30)
    vdisk = 80.0 * np.sqrt(r) / (1 + 0.3 * r)     # toy declining baryons
    g = {"R": r, "Vgas": np.zeros_like(r), "Vdisk": vdisk,
         "Vbul": np.zeros_like(r), "eV": np.full_like(r, 2.0)}
    true_vh = 120.0
    g["Vobs"] = np.sqrt(s.v_bar_sq(g) + true_vh**2) + rng.normal(0, 2.0, 30)
    vh, lo, hi, _ = s.fit_ssv(g)
    assert abs(vh - true_vh) < 3.0
    assert lo < true_vh < hi


def test_nfw_velocity_at_r200_is_v200():
    v200, c = 150.0, 10.0
    r200 = v200 / (10.0 * s.H0_KMS_KPC)
    assert abs(math.sqrt(s.v_nfw_sq(np.array([r200]), v200, c)[0])
               - v200) < 1e-9


def test_flynn_model_anchors_outer_endpoint():
    """The omega construction (their eq. 6) makes the OUTER endpoint exact;
    the inner point picks up the extra omega*R1 (small)."""
    curves = _curves()
    g = curves["NGC3198"]
    v = s.v_flynn(g)
    assert abs(v[-1] - g["Vobs"][-1]) < 1e-9
    omega = (v[-1] - g["Vobs"][0] * math.sqrt(g["R"][0] / g["R"][-1])) \
        / g["R"][-1]
    assert abs(v[0] - (g["Vobs"][0] + omega * g["R"][0])) < 1e-9


def test_headline_rule_c_slope_and_rule_b_overshoot():
    """Pin the pre-registered outcomes using SSV fits only (fast path)."""
    curves, table = _curves(), _table()
    sample = s.select_sample(curves, table, q_max=1)
    assert len(sample) == 83
    res = {}
    for gal in sample:
        vh, lo, hi, c2 = s.fit_ssv(curves[gal])
        res[gal] = {"vh": vh, "vh_lo": lo, "vh_hi": hi,
                    "chi2_ssv": c2}
    rc = s.rule_c(table, res)
    assert rc["verdict"] == "PASS"
    assert abs(rc["slope"] - 0.256) < 0.02
    assert rc["scatter_dex"] < 0.2
    rb = s.rule_b(curves, res)
    assert rb["verdict"] == "FAIL"
    q = rb["median_frac_residual_quintiles"]
    assert q[0] < -0.05, "inner-quintile overshoot is the falsifier"
    assert q[4] > 0.05, "outer-quintile undershoot is the other half"

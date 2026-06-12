"""Tests for #149 H-EXT -- the composite-body extensivity battery.

Fast CPU checks:
  (i)   the measurement helpers are correct on synthetic fields
        (radial profile, log-slope fit, core finder, aperture energy);
  (ii)  rule logic (R1/R2/R3 of #149) behaves on stub results;
  (iii) the quick-mode battery runs end-to-end as a smoke test: the E1
        control sees a NEGATIVE Bernoulli tail of the right order (the
        quick geometry is too tight for the 15% physics window -- that
        validation lives in the full run's receipt, which is the
        decisive artifact).
"""

import math
import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_iv")
sys.path.insert(0, os.path.abspath(SRC))

import extensivity_battery as ext  # noqa: E402


def _grid(n=128, L=40.0):
    x = (np.arange(n) - n / 2) * (L / n)
    return np.meshgrid(x, x, indexing="ij")


def test_radial_profile_recovers_power_law():
    X, Y = _grid()
    R = np.sqrt(X * X + Y * Y) + 1e-9
    field = 1.0 / R ** 2
    r_edges = np.arange(2.0, 15.0, 1.0)
    rc, prof = ext.radial_profile(field, X, Y, (0.0, 0.0), r_edges)
    assert np.all(np.isfinite(prof))
    # r^2-weighted profile should be ~ constant
    flat = prof * rc ** 2
    assert np.nanstd(flat) / np.nanmean(flat) < 0.05


def test_fit_logslope_synthetic():
    rc = np.arange(5.0, 30.0, 1.0)
    for s_true in (2.0, 4.0, 6.0):
        vals = 3.0 * rc ** (-s_true)
        s, n = ext.fit_logslope(rc, vals, np.ones(len(rc), dtype=bool))
        assert n == len(rc)
        assert abs(s - s_true) < 1e-9
    s, n = ext.fit_logslope(rc, rc * 0 + 1.0,
                            np.zeros(len(rc), dtype=bool))
    assert s is None and n == 0


def test_find_cores_two_dips():
    X, Y = _grid()
    rho = np.ones_like(X)
    for cx, cy in ((-5.0, 0.0), (5.0, 0.0)):
        rho -= 0.9 * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2))
    cores = ext.find_cores(rho, X, Y, 2, r_search=15.0, min_sep=3.0)
    got = sorted(c[0] for c in cores)
    assert abs(got[0] + 5.0) < 0.5 and abs(got[1] - 5.0) < 0.5


def test_aperture_energy_uniform():
    X, Y = _grid()
    e = np.ones_like(X) * 2.0
    val = ext.aperture_energy(e, X, Y, (0.0, 0.0), 5.0)
    assert abs(val / (2.0 * math.pi * 25.0) - 1.0) < 0.05


def _stub(plateau_dev, ratio, slope, e3_ratio=None):
    out = {"E1": {"rel_dev": plateau_dev},
           "E2": {"ratio_to_E1_plateau": ratio, "slope": slope}}
    if e3_ratio is not None:
        out["E3"] = {"ratio": e3_ratio}
    return out


def test_rule_logic():
    # clean negative: valid control, no monopole at 5%, steep ladder
    r = ext.evaluate_rules(_stub(0.10, 0.02, 5.8))
    assert r["R3_instrument_valid"] and r["R2_clean_negative"]
    assert not r["R1_monopole_found"]
    # invalid control poisons R2 (instrument, not physics)
    r = ext.evaluate_rules(_stub(0.30, 0.02, 5.8))
    assert not r["R3_instrument_valid"] and not r["R2_clean_negative"]
    # monopole branch: slope 2, amplitude large, doubling clusters
    r = ext.evaluate_rules(_stub(0.10, 0.50, 2.1, e3_ratio=2.2))
    assert r["R1_monopole_found"] and not r["R2_clean_negative"]
    # slope unmeasurable -> amplitude clause alone decides
    r = ext.evaluate_rules(_stub(0.10, 0.03, None))
    assert r["R2_clean_negative"]
    assert "amplitude" in r["R2_slope_clause"]


def test_quick_battery_smoke():
    out = ext.run_battery(quick=True)
    e1 = out["E1"]
    # quick geometry is too tight for the 15% window; smoke-test the
    # sign and order of the Bernoulli tail only
    assert e1["drho_r2_plateau_relaxed"] < 0.0
    assert 0.05 < abs(e1["drho_r2_plateau_relaxed"]) < 1.5
    assert "E2" in out and "E2b" in out and "profiles" in out
    assert len(out["profiles"]["r"]) == len(out["profiles"]["E2_absdrho"])

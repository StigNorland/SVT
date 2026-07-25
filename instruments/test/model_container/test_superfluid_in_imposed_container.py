"""Tests for #162 -- superfluid in an imposed container.

Fast CPU checks of the load-bearing pieces:
  (i)   POSITIVE CONTROL: an undriven phonon oscillates at the Bogoliubov
        frequency (validates the split-step solver before its verdict is
        trusted);
  (ii)  the evolution is norm-conserving (unitary split-step);
  (iii) matched parameters give the cubic and log media the SAME dispersion
        (the setup that makes the null test sharp);
  (iv)  R-consistency: the local phase-advance rate equals -mu_local to
        numerical precision, for all three media (the effect/cause dictionary);
  (v)   R-prediction: with c_s matched, the log medium's shear response is
        indistinguishable from the ordinary GPE (the clean negative), while the
        free field -- not a fluid -- does not respond;
  (vi)  the verdict function applies the pre-registered decision rules.
"""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_container")
sys.path.insert(0, os.path.abspath(SRC))

import superfluid_in_imposed_container as c  # noqa: E402

FAST = dict(N=24, L=20.0)


def test_positive_control_phonon_matches_bogoliubov():
    params = c.matched_params(cs2=1.0)
    for medium in ("cubic", "log"):
        wm, wb = c.measure_phonon_frequency(medium, params, k_index=2,
                                            periods=3.0, dt=5e-3, **FAST)
        assert abs(wm - wb) / wb < 0.06, f"{medium}: {wm} vs {wb}"


def test_norm_conserved():
    params = c.matched_params(cs2=1.0)
    N, L = 24, 20.0
    X, Y, KX, KY = c.make_grid(N, L)
    rng = np.random.default_rng(0)
    psi = (np.sqrt(params["rho0"])
           * (1.0 + 1e-2 * rng.standard_normal((N, N)))).astype(np.complex128)
    n0 = c.norm(psi, L, N)
    psi1 = c.evolve(psi, 200, 5e-3, "log", params, KX, KY,
                    shear=lambda t: 0.05 * np.sin(1.3 * t))
    assert abs(c.norm(psi1, L, N) - n0) / n0 < 1e-10


def test_matched_params_share_dispersion():
    params = c.matched_params(cs2=1.0)
    k = np.linspace(0.1, 3.0, 20)
    wc = c.bogoliubov(k, "cubic", params)
    wl = c.bogoliubov(k, "log", params)
    assert np.max(np.abs(wc - wl)) < 1e-12
    # and the log sound speed is density-independent (its signature)
    assert c.sound_speed_sq("log", params) == params["b"]


def test_consistency_effect_cause_dictionary():
    params = c.matched_params(cs2=1.0)
    for medium in c.MEDIA:
        err = c.consistency_error(medium, params, N=32, L=20.0, dt=2e-3)
        assert err < 1e-3, f"{medium}: phase-rate vs -mu_local err {err}"


def test_shear_response_log_indistinguishable_from_cubic():
    out = c.compare_shear_response(cs2=1.0, k_index=2, h0=0.08,
                                   n_drive=5.0, dt=5e-3, **FAST)
    # the clean negative: matched-c_s log tracks the ordinary GPE
    assert out["diff_log_vs_cubic"] < 1e-2
    # both fluids respond (growth > 1); the free field does not
    assert out["cubic"]["growth"] > 1.05
    assert out["log"]["growth"] > 1.05
    assert out["diff_log_vs_linear"] > 0.1


def test_verdict_rules():
    v = c.verdict(cons_err=1e-7, diff_log_vs_cubic=1e-5)
    assert v["consistency"] == "PASS"
    assert v["prediction"] == "R-NEGATIVE"
    v2 = c.verdict(cons_err=1e-1, diff_log_vs_cubic=0.5)
    assert v2["consistency"] == "FAIL"
    assert v2["prediction"] == "R-POSITIVE"

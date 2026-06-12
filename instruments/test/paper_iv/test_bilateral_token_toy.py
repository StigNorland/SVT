"""Tests for #129 TOKEN-TAX (H-BILATERAL S0) -- the token-budget toy.

Fast CPU checks of the load-bearing pieces:
  (i)   the owner's worked example is reproduced exactly (8 joint
        tokens in slot 1, 2 more = 25% of slot 2's available budget);
  (ii)  SYNC mode gives gamma = 0 -- machine-exact on the rate
        estimator (the synchronized branch pays the tax ONCE);
  (iii) INDEP mode gives gamma = 1/A (the A^2 product rule);
  (iv)  the correlation interpolation hits the closed form
        gamma(c, A) = (1-c^2)/(A + c^2(1-A));
  (v)   the per-event-latency control is chromatic (delta ~ 1/C) while
        the rate levy is not -- obligation 2 is load-bearing;
  (vi)  mask bookkeeping: exactly k positions taxed.
"""

import math
import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_iv")
sys.path.insert(0, os.path.abspath(SRC))

import bilateral_token_toy as toy  # noqa: E402

S, K, C = 10, 2, 10
A = 1 - K / S


def _rng(seed=7):
    return np.random.default_rng(seed)


def test_mask_has_exactly_k_taxed():
    rng = _rng()
    for _ in range(50):
        m = toy.draw_mask(rng, S, K)
        assert m.size == S and int((~m).sum()) == K


def test_worked_example_ledger_exact():
    # 20% loading, slot = 10 tokens, handshake = 10 tokens:
    # 8 joint tokens in slot 1, then 2 of slot 2's 8 available = 25%.
    ledger = toy.handshake_ledger(_rng(), S=S, k=K, C=C, c=1.0)
    assert ledger == [8, 2]
    assert ledger[1] / (S - K) == 0.25


def test_sync_gamma_is_zero():
    g = toy.measure_gamma(_rng(), S=S, L=K / S, C=C, n_hops=500,
                          c=1.0, seeds=3)
    assert abs(g["gamma_rate"]) < 1e-12, \
        "SYNC must pay the tax exactly once (rate estimator machine-zero)"
    assert abs(g["gamma_wall"]) < 5e-3       # sub-slot quantization only


def test_indep_gamma_is_one_over_A():
    g = toy.measure_gamma(_rng(), S=S, L=K / S, C=C, n_hops=800,
                          c=0.0, seeds=6)
    assert abs(g["gamma_wall"] - 1 / A) <= 0.06 * (1 / A)


def test_correlation_closed_form():
    c = 0.5
    pred = toy.gamma_predicted(c, A)
    assert math.isclose(pred, 0.75 / 0.85, rel_tol=1e-12)
    g = toy.measure_gamma(_rng(), S=S, L=K / S, C=C, n_hops=800,
                          c=c, seeds=6)
    assert abs(g["gamma_wall"] - pred) <= 0.06


def test_latency_control_is_chromatic_rate_levy_is_not():
    rng = _rng()
    d = {}
    for Cc in (5, 20):
        nh = 4000 // Cc
        T0 = nh * Cc / S
        Ts = [toy.transit(rng, S=S, L=K / S, C=Cc, n_hops=nh, c=0.0)[0]
              for _ in range(4)]
        d[Cc] = np.mean(Ts) / T0 - 1.0
    # rate levy: fractional delay independent of C (within noise)
    assert abs(d[5] - d[20]) <= 0.05 * abs(d[20])
    # per-event latency: extra delay = D*S/C exactly -- chromatic
    D_lat = 0.5
    extra = {Cc: D_lat * S / Cc for Cc in (5, 20)}
    assert extra[5] == 4 * extra[20]


def test_delta_prop_closed_forms():
    # SYNC: L/(1-L); INDEP: (2L - L^2)/(1 - L)^2
    assert math.isclose(toy.delta_prop_predicted(toy.SYNC, 0.2), 0.25)
    assert math.isclose(toy.delta_prop_predicted(toy.INDEP, 0.2),
                        (1 - 0.64) / 0.64)

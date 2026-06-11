"""Tests for #129 H-SPATIAL -- the index/clock-delay battery.

Fast CPU versions (small grids) of the load-bearing checks:
  (i)   the dealiased stepper is stable at probe amplitudes (the
        un-dealiased split-step has a high-k instability that corrupted
        early runs -- pinned here so it cannot silently return);
  (ii)  the instrument detects a REAL index (varying-b positive control)
        with the predicted sign and magnitude;
  (iii) the S1 null: a Thomas-Fermi density depression produces no
        measurable propagation delay (gamma_eff ~ 0), while the clock
        prediction for the same well is large -- the R2 separation;
  (iv)  the arrival-shift estimator recovers a known synthetic delay.
"""

import math
import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_iv")
sys.path.insert(0, os.path.abspath(SRC))

os.environ["SSV_GPU"] = "0"          # force CPU before import
import h_spatial_index as h          # noqa: E402

CFG = dict(nx=512, ny=128, dx=0.5, x0=-80.0, w=12.0, x_det=80.0,
           t_end=200.0, dt=0.1, record_every=4)
SIGMA = 25.0
LAM = 8.0
K = 2 * math.pi / LAM
OM = math.sqrt(h.B0) * K


def _grids():
    return h.grids(CFG["nx"], CFG["ny"], CFG["dx"])


def test_stepper_stable_at_probe_amplitude():
    X, Y = _grids()
    med = h.Medium2D(CFG["nx"], CFG["ny"], CFG["dx"])
    g = (np.exp(-((X - CFG["x0"]) / CFG["w"]) ** 2)
         * np.exp(-(Y / (0.3 * CFG["ny"] * CFG["dx"])) ** 2))
    u = 1e-3 * g * np.cos(K * (X - CFG["x0"]))
    phi = (math.sqrt(h.B0) / K) * 1e-3 * g * np.sin(K * (X - CFG["x0"]))
    psi = (np.sqrt(1.0 + u) * np.exp(1j * phi)).astype(np.complex64)
    for _ in range(1500):                       # t = 150
        psi = med.step(psi, 0.1)
    assert np.abs(np.abs(psi) ** 2 - 1.0).max() < 5e-3, \
        "high-k instability returned (dealiasing broken?)"


def test_arrival_shift_recovers_synthetic_delay():
    t = np.arange(0, 200, 0.4)
    env = np.exp(-((t - 90) / 18) ** 2)
    for tau in (0.0, 0.7, 2.3):
        s_ref = env * np.cos(OM * t)
        env_d = np.exp(-((t - 90 - tau) / 18) ** 2)
        s_test = env_d * np.cos(OM * (t - tau))
        got = h.arrival_shift(t, s_ref, s_test, OM)
        assert abs(got - tau) < 0.05, (tau, got)


def _battery_small(V=None, b=None):
    base = dict(CFG)
    k = K
    t, cols_ref = h.run_transit(k=k, **base)
    s_ref = h.col_signal(t, cols_ref, CFG["ny"], CFG["dx"], k)
    if V is not None:
        t2, cols = h.transit_cols(k=k, V=V, **base)
    else:
        t2, cols = h.run_transit(k=k, b=b, **base)
    s = h.col_signal(t, cols, CFG["ny"], CFG["dx"], k)
    return t, s_ref, s


def test_positive_control_detects_real_index():
    X, Y = _grids()
    r2 = X**2 + Y**2
    eta = 0.04
    b_well = (h.B0 * (1 - eta * np.exp(-r2 / SIGMA**2))).astype(np.float32)
    t, s_ref, s = _battery_small(b=b_well)
    d = h.arrival_shift(t, s_ref, s, OM)
    pred = h.predicted_index_delay_bwell(eta, SIGMA, CFG["dx"],
                                         CFG["nx"] * CFG["dx"], K)
    assert pred > 0.4, "control well too weak to test"
    assert abs(d / pred - 1.0) < 0.35, (d, pred)


def test_depression_null_vs_clock_delay():
    """The R2 separation: index delay ~ 0 while the clock delay for the
    same well is large."""
    X, Y = _grids()
    r2 = X**2 + Y**2
    v0 = 0.1
    V = (v0 * np.exp(-r2 / SIGMA**2)).astype(np.float32)
    t, s_ref, s = _battery_small(V=V)
    d_idx = h.arrival_shift(t, s_ref, s, OM)
    d_clk = h.predicted_clock_delay(v0, SIGMA)
    assert d_clk > 4.0
    assert abs(d_idx / d_clk) < 0.1, (d_idx, d_clk)

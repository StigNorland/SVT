"""Tests for #124 D4/D4b -- pitch-vs-Q sweep machinery.

Fast checks only (no N-body): (i) the m=2 phase-vs-ln r pitch estimator of
disc_nbody.fourier_modes recovers the pitch of a synthetic logarithmic
spiral; (ii) the pre-registered D4 decision logic (A2 validity floor,
Spearman threshold, per-time verdicts) behaves as posted to #124,
including on the actual D4b outcome shape (strong arms, no Q trend =>
FAIL, not INCONCLUSIVE).
"""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_vi_b")
sys.path.insert(0, os.path.abspath(SRC))

os.environ.pop("SSV_GPU", None)         # force CPU backend for the import
import disc_nbody as dn                  # noqa: E402
import disc_nbody_d4_pitch as d4         # noqa: E402


def _log_spiral_points(pitch_deg, n=120_000, rlo=1.0, rhi=4.0, seed=3):
    """Two-armed logarithmic spiral: phi = ln(r)/tan(pitch) + (0 or pi),
    with azimuthal scatter small enough to keep A2 well above the floor."""
    rng = np.random.default_rng(seed)
    r = np.exp(rng.uniform(np.log(rlo), np.log(rhi), n))
    arm = rng.integers(0, 2, n) * np.pi
    phi = (np.log(r) / np.tan(np.radians(pitch_deg)) + arm
           + 0.25 * rng.standard_normal(n))
    return np.stack([r * np.cos(phi), r * np.sin(phi)], axis=1)


def test_pitch_estimator_recovers_synthetic_spiral():
    for true_pitch in (15.0, 30.0):
        pos = _log_spiral_points(true_pitch)
        amps, pitch = dn.fourier_modes(pos)
        assert amps[2] > d4.A2_FLOOR, "synthetic arms below validity floor"
        assert abs(pitch - true_pitch) < 5.0, (
            f"pitch {pitch:.1f} vs true {true_pitch:.1f}")


def test_spearman_perfect_and_anti():
    x = np.array([1.0, 1.3, 1.6, 2.0])
    assert d4.spearman(x, np.array([1.0, 2.0, 3.0, 4.0])) == 1.0
    assert d4.spearman(x, np.array([4.0, 3.0, 2.0, 1.0])) == -1.0


def _rows(t_pitch_a2):
    return [{"t": t, "A2": a2, "pitch_deg": p, "v_ratio": 1.0}
            for (t, p, a2) in t_pitch_a2]


def test_evaluate_pass_fail_inconclusive():
    ts = (20.0,)
    # increasing pitch with Q, all valid -> PASS
    rec = {(q, 11): _rows([(20.0, 10.0 + 10.0 * q, 0.10)])
           for q in d4.Q_GRID}
    assert d4.evaluate(rec, t_samples=ts)["overall"] == "PASS"
    # strong arms, no trend (the D4b shape) -> FAIL, not INCONCLUSIVE
    pitches = {1.0: 24.0, 1.3: 23.5, 1.6: 45.8, 2.0: 24.9}
    rec = {(q, 11): _rows([(20.0, pitches[q], 0.10)]) for q in d4.Q_GRID}
    assert d4.evaluate(rec, t_samples=ts)["overall"] == "FAIL"
    # arms below the validity floor (the D4 v_h=0.45 shape) -> INCONCLUSIVE
    rec = {(q, 11): _rows([(20.0, 30.0, 0.01)]) for q in d4.Q_GRID}
    assert d4.evaluate(rec, t_samples=ts)["overall"] == "INCONCLUSIVE"


def test_evaluate_means_over_seeds_and_applies_floor_per_run():
    ts = (20.0,)
    rec = {}
    for q in d4.Q_GRID:
        rec[(q, 11)] = _rows([(20.0, 20.0, 0.10)])      # valid
        rec[(q, 7)] = _rows([(20.0, 80.0, 0.005)])      # floored out
    out = d4.evaluate(rec, t_samples=ts)
    e = out["per_time"]["20.0"]
    assert e["Q_valid"] == sorted(d4.Q_GRID)
    assert all(abs(p - 20.0) < 1e-9 for p in e["pitch_deg"])

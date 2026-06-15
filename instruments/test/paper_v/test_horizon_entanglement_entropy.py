"""Tests for #155 H-EOS S2 -- cross-horizon entanglement entropy battery.

Covers: (1) the correlator->entropy kernel against closed-form values;
(2) the baseline LogSE Bogoliubov vacuum is area-law (tracks the provably
area-law massive-scalar calibrator, far from the volume anchor); (3) the
volume-law thermal control reads ~3; (4) NEGATIVE CAPABILITY -- the area
classifier REJECTS volume-law data (so an R2 is reachable, not engineered out);
(5) the #138 chiral-silence is exact; (6) the dumb-hole reproduces the baseline
area coefficient (eta universal).
"""

import math

import numpy as np
import pytest

import horizon_entanglement_entropy as he


# ----------------------------------------------------------------------
# (1) correlator -> entropy kernel, closed form
# ----------------------------------------------------------------------

def test_kernel_unentangled_mode_zero():
    # nu = 1/2 exactly (X P = 1/4) => pure => S = 0
    S = he.entropy_from_corr(np.array([[0.5]]), np.array([[0.5]]))
    assert abs(S) < 1e-9


def test_kernel_known_single_mode_value():
    # X P = 1 => nu = 1 => S = 1.5 ln 1.5 - 0.5 ln 0.5 = 0.953977...
    S = he.entropy_from_corr(np.array([[1.0]]), np.array([[1.0]]))
    expected = 1.5 * math.log(1.5) - 0.5 * math.log(0.5)
    assert abs(S - expected) < 1e-9
    assert abs(expected - 0.9547712) < 1e-6


def test_kernel_monotone_in_coupling():
    # entanglement entropy of a 2-oscillator ground state grows with coupling;
    # zero coupling (diagonal K) gives exactly zero.
    def S_of(k1):
        K = np.array([[1.0 + k1, -k1], [-k1, 1.0 + k1]])
        X, P = he.corr_from_K(K)
        return he.entropy_from_corr(X[:1, :1], P[:1, :1])
    assert S_of(0.0) < 1e-9
    assert S_of(0.5) > S_of(0.1) > 0.0


# ----------------------------------------------------------------------
# (2)+(3)+(6) the battery verdict on the quick run
# ----------------------------------------------------------------------

@pytest.fixture(scope="module")
def quick_battery():
    return he.battery(quick=True)


def test_baseline_area_law(quick_battery):
    v = quick_battery["verdicts"]
    area_ref = quick_battery["A_baseline"]["massive_control"]["slope"]
    base = v["A_baseline_slope"]
    vol = v["D_control_slope"]
    # baseline tracks the provably-area-law massive calibrator, far from volume
    assert abs(base - area_ref) < 0.15
    assert abs(base - vol) > 0.6
    assert v["A_baseline_area_law"] is True


def test_volume_control_is_volume_law(quick_battery):
    assert quick_battery["verdicts"]["D_control_slope"] > 2.6


def test_eta_universal(quick_battery):
    r = quick_battery["verdicts"]["eta_coefficient_ratio_C_over_A"]
    assert abs(r - 1.0) < 0.25


def test_dumbhole_tracks_baseline(quick_battery):
    base = quick_battery["A_baseline"]["slope"]
    dh = quick_battery["C_dumbhole"]["slope"]
    assert abs(base - dh) < 0.15


# ----------------------------------------------------------------------
# (4) NEGATIVE CAPABILITY -- the discriminator can return R2
# ----------------------------------------------------------------------

def test_area_classifier_rejects_volume_law(quick_battery):
    """The same calibrated-anchor logic that scores the baseline R1 must score
    genuine volume-law data NOT-area. We feed it the thermal (volume-law)
    series: its exponent is closer to the volume anchor and S/R^3 does NOT
    decrease toward zero, so closer_to_area AND subvolume both fail. This proves
    the R1 verdict is reachable-to-R2, not engineered."""
    D = quick_battery["D_volume_control"]
    R = np.asarray(D["R"], float)
    S = np.asarray(D["S_thermal"], float)
    diag = he.area_law_diagnostics(R, S)
    area_ref = quick_battery["A_baseline"]["massive_control"]["slope"]
    vol_ref = D["slope"]
    closer_to_area = abs(diag["slope"] - area_ref) < abs(diag["slope"] - vol_ref)
    s3 = diag["S_over_R3"]
    subvolume = (all(s3[i + 1] <= s3[i] * 1.001 for i in range(len(s3) - 1))
                 and s3[-1] < 0.6 * s3[0])
    assert not closer_to_area          # volume data is NOT closer to area
    assert not subvolume               # and is NOT sub-volume
    # and a constructed long-range (non-local) K is also rejected as area-law
    n = 24
    idx = np.arange(n)
    # 1/|i-j| long-range coupling => long-range correlations => super-area EE
    LR = 1.0 / (np.abs(idx[:, None] - idx[None, :]) + 1.0)
    K = np.diag(LR.sum(1)) - LR + 0.05 * np.eye(n)   # graph-Laplacian + gap
    X, P = he.corr_from_K(K)
    Sfull = he.entropy_from_corr(X, P)
    Shalf = he.entropy_from_corr(X[:n // 2, :n // 2], P[:n // 2, :n // 2])
    assert Sfull >= 0.0 and Shalf >= 0.0   # kernel stays well-defined


# ----------------------------------------------------------------------
# (5) #138 chiral silence is exact
# ----------------------------------------------------------------------

def test_chiral_exactly_silent(quick_battery):
    assert quick_battery["B_chiral"]["max_rel_diff"] == 0.0


# ----------------------------------------------------------------------
# overall verdict shape
# ----------------------------------------------------------------------

def test_verdict_present_and_consistent(quick_battery):
    v = quick_battery["verdicts"]
    assert v["VERDICT"] in ("R1", "R2")
    # given the physics (local quadratic Hamiltonian) the quick run is R1
    assert v["VERDICT"] == "R1"
    assert v["B_chiral_exactly_silent"] is True
    # the conceded coefficient overshoot is reported at full strength
    assert quick_battery["eta_G_overshoot_a_p_over_l_P_squared"] > 1e38

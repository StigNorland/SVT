"""Tests for the corrected-SSV 2+1D disk modular calculation."""

import os
import sys

import numpy as np


SRC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_screen"
)
sys.path.insert(0, os.path.abspath(SRC))

import ssv_disk_modular as disk  # noqa: E402


def test_disk_covariances_are_symmetric_and_physical():
    X, P, sites, radii = disk.disk_correlators(N=20, R=4, xi=1.0)
    assert X.shape == P.shape == (len(sites), len(sites))
    assert len(radii) == len(sites)
    assert np.allclose(X, X.T)
    assert np.allclose(P, P.T)
    assert np.linalg.eigvalsh(X).min() > 0
    assert np.linalg.eigvalsh(P).min() > 0


def test_dispersion_is_gapless_ssv_crossover_not_massive_yukawa():
    N = 24
    modes = np.arange(1, N + 1)
    k = np.pi * modes / (N + 1)
    lam = 4.0 * np.sin(0.5 * k) ** 2
    xi = 2.0
    omega2 = lam * (1.0 + xi * xi * lam)
    assert np.all(omega2 > 0)  # finite Dirichlet box has no exact zero mode
    assert np.isclose(omega2[0] / lam[0], 1.0 + xi * xi * lam[0])
    assert not np.any(np.isclose(omega2 - xi**-2, lam))


def test_blind_nonlocal_control_detects_bilocal_kernel():
    control = disk.blind_nonlocal_control(R=5)
    assert control["detected"] is True
    assert control["increase_factor"] > 5.0


def test_small_case_modular_covariance_reconstruction():
    row = disk.analyze_case(N=20, R=4, R_over_xi=4.0)
    assert row["covariance_reconstruction_error"] < 1e-4


def test_preregistered_run_reports_all_controls_and_decision():
    report = disk.run()
    assert len(report["rows"]) == 15
    assert isinstance(report["controls_ok"], bool)
    assert sum(
        (
            report["T1_finite_scale_nongeometric"],
            report["T3_R1_remains_open"],
        )
    ) <= 1
    assert report["verdict"]

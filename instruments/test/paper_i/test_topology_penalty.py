"""Unit tests for topology_penalty.py."""

import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from paper_i.topology_penalty import (
    core_mask,
    topology_penalty_energy,
    topology_penalty_gradient,
)


def test_zero_mu_zero_energy():
    psi = np.ones((4, 4, 4), dtype=complex)
    mask = np.zeros_like(psi, dtype=bool)
    assert topology_penalty_energy(psi, mask, rho_target=0.0, mu=0.0, dx=1.0) == 0.0


def test_zero_mu_zero_gradient():
    psi = np.ones((4, 4, 4), dtype=complex)
    mask = np.zeros_like(psi, dtype=bool)
    g = topology_penalty_gradient(psi, mask, rho_target=0.0, mu=0.0)
    assert np.all(g == 0.0)


def test_empty_mask_zero_energy():
    psi = np.ones((4, 4, 4), dtype=complex) * 2.0
    mask = np.zeros_like(psi, dtype=bool)
    assert topology_penalty_energy(psi, mask, rho_target=0.0, mu=1.0, dx=1.0) == 0.0


def test_full_mask_uniform_energy():
    psi = np.ones((4, 4, 4), dtype=complex) * 2.0  # rho = 4
    mask = np.ones_like(psi, dtype=bool)
    # excess = max(4 - 0, 0) = 4; sum = 4^2 * 64 cells * 1 = 1024
    e = topology_penalty_energy(psi, mask, rho_target=0.0, mu=1.0, dx=1.0)
    assert e == 1024.0


def test_rho_target_subtracts():
    psi = np.ones((4, 4, 4), dtype=complex) * 2.0  # rho = 4
    mask = np.ones_like(psi, dtype=bool)
    # excess = max(4 - 3, 0) = 1; sum = 1 * 64 = 64
    e = topology_penalty_energy(psi, mask, rho_target=3.0, mu=1.0, dx=1.0)
    assert e == 64.0


def test_below_target_no_penalty():
    psi = np.ones((4, 4, 4), dtype=complex) * 0.1  # rho = 0.01
    mask = np.ones_like(psi, dtype=bool)
    e = topology_penalty_energy(psi, mask, rho_target=0.5, mu=1.0, dx=1.0)
    assert e == 0.0


def test_dx_cubed_scaling():
    psi = np.ones((4, 4, 4), dtype=complex)  # rho = 1
    mask = np.ones_like(psi, dtype=bool)
    e_dx1 = topology_penalty_energy(psi, mask, rho_target=0.0, mu=1.0, dx=1.0)
    e_dx2 = topology_penalty_energy(psi, mask, rho_target=0.0, mu=1.0, dx=2.0)
    assert e_dx2 == e_dx1 * 8.0


def test_gradient_matches_finite_difference():
    """Numerical gradient check via finite differences of the energy."""
    np.random.seed(0)
    psi = (np.random.randn(3, 3, 3) + 1j * np.random.randn(3, 3, 3)) * 0.5 + 1.0
    mask = np.ones_like(psi, dtype=bool)
    mu = 1.0
    rho_target = 0.1
    dx = 0.5

    analytical = topology_penalty_gradient(psi, mask, rho_target, mu)

    # Finite difference of energy in psi^* direction
    # Wirtinger: dE/dpsi^* = (1/2)(dE/d(Re psi) + i * dE/d(Im psi))
    eps = 1e-6
    numerical = np.zeros_like(psi)
    for idx in np.ndindex(psi.shape):
        psi_p = psi.copy()
        psi_p[idx] += eps
        psi_m = psi.copy()
        psi_m[idx] -= eps
        e_p = topology_penalty_energy(psi_p, mask, rho_target, mu, dx)
        e_m = topology_penalty_energy(psi_m, mask, rho_target, mu, dx)
        dE_dRe = (e_p - e_m) / (2 * eps)

        psi_p = psi.copy()
        psi_p[idx] += 1j * eps
        psi_m = psi.copy()
        psi_m[idx] -= 1j * eps
        e_p = topology_penalty_energy(psi_p, mask, rho_target, mu, dx)
        e_m = topology_penalty_energy(psi_m, mask, rho_target, mu, dx)
        dE_dIm = (e_p - e_m) / (2 * eps)

        # dE/dpsi^* in continuous theory: 1/2 * (dE/dRe + i * dE/dIm)
        # Multiplied by dx^3 to match the discretization (energy has dx^3, gradient density doesn't)
        numerical[idx] = 0.5 * (dE_dRe + 1j * dE_dIm) / (dx ** 3)

    # Check agreement (modest tolerance for finite-difference noise)
    assert np.allclose(analytical, numerical, atol=1e-5, rtol=1e-3), \
        f"max diff = {np.max(np.abs(analytical - numerical))}"


def test_core_mask_basic():
    """Cells with rho < threshold are masked."""
    psi = np.array([0.1, 0.5, 1.0, 0.0]).reshape((2, 2, 1)).astype(complex)
    mask = core_mask(psi, threshold=0.5)
    # rho = [0.01, 0.25, 1.0, 0.0]; below 0.5: indices 0, 1, 3
    expected = np.array([[True, True], [False, True]]).reshape((2, 2, 1))
    assert np.array_equal(mask, expected)


def test_gradient_zero_outside_mask():
    np.random.seed(0)
    psi = np.random.randn(4, 4, 4) + 1j * np.random.randn(4, 4, 4)
    mask = np.zeros_like(psi, dtype=bool)
    mask[0, 0, 0] = True
    g = topology_penalty_gradient(psi, mask, rho_target=0.0, mu=1.0)
    # All entries except [0,0,0] should be zero
    other_indices = tuple(slice(None) if i != 0 else slice(1, None) for i in range(3))
    # Easier: check that gradient at masked cell is nonzero and elsewhere zero
    assert g[0, 0, 0] != 0
    masked_count = np.sum(g != 0)
    assert masked_count == 1

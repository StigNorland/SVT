"""Unit tests for topology_helpers.py."""

import sys
from pathlib import Path

import numpy as np
import pytest

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from paper_i.topology_helpers import count_vortex_links, vortex_link_density


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _vortex_z_field(N: int, z_extent: int) -> np.ndarray:
    """Complex field with a single straight vortex line along z.

    Uses even N so the vortex sits at the centre of plaquette (N//2-1, N//2-1)
    rather than on a grid point.  Amplitude = tanh(r) so the core is zero.
    """
    x = np.arange(N) - (N - 1) / 2.0
    y = np.arange(N) - (N - 1) / 2.0
    X, Y = np.meshgrid(x, y, indexing="ij")
    phase = np.arctan2(Y, X)
    amp = np.tanh(np.sqrt(X**2 + Y**2))
    field_2d = amp * np.exp(1j * phase)
    return np.stack([field_2d] * z_extent, axis=-1)


def _antivortex_z_field(N: int, z_extent: int) -> np.ndarray:
    """Like _vortex_z_field but with winding -2pi (antivortex)."""
    x = np.arange(N) - (N - 1) / 2.0
    y = np.arange(N) - (N - 1) / 2.0
    X, Y = np.meshgrid(x, y, indexing="ij")
    phase = -np.arctan2(Y, X)
    amp = np.tanh(np.sqrt(X**2 + Y**2))
    field_2d = amp * np.exp(1j * phase)
    return np.stack([field_2d] * z_extent, axis=-1)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_uniform_field_has_no_links():
    psi = np.ones((6, 6, 6), dtype=complex)
    assert count_vortex_links(psi) == 0


def test_uniform_real_field_has_no_links():
    psi = 2.0 * np.ones((8, 8, 8), dtype=complex)
    assert count_vortex_links(psi) == 0


def test_vortex_line_z_gives_nonzero_links():
    N = 8
    psi = _vortex_z_field(N, z_extent=N)
    assert count_vortex_links(psi) > 0


def test_vortex_line_z_gives_exactly_nz_links():
    """One straight vortex in z should produce exactly Nz xy-plaquette links."""
    N = 8
    psi = _vortex_z_field(N, z_extent=N)
    links = count_vortex_links(psi)
    # One xy-plaquette per z-slice has |W| = 2pi; xz and yz faces have |W| = 0.
    assert links == N


def test_antivortex_gives_same_link_count_as_vortex():
    """count_vortex_links counts |W| > pi, so vortex and antivortex contribute equally."""
    N = 8
    psi_v = _vortex_z_field(N, z_extent=N)
    psi_av = _antivortex_z_field(N, z_extent=N)
    assert count_vortex_links(psi_v) == count_vortex_links(psi_av)


def test_vortex_more_links_than_uniform():
    N = 8
    psi_v = _vortex_z_field(N, z_extent=N)
    psi_u = np.ones((N, N, N), dtype=complex)
    assert count_vortex_links(psi_v) > count_vortex_links(psi_u)


def test_dissolving_vortex_eventually_loses_all_links():
    """Interpolating strongly toward the uniform condensate removes all links."""
    N = 8
    psi_vortex = _vortex_z_field(N, z_extent=N)
    psi_uniform = np.ones_like(psi_vortex)
    # At alpha=0.99 toward uniform, phase winding is < pi everywhere
    psi_nearly_uniform = 0.01 * psi_vortex + 0.99 * psi_uniform
    assert count_vortex_links(psi_nearly_uniform) == 0


def test_return_type_is_int():
    psi = np.ones((4, 4, 4), dtype=complex)
    result = count_vortex_links(psi)
    assert isinstance(result, int)


def test_vortex_link_density_nonzero_for_vortex():
    N = 8
    psi = _vortex_z_field(N, z_extent=N)
    density = vortex_link_density(psi, dx=0.5)
    assert density > 0.0
    assert np.isfinite(density)


def test_vortex_link_density_zero_for_uniform():
    N = 8
    psi = np.ones((N, N, N), dtype=complex)
    density = vortex_link_density(psi, dx=0.5)
    assert density == 0.0


def test_vortex_link_density_scales_with_dx():
    """Density should be approximately grid-independent for same physical vortex."""
    N_coarse, N_fine = 8, 16
    dx_coarse, dx_fine = 1.0, 0.5  # same physical domain (8 xi)
    psi_coarse = _vortex_z_field(N_coarse, z_extent=N_coarse)
    psi_fine = _vortex_z_field(N_fine, z_extent=N_fine)
    density_coarse = vortex_link_density(psi_coarse, dx=dx_coarse)
    density_fine = vortex_link_density(psi_fine, dx=dx_fine)
    # Both represent the same physical vortex; densities should agree within 20%
    assert abs(density_coarse - density_fine) / max(density_coarse, density_fine) < 0.2


def test_two_parallel_vortices_double_link_count():
    """Two vortex lines should give approximately twice the link count."""
    N = 16
    x = np.arange(N) - (N - 1) / 2.0
    y = np.arange(N) - (N - 1) / 2.0
    X, Y = np.meshgrid(x, y, indexing="ij")
    # Vortex at (-4, 0) and (+4, 0)
    r1 = np.sqrt((X + 4) ** 2 + Y**2)
    r2 = np.sqrt((X - 4) ** 2 + Y**2)
    phase = np.arctan2(Y, X + 4) + np.arctan2(Y, X - 4)
    amp = np.tanh(r1) * np.tanh(r2)
    field_2d = amp * np.exp(1j * phase)
    psi_two = np.stack([field_2d] * N, axis=-1)

    psi_one = _vortex_z_field(N, z_extent=N)
    links_one = count_vortex_links(psi_one)
    links_two = count_vortex_links(psi_two)
    # Two vortices => roughly twice as many links
    assert links_two >= links_one * 1.5

"""Tests for #122 — the time-dilation-field rotation-curve model (VI-a).

Guards both the structural rebuild and the honest finding:
  - gravity = r dΦ/dr with Φ_CBH = -G M_BH/r gives the **Newtonian/Keplerian
    limit near the CBH**, exactly (the thing the old phenomenological fit lacked);
  - the wave field is core-suppressed inside r0 and flat (J0 -> 0) far out;
  - components add in quadrature (v_total^2 = sum v_i^2);
  - and the key result: M31's measured baryons cannot supply the flat curve, so
    the CBH 'wave' term must contribute a large FREE amplitude — i.e. the flat
    curve is NOT produced by the CBH frequency, it needs a dark-matter-equivalent
    normalisation.  If a future change makes baryons alone suffice, that is a
    data/units bug, not a discovery.
"""

import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parents[1]
p = str(SRC / "paper_vi_a")
if p not in sys.path:
    sys.path.insert(0, p)

from rotation_curve_timedilation import (  # noqa: E402
    G, M_BH_MSUN, bh_node_spacing,
    v2_cbh, v2_disc, v2_wave, v2_baryons_fixed, ssv_total, load_data,
)


def test_newtonian_keplerian_limit_at_cbh():
    """v2_cbh(r) == G M_BH / r exactly: the recovered weak-field Newtonian limit."""
    r = np.array([0.05, 0.5, 5.0])
    assert np.allclose(v2_cbh(r), G * M_BH_MSUN / r, rtol=1e-12)
    # Keplerian: v*sqrt(r) constant; rises as r -> 0.
    vk = np.sqrt(v2_cbh(r)) * np.sqrt(r)
    assert np.allclose(vk, vk[0], rtol=1e-12)


def test_wave_core_suppressed_and_flat():
    dr = bh_node_spacing()
    # Core-suppressed: v2_wave is a tiny fraction of V_w^2 deep in the core.
    assert v2_wave(np.array([1e-3]), 200.0, 2.0, -0.3, dr)[0] / 200.0**2 < 1e-3
    # Far out: J0 -> 0, envelope -> 1, so v2_wave -> V_w^2.
    far = v2_wave(np.array([5000.0]), 200.0, 2.0, -0.3, dr)[0]
    assert abs(far - 200.0**2) / 200.0**2 < 0.05


def test_components_add_in_quadrature():
    r = np.array([2.0, 10.0, 30.0])
    dr = bh_node_spacing()
    total2 = ssv_total(r, 3e10, 1.0, 7e10, 5.3, 180.0, 2.0, -0.3) ** 2
    parts = (v2_cbh(r) + 1e-30)  # cbh
    from rotation_curve_timedilation import v2_bulge
    parts = v2_cbh(r) + v2_bulge(r, 3e10, 1.0) + v2_disc(r, 7e10, 5.3) + v2_wave(r, 180.0, 2.0, -0.3, dr)
    assert np.allclose(total2, parts, rtol=1e-10)


def test_flat_curve_not_produced_by_baryons():
    """M31's measured baryons fall far short of the observed flat curve, so the
    CBH 'wave' term must supply a large free amplitude (the honest negative)."""
    r, v, e = load_data(0.0)
    r_out = r[-5:]               # outermost points
    v_obs2 = (v[-5:]) ** 2
    v_bar2 = v2_baryons_fixed(r_out)
    # baryons supply well under half of v^2 at large radius:
    assert np.mean(v_bar2 / v_obs2) < 0.45
    # so the residual the wave must cover is the majority:
    assert np.mean(1.0 - v_bar2 / v_obs2) > 0.55

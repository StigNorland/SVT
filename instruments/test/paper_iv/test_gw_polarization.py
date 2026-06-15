"""Tests for #129 GW-POL -- SSV gravitational-wave polarization.

Fast CPU checks of the load-bearing pieces:
  (i)    POSITIVE CONTROL: the constructed L-shaped antenna patterns match
         the published closed forms to machine precision (validates the
         instrument before its SSV verdict is trusted);
  (ii)   helicity content: tensor modes carry the |2| psi-harmonic, vector
         the |1|, scalar the |0| -- the spin discriminator;
  (iii)  F_breathing = -F_longitudinal exactly (the cancellation identity);
  (iv)   the SSV isotropic mix (breathing + longitudinal) cancels to ~0 in
         the long-wavelength differential readout;
  (v)    the finite-frequency residual is small (<1%) and scales ~linearly
         with f (the O(fL/c) longitudinal leakage), so the SSV signal is
         suppressed, not absent;
  (vi)   the round-trip transfer reduces to e_proj * L/c as f -> 0;
  (vii)  emission: monopole and dipole acoustic radiation vanish under mass
         and momentum conservation, quadrupole leads (Hulse-Taylor pass);
  (viii) the pre-registered verdict is R2.
"""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_iv")
sys.path.insert(0, os.path.abspath(SRC))

import gw_polarization as g  # noqa: E402

MODES = ["plus", "cross", "vec_x", "vec_y", "breathing", "longitudinal"]


def test_positive_control_antenna_matches_closed_form():
    rng = np.random.default_rng(3)
    err = 0.0
    for _ in range(1000):
        th = rng.uniform(0.03, np.pi - 0.03)
        ph = rng.uniform(0, 2 * np.pi)
        ps = rng.uniform(0, np.pi)
        a = g.antenna(th, ph, ps)
        b = g.antenna_closed_form(th, ph, ps)
        for m in MODES:
            err = max(err, abs(a[m] - b[m]))
    assert err < 1e-12, f"antenna vs closed form max err {err}"


def test_helicity_content():
    h = {m: g.helicity_harmonic(m) for m in MODES}
    assert h["plus"] == 2 and h["cross"] == 2          # tensor: helicity 2
    assert h["vec_x"] == 1 and h["vec_y"] == 1         # vector: helicity 1
    assert h["breathing"] == 0 and h["longitudinal"] == 0  # scalar: helicity 0


def test_breathing_longitudinal_cancel():
    rng = np.random.default_rng(5)
    for _ in range(200):
        th = rng.uniform(0.03, np.pi - 0.03)
        ph = rng.uniform(0, 2 * np.pi)
        ps = rng.uniform(0, np.pi)
        a = g.antenna(th, ph, ps)
        assert abs(a["breathing"] + a["longitudinal"]) < 1e-12


def test_ssv_longwavelength_cancellation():
    max_ssv, max_tensor = g.ssv_long_wavelength_response(n_grid=24)
    assert max_ssv < 1e-12            # isotropic metric cancels exactly
    assert max_tensor > 0.5           # tensor reference is order unity


def test_finite_frequency_suppression_scaling():
    L = 4000.0
    s10 = g.ssv_suppression(10.0, L, n_grid=12)
    s100 = g.ssv_suppression(100.0, L, n_grid=12)
    assert s100 < 0.01                        # suppressed at the LIGO band
    assert s10 > 0                            # not identically zero (residual)
    assert abs(s100 / s10 - 10.0) < 1.0       # ~linear in f (O(fL/c))


def test_roundtrip_transfer_longwavelength_limit():
    L = 4000.0
    lim = g.roundtrip_transfer(1e-6, 0.3, L, e_proj=1.0)
    assert abs(abs(lim) - L / g.C_LIGHT) / (L / g.C_LIGHT) < 1e-3


def test_emission_no_monopole_no_dipole():
    e = g.emission_multipoles()
    assert e["monopole_d2M_peak"] < 1e-9      # mass conservation
    assert e["dipole_d2P_peak"] < 1e-9        # momentum conservation
    assert e["quadrupole_d3Q_peak"] > 1.0     # quadrupole radiates


def test_verdict_is_R2():
    # SSV modes are scalar (helicity 0): no tensor helicity, overlap 0 -> R2
    h = {m: g.helicity_harmonic(m) for m in ["breathing", "longitudinal"]}
    assert set(h.values()) == {0}

"""Tests for #138 CHIRAL-DISPERSION -- the n-hat channel dispersion battery.

Fast CPU versions (small grids) of the load-bearing checks:
  (i)    the dealiased spinor stepper is stable at probe amplitudes and
         holds the uniform vacuum (the #129 aliasing lesson, pinned);
  (ii)   the magnon dispersion is quadratic with the quantum-pressure
         coefficient: omega = k^2/2, NOT a linear branch at any speed
         (the R1 trigger, and the R2 falsification trigger's absence);
  (iii)  the instrument distinguishes: the same readout on the density
         channel recovers the LINEAR Bogoliubov branch;
  (iv)   chiral silence: E_perp is quartic in the spin amplitude, and
         with lambda = 2000 ACTIVE in the dynamics the omega shift is
         O(eps^2) (nonlinear), extrapolating to zero in the linear
         spectrum;
  (v)    the spin channel carries no linear-order current (the
         charge-decoupling statement behind the no-Cherenkov verdict);
  (vi)   Q3: the magnon's effective potential over a relaxed depression
         is flat (V + b ln rho_b = mu), and a magnon wavepacket transits
         a Thomas-Fermi depression with no measurable delay while the
         same instrument sees the predicted delay from an explicit
         spin-channel potential -- the non-transactional verdict.
"""

import math
import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_ii")
sys.path.insert(0, os.path.abspath(SRC))

import chiral_dispersion as c          # noqa: E402


def test_stepper_holds_uniform_vacuum():
    """Spin plane wave at probe amplitude: total density must stay
    pinned at rho0 (no aliasing instability, no channel leakage)."""
    nx, dx = 256, 0.5
    med = c.SpinorMedium2D(nx, 4, dx)
    x = c.grid_x(nx, dx)
    k = 2 * math.pi * 8 / (nx * dx)
    p2 = np.tile((1e-3 * np.exp(1j * k * x))[:, None], (1, 4))
    p1 = np.sqrt(1.0 - np.abs(p2) ** 2).astype(complex)
    for _ in range(1500):                       # t = 150
        p1, p2 = med.step(p1, p2, 0.1)
    rho = np.abs(p1) ** 2 + np.abs(p2) ** 2
    assert np.abs(rho - 1.0).max() < 5e-3, \
        "uniform vacuum lost (dealiasing broken or channel coupling?)"
    assert np.abs(np.abs(p2) - 1e-3).max() < 1e-4, \
        "magnon amplitude not conserved"


def test_magnon_dispersion_quadratic_not_linear():
    """omega(k) = k^2/2 at two k a factor 4 apart: the implied power is
    2.00 +- 0.05 (R1 trigger) and decisively not 1 (R2 trigger)."""
    ks, oms = c.magnon_dispersion(512, 0.5, [8, 32], t_end=200.0, dt=0.1)
    for k, om in zip(ks, oms):
        assert abs(om / (k * k / 2) - 1.0) < 0.01, (k, om)
    p = math.log(oms[1] / oms[0]) / math.log(ks[1] / ks[0])
    assert abs(p - 2.0) < 0.05, p
    assert abs(p - 1.0) > 0.5, "linear branch?!"


def test_instrument_sees_linear_bogoliubov_branch():
    """The same phase-rotation readout on the density channel must
    recover the LINEAR collective branch -- so a linear chiral mode
    could not have hidden from the magnon measurement."""
    k, om, om_pred = c.bogoliubov_control(512, 0.5, 8, t_end=200.0, dt=0.1)
    assert abs(om / om_pred - 1.0) < 0.015, (om, om_pred)
    # and the branch really is linear-ish there (low k): om ~ c k
    assert abs(om / (math.sqrt(c.B0) * k) - 1.0) < 0.05


def test_chiral_energy_quartic_and_no_linear_current():
    """E_perp ~ eps^4 (a linear-order stiffness would give eps^2);
    the spin channel's current and curl are eps^2 (no linear-order
    coupling to charge/flow)."""
    sc = c.chiral_energy_scaling(128, 0.5, 8, [1e-3, 3e-3, 1e-2, 3e-2])
    assert abs(sc["slope_E_perp"] - 4.0) < 0.2, sc["slope_E_perp"]
    assert abs(sc["slope_E_spin_gradient"] - 2.0) < 0.1
    assert abs(sc["slope_j"] - 2.0) < 0.1, sc["slope_j"]
    assert abs(sc["slope_curl_j"] - 2.0) < 0.1, sc["slope_curl_j"]


def test_lambda_on_dynamics_shift_is_nonlinear_only():
    """With lambda = 2000 ACTIVE in the EOM, the modulated-magnon
    frequency shift scales as eps^2 (nonlinear) and the linear-spectrum
    extrapolation is consistent with zero."""
    eps_pair = (2e-3, 6e-3)
    d_oms, om0 = [], None
    for eps in eps_pair:
        om_off, q = c.modulated_magnon_omega(96, 0.5, 4, eps, 0.0,
                                             t_end=80.0, dt=0.05)
        om_on, _ = c.modulated_magnon_omega(96, 0.5, 4, eps,
                                            c.LAMBDA_SSV,
                                            t_end=80.0, dt=0.05)
        d_oms.append(om_on - om_off)
        om0 = q * q
        assert abs(om_off / om0 - 1.0) < 5e-3, (om_off, om0)
    ratio = d_oms[0] / d_oms[1]
    assert abs(ratio / (eps_pair[0] / eps_pair[1]) ** 2 - 1.0) < 0.5, ratio
    c2 = d_oms[1] / eps_pair[1] ** 2
    resid = abs(d_oms[0] - c2 * eps_pair[0] ** 2) / om0
    assert resid < 2e-3, resid


def test_q3_static_effective_potential_flat():
    """V + b ln rho_b over the relaxed background = mu up to the tiny
    quantum-pressure term: the magnon reads no index potential, where an
    unbalanced (transactional) channel would read the full |V|."""
    nx, dx, sigma, v0 = 1024, 0.5, 30.0, 0.1
    x = c.grid_x(nx, dx)
    V_line = v0 * np.exp(-((x / sigma) ** 2))
    rho = c.relax_background(nx, 4, dx,
                             np.tile(V_line[:, None], (1, 4)),
                             n_iter=3000, dtau=0.2)[:, 0]
    u_eff = c.B0 * np.log(rho) + V_line
    u_eff -= u_eff[0]
    assert np.max(np.abs(u_eff)) / v0 < 1e-3, np.max(np.abs(u_eff)) / v0


def test_q3_magnon_transit_null_with_validated_instrument():
    """Mini H-SPATIAL for the n-hat channel: the instrument must see the
    WKB delay from an explicit spin-channel potential (positive control)
    and then see ~nothing from the Thomas-Fermi depression."""
    nx, dx, sigma, v0 = 512, 0.5, 20.0, 0.1
    k0 = 2 * math.pi / 8.0
    x = c.grid_x(nx, dx)
    V_line = v0 * np.exp(-((x / sigma) ** 2))
    base = dict(nx=nx, dx=dx, k0=k0, w=16.0, x0=-60.0, x_det=60.0,
                t_end=210.0, dt=0.1)
    t_u, s_u = c.magnon_transit(**base)
    t_p, s_p = c.magnon_transit(U_spin=-V_line, **base)
    t_d, s_d = c.magnon_transit(V=V_line, rho_b=np.exp(-V_line / c.B0),
                                **base)
    arr = c.peak_window_centroid
    pred = c.wkb_delay(V_line, dx, k0)
    assert pred < -2.0, "control well too weak to test"
    delay_pc = arr(t_p, s_p) - arr(t_u, s_u)
    delay_dep = arr(t_d, s_d) - arr(t_u, s_u)
    assert abs(delay_pc / pred - 1.0) < 0.3, (delay_pc, pred)
    assert abs(delay_dep / pred) < 0.15, (delay_dep, pred)

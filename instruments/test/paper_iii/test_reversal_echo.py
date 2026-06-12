"""Tests for #137 REVERSAL-ECHO -- the conservativity/echo battery.

Fast CPU versions (small grids) of the load-bearing checks:
  (i)    the discrete stepper is exactly T-invertible apart from the
         dealiasing projection: one conjugate-sandwiched step undoes a
         forward step to near round-off on a resolved smooth field;
  (ii)   energy and norm are conserved through a topological-change
         event at the resonance-safe timestep (the splitting-resonance
         guard dt ~ dx^2 pinned here so it cannot silently regress);
  (iii)  the winding detector finds an imprinted defect quadrupole with
         the right charges and positions;
  (iv)   the exact echo through annihilation recovers the defect set
         and high field fidelity (branch-B death in miniature);
  (v)    an eps-perturbed reversal loses the recovery (the boundary-
         data sensitivity that makes the arrow practical, not
         dynamical).
"""

import math
import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_iii")
sys.path.insert(0, os.path.abspath(SRC))

import reversal_echo as re_  # noqa: E402

L = 96.0
D = 4.0 * re_.XI


def _state(n=256):
    dx = L / n
    med = re_.Medium((n, n), dx)
    psi0 = med.relax(re_.colliding_dipoles_2d(n, dx, D, s=L / 8.0),
                     50, 0.02)
    return med, psi0, dx


def test_stepper_is_T_invertible_one_step():
    """On a spectrally resolved smooth field the conjugate-sandwiched
    step undoes a forward step to round-off: the discrete map is
    exactly T-invertible apart from the dealiasing projection (which a
    smooth low-k field does not touch). A defect-laden field on a
    coarse grid would instead measure mask-shaving -- that effect is
    covered by the refinement ladder, not by this test."""
    n, dx = 128, 0.75
    med = re_.Medium((n, n), dx)
    x = (np.arange(n) - n / 2) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    Lx = n * dx
    psi0 = ((1.0 + 0.02 * np.cos(2 * np.pi * 3 * X / Lx))
            * np.exp(0.02j * np.sin(2 * np.pi * 2 * Y / Lx))).astype(complex)
    dt = 0.05
    psi = med.step(psi0, dt)
    psi = np.conj(med.step(np.conj(psi), dt))
    err = np.max(np.abs(psi - psi0)) / np.max(np.abs(psi0))
    assert err < 1e-12, err


def test_energy_and_norm_conserved_through_event():
    med, psi0, dx = _state(256)
    dt = 0.025                       # k_cut^2 dt/2 = pi/8 guard
    e0, n0 = med.energy(psi0), med.norm(psi0)
    psi = psi0.copy()
    for _ in range(int(48 / dt)):
        psi = med.step(psi, dt)
    drift = abs(med.energy(psi) - e0) / abs(e0)
    ndrift = abs(med.norm(psi) - n0) / n0
    # coarse-grid dealiasing shaves the core spectral tail: bounded and
    # small here, ~0 at N >= 512 (the battery's refinement ladder)
    assert drift < 2e-2, drift
    assert ndrift < 1e-4, ndrift
    assert len(re_.defects_2d(psi, dx)) == 0, "no annihilation?"


def test_winding_detector_finds_quadrupole():
    med, psi0, dx = _state(256)
    d0 = re_.defects_2d(psi0, dx)
    assert len(d0) == 4
    assert sum(q for _, _, q in d0) == 0
    xs = sorted(x for x, _, _ in d0)
    assert xs[0] < -L / 16 and xs[-1] > L / 16


def test_exact_echo_recovers_defects_and_fidelity():
    med, psi0, dx = _state(256)
    dt = 0.025
    n_steps = int(48 / dt)
    d0 = re_.defects_2d(psi0, dx)
    psi_echo = re_.echo_run(med, psi0, n_steps, dt)
    F = re_.fidelity(psi0, psi_echo)
    assert F > 0.999, F
    assert re_.defects_match(d0, re_.defects_2d(psi_echo, dx),
                             tol=2 * re_.XI), "defects not recovered"


def test_perturbed_reversal_linear_response_then_death():
    """Measured finding (recorded per rule 1, against the pre-stated
    expectation of sharp sensitivity): at the single-event scale the
    reversal is ROBUST -- an eps = 1e-3 perturbation of the reversed
    field propagates linearly (no chaotic amplification) and the echo
    still recovers. Recovery dies only at order-unity corruption.
    Pinning both ends keeps the finding from silently regressing."""
    med, psi0, dx = _state(256)
    dt = 0.025
    n_steps = int(48 / dt)
    F_small = re_.fidelity(psi0, re_.echo_run(med, psi0, n_steps, dt,
                                              eps=1e-3))
    assert F_small > 0.995, F_small
    psi_big = re_.echo_run(med, psi0, n_steps, dt, eps=0.5)
    F_big = re_.fidelity(psi0, psi_big)
    assert F_big < 0.9, F_big

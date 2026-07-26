"""Closure tests for the literal Paper-I target audit (#180)."""

import os
import sys

import numpy as np
import sympy as sp

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import ssv_target_audit as audit  # noqa: E402


def test_symbolic_bdg_determinant():
    eps, B = sp.symbols("epsilon B", positive=True, real=True)
    assert sp.simplify(audit.symbolic_dispersion() - eps * (eps - 2 * B)) == 0


def test_printed_positive_B_has_unstable_longwave_band():
    m, B, hbar = 2.0, 0.3, 1.7
    edge = audit.instability_band_edge(m, B, hbar)
    ks = np.array([0.1 * edge, 0.5 * edge, 0.9 * edge])
    assert np.all(audit.nls_bdg_omega2(ks, m, B, hbar) < 0.0)
    assert audit.nls_bdg_omega2(1.01 * edge, m, B, hbar) > 0.0


def test_actual_and_paper_claimed_sound_cones_have_opposite_sign():
    m, B = 1.3, 0.2
    assert audit.actual_longwave_c2(m, B) < 0.0
    assert audit.paper_claimed_c2(m, B) > 0.0
    assert audit.paper_claimed_c2(m, B) == -2.0 * audit.actual_longwave_c2(m, B)


def test_printed_potential_has_negative_compressibility():
    rho, b = 4.0, 0.25
    p0 = audit.pressure_from_printed_potential(rho, b)
    p1 = audit.pressure_from_printed_potential(rho + 1e-6, b)
    assert abs((p1 - p0) / 1e-6 + b) < 1e-8


def test_printed_lagrangian_has_no_unique_physical_action_normalization():
    ledger = audit.printed_dimensions_ledger()
    assert ledger["psi_dimensionless"] is True
    assert ledger["terms_consistent_as_energy_per_reference_element"] is True
    assert ledger["physical_action_density_normalization_specified"] is False
    assert ledger["unique_physical_action_normalization"] is False


def test_run_records_P0_failure():
    report = audit.run()
    assert report["gates"]["P0_action_normalization_unique"] is False
    assert report["gates"]["P0_uniform_background_stable"] is False
    assert report["status"] == "closure-grade"

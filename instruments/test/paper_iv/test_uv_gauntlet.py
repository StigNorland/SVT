"""Tests for #148 UV-GAUNTLET -- pinned formulas and margins.

Fast CPU checks:
  (i)   pinned SSV scales (a_p, E_grain, N0) are internally consistent;
  (ii)  the weak-dispersion formula matches the exact group velocity in
        its domain and the E_QG2 convention match is correct;
  (iii) the photon-decay threshold formula;
  (iv)  the receipt's margins are reproduced and every C1-C4 verdict is
        'falsified-as-written' at the pre-registered >= 2-order rule
        while C5 is the recorded non-exclusion.
"""

import math
import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_iv")
sys.path.insert(0, os.path.abspath(SRC))

import uv_gauntlet as uv  # noqa: E402


def test_pinned_scales_consistent():
    # a_p = hbar/(m_p c); E_grain = hbar c / a_p = m_p c^2; N0 = E_grain/hbar
    assert abs(uv.A_P / 2.1031e-16 - 1.0) < 1e-3
    assert abs(uv.E_GRAIN_GEV / 0.93827 - 1.0) < 1e-3
    assert abs(uv.N0 / 1.4255e24 - 1.0) < 1e-3
    e_from_ap = uv.HBAR * uv.C / uv.A_P / uv.GEV
    assert abs(e_from_ap / uv.E_GRAIN_GEV - 1.0) < 1e-12


def test_weak_dispersion_matches_exact_group_velocity():
    for e in (1e-3, 1e-2, 0.05):
        delta_weak = uv.delta_v_over_c(e)
        delta_exact = uv.vg_over_c_exact(e) - 1.0
        # next-order relative correction is O((k a_p)^2)
        tol = 2.0 * (e / uv.E_GRAIN_GEV) ** 2 + 1e-12
        assert abs(delta_weak / delta_exact - 1.0) < tol


def test_eqg2_convention_match():
    # (3/8)(E/E_grain)^2 == (3/2)(E/E_QG2)^2  =>  E_QG2 = 2 E_grain
    eqg = uv.effective_eqg2()
    assert abs(eqg / (2.0 * uv.E_GRAIN_GEV) - 1.0) < 1e-12
    e = 0.01
    assert abs(0.375 * (e / uv.E_GRAIN_GEV) ** 2
               - 1.5 * (e / eqg) ** 2) < 1e-18


def test_photon_decay_threshold():
    # threshold delta = 2 (m_e c^2 / E)^2
    d = uv.photon_decay_threshold_delta(1.42e6)
    assert abs(d / (2.0 * (uv.M_E_GEV / 1.42e6) ** 2) - 1.0) < 1e-12
    assert d < 1e-18


def test_receipt_margins_and_verdicts():
    r = uv.run()
    c1 = r["C1_ceiling_vs_photons"]
    margins = [row["margin_orders"] for row in c1["rows"]]
    assert min(margins) > 4.0 and max(margins) > 6.0
    assert c1["verdict"] == "falsified-as-written"

    c2 = r["C2_grain_dispersion_vs_GRB_TOF"]
    assert 10.0 < c2["margin_orders"] < 12.0
    assert c2["delta_v_at_31GeV"] > 1.0          # perturbative collapse
    assert c2["verdict"] == "falsified-as-written"

    c3 = r["C3_superluminal_photon_decay"]
    assert c3["margin_orders_above_decay_threshold"] > 25.0
    assert c3["k_a_p"] > 1e5                     # outside perturbative domain
    assert c3["verdict"] == "falsified-as-written"

    c4 = r["C4_collider_compositeness"]
    assert c4["margin_orders_energy"] >= 2.0
    assert c4["margin_orders_length"] >= 2.0
    assert c4["verdict"] == "falsified-as-written"

    c5 = r["C5_lab_lorentz_non_exclusion"]
    assert c5["predicted_anisotropy_signal"] < c5["bound"]
    assert "NOT excluded" in c5["verdict"]

    assert len(r["survivor_requirements"]) == 3
    assert len(r["honesty_clauses"]) == 3

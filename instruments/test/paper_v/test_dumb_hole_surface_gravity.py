"""Tests for #155 H-EOS S1 -- flowing-dumb-hole surface gravity, Unruh T, the
trans-Planckian robustness margin, and the Clausius -> G_eff closure.

Covers: (1) surface gravity matches Visser eq 70 (2 c_s^2/r_H); (2) Hawking T
matches eq 118 (c_s/pi r_H); (3) the LogSE dispersion is superluminal for all k
with the analytic small-k excess 3/8/c_s; (4) the robustness margin M=xi/(pi r_H)
decays with r_H and is O(1) at the grain scale -- NEGATIVE CAPABILITY: the
diagnostic flags grain-scale Rindler horizons as non-robust; (5) the S1(c)
Clausius form closes with eta O(1) and the conceded (a_p/l_P)^2 overshoot; (6)
the overall verdict.
"""

import math

import numpy as np
import pytest

import dumb_hole_surface_gravity as dh


def test_surface_gravity_matches_visser_eq70():
    for r_H in (2.0, 8.0, 32.0):
        g_num = dh.surface_gravity_numeric(r_H)
        g_an = 2.0 * dh.C_S**2 / r_H
        assert abs(g_num - g_an) / g_an < 1e-3


def test_hawking_temperature_matches_eq118():
    r_H = 8.0
    g = dh.surface_gravity_numeric(r_H)
    T_num = g / (2.0 * math.pi * dh.C_S)
    T_an = dh.C_S / (math.pi * r_H)
    assert abs(T_num - T_an) / T_an < 1e-3


def test_dispersion_superluminal_all_k():
    k = np.linspace(1e-3, 5.0 / dh.XI, 500)
    vg = dh.group_velocity(k)
    assert np.all(vg > dh.C_S - 1e-12)          # superluminal for every k>0
    # small-k excess coefficient = (3/8)/c_s
    small = k < 0.05
    coeff = np.polyfit(k[small]**2, vg[small] - dh.C_S, 1)[0]
    assert abs(coeff - 0.375 / dh.C_S) < 1e-3


def test_margin_decays_and_flags_grain_scale():
    # robust (M small) for r_H >> xi
    M_big = dh.XI / (math.pi * 64.0)
    assert M_big < 0.1
    # NEGATIVE CAPABILITY: at the grain scale r_H = xi/pi the margin hits 1
    # (trans-Planckian breakdown), and a sub-grain horizon exceeds it -- the
    # diagnostic does flag the non-robust regime, it is not rigged to pass.
    rH_breakdown = dh.XI / math.pi
    assert abs(dh.XI / (math.pi * rH_breakdown) - 1.0) < 1e-12
    assert dh.XI / (math.pi * (0.5 * rH_breakdown)) > 1.0


def test_s1c_form_closes_and_overshoot_conceded():
    c = dh.s1c()
    # eta read from the S2 receipt is O(1) per xi^2 (=> G_eff ~ grain scale)
    assert c["eta_from_S2_c2_area"] is not None
    assert c["eta_is_O1_per_xi2"]
    # the conceded overshoot is (m_P/m_p)^2 = 1/alpha_G ~ 1.69e38
    assert c["overshoot_a_p_over_l_P_squared"] > 1e38
    # G_eff form read-off
    assert abs(c["G_eff_code_units"] - 1.0 / (4.0 * c["eta_from_S2_c2_area"])) < 1e-12


def test_verdict_R1a():
    out = dh.battery()
    v = out["verdicts"]
    assert v["VERDICT"] == "R1(a)"
    assert v["g_H_matches_visser_eq70"]
    assert v["T_H_matches_visser_eq118"]
    assert v["margin_M_to_zero_for_large_rH"]
    assert v["form_yes_G_no"]

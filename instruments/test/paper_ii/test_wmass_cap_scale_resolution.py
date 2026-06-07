"""Tests for the W-mass cap bending-stiffness resolution (#105).

Pins the four findings:
  E  m_W = pi phi^2 (m_e/alpha^2); m_e/alpha^2 ~ 9.6 GeV; true R_cap ~ 1.633 xi/alpha
     (so the text's 1.70 is stale and phi matches to <1%);
  A  local stiffness is O(1)*alpha^-2; the equilibrium cubic then puts the cap at
     ~alpha^(-2/3) ~ 31 xi -> m_W ~ 1.6 GeV (the 232x gap = one power of 1/alpha);
  B  the ring-scale resolution m_W ~ m_e/alpha^2 (scale derived; pi phi^2 is O(1));
  A' linear lambda_perp running lands lambda_bend within ~5% of phi^3/alpha^3.
"""

import math
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_ii")
if p not in sys.path:
    sys.path.insert(0, p)

import wmass_cap_scale_resolution as w  # noqa: E402


def test_E_mass_scale_and_formula():
    assert abs(w.m_e_over_alpha2_gev() - 9.60) < 0.05
    m_W = math.pi * w.PHI**2 * w.m_e_over_alpha2_gev()
    assert abs(m_W - 78.9) < 0.3                      # the phi-cap prediction
    assert abs(m_W - w.M_W_OBS_GEV) / w.M_W_OBS_GEV < 0.02   # within 1.8% of observed


def test_E_true_Rcap_makes_1p70_stale():
    Rcap = w.true_Rcap_over_xi_alpha()
    assert abs(Rcap - 1.633) < 0.005                  # NOT 1.70
    assert abs(Rcap - w.PHI) / w.PHI < 0.01           # phi matches true cap to <1%


def test_A_gap_is_one_power_of_inverse_alpha():
    assert abs(w.gap_factor() - 232) < 3
    # the gap is structurally (phi^3 / ((J+K)/4)) * (1/alpha)
    structural = (w.PHI**3 / w.JK_OVER_4) * (1.0 / w.ALPHA)
    assert abs(w.gap_factor() - structural) / structural < 1e-6


def test_A_local_bending_gives_wrong_scale():
    R_loc = w.R_equilibrium_xi(w.lambda_bend_local())
    # local equilibrium sits near the alpha^(-2/3) scale, far below the ring scale xi/alpha
    assert 25 < R_loc < 40
    assert R_loc * w.ALPHA < 0.3                       # << 1, i.e. << xi/alpha
    assert w.m_W_from_Rcap(R_loc) < 2.5                # GeV, ~50x too small


def test_A_required_stiffness_recovers_phi_over_alpha():
    R_req = w.R_equilibrium_xi(w.lambda_bend_required())
    assert abs(R_req * w.ALPHA - w.PHI) / w.PHI < 0.05   # 7.7% tau correction band


def test_B_resolution_scale_is_derived():
    # m_W scale is the inherited ring/core ratio squared: m_e (R*/xi)^2 = m_e/alpha^2
    Rstar_over_xi = 1.0 / w.ALPHA
    assert abs(w.m_W_from_Rcap(w.PHI * Rstar_over_xi) - 78.9) < 0.3
    # the residual prefactor is genuinely O(1)
    assert 5 < math.pi * w.PHI**2 < 12


def test_Aprime_linear_running_closes_to_few_percent():
    lam_run = w.lambda_bend_running()
    lam_req = w.lambda_bend_required()
    assert abs(lam_run - lam_req) / lam_req < 0.06     # within ~5%

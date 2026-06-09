"""Tests for #115 "nail it down" — the fully-coupled end-to-end relaxation.

A fast smoke test (coarse grid) of the two load-bearing findings of the complete
relaxation (texture + amplitude + chiral-shear + log-potential, all at once):

  1. The chiral-shear term STABILISES the hopfion — under true monotone descent
     the Hopf charge is preserved (it does not unwind to 0).  So the texture is a
     genuine stable object, not a collapsing transient.
  2. Even fully coupled, the relaxed energy scales O(1) per Q-step, not the ×207
     the lepton masses demand.

The quantitative, better-resolved run (N=40, λ-invariance across λ_⊥∈{1,2,4}) is
in hopf_full_relax.__main__ and the result note; here we just guard the
qualitative verdict cheaply.
"""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from hopf_full_relax import run  # noqa: E402


def test_full_relax_hopf_stable_and_flat():
    r1 = run(1, 1, grid_n=28, half_width=6.0, lam=2.0, dt=1e-4, steps=800)
    r2 = run(2, 1, grid_n=28, half_width=6.0, lam=2.0, dt=1e-4, steps=800)
    # (1) Hopf charge preserved under monotone descent (chiral-shear stabilises).
    assert abs(r1["Qf"]) > 0.7, r1["Qf"]
    assert abs(r2["Qf"]) > 0.7 * 2, r2["Qf"]
    # (2) Monotone descent: energy did not increase.
    assert r1["Ef"] <= r1["E0"] + 1e-6
    assert r2["Ef"] <= r2["E0"] + 1e-6
    # (3) Coupled energy ratio is O(1), not the ×207 the muon needs.
    ratio = r2["Ef"] / r1["Ef"]
    assert ratio < 5.0, ratio
    assert ratio < 0.05 * 206.768

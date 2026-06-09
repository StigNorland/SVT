"""Tests for #115 Gate G3′ — the saturation / log-potential sector.

The last surviving route to a generation mass hierarchy was the LogSE saturation
term acting on a relaxed (depleted) core.  These guard the negative result:
  - the texture forces deeper core depletion at higher Q (A_min decreases), so
    the saturation mechanism IS engaged — this is not a null setup;
  - yet the relaxed energy still scales O(1) per step (≪ the ×207 / ×17 the
    masses demand), because depletion is bounded (ρ ≥ 0).
A future change that made this suddenly look steep enough would be a bug.
"""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

from hopf_saturation_relax import summary  # noqa: E402

GRID_N = 48
HALF = 6.0


def test_g3prime_saturation_engaged_but_too_flat():
    s = summary(GRID_N, HALF)
    rows = s["rows"]
    # The mechanism is genuinely engaged: deeper depletion at higher Q.
    assert rows[0]["A_min"] > rows[1]["A_min"] > rows[2]["A_min"], \
        [r["A_min"] for r in rows]
    # ...and the amplitude really does deplete (core notch forms).
    assert rows[2]["A_min"] < 0.5
    # Yet the energy step is O(1), not the ×207 the muon needs.
    assert s["Etot_ratio_2_1"] < 5.0, s["Etot_ratio_2_1"]
    assert s["Etot_ratio_2_1"] < 0.05 * s["required_mu_over_e"]
    # Even the saturation-only (E_pot) step falls far short.
    assert s["Epot_ratio_2_1"] < 0.1 * s["required_mu_over_e"]

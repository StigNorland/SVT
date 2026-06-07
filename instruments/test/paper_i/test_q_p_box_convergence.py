"""Tests for the Q_p box-convergence gate (#98).

Pins the honest negative: the proton far-field Q_p estimators extracted from the
saved static trefoil states are NOT box-converged and are dominated by a
box-filling / boundary background pedestal, so alpha_G stays blocked. (The #108
box-contamination lesson, in the static gravity sector.)
"""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_i")
if p not in sys.path:
    sys.path.insert(0, p)

import q_p_box_convergence as q  # noqa: E402

DATA = SRC_ROOT.parents[1] / "papers" / "SSV-I" / "data"
BOX_N24 = [DATA / f"trefoil-state-n24-hw{h}-200steps-2026-05-06.npz" for h in (5, 6, 7)]


def test_spread_helper():
    assert abs(q.spread_pct([100, 90, 60]) - q.spread_pct([100, 90, 60])) < 1e-9
    assert q.spread_pct([10, 10, 10]) < 1e-9


def test_qp_is_box_unstable_and_pedestal_dominated():
    rows = [q.state_observables(f) for f in BOX_N24 if f.exists()]
    assert len(rows) == 3
    ev = q.evaluate(rows)
    # box-sweep spread is far above the 5% gate
    assert ev["deficit_volume_spread_pct"] > 20.0
    # the apparent charge is dominated by the box-filling/boundary background
    assert ev["mean_pedestal_fraction"] > 0.8
    # therefore the gate FAILS -> alpha_G stays blocked
    assert ev["passes_gate"] is False

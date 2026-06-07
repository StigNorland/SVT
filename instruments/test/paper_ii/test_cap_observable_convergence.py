"""Tests for the reconnection cap observable (#97).

Pins both findings (fast settings — small grids, short evolution):
  POSITIVE  the threshold-free `moment` radius converges with grid far better
            than the legacy hard-threshold `volume` radius;
  NEGATIVE  the 2-ring harness shows monotonic depletion growth with no
            transient cap (center never depletes, R_cap has no interior peak),
            so the phi cap-geometry ansatz is not testable with it.
"""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_ii")
if p not in sys.path:
    sys.path.insert(0, p)

import cap_observable_convergence as c  # noqa: E402


def test_moment_converges_better_than_volume():
    conv = c.grid_convergence(lam=1.0, T=0.045, ns=(24, 32, 40))
    moment = conv["moment"]["spread_pct"]
    volume = conv["volume"]["spread_pct"]
    assert moment < 5.0                        # grid-stable to a few percent
    assert moment < 0.3 * volume               # far better than the legacy hard count


def test_no_transient_cap_in_two_ring_harness():
    tr = c.dynamics_trace(n=24, lam=1.0, T=0.03, frames=15)
    # the geometric centre never depletes (|psi| does not drop below its start)
    assert tr["center_abs"][-1] >= tr["center_abs"][0] - 1e-6
    # depletion and cap radius grow monotonically: no interior peak => no transient cap
    assert not c.has_interior_peak(tr["rcap"])
    assert not c.has_interior_peak(tr["sum_w"])


def test_has_interior_peak_detector():
    assert c.has_interior_peak([1.0, 2.0, 3.0, 1.0])      # rises then falls
    assert not c.has_interior_peak([1.0, 2.0, 3.0, 4.0])  # monotonic rise

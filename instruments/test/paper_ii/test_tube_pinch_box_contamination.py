"""Box-contamination diagnostic for the tube-pinch cap (#108 / #97).

The negative `R_cap ∝ √λ_⊥` scaling in #108 turns out to be a box artefact, not a
falsification of ring-inheritance: at FIXED dx and FIXED physics (throat
R0 = κ√λ ξ held constant), enlarging the box makes the measured cap radius grow
and its localization collapse — the "cap" tracks the box, not the throat. This
pins the large free-intercept floor (B≈5ξ) seen in the scaling fit as box-scale.
"""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_ii")
if p not in sys.path:
    sys.path.insert(0, p)

import tube_pinch_cap_harness as h  # noqa: E402


def test_cap_radius_tracks_the_box_not_the_throat():
    # same dx (=0.75) and same physics across all three; only the box grows
    sweep = h.box_contamination_sweep(
        [(18, 24), (27, 36), (36, 48)],
        lambda_perp=2.0, kappa=3.0, tube_half_length_factor=0.08,
        edge_width=0.5, pinch_kick=1.5, duration=0.025, snapshots=21,
    )
    throats = {round(s["throat_radius"], 6) for s in sweep}
    assert len(throats) == 1                     # physics genuinely held fixed
    R = [s["max_radius"] for s in sweep]
    loc = [s["localization"] for s in sweep]
    assert R[0] < R[1] < R[2]                    # radius tracks the box
    assert R[-1] > 1.6 * R[0]                    # ... and grows substantially
    assert loc[0] > loc[-1]                      # localization degrades with box
    assert not sweep[-1]["cap_exists"]           # cap-event gate fails in a big box

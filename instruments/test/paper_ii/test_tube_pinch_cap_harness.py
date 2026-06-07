"""Tests for the Paper II #108 tube-pinch cap harness."""

import math
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_ii")
if p not in sys.path:
    sys.path.insert(0, p)

import tube_pinch_cap_harness as h  # noqa: E402


def test_throat_radius_tracks_sqrt_lambda():
    cfg1 = h.TubePinchConfig(lambda_perp=1.0, kappa=3.0)
    cfg4 = h.TubePinchConfig(lambda_perp=4.0, kappa=3.0)
    assert math.isclose(cfg4.throat_radius / cfg1.throat_radius, 2.0)


def test_fixed_radius_control_does_not_track_lambda():
    cfg1 = h.TubePinchConfig(lambda_perp=1.0, fixed_radius=3.0)
    cfg4 = h.TubePinchConfig(lambda_perp=4.0, fixed_radius=3.0)
    assert cfg1.throat_radius == cfg4.throat_radius == 3.0


def test_event_gate_accepts_transient_localized_cap():
    metrics = [
        {"cap_radius": 2.0, "cap_plane_depletion": 10.0, "localization_fraction": 0.20},
        {"cap_radius": 3.0, "cap_plane_depletion": 20.0, "localization_fraction": 0.25},
        {"cap_radius": 2.1, "cap_plane_depletion": 12.0, "localization_fraction": 0.22},
    ]
    decision = h.decide_cap_event(metrics)
    assert decision.cap_exists
    assert decision.peak_index == 1


def test_event_gate_rejects_monotonic_spread():
    metrics = [
        {"cap_radius": 2.0, "cap_plane_depletion": 10.0, "localization_fraction": 0.20},
        {"cap_radius": 3.0, "cap_plane_depletion": 20.0, "localization_fraction": 0.25},
        {"cap_radius": 4.0, "cap_plane_depletion": 30.0, "localization_fraction": 0.22},
    ]
    decision = h.decide_cap_event(metrics)
    assert not decision.cap_exists
    assert "no interior cap peak" in decision.reason


def test_cap_localization_uses_physical_slab_not_grid_slice():
    cfg = h.TubePinchConfig(n=16, fixed_radius=2.0, lambda_perp=0.0)
    base = cfg.base_config()
    psi = h.tube_pinch_initial_state(cfg)
    metrics = h.cap_plane_metrics(psi, base)
    assert metrics["cap_plane_depletion"] >= metrics["cap_slice_depletion"]
    assert metrics["localization_fraction"] > 0.0


def test_tube_pinch_trace_schema_fast():
    cfg = h.TubePinchConfig(
        n=16,
        lambda_perp=1.0,
        kappa=2.0,
        duration=0.002,
        snapshots=3,
        stability_safety=0.5,
    )
    trace = h.trace_tube_pinch(cfg)
    assert trace["steps"] >= 2
    assert len(trace["metrics"]) == 3
    assert "cap_exists" in trace["decision"]
    assert trace["effective_dt"] > 0.0


def test_worker_case_schema_fast():
    cfg = h.TubePinchConfig(
        n=16,
        lambda_perp=0.0,
        fixed_radius=2.0,
        duration=0.001,
        snapshots=3,
    )
    rows = h._run_cases_parallel([("test", cfg, "control")], workers=1)
    assert len(rows) == 1
    assert rows[0]["ansatz"] == "test"
    assert rows[0]["control"] == "control"
    assert "cap_exists" in rows[0]["decision"]


def test_scaling_scan_accepts_custom_small_grid():
    result = h.scaling_scan(
        workers=1,
        lambdas=(0.5, 1.0, 2.0),
        ns=(16,),
        duration=0.001,
        snapshots=3,
    )
    assert result["n_values"] == [16]
    assert result["lambdas"] == [0.5, 1.0, 2.0]
    assert len(result["rows"]) == 3
    assert "16" in result["fits_by_n"]

"""Tests for #147 DSPH-LEDGER -- the dwarf-spheroidal discriminator.

Fast CPU checks:
  (i)   pinned data integrity (8 classical dwarfs, McConnachie values);
  (ii)  Wolf estimator + model arithmetic (model A at the H9 MW reference
        ~ 124 km/s; model B normalization);
  (iii) verdict logic hits each pre-registered B1 branch on synthetic
        ledgers;
  (iv)  the real ledger runs, rules evaluate, and the receipt is coherent
        (budget ratios positive, B3 count in range, sweep present).
"""

import math
import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "paper_vi")
sys.path.insert(0, os.path.abspath(SRC))

import dsph_ledger as dl  # noqa: E402


def test_pinned_data_integrity():
    assert len(dl.DSPH) == 8
    names = [d[0] for d in dl.DSPH]
    for n in ("Fornax", "Draco", "Sculptor", "Ursa Minor"):
        assert n in names
    for _, lv6, sigma, re_pc in dl.DSPH:
        assert 0.1 < lv6 < 50 and 5 < sigma < 13 and 150 < re_pc < 800


def test_model_a_at_mw_reference():
    # log10 v_h = 0.256 * log10(6e10) - 0.665 -> ~124 km/s
    assert abs(dl.model_a_vh(dl.M_MW) / 124.2 - 1.0) < 0.01


def test_model_b_normalization():
    # at the MW reference point itself, model B = model A by construction
    vb = dl.model_b_vh(dl.R_MW_KPC, dl.V_MW)
    assert abs(vb / dl.model_a_vh(dl.M_MW) - 1.0) < 1e-12


def test_wolf_estimator_arithmetic():
    r = dl.dwarf_row("X", 1.0, 9.0, 300.0, ml=1.6, vrot=3.0)
    assert abs(r["v_c_kms"] - math.sqrt(3.0) * 9.0) < 1e-9
    assert abs(r["r_half_pc"] - 400.0) < 1e-9
    vbar2 = dl.G_PC * (1.6e6 / 2.0) / 400.0
    assert abs(r["v_bar_kms"] ** 2 - vbar2) < 1e-9
    assert r["v_h_obs_kms"] < r["v_c_kms"]


def _fake(delta_a, delta_b, below=0):
    rows = []
    for i in range(8):
        rows.append({"delta_A_dex": delta_a, "delta_B_dex": delta_b,
                     "below_half_sigma": i < below,
                     "budget_ratio": 1e15})
    return rows


def test_b1_branches():
    v = dl.verdicts(_fake(0.2, 2.7))
    assert v["B1"].startswith("rotation-proportional entrainment FALSIFIED")
    v = dl.verdicts(_fake(-0.8, 2.7))
    assert "below relation" in v["B1"]
    v = dl.verdicts(_fake(0.8, 2.7))
    assert "under-predicts" in v["B1"]
    v = dl.verdicts(_fake(0.2, 1.0))
    assert v["B1"] == "inconclusive on pre-registered thresholds"


def test_b3_threshold():
    assert dl.verdicts(_fake(0.2, 2.7, below=6))["B3"].startswith(
        "universal kpc-scale core FALSIFIED")
    assert dl.verdicts(_fake(0.2, 2.7, below=5))["B3"].startswith(
        "universal core survives")


def test_real_ledger_runs_and_is_coherent():
    receipt = dl.main(quick=True)
    rows = receipt["baseline_ledger"]
    assert len(rows) == 8
    for r in rows:
        assert r["budget_ratio"] > 0
        assert r["v_h_obs_kms"] > 0
        assert r["v_h_modelB_upper_kms"] < r["v_h_modelA_kms"]
    v = receipt["verdicts"]
    assert 0 <= v["B3_n_below_half_sigma"] <= 8
    assert len(receipt["sweep"]) == 27
    assert isinstance(receipt["B1_sweep_stable"], bool)


def _receipt_floats(obj):
    """Every float the receipt writes, skipping bools (which are ints in Python)."""
    if isinstance(obj, bool):
        return
    if isinstance(obj, float):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _receipt_floats(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _receipt_floats(v)


def test_receipt_is_stable_under_environment_drift():
    """The receipt is tracked and the suite rewrites it, so instability is churn.

    Two runs on one machine are byte-identical -- the arithmetic is
    deterministic -- but results move by up to ~4e-15 relative *across*
    environments (BLAS/CPU reduction order). Unrounded, that moved 25 of the 259
    floats and dirtied the working tree five times during the #198 work, once
    getting swept into an unrelated commit by `git add -A`.

    Rounding is monotonic, so testing both ends of the drift interval against
    every value is exact rather than statistical: if neither endpoint moves the
    written value, nothing inside the interval does.
    """
    receipt = dl.main(quick=True)
    values = [v for v in _receipt_floats(receipt)
              if v != 0.0 and math.isfinite(v)]
    assert len(values) > 200, "receipt unexpectedly small; test would prove little"

    def written(x):
        return float(f"{x:.{dl.RECEIPT_SIGFIGS}g}")

    drift = 100 * 4e-15          # 100x the worst drift actually observed
    moved = [x for x in values
             if written(x * (1 + drift)) != written(x)
             or written(x * (1 - drift)) != written(x)]
    assert not moved, (
        f"{len(moved)} receipt value(s) sit within {drift:.0e} relative of a "
        f"rounding boundary at {dl.RECEIPT_SIGFIGS} s.f., so the tracked file "
        f"can churn across environments: {moved[:5]}")


def test_rounding_actually_changes_what_is_written():
    """Guard on the guard: if _stable stopped rounding, the test above would
    still pass on today's values, so assert the rounding is real."""
    assert dl._stable(1.0 / 3.0) != 1.0 / 3.0
    assert dl._stable(1.0 / 3.0) == float(f"{1/3:.{dl.RECEIPT_SIGFIGS}g}")
    # bools must survive as bools, not become 1/0
    assert dl._stable({"flag": True})["flag"] is True
    assert dl._stable([1, 2.5]) == [1, 2.5]

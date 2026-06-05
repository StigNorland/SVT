"""Regression tests for #80 Pass 4: SO(10) 16 = one anomaly-free generation."""

from so10_generation_embedding import (
    ONE_GENERATION,
    anomaly_sums,
    electric_charge_sum,
    so10_16_weights,
    so10_16bar_weights,
    ssv_charge_audit,
    total_states,
)


def test_spinor_weight_counts():
    assert len(so10_16_weights()) == 16          # even parity
    assert len(so10_16bar_weights()) == 16        # odd parity
    assert len(so10_16_weights()) + len(so10_16bar_weights()) == 32


def test_even_parity_defines_the_16():
    for w in so10_16_weights():
        assert w.count(-1) % 2 == 0
    for w in so10_16bar_weights():
        assert w.count(-1) % 2 == 1


def test_one_generation_has_16_states():
    assert total_states() == 16


def test_all_anomalies_cancel():
    # the whole point: one generation = one anomaly-free irrep
    for name, val in anomaly_sums().items():
        assert abs(val) < 1e-12, f"{name} = {val} (should vanish)"


def test_electric_charge_sums_to_zero():
    assert abs(electric_charge_sum()) < 1e-12


def test_hypercharge_cube_anomaly_explicit():
    # independent recomputation of sum Y^3 to guard the convention
    s = sum(f.hypercharge_Y**3 * f.multiplicity for f in ONE_GENERATION)
    assert abs(s) < 1e-12


def test_b_minus_L_separates_quarks_and_leptons():
    for f in ONE_GENERATION:
        if f.color_label in ("3", "3bar"):
            assert abs(abs(f.B_minus_L) - 1/3) < 1e-12   # quarks: |B-L| = 1/3
        else:
            assert abs(abs(f.B_minus_L) - 1.0) < 1e-12   # leptons: |B-L| = 1


def test_audit_has_no_absent_charges():
    audit = ssv_charge_audit()
    statuses = [a.status for a in audit]
    assert "ABSENT" not in statuses
    assert statuses.count("PRESENT") == 2                 # both colour Cartan
    assert statuses.count("TOPOLOGICAL-CANDIDATE") == 1   # B-L
    # 5 Cartan charges (2 colour + T3 + Y + B-L) + 1 chirality Z2 label = 6 rows
    assert len(audit) == 6
    cartan = [a for a in audit if "chirality" not in a.cartan_charge.lower()]
    assert len(cartan) == 5                               # rank SO(10) = 5

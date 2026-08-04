"""Focused tests for the issue-230 matched-dwarf audit."""

import copy
import os
import sys

import pytest

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import matched_dwarf_audit as audit  # noqa: E402


def test_internal_proxies_have_expected_dimensions_and_scaling():
    first = audit.baryonic_quantities(1.0e8, 5.0e8, 2.0)
    doubled_mass = audit.baryonic_quantities(2.0e8, 1.0e9, 2.0)
    doubled_radius = audit.baryonic_quantities(1.0e8, 5.0e8, 4.0)
    assert doubled_mass["gamma_dyn_gyr_inv"] / first["gamma_dyn_gyr_inv"] == pytest.approx(2**0.5)
    assert doubled_radius["gamma_dyn_gyr_inv"] / first["gamma_dyn_gyr_inv"] == pytest.approx(2**-1.5)
    assert first["gamma_gas_gyr_inv"] == pytest.approx(first["fgas"] * first["gamma_dyn_gyr_inv"])


def test_control_selection_does_not_depend_on_rotation_amplitude():
    table = audit.parse_sparc_table()
    curves = audit.parse_mass_models(audit.SPARC_CURVES)
    original = audit.select_controls(table, curves)
    changed = copy.deepcopy(table)
    for row in changed.values():
        if row["Vflat"] > 0:
            row["Vflat"] *= 3.0
    modified = audit.select_controls(changed, curves)
    assert modified == original
    assert "DDO154" in original[0]


def test_homogeneous_udg_quality_exclusion_is_frozen():
    robust = [galaxy.name for galaxy in audit.UDGS if galaxy.robust]
    excluded = [galaxy.name for galaxy in audit.UDGS if not galaxy.robust]
    assert len(robust) == 5
    assert excluded == ["AGC749290"]


def test_wls_recovers_exact_proxy_relation_with_full_rank():
    rows = []
    for index, gamma in enumerate((0.2, 0.4, 0.8, 1.6, 3.2)):
        rows.append({
            "name": f"g{index}", "source_class": "UDG" if index < 2 else "SPARC",
            "gamma_dyn_gyr_inv": gamma, "gamma_gas_gyr_inv": 0.8 * gamma,
            "fgas": 0.8, "log10_dout": 0.3 + 1.7 * __import__("math").log10(gamma),
            "sigma_log10_dout": 0.1,
        })
    fit = audit.fit_wls(rows, ("log10_gamma_dyn",))
    assert fit["full_rank"]
    assert fit["coefficients"] == pytest.approx([0.3, 1.7])
    assert fit["chi2"] == pytest.approx(0.0, abs=1e-20)


def test_geometry_sensitivity_has_physical_direction():
    table = audit.parse_sparc_table()
    curves = audit.parse_mass_models(audit.SPARC_CURVES)
    controls, _ = audit.select_controls(table, curves)
    row = audit.build_summary_rows(controls, table, curves)[0]
    low = audit.geometry_variant([row], "inclination_low")[0]
    high = audit.geometry_variant([row], "inclination_high")[0]
    distance_low = audit.geometry_variant([row], "distance_low")[0]
    distance_high = audit.geometry_variant([row], "distance_high")[0]
    assert low["dout"] > row["dout"] > high["dout"]
    assert distance_low["dout"] > row["dout"] > distance_high["dout"]


def test_gate_order_prevents_support_without_common_radial_contract():
    report = audit.run(include_radial=False)
    assert report["decision"] == "UNSUPPORTED"
    assert not report["gate_A"]["common_radial_contract"]
    assert not report["gate_B"]["internal_update_support"]
    assert not report["gate_C"]["activated"]
    assert not report["gate_C"]["shared_screen_support"]
    assert report["radial_fits"] == []


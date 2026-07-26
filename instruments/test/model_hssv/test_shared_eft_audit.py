"""Independent-sector controls for the issue-180 shared EFT."""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_hssv")
sys.path.insert(0, os.path.abspath(SRC))

import shared_eft_audit as shared  # noqa: E402


def test_one_standard_model_generation_is_anomaly_free():
    assert shared.u1_cubic_anomaly() == 0
    assert shared.mixed_gravity_u1_anomaly() == 0
    assert shared.su2_squared_u1_anomaly() == 0
    assert shared.su3_squared_u1_anomaly() == 0
    assert shared.su3_cubic_anomaly_units() == 0
    assert shared.su2_doublet_count() % 2 == 0
    assert shared.anomaly_free() is True


def test_scalar_goldstone_does_not_supply_transverse_photon_helicities():
    dof = shared.independent_sector_dof()
    assert dof["complex_scalar_goldstones"] == 1
    assert dof["maxwell_photon_helicities"] == 2
    assert shared.scalar_can_supply_photon_helicities() is False

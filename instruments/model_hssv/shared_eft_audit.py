"""Degree-of-freedom and anomaly controls for issue #180.

This does not claim emergence.  It checks the deliberately weaker control in
which Einstein gravity, Maxwell/Yang-Mills fields, and one Standard-Model
generation are independently supplied in a common covariant EFT.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any


LEFT_HANDED_WEYL = (
    # name, multiplicity, hypercharge
    ("Q_L", 6, Fraction(1, 6)),
    ("u_R^c", 3, Fraction(-2, 3)),
    ("d_R^c", 3, Fraction(1, 3)),
    ("L_L", 2, Fraction(-1, 2)),
    ("e_R^c", 1, Fraction(1, 1)),
)


def u1_cubic_anomaly() -> Fraction:
    return sum((mult * hypercharge ** 3
                for _, mult, hypercharge in LEFT_HANDED_WEYL), Fraction())


def mixed_gravity_u1_anomaly() -> Fraction:
    return sum((mult * hypercharge
                for _, mult, hypercharge in LEFT_HANDED_WEYL), Fraction())


def su2_squared_u1_anomaly() -> Fraction:
    # Three colored Q_L doublets and one lepton doublet; T(fund)=1/2.
    return 3 * Fraction(1, 6) * Fraction(1, 2) + (
        Fraction(-1, 2) * Fraction(1, 2)
    )


def su3_squared_u1_anomaly() -> Fraction:
    # Two Q_L SU(2) components, plus the left-handed conjugates u^c,d^c.
    return (
        2 * Fraction(1, 6) * Fraction(1, 2)
        + Fraction(-2, 3) * Fraction(1, 2)
        + Fraction(1, 3) * Fraction(1, 2)
    )


def su3_cubic_anomaly_units() -> int:
    """Triplet-minus-antitriplet units: 2 Q components - u^c - d^c."""
    return 2 - 1 - 1


def su2_doublet_count() -> int:
    """Number of left Weyl SU(2) doublets; even means no Witten anomaly."""
    return 3 + 1


def anomaly_free() -> bool:
    return (
        u1_cubic_anomaly() == 0
        and mixed_gravity_u1_anomaly() == 0
        and su2_squared_u1_anomaly() == 0
        and su3_squared_u1_anomaly() == 0
        and su3_cubic_anomaly_units() == 0
        and su2_doublet_count() % 2 == 0
    )


def scalar_can_supply_photon_helicities() -> bool:
    """A single complex-scalar Goldstone is one spin-0 mode, not helicity +/-1."""
    return False


def independent_sector_dof() -> dict[str, int]:
    return {
        "massless_graviton_helicities": 2,
        "maxwell_photon_helicities": 2,
        "complex_scalar_goldstones": 1,
    }


def run() -> dict[str, Any]:
    return {
        "issue": 180,
        "instrument": "shared_eft_audit",
        "status": "closure-grade",
        "anomalies": {
            "U1_cubed": str(u1_cubic_anomaly()),
            "gravity_squared_U1": str(mixed_gravity_u1_anomaly()),
            "SU2_squared_U1": str(su2_squared_u1_anomaly()),
            "SU3_squared_U1": str(su3_squared_u1_anomaly()),
            "SU3_cubed_units": su3_cubic_anomaly_units(),
            "SU2_doublets": su2_doublet_count(),
            "all_cancel": anomaly_free(),
        },
        "degrees_of_freedom": independent_sector_dof(),
        "scalar_supplies_transverse_photon": scalar_can_supply_photon_helicities(),
        "interpretation": (
            "Independent Einstein/Maxwell/anomaly-free chiral sectors are "
            "ordinary compatible EFT ingredients, but inserting them is K2 "
            "structure and cannot repair the unstable literal SSV scalar."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))

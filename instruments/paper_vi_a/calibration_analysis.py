"""Numerical checks for the SSV-VI-a calibration constant C (RETIRED CLAIM).

The CBH standing-wave mechanism C calibrated is falsified (#122/#124); see
the falsification appendix of papers/SSV-VI.  The original VI-a text lives
in git history.  Kept as the record of:

1. the empirical central-value check C = Delta r * M_BH for the five-galaxy
   table of the retired VI-a manuscript;
2. the closed-form value derived in derive_C.py, reproduced here only as a
   consistency check.

Failed exploratory routes based on flat velocity, healing length, or acoustic
matching were moved to
instruments/_fitted_quarantine/paper_vi_a/calibration_analysis_failed_exploration.py.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# CODATA constants.
HBAR = 1.054571817e-34
C_LIGHT = 2.99792458e8
ALPHA = 7.2973525693e-3
G = 6.67430e-11
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27

# Conversions.
M_SUN = 1.98892e30
KPC = 3.0856775815e19


@dataclass(frozen=True)
class GalaxyAnchor:
    name: str
    m_bh_1e8_msun: float
    delta_r_kpc: float

    @property
    def m_bh_msun(self) -> float:
        return self.m_bh_1e8_msun * 1.0e8

    @property
    def c_inferred_1e9(self) -> float:
        return self.m_bh_msun * self.delta_r_kpc / 1.0e9


GALAXIES = (
    GalaxyAnchor("NGC 224 (M31)", 1.4, 12.9),
    GalaxyAnchor("NGC 3031 (M81)", 0.70, 26.0),
    GalaxyAnchor("NGC 4736", 0.10, 180.0),
    GalaxyAnchor("NGC 2903", 0.03, 600.0),
    GalaxyAnchor("Milky Way", 0.043, 420.0),
)


def derived_c_kg_m() -> float:
    alpha_g = G * M_P**2 / (HBAR * C_LIGHT)
    n_p = (M_P / M_E) * ALPHA
    return HBAR * n_p**9 / (2.0 * alpha_g * C_LIGHT * ALPHA**25)


def main() -> None:
    print("SSV-VI-a calibration constant C")
    print("=" * 72)
    print(f"{'Galaxy':<18} {'M_BH (1e8 Msun)':>16} {'Delta r (kpc)':>14} {'C (1e9 kpc Msun)':>20}")
    print("-" * 72)

    inferred = []
    for galaxy in GALAXIES:
        inferred.append(galaxy.c_inferred_1e9)
        print(
            f"{galaxy.name:<18} {galaxy.m_bh_1e8_msun:>16.3f} "
            f"{galaxy.delta_r_kpc:>14.1f} {galaxy.c_inferred_1e9:>20.3f}"
        )

    mean = math.fsum(inferred) / len(inferred)
    sample_std = math.sqrt(math.fsum((x - mean) ** 2 for x in inferred) / (len(inferred) - 1))
    c_derived_1e9 = derived_c_kg_m() / (KPC * M_SUN) / 1.0e9
    rel = (c_derived_1e9 - mean) / mean

    print("-" * 72)
    print(f"Mean of listed central values: {mean:.3f}e9 kpc Msun")
    print(f"Sample scatter of central values: {sample_std:.3f}e9 kpc Msun")
    print()
    print(f"Closed-form C from derive_C.py: {c_derived_1e9:.3f}e9 kpc Msun")
    print(f"Relative to listed-value mean: {rel * 100:+.2f}%")
    print()
    print("Note: the manuscript treats the galaxy spacings as approximate anchors,")
    print("not as a precision weighted measurement of C.")


if __name__ == "__main__":
    main()

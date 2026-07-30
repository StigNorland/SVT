"""Issue #220 control: corrected versus legacy L_perp core integrals.

The active Paper I profile is the coefficient-one conventional-healing-length
solution.  The coefficient-two implementation remains only as an explicitly
named legacy control.  The exact coordinate relation

    f_corrected(r) = f_legacy(r / sqrt(2))

predicts

    I_curl_corrected = I_curl_legacy / 2,
    J_bend_corrected = J_bend_legacy / 2,
    K_bend_corrected = K_bend_legacy.

Both profiles are integrated independently.  This script checks the prediction
instead of maintaining a second copy of the coefficient-one ODE solver.
"""

from __future__ import annotations

import math
import sys

import numpy as np

sys.path.insert(0, "instruments/paper_i")

from corrected_vortex_profile import CorrectedVortexProfile  # noqa: E402
from vortex_profile import VortexProfile as LegacyVortexProfile  # noqa: E402

from lperp_core_integral import compute_core_integrals  # noqa: E402


ALPHA = 1.0 / 137.035999084
PHI = (1.0 + math.sqrt(5.0)) / 2.0
R_MAX = 15.0
N_PROFILE = 6000


def profile_integrals(profile_type):
    """Solve one profile class and return its slope and three core integrals."""
    profile = profile_type.solve(
        x_min=1.0e-4,
        x_max=R_MAX,
        n=N_PROFILE,
    )
    r = np.asarray(profile.xs)
    f = np.asarray(profile.fs)
    fp = np.asarray(profile.fps)
    return profile.slope, compute_core_integrals(r, f, fp, R_MAX)


def main() -> None:
    legacy_slope, legacy = profile_integrals(LegacyVortexProfile)
    corrected_slope, corrected = profile_integrals(CorrectedVortexProfile)
    ic_legacy, jb_legacy, kb_legacy = legacy
    ic_corrected, jb_corrected, kb_corrected = corrected

    print("=" * 72)
    print("Issue #220 — corrected versus legacy L_perp profile control")
    print("=" * 72)
    print()
    print("Legacy coefficient-two control:")
    print(f"  slope = {legacy_slope:.8f}")
    print(f"  I_curl = {ic_legacy:.6f}")
    print(f"  J_bend = {jb_legacy:.6f}")
    print(f"  K_bend = {kb_legacy:.6f}")
    print()
    print("Corrected coefficient-one baseline:")
    print(f"  slope = {corrected_slope:.8f}")
    print(f"  I_curl = {ic_corrected:.6f}")
    print(f"  J_bend = {jb_corrected:.6f}")
    print(f"  K_bend = {kb_corrected:.6f}")
    print(f"  (J+K)/4 = {(jb_corrected + kb_corrected) / 4.0:.6f}")
    print()

    predictions = {
        "I_curl": ic_legacy / 2.0,
        "J_bend": jb_legacy / 2.0,
        "K_bend": kb_legacy,
    }
    observed = {
        "I_curl": ic_corrected,
        "J_bend": jb_corrected,
        "K_bend": kb_corrected,
    }
    print("Exact-rescaling negative control:")
    for name in ("I_curl", "J_bend", "K_bend"):
        drift = 100.0 * (observed[name] / predictions[name] - 1.0)
        print(
            f"  {name:7s}: predicted={predictions[name]:.6f}, "
            f"direct={observed[name]:.6f}, drift={drift:+.4f}%"
        )
    print()

    lam_perp = ALPHA**-2
    lam_required = PHI**3 / ALPHA**3
    lam_local_legacy = lam_perp * (jb_legacy + kb_legacy) / 4.0
    lam_local_corrected = lam_perp * (jb_corrected + kb_corrected) / 4.0
    print("Local bending verdict:")
    print(
        f"  legacy gap    = {lam_required / lam_local_legacy:.1f}x "
        "(control only)"
    )
    print(f"  corrected gap = {lam_required / lam_local_corrected:.1f}x")
    print()
    print(
        "VERDICT: the convention correction increases the local-bending "
        "shortfall; the qualitative no-local-equilibrium result survives."
    )


if __name__ == "__main__":
    main()

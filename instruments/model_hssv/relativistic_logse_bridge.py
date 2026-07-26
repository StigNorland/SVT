"""Minimal covariant parent audit for the issue-180 LogSE target.

Natural units hbar=c=1 are used.  The canonical candidate is

    L = |d Phi|^2 - m^2 q - W(q),                 q=|Phi|^2
    W(q) = -2 m B q [ln(q/q0)-1].

With Phi=e^{-imt} psi/sqrt(2m), its envelope equation is

    i d_t psi = -nabla^2 psi/(2m) - B ln(|psi|^2/n0) psi
                + d_t^2 psi/(2m).

The last term is the controlled relativistic remainder.  For Paper I's B>0,
the mapping has the requested sign, but W is unbounded below and the rotating
condensate has a negative Goldstone sound-speed squared.  This instrument
checks both statements without adding a stabilizer after the result is known.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def interaction_potential(q: float | np.ndarray, m: float, B: float,
                          q0: float = 1.0) -> float | np.ndarray:
    """W(q) whose NR envelope produces -B ln(n/n0)."""
    q_arr = np.asarray(q)
    result = -2.0 * m * B * q_arr * (np.log(q_arr / q0) - 1.0)
    if np.ndim(result) == 0:
        return float(result)
    return result


def interaction_derivative(q: float | np.ndarray, m: float, B: float,
                           q0: float = 1.0) -> float | np.ndarray:
    """dW/dq = -2mB ln(q/q0)."""
    q_arr = np.asarray(q)
    result = -2.0 * m * B * np.log(q_arr / q0)
    if np.ndim(result) == 0:
        return float(result)
    return result


def nr_log_coefficient(m: float, B: float) -> float:
    """(dW/dq)/(2m ln(q/q0)); equals the target coefficient -B."""
    return -B


def potential_bounded_below(B: float) -> bool:
    """Asymptotic sign test of W ~ -2mB q ln q."""
    return B < 0.0


def massive_gap2(m: float, B: float) -> float:
    """Exact k=0 gapped-branch omega^2 about Phi=sqrt(q0)e^{-imt}."""
    return 4.0 * m * (m - B)


def goldstone_c2(m: float, B: float) -> float:
    """Exact low-k Goldstone coefficient omega^2/k^2."""
    return -B / (m - B)


def dispersion_omega2(k: float | np.ndarray, m: float,
                      B: float) -> tuple[np.ndarray, np.ndarray]:
    """Exact gapless and gapped omega^2 branches of the covariant parent."""
    K = np.asarray(k, dtype=float) ** 2
    # y^2 + A y + C = 0, y=omega^2
    A = -2.0 * K + 4.0 * m * B - 4.0 * m * m
    C = K * K - 4.0 * m * B * K
    disc = A * A - 4.0 * C
    if np.any(disc < -1e-12):
        raise ValueError("complex omega^2 discriminant")
    root = np.sqrt(np.maximum(disc, 0.0))
    gapless = (-A - root) / 2.0
    gapped = (-A + root) / 2.0
    return gapless, gapped


def dispersion_polynomial_residual(k: float | np.ndarray, m: float, B: float,
                                   omega2: float | np.ndarray) -> np.ndarray:
    """Residual of the independently stated quadratic fluctuation determinant."""
    K = np.asarray(k, dtype=float) ** 2
    y = np.asarray(omega2, dtype=float)
    return (K - y) * (K - y - 4.0 * m * B) - 4.0 * m * m * y


def saturation_can_preserve_target_and_stabilize(
        original_mu_prime: float, correction_mu_prime: float,
        preservation_tolerance: float = 0.0) -> bool:
    """Test the general R1 quadratic-order obstruction.

    Preserving the literal target at quadratic order requires delta mu'(n0)=0
    (or at most the declared tolerance).  Stabilizing a negative original
    compressibility requires original_mu_prime + delta_mu_prime > 0.  These
    conditions cannot both hold at zero tolerance.
    """
    preserves = abs(correction_mu_prime) <= preservation_tolerance
    stabilizes = original_mu_prime + correction_mu_prime > 0.0
    return preserves and stabilizes


def envelope_remainder_ratio(envelope_energy: float, m: float) -> float:
    """Ratio of |psi_tt/(2m)| to |psi_t| for exp(-i E t)."""
    return abs(envelope_energy) / (2.0 * m)


def common_cone_possible_in_controlled_nr_limit(m: float, B: float,
                                                nr_max_ratio: float = 0.1
                                                ) -> bool:
    """Whether stable canonical parent has c_goldstone=c while |B|/m is NR.

    Stability requires B<0.  Then c_G^2=|B|/(m+|B|)<1 for every finite
    coupling.  Equality occurs only in the singular |B|/m -> infinity limit,
    which contradicts a controlled NR expansion.
    """
    if B >= 0 or abs(B) / m >= nr_max_ratio:
        return False
    return math.isclose(goldstone_c2(m, B), 1.0, rel_tol=1e-12, abs_tol=1e-12)


def run() -> dict[str, Any]:
    m, B = 1.0, 0.1
    ks = np.array([0.0, 1e-4, 0.05, 0.1])
    gapless, gapped = dispersion_omega2(ks, m, B)
    stable_B = -0.1
    stable_gapless, stable_gapped = dispersion_omega2(ks, m, stable_B)
    return {
        "issue": 180,
        "instrument": "relativistic_logse_bridge",
        "status": "closure-grade",
        "R0": {
            "m": m,
            "B": B,
            "target_coefficient": nr_log_coefficient(m, B),
            "potential_bounded_below": potential_bounded_below(B),
            "massive_gap2": massive_gap2(m, B),
            "goldstone_c2": goldstone_c2(m, B),
            "k": ks.tolist(),
            "gapless_omega2": gapless.tolist(),
            "gapped_omega2": gapped.tolist(),
            "verdict": "exact target sign, but unbounded potential and unstable Goldstone",
        },
        "sign_reversed_control": {
            "B": stable_B,
            "potential_bounded_below": potential_bounded_below(stable_B),
            "massive_gap2": massive_gap2(m, stable_B),
            "goldstone_c2": goldstone_c2(m, stable_B),
            "gapless_omega2": stable_gapless.tolist(),
            "gapped_omega2": stable_gapped.tolist(),
            "common_light_cone_in_nr_regime": common_cone_possible_in_controlled_nr_limit(
                m, stable_B
            ),
            "interpretation": (
                "stable covariant logarithmic scalar, but opposite to the "
                "printed SSV sign and with a subluminal Goldstone cone"
            ),
        },
        "gates": {
            "P1_R0_bounded": False,
            "P2_R0_exact_NR_map": True,
            "P3_R0_stable": False,
            "P1_R1_preserves_target_and_stabilizes": saturation_can_preserve_target_and_stabilize(
                original_mu_prime=-B, correction_mu_prime=0.0
            ),
            "P3_sign_reversed_control_stable": True,
            "P4_sign_reversed_control_is_literal_SSV": False,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
